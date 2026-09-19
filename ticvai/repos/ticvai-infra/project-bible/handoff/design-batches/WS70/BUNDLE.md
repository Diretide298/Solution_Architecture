# WS70 — Unified BI Reporting and AI Analytics Platform board 9

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
| `ANL-051` | AI Analytics Command Center | listDetail | 0 | 0 | — |
| `ANL-052` | Ask TICVAI — Natural Language Analytics | listDetail | 0 | 0 | — |
| `ANL-053` | AI-Generated Dashboard Studio | listDetail | 0 | 0 | — |
| `ANL-054` | AI Report Generator | listDetail | 0 | 0 | — |
| `ANL-055` | Anomaly Detection Center | listDetail | 0 | 0 | — |
| `ANL-056` | Root-Cause Analysis Explorer | listDetail | 0 | 0 | — |
| `ANL-057` | Forecasting & Predictive Analytics Studio | configEditor | 0 | 0 | — |
| `ANL-058` | AI Recommendation & Next-Best-Action Center | listDetail | 0 | 0 | — |
| `ANL-059` | AI Insight History, Evidence & Explainability | configEditor | 0 | 0 | — |
| `ANL-060` | AI Analytics Governance & Model Control | listDetail | 0 | 0 | — |

## Thin screens in this batch

