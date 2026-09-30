# WS68 — Unified BI Reporting and AI Analytics Platform board 3

**10 screens · 10 operations · 18 schemas · 3 permissions**

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
| `ANL-031` | Report Catalogue & Library | listDetail | 2 | 0 | — |
| `ANL-032` | Report Creation Wizard | configEditor | 1 | 0 | — |
| `ANL-033` | Data Domain & Dataset Selector | listDetail | 1 | 0 | — |
| `ANL-034` | Field & Column Selector | listDetail | 1 | 0 | — |
| `ANL-035` | Filter & Parameter Builder | listDetail | 1 | 0 | — |
| `ANL-036` | Grouping, Aggregation & Calculation Builder | listDetail | 1 | 0 | — |
| `ANL-037` | Cross-Domain Report Composer | listDetail | 2 | 0 | — |
| `ANL-038` | Report Layout & Formatting Designer | configEditor | 1 | 0 | — |
| `ANL-039` | Report Preview, Test & Validation | listDetail | 3 | 0 | — |
| `ANL-040` | Save, Run & Report Results Viewer | commandCentre | 2 | 0 | — |

## Thin screens in this batch

**ANL-031, ANL-033, ANL-035, ANL-036, ANL-037, ANL-039 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ANL-031",
  "name": "Report Catalogue & Library",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.1",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/report-catalogue-library-anl-031",
   "component": "apps/venue-management-web/src/routes/analytics/ReportCatalogueLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-032",
    "ANL-033",
    "ANL-034",
    "ANL-035",
    "ANL-036",
    "ANL-037",
    "ANL-038",
    "ANL-039",
    "ANL-040"
   ],
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Back to Executive Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ANL-040",
     "trigger": "Save, Run & Report Results Viewer",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-032",
     "trigger": "Report Creation Wizard",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-033",
     "trigger": "Data Domain & Dataset Selector",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-034",
     "trigger": "Field & Column Selector",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-035",
     "trigger": "Filter & Parameter Builder",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-036",
     "trigger": "Grouping, Aggregation & Calculation Builder",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-037",
     "trigger": "Cross-Domain Report Composer",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-038",
     "trigger": "Report Layout & Formatting Designer",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-039",
     "trigger": "Report Preview, Test & Validation",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can search, filter, organize and access authorized reports from one centralized report library.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each report shall display) and no metric row",
  "purpose": "Provide a centralized repository containing all TICVAI standard, custom, scheduled and AI-generated reports.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 27 §Each report shall display"
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
       "label": "Every report catalogue",
       "columns": [
        "Report Name",
        "Report ID",
        "Description",
        "Category",
        "Business Domain",
        "Owner",
        "Report Type",
        "Site Scope",
        "Created Date",
        "Last Run",
        "Last Modified",
        "Status",
        "Usage Count"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 27 §Each report shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected report catalogue",
       "bindsTo": null,
       "columns": [
        "Report Name",
        "Report ID",
        "Description",
        "Category",
        "Business Domain",
        "Owner",
        "Report Type",
        "Site Scope",
        "Created Date",
        "Last Run",
        "Last Modified",
        "Status",
        "Usage Count"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Report Categories”, “Report Types”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 27 §Each report shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report catalogue list.",
   "error": "Could not load. Names which read failed and leaves the report catalogue untouched.",
   "emptyFirstRun": "No report catalogue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the report catalogue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReports",
    "contract": "reporting",
    "purpose": "The catalogue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSeededReports",
    "contract": "reporting",
    "purpose": "What ships with the platform",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Report Name",
    "Report ID",
    "Description",
    "Category",
    "Business Domain",
    "Owner"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-031",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-031"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 27. 0 of 13 labels bound to a contract property; 13 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-032",
  "name": "Report Creation Wizard",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.2",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/report-creation-wizard-anl-032",
   "component": "apps/venue-management-web/src/routes/analytics/ReportCreationWizard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-031"
   ],
   "exitTo": [
    "ANL-031"
   ],
   "transitions": [
    {
     "to": "ANL-031",
     "trigger": "Back to Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An authorized business user can create the initial structure of a report without knowing the underlying database schema.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Select one or multiple domains) and no display directory — it is settings, not a population",
  "purpose": "Guide users through creation of a new report without requiring technical knowledge. Step 1 — Report Information",
  "gaps": [
   {
    "operation": null,
    "why": "**Report Creation Wizard declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Report Name",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Category",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tags",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 28 §Configure"
      },
      {
       "kind": "textField",
       "label": "Step 2 — Business Domain",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 28 §Configure"
      },
      {
       "kind": "textField",
       "label": "Inventory • Resources • Marketing",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 28 §Select one or multiple domains"
      },
      {
       "kind": "textField",
       "label": "Step 3 — Report Type",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 28 §Select one or multiple domains"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report creation wizard configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the report creation wizard untouched.",
   "emptyFirstRun": "No report creation wizard configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createReport",
    "contract": "reporting",
    "purpose": "Create a report",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReports"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-032",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-032"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 28. 0 of 0 labels bound to a contract property; 9 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-033",
  "name": "Data Domain & Dataset Selector",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.3",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/data-domain-dataset-selector-anl-033",
   "component": "apps/venue-management-web/src/routes/analytics/DataDomainDatasetSelector.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-031"
   ],
   "exitTo": [
    "ANL-031"
   ],
   "transitions": [
    {
     "to": "ANL-031",
     "trigger": "Back to Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Only approved semantic datasets shall be exposed to report creators; direct production-database access shall not be required.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow users to select approved TICVAI data sources for reporting.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 29 §Show"
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
       "label": "Every data domain dataset",
       "columns": [
        "Dataset Name",
        "Description",
        "Domain",
        "Available Date Range",
        "Refresh Frequency",
        "Last Refresh",
        "Data Owner",
        "Security Classification"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 29 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected data domain dataset",
       "bindsTo": null,
       "columns": [
        "Dataset Name",
        "Description",
        "Domain",
        "Available Date Range",
        "Refresh Frequency",
        "Last Refresh",
        "Data Owner",
        "Security Classification"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Ticketing”, “Sales”, “Finance”, “Payments”, “Access”, “Customer”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 29 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data domain dataset list.",
   "error": "Could not load. Names which read failed and leaves the data domain dataset untouched.",
   "emptyFirstRun": "No data domain dataset yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data domain dataset are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSemanticModel",
    "contract": "reporting",
    "purpose": "Domains and datasets",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Dataset Name",
    "Description",
    "Domain",
    "Available Date Range",
    "Refresh Frequency",
    "Last Refresh"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-033",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-033"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 29. 0 of 8 labels bound to a contract property; 8 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-034",
  "name": "Field & Column Selector",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.4",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/field-column-selector-anl-034",
   "component": "apps/venue-management-web/src/routes/analytics/FieldColumnSelector.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-031"
   ],
   "exitTo": [
    "ANL-031"
   ],
   "transitions": [
    {
     "to": "ANL-031",
     "trigger": "Back to Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can construct the report output using approved business-friendly field names.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to visually select which information appears in the report.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Reorder columns, Rename display labels, Set width, Configure formatting. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 30 §Users can"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 30"
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
       "label": "Reorder columns",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 30 §Users can"
      },
      {
       "kind": "secondaryButton",
       "label": "Rename display labels",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 30 §Users can"
      },
      {
       "kind": "secondaryButton",
       "label": "Set width",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 30 §Users can"
      },
      {
       "kind": "secondaryButton",
       "label": "Configure formatting",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 30 §Users can"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The field column selector list.",
   "error": "Could not load. Names which read failed and leaves the field column selector untouched.",
   "emptyFirstRun": "No field column selector yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the field column selector are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReportFields",
    "contract": "reporting",
    "purpose": "Fields available here",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-034",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-034"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 4 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-035",
  "name": "Filter & Parameter Builder",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.5",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/filter-parameter-builder-anl-035",
   "component": "apps/venue-management-web/src/routes/analytics/FilterParameterBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-031"
   ],
   "exitTo": [
    "ANL-031"
   ],
   "transitions": [
    {
     "to": "ANL-031",
     "trigger": "Back to Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can create complex report filters without SQL or technical query syntax.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow report creators to define which records are included.",
  "gaps": [
   {
    "operation": null,
    "why": "**Filter & Parameter Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 31"
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
       "label": "Search filter parameter",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 31 §Standard Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Date Range",
        "Site",
        "Venue",
        "Attraction",
        "Business Unit",
        "Product",
        "Ticket Type",
        "Channel",
        "Customer",
        "Membership",
        "POS",
        "Cashier",
        "Payment Method",
        "Transaction Status"
       ],
       "notes": "The pack filters this screen by date range, site, venue, attraction, business unit, product and 8 more — which are present is a decision the pack already made.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 31 §Standard Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The filter parameter list.",
   "error": "Could not load. Names which read failed and leaves the filter parameter untouched.",
   "emptyFirstRun": "No filter parameter yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the filter parameter are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Filters and parameters",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getReport",
     "listReports"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-035",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-035"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 31. 0 of 14 labels bound to a contract property; 14 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "reportId",
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
  "id": "ANL-036",
  "name": "Grouping, Aggregation & Calculation Builder",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.6",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/grouping-aggregation-calculation-builder-anl-036",
   "component": "apps/venue-management-web/src/routes/analytics/GroupingAggregationCalculationBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-031"
   ],
   "exitTo": [
    "ANL-031"
   ],
   "transitions": [
    {
     "to": "ANL-031",
     "trigger": "Back to Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Business users can create summaries and derived metrics using governed calculation tools.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Turn detailed transactional data into meaningful management reporting.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Period-over-Period Change. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 32 §Support"
   },
   {
    "operation": null,
    "why": "**Grouping, Aggregation & Calculation Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 32"
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
       "label": "Search grouping aggregation calculation",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 32 §Users can group by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Site",
        "Attraction",
        "Product",
        "Ticket Type",
        "Channel",
        "Customer Segment",
        "Cashier",
        "Date",
        "Week",
        "Month",
        "Year"
       ],
       "notes": "The pack filters this screen by site, attraction, product, ticket type, channel, customer segment and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 32 §Users can group by"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Period-over-Period Change",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 32 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The grouping aggregation calculation list.",
   "error": "Could not load. Names which read failed and leaves the grouping aggregation calculation untouched.",
   "emptyFirstRun": "No grouping aggregation calculation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the grouping aggregation calculation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Grouping and calculations",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getReport",
     "listReports"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-036",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-036"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 32. 0 of 11 labels bound to a contract property; 12 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "reportId",
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
  "id": "ANL-037",
  "name": "Cross-Domain Report Composer",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.7",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/cross-domain-report-composer-anl-037",
   "component": "apps/venue-management-web/src/routes/analytics/CrossDomainReportComposer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-031"
   ],
   "exitTo": [
    "ANL-031"
   ],
   "transitions": [
    {
     "to": "ANL-031",
     "trigger": "Back to Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can create cross-domain analytics while maintaining governed data relationships and security.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized users to combine information across multiple TICVAI modules. This is one of the most important capabilities of Board 3.",
  "gaps": [
   {
    "operation": null,
    "why": "**Cross-Domain Report Composer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 34"
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
       "impliedBy": "updateReport",
       "label": "Save report",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateReport"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-domain report composer list.",
   "error": "Could not load. Names which read failed and leaves the cross-domain report composer untouched.",
   "emptyFirstRun": "No cross-domain report composer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-domain report composer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSemanticModel",
    "contract": "reporting",
    "purpose": "How domains relate",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Compose across them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getReport",
     "listReports"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-037",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-037"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "reportId",
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
  "id": "ANL-038",
  "name": "Report Layout & Formatting Designer",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.8",
   "page": 35
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/report-layout-formatting-designer-anl-038",
   "component": "apps/venue-management-web/src/routes/analytics/ReportLayoutFormattingDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-031"
   ],
   "exitTo": [
    "ANL-031"
   ],
   "transitions": [
    {
     "to": "ANL-031",
     "trigger": "Back to Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can produce professional reports suitable for operational, financial and management use.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control how the final report is displayed.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: TICVAI branding, Report logo. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Support"
   },
   {
    "operation": null,
    "why": "**Report Layout & Formatting Designer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Column labels",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number format",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Percentage",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Date format",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Decimal precision",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Conditional formatting",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "TICVAI branding",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Report logo",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 35 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report layout formatting configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the report layout formatting untouched.",
   "emptyFirstRun": "No report layout formatting configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Layout and formatting",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getReport",
     "listReports"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-038",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-038"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 35. 0 of 0 labels bound to a contract property; 9 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "reportId",
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
  "id": "ANL-039",
  "name": "Report Preview, Test & Validation",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.9",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/report-preview-test-validation-anl-039",
   "component": "apps/venue-management-web/src/routes/analytics/ReportPreviewTestValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-031"
   ],
   "exitTo": [
    "ANL-031"
   ],
   "transitions": [
    {
     "to": "ANL-031",
     "trigger": "Back to Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Critical data, security or calculation issues must be identified before the report is published.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow users to verify report accuracy before saving or publishing it.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 36 §Display"
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
       "label": "Every report preview test",
       "columns": [
        "Sample Results",
        "Total Records",
        "Applied Filters",
        "Calculated Fields",
        "Grouping",
        "Totals",
        "Execution Time",
        "Data Refresh Time"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 36 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected report preview test",
       "bindsTo": null,
       "columns": [
        "Sample Results",
        "Total Records",
        "Applied Filters",
        "Calculated Fields",
        "Grouping",
        "Totals",
        "Execution Time",
        "Data Refresh Time"
       ],
       "notes": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 36 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The report preview test list.",
   "error": "Could not load. Names which read failed and leaves the report preview test untouched.",
   "emptyFirstRun": "No report preview test yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the report preview test are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run it against a sample",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getReportExecution",
    "contract": "reporting",
    "purpose": "How the run went",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "cancelReportExecution",
    "contract": "reporting",
    "purpose": "Stop a run that is going to be wrong anyway",
    "trigger": "onAction",
    "provenance": "wiring gap, 19 September 2026 — the screen showed the noun and could not act on it",
    "invalidates": [
     "listReportExecutions"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Sample Results",
    "Total Records",
    "Applied Filters",
    "Calculated Fields",
    "Grouping",
    "Totals"
   ],
   "params": [
    {
     "name": "executionId",
     "from": "navigation"
    },
    {
     "name": "reportId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-039",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-039"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 36. 0 of 8 labels bound to a contract property; 8 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ANL-040",
  "name": "Save, Run & Report Results Viewer",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "source": {
   "pack": "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf",
   "board": "3",
   "number": "3.10",
   "page": 37
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/save-run-report-results-viewer-anl-040",
   "component": "apps/venue-management-web/src/routes/analytics/SaveRunReportResultsViewer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-031"
   ],
   "exitTo": [
    "ANL-031"
   ],
   "transitions": [
    {
     "to": "ANL-031",
     "trigger": "Back to Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can execute reports interactively, analyze the results and export authorized data in supported formats. AI — “Ask TICVAI to Build My Report” Board 3 should include AI throughout the report-building process rather than making AI a separate disconnected feature.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display; Dashboard Designer Report Builder) and a per-row directory (§KPI cards/charts Rows, columns, matrices) — counts over a population, then the population",
  "purpose": "Provide the final operational interface for executing and consuming reports.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §KPI cards/charts Rows, columns, matrices"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Report Name",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Description",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Owner",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Last Run",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Data Refresh",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Applied Parameters",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Reporting Period",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Visual management dashboards Detailed reporting",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §Dashboard Designer Report Builder"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every save run report",
       "columns": [
        "Executive/operational monitoring Analysis/reconciliation/detail",
        "Persistent dashboard layout Parameter-driven report execution"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §KPI cards/charts Rows, columns, matrices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected save run report",
       "bindsTo": null,
       "columns": [
        "Executive/operational monitoring Analysis/reconciliation/detail",
        "Persistent dashboard layout Parameter-driven report execution"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Further Actions”, “A user could type”, “Visualization focused Data/report focused”.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §KPI cards/charts Rows, columns, matrices"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Excel, PDF, CSV, XML. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 37 §Authorized users can export to"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The save run report list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the save run report untouched.",
   "emptyFirstRun": "No save run report yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the save run report are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getReportResult",
    "contract": "reporting",
    "purpose": "The results",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-040",
   "workshopBoard": "wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-040"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 37. 0 of 2 labels bound to a contract property; 20 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "executionId",
     "from": "navigation"
    },
    {
     "name": "reportId",
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
 "cancelReportExecution": {
  "method": "DELETE",
  "path": "/report-executions/{executionId}",
  "contract": "reporting",
  "summary": "Cancel a running execution",
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
  "responds": null
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
 "getReportExecution": {
  "method": "GET",
  "path": "/report-executions/{executionId}",
  "contract": "reporting",
  "summary": "Execution status, and where its result is",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReportExecution"
 },
 "getReportResult": {
  "method": "GET",
  "path": "/report-executions/{executionId}/result",
  "contract": "reporting",
  "summary": "Paged result rows",
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
  "responds": "ReportResult"
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
 "listReportFields": {
  "method": "GET",
  "path": "/report-fields",
  "contract": "reporting",
  "summary": "Fields available for a data source",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "dataSource",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "ReportField"
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
 "listSeededReports": {
  "method": "GET",
  "path": "/reports/seeded",
  "contract": "reporting",
  "summary": "The reports every venue starts with",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SeededReport"
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
 "ReportExecution": {
  "x-ticvai-persistence": "reporting.execution",
  "type": "object",
  "required": [
   "id",
   "reportId",
   "definitionVersion",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "reportId": {
    "type": "string",
    "format": "uuid"
   },
   "reportName": {
    "type": "string"
   },
   "definitionVersion": {
    "type": "string",
    "description": "The version this ran against. With the parameters and scope below, it is everything needed to reproduce the result.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ExecutionStatus"
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "The parameters it ran with, keyed by `ReportParameter.key` of `definitionVersion` — defaults filled in, so the record is complete."
   },
   "scopeApplied": {
    "type": "array",
    "description": "Scope paths the caller held. What constrained the result.",
    "items": {
     "type": "string"
    }
   },
   "rowCount": {
    "type": "integer",
    "nullable": true
   },
   "durationMs": {
    "type": "integer",
    "nullable": true
   },
   "error": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "scheduleId": {
    "type": "string",
    "format": "uuid",
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
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Results are retained for a limited period, then discarded."
   }
  }
 },
 "ReportField": {
  "x-ticvai-persistence": "none — metadata catalogue, generated",
  "type": "object",
  "required": [
   "key",
   "label",
   "type",
   "isGroupable",
   "isAggregatable",
   "isFilterable"
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
   "isGroupable": {
    "type": "boolean"
   },
   "isAggregatable": {
    "type": "boolean"
   },
   "isFilterable": {
    "type": "boolean"
   },
   "isPersonalData": {
    "type": "boolean",
    "description": "Requires REPORT_EXPORT_PII to include in an export."
   },
   "requiredPermission": {
    "allOf": [
     {
      "$ref": "../shared/permissions.yaml#/components/schemas/Permission"
     }
    ],
    "nullable": true,
    "description": "The permission a principal needs to see this field. Null where the report's own permission is enough."
   },
   "enumValues": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
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
 },
 "SeededReport": {
  "type": "object",
  "description": "BL-053. **`ReportDefinition.isSystem` existed and nothing populated it.** Twenty-eight requirements asked for dashboards and analyses over data that was already there, and the answer to every one of them was *\"the builder can do that\"* — which is true and is not a deliverable.\n**A venue opening on Monday does not want a report builder. It wants the eight reports every venue runs**, and the ability to change them.\nSeeded at provisioning, `isSystem` true, and **clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse a system report with 409, and a venue that wants one different clones it with `createReport`. The eight codes are listed on `listSeededReports` (proposed, audit R282).\n",
  "required": [
   "code",
   "name",
   "category",
   "dataSource"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "category": {
    "$ref": "#/components/schemas/ReportCategory"
   },
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "appliesToVenueKinds": {
    "type": "array",
    "description": "**A water park does not need a theatre's seat-utilisation report.** Empty means every venue kind.\n",
    "items": {
     "type": "string"
    }
   },
   "defaultSchedule": {
    "$ref": "#/components/schemas/Cadence"
   },
   "rationale": {
    "type": "string",
    "description": "**Why this report ships, in words a venue manager reads.** A seeded report with no rationale is one somebody deletes as clutter in the first week.\n"
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
