# WS124 — AI Governance board 4

**10 screens · 20 operations · 17 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_APPROVE, AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-549` | AI Governance Monitoring Command Center | commandCentre | 5 | 0 | — |
| `ADM-550` | AI Risk Register & Risk Exposure Management | listDetail | 2 | 0 | — |
| `ADM-551` | AI Governance Control Library & Control Effectiveness | listDetail | 2 | 0 | — |
| `ADM-552` | AI Policy Compliance & Violation Monitoring | commandCentre | 2 | 0 | — |
| `ADM-553` | AI Data, Privacy & Usage Compliance Monitoring | commandCentre | 2 | 0 | — |
| `ADM-554` | AI Quality, Behavior & Governance Drift Monitoring | listDetail | 6 | 0 | — |
| `ADM-555` | AI Governance Alert & Detection Center | listDetail | 3 | 0 | — |
| `ADM-556` | AI Incident & Remediation Management | configEditor | 6 | 0 | — |
| `ADM-557` | AI Compliance, Assurance & Governance Reporting | listDetail | 3 | 0 | — |
| `ADM-558` | AI Governance Review, Action Plan & Continuous Improvement | configEditor | 2 | 0 | — |

## Thin screens in this batch

**ADM-551, ADM-555, ADM-558 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-549",
  "name": "AI Governance Monitoring Command Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "1",
   "page": 82
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-governance-monitoring-command-center-adm-549",
   "component": "apps/ticvai-web/src/routes/platform/AiGovernanceMonitoringCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-550",
    "ADM-551",
    "ADM-552",
    "ADM-553",
    "ADM-554",
    "ADM-555",
    "ADM-556",
    "ADM-557",
    "ADM-558"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-550",
     "trigger": "AI Risk Register & Risk Exposure Management",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-551",
     "trigger": "AI Governance Control Library & Control Effectiveness",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-552",
     "trigger": "AI Policy Compliance & Violation Monitoring",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-553",
     "trigger": "AI Data, Privacy & Usage Compliance Monitoring",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-554",
     "trigger": "AI Quality, Behavior & Governance Drift Monitoring",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "releaseId"
     ]
    },
    {
     "to": "ADM-555",
     "trigger": "AI Governance Alert & Detection Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-556",
     "trigger": "AI Incident & Remediation Management",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "capabilityKey",
      "incidentId",
      "releaseId"
     ]
    },
    {
     "to": "ADM-557",
     "trigger": "AI Compliance, Assurance & Governance Reporting",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-558",
     "trigger": "AI Governance Review, Action Plan & Continuous Improvement",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide executives, governance teams and authorized administrators with one centralized real-time view of AI governance health across TICVAI.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search governance monitoring",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Capability",
        "Module",
        "Environment",
        "Risk",
        "Status",
        "Provider",
        "Model",
        "Date"
       ],
       "notes": "The pack filters this screen by tenant, venue, capability, module, environment, risk and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Filters"
      },
      {
       "kind": "dataTable",
       "label": "Capability health",
       "bindsTo": "AiCapabilityHealth",
       "columns": [
        "AiCapabilityHealth.capabilityKey",
        "AiCapabilityHealth.availability",
        "AiCapabilityHealth.p95LatencyMs",
        "AiCapabilityHealth.errorRate",
        "AiCapabilityHealth.breakerState",
        "AiCapabilityHealth.degraded",
        "AiCapabilityHealth.dataFreshness"
       ],
       "operation": "listAiCapabilityHealth",
       "notes": "**Overall AI health in production** (21 September minutes, M21-13).",
       "provenance": "29 September pass (P29 group A)"
      },
      {
       "kind": "chart",
       "label": "Spend by agent",
       "bindsTo": "AiUsageReport",
       "operation": "getAiUsage",
       "notes": "`getAiUsage` grouped by `agent`, with the month-end projection labelled a forecast: which agents consume the most, and for what (M21-13).",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active AI Capabilities",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "AI Decisions Today",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Governance Compliance Rate",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Policy Violations",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "High-Risk Events",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Critical AI Events",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Open AI Incidents",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Active Exceptions",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Controls Passing",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Controls Failing",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "AI Capabilities Under Review",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Governance Health Score",
       "provenance": "pack AI_Governance_Reference.pdf, page 82 §Header KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance monitoring list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the governance monitoring untouched.",
   "emptyFirstRun": "No governance monitoring yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance monitoring are still there. Names the active filter and offers to clear it.",
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
    "operationId": "listAiGovernanceAlerts",
    "contract": "ai",
    "purpose": "Governance alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiIncidents",
    "contract": "ai",
    "purpose": "AI incidents",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiCapabilityHealth",
    "contract": "ai",
    "purpose": "Health per capability",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   },
   {
    "operationId": "getAiUsage",
    "contract": "ai",
    "purpose": "Consumption by agent",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-549",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-549"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 82. 0 of 10 labels bound to a contract property; 22 of 58 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-550",
  "name": "AI Risk Register & Risk Exposure Management",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "2",
   "page": 84
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-risk-register-risk-exposure-management-adm-550",
   "component": "apps/ticvai-web/src/routes/platform/AiRiskRegisterRiskExposureManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-549"
   ],
   "exitTo": [
    "ADM-549"
   ],
   "transitions": [
    {
     "to": "ADM-549",
     "trigger": "Back to AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain the enterprise risk register specifically for TICVAI AI capabilities. Board 1 classifies individual capabilities/actions. Board 4 manages the ongoing risk exposure after those capabilities are operational.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 21 actions on this screen and the screen declares 0 operations.** Unserved: Customer, Commercial, Financial, Operational, Security, Model / AI Quality, Risk Matrix, Critical …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Governance_Reference.pdf, page 84 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 84"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 84"
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
       "label": "Customer",
       "provenance": "pack AI_Governance_Reference.pdf, page 84 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Commercial",
       "provenance": "pack AI_Governance_Reference.pdf, page 84 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Financial",
       "provenance": "pack AI_Governance_Reference.pdf, page 84 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Operational",
       "provenance": "pack AI_Governance_Reference.pdf, page 84 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Security",
       "provenance": "pack AI_Governance_Reference.pdf, page 84 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Model / AI Quality",
       "provenance": "pack AI_Governance_Reference.pdf, page 84 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Risk Matrix",
       "provenance": "pack AI_Governance_Reference.pdf, page 84 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Critical",
       "provenance": "pack AI_Governance_Reference.pdf, page 84 §Support"
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
   "loading": "The risk register risk list.",
   "error": "Could not load. Names which read failed and leaves the risk register risk untouched.",
   "emptyFirstRun": "No risk register risk yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the risk register risk are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiRiskRegister",
    "contract": "ai",
    "purpose": "The AI risk register",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setAiRiskRegisterEntry",
    "contract": "ai",
    "purpose": "Record or update a risk register entry",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-550",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-550"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 84. 0 of 0 labels bound to a contract property; 21 of 64 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "entryId",
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
  "id": "ADM-551",
  "name": "AI Governance Control Library & Control Effectiveness",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "3",
   "page": 86
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-governance-control-library-control-effectiveness-adm-551",
   "component": "apps/ticvai-web/src/routes/platform/AiGovernanceControlLibraryControlEffectiveness.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-549"
   ],
   "exitTo": [
    "ADM-549"
   ],
   "transitions": [
    {
     "to": "ADM-549",
     "trigger": "Back to AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define and continuously test whether the controls designed to govern AI are actually working. A policy existing on paper does not mean the control is effective.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 86"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 86"
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
       "impliedBy": "listAiControls",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "runAiControlTest",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "runAiControlTest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance effectiveness list.",
   "error": "Could not load. Names which read failed and leaves the governance effectiveness untouched.",
   "emptyFirstRun": "No governance effectiveness yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance effectiveness are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiControls",
    "contract": "ai",
    "purpose": "Governance controls",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "runAiControlTest",
    "contract": "ai",
    "purpose": "Test a control now",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-551",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-551"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 86. 0 of 0 labels bound to a contract property; 0 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "controlKey",
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
  "id": "ADM-552",
  "name": "AI Policy Compliance & Violation Monitoring",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "4",
   "page": 87
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-policy-compliance-violation-monitoring-adm-552",
   "component": "apps/ticvai-web/src/routes/platform/AiPolicyComplianceViolationMonitoring.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-549"
   ],
   "exitTo": [
    "ADM-549"
   ],
   "transitions": [
    {
     "to": "ADM-549",
     "trigger": "Back to AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Compliance KPIs) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Continuously detect AI activity that violates or attempts to violate Board 1 governance policies.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Governance_Reference.pdf, page 87 §Show"
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
       "label": "Evaluated Actions",
       "provenance": "pack AI_Governance_Reference.pdf, page 87 §Compliance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Compliant",
       "provenance": "pack AI_Governance_Reference.pdf, page 87 §Compliance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Blocked by Policy",
       "provenance": "pack AI_Governance_Reference.pdf, page 87 §Compliance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Policy Violations",
       "provenance": "pack AI_Governance_Reference.pdf, page 87 §Compliance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Attempted Violations",
       "provenance": "pack AI_Governance_Reference.pdf, page 87 §Compliance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Exception-Based Actions",
       "provenance": "pack AI_Governance_Reference.pdf, page 87 §Compliance KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Unknown / Unclassified Actions",
       "provenance": "pack AI_Governance_Reference.pdf, page 87 §Compliance KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every policy compliance violation",
       "columns": [
        "Request",
        "→ Governance Evaluation",
        "→ Violation Detected",
        "→ Execution Blocked",
        "→ Alert Created",
        "Repeated Violation Detection",
        "14 times in 24 hours"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Governance_Reference.pdf, page 87 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected policy compliance violation",
       "bindsTo": null,
       "columns": [
        "Request",
        "→ Governance Evaluation",
        "→ Violation Detected",
        "→ Execution Blocked",
        "→ Alert Created",
        "Repeated Violation Detection",
        "14 times in 24 hours"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Actor”.",
       "provenance": "pack AI_Governance_Reference.pdf, page 87 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The policy compliance violation list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the policy compliance violation untouched.",
   "emptyFirstRun": "No policy compliance violation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the policy compliance violation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiGovernanceAlerts",
    "contract": "ai",
    "purpose": "Governance alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideAiGovernanceAlert",
    "contract": "ai",
    "purpose": "Acknowledge, dismiss, resolve, or open an incident",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-552",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-552"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 87. 0 of 7 labels bound to a contract property; 14 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "alertId",
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
  "id": "ADM-553",
  "name": "AI Data, Privacy & Usage Compliance Monitoring",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "5",
   "page": 89
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-data-privacy-usage-compliance-monitoring-adm-553",
   "component": "apps/ticvai-web/src/routes/platform/AiDataPrivacyUsageComplianceMonitoring.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-549"
   ],
   "exitTo": [
    "ADM-549"
   ],
   "transitions": [
    {
     "to": "ADM-549",
     "trigger": "Back to AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Data Usage KPIs) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Monitor whether AI capabilities are actually using data according to the policies configured in Board 1. This screen is monitoring—not the configuration of the data policies themselves.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Governance_Reference.pdf, page 89 §Show"
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
       "label": "AI Data Requests",
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Data Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Allowed",
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Data Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Conditionally Allowed",
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Data Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Blocked",
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Data Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "External Transfers",
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Data Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Masked / Redacted",
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Data Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Data Policy Violations",
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Data Usage KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Unknown Data Categories",
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Data Usage KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every data privacy usage",
       "columns": [
        "Provider",
        "Approved Provider A",
        "Data Categories Sent",
        "Product",
        "Basket Context",
        "Venue",
        "Prohibited Data",
        "Full Payment Details",
        "Restricted PII",
        "Data Minimization Monitoring",
        "Requested Data",
        "Actually Sent",
        "24 available fields",
        "↓",
        "8 required fields",
        "6 sent after masking",
        "Sensitive Data Alert"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected data privacy usage",
       "bindsTo": null,
       "columns": [
        "Provider",
        "Approved Provider A",
        "Data Categories Sent",
        "Product",
        "Basket Context",
        "Venue",
        "Prohibited Data",
        "Full Payment Details",
        "Restricted PII",
        "Data Minimization Monitoring",
        "Requested Data",
        "Actually Sent",
        "24 available fields",
        "↓",
        "8 required fields",
        "6 sent after masking",
        "Sensitive Data Alert"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Data Usage Matrix”, “HIGH”, “Response”.",
       "provenance": "pack AI_Governance_Reference.pdf, page 89 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data privacy usage list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the data privacy usage untouched.",
   "emptyFirstRun": "No data privacy usage yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data privacy usage are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiGovernanceAlerts",
    "contract": "ai",
    "purpose": "Governance alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideAiGovernanceAlert",
    "contract": "ai",
    "purpose": "Acknowledge, dismiss, resolve, or open an incident",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-553",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-553"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 89. 0 of 17 labels bound to a contract property; 25 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "alertId",
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
  "id": "ADM-554",
  "name": "AI Quality, Behavior & Governance Drift Monitoring",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "6",
   "page": 90
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-quality-behavior-governance-drift-monitoring-adm-554",
   "component": "apps/ticvai-web/src/routes/platform/AiQualityBehaviorGovernanceDriftMonitoring.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-549"
   ],
   "exitTo": [
    "ADM-549"
   ],
   "transitions": [
    {
     "to": "ADM-549",
     "trigger": "Back to AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Detect meaningful changes in AI behavior that may increase governance risk. This is not the full model monitoring platform. Board 4 focuses specifically on governance-relevant behavioral changes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 90"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 90"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "publishGate",
       "impliedBy": "promoteAiRelease",
       "notes": "Declares `promoteAiRelease`. **The gate names what the publish will affect before it happens**: which tenants, venues or capabilities take the new version, and that the previous one stays available to roll back to.",
       "provenance": "check-screens publish rule, 29 September 2026"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "runAiEvaluation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAiEvaluations",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "runAiEvaluation"
      },
      {
       "kind": "dataTable",
       "label": "Training and backtest runs",
       "bindsTo": "AiTrainingRun",
       "columns": [
        "AiTrainingRun.capabilityKey",
        "AiTrainingRun.trainingWindowFrom",
        "AiTrainingRun.trainingWindowTo",
        "AiTrainingRun.includesImportedHistory",
        "AiTrainingRun.status",
        "AiTrainingRun.metrics",
        "AiTrainingRun.releaseId"
       ],
       "operation": "listAiTrainingRuns",
       "notes": "**Per tenant, own data only** (AIP-149). A run that passes its shadow gate raises `promotionReady`; the admin promotes it here with `promoteAiRelease`. Nothing switches by itself (AI-D16).",
       "provenance": "29 September pass (P29 group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The quality behavior governance list.",
   "error": "Could not load. Names which read failed and leaves the quality behavior governance untouched.",
   "emptyFirstRun": "No quality behavior governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the quality behavior governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "runAiEvaluation",
    "contract": "ai",
    "purpose": "Evaluate a candidate",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiEvaluations",
    "contract": "ai",
    "purpose": "Evaluation runs",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "promoteAiRelease",
    "contract": "ai",
    "purpose": "Promote a release to its next stage (a person)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "rollbackAiRelease",
    "contract": "ai",
    "purpose": "Roll a release back",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiGovernanceAlerts",
    "contract": "ai",
    "purpose": "Governance alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiTrainingRuns",
    "contract": "ai",
    "purpose": "The per-tenant training and backtest runs",
    "trigger": "onLoad",
    "provenance": "29 September pass (P29 group A)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-554",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-554"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 90. 0 of 0 labels bound to a contract property; 0 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "releaseId",
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
  "id": "ADM-555",
  "name": "AI Governance Alert & Detection Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "7",
   "page": 92
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-governance-alert-detection-center-adm-555",
   "component": "apps/ticvai-web/src/routes/platform/AiGovernanceAlertDetectionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-549"
   ],
   "exitTo": [
    "ADM-549"
   ],
   "transitions": [
    {
     "to": "ADM-549",
     "trigger": "Back to AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Centralize governance-related alerts generated from policy, control, data, behavior and operational monitoring.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 92"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 92"
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
       "impliedBy": "listAiGovernanceAlerts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "decideAiGovernanceAlert",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideAiGovernanceAlert"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance alert detection list.",
   "error": "Could not load. Names which read failed and leaves the governance alert detection untouched.",
   "emptyFirstRun": "No governance alert detection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance alert detection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiGovernanceAlerts",
    "contract": "ai",
    "purpose": "Governance alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideAiGovernanceAlert",
    "contract": "ai",
    "purpose": "Acknowledge, dismiss, resolve, or open an incident",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "openAiIncident",
    "contract": "ai",
    "purpose": "Open an AI incident",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-555",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-555"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 92. 0 of 0 labels bound to a contract property; 0 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "alertId",
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
  "id": "ADM-556",
  "name": "AI Incident & Remediation Management",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "8",
   "page": 94
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-incident-remediation-management-adm-556",
   "component": "apps/ticvai-web/src/routes/platform/AiIncidentRemediationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-549"
   ],
   "exitTo": [
    "ADM-549"
   ],
   "transitions": [
    {
     "to": "ADM-549",
     "trigger": "Back to AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Manage significant AI governance failures from detection through containment, investigation, remediation and closure.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Revalidate thresholds Fraud Team 15 Sep Pending, Run control test Governance 15 Sep Pending. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Governance_Reference.pdf, page 94 §Action Owner Due Status"
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
       "label": "Root Cause",
       "provenance": "pack AI_Governance_Reference.pdf, page 94 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Impact",
       "provenance": "pack AI_Governance_Reference.pdf, page 94 §Capture"
      },
      {
       "kind": "textField",
       "label": "Customers / Transactions Affected",
       "provenance": "pack AI_Governance_Reference.pdf, page 94 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Control Failure",
       "provenance": "pack AI_Governance_Reference.pdf, page 94 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Corrective Actions",
       "provenance": "pack AI_Governance_Reference.pdf, page 94 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Preventive Actions",
       "provenance": "pack AI_Governance_Reference.pdf, page 94 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Lessons Learned",
       "provenance": "pack AI_Governance_Reference.pdf, page 94 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Revalidate thresholds Fraud Team 15 Sep Pending",
       "provenance": "pack AI_Governance_Reference.pdf, page 94 §Action Owner Due Status"
      },
      {
       "kind": "secondaryButton",
       "label": "Run control test Governance 15 Sep Pending",
       "provenance": "pack AI_Governance_Reference.pdf, page 94 §Action Owner Due Status"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The incident remediation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the incident remediation untouched.",
   "emptyFirstRun": "No incident remediation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "pauseAiCapability",
    "contract": "ai",
    "purpose": "Stop a capability now",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "rollbackAiRelease",
    "contract": "ai",
    "purpose": "Roll a release back",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiIncidents",
    "contract": "ai",
    "purpose": "AI incidents",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "openAiIncident",
    "contract": "ai",
    "purpose": "Open an AI incident",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "containAiIncident",
    "contract": "ai",
    "purpose": "Contain an incident",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "closeAiIncident",
    "contract": "ai",
    "purpose": "Close an incident",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-556",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-556"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 94. 0 of 0 labels bound to a contract property; 9 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "capabilityKey",
     "from": "navigation"
    },
    {
     "name": "incidentId",
     "from": "navigation"
    },
    {
     "name": "releaseId",
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
  "id": "ADM-557",
  "name": "AI Compliance, Assurance & Governance Reporting",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "9",
   "page": 95
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-compliance-assurance-governance-reporting-adm-557",
   "component": "apps/ticvai-web/src/routes/platform/AiComplianceAssuranceGovernanceReporting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-549"
   ],
   "exitTo": [
    "ADM-549"
   ],
   "transitions": [
    {
     "to": "ADM-549",
     "trigger": "Back to AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide structured governance evidence and management reporting without duplicating TICVAI's generic BI platform.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: AI Capability Inventory, AI Risk Register, AI Policy Compliance, AI Approval Compliance, AI Data Usage, AI Exceptions, Control Effectiveness, Model / Provider Governance …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Governance_Reference.pdf, page 95 §Support predefined reports such as"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 95"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 95"
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
       "label": "AI Capability Inventory",
       "provenance": "pack AI_Governance_Reference.pdf, page 95 §Support predefined reports such as"
      },
      {
       "kind": "secondaryButton",
       "label": "AI Risk Register",
       "provenance": "pack AI_Governance_Reference.pdf, page 95 §Support predefined reports such as"
      },
      {
       "kind": "secondaryButton",
       "label": "AI Policy Compliance",
       "provenance": "pack AI_Governance_Reference.pdf, page 95 §Support predefined reports such as"
      },
      {
       "kind": "secondaryButton",
       "label": "AI Approval Compliance",
       "provenance": "pack AI_Governance_Reference.pdf, page 95 §Support predefined reports such as"
      },
      {
       "kind": "secondaryButton",
       "label": "AI Data Usage",
       "provenance": "pack AI_Governance_Reference.pdf, page 95 §Support predefined reports such as"
      },
      {
       "kind": "secondaryButton",
       "label": "AI Exceptions",
       "provenance": "pack AI_Governance_Reference.pdf, page 95 §Support predefined reports such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Control Effectiveness",
       "provenance": "pack AI_Governance_Reference.pdf, page 95 §Support predefined reports such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Model / Provider Governance",
       "provenance": "pack AI_Governance_Reference.pdf, page 95 §Support predefined reports such as"
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
   "loading": "The compliance assurance governance list.",
   "error": "Could not load. Names which read failed and leaves the compliance assurance governance untouched.",
   "emptyFirstRun": "No compliance assurance governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the compliance assurance governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "exportAiEvidencePackage",
    "contract": "ai",
    "purpose": "Export an evidence package",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiRiskRegister",
    "contract": "ai",
    "purpose": "The AI risk register",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiControls",
    "contract": "ai",
    "purpose": "Governance controls",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-557",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-557"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 95. 0 of 0 labels bound to a contract property; 9 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-558",
  "name": "AI Governance Review, Action Plan & Continuous Improvement",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "4",
   "number": "10",
   "page": 97
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-governance-review-action-plan-continuous-improvement-adm-558",
   "component": "apps/ticvai-web/src/routes/platform/AiGovernanceReviewActionPlanContinuousImprovemen.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-549"
   ],
   "exitTo": [
    "ADM-549"
   ],
   "transitions": [
    {
     "to": "ADM-549",
     "trigger": "Back to AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Another option) and no display directory — it is settings, not a population",
  "purpose": "Bring all governance monitoring together into a structured periodic review and improvement cycle. This is the final screen of the entire AI Governance module.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Critical Continuous Monitoring Architecture. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Governance_Reference.pdf, page 97 §Actions"
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
       "label": "Pause Specific Model",
       "provenance": "pack AI_Governance_Reference.pdf, page 97 §Another option"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Critical Continuous Monitoring Architecture",
       "provenance": "pack AI_Governance_Reference.pdf, page 97 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance review action configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the governance review action untouched.",
   "emptyFirstRun": "No governance review action configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listAiGovernanceAlerts",
    "contract": "ai",
    "purpose": "Governance alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiRiskRegister",
    "contract": "ai",
    "purpose": "The AI risk register",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-558",
   "workshopBoard": "wireframes/WS17 AI Governance Board 4.dc.html#adm-558"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 97. 0 of 0 labels bound to a contract property; 6 of 187 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "closeAiIncident": {
  "method": "POST",
  "path": "/incidents/{incidentId}/close",
  "contract": "ai",
  "summary": "Close an incident",
  "permission": "AI_APPROVE",
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
  "requestBody": null,
  "responds": "AiIncident"
 },
 "containAiIncident": {
  "method": "POST",
  "path": "/incidents/{incidentId}/contain",
  "contract": "ai",
  "summary": "Contain an incident",
  "permission": "AI_APPROVE",
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
  "requestBody": null,
  "responds": "AiIncident"
 },
 "decideAiGovernanceAlert": {
  "method": "POST",
  "path": "/governance-alerts/{alertId}/decide",
  "contract": "ai",
  "summary": "Acknowledge, dismiss, resolve, or open an incident",
  "permission": "AI_CONFIGURE",
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
  "responds": "AiGovernanceAlert"
 },
 "exportAiEvidencePackage": {
  "method": "POST",
  "path": "/evidence-packages",
  "contract": "ai",
  "summary": "Export an evidence package",
  "permission": "AI_AUDIT_VIEW",
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
 "getAiUsage": {
  "method": "GET",
  "path": "/usage",
  "contract": "ai",
  "summary": "Usage, cost and performance",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
  "responds": "AiUsageReport"
 },
 "listAiCapabilityHealth": {
  "method": "GET",
  "path": "/governance/capability-health",
  "contract": "ai",
  "summary": "How each AI capability is running now",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "breakerState",
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
 "listAiControls": {
  "method": "GET",
  "path": "/controls",
  "contract": "ai",
  "summary": "Governance controls",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "effectiveness",
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
 "listAiEvaluations": {
  "method": "GET",
  "path": "/evaluations",
  "contract": "ai",
  "summary": "Evaluation runs",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "releaseId",
    "in": "query",
    "required": null
   },
   {
    "name": "capabilityKey",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
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
 "listAiGovernanceAlerts": {
  "method": "GET",
  "path": "/governance-alerts",
  "contract": "ai",
  "summary": "Governance alerts",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "severity",
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
 "listAiIncidents": {
  "method": "GET",
  "path": "/incidents",
  "contract": "ai",
  "summary": "AI incidents",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "severity",
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
 "listAiRiskRegister": {
  "method": "GET",
  "path": "/risk-register",
  "contract": "ai",
  "summary": "The AI risk register",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "category",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
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
 "listAiTrainingRuns": {
  "method": "GET",
  "path": "/training-runs",
  "contract": "ai",
  "summary": "The per-tenant training and backtest runs",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "capabilityKey",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
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
 "openAiIncident": {
  "method": "POST",
  "path": "/incidents",
  "contract": "ai",
  "summary": "Open an AI incident",
  "permission": "AI_CONFIGURE",
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
  "requestBody": null,
  "responds": "AiIncident"
 },
 "pauseAiCapability": {
  "method": "POST",
  "path": "/governance/capabilities/{capabilityKey}/pause",
  "contract": "ai",
  "summary": "Stop a capability now",
  "permission": "AI_CONFIGURE",
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
  "requestBody": null,
  "responds": "AiCapabilityRegistration"
 },
 "promoteAiRelease": {
  "method": "POST",
  "path": "/releases/{releaseId}/promote",
  "contract": "ai",
  "summary": "Promote a release to its next stage (a person)",
  "permission": "AI_APPROVE",
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
  "requestBody": null,
  "responds": "AiRelease"
 },
 "rollbackAiRelease": {
  "method": "POST",
  "path": "/releases/{releaseId}/rollback",
  "contract": "ai",
  "summary": "Roll a release back",
  "permission": "AI_APPROVE",
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
  "requestBody": null,
  "responds": "AiRelease"
 },
 "runAiControlTest": {
  "method": "POST",
  "path": "/controls/{controlKey}/tests",
  "contract": "ai",
  "summary": "Test a control now",
  "permission": "AI_AUDIT_VIEW",
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
  "requestBody": null,
  "responds": "AiControlTest"
 },
 "runAiEvaluation": {
  "method": "POST",
  "path": "/evaluations",
  "contract": "ai",
  "summary": "Evaluate a candidate",
  "permission": "AI_CONFIGURE",
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
  "requestBody": null,
  "responds": null
 },
 "setAiRiskRegisterEntry": {
  "method": "PUT",
  "path": "/risk-register/{entryId}",
  "contract": "ai",
  "summary": "Record or update a risk register entry",
  "permission": "AI_CONFIGURE",
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
  "requestBody": "AiRiskRegisterEntry",
  "responds": "AiRiskRegisterEntry"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiAutonomyLevel": {
  "type": "integer",
  "minimum": 0,
  "maximum": 4,
  "description": "**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."
 },
 "AiCapabilityFamily": {
  "type": "string",
  "enum": [
   "gatewayAndModels",
   "governance",
   "actionPipeline",
   "knowledgeRetrieval",
   "assistants",
   "analyticsInsights",
   "configurationAssistant",
   "forecasting",
   "anomalyDetection",
   "riskIntelligence",
   "recommendations",
   "decisionRecords",
   "operationsEvaluation",
   "residencyPrivacy"
  ],
  "description": "The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."
 },
 "AiCapabilityHealth": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from gateway telemetry, ai.activity and the breaker state in cache",
  "description": "How one capability is running over the last hour (21 September minutes, M21-13).",
  "required": [
   "capabilityKey"
  ],
  "properties": {
   "capabilityKey": {
    "type": "string"
   },
   "availability": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "p95LatencyMs": {
    "type": "integer"
   },
   "latencyBudgetMs": {
    "type": "integer",
    "nullable": true
   },
   "errorRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "breakerState": {
    "type": "string",
    "enum": [
     "closed",
     "halfOpen",
     "open"
    ]
   },
   "degraded": {
    "type": "boolean",
    "description": "Answering from its degradation mode (rules only, search only, a person)."
   },
   "dataFreshness": {
    "type": "string",
    "nullable": true,
    "description": "e.g. index lag, the last forecast published."
   },
   "requests": {
    "type": "integer"
   },
   "measuredAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiCapabilityRegistration": {
  "type": "object",
  "x-ticvai-persistence": "ai.capability",
  "description": "**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).",
  "required": [
   "capabilityKey",
   "family",
   "riskClass",
   "autonomyLevel"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "capabilityKey": {
    "type": "string",
    "description": "Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."
   },
   "family": {
    "$ref": "#/components/schemas/AiCapabilityFamily"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal",
    "description": "The accountable business owner (AIC-144)."
   },
   "businessFunction": {
    "type": "string",
    "nullable": true
   },
   "riskClass": {
    "$ref": "#/components/schemas/AiRiskClass"
   },
   "autonomyCeiling": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiAutonomyLevel"
     }
    ],
    "readOnly": true,
    "description": "The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."
   },
   "autonomyLevel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiAutonomyLevel"
     }
    ],
    "description": "The level in force at this scope. At most `autonomyCeiling`."
   },
   "dataCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Data categories the capability reads (ADM-524)."
   },
   "lifecycle": {
    "type": "object",
    "description": "Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.",
    "properties": {
     "development": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     },
     "staging": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     },
     "production": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     }
    }
   },
   "degradationMode": {
    "type": "string",
    "enum": [
     "rulesOnly",
     "searchOnly",
     "humanHandoff",
     "hidden",
     "failOpen",
     "lastPublished"
    ],
    "description": "What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "paused"
    ],
    "readOnly": true,
    "description": "Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."
   },
   "pausedReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "pausedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "updatedAt": {
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
 "AiControl": {
  "type": "object",
  "x-ticvai-persistence": "ai.control",
  "description": "**A governance control** (AIC-219, ADM-551). Deterministic controls run nightly as SQL over system records (design 4.4): every applied tier-2 action has an approver other than the requester; no L3+ action executed without approval; no card field in any prompt.",
  "required": [
   "controlKey",
   "name",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "controlKey": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "deterministic",
     "manual"
    ]
   },
   "checkRef": {
    "type": "string",
    "nullable": true,
    "description": "The registered check a deterministic control runs. Not free SQL from a request."
   },
   "frequency": {
    "type": "string",
    "enum": [
     "nightly",
     "weekly",
     "monthly",
     "onDemand"
    ]
   },
   "capabilityKeys": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal"
   },
   "effectiveness": {
    "type": "string",
    "enum": [
     "effective",
     "partiallyEffective",
     "ineffective",
     "untested"
    ],
    "readOnly": true
   },
   "lastTestedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiControlTest": {
  "type": "object",
  "x-ticvai-persistence": "ai.control_test",
  "description": "One run of a control and what it found. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.",
  "required": [
   "controlId",
   "result"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "controlId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.control"
   },
   "result": {
    "type": "string",
    "enum": [
     "pass",
     "fail",
     "error"
    ]
   },
   "exceptionsFound": {
    "type": "integer",
    "minimum": 0
   },
   "evidence": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "runByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal",
    "description": "Null where the nightly job ran it."
   },
   "runAt": {
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
 "AiEvaluationRun": {
  "type": "object",
  "x-ticvai-persistence": "ai.eval_run",
  "description": "One evaluation of a candidate against its baseline: offline golden set, backtest or shadow comparison. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.",
  "required": [
   "suiteId",
   "kind",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "suiteId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.eval_suite"
   },
   "releaseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.release"
   },
   "kind": {
    "type": "string",
    "enum": [
     "offline",
     "backtest",
     "shadow"
    ]
   },
   "candidateRef": {
    "type": "string"
   },
   "baselineRef": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "running",
     "passed",
     "failed",
     "error"
    ],
    "readOnly": true
   },
   "metrics": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true
   },
   "gate": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true,
    "description": "The promotion gate thresholds (design 3.5 table) and whether each passed."
   },
   "isolationCasesPassed": {
    "type": "boolean",
    "readOnly": true,
    "description": "False blocks release, whatever the other metrics say."
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiGovernanceAlert": {
  "type": "object",
  "x-ticvai-persistence": "ai.governance_alert",
  "description": "**A governance alert** (design 4.4, AIC-210..223; ADM-549..555). Kept separate from operational incidents and linked where both apply (AIC-250). **`promotionReady`** (design 3.12, decided 29 September): a shadow model passed its promotion gate; the alert names the release and waits for a person to call `promoteAiRelease`. Monitoring never switches a model (AIC-252).",
  "required": [
   "kind",
   "severity",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "policyViolation",
     "crossScopeAttempt",
     "maskingDefect",
     "dataUsage",
     "behaviourDrift",
     "inputDrift",
     "bias",
     "overrideRateShift",
     "controlFailed",
     "spend",
     "providerBreaker",
     "evaluationRegression",
     "forecastNotPublished",
     "indexLag",
     "promotionReady"
    ]
   },
   "severity": {
    "type": "string",
    "enum": [
     "info",
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "capabilityKey": {
    "type": "string",
    "nullable": true
   },
   "releaseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.release",
    "description": "For `promotionReady` and `evaluationRegression`: the release concerned."
   },
   "subjectRef": {
    "type": "string",
    "nullable": true
   },
   "evidence": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "acknowledged",
     "dismissed",
     "resolved",
     "incidentOpened"
    ],
    "readOnly": true
   },
   "incidentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.incident"
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "note": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiIncident": {
  "type": "object",
  "x-ticvai-persistence": "ai.incident",
  "description": "**An AI governance incident** (ADM-556): detection, containment, investigation, remediation and closure.",
  "required": [
   "reference",
   "title",
   "severity",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "reference": {
    "type": "string",
    "readOnly": true
   },
   "title": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "governance",
     "operational",
     "both"
    ]
   },
   "severity": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "contained",
     "investigating",
     "remediating",
     "closed"
    ],
    "readOnly": true
   },
   "capabilityKeys": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "alertIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "operationalIncidentRef": {
    "type": "string",
    "nullable": true,
    "description": "The linked operational incident, where both apply (AIC-250)."
   },
   "containment": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "action": {
       "type": "string"
      },
      "targetRef": {
       "type": "string"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "byPrincipalId": {
       "type": "string",
       "format": "uuid"
      }
     }
    },
    "readOnly": true
   },
   "rootCause": {
    "type": "string",
    "nullable": true
   },
   "remediation": {
    "type": "string",
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "containedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRelease": {
  "type": "object",
  "x-ticvai-persistence": "ai.release",
  "description": "**The release pointer per capability and tenant** (design 3.5): draft, offline evaluation, shadow, canary, production, monitored. Rollback is a pointer switch. **A model goes live only when a person promotes it** (design 3.12, decided 29 September).",
  "required": [
   "capabilityKey",
   "artefactKind",
   "candidateRef",
   "layer",
   "stage"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "capabilityKey": {
    "type": "string"
   },
   "artefactKind": {
    "type": "string",
    "enum": [
     "model",
     "prompt",
     "routing",
     "embedding",
     "retrieval",
     "rule"
    ]
   },
   "candidateRef": {
    "type": "string"
   },
   "currentRef": {
    "type": "string",
    "nullable": true,
    "description": "What production runs now: the rule, or the previously promoted artefact."
   },
   "previousRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "layer": {
    "type": "string",
    "enum": [
     "platform",
     "tenant"
    ]
   },
   "suggestionKind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SuggestionKind"
     }
    ],
    "nullable": true,
    "description": "Where the capability answers a `requestSuggestion` kind: promotion rewrites that kind's assignment in `AiPolicy.suggestionProviders`."
   },
   "stage": {
    "type": "string",
    "enum": [
     "draft",
     "offlineEval",
     "shadow",
     "canary",
     "production",
     "monitored",
     "rolledBack",
     "rejected"
    ],
    "readOnly": true
   },
   "shadowStartedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "gatePassedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the shadow run passed its gate and `promotionReady` was raised."
   },
   "canaryScope": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Venues or share of traffic in canary."
   },
   "promotedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "promotedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "rolledBackByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "rolledBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRiskClass": {
  "type": "string",
  "enum": [
   "low",
   "medium",
   "high",
   "critical"
  ],
  "description": "Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."
 },
 "AiRiskRegisterEntry": {
  "type": "object",
  "x-ticvai-persistence": "ai.risk_register",
  "description": "**The AI risk register** (ADM-550): ongoing risks of AI capabilities with likelihood, impact, controls and residual rating. Board 1 classifies capabilities; this manages the risks over time.",
  "required": [
   "title",
   "category",
   "likelihood",
   "impact"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "title": {
    "type": "string"
   },
   "category": {
    "type": "string",
    "enum": [
     "customer",
     "commercial",
     "financial",
     "operational",
     "security",
     "modelQuality",
     "privacy",
     "compliance"
    ]
   },
   "capabilityKeys": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "likelihood": {
    "type": "integer",
    "minimum": 1,
    "maximum": 5
   },
   "impact": {
    "type": "integer",
    "minimum": 1,
    "maximum": 5
   },
   "inherentRating": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "readOnly": true
   },
   "controlKeys": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "residualRating": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "treatment": {
    "type": "string",
    "enum": [
     "accept",
     "mitigate",
     "transfer",
     "avoid"
    ]
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "mitigating",
     "accepted",
     "closed"
    ]
   },
   "reviewDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "updatedAt": {
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
 "AiTrainingRun": {
  "type": "object",
  "x-ticvai-persistence": "ai.training_run",
  "description": "**One per-tenant training run** (29 September, AI functions review; design 3.5): trained on the tenant's own data only, backtested, then run in shadow. When its shadow period passes the gate, the release moves to `gatePassedAt` and a `promotionReady` alert goes to the admin (AI-D16).",
  "required": [
   "capabilityKey",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "capabilityKey": {
    "type": "string"
   },
   "suggestionKind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SuggestionKind"
     }
    ],
    "nullable": true
   },
   "forecastDefinitionKey": {
    "type": "string",
    "nullable": true
   },
   "trainingWindowFrom": {
    "type": "string",
    "format": "date"
   },
   "trainingWindowTo": {
    "type": "string",
    "format": "date"
   },
   "dataCutoffAt": {
    "type": "string",
    "format": "date-time"
   },
   "includesImportedHistory": {
    "type": "boolean",
    "default": false
   },
   "featureSetVersion": {
    "type": "string"
   },
   "artefactRef": {
    "type": "string",
    "nullable": true,
    "description": "The model file in the tenant's Blob container."
   },
   "backtestRunId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.eval_run"
   },
   "releaseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.release"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "training",
     "backtesting",
     "shadow",
     "gatePassed",
     "gateFailed",
     "failed"
    ]
   },
   "metrics": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiUsageReport": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from ai.activity",
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
    "type": "string"
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "interactions": {
       "type": "integer"
      },
      "promptTokens": {
       "type": "integer"
      },
      "completionTokens": {
       "type": "integer"
      },
      "cost": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "p95LatencyMs": {
       "type": "integer"
      },
      "refusalRate": {
       "type": "number"
      },
      "rejectionRate": {
       "type": "number",
       "description": "Proposals a person refused. **The number that says whether the assistant is worth having**, and the one nobody thinks to measure.\n"
      }
     }
    }
   },
   "forecast": {
    "type": "object",
    "nullable": true,
    "description": "**A month-end projection, labelled a forecast** (AI design 2.3, 4.5). Present where `to` is inside the current month. Never added into `rows`.\n",
    "properties": {
     "label": {
      "type": "string",
      "enum": [
       "forecast"
      ]
     },
     "periodEnd": {
      "type": "string",
      "format": "date"
     },
     "projectedTokens": {
      "type": "integer"
     },
     "projectedCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "basis": {
      "type": "string",
      "description": "How it was projected, e.g. the run rate of the last 7 days."
     }
    }
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
 "SuggestionKind": {
  "type": "string",
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline.\n",
  "enum": [
   "price",
   "replenishment",
   "requisition",
   "demandForecast",
   "prepPlan",
   "menuEngineering",
   "staffing",
   "slaTarget",
   "waitTime",
   "upsell",
   "segmentation",
   "anomaly",
   "scenario",
   "sendTime",
   "wasteRisk",
   "queueBalancing",
   "itinerary"
  ]
 }
}
```
