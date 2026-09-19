# WS20 — Approval Workflows and Governance board 8

**10 screens · 0 operations · 0 schemas · 0 permissions**

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
| `ADM-359` | Approval Executive KPI Dashboard | listDetail | 0 | 0 | — |
| `ADM-360` | Approval Volume & Outcome Analytics | listDetail | 0 | 0 | — |
| `ADM-361` | Approval Processing Time Analytics | listDetail | 0 | 0 | — |
| `ADM-362` | Bottleneck Analysis & Heatmap | listDetail | 0 | 0 | — |
| `ADM-363` | Approval Trend & Comparative Analytics | listDetail | 0 | 0 | — |
| `ADM-364` | Approver & Team Performance Analytics | commandCentre | 0 | 0 | — |
| `ADM-365` | Risk & Governance Analytics | listDetail | 0 | 0 | — |
| `ADM-366` | AI Approval Intelligence Center | listDetail | 0 | 0 | — |
| `ADM-367` | AI Optimization & What-If Simulator | listDetail | 0 | 0 | — |
| `ADM-368` | AI Governance Executive Advisor | listDetail | 0 | 0 | — |

## Thin screens in this batch

**ADM-359, ADM-360, ADM-361, ADM-362, ADM-363, ADM-365, ADM-366, ADM-367, ADM-368 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-359",
  "name": "Approval Executive KPI Dashboard",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "1",
   "page": 72
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-executive-kpi-dashboard-adm-359",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalExecutiveKpiDashboard.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide executives and senior management with a high-level view of approval performance across TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 72"
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
       "label": "Search approval executive kpi",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 72 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Department",
        "Module",
        "Workflow",
        "Request type",
        "Date range",
        "Risk",
        "Priority"
       ],
       "notes": "The pack filters this screen by tenant, venue, department, module, workflow, request type and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 72 §Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval executive kpi list.",
   "error": "Could not load. Names which read failed and leaves the approval executive kpi untouched.",
   "emptyFirstRun": "No approval executive kpi yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval executive kpi are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-359"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 72. 0 of 9 labels bound to a contract property; 9 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-360",
    "ADM-361",
    "ADM-362",
    "ADM-363",
    "ADM-364",
    "ADM-365",
    "ADM-366",
    "ADM-367",
    "ADM-368"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ADM-368",
     "trigger": "AI Governance Executive Advisor",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-360",
     "trigger": "Approval Volume & Outcome Analytics",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-361",
     "trigger": "Approval Processing Time Analytics",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-362",
     "trigger": "Bottleneck Analysis & Heatmap",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-363",
     "trigger": "Approval Trend & Comparative Analytics",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-364",
     "trigger": "Approver & Team Performance Analytics",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-365",
     "trigger": "Risk & Governance Analytics",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-366",
     "trigger": "AI Approval Intelligence Center",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-367",
     "trigger": "AI Optimization & What-If Simulator",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    }
   ]
  },
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
  "id": "ADM-360",
  "name": "Approval Volume & Outcome Analytics",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "2",
   "page": 72
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-volume-outcome-analytics-adm-360",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalVolumeOutcomeAnalytics.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Analyze how many approval requests are being generated and what happens to them.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 72"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 72"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The approval volume outcome list.",
   "error": "Could not load. Names which read failed and leaves the approval volume outcome untouched.",
   "emptyFirstRun": "No approval volume outcome yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval volume outcome are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-360"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 72. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-359"
   ],
   "exitTo": [
    "ADM-359"
   ],
   "transitions": [
    {
     "to": "ADM-359",
     "trigger": "Back to Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-361",
  "name": "Approval Processing Time Analytics",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "3",
   "page": 73
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-processing-time-analytics-adm-361",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalProcessingTimeAnalytics.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure exactly how long approval processes and individual stages take. The matrix explicitly requires processing-time analytics.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 73"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 73"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The approval processing time list.",
   "error": "Could not load. Names which read failed and leaves the approval processing time untouched.",
   "emptyFirstRun": "No approval processing time yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval processing time are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-361"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 73. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-359"
   ],
   "exitTo": [
    "ADM-359"
   ],
   "transitions": [
    {
     "to": "ADM-359",
     "trigger": "Back to Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-362",
  "name": "Bottleneck Analysis & Heatmap",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "4",
   "page": 74
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/bottleneck-analysis-heatmap-adm-362",
   "component": "apps/ticvai-web/src/routes/platform/BottleneckAnalysisHeatmap.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Columns) and no metric row",
  "purpose": "Automatically identify where approval processes are becoming slow or congested. The source explicitly requires approval bottleneck analysis.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 74 §Columns"
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
       "label": "Every bottleneck analysis heatmap",
       "columns": [
        "Refund",
        "Discount",
        "Price Override",
        "Complimentary",
        "Access Change",
        "Configuration"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 74 §Columns"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected bottleneck analysis heatmap",
       "bindsTo": null,
       "columns": [
        "Refund",
        "Discount",
        "Price Override",
        "Complimentary",
        "Access Change",
        "Configuration"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Rows”, “Cells”, “Commercial”, “Director”.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 74 §Columns"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bottleneck analysis heatmap list.",
   "error": "Could not load. Names which read failed and leaves the bottleneck analysis heatmap untouched.",
   "emptyFirstRun": "No bottleneck analysis heatmap yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bottleneck analysis heatmap are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Refund",
    "Discount",
    "Price Override",
    "Complimentary",
    "Access Change",
    "Configuration"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-362"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 74. 0 of 6 labels bound to a contract property; 6 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-359"
   ],
   "exitTo": [
    "ADM-359"
   ],
   "transitions": [
    {
     "to": "ADM-359",
     "trigger": "Back to Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-363",
  "name": "Approval Trend & Comparative Analytics",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "5",
   "page": 75
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-trend-comparative-analytics-adm-363",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalTrendComparativeAnalytics.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Identify whether approval performance is improving or deteriorating over time. The matrix specifically requires approval trend reporting.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 75"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 75"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The approval trend comparative list.",
   "error": "Could not load. Names which read failed and leaves the approval trend comparative untouched.",
   "emptyFirstRun": "No approval trend comparative yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval trend comparative are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-363"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 75. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-359"
   ],
   "exitTo": [
    "ADM-359"
   ],
   "transitions": [
    {
     "to": "ADM-359",
     "trigger": "Back to Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-364",
  "name": "Approver & Team Performance Analytics",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "6",
   "page": 76
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approver-team-performance-analytics-adm-364",
   "component": "apps/ticvai-web/src/routes/platform/ApproverTeamPerformanceAnalytics.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Understand workload and operational performance at approver and team level without reducing governance to a simplistic employee ranking.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Assigned requests",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 76 §Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Completed approvals",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 76 §Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Average response time",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 76 §Metrics"
      },
      {
       "kind": "metricTile",
       "label": "SLA compliance",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 76 §Metrics"
      },
      {
       "kind": "metricTile",
       "label": "escalation rate",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 76 §Metrics"
      },
      {
       "kind": "metricTile",
       "label": "workload",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 76 §Metrics"
      },
      {
       "kind": "metricTile",
       "label": "pending queue",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 76 §Metrics"
      },
      {
       "kind": "metricTile",
       "label": "delegation frequency",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 76 §Metrics"
      },
      {
       "kind": "metricTile",
       "label": "approval/rejection ratio",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 76 §Metrics"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approver team performance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the approver team performance untouched.",
   "emptyFirstRun": "No approver team performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approver team performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Assigned requests",
    "Completed approvals",
    "Average response time",
    "SLA compliance",
    "escalation rate",
    "workload"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-364"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 76. 0 of 0 labels bound to a contract property; 9 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-359"
   ],
   "exitTo": [
    "ADM-359"
   ],
   "transitions": [
    {
     "to": "ADM-359",
     "trigger": "Back to Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-365",
  "name": "Risk & Governance Analytics",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "7",
   "page": 77
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/risk-governance-analytics-adm-365",
   "component": "apps/ticvai-web/src/routes/platform/RiskGovernanceAnalytics.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide management with consolidated visibility of approval risk.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 77"
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
       "label": "Search risk governance analytics",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 77 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Workflow",
        "venue",
        "department",
        "requester",
        "approver",
        "transaction type",
        "value",
        "AI risk score"
       ],
       "notes": "The pack filters this screen by workflow, venue, department, requester, approver, transaction type and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 77 §Analyze by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The risk governance analytics list.",
   "error": "Could not load. Names which read failed and leaves the risk governance analytics untouched.",
   "emptyFirstRun": "No risk governance analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the risk governance analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-365"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 77. 0 of 8 labels bound to a contract property; 8 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-359"
   ],
   "exitTo": [
    "ADM-359"
   ],
   "transitions": [
    {
     "to": "ADM-359",
     "trigger": "Back to Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-366",
  "name": "AI Approval Intelligence Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "8",
   "page": 77
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-approval-intelligence-center-adm-366",
   "component": "apps/ticvai-web/src/routes/platform/AiApprovalIntelligenceCenter.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide one centralized location for AI-generated approval intelligence. This should be one of the strongest screens in the entire module.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 77"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 77"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The approval intelligence list.",
   "error": "Could not load. Names which read failed and leaves the approval intelligence untouched.",
   "emptyFirstRun": "No approval intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-366"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 77. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-359"
   ],
   "exitTo": [
    "ADM-359"
   ],
   "transitions": [
    {
     "to": "ADM-359",
     "trigger": "Back to Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-367",
  "name": "AI Optimization & What-If Simulator",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "9",
   "page": 78
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-optimization-what-if-simulator-adm-367",
   "component": "apps/ticvai-web/src/routes/platform/AiOptimizationWhatIfSimulator.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow management to evaluate proposed governance changes before implementing them.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 78"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 78"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The optimization what-if simulator list.",
   "error": "Could not load. Names which read failed and leaves the optimization what-if simulator untouched.",
   "emptyFirstRun": "No optimization what-if simulator yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the optimization what-if simulator are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-367"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 78. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-359"
   ],
   "exitTo": [
    "ADM-359"
   ],
   "transitions": [
    {
     "to": "ADM-359",
     "trigger": "Back to Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-368",
  "name": "AI Governance Executive Advisor",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "8",
   "number": "10",
   "page": 79
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-governance-executive-advisor-adm-368",
   "component": "apps/ticvai-web/src/routes/platform/AiGovernanceExecutiveAdvisor.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Turn all approval analytics into prioritized management recommendations. Instead of management examining dozens of dashboards, TICVAI AI should answer: “What requires my attention?”",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 79"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 79"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The governance executive advisor list.",
   "error": "Could not load. Names which read failed and leaves the governance executive advisor untouched.",
   "emptyFirstRun": "No governance executive advisor yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance executive advisor are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-368"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 79. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-359"
   ],
   "exitTo": [
    "ADM-359"
   ],
   "transitions": [
    {
     "to": "ADM-359",
     "trigger": "Back to Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
