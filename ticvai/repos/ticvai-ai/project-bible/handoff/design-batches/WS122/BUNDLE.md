# WS122 — AI Governance board 2

**10 screens · 25 operations · 34 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `AI_APPROVE, AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-529` | AI Human Oversight Command Center | commandCentre | 2 | 0 | — |
| `ADM-530` | AI Approval Requirement & Routing Configuration | listDetail | 6 | 1 | — |
| `ADM-531` | AI Approval Review Workspace | configEditor | 3 | 0 | — |
| `ADM-532` | Conditional Approval & Approval Conditions | listDetail | 4 | 0 | — |
| `ADM-533` | Human Review, Challenge & AI Clarification Workspace | listDetail | 3 | 0 | — |
| `ADM-534` | Escalation, Delegation & Approval SLA Management | listDetail | 6 | 0 | — |
| `ADM-535` | Live AI Execution Oversight & Human Intervention | listDetail | 5 | 2 | — |
| `ADM-536` | Human Override & Manual Control Center | listDetail | 4 | 0 | — |
| `ADM-537` | Approval & Intervention History / Decision Timeline | listDetail | 2 | 0 | — |
| `ADM-538` | Human Oversight Workflow Simulator & Readiness Center | configEditor | 2 | 0 | — |

## Thin screens in this batch

