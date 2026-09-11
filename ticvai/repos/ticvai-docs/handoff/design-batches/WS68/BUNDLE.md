# WS68 — Unified BI Reporting and AI Analytics Platform board 3

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
| `ANL-031` | Report Catalogue & Library | listDetail | 0 | 0 | — |
| `ANL-032` | Report Creation Wizard | configEditor | 0 | 0 | — |
| `ANL-033` | Data Domain & Dataset Selector | listDetail | 0 | 0 | — |
| `ANL-034` | Field & Column Selector | listDetail | 0 | 0 | — |
| `ANL-035` | Filter & Parameter Builder | listDetail | 0 | 0 | — |
| `ANL-036` | Grouping, Aggregation & Calculation Builder | listDetail | 0 | 0 | — |
| `ANL-037` | Cross-Domain Report Composer | listDetail | 0 | 0 | — |
| `ANL-038` | Report Layout & Formatting Designer | configEditor | 0 | 0 | — |
| `ANL-039` | Report Preview, Test & Validation | listDetail | 0 | 0 | — |
| `ANL-040` | Save, Run & Report Results Viewer | commandCentre | 0 | 0 | — |

## Thin screens in this batch

**ANL-031, ANL-033, ANL-034, ANL-035, ANL-036, ANL-037, ANL-039 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each report shall display) and no metric row",
  "purpose": "Provide a centralized repository containing all TICVAI standard, custom, scheduled and AI-generated reports.",
  "purposeNote": "Users can search, filter, organize and access authorized reports from one centralized report library.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-031"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 27. 0 of 13 labels bound to a contract property; 13 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Select one or multiple domains) and no display directory — it is settings, not a population",
  "purpose": "Guide users through creation of a new report without requiring technical knowledge. Step 1 — Report Information",
  "purposeNote": "An authorized business user can create the initial structure of a report without knowing the underlying database schema.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-032"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 28. 0 of 0 labels bound to a contract property; 9 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow users to select approved TICVAI data sources for reporting.",
  "purposeNote": "Only approved semantic datasets shall be exposed to report creators; direct production-database access shall not be required.",
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
  "apis": [],
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
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-033"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 29. 0 of 8 labels bound to a contract property; 8 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to visually select which information appears in the report.",
  "purposeNote": "Users can construct the report output using approved business-friendly field names.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Configure formatting. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Configure formatting",
       "provenance": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 30 §Users can"
      }
     ]
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-034"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 1 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow report creators to define which records are included.",
  "purposeNote": "Users can create complex report filters without SQL or technical query syntax.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-035"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 31. 0 of 14 labels bound to a contract property; 14 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Turn detailed transactional data into meaningful management reporting.",
  "purposeNote": "Business users can create summaries and derived metrics using governed calculation tools.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-036"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 32. 0 of 11 labels bound to a contract property; 12 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized users to combine information across multiple TICVAI modules. This is one of the most important capabilities of Board 3.",
  "purposeNote": "Authorized users can create cross-domain analytics while maintaining governed data relationships and security.",
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
   "regions": []
  },
  "states": {
   "loading": "The cross-domain report composer list.",
   "error": "Could not load. Names which read failed and leaves the cross-domain report composer untouched.",
   "emptyFirstRun": "No cross-domain report composer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-domain report composer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-037"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control how the final report is displayed.",
  "purposeNote": "Users can produce professional reports suitable for operational, financial and management use.",
  "gaps": [
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
    }
   ]
  },
  "states": {
   "loading": "The report layout formatting configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the report layout formatting untouched.",
   "emptyFirstRun": "No report layout formatting configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-038"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 35. 0 of 0 labels bound to a contract property; 7 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow users to verify report accuracy before saving or publishing it.",
  "purposeNote": "Critical data, security or calculation issues must be identified before the report is published.",
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
  "apis": [],
  "entryState": {
   "preloaded": [
    "Sample Results",
    "Total Records",
    "Applied Filters",
    "Calculated Fields",
    "Grouping",
    "Totals"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-039"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 36. 0 of 8 labels bound to a contract property; 8 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display; Dashboard Designer Report Builder) and a per-row directory (§KPI cards/charts Rows, columns, matrices) — counts over a population, then the population",
  "purpose": "Provide the final operational interface for executing and consuming reports.",
  "purposeNote": "Users can execute reports interactively, analyze the results and export authorized data in supported formats. AI — “Ask TICVAI to Build My Report” Board 3 should include AI throughout the report-building process rather than making AI a separate disconnected feature.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-040"
  },
  "apisNote": "Regenerated 9 September 2026 from Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf page 37. 0 of 2 labels bound to a contract property; 20 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
