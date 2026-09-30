# WS123 — AI Governance board 3

**10 screens · 7 operations · 15 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `AI_AUDIT_VIEW, AI_USE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-539` | AI Explainability & Audit Command Center | commandCentre | 1 | 0 | — |
| `ADM-540` | AI Decision Explorer & Search | listDetail | 2 | 0 | — |
| `ADM-541` | AI Decision Explanation Workspace | listDetail | 1 | 0 | — |
| `ADM-542` | Data, Feature & Evidence Provenance | listDetail | 1 | 0 | — |
| `ADM-543` | Candidate, Rule & Decision Path Trace | listDetail | 2 | 0 | — |
| `ADM-544` | Model, Provider & AI Runtime Trace | listDetail | 2 | 0 | — |
| `ADM-545` | Governance, Approval & Human Decision Trace | listDetail | 1 | 0 | — |
| `ADM-546` | Execution & Business Outcome Trace | listDetail | 2 | 0 | — |
| `ADM-547` | AI Audit Record & Evidence Package | listDetail | 2 | 0 | — |
| `ADM-548` | AI Trace Investigation & Replay Simulator | listDetail | 2 | 0 | — |

## Thin screens in this batch

**ADM-541, ADM-542, ADM-543, ADM-544, ADM-545, ADM-546, ADM-548 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-539",
  "name": "AI Explainability & Audit Command Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "1",
   "page": 55
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-explainability-audit-command-center-adm-539",
   "component": "apps/ticvai-web/src/routes/platform/AiExplainabilityAuditCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-540",
    "ADM-541",
    "ADM-542",
    "ADM-543",
    "ADM-544",
    "ADM-545",
    "ADM-546",
    "ADM-547",
    "ADM-548"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-540",
     "trigger": "AI Decision Explorer & Search",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-541",
     "trigger": "AI Decision Explanation Workspace",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-542",
     "trigger": "Data, Feature & Evidence Provenance",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-543",
     "trigger": "Candidate, Rule & Decision Path Trace",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-544",
     "trigger": "Model, Provider & AI Runtime Trace",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-545",
     "trigger": "Governance, Approval & Human Decision Trace",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-546",
     "trigger": "Execution & Business Outcome Trace",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-547",
     "trigger": "AI Audit Record & Evidence Package",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-548",
     "trigger": "AI Trace Investigation & Replay Simulator",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide management, governance teams and authorized auditors with one central view of AI decisions, explanations, trace completeness and audit status across TICVAI.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search explainability audit",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Capability",
        "Risk",
        "Model",
        "Provider",
        "Human Involvement",
        "Decision",
        "Environment",
        "Date"
       ],
       "notes": "The pack filters this screen by tenant, venue, capability, risk, model, provider and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "AI Decisions Today",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Governed AI Actions",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Automated Decisions",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Human-Reviewed Decisions",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Human Overrides",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Blocked Decisions",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Explainability Coverage",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Complete Decision Traces",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Incomplete Traces",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Audit Warnings",
       "provenance": "pack AI_Governance_Reference.pdf, page 55 §Header KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The explainability audit list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the explainability audit untouched.",
   "emptyFirstRun": "No explainability audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the explainability audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchAiDecisions",
    "contract": "ai",
    "purpose": "Find AI decisions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-539",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-539"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 55. 0 of 10 labels bound to a contract property; 20 of 58 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-540",
  "name": "AI Decision Explorer & Search",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "2",
   "page": 56
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-decision-explorer-search-adm-540",
   "component": "apps/ticvai-web/src/routes/platform/AiDecisionExplorerSearch.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-539"
   ],
   "exitTo": [
    "ADM-539"
   ],
   "transitions": [
    {
     "to": "ADM-539",
     "trigger": "Back to AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized users to locate any AI decision or AI-driven action across TICVAI. This becomes the entry point when someone asks: “Why did TICVAI do this?” Search By Support: Decision ID Trace ID Approval ID Execution ID Transaction ID Customer Reference Session ID User Product Ticket Order Venue AI Capability Model Version Date / Time Example Search Transaction ORD-928410 Results: Time AI Capability Decision Related Object Result 13:42 Recommendation AI Fast Pass ORD-928410 Accepted 13:44 Recommendation AI Family Meal ORD-928410 Ignored 13:46 Fraud AI Risk Assessment ORD-928410 Low Risk Decision Card Selecting a decision displays: Decision ID DEC-49102 Capability Recommendation Engine Customer CUS-****821 Channel B2C Journey Stage Checkout Decision Recommend Fast Pass Rank #1 Confidence 87% Model REC-v3.2 Status Delivered Relationship Search Allow navigation: Customer → Session → Decision → Delivery → Transaction",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 56"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 56"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "searchAiDecisions",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getAiDecisionTrace",
       "notes": "One record, read-only."
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue",
       "operation": "searchAiDecisions",
       "notes": "Sent as `venueId` (18 September minutes, M18-03: searchable by venue).",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "searchField",
       "label": "Customer",
       "operation": "searchAiDecisions",
       "notes": "Sent as `subjectRef`, the guest profile id (M18-03: searchable by customer).",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The decision search list.",
   "error": "Could not load. Names which read failed and leaves the decision search untouched.",
   "emptyFirstRun": "No decision search yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the decision search are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchAiDecisions",
    "contract": "ai",
    "purpose": "Find AI decisions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-540",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-540"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 56. 0 of 0 labels bound to a contract property; 0 of 61 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionRecordId",
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
  "id": "ADM-541",
  "name": "AI Decision Explanation Workspace",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "3",
   "page": 58
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-decision-explanation-workspace-adm-541",
   "component": "apps/ticvai-web/src/routes/platform/AiDecisionExplanationWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-539"
   ],
   "exitTo": [
    "ADM-539"
   ],
   "transitions": [
    {
     "to": "ADM-539",
     "trigger": "Back to AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Explain a selected AI decision in a clear business-readable format.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 58"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 58"
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
       "impliedBy": "getAiDecisionTrace",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The decision explanation list.",
   "error": "Could not load. Names which read failed and leaves the decision explanation untouched.",
   "emptyFirstRun": "No decision explanation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the decision explanation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-541",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-541"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 58. 0 of 0 labels bound to a contract property; 0 of 54 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionRecordId",
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
  "id": "ADM-542",
  "name": "Data, Feature & Evidence Provenance",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "4",
   "page": 60
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/data-feature-evidence-provenance-adm-542",
   "component": "apps/ticvai-web/src/routes/platform/DataFeatureEvidenceProvenance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-539"
   ],
   "exitTo": [
    "ADM-539"
   ],
   "transitions": [
    {
     "to": "ADM-539",
     "trigger": "Back to AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show exactly which data and evidence contributed to an AI decision and where each item originated. This is critical for trust.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 60"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 60"
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
       "impliedBy": "getAiDecisionTrace",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data feature evidence list.",
   "error": "Could not load. Names which read failed and leaves the data feature evidence untouched.",
   "emptyFirstRun": "No data feature evidence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data feature evidence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-542",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-542"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 60. 0 of 0 labels bound to a contract property; 0 of 60 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionRecordId",
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
  "id": "ADM-543",
  "name": "Candidate, Rule & Decision Path Trace",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "5",
   "page": 62
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/candidate-rule-decision-path-trace-adm-543",
   "component": "apps/ticvai-web/src/routes/platform/CandidateRuleDecisionPathTrace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-539"
   ],
   "exitTo": [
    "ADM-539"
   ],
   "transitions": [
    {
     "to": "ADM-539",
     "trigger": "Back to AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Explain how TICVAI moved from all possible options to the final AI decision. This is particularly important for recommendation, fraud, pricing and configuration decisions. Example — Recommendation 48 Potential Products ↓ 42 Active 6 removed ↓ 35 Channel Eligible 7 removed ↓ 28 Date / Time Eligible 7 removed ↓ 22 Customer Eligible 6 removed ↓ 18 Capacity Available 4 removed ↓ 14 Passed Exclusions 4 removed ↓ 10 Passed Guardrails 4 removed ↓ 10 Ranked ↓ Fast Pass #1",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Governance_Reference.pdf, page 62 §Show"
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
       "label": "Every candidate rule decision",
       "columns": [
        "Rule",
        "CAP-014",
        "PASS",
        "Exclusion Trace",
        "VIP Tour",
        "Remaining Capacity = 0"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Governance_Reference.pdf, page 62 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected candidate rule decision",
       "bindsTo": null,
       "columns": [
        "Rule",
        "CAP-014",
        "PASS",
        "Exclusion Trace",
        "VIP Tour",
        "Remaining Capacity = 0"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Candidate Table”, “Governance”, “Approval”, “Signals”.",
       "provenance": "pack AI_Governance_Reference.pdf, page 62 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The candidate rule decision list.",
   "error": "Could not load. Names which read failed and leaves the candidate rule decision untouched.",
   "emptyFirstRun": "No candidate rule decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the candidate rule decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "explainRecommendationDecision",
    "contract": "ai",
    "purpose": "Why these recommendations",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Rule",
    "CAP-014",
    "PASS",
    "Exclusion Trace",
    "VIP Tour",
    "Remaining Capacity = 0"
   ],
   "params": [
    {
     "name": "decisionId",
     "from": "navigation"
    },
    {
     "name": "decisionRecordId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-543",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-543"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 62. 0 of 6 labels bound to a contract property; 11 of 62 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-544",
  "name": "Model, Provider & AI Runtime Trace",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "6",
   "page": 64
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/model-provider-ai-runtime-trace-adm-544",
   "component": "apps/ticvai-web/src/routes/platform/ModelProviderAiRuntimeTrace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-539"
   ],
   "exitTo": [
    "ADM-539"
   ],
   "transitions": [
    {
     "to": "ADM-539",
     "trigger": "Back to AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Record which AI technology produced or contributed to the decision. This gives TICVAI provider and model traceability without duplicating AI Platform configuration.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Governance_Reference.pdf, page 64 §Show"
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
       "label": "Every model provider runtime",
       "columns": [
        "AI Capability",
        "Engine",
        "Provider",
        "Model",
        "Model Version",
        "Deployment Reference",
        "Prompt / Template Version Reference",
        "Rule Engine Version",
        "Feature Set Version",
        "Knowledge Source Version",
        "Request Timestamp",
        "Response Timestamp",
        "Latency",
        "Tokens / Compute where applicable",
        "Provider Request Reference",
        "Fallback Used",
        "Retry Count",
        "Primary Provider",
        "↓",
        "Timeout",
        "Fallback Provider",
        "Success"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Governance_Reference.pdf, page 64 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected model provider runtime",
       "bindsTo": null,
       "columns": [
        "AI Capability",
        "Engine",
        "Provider",
        "Model",
        "Model Version",
        "Deployment Reference",
        "Prompt / Template Version Reference",
        "Rule Engine Version",
        "Feature Set Version",
        "Knowledge Source Version",
        "Request Timestamp",
        "Response Timestamp",
        "Latency",
        "Tokens / Compute where applicable",
        "Provider Request Reference",
        "Fallback Used",
        "Retry Count",
        "Primary Provider",
        "↓",
        "Timeout",
        "Fallback Provider",
        "Success"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Prompt Template”, “Latency”, “Version Traceability”, “Important Boundary”.",
       "provenance": "pack AI_Governance_Reference.pdf, page 64 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The model provider runtime list.",
   "error": "Could not load. Names which read failed and leaves the model provider runtime untouched.",
   "emptyFirstRun": "No model provider runtime yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the model provider runtime are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiModels",
    "contract": "ai",
    "purpose": "The model catalogue",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "AI Capability",
    "Engine",
    "Provider",
    "Model",
    "Model Version",
    "Deployment Reference"
   ],
   "params": [
    {
     "name": "decisionRecordId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-544",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-544"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 64. 0 of 22 labels bound to a contract property; 22 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-545",
  "name": "Governance, Approval & Human Decision Trace",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "7",
   "page": 66
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/governance-approval-human-decision-trace-adm-545",
   "component": "apps/ticvai-web/src/routes/platform/GovernanceApprovalHumanDecisionTrace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-539"
   ],
   "exitTo": [
    "ADM-539"
   ],
   "transitions": [
    {
     "to": "ADM-539",
     "trigger": "Back to AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Connect Board 1 and Board 2 governance activity to the AI decision.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 66"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 66"
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
       "impliedBy": "getAiDecisionTrace",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance approval human list.",
   "error": "Could not load. Names which read failed and leaves the governance approval human untouched.",
   "emptyFirstRun": "No governance approval human yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance approval human are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-545",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-545"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 66. 0 of 0 labels bound to a contract property; 0 of 65 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionRecordId",
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
  "id": "ADM-546",
  "name": "Execution & Business Outcome Trace",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "8",
   "page": 68
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/execution-business-outcome-trace-adm-546",
   "component": "apps/ticvai-web/src/routes/platform/ExecutionBusinessOutcomeTrace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-539"
   ],
   "exitTo": [
    "ADM-539"
   ],
   "transitions": [
    {
     "to": "ADM-539",
     "trigger": "Back to AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Connect the AI decision to what actually happened in TICVAI. A good AI audit cannot stop at: “AI recommended X.” It needs to know: Was X actually executed, and what was the outcome? Execution Trace Example: AI Proposal Change Adult Weekend Price ↓ Approved AED 150 ↓ Execution Authorization AUTH-9281 ↓ Pricing API Update Pricing Profile ↓ Execution Result SUCCESS Before / After Before Adult Weekend = AED 140 After Adult Weekend = AED 150 Execution Metadata Execution ID Owning Module API / Service Start Time Completion Time Result Retry Failure Rollback Final State",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 68"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 68"
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
       "impliedBy": "getActionPlan",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The execution business outcome list.",
   "error": "Could not load. Names which read failed and leaves the execution business outcome untouched.",
   "emptyFirstRun": "No execution business outcome yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the execution business outcome are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-546",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-546"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 68. 0 of 0 labels bound to a contract property; 0 of 65 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionRecordId",
     "from": "navigation"
    },
    {
     "name": "planId",
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
  "id": "ADM-547",
  "name": "AI Audit Record & Evidence Package",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "9",
   "page": 70
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-audit-record-evidence-package-adm-547",
   "component": "apps/ticvai-web/src/routes/platform/AiAuditRecordEvidencePackage.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-539"
   ],
   "exitTo": [
    "ADM-539"
   ],
   "transitions": [
    {
     "to": "ADM-539",
     "trigger": "Back to AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a complete, tamper-evident audit package for an AI decision or group of decisions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Single Decision, Customer Journey, AI Capability, Incident, Model Version, Governance Policy. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Governance_Reference.pdf, page 70 §Allow"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 70"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 70"
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
       "label": "Single Decision",
       "provenance": "pack AI_Governance_Reference.pdf, page 70 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Journey",
       "provenance": "pack AI_Governance_Reference.pdf, page 70 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "AI Capability",
       "provenance": "pack AI_Governance_Reference.pdf, page 70 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Incident",
       "provenance": "pack AI_Governance_Reference.pdf, page 70 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Model Version",
       "provenance": "pack AI_Governance_Reference.pdf, page 70 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Governance Policy",
       "provenance": "pack AI_Governance_Reference.pdf, page 70 §Allow"
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
   "loading": "The audit record evidence list.",
   "error": "Could not load. Names which read failed and leaves the audit record evidence untouched.",
   "emptyFirstRun": "No audit record evidence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the audit record evidence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchAiDecisions",
    "contract": "ai",
    "purpose": "Find AI decisions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "exportAiEvidencePackage",
    "contract": "ai",
    "purpose": "Export an evidence package",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-547",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-547"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 70. 0 of 0 labels bound to a contract property; 6 of 50 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-548",
  "name": "AI Trace Investigation & Replay Simulator",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "3",
   "number": "10",
   "page": 71
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-trace-investigation-replay-simulator-adm-548",
   "component": "apps/ticvai-web/src/routes/platform/AiTraceInvestigationReplaySimulator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-539"
   ],
   "exitTo": [
    "ADM-539"
   ],
   "transitions": [
    {
     "to": "ADM-539",
     "trigger": "Back to AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare) and no metric row",
  "purpose": "Allow authorized governance/technical teams to reconstruct an AI decision and understand whether the same conditions would produce the same or a different outcome. This should be a powerful investigation tool.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Governance_Reference.pdf, page 71 §Compare"
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
       "label": "Every trace investigation replay",
       "columns": [
        "Model v3.2",
        "Model v3.3",
        "Alternative Policy Replay",
        "Governance v1.4",
        "Governance v1.5",
        "Comparison"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Governance_Reference.pdf, page 71 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected trace investigation replay",
       "bindsTo": null,
       "columns": [
        "Model v3.2",
        "Model v3.3",
        "Alternative Policy Replay",
        "Governance v1.4",
        "Governance v1.5",
        "Comparison"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Original Time”, “Result”, “Exact Historical Replay”, “Element Original Replay”, “Eligibility Same Same”, “Authorized investigator can record”.",
       "provenance": "pack AI_Governance_Reference.pdf, page 71 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The trace investigation replay list.",
   "error": "Could not load. Names which read failed and leaves the trace investigation replay untouched.",
   "emptyFirstRun": "No trace investigation replay yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the trace investigation replay are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "replayAiDecision",
    "contract": "ai",
    "purpose": "Re-simulate a decision",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Model v3.2",
    "Model v3.3",
    "Alternative Policy Replay",
    "Governance v1.4",
    "Governance v1.5",
    "Comparison"
   ],
   "params": [
    {
     "name": "decisionRecordId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-548",
   "workshopBoard": "wireframes/WS16 AI Governance Board 3.dc.html#adm-548"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 71. 0 of 6 labels bound to a contract property; 6 of 259 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "explainRecommendationDecision": {
  "method": "GET",
  "path": "/recommendations/decisions/{decisionId}/explanation",
  "contract": "ai",
  "summary": "Why these recommendations",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "depth",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiRecommendationExplanation"
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
 "getActionPlan": {
  "method": "GET",
  "path": "/action-plans/{planId}",
  "contract": "ai",
  "summary": "A plan with its steps",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiActionPlanDetail"
 },
 "getAiDecisionTrace": {
  "method": "GET",
  "path": "/decision-records/{decisionRecordId}/trace",
  "contract": "ai",
  "summary": "The full trace of a decision",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "depth",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiDecisionTrace"
 },
 "listAiModels": {
  "method": "GET",
  "path": "/models",
  "contract": "ai",
  "summary": "The model catalogue",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "layer",
    "in": "query",
    "required": null
   },
   {
    "name": "producerType",
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
 "replayAiDecision": {
  "method": "POST",
  "path": "/decision-records/{decisionRecordId}/replay",
  "contract": "ai",
  "summary": "Re-simulate a decision",
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
  "responds": "AiReplayResult"
 },
 "searchAiDecisions": {
  "method": "GET",
  "path": "/decision-records",
  "contract": "ai",
  "summary": "Find AI decisions",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "capabilityKey",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "subjectRef",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "traceId",
    "in": "query",
    "required": null
   },
   {
    "name": "policyVersion",
    "in": "query",
    "required": null
   },
   {
    "name": "modelVersion",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiActionPlan": {
  "type": "object",
  "x-ticvai-persistence": "ai.action_plan",
  "description": "**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).",
  "required": [
   "origin",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "origin": {
    "type": "string",
    "enum": [
     "configurationSession",
     "generateConfiguration",
     "assistant",
     "riskCase",
     "operationalRequirement",
     "rollback"
    ]
   },
   "originRef": {
    "type": "string",
    "nullable": true
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "validated",
     "simulated",
     "awaitingApproval",
     "approved",
     "executing",
     "paused",
     "completed",
     "partiallyCompleted",
     "failed",
     "compensated",
     "cancelled",
     "rolledBack"
    ],
    "readOnly": true
   },
   "autonomyLevel": {
    "$ref": "#/components/schemas/AiAutonomyLevel"
   },
   "approvalTier": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request, where tier 2 or the matrix caught the plan."
   },
   "proposedActionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.proposed_action",
    "description": "The `ai.proposed_action` the plan is presented as for a decision."
   },
   "changeSetHash": {
    "type": "string",
    "readOnly": true
   },
   "governanceOutcome": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiGovernanceOutcome"
     }
    ],
    "readOnly": true
   },
   "policyVersionRef": {
    "type": "string",
    "readOnly": true,
    "description": "The governance policy version that decided it."
   },
   "simulation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true,
    "description": "Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."
   },
   "partialCompletionAllowed": {
    "type": "boolean",
    "default": false,
    "description": "Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."
   },
   "rollbackOfPlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.action_plan"
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "createdAt": {
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
 "AiActionPlanDetail": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.action_plan with its ai.action_step rows",
  "description": "A plan with its steps in DAG order.",
  "required": [
   "plan",
   "steps"
  ],
  "properties": {
   "plan": {
    "$ref": "#/components/schemas/AiActionPlan"
   },
   "steps": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiActionStep"
    }
   }
  }
 },
 "AiActionStep": {
  "type": "object",
  "x-ticvai-persistence": "ai.action_step",
  "description": "One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).",
  "required": [
   "planId",
   "stepNumber",
   "toolKey",
   "targetContract",
   "targetOperation",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.action_plan"
   },
   "stepNumber": {
    "type": "integer",
    "minimum": 1
   },
   "dependsOn": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 1
    },
    "description": "Step numbers that must succeed first. The plan is a DAG."
   },
   "toolKey": {
    "type": "string"
   },
   "targetContract": {
    "type": "string"
   },
   "targetOperation": {
    "type": "string"
   },
   "contractVersion": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body of `targetOperation`, validated against it before the plan is approved."
   },
   "provenance": {
    "$ref": "#/components/schemas/AiProvenance"
   },
   "idempotencyKey": {
    "type": "string",
    "readOnly": true
   },
   "targetObjectRef": {
    "type": "string",
    "nullable": true
   },
   "targetObjectVersion": {
    "type": "string",
    "nullable": true,
    "description": "The version the step was planned against. A different version at execution is drift."
   },
   "reversible": {
    "type": "boolean"
   },
   "compensation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "validated",
     "running",
     "succeeded",
     "failed",
     "compensated",
     "skipped",
     "paused"
    ],
    "readOnly": true
   },
   "attempts": {
    "type": "integer",
    "minimum": 0,
    "maximum": 3,
    "readOnly": true,
    "description": "Bounded at 3 (AIC-135)."
   },
   "lastError": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "resultRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The owning service's response: success is its answer, not a model's judgement (AIC-097)."
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "AiCapability": {
  "type": "string",
  "description": "What a capability needs, not which provider serves it. This indirection is what makes \"no provider SDK in capability code\" enforceable.\n**`speechToText` and `textToSpeech` added 18 August (BL-164)** — voice added rather than declined. **Speech is the capability where UAE residency is hardest to satisfy**: the major providers run it in fewer regions than text, and a guest speaking into a kiosk is producing personal data in the moment. `AiProvider.residency` already carries the constraint and **speech is the capability most likely to fail it**, which is why it is separate rather than folded into `chat`.\n",
  "enum": [
   "chat",
   "embedding",
   "vision",
   "rerank",
   "speechToText",
   "textToSpeech"
  ]
 },
 "AiDecisionRecord": {
  "type": "object",
  "x-ticvai-persistence": "ai.decision_record",
  "description": "**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.",
  "required": [
   "traceId",
   "capabilityKey",
   "outcome",
   "recordHash"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "traceId": {
    "type": "string"
   },
   "capabilityKey": {
    "type": "string"
   },
   "task": {
    "type": "string",
    "nullable": true
   },
   "subjectKind": {
    "type": "string",
    "nullable": true
   },
   "subjectRef": {
    "type": "string",
    "nullable": true
   },
   "inputsRef": {
    "type": "string",
    "nullable": true,
    "description": "Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."
   },
   "evidence": {
    "$ref": "#/components/schemas/AiEvidenceItemList"
   },
   "producer": {
    "type": "string",
    "nullable": true
   },
   "modelVersion": {
    "type": "string",
    "nullable": true
   },
   "promptTemplateVersion": {
    "type": "string",
    "nullable": true
   },
   "featureSetVersion": {
    "type": "string",
    "nullable": true
   },
   "knowledgeVersion": {
    "type": "string",
    "nullable": true
   },
   "ruleVersions": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "governanceOutcome": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiGovernanceOutcome"
     }
    ],
    "nullable": true
   },
   "policyVersion": {
    "type": "string",
    "nullable": true
   },
   "approvals": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Approval requests and their decisions."
   },
   "humanDecision": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Override or intervention, where a person changed the outcome."
   },
   "executionResult": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "outcomeRef": {
    "type": "string",
    "nullable": true,
    "description": "The business outcome it links to (an order, a published version, a closed case)."
   },
   "outcome": {
    "type": "string",
    "enum": [
     "answered",
     "refused",
     "allowed",
     "blocked",
     "executed",
     "failed",
     "approvedThenFailed",
     "published",
     "suggested"
    ],
    "description": "`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."
   },
   "annotations": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "byPrincipalId": {
       "type": "string",
       "format": "uuid"
      },
      "note": {
       "type": "string"
      }
     }
    },
    "readOnly": true,
    "description": "Corrections, appended; the original fields are never edited."
   },
   "previousHash": {
    "type": "string",
    "readOnly": true
   },
   "recordHash": {
    "type": "string",
    "readOnly": true
   },
   "createdAt": {
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
 "AiDecisionTrace": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.decision_record with the rows it references",
  "description": "**The full trace of one decision** (ADM-540..546): record, evidence, candidates and rules, model and runtime, governance and approvals, execution and business outcome. Depth is gated by permission (AIC-195).",
  "required": [
   "record"
  ],
  "properties": {
   "record": {
    "$ref": "#/components/schemas/AiDecisionRecord"
   },
   "depth": {
    "type": "string",
    "enum": [
     "business",
     "governance",
     "technical"
    ]
   },
   "explanation": {
    "type": "string",
    "description": "Built from structured evidence, never a model's chain of thought (AIC-192)."
   },
   "activity": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiInteraction"
    },
    "description": "The model calls behind it (`technical` depth)."
   },
   "plan": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiActionPlanDetail"
     }
    ],
    "nullable": true
   },
   "interventions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiIntervention"
    }
   },
   "chainVerified": {
    "type": "boolean",
    "description": "The hash chain around this record verifies."
   }
  }
 },
 "AiEvidenceItemList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "The evidence of one decision record, stored with it.",
  "items": {
   "$ref": "#/components/schemas/AiEvidenceItem"
  }
 },
 "AiGovernanceOutcome": {
  "type": "string",
  "enum": [
   "allow",
   "allowWithConditions",
   "prepareOnly",
   "approvalRequired",
   "escalate",
   "block"
  ],
  "description": "What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."
 },
 "AiInteraction": {
  "type": "object",
  "x-ticvai-persistence": "ai.activity",
  "required": [
   "id",
   "principalId",
   "capability",
   "outcome",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "conversationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "audience": {
    "type": "string",
    "enum": [
     "staff",
     "guest"
    ],
    "description": "**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"
   },
   "billableToTenantId": {
    "type": "string",
    "format": "uuid",
    "description": "Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"
   },
   "scopePath": {
    "type": "string"
   },
   "capability": {
    "type": "string"
   },
   "prompt": {
    "type": "string"
   },
   "response": {
    "type": "string"
   },
   "sources": {
    "$ref": "#/components/schemas/AiSourceList"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "answered",
     "refused",
     "applied",
     "rejected",
     "failed"
    ]
   },
   "refusalReason": {
    "type": "string",
    "nullable": true
   },
   "provider": {
    "$ref": "#/components/schemas/AiProviderKind"
   },
   "model": {
    "type": "string"
   },
   "promptTokens": {
    "type": "integer"
   },
   "completionTokens": {
    "type": "integer"
   },
   "cost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "x-ticvai-column": "cost_amount",
    "description": "What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"
   },
   "latencyMs": {
    "type": "integer"
   },
   "maskedFieldCount": {
    "type": "integer",
    "description": "How many fields were redacted. Zero on a prompt touching guest data is a defect."
   },
   "traceId": {
    "type": "string"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."
   },
   "cacheLayer": {
    "type": "string",
    "nullable": true,
    "enum": [
     "guardrail",
     "semantic",
     "exact",
     "negative",
     "analytics"
    ],
    "description": "Which cache answered, where one did (AI design 3.6). Null for a model call."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiIntervention": {
  "type": "object",
  "x-ticvai-persistence": "ai.intervention",
  "description": "**A person stepping in** (AIC-187, ADM-535, ADM-536): an override, pause, resume, stop, retry or rollback, with the original AI decision and the human one side by side.",
  "required": [
   "kind",
   "targetKind",
   "targetRef"
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
     "override",
     "pause",
     "resume",
     "cancel",
     "retry",
     "rollback",
     "capabilityPause",
     "capabilityResume"
    ]
   },
   "targetKind": {
    "type": "string",
    "enum": [
     "plan",
     "step",
     "decision",
     "capability"
    ]
   },
   "targetRef": {
    "type": "string"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "originalDecision": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "humanDecision": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "reason": {
    "type": "string",
    "maxLength": 2000
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "createdAt": {
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
 "AiModel": {
  "type": "object",
  "x-ticvai-persistence": "ai.model",
  "description": "**The model catalogue** (design 3.1 Registry, 3.3; AIC-013, AIC-026). One row per model a task can be routed to: large language models, embedding and reranking models, and classical models (LightGBM, statistical forecasters) registered the same way so lifecycle, release and audit are uniform. **Platform rows** are mastered in the control plane and replicated read-only into each tenant database with the tenant root as `scopePath`; a tenant row exists only where bring-your-own-key is enabled for the tenant.",
  "required": [
   "layer",
   "modelName",
   "producerType"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "layer": {
    "type": "string",
    "enum": [
     "platform",
     "tenant"
    ]
   },
   "providerKind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiProviderKind"
     }
    ],
    "nullable": true
   },
   "producerType": {
    "type": "string",
    "enum": [
     "llm",
     "embedding",
     "reranker",
     "classical",
     "rule"
    ]
   },
   "modelName": {
    "type": "string",
    "description": "The deployment or model name as the provider knows it, or the package and version for a classical model."
   },
   "capabilities": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiCapability"
    }
   },
   "contextTokens": {
    "type": "integer",
    "nullable": true
   },
   "toolCalling": {
    "type": "boolean",
    "default": false
   },
   "structuredOutput": {
    "type": "boolean",
    "default": false
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "residency": {
    "type": "string",
    "nullable": true,
    "description": "Where inference happens. Checked against `tenancy.RegionSettings.allowedAiResidencies`."
   },
   "inputCostPerMillionTokens": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "outputCostPerMillionTokens": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
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
   "isDefaultForTasks": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Tasks this model is the default for (AIC-010), e.g. `assistant.guest.answer`, `config.extract`."
   },
   "taskFitness": {
    "type": "array",
    "readOnly": true,
    "description": "**Evaluated fitness per task** (21 September minutes, M21-09, our proposal): a score from the task's golden set (`runAiEvaluation`) and the band the task needs. Below `floor` the model is underpowered for the task; far above `ceiling` it is overpowered (it costs more than the task needs). `setAiProvider` returns a warning (`AiProvider.fitnessWarnings`) when a choice falls outside the band, and ADM-037 shows the band beside `setAiModel`; neither refuses on it.",
    "items": {
     "type": "object",
     "required": [
      "taskKey",
      "score"
     ],
     "properties": {
      "taskKey": {
       "type": "string"
      },
      "score": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "floor": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "ceiling": {
       "type": "number",
       "minimum": 0,
       "maximum": 1,
       "nullable": true
      },
      "evaluationRunId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "evaluatedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiProviderKind": {
  "type": "string",
  "enum": [
   "openai",
   "gemini",
   "anthropic",
   "azureOpenai",
   "localLlm",
   "openaiCompatible"
  ],
  "description": "`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"
 },
 "AiRecommendationExplanation": {
  "type": "object",
  "x-ticvai-persistence": "none — built from ai.rec_decision and its decision record",
  "description": "Why these items (AIR-193..202), at three depths each gated by permission (AIC-195): business, governance, technical.",
  "required": [
   "decisionId",
   "depth"
  ],
  "properties": {
   "decisionId": {
    "type": "string",
    "format": "uuid"
   },
   "depth": {
    "type": "string",
    "enum": [
     "business",
     "governance",
     "technical"
    ]
   },
   "funnel": {
    "type": "object",
    "additionalProperties": true
   },
   "exclusions": {
    "type": "object",
    "additionalProperties": true
   },
   "items": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "trackingId": {
       "type": "string",
       "format": "uuid"
      },
      "productId": {
       "type": "string",
       "format": "uuid"
      },
      "reasons": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "scoreBreakdown": {
       "type": "object",
       "additionalProperties": true,
       "nullable": true
      }
     }
    }
   },
   "versions": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Strategy, model and feature-set versions. `technical` depth only."
   }
  }
 },
 "AiReplayResult": {
  "type": "object",
  "x-ticvai-persistence": "none — a re-simulation, never stored as a decision",
  "description": "**A re-simulation, labelled as one** (AIC-206, ADM-548): the same inputs through today's or the recorded versions. It runs no production action and is never evidence of what happened.",
  "required": [
   "decisionRecordId",
   "label",
   "sameOutcome"
  ],
  "properties": {
   "decisionRecordId": {
    "type": "string",
    "format": "uuid"
   },
   "label": {
    "type": "string",
    "enum": [
     "reSimulation"
    ]
   },
   "versionsUsed": {
    "type": "string",
    "enum": [
     "recorded",
     "current"
    ]
   },
   "sameOutcome": {
    "type": "boolean"
   },
   "original": {
    "type": "object",
    "additionalProperties": true
   },
   "replayed": {
    "type": "object",
    "additionalProperties": true
   },
   "differences": {
    "type": "array",
    "items": {
     "type": "string"
    }
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
 }
}
```