**ADM-531, ADM-533, ADM-536, ADM-537 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-529",
  "name": "AI Human Oversight Command Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "1",
   "page": 30
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-human-oversight-command-center-adm-529",
   "component": "apps/ticvai-web/src/routes/platform/AiHumanOversightCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-530",
    "ADM-531",
    "ADM-532",
    "ADM-533",
    "ADM-534",
    "ADM-535",
    "ADM-536",
    "ADM-537",
    "ADM-538"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-530",
     "trigger": "AI Approval Requirement & Routing Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-531",
     "trigger": "AI Approval Review Workspace",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-532",
     "trigger": "Conditional Approval & Approval Conditions",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-533",
     "trigger": "Human Review, Challenge & AI Clarification Workspace",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-534",
     "trigger": "Escalation, Delegation & Approval SLA Management",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-535",
     "trigger": "Live AI Execution Oversight & Human Intervention",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-536",
     "trigger": "Human Override & Manual Control Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-537",
     "trigger": "Approval & Intervention History / Decision Timeline",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-538",
     "trigger": "Human Oversight Workflow Simulator & Readiness Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide one central operational view of all AI activities requiring human oversight across TICVAI. This should become the control room for AI actions waiting for human intervention.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search human oversight",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "AI Capability",
        "Module",
        "Risk",
        "Approver",
        "Status",
        "Environment",
        "Date",
        "SLA"
       ],
       "notes": "The pack filters this screen by tenant, venue, ai capability, module, risk, approver and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Pending AI Approvals",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "High-Risk Reviews",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Critical Reviews",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Awaiting Additional Approver",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Conditional Approvals",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Requested Changes",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Escalated Cases",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Overdue Reviews",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Active AI Executions Under Oversight",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Human Interventions Today",
       "provenance": "pack AI_Governance_Reference.pdf, page 30 §Header KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The human oversight list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the human oversight untouched.",
   "emptyFirstRun": "No human oversight yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the human oversight are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listProposedActions",
    "contract": "ai",
    "purpose": "What the assistant has proposed and nobody has decided",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-529",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-529"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 30. 0 of 10 labels bound to a contract property; 20 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "planId",
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
  "id": "ADM-530",
  "name": "AI Approval Requirement & Routing Configuration",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "2",
   "page": 31
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-approval-requirement-routing-configuration-adm-530",
   "component": "apps/ticvai-web/src/routes/platform/AiApprovalRequirementRoutingConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-529"
   ],
   "exitTo": [
    "ADM-529"
   ],
   "transitions": [
    {
     "to": "ADM-529",
     "trigger": "Back to AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Translate Board 1 governance decisions into the correct human approval workflow.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 11 actions on this screen and the screen declares 0 operations.** Unserved: Single Approval, Sequential Approval, Parallel Approval, Conditional Approval, Risk-Based Approval, → Commercial Manager, → Commercial Manager + General Manager, → Commercial Director + General Manager …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Governance_Reference.pdf, page 31 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 31"
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
       "label": "Single Approval",
       "provenance": "pack AI_Governance_Reference.pdf, page 31 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Sequential Approval",
       "provenance": "pack AI_Governance_Reference.pdf, page 31 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Parallel Approval",
       "provenance": "pack AI_Governance_Reference.pdf, page 31 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Conditional Approval",
       "provenance": "pack AI_Governance_Reference.pdf, page 31 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Risk-Based Approval",
       "provenance": "pack AI_Governance_Reference.pdf, page 31 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "→ Commercial Manager",
       "provenance": "pack AI_Governance_Reference.pdf, page 31 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "→ Commercial Manager + General Manager",
       "provenance": "pack AI_Governance_Reference.pdf, page 31 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "→ Commercial Director + General Manager",
       "provenance": "pack AI_Governance_Reference.pdf, page 31 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save approval matrix",
       "operation": "setApprovalMatrix",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "secondaryButton",
       "label": "Test a routing",
       "operation": "evaluateApprovalRequirement",
       "notes": "Evaluates a sample AI action (kind `aiRecommendation`, amount, scope) against the matrix and shows who would approve it.",
       "provenance": "29 September pass (group A)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Approval matrix for AI actions",
       "operation": "listApprovalMatrices",
       "notes": "**AI actions route through the shared approval matrix** (18 September minutes, M18-02), kind `aiRecommendation`: an approver is authorised up to a limit and anything above it escalates.",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval requirement routing list.",
   "error": "Could not load. Names which read failed and leaves the approval requirement routing untouched.",
   "emptyFirstRun": "No approval requirement routing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval requirement routing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createAiGovernancePolicyDraft",
    "contract": "ai",
    "purpose": "Draft a governance policy, or a new version of one",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiGovernancePolicyVersions",
    "contract": "ai",
    "purpose": "Governance policies and their versions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiTools",
    "contract": "ai",
    "purpose": "The tool registry",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listApprovalMatrices",
    "contract": "approvals",
    "purpose": "The matrices AI actions route through",
    "trigger": "onLoad",
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Thresholds and levels for AI actions",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalMatrices"
    ],
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "evaluateApprovalRequirement",
    "contract": "approvals",
    "purpose": "Who would approve this AI action",
    "trigger": "onAction",
    "provenance": "29 September pass (group A)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-530",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-530"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 31. 0 of 0 labels bound to a contract property; 11 of 60 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetApprovalMatrix",
    "component": "modal",
    "trigger": "Save approval matrix",
    "body": "**Collects the matrix for kind `aiRecommendation`** before `setApprovalMatrix` is called: levels, the value range each approver may approve, and the escalation above it. Dismissing sends nothing.",
    "confirm": {
     "label": "Save approval matrix",
     "operation": "setApprovalMatrix"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "levels",
      "thresholds"
     ]
    },
    "provenance": "29 September pass (group A)"
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
  "id": "ADM-531",
  "name": "AI Approval Review Workspace",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "3",
   "page": 33
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-approval-review-workspace-adm-531",
   "component": "apps/ticvai-web/src/routes/platform/AiApprovalReviewWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-529"
   ],
   "exitTo": [
    "ADM-529"
   ],
   "transitions": [
    {
     "to": "ADM-529",
     "trigger": "Back to AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration Current Proposed) and no display directory — it is settings, not a population",
  "purpose": "Give the human approver enough information to make an informed decision without having to navigate across many TICVAI modules. This should be one of the strongest screens in the board.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Adult Weekend Price AED 140 AED 150",
       "provenance": "pack AI_Governance_Reference.pdf, page 33 §Configuration Current Proposed"
      },
      {
       "kind": "textField",
       "label": "Effective Date Current 1 Oct 2026",
       "provenance": "pack AI_Governance_Reference.pdf, page 33 §Configuration Current Proposed"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval review configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval review untouched.",
   "emptyFirstRun": "No approval review configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "simulateActionPlan",
    "contract": "ai",
    "purpose": "Validate and simulate a plan without changing anything",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideProposedAction",
    "contract": "ai",
    "purpose": "Approve or reject a proposal (tier 1 here; tier 2 routed to Approvals)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-531",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-531"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 33. 0 of 0 labels bound to a contract property; 2 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "actionId",
     "from": "navigation"
    },
    {
     "name": "planId",
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
  "id": "ADM-532",
  "name": "Conditional Approval & Approval Conditions",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "4",
   "page": 35
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/conditional-approval-approval-conditions-adm-532",
   "component": "apps/ticvai-web/src/routes/platform/ConditionalApprovalApprovalConditions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-529"
   ],
   "exitTo": [
    "ADM-529"
   ],
   "transitions": [
    {
     "to": "ADM-529",
     "trigger": "Back to AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow humans to approve an AI action subject to explicit conditions rather than treating approval as simply Yes/No.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 35"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 35"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getActionPlan",
       "notes": "One record, read-only.",
       "operation": "getActionPlan"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "decideProposedAction",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideProposedAction"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Approval condition for this action",
       "operation": "evaluateApprovalRequirement",
       "notes": "**Conditional authority** (M18-02): the approver's limit for this kind and amount, and whether the action is within it or must escalate.",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "dataTable",
       "label": "Threshold ranges",
       "operation": "listApprovalMatrices",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The conditional approval approval list.",
   "error": "Could not load. Names which read failed and leaves the conditional approval approval untouched.",
   "emptyFirstRun": "No conditional approval approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the conditional approval approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideProposedAction",
    "contract": "ai",
    "purpose": "Approve or reject a proposal (tier 1 here; tier 2 routed to Approvals)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "evaluateApprovalRequirement",
    "contract": "approvals",
    "purpose": "Whether this action is within the approver's limit",
    "trigger": "onLoad",
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "listApprovalMatrices",
    "contract": "approvals",
    "purpose": "The threshold ranges",
    "trigger": "onLoad",
    "provenance": "29 September pass (group A)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-532",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-532"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 35. 0 of 0 labels bound to a contract property; 0 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "actionId",
     "from": "navigation"
    },
    {
     "name": "planId",
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
  "id": "ADM-533",
  "name": "Human Review, Challenge & AI Clarification Workspace",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "5",
   "page": 36
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/human-review-challenge-ai-clarification-workspace-adm-533",
   "component": "apps/ticvai-web/src/routes/platform/HumanReviewChallengeAiClarificationWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-529"
   ],
   "exitTo": [
    "ADM-529"
   ],
   "transitions": [
    {
     "to": "ADM-529",
     "trigger": "Back to AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow the approver to question the AI proposal before making a decision. Human oversight should not mean simply clicking Approve.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Governance_Reference.pdf, page 36 §Show"
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
       "label": "Every human review challenge",
       "columns": [
        "Proposed Action",
        "Business Context",
        "Risk",
        "Impact",
        "AI Recommendation",
        "Validation",
        "Alternatives",
        "Ask AI"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Governance_Reference.pdf, page 36 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected human review challenge",
       "bindsTo": null,
       "columns": [
        "Proposed Action",
        "Business Context",
        "Risk",
        "Impact",
        "AI Recommendation",
        "Validation",
        "Alternatives",
        "Ask AI"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Other Example Questions”, “Important Requirement”, “If evidence is unavailable”.",
       "provenance": "pack AI_Governance_Reference.pdf, page 36 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The human review challenge list.",
   "error": "Could not load. Names which read failed and leaves the human review challenge untouched.",
   "emptyFirstRun": "No human review challenge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the human review challenge are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "overrideAiDecision",
    "contract": "ai",
    "purpose": "Override an AI decision",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "sendAiMessage",
    "contract": "ai",
    "purpose": "Ask the assistant",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Proposed Action",
    "Business Context",
    "Risk",
    "Impact",
    "AI Recommendation",
    "Validation"
   ],
   "params": [
    {
     "name": "conversationId",
     "from": "navigation"
    },
    {
     "name": "decisionRecordId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-533",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-533"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 36. 0 of 8 labels bound to a contract property; 8 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-534",
  "name": "Escalation, Delegation & Approval SLA Management",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "6",
   "page": 37
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/escalation-delegation-approval-sla-management-adm-534",
   "component": "apps/ticvai-web/src/routes/platform/EscalationDelegationApprovalSlaManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-529"
   ],
   "exitTo": [
    "ADM-529"
   ],
   "transitions": [
    {
     "to": "ADM-529",
     "trigger": "Back to AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Ensure AI approvals do not remain indefinitely pending and provide controlled routing when approvers are unavailable or additional authority is required.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 37"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 37"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getActionPlan",
       "notes": "One record, read-only.",
       "operation": "getActionPlan"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listProposedActions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "operation": "listProposedActions"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Delegations in force",
       "operation": "listApprovalDelegations",
       "provenance": "29 September pass (group A)"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "operation": "escalateApprovalRequest",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "secondaryButton",
       "label": "Delegate",
       "operation": "createApprovalDelegation",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "secondaryButton",
       "label": "Save approval SLA",
       "operation": "setApprovalSlaPolicy",
       "notes": "Escalation, delegation and SLA apply to AI actions as to any approval (M18-02).",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The escalation delegation approval list.",
   "error": "Could not load. Names which read failed and leaves the escalation delegation approval untouched.",
   "emptyFirstRun": "No escalation delegation approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the escalation delegation approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listProposedActions",
    "contract": "ai",
    "purpose": "What the assistant has proposed and nobody has decided",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listApprovalDelegations",
    "contract": "approvals",
    "purpose": "Who is acting for whom",
    "trigger": "onLoad",
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "escalateApprovalRequest",
    "contract": "approvals",
    "purpose": "Send an AI action to the next level",
    "trigger": "onAction",
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "createApprovalDelegation",
    "contract": "approvals",
    "purpose": "Delegate approval authority",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalDelegations"
    ],
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "setApprovalSlaPolicy",
    "contract": "approvals",
    "purpose": "The SLA and its escalation",
    "trigger": "onAction",
    "provenance": "29 September pass (group A)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-534",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-534"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 0 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "planId",
     "from": "navigation"
    },
    {
     "name": "requestId",
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
  "id": "ADM-535",
  "name": "Live AI Execution Oversight & Human Intervention",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "7",
   "page": 39
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/live-ai-execution-oversight-human-intervention-adm-535",
   "component": "apps/ticvai-web/src/routes/platform/LiveAiExecutionOversightHumanIntervention.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-529"
   ],
   "exitTo": [
    "ADM-529"
   ],
   "transitions": [
    {
     "to": "ADM-529",
     "trigger": "Back to AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§High-impact intervention should show) and no metric row",
  "purpose": "Allow authorized humans to monitor and intervene after an AI-driven action has been approved and entered execution. This is different from approval.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Governance_Reference.pdf, page 39 §High-impact intervention should show"
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
       "label": "Every live execution oversight",
       "columns": [
        "Impact of Pausing",
        "Completed objects remain",
        "4 actions will remain pending",
        "No active transaction affected",
        "Emergency Stop",
        "Emergency Stop AI Execution",
        "Authorized Role",
        "Reason",
        "Confirmation",
        "Audit Record"
       ],
       "bindsTo": null,
       "operation": "getActionPlan",
       "provenance": "pack AI_Governance_Reference.pdf, page 39 §High-impact intervention should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected live execution oversight",
       "bindsTo": null,
       "columns": [
        "Impact of Pausing",
        "Completed objects remain",
        "4 actions will remain pending",
        "No active transaction affected",
        "Emergency Stop",
        "Emergency Stop AI Execution",
        "Authorized Role",
        "Reason",
        "Confirmation",
        "Audit Record"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Approval answers”, “Step Action Module Status”, “Administrator notices”.",
       "provenance": "pack AI_Governance_Reference.pdf, page 39 §High-impact intervention should show",
       "operation": "getActionPlan"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Pause",
       "operation": "pauseActionPlan",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeActionPlan",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel plan",
       "operation": "cancelActionPlan",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "destructiveButton",
       "label": "Roll back",
       "operation": "rollbackActionPlan",
       "notes": "**Rollback on partial failure** (21 September minutes, M21-12): plans the compensating steps in reverse dependency order, for approval like any plan.",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The live execution oversight list.",
   "error": "Could not load. Names which read failed and leaves the live execution oversight untouched.",
   "emptyFirstRun": "No live execution oversight yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the live execution oversight are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "pauseActionPlan",
    "contract": "ai",
    "purpose": "Pause an executing plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "resumeActionPlan",
    "contract": "ai",
    "purpose": "Resume a paused plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "cancelActionPlan",
    "contract": "ai",
    "purpose": "Cancel a plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "rollbackActionPlan",
    "contract": "ai",
    "purpose": "Plan the rollback of a partly executed plan",
    "trigger": "onAction",
    "provenance": "29 September pass (group A)"
   }
  ],
  "entryState": {
   "preloaded": [
    "Impact of Pausing",
    "Completed objects remain",
    "4 actions will remain pending",
    "No active transaction affected",
    "Emergency Stop",
    "Emergency Stop AI Execution"
   ],
   "params": [
    {
     "name": "planId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-535",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-535"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 39. 0 of 10 labels bound to a contract property; 10 of 54 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "confirmCancelActionPlan",
    "component": "confirmDialog",
    "trigger": "Cancel plan",
    "body": "**Names the plan, the steps already executed and what stays applied**: cancelling stops the remaining steps; it does not undo the executed ones (that is Roll back).",
    "provenance": "29 September pass (group A)"
   },
   {
    "id": "confirmRollbackActionPlan",
    "component": "confirmDialog",
    "trigger": "Roll back",
    "body": "**Names each executed step and its compensation**, and that the rollback plan goes for approval before it runs.",
    "provenance": "29 September pass (group A)"
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
  "id": "ADM-536",
  "name": "Human Override & Manual Control Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "8",
   "page": 41
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/human-override-manual-control-center-adm-536",
   "component": "apps/ticvai-web/src/routes/platform/HumanOverrideManualControlCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-529"
   ],
   "exitTo": [
    "ADM-529"
   ],
   "transitions": [
    {
     "to": "ADM-529",
     "trigger": "Back to AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide controlled mechanisms for humans to override an AI recommendation or take control when AI output is inappropriate. Human override should always be possible where governance requires it.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 41"
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
       "impliedBy": "pauseAiCapability",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "pauseAiCapability"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The human override manual list.",
   "error": "Could not load. Names which read failed and leaves the human override manual untouched.",
   "emptyFirstRun": "No human override manual yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the human override manual are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "pauseAiCapability",
    "contract": "ai",
    "purpose": "Stop a capability now",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "resumeAiCapability",
    "contract": "ai",
    "purpose": "Resume a paused capability",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "pauseActionPlan",
    "contract": "ai",
    "purpose": "Pause an executing plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "overrideAiDecision",
    "contract": "ai",
    "purpose": "Override an AI decision",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-536",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-536"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 41. 0 of 0 labels bound to a contract property; 0 of 54 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "capabilityKey",
     "from": "navigation"
    },
    {
     "name": "decisionRecordId",
     "from": "navigation"
    },
    {
     "name": "planId",
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
  "id": "ADM-537",
  "name": "Approval & Intervention History / Decision Timeline",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "9",
   "page": 42
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-intervention-history-decision-timeline-adm-537",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalInterventionHistoryDecisionTimeline.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-529"
   ],
   "exitTo": [
    "ADM-529"
   ],
   "transitions": [
    {
     "to": "ADM-529",
     "trigger": "Back to AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide complete operational history of human involvement in AI activity. This is the human-oversight timeline; Board 3 will later provide deeper enterprise AI explainability and audit.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 42"
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
       "label": "Search approval intervention history",
       "provenance": "pack AI_Governance_Reference.pdf, page 42 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "AI Capability",
        "User",
        "Approver",
        "Module",
        "Decision",
        "Risk",
        "Venue",
        "Tenant",
        "Date"
       ],
       "notes": "The pack filters this screen by ai capability, user, approver, module, decision, risk and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack AI_Governance_Reference.pdf, page 42 §Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval intervention history list.",
   "error": "Could not load. Names which read failed and leaves the approval intervention history untouched.",
   "emptyFirstRun": "No approval intervention history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval intervention history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchAiDecisions",
    "contract": "ai",
    "purpose": "Find AI decisions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-537",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-537"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 42. 0 of 9 labels bound to a contract property; 9 of 63 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionRecordId",
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
  "id": "ADM-538",
  "name": "Human Oversight Workflow Simulator & Readiness Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "2",
   "number": "10",
   "page": 44
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/human-oversight-workflow-simulator-readiness-center-adm-538",
   "component": "apps/ticvai-web/src/routes/platform/HumanOversightWorkflowSimulatorReadinessCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-529"
   ],
   "exitTo": [
    "ADM-529"
   ],
   "transitions": [
    {
     "to": "ADM-529",
     "trigger": "Back to AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Board 1 defines) and no display directory — it is settings, not a population",
  "purpose": "Allow Soft Labs/TICVAI administrators to test the entire human-in-the-loop workflow before activating it in production.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: but Operations Assistant lacks Pricing approval rights,. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Governance_Reference.pdf, page 44 §Operations Assistant"
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
       "label": "Risk",
       "provenance": "pack AI_Governance_Reference.pdf, page 44 §Board 1 defines"
      },
      {
       "kind": "selectField",
       "label": "Autonomy",
       "provenance": "pack AI_Governance_Reference.pdf, page 44 §Board 1 defines"
      },
      {
       "kind": "selectField",
       "label": "AI permissions",
       "provenance": "pack AI_Governance_Reference.pdf, page 44 §Board 1 defines"
      },
      {
       "kind": "selectField",
       "label": "Data usage",
       "provenance": "pack AI_Governance_Reference.pdf, page 44 §Board 1 defines"
      },
      {
       "kind": "selectField",
       "label": "Policy",
       "provenance": "pack AI_Governance_Reference.pdf, page 44 §Board 1 defines"
      },
      {
       "kind": "selectField",
       "label": "Governance decision",
       "provenance": "pack AI_Governance_Reference.pdf, page 44 §Board 1 defines"
      },
      {
       "kind": "textField",
       "label": "Important Boundary — Owning Modules",
       "provenance": "pack AI_Governance_Reference.pdf, page 44 §Board 1 defines"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "but Operations Assistant lacks Pricing approval rights,",
       "provenance": "pack AI_Governance_Reference.pdf, page 44 §Operations Assistant"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The human oversight workflow configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the human oversight workflow untouched.",
   "emptyFirstRun": "No human oversight workflow configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "simulateAiGovernancePolicy",
    "contract": "ai",
    "purpose": "Test a draft policy before it is published",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "simulateActionPlan",
    "contract": "ai",
    "purpose": "Validate and simulate a plan without changing anything",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-538",
   "workshopBoard": "wireframes/WS15 AI Governance Board 2.dc.html#adm-538"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 44. 0 of 0 labels bound to a contract property; 8 of 269 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "planId",
     "from": "navigation"
    },
    {
     "name": "versionId",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "cancelActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/cancel",
  "contract": "ai",
  "summary": "Cancel a plan",
  "permission": "AI_USE",
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
  "responds": "AiActionPlan"
 },
 "createAiGovernancePolicyDraft": {
  "method": "POST",
  "path": "/governance/policy-drafts",
  "contract": "ai",
  "summary": "Draft a governance policy, or a new version of one",
  "permission": "AI_CONFIGURE",
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
  "responds": "AiGovernancePolicyVersion"
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
 "decideProposedAction": {
  "method": "POST",
  "path": "/proposed-actions/{actionId}/decide",
  "contract": "ai",
  "summary": "Approve or reject a proposal",
  "permission": "AI_USE",
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
  "responds": "ProposedAction"
 },
 "escalateApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/escalate",
  "contract": "approvals",
  "summary": "Move it up a level",
  "permission": "APPROVAL_REQUEST",
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
 "evaluateApprovalRequirement": {
  "method": "POST",
  "path": "/approval-requests/evaluate",
  "contract": "approvals",
  "summary": "Does this need approval, and from whom",
  "permission": "APPROVAL_VIEW",
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
  "responds": "ApprovalRequirement"
 },
 "getActionPlan": {
  "method": "GET",
  "path": "/action-plans/{planId}",
  "contract": "ai",
  "summary": "A plan with its steps",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiActionPlanDetail"
 },
 "getAiDecisionTrace": {
  "method": "GET",
  "path": "/decision-records/{decisionRecordId}/trace",
  "contract": "ai",
  "summary": "The full trace of a decision",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "depth",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiDecisionTrace"
 },
 "listAiGovernancePolicyVersions": {
  "method": "GET",
  "path": "/governance/policy-versions",
  "contract": "ai",
  "summary": "Governance policies and their versions",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "policyId",
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
 "listAiTools": {
  "method": "GET",
  "path": "/tools",
  "contract": "ai",
  "summary": "The tool registry",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "targetContract",
    "in": "query",
    "required": null
   },
   {
    "name": "effect",
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
 "listProposedActions": {
  "method": "GET",
  "path": "/proposed-actions",
  "contract": "ai",
  "summary": "What the assistant has proposed and nobody has decided",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProposedAction"
 },
 "overrideAiDecision": {
  "method": "POST",
  "path": "/decision-records/{decisionRecordId}/override",
  "contract": "ai",
  "summary": "Override an AI decision",
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
  "responds": "AiIntervention"
 },
 "pauseActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/pause",
  "contract": "ai",
  "summary": "Pause an executing plan",
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
  "responds": "AiActionPlan"
 },
 "pauseAiCapability": {
  "method": "POST",
  "path": "/governance/capabilities/{capabilityKey}/pause",
  "contract": "ai",
  "summary": "Stop a capability now",
  "permission": "AI_CONFIGURE",
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
  "responds": "AiCapabilityRegistration"
 },
 "resumeActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/resume",
  "contract": "ai",
  "summary": "Resume a paused plan",
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
  "responds": "AiActionPlan"
 },
 "resumeAiCapability": {
  "method": "POST",
  "path": "/governance/capabilities/{capabilityKey}/resume",
  "contract": "ai",
  "summary": "Resume a paused capability",
  "permission": "AI_APPROVE",
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
  "responds": "AiCapabilityRegistration"
 },
 "rollbackActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/rollback",
  "contract": "ai",
  "summary": "Plan a rollback",
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
  "responds": null
 },
 "searchAiDecisions": {
  "method": "GET",
  "path": "/decision-records",
  "contract": "ai",
  "summary": "Find AI decisions",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "capabilityKey",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "subjectRef",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "traceId",
    "in": "query",
    "required": null
   },
   {
    "name": "policyVersion",
    "in": "query",
    "required": null
   },
   {
    "name": "modelVersion",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
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
 "sendAiMessage": {
  "method": "POST",
  "path": "/conversations/{conversationId}/messages",
  "contract": "ai",
  "summary": "Ask",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiMessage"
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
 "setApprovalSlaPolicy": {
  "method": "PUT",
  "path": "/approval-sla-policies",
  "contract": "approvals",
  "summary": "How long a decision may take, and what happens when it does not",
  "permission": "APPROVAL_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ApprovalSlaPolicy",
  "responds": "ApprovalSlaPolicy"
 },
 "simulateActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/simulate",
  "contract": "ai",
  "summary": "Validate and simulate a plan without changing anything",
  "permission": "AI_USE",
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
  "responds": "AiActionPlanDetail"
 },
 "simulateAiGovernancePolicy": {
  "method": "POST",
  "path": "/governance/policy-versions/{versionId}/simulate",
  "contract": "ai",
  "summary": "Test a draft policy before it is published",
  "permission": "AI_CONFIGURE",
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
  "responds": "AiPolicySimulation"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiActionPlan": {
  "type": "object",
  "x-ticvai-persistence": "ai.action_plan",
  "description": "**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).",
  "required": [
   "origin",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "origin": {
    "type": "string",
    "enum": [
     "configurationSession",
     "generateConfiguration",
     "assistant",
     "riskCase",
     "operationalRequirement",
     "rollback"
    ]
   },
   "originRef": {
    "type": "string",
    "nullable": true
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "validated",
     "simulated",
     "awaitingApproval",
     "approved",
     "executing",
     "paused",
     "completed",
     "partiallyCompleted",
     "failed",
     "compensated",
     "cancelled",
     "rolledBack"
    ],
    "readOnly": true
   },
   "autonomyLevel": {
    "$ref": "#/components/schemas/AiAutonomyLevel"
   },
   "approvalTier": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request, where tier 2 or the matrix caught the plan."
   },
   "proposedActionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.proposed_action",
    "description": "The `ai.proposed_action` the plan is presented as for a decision."
   },
   "changeSetHash": {
    "type": "string",
    "readOnly": true
   },
   "governanceOutcome": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiGovernanceOutcome"
     }
    ],
    "readOnly": true
   },
   "policyVersionRef": {
    "type": "string",
    "readOnly": true,
    "description": "The governance policy version that decided it."
   },
   "simulation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true,
    "description": "Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."
   },
   "partialCompletionAllowed": {
    "type": "boolean",
    "default": false,
    "description": "Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."
   },
   "rollbackOfPlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.action_plan"
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiActionPlanDetail": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.action_plan with its ai.action_step rows",
  "description": "A plan with its steps in DAG order.",
  "required": [
   "plan",
   "steps"
  ],
  "properties": {
   "plan": {
    "$ref": "#/components/schemas/AiActionPlan"
   },
   "steps": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiActionStep"
    }
   }
  }
 },
 "AiActionStep": {
  "type": "object",
  "x-ticvai-persistence": "ai.action_step",
  "description": "One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).",
  "required": [
   "planId",
   "stepNumber",
   "toolKey",
   "targetContract",
   "targetOperation",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.action_plan"
   },
   "stepNumber": {
    "type": "integer",
    "minimum": 1
   },
   "dependsOn": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 1
    },
    "description": "Step numbers that must succeed first. The plan is a DAG."
   },
   "toolKey": {
    "type": "string"
   },
   "targetContract": {
    "type": "string"
   },
   "targetOperation": {
    "type": "string"
   },
   "contractVersion": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body of `targetOperation`, validated against it before the plan is approved."
   },
   "provenance": {
    "$ref": "#/components/schemas/AiProvenance"
   },
   "idempotencyKey": {
    "type": "string",
    "readOnly": true
   },
   "targetObjectRef": {
    "type": "string",
    "nullable": true
   },
   "targetObjectVersion": {
    "type": "string",
    "nullable": true,
    "description": "The version the step was planned against. A different version at execution is drift."
   },
   "reversible": {
    "type": "boolean"
   },
   "compensation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "validated",
     "running",
     "succeeded",
     "failed",
     "compensated",
     "skipped",
     "paused"
    ],
    "readOnly": true
   },
   "attempts": {
    "type": "integer",
    "minimum": 0,
    "maximum": 3,
    "readOnly": true,
    "description": "Bounded at 3 (AIC-135)."
   },
   "lastError": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "resultRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The owning service's response: success is its answer, not a model's judgement (AIC-097)."
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
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
 "AiAutonomyLevel": {
  "type": "integer",
  "minimum": 0,
  "maximum": 4,
  "description": "**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."
 },
 "AiCapabilityFamily": {
  "type": "string",
  "enum": [
   "gatewayAndModels",
   "governance",
   "actionPipeline",
   "knowledgeRetrieval",
   "assistants",
   "analyticsInsights",
   "configurationAssistant",
   "forecasting",
   "anomalyDetection",
   "riskIntelligence",
   "recommendations",
   "decisionRecords",
   "operationsEvaluation",
   "residencyPrivacy"
  ],
  "description": "The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."
 },
 "AiCapabilityRegistration": {
  "type": "object",
  "x-ticvai-persistence": "ai.capability",
  "description": "**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).",
  "required": [
   "capabilityKey",
   "family",
   "riskClass",
   "autonomyLevel"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "capabilityKey": {
    "type": "string",
    "description": "Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."
   },
   "family": {
    "$ref": "#/components/schemas/AiCapabilityFamily"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal",
    "description": "The accountable business owner (AIC-144)."
   },
   "businessFunction": {
    "type": "string",
    "nullable": true
   },
   "riskClass": {
    "$ref": "#/components/schemas/AiRiskClass"
   },
   "autonomyCeiling": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiAutonomyLevel"
     }
    ],
    "readOnly": true,
    "description": "The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."
   },
   "autonomyLevel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiAutonomyLevel"
     }
    ],
    "description": "The level in force at this scope. At most `autonomyCeiling`."
   },
   "dataCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Data categories the capability reads (ADM-524)."
   },
   "lifecycle": {
    "type": "object",
    "description": "Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.",
    "properties": {
     "development": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     },
     "staging": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     },
     "production": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     }
    }
   },
   "degradationMode": {
    "type": "string",
    "enum": [
     "rulesOnly",
     "searchOnly",
     "humanHandoff",
     "hidden",
     "failOpen",
     "lastPublished"
    ],
    "description": "What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "paused"
    ],
    "readOnly": true,
    "description": "Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."
   },
   "pausedReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "pausedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "updatedAt": {
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
 "AiDecisionRecord": {
  "type": "object",
  "x-ticvai-persistence": "ai.decision_record",
  "description": "**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.",
  "required": [
   "traceId",
   "capabilityKey",
   "outcome",
   "recordHash"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "traceId": {
    "type": "string"
   },
   "capabilityKey": {
    "type": "string"
   },
   "task": {
    "type": "string",
    "nullable": true
   },
   "subjectKind": {
    "type": "string",
    "nullable": true
   },
   "subjectRef": {
    "type": "string",
    "nullable": true
   },
   "inputsRef": {
    "type": "string",
    "nullable": true,
    "description": "Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."
   },
   "evidence": {
    "$ref": "#/components/schemas/AiEvidenceItemList"
   },
   "producer": {
    "type": "string",
    "nullable": true
   },
   "modelVersion": {
    "type": "string",
    "nullable": true
   },
   "promptTemplateVersion": {
    "type": "string",
    "nullable": true
   },
   "featureSetVersion": {
    "type": "string",
    "nullable": true
   },
   "knowledgeVersion": {
    "type": "string",
    "nullable": true
   },
   "ruleVersions": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "governanceOutcome": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiGovernanceOutcome"
     }
    ],
    "nullable": true
   },
   "policyVersion": {
    "type": "string",
    "nullable": true
   },
   "approvals": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Approval requests and their decisions."
   },
   "humanDecision": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Override or intervention, where a person changed the outcome."
   },
   "executionResult": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "outcomeRef": {
    "type": "string",
    "nullable": true,
    "description": "The business outcome it links to (an order, a published version, a closed case)."
   },
   "outcome": {
    "type": "string",
    "enum": [
     "answered",
     "refused",
     "allowed",
     "blocked",
     "executed",
     "failed",
     "approvedThenFailed",
     "published",
     "suggested"
    ],
    "description": "`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."
   },
   "annotations": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "byPrincipalId": {
       "type": "string",
       "format": "uuid"
      },
      "note": {
       "type": "string"
      }
     }
    },
    "readOnly": true,
    "description": "Corrections, appended; the original fields are never edited."
   },
   "previousHash": {
    "type": "string",
    "readOnly": true
   },
   "recordHash": {
    "type": "string",
    "readOnly": true
   },
   "createdAt": {
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
 "AiDecisionTrace": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.decision_record with the rows it references",
  "description": "**The full trace of one decision** (ADM-540..546): record, evidence, candidates and rules, model and runtime, governance and approvals, execution and business outcome. Depth is gated by permission (AIC-195).",
  "required": [
   "record"
  ],
  "properties": {
   "record": {
    "$ref": "#/components/schemas/AiDecisionRecord"
   },
   "depth": {
    "type": "string",
    "enum": [
     "business",
     "governance",
     "technical"
    ]
   },
   "explanation": {
    "type": "string",
    "description": "Built from structured evidence, never a model's chain of thought (AIC-192)."
   },
   "activity": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiInteraction"
    },
    "description": "The model calls behind it (`technical` depth)."
   },
   "plan": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiActionPlanDetail"
     }
    ],
    "nullable": true
   },
   "interventions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiIntervention"
    }
   },
   "chainVerified": {
    "type": "boolean",
    "description": "The hash chain around this record verifies."
   }
  }
 },
 "AiEvidenceItemList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "The evidence of one decision record, stored with it.",
  "items": {
   "$ref": "#/components/schemas/AiEvidenceItem"
  }
 },
 "AiGovernanceOutcome": {
  "type": "string",
  "enum": [
   "allow",
   "allowWithConditions",
   "prepareOnly",
   "approvalRequired",
   "escalate",
   "block"
  ],
  "description": "What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."
 },
 "AiGovernancePolicyVersion": {
  "type": "object",
  "x-ticvai-persistence": "ai.governance_policy_version",
  "description": "One version of a governance policy. **Published versions are never edited**: a change is a new version, and the previous one becomes `superseded` in the same transaction (AIC-165).",
  "required": [
   "policyId",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "policyId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.governance_policy"
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "simulated",
     "published",
     "superseded"
    ]
   },
   "rules": {
    "$ref": "#/components/schemas/AiGovernanceRuleList"
   },
   "changeNote": {
    "type": "string",
    "nullable": true
   },
   "simulationSummary": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true,
    "description": "The last `simulateAiGovernancePolicy` result: decisions that would change, by outcome."
   },
   "draftedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "supersededAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiGovernanceRule": {
  "type": "object",
  "x-ticvai-persistence": "none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList",
  "description": "One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).",
  "required": [
   "effect"
  ],
  "properties": {
   "effect": {
    "$ref": "#/components/schemas/AiGovernanceOutcome"
   },
   "capabilityKeys": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Registered capabilities it applies to. Empty means every capability the policy names."
   },
   "actions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "read",
      "analyze",
      "recommend",
      "generate",
      "prepare",
      "create",
      "modify",
      "publish",
      "execute",
      "delete"
     ]
    },
    "description": "ADM-523: what AI may do, from reading to executing."
   },
   "dataCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Permitted purposes for those categories (AIC-156, AIR-182)."
   },
   "maxAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Above this value the effect escalates one step (for example to `approvalRequired`)."
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Roles the rule applies to; empty means every role."
   },
   "environments": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "development",
      "sandbox",
      "staging",
      "production"
     ]
    },
    "description": "ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."
   },
   "conditions": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."
   }
  }
 },
 "AiGovernanceRuleList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "The rules of one policy version, stored with the version as one `jsonb` column.",
  "items": {
   "$ref": "#/components/schemas/AiGovernanceRule"
  }
 },
 "AiInteraction": {
  "type": "object",
  "x-ticvai-persistence": "ai.activity",
  "required": [
   "id",
   "principalId",
   "capability",
   "outcome",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "conversationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "audience": {
    "type": "string",
    "enum": [
     "staff",
     "guest"
    ],
    "description": "**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"
   },
   "billableToTenantId": {
    "type": "string",
    "format": "uuid",
    "description": "Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"
   },
   "scopePath": {
    "type": "string"
   },
   "capability": {
    "type": "string"
   },
   "prompt": {
    "type": "string"
   },
   "response": {
    "type": "string"
   },
   "sources": {
    "$ref": "#/components/schemas/AiSourceList"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "answered",
     "refused",
     "applied",
     "rejected",
     "failed"
    ]
   },
   "refusalReason": {
    "type": "string",
    "nullable": true
   },
   "provider": {
    "$ref": "#/components/schemas/AiProviderKind"
   },
   "model": {
    "type": "string"
   },
   "promptTokens": {
    "type": "integer"
   },
   "completionTokens": {
    "type": "integer"
   },
   "cost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "x-ticvai-column": "cost_amount",
    "description": "What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"
   },
   "latencyMs": {
    "type": "integer"
   },
   "maskedFieldCount": {
    "type": "integer",
    "description": "How many fields were redacted. Zero on a prompt touching guest data is a defect."
   },
   "traceId": {
    "type": "string"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."
   },
   "cacheLayer": {
    "type": "string",
    "nullable": true,
    "enum": [
     "guardrail",
     "semantic",
     "exact",
     "negative",
     "analytics"
    ],
    "description": "Which cache answered, where one did (AI design 3.6). Null for a model call."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiIntervention": {
  "type": "object",
  "x-ticvai-persistence": "ai.intervention",
  "description": "**A person stepping in** (AIC-187, ADM-535, ADM-536): an override, pause, resume, stop, retry or rollback, with the original AI decision and the human one side by side.",
  "required": [
   "kind",
   "targetKind",
   "targetRef"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "override",
     "pause",
     "resume",
     "cancel",
     "retry",
     "rollback",
     "capabilityPause",
     "capabilityResume"
    ]
   },
   "targetKind": {
    "type": "string",
    "enum": [
     "plan",
     "step",
     "decision",
     "capability"
    ]
   },
   "targetRef": {
    "type": "string"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "originalDecision": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "humanDecision": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "reason": {
    "type": "string",
    "maxLength": 2000
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "createdAt": {
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
 "AiMessage": {
  "type": "object",
  "x-ticvai-persistence": "ai.message",
  "required": [
   "id",
   "conversationId",
   "role",
   "content",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "conversationId": {
    "type": "string",
    "format": "uuid"
   },
   "role": {
    "type": "string",
    "enum": [
     "user",
     "assistant",
     "system"
    ]
   },
   "content": {
    "type": "string"
   },
   "sources": {
    "$ref": "#/components/schemas/AiSourceList"
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "description": "8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"
   },
   "rationale": {
    "type": "string",
    "nullable": true,
    "description": "8.3.68, 8.3.69."
   },
   "proposedAction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProposedAction"
     }
    ],
    "nullable": true,
    "description": "Present where the answer suggests a change. **A draft, never applied here.**"
   },
   "traceId": {
    "type": "string"
   },
   "provider": {
    "$ref": "#/components/schemas/AiProviderKind"
   },
   "model": {
    "type": "string"
   },
   "promptTokens": {
    "type": "integer"
   },
   "completionTokens": {
    "type": "integer"
   },
   "latencyMs": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiPolicySimulation": {
  "type": "object",
  "x-ticvai-persistence": "none — computed; summary kept on ai.governance_policy_version.simulationSummary",
  "description": "What a draft policy version would have decided over recorded decisions and the test cases (ADM-527).",
  "required": [
   "evaluated"
  ],
  "properties": {
   "evaluated": {
    "type": "integer"
   },
   "wouldChange": {
    "type": "integer"
   },
   "byOutcome": {
    "type": "object",
    "additionalProperties": true,
    "description": "Counts per outcome, current against draft."
   },
   "examples": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "decisionRecordId": {
       "type": "string",
       "format": "uuid"
      },
      "current": {
       "$ref": "#/components/schemas/AiGovernanceOutcome"
      },
      "draft": {
       "$ref": "#/components/schemas/AiGovernanceOutcome"
      },
      "capabilityKey": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "AiProviderKind": {
  "type": "string",
  "enum": [
   "openai",
   "gemini",
   "anthropic",
   "azureOpenai",
   "localLlm",
   "openaiCompatible"
  ],
  "description": "`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"
 },
 "AiRiskClass": {
  "type": "string",
  "enum": [
   "low",
   "medium",
   "high",
   "critical"
  ],
  "description": "Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."
 },
 "AiSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n",
  "items": {
   "$ref": "#/components/schemas/AiSource"
  }
 },
 "AiTool": {
  "type": "object",
  "x-ticvai-persistence": "ai.tool",
  "description": "**The tool registry** (design 3.1 Registry, 3.8; AIC-088, AIC-089). The executor calls owning modules only for tools registered here: each names its target operation at a contract version, whether it reads, writes or destroys, its risk, the permission it needs, its compensation and timeout. Platform rows, replicated read-only into each tenant database with the tenant root as `scopePath`; written only by `setAiTool` (`PLATFORM_AI_MANAGE`).",
  "x-ticvai-registered-tools-note": "Registrations the release seeds through `setAiTool` for the resources and white-label assistants (29 September, build; 1.2.59, 2.6.50), so a conversational command or a configuration plan can change a resource schedule, a booking, an allocation or the storefront theme, fonts, header, navigation, homepage and pages. Each owner operation accepts `Prefer: validate-only` (added by its owner the same day). `white-label.publishTenantConfig` is deliberately not a tool: the assistant prepares, a person publishes.",
  "x-ticvai-registered-tools": [
   {
    "toolKey": "resources.setResourceSchedule",
    "targetContract": "resources",
    "targetOperation": "setResourceSchedule",
    "effect": "write",
    "riskClass": "medium",
    "permission": "RESOURCE_CONFIGURE",
    "reversible": true,
    "compensationOperation": "setResourceSchedule",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "resources.updateResourceBooking",
    "targetContract": "resources",
    "targetOperation": "updateResourceBooking",
    "effect": "write",
    "riskClass": "medium",
    "permission": "RESOURCE_BOOK",
    "reversible": true,
    "compensationOperation": "updateResourceBooking",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "resources.allocateResources",
    "targetContract": "resources",
    "targetOperation": "allocateResources",
    "effect": "write",
    "riskClass": "medium",
    "permission": "RESOURCE_BOOK",
    "reversible": true,
    "compensationOperation": "replaceResourceAllocation",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setTheme",
    "targetContract": "white-label",
    "targetOperation": "setTheme",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setFonts",
    "targetContract": "white-label",
    "targetOperation": "setFonts",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setHeader",
    "targetContract": "white-label",
    "targetOperation": "setHeader",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setNavigation",
    "targetContract": "white-label",
    "targetOperation": "setNavigation",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setHomepageLayout",
    "targetContract": "white-label",
    "targetOperation": "setHomepageLayout",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.createContentPage",
    "targetContract": "white-label",
    "targetOperation": "createContentPage",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "deleteContentPage",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "venue-map.generateVisitPlan",
    "targetContract": "venue-map",
    "targetOperation": "generateVisitPlan",
    "effect": "write",
    "riskClass": "low",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": null,
    "timeoutMs": 3000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest"
   },
   {
    "toolKey": "venue-map.getVisitPlan",
    "targetContract": "venue-map",
    "targetOperation": "getVisitPlan",
    "effect": "read",
    "riskClass": "low",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": null,
    "timeoutMs": 2000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest"
   },
   {
    "toolKey": "venue-map.listVisitPlanAlternatives",
    "targetContract": "venue-map",
    "targetOperation": "listVisitPlanAlternatives",
    "effect": "read",
    "riskClass": "low",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": null,
    "timeoutMs": 2000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest"
   },
   {
    "toolKey": "venue-map.updateVisitPlan",
    "targetContract": "venue-map",
    "targetOperation": "updateVisitPlan",
    "effect": "write",
    "riskClass": "low",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": "updateVisitPlan",
    "timeoutMs": 3000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest"
   },
   {
    "toolKey": "venue-map.bookVisitPlan",
    "targetContract": "venue-map",
    "targetOperation": "bookVisitPlan",
    "effect": "write",
    "riskClass": "medium",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": "orders.removeCartLine",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest",
    "requiresGuestConfirmation": true
   }
  ],
  "x-ticvai-registered-tools-planner-note": "**The planner agent's tools** (29 September, MOB-6; the assistant profile `planner.guest`, audience guest, `guestCapabilityScope` `visitPlanning`). The agent refines a rules plan by chat on GST-054 through these five `venue-map` operations, **always called as the guest whose plan it is** (permission null, the guest session's own plan), so every change is a plan version the guest can undo. `bookVisitPlan` needs the guest to press Book in the app; the agent may prepare it and never checks out. AI writes nothing outside `ai.*` (ADR-0020): the plan tables are written by the venue-map service these tools call. **Grounding** (30 September client meeting, MoM 4.7): the agent's candidates are only what these tools return for a day, i.e. the rides, dining and retail points (shops and kiosks) on the published map of that day's venue; it never proposes a point from another venue or from general knowledge, and says so when a preference is not met there (`VisitPlan.unmatchedPreferences`).",
  "required": [
   "toolKey",
   "targetContract",
   "targetOperation",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "toolKey": {
    "type": "string"
   },
   "targetContract": {
    "type": "string"
   },
   "targetOperation": {
    "type": "string"
   },
   "contractVersion": {
    "type": "string"
   },
   "effect": {
    "type": "string",
    "enum": [
     "read",
     "write",
     "destructive"
    ]
   },
   "riskClass": {
    "$ref": "#/components/schemas/AiRiskClass"
   },
   "permission": {
    "type": "string",
    "description": "The permission the requester must hold for the executor to call it on their behalf."
   },
   "reversible": {
    "type": "boolean",
    "description": "Non-reversible steps (a refund, a publish) need the stronger approval tier (AIC-099)."
   },
   "compensationOperation": {
    "type": "string",
    "nullable": true
   },
   "timeoutMs": {
    "type": "integer",
    "minimum": 1
   },
   "idempotent": {
    "type": "boolean",
    "default": true
   },
   "validateOnly": {
    "type": "boolean",
    "default": false,
    "description": "The owner accepts `Prefer: validate-only` on it (design 2.3)."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "disabled"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
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
 "ApprovalRequirement": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "description": "The answer to \"does this need approval\", returned before the action.",
  "required": [
   "isRequired"
  ],
  "properties": {
   "isRequired": {
    "type": "boolean"
   },
   "matchedRule": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ApprovalRule"
     }
    ],
    "nullable": true
   },
   "matrixVersion": {
    "type": "integer",
    "nullable": true
   },
   "approvers": {
    "type": "array",
    "description": "Resolved, with delegations applied. **Named so the caller can say \"this needs Sara\"** rather than \"this needs approval\".\n",
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
      "level": {
       "type": "integer"
      },
      "isDelegate": {
       "type": "boolean"
      },
      "delegatedFrom": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true
   },
   "noApproverAvailable": {
    "type": "boolean",
    "description": "**The case that must not fail silently.** A rule requiring a role nobody at this venue holds means the action is blocked forever, and the caller needs to know that now rather than after raising a request nobody can decide.\n"
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
 "ApprovalSlaPolicy": {
  "type": "object",
  "x-ticvai-persistence": "approvals.sla_policy",
  "description": "Approvals boards 5.5 and 5.6. **A target with no consequence is a number in a table**, so the reminder and breach behaviour are part of the policy.\n",
  "required": [
   "code"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "appliesToRequestKinds": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "targetMinutes": {
    "type": "integer"
   },
   "businessHoursOnly": {
    "type": "boolean",
    "default": true,
    "description": "**A four-hour SLA starting at five in the afternoon is breached by nine the next morning with nobody having done anything wrong.**\n"
   },
   "calendarId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reminders": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "atPercentOfTarget": {
       "type": "integer"
      },
      "notify": {
       "type": "string",
       "enum": [
        "approver",
        "approverManager",
        "requester",
        "escalationGroup"
       ]
      }
     }
    }
   },
   "firstReminderAtPercent": {
    "type": "integer",
    "minimum": 1,
    "maximum": 100,
    "nullable": true,
    "description": "**Percent of `targetMinutes` at which the first reminder goes** (decided 29 September, readiness close-out: the reminder steps are percentages of target). A column so the SLA, Escalation, Reminder & Timeout Rules screen reads it rather than unpacking `reminders`; the reminder in `reminders` at this percentage says whom it notifies (data model for the agreed operations, 29 September)."
   },
   "secondReminderAtPercent": {
    "type": "integer",
    "minimum": 1,
    "maximum": 100,
    "nullable": true,
    "description": "Percent of `targetMinutes` at which the second reminder goes; above `firstReminderAtPercent`"
   },
   "escalateAtPercent": {
    "type": "integer",
    "minimum": 1,
    "maximum": 100,
    "nullable": true,
    "description": "Percent of `targetMinutes` at which the request or workflow escalates; at or above `secondReminderAtPercent`"
   },
   "onBreach": {
    "type": "string",
    "enum": [
     "notifyOnly",
     "escalate",
     "autoApprove",
     "autoReject"
    ],
    "default": "escalate"
   },
   "autoActionAllowed": {
    "type": "boolean",
    "default": false,
    "description": "**Auto-approval on breach is off unless somebody says otherwise, in writing.** A queue that approves itself when nobody looks is not an approval process.\n"
   },
   "escalationGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
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
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
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
 "ProposedAction": {
  "type": "object",
  "x-ticvai-persistence": "ai.proposed_action",
  "required": [
   "id",
   "kind",
   "targetContract",
   "targetOperation",
   "payload",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "interactionId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "pricing",
     "promotion",
     "operational",
     "financial",
     "configuration",
     "content",
     "audience"
    ],
    "description": "`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."
   },
   "targetContract": {
    "type": "string",
    "description": "Which contract would perform it. The assistant never performs it itself."
   },
   "targetOperation": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "description": "**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n",
    "enum": [
     "proposed",
     "approved",
     "rejected",
     "applied",
     "expired"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."
   },
   "approvalLevel": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decisionReason": {
    "type": "string",
    "nullable": true,
    "description": "Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"
   },
   "proposedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan",
    "description": "The plan this action presents for a decision (AI design 2.2 D, 3.8)."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."
   },
   "changeSetHash": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."
   }
  }
 }
}
```
