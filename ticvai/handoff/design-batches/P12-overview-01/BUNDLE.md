# P12-overview-01 — P12 · Overview

**2 screens · 18 operations · 31 schemas · 4 permissions**

Platform P12 Venue Support · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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
  `CASE_MANAGE, CASE_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SUP-002` | Agent Dashboard | listDetail | 9 | 6 | — |
| `SUP-008` | Agent Performance & SLA View | listDetail | 10 | 6 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "SUP-002",
  "name": "Agent Dashboard",
  "module": "Overview",
  "requiresModule": "marketing",
  "wave": 3,
  "capability": "C32",
  "implementation": {
   "app": "venue-support-web",
   "route": "/general/agent-dashboard",
   "component": "apps/venue-support-web/src/routes/general/AgentDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-001"
   ],
   "inferred": true,
   "exitTo": [
    "SUP-001",
    "SUP-003",
    "SUP-004"
   ],
   "transitions": [
    {
     "to": "SUP-001",
     "trigger": "Agent Login",
     "provenance": "derived — SUP-001 declares entryState.params challengeId and SUP-002 holds none of them. The edge carries nothing: SUP-002 is opened from SUP-001, so this edge is the way back and SUP-001 keeps its own state"
    },
    {
     "to": "SUP-004",
     "trigger": "Conversation Queue",
     "carries": [
      "caseId",
      "conversationId"
     ],
     "provenance": "derived — SUP-004 declares entryState.params caseId, conversationId and SUP-002 holds caseId, conversationId, so an edge into it carries them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Drawn 26 August** — `Dashboards Board` frame `sup-002`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.",
  "density": "compact",
  "boardFrames": [
   "Dashboards Board.dc.html#sup-002"
  ],
  "pattern": "listDetail",
  "patternReason": "`listCases` reads the population and `getCase` reads one of them — list, select, act",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listCases",
       "notes": "Sends `?status=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Assigned to principal id",
       "operation": "listCases",
       "notes": "Sends `?assignedToPrincipalId=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "toggle",
       "label": "Breached sla",
       "operation": "listCases",
       "notes": "Sends `?breachedSla=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Priority",
       "operation": "listCases",
       "notes": "Sends `?priority=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "dataTable",
       "label": "Every case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "dataTable",
       "label": "Every conversation",
       "bindsTo": "Conversation",
       "columns": [
        "Conversation.id",
        "Conversation.telephony",
        "Conversation.assistSessionId",
        "Conversation.channel",
        "Conversation.state",
        "Conversation.subjectId",
        "Conversation.venueId",
        "Conversation.assignedPrincipalId",
        "Conversation.queueId",
        "Conversation.queuePosition",
        "Conversation.estimatedWaitSeconds",
        "Conversation.handoverReason"
       ],
       "operation": "listConversations",
       "provenance": "contract marketing-crm.yaml GET /conversations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.kind",
        "Case.channel",
        "Case.recordedAt",
        "Case.syncedAt",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "detailPanel",
       "label": "The case",
       "bindsTo": "CaseDetail",
       "columns": [
        "CaseDetail.id",
        "CaseDetail.caseNumber",
        "CaseDetail.subjectId",
        "CaseDetail.guestName",
        "CaseDetail.subject",
        "CaseDetail.kind",
        "CaseDetail.channel",
        "CaseDetail.recordedAt",
        "CaseDetail.syncedAt",
        "CaseDetail.categoryId",
        "CaseDetail.status",
        "CaseDetail.priority",
        "CaseDetail.assignedToPrincipalId",
        "CaseDetail.venueId",
        "CaseDetail.relatedOrderId",
        "CaseDetail.slaDueAt"
       ],
       "operation": "getCase",
       "provenance": "contract marketing-crm.yaml GET /cases/{caseId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add case message",
       "operation": "addCaseMessage",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Create case",
       "operation": "createCase",
       "provenance": "contract marketing-crm.yaml POST /cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate case",
       "operation": "escalateCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen case",
       "operation": "reopenCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Save case",
       "operation": "updateCase",
       "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save agent availability",
       "operation": "setAgentAvailability",
       "provenance": "contract marketing-crm.yaml PUT /agent-availability"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The agent list.",
   "error": "Could not load. Names which read failed and leaves the agent untouched.",
   "emptyFirstRun": "No agent yet. Offers Add case message (`addCaseMessage`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, assignedToPrincipalId, breachedSla, priority and the agent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `CASE_VIEW`, which `listCases` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCases",
    "contract": "marketing-crm",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "addCaseMessage",
    "contract": "marketing-crm",
    "purpose": "Add a message or internal note",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "createCase",
    "contract": "marketing-crm",
    "purpose": "Raise a service case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "escalateCase",
    "contract": "marketing-crm",
    "purpose": "Escalate a case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "getCase",
    "contract": "marketing-crm",
    "purpose": "Read a case with its thread",
    "trigger": "onAction"
   },
   {
    "operationId": "reopenCase",
    "contract": "marketing-crm",
    "purpose": "Reopen a resolved case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "updateCase",
    "contract": "marketing-crm",
    "purpose": "Assign, reprioritise or resolve a case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "listConversations",
    "contract": "marketing-crm",
    "purpose": "The omnichannel inbox",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAgentAvailability",
    "contract": "marketing-crm",
    "purpose": "An agent goes available, away or offline",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "caseId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `caseId`.",
   "preloaded": [
    "Case.id",
    "Case.caseNumber",
    "Case.subjectId",
    "Case.guestName",
    "Case.subject"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-002",
   "derivedFrom": "wireframes/reference/Dashboards Board.dc.html",
   "note": "**Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAddCaseMessage",
    "component": "modal",
    "trigger": "Add case message",
    "body": "**Collects what `addCaseMessage` sends before it is called.** Required: `id`, `body`, `isInternal`, `recordedAt`. Optional: `channel`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add case message",
     "operation": "addCaseMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "body",
      "isInternal",
      "recordedAt",
      "channel",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
   },
   {
    "id": "formCreateCase",
    "component": "modal",
    "trigger": "Create case",
    "body": "**Collects what `createCase` sends before it is called.** Required: `id`, `subject`, `description`, `channel`, `recordedAt`. Optional: `subjectId`, `categoryId`, `priority`, `kind`, `venueId`, `relatedOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCaseRequest",
    "confirm": {
     "label": "Create case",
     "operation": "createCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "subject",
      "description",
      "channel",
      "recordedAt",
      "subjectId",
      "categoryId",
      "priority",
      "kind",
      "venueId",
      "relatedOrderId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases"
   },
   {
    "id": "formEscalateCase",
    "component": "modal",
    "trigger": "Escalate case",
    "body": "**Collects what `escalateCase` sends before it is called.** Required: `reason`. Optional: `assignToPrincipalId`, `newPriority`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Escalate case",
     "operation": "escalateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "assignToPrincipalId",
      "newPriority"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
   },
   {
    "id": "formReopenCase",
    "component": "modal",
    "trigger": "Reopen case",
    "body": "**Collects what `reopenCase` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen case",
     "operation": "reopenCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
   },
   {
    "id": "formUpdateCase",
    "component": "modal",
    "trigger": "Save case",
    "body": "**Collects what `updateCase` sends before it is called.** Nothing in the body is required. Optional: `status`, `priority`, `assignedToPrincipalId`, `categoryId`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save case",
     "operation": "updateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "priority",
      "assignedToPrincipalId",
      "categoryId",
      "resolutionNote"
     ]
    },
    "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
   },
   {
    "id": "formSetAgentAvailability",
    "component": "modal",
    "trigger": "Save agent availability",
    "body": "**Collects what `setAgentAvailability` sends before it is called.** Required: `state`. Optional: `maxConcurrent`, `queueIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save agent availability",
     "operation": "setAgentAvailability"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "state",
      "maxConcurrent",
      "queueIds"
     ]
    },
    "provenance": "contract marketing-crm.yaml PUT /agent-availability"
   }
  ],
  "_platform": {
   "code": "P12",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Support",
   "name": "Venue Support — Agent Console",
   "offlineCapable": false,
   "app": "venue-support-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SUP-008",
  "name": "Agent Performance & SLA View",
  "module": "Overview",
  "requiresModule": "analytics",
  "wave": 3,
  "capability": "C21",
  "implementation": {
   "app": "venue-support-web",
   "route": "/general/agent-performance-and-sla-view",
   "component": "apps/venue-support-web/src/routes/general/AgentPerformanceAndSlaViewDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-001"
   ],
   "inferred": true,
   "exitTo": [
    "SUP-001",
    "SUP-002",
    "SUP-003"
   ],
   "transitions": [
    {
     "to": "SUP-001",
     "trigger": "Agent Login",
     "provenance": "derived — SUP-001 declares entryState.params challengeId and SUP-008 holds none of them. The edge carries nothing: SUP-008 is opened from SUP-001, so this edge is the way back and SUP-001 keeps its own state"
    },
    {
     "to": "SUP-002",
     "trigger": "Agent Dashboard",
     "carries": [
      "caseId"
     ],
     "provenance": "derived — SUP-002 declares entryState.params caseId and SUP-008 holds caseId, so an edge into it carries them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReports` reads the population and `getFinancialReport` reads one of them — list, select, act",
  "purpose": "Produce agent performance & sla view for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Category",
       "operation": "listReports",
       "notes": "Sends `?category=` to `listReports`.",
       "provenance": "contract reporting.yaml GET /reports"
      },
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "listReports",
       "notes": "Sends `?search=` to `listReports`.",
       "provenance": "contract reporting.yaml GET /reports"
      },
      {
       "kind": "dataTable",
       "label": "Every report definition",
       "bindsTo": "ReportDefinition",
       "columns": [
        "ReportDefinition.name",
        "ReportDefinition.description",
        "ReportDefinition.category",
        "ReportDefinition.dataSource",
        "ReportDefinition.columns",
        "ReportDefinition.filters",
        "ReportDefinition.groupBy",
        "ReportDefinition.parameters",
        "ReportDefinition.requiredPermission",
        "ReportDefinition.maxDateRangeDays",
        "ReportDefinition.id",
        "ReportDefinition.isSystem"
       ],
       "operation": "listReports",
       "provenance": "contract reporting.yaml GET /reports"
      },
      {
       "kind": "dataTable",
       "label": "Every conversation",
       "bindsTo": "Conversation",
       "columns": [
        "Conversation.id",
        "Conversation.telephony",
        "Conversation.assistSessionId",
        "Conversation.channel",
        "Conversation.state",
        "Conversation.subjectId",
        "Conversation.venueId",
        "Conversation.assignedPrincipalId",
        "Conversation.queueId",
        "Conversation.queuePosition",
        "Conversation.estimatedWaitSeconds",
        "Conversation.handoverReason"
       ],
       "operation": "listConversations",
       "provenance": "contract marketing-crm.yaml GET /conversations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected report definition",
       "bindsTo": "ReportDefinition",
       "columns": [
        "ReportDefinition.name",
        "ReportDefinition.description",
        "ReportDefinition.category",
        "ReportDefinition.dataSource",
        "ReportDefinition.columns",
        "ReportDefinition.filters",
        "ReportDefinition.groupBy",
        "ReportDefinition.parameters",
        "ReportDefinition.requiredPermission",
        "ReportDefinition.maxDateRangeDays",
        "ReportDefinition.id",
        "ReportDefinition.isSystem",
        "ReportDefinition.isRetired",
        "ReportDefinition.estimatedCost",
        "ReportDefinition.createdByPrincipalId",
        "ReportDefinition.lastRunAt"
       ],
       "operation": "getReport",
       "provenance": "contract reporting.yaml GET /reports/{reportId}"
      },
      {
       "kind": "detailPanel",
       "label": "The financial report",
       "bindsTo": "FinancialReport",
       "columns": [
        "FinancialReport.report",
        "FinancialReport.fiscalPeriodId",
        "FinancialReport.legalEntityId",
        "FinancialReport.currency",
        "FinancialReport.currencyScale",
        "FinancialReport.generatedAt",
        "FinancialReport.sections"
       ],
       "operation": "getFinancialReport",
       "provenance": "contract finance.yaml GET /reports/financial"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask reporting question",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Create report",
       "operation": "createReport",
       "provenance": "contract reporting.yaml POST /reports"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete report",
       "operation": "deleteReport",
       "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save natural language query",
       "operation": "saveNaturalLanguageQuery",
       "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
      },
      {
       "kind": "secondaryButton",
       "label": "Save report",
       "operation": "updateReport",
       "provenance": "contract reporting.yaml PUT /reports/{reportId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteReport",
    "component": "confirmDialog",
    "trigger": "Delete report",
    "body": "**Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A agent performance sla this affects should be identified in the dialog, not just counted.",
    "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
   },
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   },
   {
    "id": "formAskReportingQuestion",
    "component": "modal",
    "trigger": "Ask reporting question",
    "body": "**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Ask reporting question",
     "operation": "askReportingQuestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "question",
      "conversationId",
      "venueId"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/ask"
   },
   {
    "id": "formCreateReport",
    "component": "modal",
    "trigger": "Create report",
    "body": "**Collects what `createReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateReportRequest",
    "confirm": {
     "label": "Create report",
     "operation": "createReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "category",
      "dataSource",
      "columns",
      "requiredPermission",
      "description",
      "filters",
      "groupBy",
      "parameters",
      "maxDateRangeDays"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports"
   },
   {
    "id": "formSaveNaturalLanguageQuery",
    "component": "modal",
    "trigger": "Save natural language query",
    "body": "**Collects what `saveNaturalLanguageQuery` sends before it is called.** Required: `name`. Optional: `category`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save natural language query",
     "operation": "saveNaturalLanguageQuery"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "category"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
   },
   {
    "id": "formUpdateReport",
    "component": "modal",
    "trigger": "Save report",
    "body": "**Collects what `updateReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateReportRequest",
    "confirm": {
     "label": "Save report",
     "operation": "updateReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "category",
      "dataSource",
      "columns",
      "requiredPermission",
      "description",
      "filters",
      "groupBy",
      "parameters",
      "maxDateRangeDays"
     ]
    },
    "provenance": "contract reporting.yaml PUT /reports/{reportId}"
   }
  ],
  "states": {
   "loading": "The agent performance sla list.",
   "error": "Could not load. Names which read failed and leaves the agent performance sla untouched.",
   "emptyFirstRun": "No agent performance sla yet. Offers Create report (`createReport`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on category, search and the agent performance sla are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "createReport",
    "contract": "reporting",
    "purpose": "Create a custom report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "deleteReport",
    "contract": "reporting",
    "purpose": "Retire a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "getFinancialReport",
    "contract": "finance",
    "purpose": "P&L, balance sheet or cash flow",
    "trigger": "onLoad"
   },
   {
    "operationId": "getReport",
    "contract": "reporting",
    "purpose": "Read a report definition",
    "trigger": "onAction"
   },
   {
    "operationId": "listReports",
    "contract": "reporting",
    "purpose": "List available report definitions",
    "trigger": "onLoad"
   },
   {
    "operationId": "saveNaturalLanguageQuery",
    "contract": "reporting",
    "purpose": "Save a natural-language answer as a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Publish a new version of a definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "listConversations",
    "contract": "marketing-crm",
    "purpose": "The omnichannel inbox",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "conversationId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom.",
   "preloaded": [
    "ReportDefinition.name",
    "ReportDefinition.description",
    "ReportDefinition.category",
    "ReportDefinition.dataSource",
    "ReportDefinition.columns"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P12",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Support",
   "name": "Venue Support — Agent Console",
   "offlineCapable": false,
   "app": "venue-support-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
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
 "addCaseMessage": {
  "method": "POST",
  "path": "/cases/{caseId}/messages",
  "contract": "marketing-crm",
  "summary": "Add a message or internal note",
  "permission": "CASE_MANAGE",
  "offlineCapable": true,
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
  "responds": "CaseMessage"
 },
 "askReportingQuestion": {
  "method": "POST",
  "path": "/reports/ask",
  "contract": "reporting",
  "summary": "Natural-language reporting query",
  "permission": "REPORT_VIEW_VENUE",
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
  "responds": "NaturalLanguageAnswer"
 },
 "createCase": {
  "method": "POST",
  "path": "/cases",
  "contract": "marketing-crm",
  "summary": "Raise a service case",
  "permission": "CASE_MANAGE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateCaseRequest",
  "responds": "Case"
 },
 "createReport": {
  "method": "POST",
  "path": "/reports",
  "contract": "reporting",
  "summary": "Create a custom report definition",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateReportRequest",
  "responds": "ReportDefinition"
 },
 "deleteReport": {
  "method": "DELETE",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Retire a report definition",
  "permission": "REPORT_MANAGE",
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
 "escalateCase": {
  "method": "POST",
  "path": "/cases/{caseId}/escalate",
  "contract": "marketing-crm",
  "summary": "Escalate a case",
  "permission": "CASE_MANAGE",
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
  "responds": "Case"
 },
 "getCase": {
  "method": "GET",
  "path": "/cases/{caseId}",
  "contract": "marketing-crm",
  "summary": "Read a case with its thread",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CaseDetail"
 },
 "getFinancialReport": {
  "method": "GET",
  "path": "/reports/financial",
  "contract": "finance",
  "summary": "Financial statements, revenue and tax summaries",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "report",
    "in": "query",
    "required": true
   },
   {
    "name": "fiscalPeriodId",
    "in": "query",
    "required": true
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "costCenterId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "FinancialReport"
 },
 "getReport": {
  "method": "GET",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Read a report definition",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReportDefinition"
 },
 "listCases": {
  "method": "GET",
  "path": "/cases",
  "contract": "marketing-crm",
  "summary": "List service cases",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "assignedToPrincipalId",
    "in": "query",
    "required": null
   },
   {
    "name": "breachedSla",
    "in": "query",
    "required": null
   },
   {
    "name": "priority",
    "in": "query",
    "required": null
   },
   {
    "name": "membershipId",
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
 "listConversations": {
  "method": "GET",
  "path": "/conversations",
  "contract": "marketing-crm",
  "summary": "The omnichannel inbox",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "state",
    "in": "query",
    "required": null
   },
   {
    "name": "assignedToMe",
    "in": "query",
    "required": null
   },
   {
    "name": "channel",
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
 "listReports": {
  "method": "GET",
  "path": "/reports",
  "contract": "reporting",
  "summary": "List available report definitions",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "category",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
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
 "reopenCase": {
  "method": "POST",
  "path": "/cases/{caseId}/reopen",
  "contract": "marketing-crm",
  "summary": "Reopen a resolved case",
  "permission": "CASE_MANAGE",
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
  "responds": "Case"
 },
 "runReport": {
  "method": "POST",
  "path": "/reports/{reportId}/run",
  "contract": "reporting",
  "summary": "Run a report",
  "permission": "REPORT_VIEW_VENUE",
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
  "requestBody": "RunReportRequest",
  "responds": "ReportResult"
 },
 "saveNaturalLanguageQuery": {
  "method": "POST",
  "path": "/reports/ask/{conversationId}/save",
  "contract": "reporting",
  "summary": "Save a natural-language answer as a report definition",
  "permission": "REPORT_MANAGE",
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
  "responds": "ReportDefinition"
 },
 "setAgentAvailability": {
  "method": "PUT",
  "path": "/agent-availability",
  "contract": "marketing-crm",
  "summary": "An agent goes available, away or offline",
  "permission": "CASE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AgentAvailability"
 },
 "updateCase": {
  "method": "PATCH",
  "path": "/cases/{caseId}",
  "contract": "marketing-crm",
  "summary": "Assign, reprioritise or resolve a case",
  "permission": "CASE_MANAGE",
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
  "responds": "Case"
 },
 "updateReport": {
  "method": "PUT",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Publish a new version of a definition",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateReportRequest",
  "responds": "ReportDefinition"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AgentAvailability": {
  "type": "object",
  "x-ticvai-persistence": "marketing.agent_availability",
  "required": [
   "principalId",
   "state"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The caller."
   },
   "state": {
    "type": "string",
    "enum": [
     "available",
     "busy",
     "away",
     "offline"
    ]
   },
   "maxConcurrent": {
    "type": "integer",
    "nullable": true
   },
   "queueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When this state lapses on its own — **availability expires** rather than persisting through a closed laptop."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "Case": {
  "x-ticvai-persistence": "marketing.case",
  "x-ticvai-retired-columns": [
   "guest_name",
   "subject",
   "is_sla_breached"
  ],
  "type": "object",
  "required": [
   "id",
   "caseNumber",
   "subject",
   "status",
   "priority",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."
   },
   "caseNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"
   },
   "subject": {
    "type": "string",
    "x-ticvai-column": "title",
    "description": "**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CaseKind"
     }
    ],
    "nullable": true,
    "description": "What the guest said it was about, where the guest raised it."
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "description": "How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time the case was raised — the start of the SLA clock."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the case arrived. Equal to `recordedAt` for a case raised online."
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"
   },
   "status": {
    "$ref": "#/components/schemas/CaseStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "relatedOrderId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isSlaBreached": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"
   },
   "slaPausedSeconds": {
    "type": "integer",
    "description": "Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"
   },
   "escalationCount": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "CaseDetail": {
  "x-ticvai-persistence": "marketing.case",
  "allOf": [
   {
    "$ref": "#/components/schemas/Case"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string"
     },
     "resolutionNote": {
      "type": "string",
      "nullable": true
     },
     "messages": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CaseMessage"
      }
     }
    }
   }
  ]
 },
 "CaseKind": {
  "type": "string",
  "description": "**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n",
  "enum": [
   "lostProperty",
   "complaint",
   "question",
   "accessibility",
   "refundRequest",
   "other"
  ]
 },
 "CaseMessage": {
  "x-ticvai-persistence": "marketing.case_message",
  "type": "object",
  "required": [
   "id",
   "body",
   "isInternal",
   "authorKind",
   "recordedAt"
  ],
  "properties": {
   "resolution": {
    "type": "string",
    "description": "**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"
   },
   "id": {
    "type": "string"
   },
   "body": {
    "type": "string"
   },
   "isInternal": {
    "type": "boolean"
   },
   "authorKind": {
    "type": "string",
    "enum": [
     "agent",
     "guest",
     "system",
     "ai"
    ]
   },
   "authorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time — `addCaseMessage` is offline-capable."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the message arrived."
   }
  }
 },
 "CasePriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent"
  ]
 },
 "CaseStatus": {
  "type": "string",
  "enum": [
   "open",
   "inProgress",
   "awaitingGuest",
   "escalated",
   "resolved",
   "closed"
  ]
 },
 "Conversation": {
  "type": "object",
  "x-ticvai-persistence": "marketing.conversation",
  "description": "22.8. **A conversation is not a case.** A case is a ticket measured in hours; a conversation is a live session measured in seconds, with somebody waiting. A conversation may create a case; it is not one.\n",
  "required": [
   "id",
   "channel",
   "state"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "telephony": {
    "type": "object",
    "nullable": true,
    "description": "BL-083. **`ConversationChannel` included `voice` with nothing behind it** — the model anticipated telephony and stopped at the enum.\n**Not an integration, a binding.** Genesys, Avaya, Amazon Connect, Teams and 3CX all do call control themselves; what the platform needs is the call bound to the guest and the case, so **an agent who answers already knows who is calling and what about.**\n",
    "properties": {
     "providerCallId": {
      "type": "string"
     },
     "direction": {
      "type": "string",
      "enum": [
       "inbound",
       "outbound",
       "transferred"
      ]
     },
     "fromNumberMasked": {
      "type": "string",
      "nullable": true,
      "description": "**Masked, and it is still personal data.** A phone number identifies a person more reliably than a name does.\n"
     },
     "recordingRef": {
      "type": "string",
      "nullable": true,
      "description": "Held by the provider, referenced here. **Recording consent is jurisdictional and the platform does not assume it** — a reference with no consent record is a recording nobody may play.\n"
     },
     "agentState": {
      "type": "string",
      "enum": [
       "available",
       "onCall",
       "wrapUp",
       "away",
       "offline"
      ],
      "nullable": true
     }
    }
   },
   "assistSessionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-094. **`startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced the other** — so the traceability 2.13.20 asks for had no link to follow.\n**The link is here rather than on the assist session**, because a case may span several assists and an assist belongs to at most one case.\n"
   },
   "channel": {
    "$ref": "#/components/schemas/ConversationChannel"
   },
   "state": {
    "$ref": "#/components/schemas/ConversationState"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "22.8.3. Resolved from phone, email, membership number or a signed-in session. **A conversation with none of those stays anonymous rather than being guessed at.**\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assignedPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queuePosition": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). Null once claimed."
   },
   "estimatedWaitSeconds": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). Null once claimed."
   },
   "handoverReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "guestRequested",
     "assistantRefused",
     "assistantFailed",
     "outOfScope",
     "negativeSentiment",
     "complexIntent",
     "paymentIssue"
    ]
   },
   "handoverSummary": {
    "type": "string",
    "nullable": true,
    "description": "**The assistant's own account of what the guest wants**, so an agent opens with context rather than reading a transcript while somebody waits.\n"
   },
   "sentiment": {
    "type": "string",
    "nullable": true,
    "enum": [
     "positive",
     "neutral",
     "negative",
     "escalating"
    ],
    "description": "22.8.16. **`escalating` is a routing signal**, not a report line."
   },
   "intent": {
    "type": "string",
    "nullable": true,
    "description": "22.8.13. What the guest appears to want, used for routing."
   },
   "locale": {
    "type": "string"
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "22.8.12. Where the conversation raised one."
   },
   "messages": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ConversationMessage"
    }
   },
   "firstResponseSeconds": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "outcome": {
    "type": "string",
    "nullable": true,
    "enum": [
     "resolved",
     "caseRaised",
     "abandonedByGuest",
     "timedOut",
     "spam"
    ]
   }
  }
 },
 "ConversationChannel": {
  "type": "string",
  "enum": [
   "webChat",
   "inAppChat",
   "whatsapp",
   "sms",
   "email",
   "kiosk",
   "voice"
  ]
 },
 "ConversationMessage": {
  "type": "object",
  "x-ticvai-persistence": "marketing.conversation_message + marketing.conversation_message_attachment",
  "required": [
   "id",
   "sender",
   "body",
   "sentAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "sender": {
    "type": "string",
    "enum": [
     "guest",
     "agent",
     "assistant",
     "system"
    ],
    "description": "**Resolved, never declared.** The assistant is labelled as one — a guest talking to a bot that presents as a person is a complaint waiting for the moment they find out.\n"
   },
   "senderPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "body": {
    "type": "string"
   },
   "attachments": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "assetId": {
       "type": "string",
       "format": "uuid"
      },
      "kind": {
       "type": "string",
       "enum": [
        "image",
        "video",
        "document",
        "ticket",
        "qr",
        "paymentLink"
       ]
      }
     }
    }
   },
   "aiInteractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the assistant sent it. **Links the message to its tokens and cost**, so a conversation's spend is attributable (CF-14).\n"
   },
   "sentAt": {
    "type": "string",
    "format": "date-time"
   },
   "readAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ConversationState": {
  "type": "string",
  "description": "**`withAssistant` and `queued` are different, and the second has a person waiting.** Merging them makes the service level unmeasurable, because time with a bot is not time in a queue.\n",
  "enum": [
   "withAssistant",
   "queued",
   "withAgent",
   "waitingOnGuest",
   "resolved",
   "abandoned",
   "timedOut"
  ]
 },
 "CreateCaseRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "subject",
   "description",
   "channel",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "subject": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 10000
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. Must belong to `subjectId` when both are given (422). (decided 29 September, coordinator decision DM4, writers pass)"
   },
   "priority": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CasePriority"
     }
    ],
    "default": "normal"
   },
   "kind": {
    "$ref": "#/components/schemas/CaseKind"
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "relatedOrderId": {
    "type": "string"
   },
   "attachmentRefs": {
    "type": "array",
    "description": "Stored on the opening `CaseMessage`, not on the case.",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time the case was raised. The server stamps `Case.syncedAt` on arrival."
   }
  }
 },
 "CreateReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "category",
   "dataSource",
   "columns",
   "requiredPermission"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "category": {
    "$ref": "#/components/schemas/ReportCategory"
   },
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "columns": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/ReportColumn"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportFilter"
    }
   },
   "groupBy": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "parameters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportParameter"
    }
   },
   "requiredPermission": {
    "$ref": "../shared/permissions.yaml#/components/schemas/Permission",
    "description": "Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"
   },
   "maxDateRangeDays": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "default": 366,
    "description": "Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."
   }
  }
 },
 "DataSource": {
  "type": "string",
  "description": "What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n",
  "enum": [
   "orders",
   "orderLines",
   "payments",
   "refunds",
   "shifts",
   "scanEvents",
   "entitlements",
   "products",
   "inventory",
   "stockMovements",
   "stockCounts",
   "waste",
   "workstations",
   "devices",
   "principals",
   "loyalty",
   "reviews",
   "queueEntries",
   "guests",
   "campaigns",
   "cases",
   "ledgerEntries",
   "workOrders",
   "approvals",
   "purchaseOrders",
   "receipts",
   "requisitions",
   "stockBatches",
   "resourceBookings",
   "delegations",
   "forms",
   "challenges",
   "wallets",
   "resaleListings",
   "accreditationApplications",
   "accreditationHolders",
   "accreditationCredentials",
   "forecastPoints"
  ],
  "x-ticvai-forecast-points": "**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"
 },
 "FieldType": {
  "type": "string",
  "enum": [
   "string",
   "integer",
   "decimal",
   "money",
   "boolean",
   "date",
   "dateTime",
   "uuid",
   "enum"
  ]
 },
 "FinancialReport": {
  "x-ticvai-persistence": "none — computed from replica",
  "type": "object",
  "required": [
   "report",
   "fiscalPeriodId",
   "currency",
   "generatedAt",
   "sections"
  ],
  "properties": {
   "report": {
    "$ref": "#/components/schemas/FinancialReportKind"
   },
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "name",
      "lines",
      "total"
     ],
     "properties": {
      "name": {
       "type": "string"
      },
      "lines": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "label": {
          "type": "string"
         },
         "accountCode": {
          "type": "string",
          "nullable": true
         },
         "amount": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         },
         "priorPeriodAmount": {
          "allOf": [
           {
            "$ref": "../shared/common.yaml#/components/schemas/Money"
           }
          ],
          "description": "The same line for **the same period last year** (decided 28 September, audit R127 (3)). Absent where that period did not exist."
         }
        }
       }
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "FinancialReportKind": {
  "type": "string",
  "description": "The report `getFinancialReport` returns. One vocabulary for the query and the response.",
  "enum": [
   "profitAndLoss",
   "balanceSheet",
   "cashFlow",
   "revenueByVenue",
   "revenueByProduct",
   "taxSummary"
  ]
 },
 "GeneratedQuery": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n",
  "properties": {
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "columns": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportColumn"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportFilter"
    }
   },
   "groupBy": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "compiledSql": {
    "type": "string",
    "nullable": true,
    "description": "The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"
   }
  }
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
 },
 "NaturalLanguageAnswer": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "conversationId",
   "question",
   "interpretation",
   "result",
   "reliability"
  ],
  "properties": {
   "conversationId": {
    "type": "string"
   },
   "question": {
    "type": "string"
   },
   "interpretation": {
    "type": "string",
    "description": "What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."
   },
   "semanticSpec": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingSemanticQuerySpec"
     }
    ],
    "nullable": true,
    "description": "What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"
   },
   "generatedQuery": {
    "allOf": [
     {
      "$ref": "#/components/schemas/GeneratedQuery"
     }
    ],
    "nullable": true,
    "description": "The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"
   },
   "result": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportResult"
     }
    ],
    "nullable": true,
    "description": "Null when the question is outside the semantic model."
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."
   },
   "reliability": {
    "$ref": "#/components/schemas/ReportingAnswerReliability"
   },
   "unavailableReason": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingUnavailableReason"
     }
    ],
    "nullable": true,
    "description": "Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "deprecated": true,
    "description": "Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."
   },
   "suggestedFollowUps": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modelVersion": {
    "type": "string"
   },
   "tokensUsed": {
    "type": "integer"
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
 "ReportCategory": {
  "type": "string",
  "enum": [
   "sales",
   "admission",
   "financial",
   "inventory",
   "guest",
   "operations",
   "marketing",
   "workforce",
   "compliance",
   "custom"
  ]
 },
 "ReportColumn": {
  "x-ticvai-persistence": "reporting.report_column",
  "type": "object",
  "required": [
   "field"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "aggregation": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Aggregation"
     }
    ],
    "default": "none"
   },
   "sortOrder": {
    "type": "integer"
   },
   "sortDirection": {
    "type": "string",
    "enum": [
     "asc",
     "desc"
    ]
   },
   "format": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "ReportDefinition": {
  "x-ticvai-persistence": "reporting.report_definition + reporting.report_column + reporting.report_filter",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReportRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version",
     "isSystem",
     "isRetired",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "version": {
      "type": "string",
      "description": "The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."
     },
     "isSystem": {
      "type": "boolean",
      "description": "Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"
     },
     "isRetired": {
      "type": "boolean"
     },
     "estimatedCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Informs whether it may run inline or must be queued."
     },
     "createdByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     },
     "lastRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "scopePath": {
      "type": "string",
      "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
     }
    }
   }
  ]
 },
 "ReportFilter": {
  "x-ticvai-persistence": "reporting.report_filter",
  "type": "object",
  "required": [
   "field",
   "operator"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "in",
     "notIn",
     "contains",
     "isNull",
     "isNotNull"
    ]
   },
   "value": {
    "description": "**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"
   },
   "values": {
    "type": "array",
    "description": "The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.",
    "items": {}
   },
   "isParameter": {
    "type": "boolean",
    "default": false,
    "description": "Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"
   }
  }
 },
 "ReportParameter": {
  "x-ticvai-persistence": "reporting.report_parameter",
  "type": "object",
  "required": [
   "key",
   "label",
   "type",
   "isRequired"
  ],
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "type": {
    "$ref": "#/components/schemas/FieldType"
   },
   "isRequired": {
    "type": "boolean"
   },
   "defaultValue": {
    "description": "Open on purpose. A value of this parameter's `type`, used when a run supplies none."
   }
  }
 },
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "description": "**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Aggregated columns only, keyed and typed as a row is."
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
   }
  }
 },
 "ReportingAnswerReliability": {
  "type": "string",
  "description": "**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n",
  "enum": [
   "grounded",
   "partial",
   "conflictingSources",
   "insufficientEvidence"
  ]
 },
 "ReportingSemanticQuerySpec": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n",
  "required": [
   "metric",
   "period"
  ],
  "properties": {
   "metric": {
    "type": "string",
    "description": "A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."
   },
   "dimensions": {
    "type": "array",
    "maxItems": 5,
    "description": "Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.",
    "items": {
     "type": "string"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "operator"
     ],
     "properties": {
      "field": {
       "type": "string",
       "description": "A `SemanticModel` field code."
      },
      "operator": {
       "type": "string",
       "enum": [
        "equals",
        "notEquals",
        "greaterThan",
        "lessThan",
        "between",
        "in",
        "notIn",
        "isNull",
        "isNotNull"
       ]
      },
      "values": {
       "type": "array",
       "description": "**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n",
       "items": {}
      }
     }
    }
   },
   "period": {
    "type": "string",
    "description": "ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."
   },
   "comparison": {
    "type": "string",
    "nullable": true,
    "description": "As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.",
    "enum": [
     "previousPeriod",
     "samePeriodLastYear",
     "target",
     "benchmark"
    ]
   },
   "semanticModelVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."
   }
  }
 },
 "ReportingUnavailableReason": {
  "type": "string",
  "description": "Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.",
  "enum": [
   "metricNotModelled",
   "dimensionNotModelled",
   "filterNotModelled",
   "comparisonNotAvailable",
   "periodOutsideHistory"
  ]
 },
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."
   },
   "dateTo": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (audit R158)."
   },
   "forceAsync": {
    "type": "boolean",
    "default": false,
    "description": "Queue regardless of size, for a result to be collected later."
   }
  }
 }
}
```
