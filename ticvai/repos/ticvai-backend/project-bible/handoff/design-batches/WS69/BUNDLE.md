# WS69 — Unified BI Reporting and AI Analytics Platform board 4

**10 screens · 11 operations · 16 schemas · 8 permissions**

Platform P16 Venue Analytics · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `APPROVAL_CONFIGURE, PERMISSION_VIEW, REPORT_EXPORT, REPORT_SCHEDULE, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ANL-041` | Reporting Governance Command Center | listDetail | 2 | 0 | — |
| `ANL-042` | Report Scheduler | configEditor | 2 | 0 | — |
| `ANL-043` | Subscription Manager | listDetail | 2 | 0 | — |
| `ANL-044` | Distribution & Delivery Configuration | configEditor | 1 | 0 | — |
| `ANL-045` | Export & Download Center | listDetail | 2 | 0 | — |
| `ANL-046` | Report API & Data Delivery Manager | configEditor | 1 | 0 | — |
| `ANL-047` | Report Access & Sharing Control | listDetail | 1 | 0 | — |
| `ANL-048` | Delivery Monitoring & Failure Management | listDetail | 1 | 1 | — |
| `ANL-049` | Report Audit Trail & Compliance | configEditor | 1 | 0 | — |
| `ANL-050` | Retention, Archive & Governance Policy | configEditor | 3 | 0 | — |

## Thin screens in this batch

