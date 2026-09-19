# P12-overview-01 — P12 · Overview

**2 screens · 18 operations · 24 schemas · 4 permissions**

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
- **2 of these operations work offline**: addCaseMessage, createCase
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SUP-002` | Agent Dashboard | listDetail | 9 | 0 | — |
| `SUP-008` | Agent Performance & SLA View | listDetail | 10 | 1 | — |

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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — SUP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "SUP-004",
     "trigger": "Conversation Queue",
     "carries": [
      "caseId",
      "conversationId"
     ],
     "provenance": "derived — SUP-004 declares entryState.params caseId, conversationId, so an edge into it must carry them"
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
  "gaps": [
   {
    "operation": "listConversations",
    "why": "**1 declared operation reach no component on this screen**: listConversations. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every agent",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected agent",
       "bindsTo": "CaseDetail",
       "columns": [
        "CaseDetail.id",
        "CaseDetail.caseNumber",
        "CaseDetail.subjectId",
        "CaseDetail.guestName",
        "CaseDetail.subject",
        "CaseDetail.categoryId",
        "CaseDetail.status",
        "CaseDetail.priority",
        "CaseDetail.assignedToPrincipalId",
        "CaseDetail.venueId",
        "CaseDetail.relatedOrderId",
        "CaseDetail.slaDueAt",
        "CaseDetail.isSlaBreached",
        "CaseDetail.slaPausedSeconds",
        "CaseDetail.escalationCount",
        "CaseDetail.resolvedAt"
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
       "label": "Add",
       "operation": "addCaseMessage",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createCase",
       "provenance": "contract marketing-crm.yaml POST /cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "operation": "escalateCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen",
       "operation": "reopenCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateCase",
       "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
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
   "emptyFirstRun": "No agent yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the agent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
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
    "CaseDetail.id",
    "CaseDetail.caseNumber",
    "CaseDetail.subjectId",
    "CaseDetail.guestName",
    "CaseDetail.subject"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-002",
   "note": "**Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — SUP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "SUP-002",
     "trigger": "Agent Dashboard",
     "carries": [
      "caseId"
     ],
     "provenance": "derived — SUP-002 declares entryState.params caseId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReports` reads the population and `getFinancialReport` reads one of them — list, select, act",
  "purpose": "Produce agent performance & sla view for this venue.",
  "gaps": [
   {
    "operation": "getReport",
    "why": "**2 declared operations reach no component on this screen**: getReport, listConversations. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every agent performance sla",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected agent performance sla",
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
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createReport",
       "provenance": "contract reporting.yaml POST /reports"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete",
       "operation": "deleteReport",
       "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save",
       "operation": "saveNaturalLanguageQuery",
       "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
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
    "trigger": "Delete",
    "body": "**Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A agent performance sla this affects should be identified in the dialog, not just counted.",
    "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
   }
  ],
  "states": {
   "loading": "The agent performance sla list.",
   "error": "Could not load. Names which read failed and leaves the agent performance sla untouched.",
   "emptyFirstRun": "No agent performance sla yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the agent performance sla are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "from page inventory",
    "trigger": "onLoad"
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
    "trigger": "onLoad"
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
    "FinancialReport.report",
    "FinancialReport.fiscalPeriodId",
    "FinancialReport.legalEntityId",
    "FinancialReport.currency",
    "FinancialReport.currencyScale"
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
  "summary": "P&L, balance sheet or cash flow",
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
   }
  ],
  "requestBody": null,
  "responds": "Conversation"
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
  "responds": null
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
  "responds": null
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
 "Case": {
  "x-ticvai-persistence": "marketing.case",
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
    "type": "string"
   },
   "caseNumber": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string",
    "nullable": true
   },
   "subject": {
    "type": "string"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
    "type": "boolean"
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
    "format": "date-time"
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
    "readOnly": true
   },
   "estimatedWaitSeconds": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
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
  "x-ticvai-persistence": "marketing.conversation_message",
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
   "priority": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CasePriority"
     }
    ],
    "default": "normal"
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
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
    "type": "string",
    "description": "Permission needed to run this report. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"
   },
   "maxDateRangeDays": {
    "type": "integer",
    "nullable": true,
    "description": "Guards against a query spanning years of scan events."
   }
  }
 },
 "DataSource": {
  "type": "string",
  "description": "What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n",
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
   "resaleListings"
  ]
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
    "type": "string"
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
          "$ref": "../shared/common.yaml#/components/schemas/Money"
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
   "confidence"
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
    "description": "What the question was understood to mean, in plain language."
   },
   "generatedQuery": {
    "type": "object",
    "description": "The structured query produced — data source, columns, filters, grouping. Returned so the answer can be checked. An answer nobody can verify is worse than no answer.\n",
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
     }
    }
   },
   "result": {
    "$ref": "#/components/schemas/ReportResult"
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
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
      "type": "string"
     },
     "isSystem": {
      "type": "boolean",
      "description": "Shipped with the platform. Cannot be amended, only cloned."
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
   "value": {},
   "values": {
    "type": "array",
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
   "defaultValue": {}
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
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true
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
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date"
   },
   "dateTo": {
    "type": "string",
    "format": "date"
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
