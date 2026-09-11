# WS69 — Unified BI Reporting and AI Analytics Platform board 4

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ANL-041` | Reporting Governance Command Center | listDetail | 0 | 0 | — |
| `ANL-042` | Report Scheduler | configEditor | 0 | 0 | — |
| `ANL-043` | Subscription Manager | listDetail | 0 | 0 | — |
| `ANL-044` | Distribution & Delivery Configuration | configEditor | 0 | 0 | — |
| `ANL-045` | Export & Download Center | listDetail | 0 | 0 | — |
| `ANL-046` | Report API & Data Delivery Manager | configEditor | 0 | 0 | — |
| `ANL-047` | Report Access & Sharing Control | listDetail | 0 | 0 | — |
| `ANL-048` | Delivery Monitoring & Failure Management | listDetail | 0 | 1 | — |
| `ANL-049` | Report Audit Trail & Compliance | configEditor | 0 | 0 | — |
| `ANL-050` | Retention, Archive & Governance Policy | configEditor | 0 | 0 | — |

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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide administrators with a centralized overview of reporting operations, governance, distribution and compliance.",
  "purposeNote": "Administrators can understand overall reporting-platform health and governance from one screen.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-041"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 40. 0 of 18 labels bound to a contract property; 18 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "back": true
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
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Frequency Options) and no display directory — it is settings, not a population",
  "purpose": "Allow authorized users to automatically generate reports according to defined schedules.",
  "purposeNote": "Authorized users can create and manage recurring report-generation schedules without technical support.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-042"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 41. 0 of 0 labels bound to a contract property; 23 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users and administrators to subscribe recipients to dashboards, reports and KPI summaries.",
  "purposeNote": "Authorized users can manage report subscriptions without modifying the original report definition.",
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
   "regions": []
  },
  "states": {
   "loading": "The subscription list.",
   "error": "Could not load. Names which read failed and leaves the subscription untouched.",
   "emptyFirstRun": "No subscription yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-043"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Define; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how generated reporting content reaches approved recipients or destinations.",
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
    }
   ]
  },
  "states": {
   "loading": "The distribution delivery configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the distribution delivery untouched.",
   "emptyFirstRun": "No distribution delivery configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-044"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 44. 0 of 0 labels bound to a contract property; 14 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide centralized management of report and dashboard exports. The source matrix requires reporting export to multiple formats, including PDF, Excel, delimited text and XML.",
  "purposeNote": "Users can export authorized information while TICVAI maintains control and auditability over data extraction.",
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
  "apis": [],
  "entryState": {
   "preloaded": [
    "Export ID",
    "Report",
    "Requested By",
    "Site",
    "Format",
    "Requested Time"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-045"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 45. 0 of 11 labels bound to a contract property; 19 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow approved systems to receive reporting information programmatically. This supports the requirement for report export/access through APIs.",
  "purposeNote": "External approved systems can consume governed reporting data without receiving unrestricted access to TICVAI's operational database.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-046"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 46. 0 of 0 labels bound to a contract property; 17 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide centralized security for reports, dashboards and analytical information. The matrix specifically requires reporting access based on group rights, operating-area rights and user access rights.",
  "purposeNote": "Sharing, export and subscription cannot be used to bypass the underlying TICVAI permission model.",
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
   "regions": []
  },
  "states": {
   "loading": "The report access sharing list.",
   "error": "Could not load. Names which read failed and leaves the report access sharing untouched.",
   "emptyFirstRun": "No report access sharing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the report access sharing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-047"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Monitor scheduled report execution and distribution and provide operational management of failures.",
  "purposeNote": "Administrators can identify and resolve report-generation and distribution failures without reviewing technical server logs.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-048"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 48. 0 of 10 labels bound to a contract property; 22 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Maintain complete traceability of reporting activity. The source matrix requires report logs and audit reporting for sales history.",
  "purposeNote": "Authorized administrators and auditors can reconstruct the history of relevant reporting activity.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-049"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 49. 0 of 8 labels bound to a contract property; 22 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure retention separately for; Define) and no display directory — it is settings, not a population",
  "purpose": "Control the lifecycle of reports, generated files and historical analytical data. The reporting-platform specification requires long-term reporting history together with archival and retrieval capability.",
  "purposeNote": "Historical reporting content can be governed, archived and retrieved according to configured organizational and regulatory policies.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-050"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 50. 0 of 0 labels bound to a contract property; 14 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
