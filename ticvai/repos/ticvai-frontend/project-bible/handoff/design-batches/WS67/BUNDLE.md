# WS67 — Unified BI Reporting and AI Analytics Platform board 2

**10 screens · 11 operations · 12 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `REPORT_MANAGE, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ANL-021` | Dashboard Library | listDetail | 4 | 0 | — |
| `ANL-022` | Dashboard Creation Wizard | configEditor | 1 | 0 | — |
| `ANL-023` | Drag-and-Drop Dashboard Canvas | listDetail | 4 | 0 | — |
| `ANL-024` | Widget & Visualization Library | listDetail | 1 | 0 | — |
| `ANL-025` | KPI Builder | configEditor | 2 | 0 | — |
| `ANL-026` | Targets, Thresholds & KPI Status Rules | listDetail | 2 | 0 | — |
| `ANL-027` | Data & Filter Configuration | configEditor | 2 | 0 | — |
| `ANL-028` | Drill-Down & Interaction Designer | configEditor | 1 | 0 | — |
| `ANL-029` | Dashboard Access, Publishing & Versioning | listDetail | 1 | 0 | — |
| `ANL-030` | Dashboard Preview, Validation & Health | listDetail | 3 | 0 | — |

## Thin screens in this batch

**ANL-021, ANL-023, ANL-024, ANL-029, ANL-030 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ANL-021",
  "name": "Dashboard Library",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.1",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/dashboard-library-anl-021",
   "component": "apps/venue-management-web/src/routes/analytics/DashboardLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-022",
    "ANL-023",
    "ANL-024",
    "ANL-025",
    "ANL-026",
    "ANL-027",
    "ANL-028",
    "ANL-029",
    "ANL-030"
   ],
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Back to Executive Command Center",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true,
     "carries": [
      "dashboardId",
      "reportId"
     ]
    },
    {
     "to": "ANL-030",
     "trigger": "Dashboard Preview, Validation & Health",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "carries": [
      "dashboardId"
     ]
    },
    {
     "to": "ANL-022",
     "trigger": "Dashboard Creation Wizard",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ANL-023",
     "trigger": "Drag-and-Drop Dashboard Canvas",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "carries": [
      "dashboardId"
     ]
    },
    {
     "to": "ANL-024",
     "trigger": "Widget & Visualization Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ANL-025",
     "trigger": "KPI Builder",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ANL-026",
     "trigger": "Targets, Thresholds & KPI Status Rules",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ANL-027",
     "trigger": "Data & Filter Configuration",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "carries": [
      "dashboardId"
     ]
    },
    {
     "to": "ANL-028",
     "trigger": "Drill-Down & Interaction Designer",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "carries": [
      "dashboardId"
     ]
    },
    {
     "to": "ANL-029",
     "trigger": "Dashboard Access, Publishing & Versioning",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "carries": [
      "dashboardId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can search, filter, manage, clone and govern dashboards from one central catalogue.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display dashboard cards/table containing; Dashboard Categories; Dashboard Types) and no metric row",
  "purpose": "Provide a centralized catalogue for all standard, custom, AI-generated and embedded TICVAI dashboards.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 14 §Display dashboard cards/table containing"
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
       "label": "Every record",
       "columns": [
        "Dashboard Name",
        "Dashboard ID",
        "Category",
        "Business Domain",
        "Owner",
        "Sites/Venues",
        "Audience/Role",
        "Status",
        "Version",
        "Last Modified",
        "Last Published",
        "Usage Count",
        "Data Refresh Status",
        "Executive",
        "Operations",
        "Finance",
        "Sales",
        "Ticketing",
        "Access Control",
        "CRM",
        "Marketing",
        "Membership",
        "Loyalty",
        "F&B",
        "Retail",
        "Inventory",
        "Resources",
        "Custom",
        "System Dashboard — TICVAI standard dashboard",
        "Custom Dashboard — customer-created",
        "AI-Generated Dashboard — generated through AI"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 14 §Display dashboard cards/table containing"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected record",
       "bindsTo": null,
       "columns": [
        "Dashboard Name",
        "Dashboard ID",
        "Category",
        "Business Domain",
        "Owner",
        "Sites/Venues",
        "Audience/Role",
        "Status",
        "Version",
        "Last Modified",
        "Last Published",
        "Usage Count",
        "Data Refresh Status",
        "Executive",
        "Operations",
        "Finance",
        "Sales",
        "Ticketing",
        "Access Control",
        "CRM",
        "Marketing",
        "Membership",
        "Loyalty",
        "F&B",
        "Retail",
        "Inventory",
        "Resources",
        "Custom",
        "System Dashboard — TICVAI standard dashboard",
        "Custom Dashboard — customer-created",
        "AI-Generated Dashboard — generated through AI"
       ],
       "notes": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 14 §Display dashboard cards/table containing"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The record list.",
   "error": "Could not load. Names which read failed and leaves the record untouched.",
   "emptyFirstRun": "No record yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the record are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDashboards",
    "contract": "reporting",
    "purpose": "The library",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Open one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createDashboard",
    "contract": "reporting",
    "purpose": "Start a new one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listDashboards"
    ]
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   }
  ],
  "entryState": {
   "preloaded": [
    "Dashboard Name",
    "Dashboard ID",
    "Category",
    "Business Domain",
    "Owner",
    "Sites/Venues"
   ],
   "params": [
    {
     "name": "dashboardId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-021",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-021"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 14. 0 of 31 labels bound to a contract property; 31 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-022",
  "name": "Dashboard Creation Wizard",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.2",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/dashboard-creation-wizard-anl-022",
   "component": "apps/venue-management-web/src/routes/analytics/DashboardCreationWizard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-021"
   ],
   "exitTo": [
    "ANL-021"
   ],
   "transitions": [
    {
     "to": "ANL-021",
     "trigger": "Back to Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true,
     "carries": [
      "dashboardId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can create the initial dashboard configuration without technical/database knowledge.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Select; Select one or multiple domains) and no display directory — it is settings, not a population",
  "purpose": "Guide users through creation of a new dashboard.",
  "gaps": [
   {
    "operation": null,
    "why": "**Dashboard Creation Wizard declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Dashboard Name",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Category",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business Domain",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dashboard Owner",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tags",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default Currency",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "textField",
       "label": "Step 2 — Scope",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Select"
      },
      {
       "kind": "selectField",
       "label": "Organization",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Select"
      },
      {
       "kind": "selectField",
       "label": "Site(s)",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Select"
      },
      {
       "kind": "selectField",
       "label": "Venue(s)",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Select"
      },
      {
       "kind": "selectField",
       "label": "Attraction(s)",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Select"
      },
      {
       "kind": "selectField",
       "label": "Business Unit(s)",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Select"
      },
      {
       "kind": "textField",
       "label": "Step 3 — Data Domains",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Select"
      },
      {
       "kind": "selectField",
       "label": "Queue • Accreditation",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Select one or multiple domains"
      },
      {
       "kind": "textField",
       "label": "Step 4 — Template",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 15 §Select one or multiple domains"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The creation wizard configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the creation wizard untouched.",
   "emptyFirstRun": "No creation wizard configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createDashboard",
    "contract": "reporting",
    "purpose": "Create one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listDashboards"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-022",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-022"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 18 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-023",
  "name": "Drag-and-Drop Dashboard Canvas",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.3",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/drag-and-drop-dashboard-canvas-anl-023",
   "component": "apps/venue-management-web/src/routes/analytics/DragAndDropDashboardCanvas.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-021"
   ],
   "exitTo": [
    "ANL-021"
   ],
   "transitions": [
    {
     "to": "ANL-021",
     "trigger": "Back to Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true,
     "carries": [
      "dashboardId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A business analyst can visually construct a dashboard without coding.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the main visual workspace for dashboard construction.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 16"
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
       "impliedBy": "updateDashboard",
       "label": "Save dashboard",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getDashboard",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateDashboard"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The drag-and-drop canvas list.",
   "error": "Could not load. Names which read failed and leaves the drag-and-drop canvas untouched.",
   "emptyFirstRun": "No drag-and-drop canvas yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the drag-and-drop canvas are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateDashboard",
    "contract": "reporting",
    "purpose": "Lay it out",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getDashboard",
     "listDashboards"
    ]
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "The dashboard being edited",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "deleteDashboard",
    "contract": "reporting",
    "purpose": "Archive this dashboard",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-023",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-023"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "dashboardId",
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
 },
 {
  "id": "ANL-024",
  "name": "Widget & Visualization Library",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.4",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/widget-visualization-library-anl-024",
   "component": "apps/venue-management-web/src/routes/analytics/WidgetVisualizationLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-021"
   ],
   "exitTo": [
    "ANL-021"
   ],
   "transitions": [
    {
     "to": "ANL-021",
     "trigger": "Back to Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can search the component library and drag supported visualizations directly onto the dashboard canvas.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§KPI Components) and no metric row",
  "purpose": "Provide reusable visual components for dashboard construction.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 17 §KPI Components"
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
       "label": "Every widget visualization",
       "columns": [
        "KPI Card",
        "Target Card",
        "Variance Card",
        "Scorecard",
        "Gauge",
        "Progress Indicator"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 17 §KPI Components"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected widget visualization",
       "bindsTo": null,
       "columns": [
        "KPI Card",
        "Target Card",
        "Variance Card",
        "Scorecard",
        "Gauge",
        "Progress Indicator"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Chart Components”, “Operational Components”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 17 §KPI Components"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The widget visualization list.",
   "error": "Could not load. Names which read failed and leaves the widget visualization untouched.",
   "emptyFirstRun": "No widget visualization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the widget visualization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSemanticModel",
    "contract": "reporting",
    "purpose": "What a widget can be bound to",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "KPI Card",
    "Target Card",
    "Variance Card",
    "Scorecard",
    "Gauge",
    "Progress Indicator"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-024",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-024"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 17. 0 of 6 labels bound to a contract property; 6 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-025",
  "name": "KPI Builder",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.5",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/kpi-builder-anl-025",
   "component": "apps/venue-management-web/src/routes/analytics/KpiBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-021"
   ],
   "exitTo": [
    "ANL-021"
   ],
   "transitions": [
    {
     "to": "ANL-021",
     "trigger": "Back to Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can centrally define reusable KPIs and ensure the same KPI calculation is used across TICVAI dashboards.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Define whether) and no display directory — it is settings, not a population",
  "purpose": "Allow authorized business users to create standardized enterprise KPIs.",
  "gaps": [
   {
    "operation": null,
    "why": "**KPI Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "KPI Name",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "KPI Code",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business Domain",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Data Source",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Measure",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Formula",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Aggregation",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Unit",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Decimal Precision",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective Date",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Higher = Better",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Define whether"
      },
      {
       "kind": "selectField",
       "label": "Lower = Better",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Define whether"
      },
      {
       "kind": "selectField",
       "label": "Revenue ↑",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Define whether"
      },
      {
       "kind": "selectField",
       "label": "Conversion ↑",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Define whether"
      },
      {
       "kind": "selectField",
       "label": "Refund Rate ↓",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Define whether"
      },
      {
       "kind": "textField",
       "label": "Gate Rejection Rate ↓",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Define whether"
      },
      {
       "kind": "selectField",
       "label": "Queue Time ↓",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 18 §Define whether"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The kpi configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the kpi untouched.",
   "emptyFirstRun": "No kpi configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listKpis",
    "contract": "reporting",
    "purpose": "KPIs already defined",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createKpi",
    "contract": "reporting",
    "purpose": "Define one, for everywhere",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listKpis",
     "getKpiValues"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-025",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-025"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 21 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-026",
  "name": "Targets, Thresholds & KPI Status Rules",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.6",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/targets-thresholds-kpi-status-rules-anl-026",
   "component": "apps/venue-management-web/src/routes/analytics/TargetsThresholdsKpiStatusRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-021"
   ],
   "exitTo": [
    "ANL-021"
   ],
   "transitions": [
    {
     "to": "ANL-021",
     "trigger": "Back to Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "KPI status and alert behavior are calculated dynamically using centrally configured business thresholds.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§For each KPI) and no metric row",
  "purpose": "Configure how TICVAI determines whether KPI performance is healthy, warning or critical.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: If Critical → Generate Alert, Notify responsible user, Create operational task, Trigger AI analysis. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 19 §Users can configure"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 19 §For each KPI"
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
       "label": "Every targets thresholds kpi",
       "columns": [
        "Target",
        "Minimum",
        "Maximum",
        "Warning Threshold",
        "Critical Threshold",
        "Benchmark",
        "Tolerance",
        "Evaluation Frequency"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 19 §For each KPI"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected targets thresholds kpi",
       "bindsTo": null,
       "columns": [
        "Target",
        "Minimum",
        "Maximum",
        "Warning Threshold",
        "Critical Threshold",
        "Benchmark",
        "Tolerance",
        "Evaluation Frequency"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Capacity Utilization”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 19 §For each KPI"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "If Critical → Generate Alert",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 19 §Users can configure"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify responsible user",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 19 §Users can configure"
      },
      {
       "kind": "secondaryButton",
       "label": "Create operational task",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 19 §Users can configure"
      },
      {
       "kind": "secondaryButton",
       "label": "Trigger AI analysis",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 19 §Users can configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The targets thresholds kpi list.",
   "error": "Could not load. Names which read failed and leaves the targets thresholds kpi untouched.",
   "emptyFirstRun": "No targets thresholds kpi yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the targets thresholds kpi are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setKpiTargets",
    "contract": "reporting",
    "purpose": "Targets and thresholds",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getKpiValues"
    ]
   },
   {
    "operationId": "listKpis",
    "contract": "reporting",
    "purpose": "The KPI being targeted",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Target",
    "Minimum",
    "Maximum",
    "Warning Threshold",
    "Critical Threshold",
    "Benchmark"
   ],
   "params": [
    {
     "name": "kpiId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-026",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-026"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 19. 0 of 8 labels bound to a contract property; 12 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-027",
  "name": "Data & Filter Configuration",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.7",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/data-filter-configuration-anl-027",
   "component": "apps/venue-management-web/src/routes/analytics/DataFilterConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-021"
   ],
   "exitTo": [
    "ANL-021"
   ],
   "transitions": [
    {
     "to": "ANL-021",
     "trigger": "Back to Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true,
     "carries": [
      "dashboardId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can configure dashboard data and filters without direct access to underlying production databases.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select; Configure) and no display directory — it is settings, not a population",
  "purpose": "Control what data a dashboard/widget uses and how users can filter it.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search data filter",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Filters may be"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Global",
        "Widget-level",
        "Mandatory",
        "Optional",
        "Hidden",
        "Defaulted"
       ],
       "notes": "The pack filters this screen by global, widget-level, mandatory, optional, hidden, defaulted — which are present is a decision the pack already made.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Filters may be"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Data Domain",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Select"
      },
      {
       "kind": "selectField",
       "label": "Dataset",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Select"
      },
      {
       "kind": "selectField",
       "label": "Measure",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Select"
      },
      {
       "kind": "selectField",
       "label": "Dimension",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Select"
      },
      {
       "kind": "selectField",
       "label": "Aggregation",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Select"
      },
      {
       "kind": "selectField",
       "label": "Date Field",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Select"
      },
      {
       "kind": "selectField",
       "label": "Relationship",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Select"
      },
      {
       "kind": "selectField",
       "label": "Calculation",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Select"
      },
      {
       "kind": "selectField",
       "label": "Date Range",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Site",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Attraction",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer Segment",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 20 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data filter configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the data filter untouched.",
   "emptyFirstRun": "No data filter configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoResults": "The filter narrowed it and the data filter are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSemanticModel",
    "contract": "reporting",
    "purpose": "Datasets and fields to filter on",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updateDashboard",
    "contract": "reporting",
    "purpose": "Save the filters",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getDashboard",
     "listDashboards"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-027",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-027"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 20. 0 of 6 labels bound to a contract property; 22 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "dashboardId",
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
 },
 {
  "id": "ANL-028",
  "name": "Drill-Down & Interaction Designer",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.8",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/drill-down-interaction-designer-anl-028",
   "component": "apps/venue-management-web/src/routes/analytics/DrillDownInteractionDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-021"
   ],
   "exitTo": [
    "ANL-021"
   ],
   "transitions": [
    {
     "to": "ANL-021",
     "trigger": "Back to Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true,
     "carries": [
      "dashboardId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Dashboard designers can visually configure analytical navigation without custom development.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Define) and no display directory — it is settings, not a population",
  "purpose": "Configure how users move from high-level KPIs into deeper analytics.",
  "gaps": [
   {
    "operation": null,
    "why": "**Drill-Down & Interaction Designer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Click behavior",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 22 §Define"
      },
      {
       "kind": "selectField",
       "label": "Cross-filtering",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 22 §Define"
      },
      {
       "kind": "selectField",
       "label": "Drill-down",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 22 §Define"
      },
      {
       "kind": "selectField",
       "label": "Drill-up",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 22 §Define"
      },
      {
       "kind": "selectField",
       "label": "Drill-through",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 22 §Define"
      },
      {
       "kind": "selectField",
       "label": "Tooltip",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 22 §Define"
      },
      {
       "kind": "selectField",
       "label": "Detail page",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 22 §Define"
      },
      {
       "kind": "selectField",
       "label": "Related dashboard",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 22 §Define"
      },
      {
       "kind": "selectField",
       "label": "Underlying report",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 22 §Define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The drill-down interaction designer configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the drill-down interaction designer untouched.",
   "emptyFirstRun": "No drill-down interaction designer configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateDashboard",
    "contract": "reporting",
    "purpose": "Drill-down behaviour",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getDashboard",
     "listDashboards"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-028",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-028"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 9 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "dashboardId",
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
 },
 {
  "id": "ANL-029",
  "name": "Dashboard Access, Publishing & Versioning",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.9",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/dashboard-access-publishing-versioning-anl-029",
   "component": "apps/venue-management-web/src/routes/analytics/DashboardAccessPublishingVersioning.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-021"
   ],
   "exitTo": [
    "ANL-021"
   ],
   "transitions": [
    {
     "to": "ANL-021",
     "trigger": "Back to Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true,
     "carries": [
      "dashboardId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Only authorized and approved dashboard configurations become available to production users, with complete version history.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Govern who can access dashboards and how dashboard changes reach production.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 23 §Display"
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
       "label": "Every access publishing versioning",
       "columns": [
        "Version Number",
        "Changed By",
        "Date/Time",
        "Change Description",
        "Approval Status",
        "Published Version"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 23 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access publishing versioning",
       "bindsTo": null,
       "columns": [
        "Version Number",
        "Changed By",
        "Date/Time",
        "Change Description",
        "Approval Status",
        "Published Version"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Assign dashboards to”, “Administer”, “Rollback”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 23 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access publishing versioning list.",
   "error": "Could not load. Names which read failed and leaves the access publishing versioning untouched.",
   "emptyFirstRun": "No access publishing versioning yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access publishing versioning are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateDashboard",
    "contract": "reporting",
    "purpose": "Publish and version",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getDashboard",
     "listDashboards"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Version Number",
    "Changed By",
    "Date/Time",
    "Change Description",
    "Approval Status",
    "Published Version"
   ],
   "params": [
    {
     "name": "dashboardId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-029",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-029"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 23. 0 of 6 labels bound to a contract property; 6 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-030",
  "name": "Dashboard Preview, Validation & Health",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "2",
   "number": "2.10",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/dashboard-preview-validation-health-anl-030",
   "component": "apps/venue-management-web/src/routes/analytics/DashboardPreviewValidationHealth.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-021"
   ],
   "exitTo": [
    "ANL-021"
   ],
   "transitions": [
    {
     "to": "ANL-021",
     "trigger": "Back to Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true,
     "carries": [
      "dashboardId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The system prevents dashboards containing critical configuration or security errors from being published.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Validate dashboards before publication and monitor their technical/analytical health afterward.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 23 §Display"
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
       "label": "Every preview validation health",
       "columns": [
        "Data Last Refreshed",
        "Refresh Frequency",
        "Dataset Status",
        "Query Performance",
        "Widget Load Time",
        "Failed Widgets",
        "API Status",
        "User Count",
        "Usage Frequency"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 23 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected preview validation health",
       "bindsTo": null,
       "columns": [
        "Data Last Refreshed",
        "Refresh Frequency",
        "Dataset Status",
        "Query Performance",
        "Widget Load Time",
        "Failed Widgets",
        "API Status",
        "User Count",
        "Usage Frequency"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Preview Modes”, “Ready to Publish”, “Issues Detected”, “The end user should experience”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 23 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The preview validation health list.",
   "error": "Could not load. Names which read failed and leaves the preview validation health untouched.",
   "emptyFirstRun": "No preview validation health yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the preview validation health are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Preview",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAnalyticsPipelines",
    "contract": "reporting",
    "purpose": "Whether its data is fresh",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   }
  ],
  "entryState": {
   "preloaded": [
    "Data Last Refreshed",
    "Refresh Frequency",
    "Dataset Status",
    "Query Performance",
    "Widget Load Time",
    "Failed Widgets"
   ],
   "params": [
    {
     "name": "dashboardId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-030",
   "workshopBoard": "wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-030"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 23. 0 of 9 labels bound to a contract property; 9 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createDashboard": {
  "method": "POST",
  "path": "/dashboards",
  "contract": "reporting",
  "summary": "Create a dashboard",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateDashboardRequest",
  "responds": "Dashboard"
 },
 "createKpi": {
  "method": "POST",
  "path": "/kpis",
  "contract": "reporting",
  "summary": "Define a KPI once, for everywhere",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "KpiDefinition",
  "responds": "KpiDefinition"
 },
 "deleteDashboard": {
  "method": "DELETE",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Archive a dashboard",
  "permission": "REPORT_MANAGE",
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
  "requestBody": null,
  "responds": null
 },
 "getDashboard": {
  "method": "GET",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Read a dashboard with tile data",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "refresh",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DashboardData"
 },
 "getSemanticModel": {
  "method": "GET",
  "path": "/semantic-model",
  "contract": "reporting",
  "summary": "The business data catalogue reports are built from",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SemanticModel"
 },
 "listAnalyticsPipelines": {
  "method": "GET",
  "path": "/analytics-pipelines",
  "contract": "reporting",
  "summary": "Data sources, refresh state and freshness",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AnalyticsPipeline"
 },
 "listDashboards": {
  "method": "GET",
  "path": "/dashboards",
  "contract": "reporting",
  "summary": "List dashboards",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "module",
    "in": "query",
    "required": false
   },
   {
    "name": "includeArchived",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "Dashboard"
 },
 "listKpis": {
  "method": "GET",
  "path": "/kpis",
  "contract": "reporting",
  "summary": "The enterprise KPI library",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "KpiDefinition"
 },
 "recordDashboardView": {
  "method": "POST",
  "path": "/dashboards/{dashboardId}/views",
  "contract": "reporting",
  "summary": "Record that a dashboard was opened",
  "permission": "REPORT_VIEW_VENUE",
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
  "responds": null
 },
 "setKpiTargets": {
  "method": "PUT",
  "path": "/kpis/{kpiId}/targets",
  "contract": "reporting",
  "summary": "Targets, thresholds and what red means",
  "permission": "REPORT_MANAGE",
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
  "requestBody": null,
  "responds": "KpiTarget"
 },
 "updateDashboard": {
  "method": "PUT",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Update a dashboard",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateDashboardRequest",
  "responds": "Dashboard"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Aggregation": {
  "type": "string",
  "enum": [
   "none",
   "count",
   "countDistinct",
   "sum",
   "average",
   "min",
   "max"
  ]
 },
 "AnalyticsPipeline": {
  "type": "object",
  "x-ticvai-persistence": "reporting.pipeline",
  "description": "BI board 10.7. **Freshness decides whether a dashboard can be trusted.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "sourceKind": {
    "type": "string"
   },
   "datasets": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "schedule": {
    "type": "string",
    "nullable": true
   },
   "lastRunAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastSuccessAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "freshnessMinutes": {
    "type": "integer",
    "nullable": true
   },
   "expectedFreshnessMinutes": {
    "type": "integer",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "healthy",
     "degraded",
     "stale",
     "failed",
     "paused"
    ]
   },
   "lastError": {
    "type": "string",
    "nullable": true
   },
   "rowsLastRun": {
    "type": "integer",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "CreateDashboardRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "module",
   "tiles"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "module": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey",
    "description": "**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"
   },
   "isShared": {
    "type": "boolean",
    "default": false
   },
   "tiles": {
    "type": "array",
    "minItems": 1,
    "maxItems": 24,
    "items": {
     "$ref": "#/components/schemas/DashboardTile"
    }
   }
  }
 },
 "Dashboard": {
  "x-ticvai-persistence": "reporting.dashboard + reporting.dashboard_tile",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateDashboardRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "aggregateCost",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "aggregateCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Combined refresh load of every tile."
     },
     "archivedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "DashboardData": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/Dashboard"
   },
   {
    "type": "object",
    "properties": {
     "tileData": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "tileId": {
         "type": "string",
         "format": "uuid"
        },
        "result": {
         "$ref": "#/components/schemas/ReportResult"
        },
        "isCached": {
         "type": "boolean"
        },
        "error": {
         "type": "string",
         "nullable": true
        }
       }
      }
     }
    }
   }
  ]
 },
 "DashboardTile": {
  "x-ticvai-persistence": "reporting.dashboard_tile",
  "type": "object",
  "required": [
   "id",
   "reportId",
   "visualisation",
   "position"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "title": {
    "type": "string"
   },
   "reportId": {
    "type": "string",
    "format": "uuid"
   },
   "visualisation": {
    "type": "string",
    "description": "**Extended 22 September from eight marks to twenty** against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names eighteen components and marks every one MVP. Nine were genuinely missing — `combo`, `matrix`, `funnel`, `waterfall`, `treemap`, `scatter`, `map`, `ribbon`, `decompositionTree` — and three are layout variants of marks already here: `area` beside `line`, `donut` beside `pie`, `stackedBar100` beside `stackedBar`.\n**`number` is the source's KPI / card.** Its comparison, variance, trend sparkline and status icon are tile parameters rather than separate marks.\n**Two of the eighteen are deliberately not here** — see `x-ticvai-refuses`. The source lists them as components; the platform already models each of them elsewhere, and a second model of either is the drift this enum exists to prevent.\n",
    "enum": [
     "number",
     "line",
     "area",
     "bar",
     "stackedBar",
     "stackedBar100",
     "combo",
     "pie",
     "donut",
     "table",
     "matrix",
     "gauge",
     "heatmap",
     "funnel",
     "waterfall",
     "treemap",
     "scatter",
     "map",
     "ribbon",
     "decompositionTree"
    ],
    "x-ticvai-refuses": {
     "slicer": "**A control, not a mark.** The source's slicer / filter is already `ReportFilter.isParameter` plus `ReportParameter` — a run-time prompt bound to the report. A slicer on the canvas places that parameter; it does not render a result, so it is not a visualisation and a second filter model beside `ReportFilter` would be one somebody keeps in step by hand.",
     "narrative": "**Generated prose belongs with `ai.Suggestion`.** The source's narrative / insight text (*\"Admissions are 12% above last Tuesday\"*) is model output with traceability requirements, not a way of drawing a query result.",
     "cohort": "**Not one of the eighteen.** It appears once in the source as a *usage* — *\"the Customer & Membership dashboard shall use cards, cohort and trend charts\"* — never as a specified component. A cohort view is a `matrix` or `heatmap` over a cohort dimension."
    },
    "x-ticvai-note": "**These marks cannot yet bind data.** `ReportColumn` carries `field`, `label`, `aggregation` and `format` and **no encoding role** — no axis, series, size or colour. A `number` needs none and an eight-mark enum survived without one; a `scatter` needs x, y, size and colour, and a `combo` needs a secondary axis with stated units. **Adding `ReportColumn.role` is the harder half of this decision and is deliberately not made here** — it is the field-wells model the source's builder specifies, and it belongs with the engine and semantic-layer split that needs an ADR first.\n"
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Open on purpose, and not yet specified.** Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as `RunReportRequest.parameters`) and its display settings — for `number`, the comparison, variance, sparkline and status icon. The per-visualisation display shape waits on the field-wells decision in `visualisation`'s `x-ticvai-note`.\n"
   },
   "refreshSeconds": {
    "type": "integer",
    "minimum": 30,
    "description": "Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume.\n"
   },
   "position": {
    "type": "object",
    "required": [
     "row",
     "column",
     "width",
     "height"
    ],
    "properties": {
     "row": {
      "type": "integer"
     },
     "column": {
      "type": "integer"
     },
     "width": {
      "type": "integer"
     },
     "height": {
      "type": "integer"
     }
    }
   }
  }
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
 "KpiDefinition": {
  "type": "object",
  "x-ticvai-persistence": "reporting.kpi_definition",
  "description": "BI boards 2.5 and 10.2. **One definition, referenced everywhere** — otherwise *revenue* means two things in the same meeting.\n",
  "required": [
   "code",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "description": "`takings` and `admissions` are seeded for every tenant as system KPIs (decided 28 September, audit R283), and the five accreditation KPIs for every tenant with the accreditation module (29 September, build pass). The seeded codes are `ReportingSystemKpi`.\n"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "domain": {
    "type": "string",
    "nullable": true
   },
   "formula": {
    "type": "string",
    "description": "**Expressed against the semantic model, not against tables.** A KPI written in SQL is a KPI that breaks when the warehouse is reshaped.\n"
   },
   "unit": {
    "type": "string",
    "enum": [
     "currency",
     "count",
     "percentage",
     "duration",
     "ratio",
     "score"
    ]
   },
   "higherIsBetter": {
    "type": "boolean",
    "default": true,
    "description": "**Refund rate and revenue both go up.** Without this the status colour is a coin toss.\n"
   },
   "defaultPeriod": {
    "type": "string",
    "nullable": true
   },
   "owner": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "KpiTarget": {
  "type": "object",
  "x-ticvai-persistence": "reporting.kpi_target",
  "description": "BI board 2.6. **The threshold is what turns a number into a status.**",
  "required": [
   "scopePath",
   "period",
   "target"
  ],
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "description": "The scope this target applies to. With `period`, the key `setKpiTargets` matches on."
   },
   "period": {
    "type": "string"
   },
   "target": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "amberAt": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "redAt": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "stretch": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   }
  }
 },
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  ]
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
 "SemanticModel": {
  "type": "object",
  "x-ticvai-persistence": "reporting.semantic_model",
  "description": "BI boards 3.3 and 10.6. **A vocabulary, not a schema.** Exposing joins to report authors produces reports that are wrong invisibly.\n",
  "properties": {
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "Assigned by the server on each publish."
   },
   "domains": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
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
      "datasets": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "code": {
          "type": "string"
         },
         "name": {
          "type": "string"
         },
         "grain": {
          "type": "string",
          "description": "**What one row means.** The single most common cause of a wrong report is a join that silently multiplied the grain.\n"
         },
         "fields": {
          "type": "array",
          "items": {
           "type": "object",
           "properties": {
            "code": {
             "type": "string"
            },
            "label": {
             "type": "string"
            },
            "dataType": {
             "$ref": "#/components/schemas/FieldType"
            },
            "aggregation": {
             "allOf": [
              {
               "$ref": "#/components/schemas/Aggregation"
              }
             ],
             "nullable": true,
             "description": "The default aggregation for the field, where it has one."
            },
            "sensitive": {
             "type": "boolean",
             "default": false
            },
            "description": {
             "type": "string",
             "nullable": true
            }
           }
          }
         }
        }
       }
      }
     }
    }
   },
   "relationships": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "fromDataset": {
       "type": "string"
      },
      "toDataset": {
       "type": "string"
      },
      "cardinality": {
       "type": "string",
       "enum": [
        "oneToOne",
        "oneToMany",
        "manyToOne",
        "manyToMany"
       ]
      }
     }
    }
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
