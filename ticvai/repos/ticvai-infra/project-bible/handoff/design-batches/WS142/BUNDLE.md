# WS142 — Marketing CRM Configuration Reference v1.0 board 8

**10 screens · 16 operations · 18 schemas · 4 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
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
  `APPROVAL_CONFIGURE, CASE_MANAGE, CASE_VIEW, ORDER_REFUND`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-804` | Case Command Center | listDetail | 2 | 0 | — |
| `BO-805` | Case Queue & Search | listDetail | 3 | 0 | — |
| `BO-806` | Case Creation | listDetail | 2 | 0 | — |
| `BO-807` | Classification & Workflow | listDetail | 3 | 1 | — |
| `BO-808` | Assignment & Workload | listDetail | 2 | 0 | — |
| `BO-809` | SLA Policy Configuration | listDetail | 3 | 0 | — |
| `BO-810` | Escalation Rules | listDetail | 1 | 0 | — |
| `BO-811` | Case Workspace | listDetail | 3 | 0 | — |
| `BO-812` | Service Recovery | listDetail | 1 | 0 | — |
| `BO-813` | Case Analytics & Audit | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-804, BO-808, BO-809, BO-810, BO-811, BO-812, BO-813 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-804",
  "name": "Case Command Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "01",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/case-command-center-bo-804",
   "component": "apps/venue-management-web/src/routes/engagement-support/CaseCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-805",
    "BO-806",
    "BO-807",
    "BO-808",
    "BO-809",
    "BO-810",
    "BO-811",
    "BO-812",
    "BO-813"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-805",
     "trigger": "Case Queue & Search",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-806",
     "trigger": "Case Creation",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-807",
     "trigger": "Classification & Workflow",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-808",
     "trigger": "Assignment & Workload",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-809",
     "trigger": "SLA Policy Configuration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-810",
     "trigger": "Escalation Rules",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-811",
     "trigger": "Case Workspace",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "carries": [
      "caseId"
     ]
    },
    {
     "to": "BO-812",
     "trigger": "Service Recovery",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-813",
     "trigger": "Case Analytics & Audit",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a role-specific overview of service operations. Show new, open, pending, resolved, overdue and SLA-risk cases with escalations, response time, resolution time and CSAT. Visualize volume, priority, category, channel, venue, owner, aging and trend. Surface major incidents, repeated issues, overloaded queues and high-value guests requiring attention. Provide drill-down to saved queues and allow supervisors to take governed corrective action. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 41"
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
       "impliedBy": "listMyCases",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The case list.",
   "error": "Could not load. Names which read failed and leaves the case untouched.",
   "emptyFirstRun": "No case yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the case are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMyCases",
    "contract": "marketing-crm",
    "purpose": "The cases this guest raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCases",
    "contract": "marketing-crm",
    "purpose": "List service cases",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-804",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-804"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 41. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-805",
  "name": "Case Queue & Search",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "02",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/case-queue-search-bo-805",
   "component": "apps/venue-management-web/src/routes/engagement-support/CaseQueueSearch.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-804"
   ],
   "exitTo": [
    "BO-804"
   ],
   "transitions": [
    {
     "to": "BO-804",
     "trigger": "Back to Case Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a complete, searchable work queue for service cases. Search by case, guest, contact, transaction, ticket, booking, keyword or external reference. Filter by category, subcategory, priority, channel, venue, status, owner, SLA, date and guest tier. Support saved views, configurable columns, controlled bulk assignment/status actions and export. Display live SLA clocks and role-based action availability without exposing restricted guest data. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 41"
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
       "impliedBy": "listCases",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "textField",
       "label": "Parent category id",
       "operation": "listCaseCategories",
       "notes": "Sends `?parentCategoryId=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "toggle",
       "label": "Top level only",
       "operation": "listCaseCategories",
       "notes": "Sends `?topLevelOnly=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listCaseCategories",
       "notes": "Sends `?isActive=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "dataTable",
       "label": "Every case category",
       "bindsTo": "CaseCategory",
       "columns": [
        "CaseCategory.id",
        "CaseCategory.code",
        "CaseCategory.name",
        "CaseCategory.parentCategoryId",
        "CaseCategory.defaultPriority",
        "CaseCategory.isActive",
        "CaseCategory.scopePath"
       ],
       "operation": "listCaseCategories",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listServiceQueues",
       "notes": "Sends `?isActive=` to `listServiceQueues`.",
       "provenance": "contract marketing-crm.yaml GET /service-queues"
      },
      {
       "kind": "dataTable",
       "label": "Every service queue",
       "bindsTo": "ServiceQueue",
       "columns": [
        "ServiceQueue.id",
        "ServiceQueue.code",
        "ServiceQueue.name",
        "ServiceQueue.overflowWaitSeconds",
        "ServiceQueue.isActive",
        "ServiceQueue.scopePath"
       ],
       "operation": "listServiceQueues",
       "provenance": "contract marketing-crm.yaml GET /service-queues"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The case queue search list.",
   "error": "Could not load. Names which read failed and leaves the case queue search untouched.",
   "emptyFirstRun": "No case queue search yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the case queue search are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCases",
    "contract": "marketing-crm",
    "purpose": "The queue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listCaseCategories",
    "contract": "marketing-crm",
    "purpose": "List case categories and subcategories",
    "trigger": "onLoad"
   },
   {
    "operationId": "listServiceQueues",
    "contract": "marketing-crm",
    "purpose": "List customer-service queues",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-805",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-805"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 41. 0 of 0 labels bound to a contract property; 0 of 7 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-806",
  "name": "Case Creation",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "03",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/case-creation-bo-806",
   "component": "apps/venue-management-web/src/routes/engagement-support/CaseCreation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-804"
   ],
   "exitTo": [
    "BO-804"
   ],
   "transitions": [
    {
     "to": "BO-804",
     "trigger": "Back to Case Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a complete case from any service touchpoint. Create manually or from chatbot, conversation, survey, review, transaction, incident or API event. Capture guest, category, priority, channel, venue, subject, details, attachments and linked records. Apply defaults, mandatory fields, duplicate detection, suggested classification and SLA preview. Allow draft and submit workflows and record source, creator, timestamp and initial evidence. Configuration Scope of Work | Version 1.0 41 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**Case Creation declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 41"
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
       "impliedBy": "createCase",
       "label": "Create case",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createCase"
      },
      {
       "kind": "textField",
       "label": "Parent category id",
       "operation": "listCaseCategories",
       "notes": "Sends `?parentCategoryId=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "toggle",
       "label": "Top level only",
       "operation": "listCaseCategories",
       "notes": "Sends `?topLevelOnly=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listCaseCategories",
       "notes": "Sends `?isActive=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "dataTable",
       "label": "Every case category",
       "bindsTo": "CaseCategory",
       "columns": [
        "CaseCategory.id",
        "CaseCategory.code",
        "CaseCategory.name",
        "CaseCategory.parentCategoryId",
        "CaseCategory.defaultPriority",
        "CaseCategory.isActive",
        "CaseCategory.scopePath"
       ],
       "operation": "listCaseCategories",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The case creation list.",
   "error": "Could not load. Names which read failed and leaves the case creation untouched.",
   "emptyFirstRun": "No case creation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the case creation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createCase",
    "contract": "marketing-crm",
    "purpose": "Raise a service case",
    "trigger": "onAction"
   },
   {
    "operationId": "listCaseCategories",
    "contract": "marketing-crm",
    "purpose": "List case categories and subcategories",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-806",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-806"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 41. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-807",
  "name": "Classification & Workflow",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "04",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/classification-workflow-bo-807",
   "component": "apps/venue-management-web/src/routes/engagement-support/ClassificationWorkflow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-804"
   ],
   "exitTo": [
    "BO-804"
   ],
   "transitions": [
    {
     "to": "BO-804",
     "trigger": "Back to Case Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure case taxonomies and lifecycle states. Maintain categories, subcategories, reason codes, outcomes, severity, priority and applicable business units. Configure status model, stage transitions, mandatory fields, validation and conditional steps. Use a visual workflow for assignment, work, approval, escalation, resolution and closure. Version and approve configurations and show affected open cases before activating changes. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 42"
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
       "impliedBy": "setCaseInvestigationResolution",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setCaseInvestigationResolution"
      },
      {
       "kind": "textField",
       "label": "Parent category id",
       "operation": "listCaseCategories",
       "notes": "Sends `?parentCategoryId=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "toggle",
       "label": "Top level only",
       "operation": "listCaseCategories",
       "notes": "Sends `?topLevelOnly=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listCaseCategories",
       "notes": "Sends `?isActive=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "dataTable",
       "label": "Every case category",
       "bindsTo": "CaseCategory",
       "columns": [
        "CaseCategory.id",
        "CaseCategory.code",
        "CaseCategory.name",
        "CaseCategory.parentCategoryId",
        "CaseCategory.defaultPriority",
        "CaseCategory.isActive",
        "CaseCategory.scopePath"
       ],
       "operation": "listCaseCategories",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save case category definition",
       "operation": "setCaseCategoryDefinition",
       "permission": "CASE_MANAGE",
       "notes": "**An upsert keyed on `code`**, which is unique in the venue and never changes once created.",
       "provenance": "contract marketing-crm.yaml PUT /case-categories"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The classification workflow list.",
   "error": "Could not load. Names which read failed and leaves the classification workflow untouched.",
   "emptyFirstRun": "No classification workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the classification workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCaseInvestigationResolution",
    "contract": "marketing-crm",
    "purpose": "Classification and workflow",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listCaseCategories",
    "contract": "marketing-crm",
    "purpose": "List case categories and subcategories",
    "trigger": "onLoad"
   },
   {
    "operationId": "setCaseCategoryDefinition",
    "contract": "marketing-crm",
    "purpose": "Create or change a case category or subcategory",
    "trigger": "onAction",
    "invalidates": [
     "listCaseCategories"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-807",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-807"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetCaseCategoryDefinition",
    "component": "modal",
    "trigger": "Save case category definition",
    "body": "**Collects what `setCaseCategoryDefinition` sends before it is called.** Required: `id`, `code`, `name`, `isActive`. Optional: `parentCategoryId`, `defaultPriority`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CaseCategory",
    "confirm": {
     "label": "Save case category definition",
     "operation": "setCaseCategoryDefinition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "isActive",
      "parentCategoryId",
      "defaultPriority",
      "scopePath"
     ]
    },
    "provenance": "contract marketing-crm.yaml PUT /case-categories"
   }
  ],
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-808",
  "name": "Assignment & Workload",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "05",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/assignment-workload-bo-808",
   "component": "apps/venue-management-web/src/routes/engagement-support/AssignmentWorkload.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-804"
   ],
   "exitTo": [
    "BO-804"
   ],
   "transitions": [
    {
     "to": "BO-804",
     "trigger": "Back to Case Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Assign cases to the best available team or agent. Route by skill, department, venue, language, category, guest tier, priority and operating hours. Configure round robin, least load, ownership continuity, named team and manual assignment methods. Display capacity, utilization, open workload, absence and assignment recommendation. Require approval for restricted reassignment and retain assignment reason and history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 42"
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
       "impliedBy": "listAgentWorkloadAvailability",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listServiceQueues",
       "notes": "Sends `?isActive=` to `listServiceQueues`.",
       "provenance": "contract marketing-crm.yaml GET /service-queues"
      },
      {
       "kind": "dataTable",
       "label": "Every service queue",
       "bindsTo": "ServiceQueue",
       "columns": [
        "ServiceQueue.id",
        "ServiceQueue.code",
        "ServiceQueue.name",
        "ServiceQueue.overflowWaitSeconds",
        "ServiceQueue.isActive",
        "ServiceQueue.scopePath"
       ],
       "operation": "listServiceQueues",
       "provenance": "contract marketing-crm.yaml GET /service-queues"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workload list.",
   "error": "Could not load. Names which read failed and leaves the workload untouched.",
   "emptyFirstRun": "No workload yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workload are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAgentWorkloadAvailability",
    "contract": "marketing-crm",
    "purpose": "Assignment and workload",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listServiceQueues",
    "contract": "marketing-crm",
    "purpose": "List customer-service queues",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-808",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-808"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-809",
  "name": "SLA Policy Configuration",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "06",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/sla-policy-configuration-bo-809",
   "component": "apps/venue-management-web/src/routes/engagement-support/SlaPolicyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-804"
   ],
   "exitTo": [
    "BO-804"
   ],
   "transitions": [
    {
     "to": "BO-804",
     "trigger": "Back to Case Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define measurable service commitments and pause rules. Configure first-response and resolution targets by case type, priority, venue, channel and guest tier. Apply operating calendars, holidays, 24/7 rules, pause conditions, dependency states and warning thresholds. Define target hierarchy, precedence, exceptions and behavior when multiple SLAs apply. Simulate policies before activation and version, approve and audit every change. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 42"
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
       "impliedBy": "listSlaPolicyService",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setApprovalSlaPolicy",
       "label": "Save approval SLA policy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApprovalSlaPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sla policy list.",
   "error": "Could not load. Names which read failed and leaves the sla policy untouched.",
   "emptyFirstRun": "No sla policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sla policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSlaPolicyService",
    "contract": "marketing-crm",
    "purpose": "SLA policies",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setApprovalSlaPolicy",
    "contract": "approvals",
    "purpose": "Configure a target and its consequence",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setSlaPolicy",
    "contract": "marketing-crm",
    "purpose": "Define a case SLA policy",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listSlaPolicyService"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-809",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-809"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-810",
  "name": "Escalation Rules",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "07",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/escalation-rules-bo-810",
   "component": "apps/venue-management-web/src/routes/engagement-support/EscalationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-804"
   ],
   "exitTo": [
    "BO-804"
   ],
   "transitions": [
    {
     "to": "BO-804",
     "trigger": "Back to Case Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Automate tiered escalation before or after service risk materializes. Create time-based and condition-based triggers for response, resolution, priority, sentiment, repeat contact and compliance risk. Define escalation level, recipients, notification channel, required action, approval and acknowledgement deadline. Configure supervisor, manager, specialist and executive paths, compensation limits and override controls. Prevent escalation loops and record trigger, evaluated conditions, recipients, actions and closure. Configuration Scope of Work | Version 1.0 42 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 42"
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
       "impliedBy": "listEscalationCriticalCase",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The escalation rules list.",
   "error": "Could not load. Names which read failed and leaves the escalation rules untouched.",
   "emptyFirstRun": "No escalation rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the escalation rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEscalationCriticalCase",
    "contract": "marketing-crm",
    "purpose": "Escalation rules in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-810",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-810"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-811",
  "name": "Case Workspace",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "08",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/case-workspace-bo-811",
   "component": "apps/venue-management-web/src/routes/engagement-support/CaseWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-804"
   ],
   "exitTo": [
    "BO-804"
   ],
   "transitions": [
    {
     "to": "BO-804",
     "trigger": "Back to Case Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide one place to investigate, communicate and resolve a case. Display guest 360, case details, SLA, timeline, messages, notes, tasks, attachments and linked transactions. Support email, SMS, WhatsApp and chat responses using approved templates and complete history. Allow assignment, status, priority, task, approval, related-case and resolution actions by authority. Require reason and evidence for sensitive changes and preserve immutable history after closure. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 43"
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
       "impliedBy": "getCase",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "addCaseMessage",
       "label": "Add case message",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "addCaseMessage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The case list.",
   "error": "Could not load. Names which read failed and leaves the case untouched.",
   "emptyFirstRun": "No case yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the case are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getCase",
    "contract": "marketing-crm",
    "purpose": "The case workspace",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "addCaseMessage",
    "contract": "marketing-crm",
    "purpose": "Reply",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updateCase",
    "contract": "marketing-crm",
    "purpose": "Update it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-811",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-811"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "caseId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-812",
  "name": "Service Recovery",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "09",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/service-recovery-bo-812",
   "component": "apps/venue-management-web/src/routes/engagement-support/ServiceRecovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-804"
   ],
   "exitTo": [
    "BO-804"
   ],
   "transitions": [
    {
     "to": "BO-804",
     "trigger": "Back to Case Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure and approve fair, consistent recovery actions. Maintain compensation matrices by issue, severity, guest tier, value and business unit. Support refund, voucher, loyalty points, wallet credit, upgrade, replacement and follow-up journey actions. Apply auto-approval and manager-approval thresholds, budget limits, fraud checks and segregation of duties. Track recovery cost, delivery, redemption, guest response and effect on satisfaction and retention. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 43"
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
       "impliedBy": "setRefundCompensationService",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setRefundCompensationService"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The service recovery list.",
   "error": "Could not load. Names which read failed and leaves the service recovery untouched.",
   "emptyFirstRun": "No service recovery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the service recovery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRefundCompensationService",
    "contract": "marketing-crm",
    "purpose": "Service recovery",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-812",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-812"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-813",
  "name": "Case Analytics & Audit",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "8",
   "number": "10",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/case-analytics-audit-bo-813",
   "component": "apps/venue-management-web/src/routes/engagement-support/CaseAnalyticsAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-804"
   ],
   "exitTo": [
    "BO-804"
   ],
   "transitions": [
    {
     "to": "BO-804",
     "trigger": "Back to Case Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure service quality, root causes and operational accountability. Report case volume, SLA achievement, aging, backlog, escalation, resolution, CSAT and recovery cost. Analyze category, root cause, channel, venue, product, guest tier, team and agent performance. Track repeat cases, lost revenue, compensation, recovery effectiveness and systemic improvement actions. Provide complete audit, secured export and traceability from reported issue to final resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 43 Board 9 - Surveys, Reviews & Voice of Customer Figure 9. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 44",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 43"
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
       "impliedBy": "listMyCases",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The case analytics audit list.",
   "error": "Could not load. Names which read failed and leaves the case analytics audit untouched.",
   "emptyFirstRun": "No case analytics audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the case analytics audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMyCases",
    "contract": "marketing-crm",
    "purpose": "The cases this guest raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCases",
    "contract": "marketing-crm",
    "purpose": "List service cases",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-813",
   "workshopBoard": "wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-813"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
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
 "listAgentWorkloadAvailability": {
  "method": "GET",
  "path": "/agent-workload-availability",
  "contract": "marketing-crm",
  "summary": "Agent Workload, Availability & Workforce Control",
  "permission": "CASE_VIEW",
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
    "name": "queueId",
    "in": "query",
    "required": false
   },
   {
    "name": "team",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "skill",
    "in": "query",
    "required": false
   },
   {
    "name": "language",
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
 "listCaseCategories": {
  "method": "GET",
  "path": "/case-categories",
  "contract": "marketing-crm",
  "summary": "List case categories and subcategories",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "parentCategoryId",
    "in": "query",
    "required": false
   },
   {
    "name": "topLevelOnly",
    "in": "query",
    "required": false
   },
   {
    "name": "isActive",
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
 "listEscalationCriticalCase": {
  "method": "GET",
  "path": "/escalation-critical-case",
  "contract": "marketing-crm",
  "summary": "Escalation & Critical Case Monitor",
  "permission": "CASE_VIEW",
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
    "name": "escalationType",
    "in": "query",
    "required": false
   },
   {
    "name": "priority",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "breachedOnly",
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
 "listMyCases": {
  "method": "GET",
  "path": "/my/cases",
  "contract": "marketing-crm",
  "summary": "The cases this guest raised",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
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
 "listServiceQueues": {
  "method": "GET",
  "path": "/service-queues",
  "contract": "marketing-crm",
  "summary": "List customer-service queues",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "isActive",
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
 "listSlaPolicyService": {
  "method": "GET",
  "path": "/sla-policy-service",
  "contract": "marketing-crm",
  "summary": "SLA Policy & Service-Level Management",
  "permission": "CASE_VIEW",
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
    "name": "slaPolicyId",
    "in": "query",
    "required": false
   },
   {
    "name": "priority",
    "in": "query",
    "required": false
   },
   {
    "name": "kind",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "queueId",
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
   }
  ],
  "requestBody": null,
  "responds": "SlaPolicyServiceLevelManagementView"
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
 "setCaseCategoryDefinition": {
  "method": "PUT",
  "path": "/case-categories",
  "contract": "marketing-crm",
  "summary": "Create or change a case category or subcategory",
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
  "requestBody": "CaseCategory",
  "responds": "CaseCategory"
 },
 "setCaseInvestigationResolution": {
  "method": "PUT",
  "path": "/case-investigation-resolution",
  "contract": "marketing-crm",
  "summary": "Link a record to a case",
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
  "requestBody": "CaseInvestigationResolutionWorkspaceInput",
  "responds": "CaseInvestigationResolutionWorkspaceView"
 },
 "setRefundCompensationService": {
  "method": "PUT",
  "path": "/refund-compensation-service",
  "contract": "marketing-crm",
  "summary": "Raise or change a refund, compensation or policy-exception request on a case",
  "permission": "ORDER_REFUND",
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
  "requestBody": "RefundCompensationServiceExceptionWorkspaceInput",
  "responds": "RefundCompensationServiceExceptionWorkspaceView"
 },
 "setSlaPolicy": {
  "method": "PUT",
  "path": "/sla-policies",
  "contract": "marketing-crm",
  "summary": "Define an SLA policy",
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
  "requestBody": "MarketingSlaPolicy",
  "responds": "MarketingSlaPolicy"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a ULID."
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
 "CaseCategory": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_category",
  "description": "**The venue's case taxonomy**: categories and, under them, subcategories (`parentCategoryId`). `Case.categoryId` and the routing rules' `match.categoryIds` point here; `createCaseClassificationIntelligent` recommends one. Maintained by `setCaseCategoryDefinition`, read by `listCaseCategories` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n",
  "required": [
   "id",
   "code",
   "name",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 60
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "parentCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set on a subcategory; null on a top-level category."
   },
   "defaultPriority": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CasePriority"
     }
    ],
    "nullable": true,
    "description": "The priority a case in this category starts at before routing factors apply."
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
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
 "CaseInvestigationResolutionWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_linked_record",
  "x-ticvai-record-definition": "Related Records (agents can attach)",
  "description": "One link between a case and a record another contract owns. The reference is a pointer, never a copy.",
  "required": [
   "caseId",
   "kind",
   "referenceId"
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
    "description": "**The partition key** (ADR-0005)."
   },
   "caseId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "kind": {
    "type": "string",
    "enum": [
     "order",
     "ticket",
     "payment",
     "refund",
     "membership",
     "walletTransaction",
     "groupBooking",
     "accessEvent"
    ]
   },
   "referenceId": {
    "type": "string",
    "maxLength": 64,
    "description": "The record's id in its owning contract (orders, payments, access, wallet)."
   },
   "note": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "isActive": {
    "type": "boolean",
    "default": true,
    "description": "False unlinks; the row stays for the audit trail."
   },
   "linkedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "CaseInvestigationResolutionWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case, marketing.case_message, marketing.case_linked_record (new), marketing.sla_policy and ai.suggestion",
  "description": "The case workspace (pack 10.1.5). Recommended actions and the summary keep verified data, policy and AI recommendation apart.",
  "required": [
   "caseId",
   "caseNumber",
   "subject",
   "priority",
   "status",
   "created",
   "lastUpdated",
   "linkedRecords",
   "recommendedActions"
  ],
  "properties": {
   "caseId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "caseNumber": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "customer": {
    "type": "string",
    "nullable": true,
    "description": "The guest's name, as `Case.guestName`; null unless the caller holds GUEST_VIEW_PII."
   },
   "subject": {
    "type": "string"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "category": {
    "type": "string",
    "nullable": true,
    "description": "The category's display name."
   },
   "priority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "status": {
    "$ref": "#/components/schemas/CaseStatus"
   },
   "sla": {
    "type": "object",
    "properties": {
     "policyCode": {
      "type": "string",
      "nullable": true
     },
     "dueAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "remainingSeconds": {
      "type": "integer",
      "nullable": true,
      "description": "Negative once breached."
     },
     "isBreached": {
      "type": "boolean"
     },
     "isPaused": {
      "type": "boolean",
      "description": "True while `awaitingGuest`."
     }
    }
   },
   "owner": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The assigned agent's principal id (`Case.assignedToPrincipalId`)."
   },
   "queue": {
    "type": "string",
    "nullable": true
   },
   "created": {
    "type": "string",
    "format": "date-time",
    "description": "`Case.createdAt`."
   },
   "lastUpdated": {
    "type": "string",
    "format": "date-time"
   },
   "linkedRecords": {
    "type": "array",
    "description": "Active links, newest first.",
    "items": {
     "$ref": "#/components/schemas/CaseInvestigationResolutionWorkspaceInput"
    }
   },
   "recommendedActions": {
    "type": "array",
    "maxItems": 10,
    "items": {
     "type": "object",
     "required": [
      "action",
      "basis"
     ],
     "properties": {
      "action": {
       "type": "string",
       "enum": [
        "reply",
        "call",
        "reschedule",
        "exchange",
        "reissue",
        "requestRefund",
        "requestCompensation",
        "raiseInternalRequest",
        "escalate",
        "resolve"
       ]
      },
      "basis": {
       "type": "string",
       "enum": [
        "verifiedData",
        "policy",
        "aiRecommendation"
       ]
      },
      "reason": {
       "type": "string",
       "maxLength": 500
      },
      "policyReference": {
       "type": "string",
       "nullable": true,
       "description": "The policy the action rests on; an AI recommendation never invents one."
      }
     }
    }
   },
   "aiSummary": {
    "type": "object",
    "nullable": true,
    "description": "Where the AI policy enables `summarise`; AI-derived and labelled as such.",
    "properties": {
     "issue": {
      "type": "string"
     },
     "policy": {
      "type": "string",
      "nullable": true
     },
     "currentStatus": {
      "type": "string",
      "nullable": true
     },
     "commercialImpact": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true
     },
     "recommendedAction": {
      "type": "string",
      "nullable": true
     },
     "generatedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
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
 "MarketingSlaPolicy": {
  "type": "object",
  "x-ticvai-persistence": "marketing.sla_policy",
  "description": "**Taken from the backend workbook, 20 September.** Defines service-level response and resolution targets used by support cases.",
  "required": [
   "code",
   "name",
   "businessHoursOnly",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   },
   "code": {
    "type": "string",
    "maxLength": 100
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "priority": {
    "type": "string",
    "maxLength": 20,
    "nullable": true
   },
   "firstResponseMinutes": {
    "type": "integer",
    "nullable": true
   },
   "resolutionMinutes": {
    "type": "integer",
    "nullable": true
   },
   "escalationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "businessHoursOnly": {
    "type": "boolean"
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "RefundCompensationServiceExceptionWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_compensation_request",
  "x-ticvai-record-definition": "Request Types",
  "description": "One refund, compensation or policy-exception request raised from a case. The order, refund and approval are references, never copies.",
  "required": [
   "id",
   "caseId",
   "requestType",
   "value",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID; equals the `Idempotency-Key` header."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "caseId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Required for `fullRefund`, `partialRefund`, `feeWaiver`, `upgrade` and `discount`."
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "requestType": {
    "type": "string",
    "enum": [
     "fullRefund",
     "partialRefund",
     "serviceCredit",
     "walletCredit",
     "voucher",
     "complimentaryTicket",
     "feeWaiver",
     "upgrade",
     "discount",
     "policyException"
    ]
   },
   "value": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "The money value requested; for a complimentary ticket or upgrade, its face value. This is what the approval thresholds are compared with."
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 1000
   },
   "isPolicyException": {
    "type": "boolean",
    "default": false,
    "description": "True when the standard policy would not allow it; always needs approval."
   },
   "exceptionReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true,
    "description": "Required when `isPolicyException` is true."
   },
   "submit": {
    "type": "boolean",
    "default": false,
    "description": "False saves a draft; true routes it.",
    "writeOnly": true
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "draft",
     "pendingApproval",
     "approved",
     "declined",
     "fulfilled",
     "failed",
     "withdrawn"
    ]
   },
   "approvalRequestId": {
    "type": "string",
    "readOnly": true,
    "nullable": true
   },
   "fulfilmentOperation": {
    "type": "string",
    "readOnly": true,
    "nullable": true,
    "description": "e.g. `createRefund`, `topUpWallet`."
   },
   "fulfilmentReference": {
    "type": "string",
    "readOnly": true,
    "nullable": true,
    "description": "The refund, wallet transaction or voucher it produced."
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "RefundCompensationServiceExceptionWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case_compensation_request (new), orders.sales_order, orders.refund, orders.order_fee, orders.refund_policy and approvals.request",
  "description": "The request, the order's financial context, the policy evaluation and who must approve.",
  "required": [
   "request",
   "approvalLevel"
  ],
  "properties": {
   "request": {
    "$ref": "#/components/schemas/RefundCompensationServiceExceptionWorkspaceInput"
   },
   "originalTransaction": {
    "type": "string",
    "nullable": true,
    "description": "The order number."
   },
   "amountPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "amountUsed": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Value of tickets already scanned or consumed."
   },
   "refundableAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "What the refund policy's time bands allow now, less previous refunds."
   },
   "previousRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "fees": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "proposedRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "proposedCompensation": {
    "type": "object",
    "nullable": true,
    "properties": {
     "requestType": {
      "type": "string"
     },
     "value": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    }
   },
   "policyEvaluation": {
    "type": "object",
    "properties": {
     "standardPolicy": {
      "type": "string",
      "description": "The rule that applies, as the venue's refund policy states it."
     },
     "isWithinPolicy": {
      "type": "boolean"
     },
     "policyReference": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "approvalLevel": {
    "type": "string",
    "enum": [
     "agent",
     "secondUser",
     "approver"
    ],
    "description": "From the venue's `selfAuthoriseLimit`, `requiresSecondUserAbove` and `requiresApprovalAbove`; a policy exception is always `approver`."
   },
   "aiExplanation": {
    "type": "string",
    "nullable": true,
    "maxLength": 1000,
    "description": "AI-derived and labelled as such; cites a recorded policy or says none applies."
   }
  }
 },
 "SlaPolicyServiceLevelManagementView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case and marketing.sla_policy",
  "description": "SLA performance for the filters given. Counts are of open cases for the state counts and of cases in the period for the averages and the compliance rate.",
  "required": [
   "withinSla",
   "atRisk",
   "breached",
   "byPolicy"
  ],
  "properties": {
   "withinSla": {
    "type": "integer",
    "minimum": 0
   },
   "atRisk": {
    "type": "integer",
    "minimum": 0
   },
   "breached": {
    "type": "integer",
    "minimum": 0
   },
   "averageResponseSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Mean time to first response, less paused time."
   },
   "averageResolutionSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "slaComplianceRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Cases resolved in the period within target, over cases resolved in the period."
   },
   "byPolicy": {
    "type": "array",
    "description": "One row per SLA policy that timed a case in the period, worst compliance first.",
    "items": {
     "type": "object",
     "required": [
      "slaPolicyId",
      "code",
      "name",
      "withinSla",
      "atRisk",
      "breached"
     ],
     "properties": {
      "slaPolicyId": {
       "type": "string",
       "format": "uuid"
      },
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "firstResponseMinutes": {
       "type": "integer",
       "nullable": true
      },
      "resolutionMinutes": {
       "type": "integer",
       "nullable": true
      },
      "withinSla": {
       "type": "integer",
       "minimum": 0
      },
      "atRisk": {
       "type": "integer",
       "minimum": 0
      },
      "breached": {
       "type": "integer",
       "minimum": 0
      },
      "slaComplianceRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1,
       "nullable": true
      }
     }
    }
   },
   "forecastBreaches": {
    "type": "array",
    "maxItems": 50,
    "description": "AI forecast of open cases likely to breach before the static thresholds fire, soonest first. Advisory; empty when AI is disabled for the tenant.",
    "items": {
     "type": "object",
     "required": [
      "caseCount",
      "horizonMinutes"
     ],
     "properties": {
      "queueId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "queueName": {
       "type": "string",
       "nullable": true
      },
      "slaPolicyId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "caseCount": {
       "type": "integer",
       "minimum": 0
      },
      "horizonMinutes": {
       "type": "integer",
       "minimum": 1
      },
      "confidence": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   }
  }
 }
}
```