**ANL-051, ANL-052, ANL-053, ANL-054, ANL-055, ANL-056, ANL-058, ANL-060 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ANL-051",
  "name": "AI Analytics Command Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.1",
   "page": 109
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-analytics-command-center-anl-051",
   "component": "apps/venue-management-web/src/routes/analytics/AiAnalyticsCommandCenter.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide a centralized landing page for all AI-generated analytical intelligence across TICVAI.",
  "purposeNote": "Management can review prioritized AI intelligence across all authorized business domains from one screen.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 109 §Display"
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
       "label": "Every analytics",
       "columns": [
        "Executive Insights",
        "Revenue Insights",
        "Operations Insights",
        "Customer Insights",
        "Finance Insights",
        "Marketing Insights",
        "Access Insights",
        "Membership/Loyalty Insights",
        "Forecasts",
        "Anomalies",
        "Opportunities",
        "Risks",
        "New AI Insights",
        "Critical Insights",
        "Opportunities Detected",
        "Risks Detected",
        "Active Anomalies",
        "Forecast Alerts",
        "Recommendations Pending Review",
        "AI Queries Today"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 109 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected analytics",
       "bindsTo": null,
       "columns": [
        "Executive Insights",
        "Revenue Insights",
        "Operations Insights",
        "Customer Insights",
        "Finance Insights",
        "Marketing Insights",
        "Access Insights",
        "Membership/Loyalty Insights",
        "Forecasts",
        "Anomalies",
        "Opportunities",
        "Risks",
        "New AI Insights",
        "Critical Insights",
        "Opportunities Detected",
        "Risks Detected",
        "Active Anomalies",
        "Forecast Alerts",
        "Recommendations Pending Review",
        "AI Queries Today"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Revenue Opportunity”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 109 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The analytics list.",
   "error": "Could not load. Names which read failed and leaves the analytics untouched.",
   "emptyFirstRun": "No analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Executive Insights",
    "Revenue Insights",
    "Operations Insights",
    "Customer Insights",
    "Finance Insights",
    "Marketing Insights"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-051"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 109. 0 of 20 labels bound to a contract property; 20 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-052",
    "ANL-053",
    "ANL-054",
    "ANL-055",
    "ANL-056",
    "ANL-057",
    "ANL-058",
    "ANL-059",
    "ANL-060"
   ],
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Back to Executive Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-060",
     "trigger": "AI Analytics Governance & Model Control",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-052",
     "trigger": "Ask TICVAI — Natural Language Analytics",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-053",
     "trigger": "AI-Generated Dashboard Studio",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-054",
     "trigger": "AI Report Generator",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-055",
     "trigger": "Anomaly Detection Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-056",
     "trigger": "Root-Cause Analysis Explorer",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-057",
     "trigger": "Forecasting & Predictive Analytics Studio",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-058",
     "trigger": "AI Recommendation & Next-Best-Action Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-059",
     "trigger": "AI Insight History, Evidence & Explainability",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
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
  "id": "ANL-052",
  "name": "Ask TICVAI — Natural Language Analytics",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.2",
   "page": 110
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ask-ticvai-natural-language-analytics-anl-052",
   "component": "apps/venue-management-web/src/routes/analytics/AskTicvaiNaturalLanguageAnalytics.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to query TICVAI business information using normal language instead of manually building reports.",
  "purposeNote": "Authorized business users can obtain governed analytics without knowing report names, database fields, SQL, or Power BI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 110"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 110"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The ask ticvai natural list.",
   "error": "Could not load. Names which read failed and leaves the ask ticvai natural untouched.",
   "emptyFirstRun": "No ask ticvai natural yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ask ticvai natural are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-052"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 110. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-051"
   ],
   "exitTo": [
    "ANL-051"
   ],
   "transitions": [
    {
     "to": "ANL-051",
     "trigger": "Back to AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
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
  "id": "ANL-053",
  "name": "AI-Generated Dashboard Studio",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.3",
   "page": 111
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-generated-dashboard-studio-anl-053",
   "component": "apps/venue-management-web/src/routes/analytics/AiGeneratedDashboardStudio.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to generate dashboards from natural-language requests.",
  "purposeNote": "Users can convert natural-language analytical requirements into governed dashboard configurations.",
  "gaps": [
   {
    "operation": null,
    "why": "**AI-Generated Dashboard Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 111"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 111"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The ai-generated list.",
   "error": "Could not load. Names which read failed and leaves the ai-generated untouched.",
   "emptyFirstRun": "No ai-generated yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ai-generated are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-053"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 111. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-051"
   ],
   "exitTo": [
    "ANL-051"
   ],
   "transitions": [
    {
     "to": "ANL-051",
     "trigger": "Back to AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
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
  "id": "ANL-054",
  "name": "AI Report Generator",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.4",
   "page": 112
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-report-generator-anl-054",
   "component": "apps/venue-management-web/src/routes/analytics/AiReportGenerator.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Generate detailed reports from natural-language instructions.",
  "purposeNote": "AI-generated reports use the same approved semantic model, permissions, calculations and governance rules as manually created reports.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 112 §Show"
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
       "label": "Every report generator",
       "columns": [
        "Selected Dataset",
        "Fields",
        "Filters",
        "Grouping",
        "Calculations",
        "Sort",
        "Output"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 112 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected report generator",
       "bindsTo": null,
       "columns": [
        "Selected Dataset",
        "Fields",
        "Filters",
        "Grouping",
        "Calculations",
        "Sort",
        "Output"
       ],
       "notes": "The pack groups this record's detail under its own headings: “User asks”, “Dimensions”, “Measures”, “Relationship to Board 3”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 112 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report generator list.",
   "error": "Could not load. Names which read failed and leaves the report generator untouched.",
   "emptyFirstRun": "No report generator yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the report generator are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Selected Dataset",
    "Fields",
    "Filters",
    "Grouping",
    "Calculations",
    "Sort"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-054"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 112. 0 of 7 labels bound to a contract property; 7 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-051"
   ],
   "exitTo": [
    "ANL-051"
   ],
   "transitions": [
    {
     "to": "ANL-051",
     "trigger": "Back to AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
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
  "id": "ANL-055",
  "name": "Anomaly Detection Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.5",
   "page": 113
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/anomaly-detection-center-anl-055",
   "component": "apps/venue-management-web/src/routes/analytics/AnomalyDetectionCenter.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each Anomaly Displays) and no metric row",
  "purpose": "Automatically identify unusual behavior across TICVAI data without requiring users to manually monitor every KPI.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 113 §Each Anomaly Displays"
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
       "label": "Every anomaly detection",
       "columns": [
        "KPI",
        "Expected Range",
        "Actual Value",
        "Variance",
        "Severity",
        "Start Time",
        "Duration",
        "Affected Site",
        "Affected Domain",
        "Confidence"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 113 §Each Anomaly Displays"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected anomaly detection",
       "bindsTo": null,
       "columns": [
        "KPI",
        "Expected Range",
        "Actual Value",
        "Variance",
        "Severity",
        "Start Time",
        "Duration",
        "Affected Site",
        "Affected Domain",
        "Confidence"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Detect abnormal patterns involving”, “High Refund Anomaly”, “Detection Methods”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 113 §Each Anomaly Displays"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The anomaly detection list.",
   "error": "Could not load. Names which read failed and leaves the anomaly detection untouched.",
   "emptyFirstRun": "No anomaly detection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the anomaly detection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "KPI",
    "Expected Range",
    "Actual Value",
    "Variance",
    "Severity",
    "Start Time"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-055"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 113. 0 of 10 labels bound to a contract property; 10 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-051"
   ],
   "exitTo": [
    "ANL-051"
   ],
   "transitions": [
    {
     "to": "ANL-051",
     "trigger": "Back to AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
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
  "id": "ANL-056",
  "name": "Root-Cause Analysis Explorer",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.6",
   "page": 114
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/root-cause-analysis-explorer-anl-056",
   "component": "apps/venue-management-web/src/routes/analytics/RootCauseAnalysisExplorer.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Help users understand why a KPI changed. This is one of the most important AI capabilities in the entire platform.",
  "purposeNote": "Users can move from detecting a KPI change to understanding the strongest supported contributing factors.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 114"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 114"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The root-cause analysis list.",
   "error": "Could not load. Names which read failed and leaves the root-cause analysis untouched.",
   "emptyFirstRun": "No root-cause analysis yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the root-cause analysis are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-056"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 114. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-051"
   ],
   "exitTo": [
    "ANL-051"
   ],
   "transitions": [
    {
     "to": "ANL-051",
     "trigger": "Back to AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
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
  "id": "ANL-057",
  "name": "Forecasting & Predictive Analytics Studio",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.7",
   "page": 116
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/forecasting-predictive-analytics-studio-anl-057",
   "component": "apps/venue-management-web/src/routes/analytics/ForecastingPredictiveAnalyticsStudio.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Provide configurable forward-looking analytics across business domains.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Ticket Sales, Membership Renewals, Customer Churn. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Support forecasts for"
   },
   {
    "operation": null,
    "why": "**Forecasting & Predictive Analytics Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Next Hour",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Today",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tomorrow",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Next 7 Days",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Month End",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Quarter",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Custom",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ticket Sales",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Support forecasts for"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership Renewals",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Support forecasts for"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Churn",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 116 §Support forecasts for"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The forecasting predictive analytics configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the forecasting predictive analytics untouched.",
   "emptyFirstRun": "No forecasting predictive analytics configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-057"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 116. 0 of 0 labels bound to a contract property; 10 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-051"
   ],
   "exitTo": [
    "ANL-051"
   ],
   "transitions": [
    {
     "to": "ANL-051",
     "trigger": "Back to AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
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
  "id": "ANL-058",
  "name": "AI Recommendation & Next-Best-Action Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.8",
   "page": 117
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-recommendation-next-best-action-center-anl-058",
   "component": "apps/venue-management-web/src/routes/analytics/AiRecommendationNextBestActionCenter.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert analytical insights into prioritized business recommendations.",
  "purposeNote": "Recommendations are prioritized, explainable and measurable rather than presented as generic AI suggestions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 117"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 117"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The recommendation next-best-action list.",
   "error": "Could not load. Names which read failed and leaves the recommendation next-best-action untouched.",
   "emptyFirstRun": "No recommendation next-best-action yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation next-best-action are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-058"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 117. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-051"
   ],
   "exitTo": [
    "ANL-051"
   ],
   "transitions": [
    {
     "to": "ANL-051",
     "trigger": "Back to AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
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
  "id": "ANL-059",
  "name": "AI Insight History, Evidence & Explainability",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.9",
   "page": 118
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-insight-history-evidence-explainability-anl-059",
   "component": "apps/venue-management-web/src/routes/analytics/AiInsightHistoryEvidenceExplainability.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Create a full governance trail for AI-generated analytics and recommendations.",
  "purposeNote": "AI analytics remain auditable and traceable to supporting TICVAI data.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Who asked",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 118 §Capture"
      },
      {
       "kind": "textField",
       "label": "What data was accessed",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 118 §Capture"
      },
      {
       "kind": "textField",
       "label": "What answer was generated",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 118 §Capture"
      },
      {
       "kind": "textField",
       "label": "Whether it was exported/shared",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 118 §Capture"
      },
      {
       "kind": "textField",
       "label": "Whether recommendation was accepted",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 118 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The insight history evidence configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the insight history evidence untouched.",
   "emptyFirstRun": "No insight history evidence configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-059"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 118. 0 of 0 labels bound to a contract property; 5 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-051"
   ],
   "exitTo": [
    "ANL-051"
   ],
   "transitions": [
    {
     "to": "ANL-051",
     "trigger": "Back to AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
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
  "id": "ANL-060",
  "name": "AI Analytics Governance & Model Control",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "9",
   "number": "9.10",
   "page": 119
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-analytics-governance-model-control-anl-060",
   "component": "apps/venue-management-web/src/routes/analytics/AiAnalyticsGovernanceModelControl.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Track) and no metric row",
  "purpose": "Provide administrators with centralized control over how AI may access and use TICVAI analytics. This screen is critical because Board 9 should not give an LLM unrestricted access to the TICVAI database.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 119 §Display"
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
       "label": "Every analytics governance model",
       "columns": [
        "AI Service",
        "Model",
        "Use Case",
        "Status",
        "Consumption",
        "Cost",
        "Response Time",
        "Error Rate",
        "Queries",
        "Tokens/Units",
        "User",
        "Tenant",
        "Module"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 119 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected analytics governance model",
       "bindsTo": null,
       "columns": [
        "AI Service",
        "Model",
        "Use Case",
        "Status",
        "Consumption",
        "Cost",
        "Response Time",
        "Error Rate",
        "Queries",
        "Tokens/Units",
        "User",
        "Tenant",
        "Module"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Administrators can enable/disable”, “User”, “Ask TICVAI”, “Analytics / Data Platform”, “Authorized Result”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 119 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** ↓. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 119 §Permission & Governance Layer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The analytics governance model list.",
   "error": "Could not load. Names which read failed and leaves the analytics governance model untouched.",
   "emptyFirstRun": "No analytics governance model yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the analytics governance model are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "AI Service",
    "Model",
    "Use Case",
    "Status",
    "Consumption",
    "Cost"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-060"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 119. 0 of 13 labels bound to a contract property; 31 of 84 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ANL-051"
   ],
   "exitTo": [
    "ANL-051"
   ],
   "transitions": [
    {
     "to": "ANL-051",
     "trigger": "Back to AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026",
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