**ANL-041, ANL-043, ANL-045, ANL-047 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ANL-041",
  "name": "Reporting Governance Command Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.1",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/reporting-governance-command-center-anl-041",
   "component": "apps/venue-management-web/src/routes/analytics/ReportingGovernanceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-042",
    "ANL-043",
    "ANL-044",
    "ANL-045",
    "ANL-046",
    "ANL-047",
    "ANL-048",
    "ANL-049",
    "ANL-050"
   ],
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Back to Executive Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true,
     "carries": [
      "reportId"
     ]
    },
    {
     "to": "ANL-050",
     "trigger": "Retention, Archive & Governance Policy",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-042",
     "trigger": "Report Scheduler",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-043",
     "trigger": "Subscription Manager",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-044",
     "trigger": "Distribution & Delivery Configuration",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-045",
     "trigger": "Export & Download Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-046",
     "trigger": "Report API & Data Delivery Manager",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-047",
     "trigger": "Report Access & Sharing Control",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-048",
     "trigger": "Delivery Monitoring & Failure Management",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-049",
     "trigger": "Report Audit Trail & Compliance",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can understand overall reporting-platform health and governance from one screen.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide administrators with a centralized overview of reporting operations, governance, distribution and compliance.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 40 §Display"
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
       "label": "Every reporting governance",
       "columns": [
        "Active Reports",
        "Published Dashboards",
        "Active Schedules",
        "Active Subscriptions",
        "Reports Generated Today",
        "Successful Deliveries",
        "Failed Deliveries",
        "Pending Approvals",
        "Exports Today",
        "API Report Requests",
        "Shared Reports",
        "Governance Exceptions",
        "Recently generated reports",
        "Failed reports",
        "Recently shared reports",
        "Large exports",
        "Permission changes",
        "Scheduled-report changes"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 40 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reporting governance",
       "bindsTo": null,
       "columns": [
        "Active Reports",
        "Published Dashboards",
        "Active Schedules",
        "Active Subscriptions",
        "Reports Generated Today",
        "Successful Deliveries",
        "Failed Deliveries",
        "Pending Approvals",
        "Exports Today",
        "API Report Requests",
        "Shared Reports",
        "Governance Exceptions",
        "Recently generated reports",
        "Failed reports",
        "Recently shared reports",
        "Large exports",
        "Permission changes",
        "Scheduled-report changes"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Show health by”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 40 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reporting governance list.",
   "error": "Could not load. Names which read failed and leaves the reporting governance untouched.",
   "emptyFirstRun": "No reporting governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reporting governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReportSchedules",
    "contract": "reporting",
    "purpose": "What runs when",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listReportDeliveries",
    "contract": "reporting",
    "purpose": "What arrived and what did not",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Active Reports",
    "Published Dashboards",
    "Active Schedules",
    "Active Subscriptions",
    "Reports Generated Today",
    "Successful Deliveries"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-041",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-041"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 40. 0 of 18 labels bound to a contract property; 18 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-042",
  "name": "Report Scheduler",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.2",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/report-scheduler-anl-042",
   "component": "apps/venue-management-web/src/routes/analytics/ReportScheduler.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-041"
   ],
   "exitTo": [
    "ANL-041"
   ],
   "transitions": [
    {
     "to": "ANL-041",
     "trigger": "Back to Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can create and manage recurring report-generation schedules without technical support.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Frequency Options) and no display directory — it is settings, not a population",
  "purpose": "Allow authorized users to automatically generate reports according to defined schedules.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Schedule Name",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Report",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Report Version",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Start Date",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "End Date",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Time",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Frequency",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Run immediately",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retry on failure",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum retries",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Timeout",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "textField",
       "label": "Skip if source data is stale",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "textField",
       "label": "Wait for source refresh",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Once",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Frequency Options"
      },
      {
       "kind": "selectField",
       "label": "Hourly",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Frequency Options"
      },
      {
       "kind": "selectField",
       "label": "Daily",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Frequency Options"
      },
      {
       "kind": "selectField",
       "label": "Weekly",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Frequency Options"
      },
      {
       "kind": "selectField",
       "label": "Monthly",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Frequency Options"
      },
      {
       "kind": "selectField",
       "label": "Quarterly",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Frequency Options"
      },
      {
       "kind": "selectField",
       "label": "Yearly",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Frequency Options"
      },
      {
       "kind": "selectField",
       "label": "Custom",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 41 §Frequency Options"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report scheduler configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the report scheduler untouched.",
   "emptyFirstRun": "No report scheduler configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReportSchedules",
    "contract": "reporting",
    "purpose": "Schedules",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createReportSchedule",
    "contract": "reporting",
    "purpose": "Schedule a report",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReportSchedules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-042",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-042"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 41. 0 of 0 labels bound to a contract property; 23 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-043",
  "name": "Subscription Manager",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.3",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/subscription-manager-anl-043",
   "component": "apps/venue-management-web/src/routes/analytics/SubscriptionManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-041"
   ],
   "exitTo": [
    "ANL-041"
   ],
   "transitions": [
    {
     "to": "ANL-041",
     "trigger": "Back to Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can manage report subscriptions without modifying the original report definition.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users and administrators to subscribe recipients to dashboards, reports and KPI summaries.",
  "gaps": [
   {
    "operation": null,
    "why": "**Subscription Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 43"
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
       "impliedBy": "listReportSubscriptions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createReportSubscription",
       "label": "Create report subscription",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createReportSubscription"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The subscription list.",
   "error": "Could not load. Names which read failed and leaves the subscription untouched.",
   "emptyFirstRun": "No subscription yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReportSubscriptions",
    "contract": "reporting",
    "purpose": "Who receives what",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createReportSubscription",
    "contract": "reporting",
    "purpose": "Add a recipient",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReportSubscriptions"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-043",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-043"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-044",
  "name": "Distribution & Delivery Configuration",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.4",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/distribution-delivery-configuration-anl-044",
   "component": "apps/venue-management-web/src/routes/analytics/DistributionDeliveryConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-041"
   ],
   "exitTo": [
    "ANL-041"
   ],
   "transitions": [
    {
     "to": "ANL-041",
     "trigger": "Back to Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Define; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how generated reporting content reaches approved recipients or destinations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: TICVAI Notification Center, Secure Download, API, External approved destination. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Support configurable channels such as"
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
       "label": "Destination",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Define"
      },
      {
       "kind": "selectField",
       "label": "Recipient",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Define"
      },
      {
       "kind": "selectField",
       "label": "Format",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Define"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Define"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Define"
      },
      {
       "kind": "selectField",
       "label": "File Naming",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Define"
      },
      {
       "kind": "selectField",
       "label": "Password/Security Policy",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Define"
      },
      {
       "kind": "selectField",
       "label": "Expiration",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Define"
      },
      {
       "kind": "selectField",
       "label": "Delivery Priority",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Define"
      },
      {
       "kind": "selectField",
       "label": "Email Subject",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Email Body Template",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Attachment",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Secure Link",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Branding",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "TICVAI Notification Center",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Support configurable channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Secure Download",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Support configurable channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "API",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Support configurable channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "External approved destination",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 44 §Support configurable channels such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The distribution delivery configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the distribution delivery untouched.",
   "emptyFirstRun": "No distribution delivery configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createReportSubscription",
    "contract": "reporting",
    "purpose": "Channel, format and recipients",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReportSubscriptions"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-044",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-044"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 44. 0 of 0 labels bound to a contract property; 18 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-045",
  "name": "Export & Download Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.5",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/export-download-center-anl-045",
   "component": "apps/venue-management-web/src/routes/analytics/ExportDownloadCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-041"
   ],
   "exitTo": [
    "ANL-041"
   ],
   "transitions": [
    {
     "to": "ANL-041",
     "trigger": "Back to Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can export authorized information while TICVAI maintains control and auditability over data extraction.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide centralized management of report and dashboard exports. The source matrix requires reporting export to multiple formats, including PDF, Excel, delimited text and XML.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 45 §Display"
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
       "label": "Every export download",
       "columns": [
        "Export ID",
        "Report",
        "Requested By",
        "Site",
        "Format",
        "Requested Time",
        "Completed Time",
        "File Size",
        "Record Count",
        "Status",
        "Expiration"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 45 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected export download",
       "bindsTo": null,
       "columns": [
        "Export ID",
        "Report",
        "Requested By",
        "Site",
        "Format",
        "Requested Time",
        "Completed Time",
        "File Size",
        "Record Count",
        "Status",
        "Expiration"
       ],
       "notes": "The pack groups this record's detail under its own headings: “At minimum”, “Export Status”, “Large Exports”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 45 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The export download list.",
   "error": "Could not load. Names which read failed and leaves the export download untouched.",
   "emptyFirstRun": "No export download yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the export download are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "exportReportResult",
    "contract": "reporting",
    "purpose": "Export",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getReportExport",
    "contract": "reporting",
    "purpose": "Collect the file",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Export ID",
    "Report",
    "Requested By",
    "Site",
    "Format",
    "Requested Time"
   ],
   "params": [
    {
     "name": "executionId",
     "from": "navigation"
    },
    {
     "name": "exportId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-045",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-045"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 45. 0 of 11 labels bound to a contract property; 19 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-046",
  "name": "Report API & Data Delivery Manager",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.6",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/report-api-data-delivery-manager-anl-046",
   "component": "apps/venue-management-web/src/routes/analytics/ReportApiDataDeliveryManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-041"
   ],
   "exitTo": [
    "ANL-041"
   ],
   "transitions": [
    {
     "to": "ANL-041",
     "trigger": "Back to Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "External approved systems can consume governed reporting data without receiving unrestricted access to TICVAI's operational database.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow approved systems to receive reporting information programmatically. This supports the requirement for report export/access through APIs.",
  "gaps": [
   {
    "operation": null,
    "why": "**Report API & Data Delivery Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "API Name",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Report/Dataset",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Consumer/Application",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Authentication",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed Sites",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed Fields",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Filters",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Rate Limit",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Data Format",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 46 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report api data configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the report api data untouched.",
   "emptyFirstRun": "No report api data configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReportSubscriptions",
    "contract": "reporting",
    "purpose": "API and SFTP delivery",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Requests Today",
    "Success Rate",
    "Failed Requests",
    "Response Time",
    "Data Volume",
    "Last Request"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-046",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-046"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 46. 0 of 0 labels bound to a contract property; 17 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-047",
  "name": "Report Access & Sharing Control",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.7",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/report-access-sharing-control-anl-047",
   "component": "apps/venue-management-web/src/routes/analytics/ReportAccessSharingControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-041"
   ],
   "exitTo": [
    "ANL-041"
   ],
   "transitions": [
    {
     "to": "ANL-041",
     "trigger": "Back to Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Sharing, export and subscription cannot be used to bypass the underlying TICVAI permission model.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide centralized security for reports, dashboards and analytical information. The matrix specifically requires reporting access based on group rights, operating-area rights and user access rights.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 47"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 47"
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
       "impliedBy": "listAuthorisationPolicies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report access sharing list.",
   "error": "Could not load. Names which read failed and leaves the report access sharing untouched.",
   "emptyFirstRun": "No report access sharing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the report access sharing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAuthorisationPolicies",
    "contract": "identity",
    "purpose": "Who may see which report",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-047",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-047"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-048",
  "name": "Delivery Monitoring & Failure Management",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.8",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/delivery-monitoring-failure-management-anl-048",
   "component": "apps/venue-management-web/src/routes/analytics/DeliveryMonitoringFailureManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-041"
   ],
   "exitTo": [
    "ANL-041"
   ],
   "transitions": [
    {
     "to": "ANL-041",
     "trigger": "Back to Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can identify and resolve report-generation and distribution failures without reviewing technical server logs.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Monitor scheduled report execution and distribution and provide operational management of failures.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Retry, Cancel, View Error, Change Destination, Notify Owner, Escalate. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Display"
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
       "label": "Every delivery monitoring failure",
       "columns": [
        "Job ID",
        "Report",
        "Schedule",
        "Start Time",
        "Completion Time",
        "Recipient Count",
        "Delivery Method",
        "Status",
        "Error",
        "Retry Count"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected delivery monitoring failure",
       "bindsTo": null,
       "columns": [
        "Job ID",
        "Report",
        "Schedule",
        "Start Time",
        "Completion Time",
        "Recipient Count",
        "Delivery Method",
        "Status",
        "Error",
        "Retry Count"
       ],
       "notes": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Retry",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Error",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Change Destination",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify Owner",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Actions"
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
    "body": "**Cancel on a delivery monitoring failure is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 48 §Actions"
   }
  ],
  "states": {
   "loading": "The delivery monitoring failure list.",
   "error": "Could not load. Names which read failed and leaves the delivery monitoring failure untouched.",
   "emptyFirstRun": "No delivery monitoring failure yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the delivery monitoring failure are still there. The pack's own statuses are Running — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReportDeliveries",
    "contract": "reporting",
    "purpose": "Failures and retries",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Job ID",
    "Report",
    "Schedule",
    "Start Time",
    "Completion Time",
    "Recipient Count"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-048",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-048"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 48. 0 of 10 labels bound to a contract property; 22 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-049",
  "name": "Report Audit Trail & Compliance",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.9",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/report-audit-trail-compliance-anl-049",
   "component": "apps/venue-management-web/src/routes/analytics/ReportAuditTrailCompliance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-041"
   ],
   "exitTo": [
    "ANL-041"
   ],
   "transitions": [
    {
     "to": "ANL-041",
     "trigger": "Back to Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized administrators and auditors can reconstruct the history of relevant reporting activity.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Maintain complete traceability of reporting activity. The source matrix requires report logs and audit reporting for sales history.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search report audit trail",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Filter audit history by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "User",
        "Report",
        "Action",
        "Date",
        "Site",
        "Business Unit",
        "Export Type",
        "Status"
       ],
       "notes": "The pack filters this screen by user, report, action, date, site, business unit and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Filter audit history by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Report Created",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Report Modified",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Report Published",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Report Executed",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Report Viewed",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Report Exported",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Report Shared",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Schedule Created",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Schedule Modified",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Subscription Created",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Permission Changed",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "API Access",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Report Archived",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Report Deleted",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 49 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report audit trail configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the report audit trail untouched.",
   "emptyFirstRun": "No report audit trail configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoResults": "The filter narrowed it and the report audit trail are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReportDeliveries",
    "contract": "reporting",
    "purpose": "What left, with what in it",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-049",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-049"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 49. 0 of 8 labels bound to a contract property; 22 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-050",
  "name": "Retention, Archive & Governance Policy",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "4",
   "number": "4.10",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/retention-archive-governance-policy-anl-050",
   "component": "apps/venue-management-web/src/routes/analytics/RetentionArchiveGovernancePolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-041"
   ],
   "exitTo": [
    "ANL-041"
   ],
   "transitions": [
    {
     "to": "ANL-041",
     "trigger": "Back to Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Historical reporting content can be governed, archived and retrieved according to configured organizational and regulatory policies.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure retention separately for; Define) and no display directory — it is settings, not a population",
  "purpose": "Control the lifecycle of reports, generated files and historical analytical data. The reporting-platform specification requires long-term reporting history together with archival and retrieval capability.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Report Definitions",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Configure retention separately for"
      },
      {
       "kind": "selectField",
       "label": "Dashboard Versions",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Configure retention separately for"
      },
      {
       "kind": "selectField",
       "label": "Generated Reports",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Configure retention separately for"
      },
      {
       "kind": "selectField",
       "label": "Export Files",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Configure retention separately for"
      },
      {
       "kind": "selectField",
       "label": "Audit Logs",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Configure retention separately for"
      },
      {
       "kind": "selectField",
       "label": "Schedule History",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Configure retention separately for"
      },
      {
       "kind": "selectField",
       "label": "API Logs",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Configure retention separately for"
      },
      {
       "kind": "selectField",
       "label": "Historical Analytics",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Configure retention separately for"
      },
      {
       "kind": "selectField",
       "label": "Retention Period",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Define"
      },
      {
       "kind": "selectField",
       "label": "Archive After",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Define"
      },
      {
       "kind": "selectField",
       "label": "Delete After",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Define"
      },
      {
       "kind": "selectField",
       "label": "Legal/Compliance Hold",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Define"
      },
      {
       "kind": "selectField",
       "label": "Storage Location",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Define"
      },
      {
       "kind": "selectField",
       "label": "Retrieval Rules",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 50 §Define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The retention archive governance configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the retention archive governance untouched.",
   "emptyFirstRun": "No retention archive governance configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalRetentionPolicy",
    "contract": "approvals",
    "purpose": "Retention and archive",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getApprovalRecord"
    ]
   },
   {
    "operationId": "listDataRetentionSettings",
    "contract": "tenancy",
    "purpose": "Retention period per data class",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setDataRetentionSetting",
    "contract": "tenancy",
    "purpose": "Set a class's period",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-050",
   "workshopBoard": "wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-050"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 50. 0 of 0 labels bound to a contract property; 14 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "dataClass",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
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
 "createReportSchedule": {
  "method": "POST",
  "path": "/report-schedules",
  "contract": "reporting",
  "summary": "Schedule a report",
  "permission": "REPORT_SCHEDULE",
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
  "requestBody": "CreateReportScheduleRequest",
  "responds": "ReportSchedule"
 },
 "createReportSubscription": {
  "method": "POST",
  "path": "/report-subscriptions",
  "contract": "reporting",
  "summary": "Send a report to somebody, on terms",
  "permission": "REPORT_SCHEDULE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ReportSubscription",
  "responds": "ReportSubscription"
 },
 "exportReportResult": {
  "method": "POST",
  "path": "/report-executions/{executionId}/export",
  "contract": "reporting",
  "summary": "Export a completed result",
  "permission": "REPORT_EXPORT",
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
 "getReportExport": {
  "method": "GET",
  "path": "/report-exports/{exportId}",
  "contract": "reporting",
  "summary": "Export status and download link",
  "permission": "REPORT_EXPORT",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReportExport"
 },
 "listAuthorisationPolicies": {
  "method": "GET",
  "path": "/authorisation-policies",
  "contract": "identity",
  "summary": "Attribute-based authorisation policies",
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
  "responds": "AuthorisationPolicy"
 },
 "listDataRetentionSettings": {
  "method": "GET",
  "path": "/data-retention-settings",
  "contract": "tenancy",
  "summary": "How long the tenant keeps each class of data",
  "permission": "TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "dataClass",
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
 "listReportDeliveries": {
  "method": "GET",
  "path": "/report-deliveries",
  "contract": "reporting",
  "summary": "What was sent, to whom, and what failed",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "failedOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ReportDelivery"
 },
 "listReportSchedules": {
  "method": "GET",
  "path": "/report-schedules",
  "contract": "reporting",
  "summary": "List scheduled reports",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
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
 "listReportSubscriptions": {
  "method": "GET",
  "path": "/report-subscriptions",
  "contract": "reporting",
  "summary": "Who receives what, and by which route",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReportSubscription"
 },
 "setApprovalRetentionPolicy": {
  "method": "PUT",
  "path": "/approval-retention",
  "contract": "approvals",
  "summary": "How long decision records are kept, and what survives",
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
  "requestBody": "ApprovalRetentionPolicy",
  "responds": "ApprovalRetentionPolicy"
 },
 "setDataRetentionSetting": {
  "method": "PUT",
  "path": "/data-retention-settings/{dataClass}",
  "contract": "tenancy",
  "summary": "Set how long the tenant keeps one class of data",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "TenantDataRetentionSetting",
  "responds": "TenantDataRetentionSetting"
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
 "ApprovalRetentionPolicy": {
  "type": "object",
  "x-ticvai-persistence": "approvals.retention_policy",
  "description": "Approvals board 6.7. **Approval records outlive what they approved.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "appliesToRequestKinds": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "retainYears": {
    "type": "integer",
    "nullable": true,
    "description": "**Null takes the tenant's `approvalRecord` retention setting** (tenancy `setDataRetentionSetting`; decided 29 September, all data retention is tenant configuration). A value here applies to the request kinds this policy names and may only lengthen what the tenant setting keeps.\n"
   },
   "retainSignatures": {
    "type": "boolean",
    "default": true
   },
   "retainAttachments": {
    "type": "boolean",
    "default": false
   },
   "onExpiry": {
    "type": "string",
    "enum": [
     "delete",
     "anonymise",
     "archive"
    ],
    "default": "archive"
   },
   "overridesPrivacyDeletion": {
    "type": "boolean",
    "default": true,
    "description": "**Can extend, never shorten, what privacy retention would delete.** The interaction is decided once here instead of argued per data-subject request.\n"
   },
   "legalBasis": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AuthorisationPolicy": {
  "type": "object",
  "x-ticvai-persistence": "identity.authorisation_policy",
  "description": "3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here).\n**Settled by ADR-0068 (accepted 1 October): guest admission lives in Access only.** This engine keeps staff authorisation and was renamed to say so: `identity.access_policy` became `identity.authorisation_policy`, its versions `identity.authorisation_policy_version`, and its operations `*AuthorisationPolicy*`. \"Access policy\" now means `AccessDynamicPolicy` and nothing else.\n",
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
    "description": "Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update."
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
    "description": "**Moved only by `setAuthorisationPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n",
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
    "description": "Set by the server; every `updateAuthorisationPolicy` writes a new version."
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
 "Cadence": {
  "x-ticvai-persistence": "none — embedded in schedule",
  "type": "object",
  "description": "**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n",
  "required": [
   "frequency"
  ],
  "properties": {
   "frequency": {
    "type": "string",
    "enum": [
     "daily",
     "weekly",
     "monthly",
     "quarterly",
     "onShiftClose",
     "onPeriodClose"
    ]
   },
   "dayOfWeek": {
    "type": "integer",
    "minimum": 0,
    "maximum": 6
   },
   "dayOfMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 31
   },
   "timeOfDay": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "timeZone": {
    "type": "string",
    "readOnly": true,
    "description": "Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."
   }
  }
 },
 "CreateReportScheduleRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "reportId",
   "cadence",
   "recipients",
   "format"
  ],
  "properties": {
   "reportId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "cadence": {
    "$ref": "#/components/schemas/Cadence"
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run."
   },
   "recipients": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/Recipient"
    }
   },
   "format": {
    "$ref": "#/components/schemas/ExportFormat"
   },
   "includePersonalData": {
    "type": "boolean",
    "default": false
   },
   "skipIfEmpty": {
    "type": "boolean",
    "default": true,
    "description": "An empty report every morning trains people to ignore the report."
   }
  }
 },
 "ExecutionStatus": {
  "type": "string",
  "enum": [
   "queued",
   "running",
   "completed",
   "failed",
   "cancelled",
   "expired"
  ]
 },
 "ExportFormat": {
  "type": "string",
  "enum": [
   "csv",
   "xlsx",
   "pdf",
   "json"
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
 "Recipient": {
  "x-ticvai-persistence": "reporting.schedule_recipient",
  "type": "object",
  "description": "One recipient of a schedule. **A row of `reporting.schedule_recipient`, a child of `reporting.schedule`** — `ReportSchedule` declares the pair, which is what gives the table its `schedule_id`. Pull audit 26 September: declared on its own, the table had no column tying a recipient to its schedule.\n",
  "required": [
   "kind",
   "address"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "principal",
     "email",
     "sftp",
     "webhook"
    ]
   },
   "address": {
    "type": "string"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "ReportDelivery": {
  "type": "object",
  "x-ticvai-persistence": "reporting.delivery",
  "description": "BI boards 4.8 and 4.9. **A report that silently stopped arriving is worse than one that never existed.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subscriptionId": {
    "type": "string",
    "format": "uuid"
   },
   "reportId": {
    "type": "string",
    "format": "uuid"
   },
   "attemptedAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "delivered",
     "failed",
     "retrying",
     "suppressed"
    ]
   },
   "recipientCount": {
    "type": "integer"
   },
   "failureReason": {
    "type": "string",
    "nullable": true
   },
   "retryCount": {
    "type": "integer",
    "default": 0
   },
   "containedPersonalData": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ReportExport": {
  "x-ticvai-persistence": "reporting.export",
  "type": "object",
  "required": [
   "id",
   "executionId",
   "format",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "executionId": {
    "type": "string"
   },
   "format": {
    "$ref": "#/components/schemas/ExportFormat"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "generating",
     "ready",
     "failed",
     "expired"
    ]
   },
   "includesPersonalData": {
    "type": "boolean"
   },
   "purpose": {
    "type": "string",
    "nullable": true
   },
   "downloadUrl": {
    "type": "string",
    "nullable": true,
    "description": "Signed and expiring. Present only while status is `ready`."
   },
   "sizeBytes": {
    "type": "integer",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ReportSchedule": {
  "x-ticvai-persistence": "reporting.schedule + reporting.schedule_recipient",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReportScheduleRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "isPaused",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid",
      "description": "The schedule runs under this principal's permissions, not the recipients'. A standing grant of whatever the owner can see.\n"
     },
     "isPaused": {
      "type": "boolean"
     },
     "lastRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "lastRunStatus": {
      "$ref": "#/components/schemas/ExecutionStatus"
     },
     "nextRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "consecutiveFailures": {
      "type": "integer"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "ReportSubscription": {
  "type": "object",
  "x-ticvai-persistence": "reporting.subscription",
  "description": "BI boards 4.3 and 4.4. **Not a schedule** — one schedule serves several of these.",
  "required": [
   "reportId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "reportId": {
    "type": "string",
    "format": "uuid"
   },
   "scheduleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recipients": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "email": {
       "type": "string",
       "nullable": true
      },
      "external": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "channel": {
    "type": "string",
    "enum": [
     "email",
     "sftp",
     "webhook",
     "inPlatform"
    ]
   },
   "format": {
    "type": "string",
    "enum": [
     "pdf",
     "xlsx",
     "csv",
     "json"
    ]
   },
   "includesPersonalData": {
    "type": "boolean",
    "default": false,
    "description": "**Gates on `REPORT_EXPORT_PII` and is audited.** A report that leaves the tenant with personal data in it is a fact somebody will ask about.\n"
   },
   "runsAsPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "**The report runs under the owner's permissions, not the recipient's.**"
   },
   "active": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "TenantDataRetentionClass": {
  "type": "string",
  "description": "**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n",
  "enum": [
   "guestProfile",
   "paymentRecord",
   "financialRecord",
   "auditRecord",
   "approvalRecord",
   "complianceInspection",
   "faceTagBiometric",
   "facePassBiometric",
   "aiPrompts",
   "aiConversations",
   "aiDecisionRecords",
   "aiMetadataIndex"
  ]
 },
 "TenantDataRetentionSetting": {
  "type": "object",
  "x-ticvai-persistence": "tenancy.data_retention_setting",
  "description": "**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n",
  "required": [
   "dataClass"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "dataClass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TenantDataRetentionClass"
     }
    ],
    "x-ticvai-unique": "tenant",
    "description": "One row per class per tenant. On a write it comes from the path; a body value is ignored."
   },
   "retainAmount": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "description": "The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"
   },
   "retainUnit": {
    "type": "string",
    "nullable": true,
    "enum": [
     "days",
     "months",
     "years"
    ],
    "description": "Required with `retainAmount`."
   },
   "followsDataClass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TenantDataRetentionClass"
     }
    ],
    "nullable": true,
    "description": "Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"
   },
   "onExpiry": {
    "type": "string",
    "enum": [
     "archive",
     "anonymise",
     "delete"
    ],
    "default": "archive",
    "description": "ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"
   },
   "anchor": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "createdAt",
     "lastActivity",
     "decidedAt",
     "ticketExpiry"
    ],
    "description": "What the period is counted from. Fixed per class by the platform."
   },
   "effectiveAmount": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The period actually applied, after follows and defaults are resolved."
   },
   "effectiveUnit": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "days",
     "months",
     "years"
    ]
   },
   "isDefault": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "True when the tenant has not set this class and the platform default applies."
   },
   "defaultAmount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false
   },
   "defaultUnit": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "days",
     "months",
     "years"
    ]
   },
   "legalMinimumAmount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "A floor the law sets. A shorter period is refused (`422`)."
   },
   "legalMaximumAmount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."
   },
   "legalLimitUnit": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "days",
     "months",
     "years"
    ]
   },
   "legalBasis": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The law or requirement the limit comes from, e.g. `4.3.4`."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The tenant. Retention is set at tenant scope only."
   }
  }
 }
}
```
