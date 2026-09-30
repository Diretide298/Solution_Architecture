# WS20 — Approval Workflows and Governance board 8

**10 screens · 6 operations · 10 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `APPROVAL_CONFIGURE, APPROVAL_VIEW, PRICE_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-359` | Approval Executive KPI Dashboard | listDetail | 1 | 0 | — |
| `ADM-360` | Approval Volume & Outcome Analytics | listDetail | 1 | 0 | — |
| `ADM-361` | Approval Processing Time Analytics | listDetail | 1 | 0 | — |
| `ADM-362` | Bottleneck Analysis & Heatmap | listDetail | 1 | 0 | — |
| `ADM-363` | Approval Trend & Comparative Analytics | listDetail | 1 | 0 | — |
| `ADM-364` | Approver & Team Performance Analytics | commandCentre | 1 | 0 | — |
| `ADM-365` | Risk & Governance Analytics | listDetail | 2 | 0 | — |
| `ADM-366` | AI Approval Intelligence Center | listDetail | 2 | 0 | — |
| `ADM-367` | AI Optimization & What-If Simulator | listDetail | 1 | 0 | — |
| `ADM-368` | AI Governance Executive Advisor | listDetail | 1 | 0 | — |

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
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "The executive view",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-359",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-359"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 72. 0 of 9 labels bound to a contract property; 9 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Volume and outcome",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-360",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-360"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 72. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Processing time",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-361",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-361"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 73. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "listSlaEscalationBottleneck",
    "contract": "approvals",
    "purpose": "Where it backs up",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-362",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-362"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 74. 0 of 6 labels bound to a contract property; 6 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Trend and comparison",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-363",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-363"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 75. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "By approver and team",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-364",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-364"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 76. 0 of 0 labels bound to a contract property; 9 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "listGovernanceRiskMonitoring",
    "contract": "catalogue",
    "purpose": "Governance Risk, AI Monitoring & Control Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listGovernanceRiskLaunch",
    "contract": "promotions",
    "purpose": "Governance Audit, AI Risk & Launch Readiness",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-365",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-365"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 77. 0 of 8 labels bound to a contract property; 8 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getApprovalRequestScore",
       "notes": "One record, read-only."
      }
     ]
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
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "What the models see",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getApprovalRequestScore",
    "contract": "ai",
    "purpose": "Risk band, priority and suggested escalation for the request, as context only (no approve/reject suggestion)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-366",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-366"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 77. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "approvalRequestId",
     "from": "navigation"
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
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "simulateWorkflowTestingImpact",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateWorkflowTestingImpact"
      }
     ]
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
  "apis": [
   {
    "operationId": "simulateWorkflowTestingImpact",
    "contract": "approvals",
    "purpose": "What-if on the workflow",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-367",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-367"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 78. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Governance for the executive",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-368",
   "workshopBoard": "wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-368"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 79. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{
 "getApprovalAnalytics": {
  "method": "GET",
  "path": "/approval-analytics",
  "contract": "approvals",
  "summary": "Volumes, times, rejections and bottlenecks",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ApprovalAnalytics"
 },
 "getApprovalRequestScore": {
  "method": "GET",
  "path": "/approval-requests/{approvalRequestId}/score",
  "contract": "ai",
  "summary": "The latest context score of an approval request",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiApprovalRequestScore"
 },
 "listGovernanceRiskLaunch": {
  "method": "GET",
  "path": "/governance-risk-launch",
  "contract": "promotions",
  "summary": "Governance Audit, AI Risk & Launch Readiness",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GovernanceAuditAiRiskLaunchReadinessView"
 },
 "listGovernanceRiskMonitoring": {
  "method": "GET",
  "path": "/governance-risk-monitoring",
  "contract": "catalogue",
  "summary": "Governance Risk, AI Monitoring & Control Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "severity",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "owner",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listSlaEscalationBottleneck": {
  "method": "GET",
  "path": "/sla-escalation-bottleneck",
  "contract": "approvals",
  "summary": "SLA, Escalation & Bottleneck Monitor",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workflow",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
    "in": "query",
    "required": false
   },
   {
    "name": "escalationLevel",
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
 "simulateWorkflowTestingImpact": {
  "method": "PUT",
  "path": "/workflow-testing-impact",
  "contract": "approvals",
  "summary": "Workflow Testing, Simulation & Impact Analysis",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "WorkflowTestingSimulationImpactAnalysisInput",
  "responds": "WorkflowTestingSimulationImpactAnalysisView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiApprovalRequestScore": {
  "type": "object",
  "x-ticvai-persistence": "ai.approval_request_score",
  "description": "**Context for an approval reviewer** (11.1.73..75): risk, priority and a suggested escalation for one pending request, the latest per request. **There is no approve or reject field, by design** (minutes of 8 September: AI in approvals never recommends or influences approve or reject).",
  "required": [
   "approvalRequestId",
   "riskScore",
   "riskBand",
   "priorityScore",
   "escalationSuggestion"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "approvals.request"
   },
   "trigger": {
    "type": "string",
    "enum": [
     "submitted",
     "resubmitted",
     "slaTick",
     "escalated"
    ]
   },
   "riskScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100
   },
   "riskBand": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Design 5.6: a risk score and band, never a probability."
   },
   "priorityScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "description": "For ordering work in an inbox; higher first."
   },
   "escalationSuggestion": {
    "type": "object",
    "required": [
     "action"
    ],
    "properties": {
     "action": {
      "type": "string",
      "enum": [
       "escalate",
       "addBackupApprover",
       "none"
      ]
     },
     "reason": {
      "type": "string",
      "nullable": true
     }
    },
    "description": "A suggestion for an SLA problem, carried out if at all by a person or the tenant's SLA policy."
   },
   "signals": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "description": "e.g. `amountAboveRequesterNorm`, `requesterEntityRisk`, `outOfHours`, `irreversibleAction`, `slaDueSoon`, `stepBreachRate`, `approverUnavailable`."
      },
      "contribution": {
       "type": "number"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scoredAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "ApprovalAnalytics": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from approvals.request",
  "properties": {
   "from": {
    "type": "string",
    "format": "date"
   },
   "to": {
    "type": "string",
    "format": "date"
   },
   "groupBy": {
    "type": "string",
    "description": "The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it.",
    "enum": [
     "kind",
     "approver",
     "venue",
     "day",
     "week"
    ]
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "raised": {
       "type": "integer"
      },
      "approved": {
       "type": "integer"
      },
      "rejected": {
       "type": "integer"
      },
      "withdrawn": {
       "type": "integer"
      },
      "expired": {
       "type": "integer",
       "description": "**Requests nobody answered.** Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person.\n"
      },
      "escalated": {
       "type": "integer"
      },
      "slaBreached": {
       "type": "integer"
      },
      "medianMinutes": {
       "type": "number"
      },
      "p95Minutes": {
       "type": "number"
      }
     }
    }
   }
  }
 },
 "GovernanceAuditAiRiskLaunchReadinessView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Governance Audit, AI Risk & Launch Readiness displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "promotionConfiguration": {
    "type": "string",
    "description": "Promotion Configuration ✓"
   },
   "eligibility": {
    "type": "string",
    "description": "Eligibility ✓"
   },
   "stackingRules": {
    "type": "string",
    "description": "Stacking Rules ✓"
   },
   "budget": {
    "type": "string",
    "description": "Budget ✓"
   },
   "redemptionLimits": {
    "type": "string",
    "description": "Redemption Limits ✓"
   },
   "marginGuardrail": {
    "type": "number",
    "description": "Margin Guardrail ✓"
   },
   "simulationCompleted": {
    "type": "string",
    "description": "Simulation Completed ✓"
   },
   "requiredApproval": {
    "type": "string",
    "description": "Required Approval ✓"
   },
   "channelPublication": {
    "type": "string",
    "description": "Channel Publication ✓"
   },
   "auditRequirements": {
    "type": "string",
    "description": "Audit Requirements ✓"
   },
   "budgetCreation": {
    "type": "string",
    "description": "Budget creation"
   },
   "budgetChange": {
    "type": "string",
    "description": "Budget change"
   },
   "limitChanges": {
    "type": "integer",
    "description": "Limit changes"
   },
   "approvalSubmissions": {
    "type": "string",
    "description": "Approval submissions"
   },
   "approvalDecisions": {
    "type": "string",
    "description": "Approval decisions"
   },
   "overrides": {
    "type": "string",
    "description": "Overrides"
   },
   "automaticSuspension": {
    "type": "string",
    "description": "Automatic suspension"
   },
   "reactivation": {
    "type": "string",
    "description": "Reactivation"
   },
   "simulationResults": {
    "type": "string",
    "description": "Simulation results"
   },
   "experimentChanges": {
    "type": "string",
    "description": "Experiment changes"
   },
   "campaignLaunch": {
    "type": "string",
    "description": "Campaign launch"
   }
  }
 },
 "GovernanceRiskAiMonitoringControlCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Governance Risk, AI Monitoring & Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "risk": {
    "type": "string",
    "enum": [
     "productWithoutOwner",
     "missingApproval",
     "outdatedPricing",
     "conflictingValidity",
     "missingChannelConfiguration",
     "orphanedDependency",
     "unusedProduct",
     "duplicateProduct",
     "unusualConfigurationChange",
     "highOverrideLevel",
     "scheduledPublicationConflict",
     "expiredCommercialConfiguration",
     "activeAfterEventEnd",
     "brokenDependency"
    ],
    "description": "Risk detected (AI Monitoring, pack p.26)"
   },
   "product": {
    "type": "string",
    "description": "Product name"
   },
   "venue": {
    "type": "string",
    "description": "Venue name"
   },
   "businessImpact": {
    "type": "string",
    "description": "Business impact, in plain language"
   },
   "recommendedAction": {
    "type": "string",
    "description": "Recommended action; advisory"
   },
   "owner": {
    "type": "string",
    "description": "Owner (display name)",
    "nullable": true
   },
   "dueDate": {
    "type": "string",
    "description": "Due date",
    "format": "date",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out)"
   },
   "riskId": {
    "type": "string",
    "description": "Risk id",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid",
    "nullable": true
   },
   "severity": {
    "type": "string",
    "enum": [
     "critical",
     "high",
     "medium",
     "low"
    ],
    "description": "Severity (Risk Dashboard)"
   },
   "explanation": {
    "type": "string",
    "description": "AI explanation, e.g. the two products share 96% of their configuration; advisory"
   },
   "detectedAt": {
    "type": "string",
    "description": "Detected",
    "format": "date-time"
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
 "SlaEscalationBottleneckMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_instance, whose SLA and reminder timestamps it lists (data model for the agreed operations, 29 September)",
  "description": "**What SLA, Escalation & Bottleneck Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflow": {
    "type": "string",
    "description": "Workflow"
   },
   "instance": {
    "type": "string",
    "description": "Instance"
   },
   "currentStep": {
    "type": "string",
    "description": "Current Step"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "started": {
    "type": "string",
    "format": "date-time",
    "description": "Started"
   },
   "target": {
    "type": "string",
    "format": "date-time",
    "description": "SLA deadline"
   },
   "timeRemaining": {
    "type": "integer",
    "description": "Minutes until breach; negative once breached"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "escalationLevel": {
    "type": "string",
    "description": "Escalation Level"
   },
   "firstReminder": {
    "type": "string",
    "format": "date-time",
    "description": "First Reminder"
   },
   "secondReminder": {
    "type": "string",
    "format": "date-time",
    "description": "Second Reminder"
   },
   "managerEscalation": {
    "type": "string",
    "format": "date-time",
    "description": "Manager Escalation"
   },
   "executiveEscalation": {
    "type": "string",
    "format": "date-time",
    "description": "Executive Escalation"
   },
   "finalOutcome": {
    "type": "string",
    "description": "Final Outcome"
   }
  },
  "required": [
   "instance"
  ]
 },
 "SlaEscalationBottleneckMonitorViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "withinSla": {
    "type": "integer",
    "description": "Within SLA"
   },
   "atRisk": {
    "type": "integer",
    "description": "At Risk"
   },
   "breached": {
    "type": "integer",
    "description": "Breached"
   },
   "escalated": {
    "type": "integer",
    "description": "Escalated"
   },
   "averageProcessingTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "averageApprovalTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "longestWaitingStep": {
    "type": "string",
    "description": "Longest Waiting Step"
   }
  }
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "WorkflowTestingSimulationImpactAnalysisInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; the outcome is recorded as approvals.workflow_version test results (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Testing, Simulation & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "workflowId": {
    "type": "string",
    "description": "Workflow under test"
   },
   "testMode": {
    "type": "string",
    "enum": [
     "manualTestCase",
     "sampleTransaction",
     "historicalReplay",
     "scenarioSimulation",
     "batchTest"
    ],
    "description": "How the workflow is tested"
   },
   "version": {
    "type": "string",
    "description": "Version under test"
   },
   "compareWithVersion": {
    "type": "string",
    "description": "Existing version to compare against for regression"
   },
   "inputPayload": {
    "type": "string",
    "description": "Sample transaction as a JSON document, for manual and sample tests"
   },
   "replayFrom": {
    "type": "string",
    "format": "date",
    "description": "Historical replay start"
   },
   "replayTo": {
    "type": "string",
    "format": "date",
    "description": "Historical replay end"
   }
  },
  "required": [
   "workflowId",
   "testMode"
  ]
 },
 "WorkflowTestingSimulationImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — computed by simulation over approvals.workflow_version and the rules it calls; never executes actions (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Testing, Simulation & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowId": {
    "type": "string",
    "description": "Workflow under test"
   },
   "testMode": {
    "type": "string",
    "enum": [
     "manualTestCase",
     "sampleTransaction",
     "historicalReplay",
     "scenarioSimulation",
     "batchTest"
    ],
    "description": "How the workflow is tested"
   },
   "rulesEvaluated": {
    "type": "integer",
    "description": "Rules Evaluated"
   },
   "conditionsMatched": {
    "type": "integer",
    "description": "Conditions Matched"
   },
   "decisions": {
    "type": "integer",
    "description": "Decisions"
   },
   "approvalPath": {
    "type": "string",
    "description": "Approval Path"
   },
   "actions": {
    "type": "integer",
    "description": "Actions"
   },
   "notifications": {
    "type": "integer",
    "description": "Notifications"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "expectedOutcome": {
    "type": "string",
    "description": "Expected Outcome"
   },
   "version": {
    "type": "string",
    "description": "Version under test"
   },
   "compareWithVersion": {
    "type": "string",
    "description": "Existing version to compare against for regression"
   },
   "inputPayload": {
    "type": "string",
    "description": "Sample transaction as a JSON document, for manual and sample tests"
   },
   "replayFrom": {
    "type": "string",
    "format": "date",
    "description": "Historical replay start"
   },
   "replayTo": {
    "type": "string",
    "format": "date",
    "description": "Historical replay end"
   }
  },
  "required": [
   "workflowId",
   "testMode"
  ]
 }
}
```
