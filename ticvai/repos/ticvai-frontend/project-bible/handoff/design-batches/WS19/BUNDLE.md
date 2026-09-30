# WS19 — Approval Workflows and Governance board 7

**10 screens · 13 operations · 19 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `APPROVAL_CONFIGURE, APPROVAL_VIEW, DEVELOPER_MANAGE, DEVELOPER_VIEW, PERMISSION_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-349` | Approval Integration Command Center | commandCentre | 3 | 0 | — |
| `ADM-350` | Module Integration Registry | listDetail | 1 | 0 | — |
| `ADM-351` | Approval API Management | configEditor | 1 | 0 | — |
| `ADM-352` | Workflow Event Framework | listDetail | 2 | 0 | — |
| `ADM-353` | Webhook Configuration & Subscription Manager | configEditor | 3 | 0 | — |
| `ADM-354` | External Workflow System Integration | configEditor | 3 | 0 | — |
| `ADM-355` | Data & Workflow Mapping Studio | listDetail | 1 | 0 | — |
| `ADM-356` | Integration Security & Access Control | listDetail | 1 | 0 | — |
| `ADM-357` | Integration Monitoring, Error & Retry Center | listDetail | 2 | 0 | — |
| `ADM-358` | Integration Analytics & AI Health Advisor | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-350, ADM-352, ADM-355, ADM-356, ADM-357, ADM-358 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-349",
  "name": "Approval Integration Command Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "1",
   "page": 60
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-integration-command-center-adm-349",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalIntegrationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-350",
    "ADM-351",
    "ADM-352",
    "ADM-353",
    "ADM-354",
    "ADM-355",
    "ADM-356",
    "ADM-357",
    "ADM-358"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ADM-358",
     "trigger": "Integration Analytics & AI Health Advisor",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-350",
     "trigger": "Module Integration Registry",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-351",
     "trigger": "Approval API Management",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-352",
     "trigger": "Workflow Event Framework",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-353",
     "trigger": "Webhook Configuration & Subscription Manager",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-354",
     "trigger": "External Workflow System Integration",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-355",
     "trigger": "Data & Workflow Mapping Studio",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-356",
     "trigger": "Integration Security & Access Control",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-357",
     "trigger": "Integration Monitoring, Error & Retry Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide administrators and technical teams with a centralized overview of all systems connected to the Approval Engine.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Connected TICVAI Modules",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 60 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "External Integrations",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 60 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "API Requests Today",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 60 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Workflow Events",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 60 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Webhooks",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 60 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Failed Requests",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 60 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Integration Errors",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 60 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Response Time",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 60 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval integration list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the approval integration untouched.",
   "emptyFirstRun": "No approval integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCrossModuleOrchestration",
    "contract": "approvals",
    "purpose": "Which modules raise approvals",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listApprovalExternalProviders",
    "contract": "approvals",
    "purpose": "External providers and their health",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listApprovalExternalDispatches",
    "contract": "approvals",
    "purpose": "Levels waiting on or failed in external systems",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Connected TICVAI Modules",
    "External Integrations",
    "API Requests Today",
    "Workflow Events",
    "Active Webhooks",
    "Failed Requests"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-349",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-349"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 60. 0 of 0 labels bound to a contract property; 8 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-350",
  "name": "Module Integration Registry",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "2",
   "page": 61
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/module-integration-registry-adm-350",
   "component": "apps/ticvai-web/src/routes/platform/ModuleIntegrationRegistry.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-349"
   ],
   "exitTo": [
    "ADM-349"
   ],
   "transitions": [
    {
     "to": "ADM-349",
     "trigger": "Back to Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define which TICVAI modules are allowed to initiate and consume approval workflows.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 61"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 61"
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
   "loading": "The module integration registry list.",
   "error": "Could not load. Names which read failed and leaves the module integration registry untouched.",
   "emptyFirstRun": "No module integration registry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the module integration registry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCrossModuleOrchestration",
    "contract": "approvals",
    "purpose": "The integration registry",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-350",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-350"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 61. 0 of 0 labels bound to a contract property; 0 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-351",
  "name": "Approval API Management",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "3",
   "page": 62
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-api-management-adm-351",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalApiManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-349"
   ],
   "exitTo": [
    "ADM-349"
   ],
   "transitions": [
    {
     "to": "ADM-349",
     "trigger": "Back to Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§API Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure and monitor APIs used to create, retrieve and process approval requests. The matrix explicitly requires approval workflows to be exposed through APIs.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Endpoint",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 62 §API Configuration"
      },
      {
       "kind": "selectField",
       "label": "API version",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 62 §API Configuration"
      },
      {
       "kind": "selectField",
       "label": "Authentication",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 62 §API Configuration"
      },
      {
       "kind": "selectField",
       "label": "tenant context",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 62 §API Configuration"
      },
      {
       "kind": "selectField",
       "label": "request schema",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 62 §API Configuration"
      },
      {
       "kind": "selectField",
       "label": "response schema",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 62 §API Configuration"
      },
      {
       "kind": "selectField",
       "label": "timeout",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 62 §API Configuration"
      },
      {
       "kind": "selectField",
       "label": "retry policy",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 62 §API Configuration"
      },
      {
       "kind": "selectField",
       "label": "rate limit",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 62 §API Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval api configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval api untouched.",
   "emptyFirstRun": "No approval api configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "What the API exposes",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-351",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-351"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 62. 0 of 0 labels bound to a contract property; 9 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-352",
  "name": "Workflow Event Framework",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "4",
   "page": 63
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-event-framework-adm-352",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowEventFramework.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-349"
   ],
   "exitTo": [
    "ADM-349"
   ],
   "transitions": [
    {
     "to": "ADM-349",
     "trigger": "Back to Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the business events published by the Approval Engine. The matrix requires workflow events to be published through the platform event framework.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 63"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 63"
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
   "loading": "The workflow event framework list.",
   "error": "Could not load. Names which read failed and leaves the workflow event framework untouched.",
   "emptyFirstRun": "No workflow event framework yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow event framework are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setTriggerActionCross",
    "contract": "approvals",
    "purpose": "Workflow events",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCrossModuleOrchestration"
    ]
   },
   {
    "operationId": "listWebhookEventTypes",
    "contract": "public-api",
    "purpose": "Workflow events published through the event framework (publisher=approvals)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-352",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-352"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 63. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-353",
  "name": "Webhook Configuration & Subscription Manager",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "5",
   "page": 64
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/webhook-configuration-subscription-manager-adm-353",
   "component": "apps/ticvai-web/src/routes/platform/WebhookConfigurationSubscriptionManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-349"
   ],
   "exitTo": [
    "ADM-349"
   ],
   "transitions": [
    {
     "to": "ADM-349",
     "trigger": "Back to Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Delivery Configuration) and no display directory — it is settings, not a population",
  "purpose": "Allow external or internal systems to subscribe to approval events. The source explicitly requires webhook notifications for approval events.",
  "gaps": [
   {
    "operation": null,
    "why": "**Webhook Configuration & Subscription Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Timeout",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 64 §Delivery Configuration"
      },
      {
       "kind": "selectField",
       "label": "Retry count",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 64 §Delivery Configuration"
      },
      {
       "kind": "selectField",
       "label": "Retry interval",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 64 §Delivery Configuration"
      },
      {
       "kind": "selectField",
       "label": "failure action",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 64 §Delivery Configuration"
      },
      {
       "kind": "selectField",
       "label": "disable threshold",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 64 §Delivery Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The webhook subscription configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the webhook subscription untouched.",
   "emptyFirstRun": "No webhook subscription configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createWebhookSubscription",
    "contract": "public-api",
    "purpose": "Webhook subscriptions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listWebhookEventTypes",
    "contract": "public-api",
    "purpose": "Events a subscription can take",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listWebhookSubscriptions",
    "contract": "public-api",
    "purpose": "Existing subscriptions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-353",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-353"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 64. 0 of 0 labels bound to a contract property; 6 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-354",
  "name": "External Workflow System Integration",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "6",
   "page": 65
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/external-workflow-system-integration-adm-354",
   "component": "apps/ticvai-web/src/routes/platform/ExternalWorkflowSystemIntegration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-349"
   ],
   "exitTo": [
    "ADM-349"
   ],
   "transitions": [
    {
     "to": "ADM-349",
     "trigger": "Back to Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Allow TICVAI to integrate with third-party workflow/governance platforms when a client already operates an enterprise approval environment. The matrix specifically requires integration with third-party workflow systems.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "System name",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 65 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "integration direction",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 65 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "authentication",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 65 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "workflow mapping",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 65 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "user/role mapping",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 65 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "status mapping",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 65 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "error handling",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 65 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "synchronization mode",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 65 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The external workflow system configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the external workflow system untouched.",
   "emptyFirstRun": "No external workflow system configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "External workflow systems",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listApprovalExternalProviders",
    "contract": "approvals",
    "purpose": "Registered external workflow systems",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setApprovalExternalProvider",
    "contract": "approvals",
    "purpose": "Register or change a provider",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-354",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-354"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 65. 0 of 0 labels bound to a contract property; 8 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-355",
  "name": "Data & Workflow Mapping Studio",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "7",
   "page": 66
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/data-workflow-mapping-studio-adm-355",
   "component": "apps/ticvai-web/src/routes/platform/DataWorkflowMappingStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-349"
   ],
   "exitTo": [
    "ADM-349"
   ],
   "transitions": [
    {
     "to": "ADM-349",
     "trigger": "Back to Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Map external system data to TICVAI's approval data model without requiring custom development for every integration.",
  "gaps": [
   {
    "operation": null,
    "why": "**Data & Workflow Mapping Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 66"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 66"
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
   "loading": "The data workflow mapping list.",
   "error": "Could not load. Names which read failed and leaves the data workflow mapping untouched.",
   "emptyFirstRun": "No data workflow mapping yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data workflow mapping are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setTriggerActionCross",
    "contract": "approvals",
    "purpose": "Map external data onto a request",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCrossModuleOrchestration"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-355",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-355"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 66. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-356",
  "name": "Integration Security & Access Control",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "8",
   "page": 67
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/integration-security-access-control-adm-356",
   "component": "apps/ticvai-web/src/routes/platform/IntegrationSecurityAccessControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-349"
   ],
   "exitTo": [
    "ADM-349"
   ],
   "transitions": [
    {
     "to": "ADM-349",
     "trigger": "Back to Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern which applications and external systems can access the Approval Engine.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 67"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 67"
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
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** ☑ Create Approval Request, ☑ Read Status, ☑ Read History, ☐ Submit Approval Decision, ☐ Modify Workflow. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 67 §Permissions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAccessPolicies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The integration security access list.",
   "error": "Could not load. Names which read failed and leaves the integration security access untouched.",
   "emptyFirstRun": "No integration security access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration security access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessPolicies",
    "contract": "identity",
    "purpose": "Integration access control",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-356",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-356"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 67. 0 of 0 labels bound to a contract property; 5 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-357",
  "name": "Integration Monitoring, Error & Retry Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "9",
   "page": 68
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/integration-monitoring-error-retry-center-adm-357",
   "component": "apps/ticvai-web/src/routes/platform/IntegrationMonitoringErrorRetryCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-349"
   ],
   "exitTo": [
    "ADM-349"
   ],
   "transitions": [
    {
     "to": "ADM-349",
     "trigger": "Back to Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide technical teams with real-time monitoring of integration failures.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 68"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 68"
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
       "impliedBy": "listWorkflowExceptionFailure",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The integration monitoring error list.",
   "error": "Could not load. Names which read failed and leaves the integration monitoring error untouched.",
   "emptyFirstRun": "No integration monitoring error yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration monitoring error are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkflowExceptionFailure",
    "contract": "approvals",
    "purpose": "Errors and retries",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listApprovalExternalDispatches",
    "contract": "approvals",
    "purpose": "External dispatch errors and retries",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-357",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-357"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 68. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-358",
  "name": "Integration Analytics & AI Health Advisor",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "7",
   "number": "10",
   "page": 69
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/integration-analytics-ai-health-advisor-adm-358",
   "component": "apps/ticvai-web/src/routes/platform/IntegrationAnalyticsAiHealthAdvisor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-349"
   ],
   "exitTo": [
    "ADM-349"
   ],
   "transitions": [
    {
     "to": "ADM-349",
     "trigger": "Back to Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide technical and business teams with analytics on Approval Engine integration performance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 69"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 69"
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
       "impliedBy": "listWorkflowProcessPerformance",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The integration analytics health list.",
   "error": "Could not load. Names which read failed and leaves the integration analytics health untouched.",
   "emptyFirstRun": "No integration analytics health yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration analytics health are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkflowProcessPerformance",
    "contract": "approvals",
    "purpose": "Integration health",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-358",
   "workshopBoard": "wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-358"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 69. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createWebhookSubscription": {
  "method": "POST",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "Subscribe to business events",
  "permission": "DEVELOPER_MANAGE",
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
  "requestBody": "WebhookSubscription",
  "responds": "WebhookSubscription"
 },
 "listAccessPolicies": {
  "method": "GET",
  "path": "/access-policies",
  "contract": "identity",
  "summary": "Attribute-based access policies",
  "permission": "PERMISSION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccessPolicy"
 },
 "listApiClients": {
  "method": "GET",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Registered clients for this developer",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ApiClient"
 },
 "listApprovalExternalDispatches": {
  "method": "GET",
  "path": "/approval-external-dispatches",
  "contract": "approvals",
  "summary": "What was sent to external workflow systems, and what came back",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "providerId",
    "in": "query",
    "required": false
   },
   {
    "name": "requestId",
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
 "listApprovalExternalProviders": {
  "method": "GET",
  "path": "/approval-external-providers",
  "contract": "approvals",
  "summary": "The external workflow systems approval levels may be sent to",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
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
 "listWebhookEventTypes": {
  "method": "GET",
  "path": "/webhook-event-types",
  "contract": "public-api",
  "summary": "The events a webhook may subscribe to",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "publisher",
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
 "listWebhookSubscriptions": {
  "method": "GET",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "The tenant's webhook subscriptions, filterable by API client",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "clientId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WebhookSubscription"
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
 },
 "setApprovalExternalProvider": {
  "method": "PUT",
  "path": "/approval-external-providers",
  "contract": "approvals",
  "summary": "Register a third-party workflow system as an approver",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "ApprovalExternalProvider",
  "responds": "ApprovalExternalProvider"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessCondition": {
  "type": "object",
  "description": "**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n",
  "required": [
   "attribute",
   "operator"
  ],
  "properties": {
   "attribute": {
    "type": "string",
    "enum": [
     "user.attribute",
     "employee.attribute",
     "employee.onShift",
     "membership.tier",
     "membership.status",
     "accreditation.type",
     "accreditation.status",
     "customer.segment",
     "resource.classification",
     "venue.attribute",
     "venue.id",
     "attraction.attribute",
     "device.kind",
     "device.id",
     "device.trusted",
     "time.ofDay",
     "time.dayOfWeek",
     "time.season",
     "time.withinOperatingHours",
     "event.id",
     "event.status",
     "capacity.utilisationPercent",
     "occupancy.level",
     "risk.score",
     "ticket.status",
     "location.scopePath"
    ]
   },
   "key": {
    "type": "string",
    "nullable": true,
    "description": "For the `*.attribute` forms — which attribute, by code."
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "in",
     "notIn",
     "greaterThan",
     "lessThan",
     "between",
     "contains",
     "startsWith",
     "exists"
    ]
   },
   "value": {
    "nullable": true,
    "description": "The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"
   },
   "values": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "AccessPolicy": {
  "type": "object",
  "x-ticvai-persistence": "identity.access_policy",
  "description": "3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here). The overlap that remains is listed in the build readiness open items rather than merged in this pass.\n",
  "required": [
   "code",
   "name",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Assigned by the server on `createAccessPolicy`; the path names the policy on update."
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "isTemplate": {
    "type": "boolean",
    "default": false
   },
   "permissions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"
   },
   "conditions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AccessCondition"
    }
   },
   "combining": {
    "type": "string",
    "enum": [
     "allMustMatch",
     "anyMayMatch"
    ],
    "default": "allMustMatch"
   },
   "effect": {
    "type": "string",
    "enum": [
     "permit",
     "deny"
    ],
    "description": "**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string",
    "description": "3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"
   },
   "appliesToRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "description": "**Moved only by `setAccessPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "suspended",
     "retired"
    ]
   },
   "version": {
    "type": "integer",
    "default": 1,
    "readOnly": true,
    "description": "Set by the server; every `updateAccessPolicy` writes a new version."
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
   "delegatedAdminRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"
   }
  }
 },
 "ApiClient": {
  "type": "object",
  "x-ticvai-persistence": "control.api_client",
  "description": "CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n",
  "required": [
   "id",
   "developerId",
   "name",
   "environment",
   "scopes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "clientId": {
    "type": "string",
    "readOnly": true
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "production"
    ],
    "description": "**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"
   },
   "scopes": {
    "type": "array",
    "description": "**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n",
    "items": {
     "type": "string",
     "pattern": "^[a-zA-Z]+\\.(read|write)$"
    }
   },
   "issuedBy": {
    "type": "string",
    "enum": [
     "partner",
     "ticvai"
    ],
    "readOnly": true,
    "description": "Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"
   },
   "certificationListingId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "control.integration_listing",
    "description": "For a production client, the certified integration it was issued against."
   },
   "credentialTtlDays": {
    "type": "integer",
    "minimum": 1,
    "maximum": 730,
    "nullable": true,
    "description": "Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the key stops working unless rotated. No token is issued after it."
   },
   "allowedTenantIds": {
    "type": "array",
    "description": "13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "ipAllowList": {
    "type": "array",
    "description": "13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n",
    "items": {
     "type": "string"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked"
    ],
    "readOnly": true
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**A credential unused for a year is a credential nobody will notice being stolen.**\n"
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
 "ApprovalExternalDispatch": {
  "type": "object",
  "x-ticvai-persistence": "approvals.external_dispatch",
  "description": "11.1.65 (29 September, build pass). **One request level sent to an external workflow system**, and what became of it. Written by the platform when a level that names a provider is reached, and closed by `recordExternalApprovalDecision` or by the timeout.\n",
  "required": [
   "id",
   "requestId",
   "providerId",
   "level",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "requestId": {
    "type": "string",
    "format": "uuid"
   },
   "providerId": {
    "type": "string",
    "format": "uuid"
   },
   "level": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "sent",
     "failed",
     "decided",
     "timedOut",
     "cancelled"
    ]
   },
   "attemptCount": {
    "type": "integer",
    "default": 0
   },
   "externalReference": {
    "type": "string",
    "nullable": true,
    "description": "The provider's own id for the item, as it acknowledged or called back with."
   },
   "lastResponseCode": {
    "type": "integer",
    "nullable": true
   },
   "lastError": {
    "type": "string",
    "nullable": true
   },
   "sentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "answeredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "externalOutcome": {
    "type": "string",
    "nullable": true,
    "description": "The provider's own outcome value, before mapping."
   },
   "externalApproverRef": {
    "type": "string",
    "nullable": true,
    "description": "Who decided in the provider's system, as it named them."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ApprovalExternalProvider": {
  "type": "object",
  "x-ticvai-persistence": "approvals.external_provider",
  "description": "11.1.65 (29 September, build pass). **A third-party workflow system registered to decide approval levels**: where TICVAI sends a request, how its fields are mapped, how the answer comes back and what happens when it does not.\n",
  "required": [
   "code",
   "name",
   "endpointUrl",
   "apiClientId",
   "decisionMapping"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "The provider's stable name, and the key `setApprovalExternalProvider` upserts on."
   },
   "name": {
    "type": "string"
   },
   "endpointUrl": {
    "type": "string",
    "description": "`https` only. Where a request level is sent."
   },
   "outboundAuth": {
    "type": "string",
    "enum": [
     "bearerToken",
     "basic",
     "oauthClientCredentials",
     "mutualTls"
    ],
    "default": "oauthClientCredentials"
   },
   "outboundCredential": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "nullable": true,
    "description": "The credential TICVAI presents to the provider. Write-only, never returned, kept on a replace that omits it."
   },
   "signingSecret": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "nullable": true,
    "description": "Signs every request TICVAI sends, as webhook deliveries are signed, so the provider can tell it came from TICVAI. Write-only.\n"
   },
   "apiClientId": {
    "type": "string",
    "format": "uuid",
    "description": "The public-api client the provider calls back as. It must hold `APPROVAL_DECIDE`; `recordExternalApprovalDecision` from any other client is refused.\n"
   },
   "requestMapping": {
    "type": "array",
    "description": "Which request fields go to the provider, under which names. **Only mapped fields leave TICVAI** — a provider receives the amount and the subject it needs, not the whole request.\n",
    "items": {
     "type": "object",
     "required": [
      "from",
      "to"
     ],
     "properties": {
      "from": {
       "type": "string",
       "description": "A field of `ApprovalRequest`, e.g. `amount`, `kind`, `subjectId`, `requestedByPrincipalId`."
      },
      "to": {
       "type": "string",
       "description": "The provider's field name."
      }
     }
    }
   },
   "decisionMapping": {
    "type": "array",
    "minItems": 2,
    "description": "The provider's outcome values and the decision each means. At least one maps to `approve` and one to `reject`.",
    "items": {
     "type": "object",
     "required": [
      "externalValue",
      "decision"
     ],
     "properties": {
      "externalValue": {
       "type": "string"
      },
      "decision": {
       "type": "string",
       "enum": [
        "approve",
        "reject",
        "return",
        "requestInformation"
       ]
      }
     }
    }
   },
   "timeoutMinutes": {
    "type": "integer",
    "default": 1440,
    "description": "How long a level waits for the provider before `onTimeout` applies."
   },
   "onTimeout": {
    "type": "string",
    "enum": [
     "fallBackToRoles",
     "escalate",
     "reject"
    ],
    "default": "fallBackToRoles"
   },
   "maxAttempts": {
    "type": "integer",
    "default": 5,
    "description": "Delivery attempts, with backoff, before a dispatch is `failed` and the level falls back as on timeout."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "paused",
     "disabled"
    ],
    "default": "active",
    "description": "`paused` sends nothing and every level that names it falls back at once; the platform sets `disabled` after repeated failures, as it disables a failing webhook.\n"
   },
   "lastSuccessAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
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
 "WebhookEventCatalogueEntry": {
  "type": "object",
  "x-ticvai-persistence": "none — read from the event catalogue (events/*.yaml) shipped with the release",
  "description": "One event a webhook may subscribe to, as the event catalogue declares it. What a receiver needs to write a handler: the name, the version in the payload, who publishes it, what it is about and when, and the payload fields.\n",
  "required": [
   "name",
   "version",
   "publisher"
  ],
  "properties": {
   "name": {
    "$ref": "#/components/schemas/WebhookEventType"
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "publisher": {
    "type": "string",
    "description": "The one context that publishes it."
   },
   "aggregate": {
    "type": "string",
    "description": "What the event is about. Delivery is ordered within one instance of it."
   },
   "description": {
    "type": "string"
   },
   "emittedWhen": {
    "type": "string",
    "nullable": true
   },
   "payload": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "type"
     ],
     "properties": {
      "field": {
       "type": "string"
      },
      "type": {
       "type": "string"
      },
      "required": {
       "type": "boolean",
       "default": true
      },
      "notes": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "WebhookEventType": {
  "type": "string",
  "description": "**The webhook event catalogue: every event a subscription may name** (29 September, build pass). Each value is the `name` of an event in `events/` — `aggregate.pastTenseFact`, published through `platform.outbox` by exactly one context. A name is added here in the same change that adds its event file, and never before.\n**Added 29 September**, each closing a requirement that had the webhook mechanism and nothing to subscribe to:\n| Events | Publisher | Requirement | |---|---|---| | `device.statusChanged`, `device.tamperDetected`, `device.enrolmentChanged`, `device.firmwareReleased`, `device.firmwareRolloutCompleted` | tenancy | 16.9.56 | | `accreditation.applicationDecided`, `accreditation.holderStatusChanged`, `accreditation.credentialIssued`, `accreditation.renewalDue` | accreditation | 12.1.53 | | `approval.requested`, `approval.escalated`, `approval.stepCompleted`, `approval.expired` | approvals | 11.1.64, 11.1.66 | | `seat.held`, `seat.released`, `seat.blocked`, `seatMap.published` | seating | 21.13.4 | | `consent.deviceConsentRecorded`, `consent.deviceConsentClaimed` | marketing | 2.6.65 | | `order.chargebackRecorded` | orders | 8.3.11 to 8.3.15 (a tenant's own finance or fraud tooling) | | `entitlement.expiringSoon` | access | 5.5.30 (a tenant's own CRM) | | `apiClient.anomalyDetected` | public-api | 17 September minutes M17-07 (added 30 September with its event file) |\n**Published and deliberately not offered** (29 September, build pass, group G2): `identity.credentialResetRequested` and `identity.loginRecorded` are security signals, and a stream of them to an outside receiver is a map of which accounts are under attack; `storefront.sessionEvent` is high-volume fraud telemetry, not a business fact a receiver acts on.\n",
  "enum": [
   "access.validated",
   "accreditation.applicationDecided",
   "accreditation.credentialIssued",
   "accreditation.holderStatusChanged",
   "accreditation.renewalDue",
   "ai.ceilingApproaching",
   "apiClient.anomalyDetected",
   "approval.escalated",
   "approval.expired",
   "approval.granted",
   "approval.rejected",
   "approval.requested",
   "approval.stepCompleted",
   "assets.documentIndexed",
   "cart.abandoned",
   "catalogue.productPublished",
   "consent.deviceConsentClaimed",
   "consent.deviceConsentRecorded",
   "conversation.handedOver",
   "device.enrolmentChanged",
   "device.firmwareReleased",
   "device.firmwareRolloutCompleted",
   "device.statusChanged",
   "device.tamperDetected",
   "entitlement.expiringSoon",
   "entitlement.issued",
   "entitlement.statusChanged",
   "fnb.menuPublished",
   "fnb.orderReady",
   "inventory.purchaseOrderReceived",
   "ledger.journalPosted",
   "ledger.periodClosed",
   "maintenance.assetReturnedToService",
   "maintenance.templatePublished",
   "maintenance.workOrderCompleted",
   "marketing.caseClosed",
   "order.chargebackRecorded",
   "order.completed",
   "order.paid",
   "order.refunded",
   "performance.cancelled",
   "reporting.definitionPublished",
   "retail.merchandisePublished",
   "seat.blocked",
   "seat.held",
   "seat.released",
   "seat.sold",
   "seatMap.published",
   "shift.closed",
   "stock.depleted",
   "tenant.suspended",
   "whitelabel.contentPublished"
  ]
 },
 "WebhookSubscription": {
  "type": "object",
  "x-ticvai-persistence": "control.webhook_subscription",
  "description": "13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n",
  "required": [
   "id",
   "clientId",
   "endpointUrl",
   "eventTypes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "clientId": {
    "type": "string",
    "format": "uuid"
   },
   "endpointUrl": {
    "type": "string"
   },
   "eventTypes": {
    "type": "array",
    "description": "**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. Each entry is a name from the webhook event catalogue (`WebhookEventType`).\n",
    "items": {
     "$ref": "#/components/schemas/WebhookEventType"
    }
   },
   "filters": {
    "type": "object",
    "nullable": true,
    "description": "13.3.22. Tenant, venue, or a business condition on the payload.",
    "additionalProperties": true
   },
   "signingSecret": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "description": "**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingVerification",
     "active",
     "paused",
     "failing",
     "disabled"
    ],
    "readOnly": true
   },
   "consecutiveFailures": {
    "type": "integer",
    "readOnly": true
   },
   "disabledReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"
   }
  }
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
 }
}
```
