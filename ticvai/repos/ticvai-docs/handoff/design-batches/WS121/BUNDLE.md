# WS121 — AI Governance board 1

**10 screens · 17 operations · 20 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, AI_USE, PLATFORM_AI_MANAGE, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-519` | AI Governance Command Center | commandCentre | 5 | 0 | — |
| `ADM-520` | AI Capability Registry & Ownership | listDetail | 2 | 0 | — |
| `ADM-521` | AI Risk Classification & Assessment | listDetail | 2 | 0 | — |
| `ADM-522` | AI Autonomy Level Configuration | configEditor | 3 | 0 | — |
| `ADM-523` | AI Action & Permission Policy Builder | listDetail | 4 | 1 | — |
| `ADM-524` | AI Data Access & Usage Policy | listDetail | 4 | 0 | — |
| `ADM-525` | Environment, Tenant & Scope Governance | listDetail | 2 | 0 | — |
| `ADM-526` | AI Policy Conflict, Exception & Override Management | listDetail | 4 | 1 | — |
| `ADM-527` | AI Policy Testing & Governance Simulation | listDetail | 2 | 0 | — |
| `ADM-528` | AI Governance Policy Publication & Effective Policy Map | listDetail | 3 | 0 | — |

## Thin screens in this batch

**ADM-520, ADM-521, ADM-524, ADM-525, ADM-527 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-519",
  "name": "AI Governance Command Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "1",
   "page": 4
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-governance-command-center-adm-519",
   "component": "apps/ticvai-web/src/routes/platform/AiGovernanceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-520",
    "ADM-521",
    "ADM-522",
    "ADM-523",
    "ADM-524",
    "ADM-525",
    "ADM-526",
    "ADM-527",
    "ADM-528"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-520",
     "trigger": "AI Capability Registry & Ownership",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "capabilityKey"
     ]
    },
    {
     "to": "ADM-521",
     "trigger": "AI Risk Classification & Assessment",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "capabilityKey"
     ]
    },
    {
     "to": "ADM-522",
     "trigger": "AI Autonomy Level Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "capabilityKey"
     ]
    },
    {
     "to": "ADM-523",
     "trigger": "AI Action & Permission Policy Builder",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-524",
     "trigger": "AI Data Access & Usage Policy",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-525",
     "trigger": "Environment, Tenant & Scope Governance",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-526",
     "trigger": "AI Policy Conflict, Exception & Override Management",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-527",
     "trigger": "AI Policy Testing & Governance Simulation",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-528",
     "trigger": "AI Governance Policy Publication & Effective Policy Map",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide management with one centralized view of AI governance across the entire TICVAI platform.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "publishGate",
       "impliedBy": "promoteAiRelease",
       "notes": "Declares `promoteAiRelease`. **The gate names what the publish will affect before it happens**: which tenants, venues or capabilities take the new version, and that the previous one stays available to roll back to.",
       "provenance": "check-screens publish rule, 29 September 2026"
      },
      {
       "kind": "metricTile",
       "label": "AI Capabilities Registered",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Active Governance Policies",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Governed AI Actions Today",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Approval-Required Actions",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Blocked AI Actions",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Policy Exceptions",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "High-Risk AI Capabilities",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Policy Violations",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "AI Autonomy Coverage",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Governance Warnings",
       "provenance": "pack AI_Governance_Reference.pdf, page 4 §Header KPIs"
      },
      {
       "kind": "dataTable",
       "label": "AI maturity by question",
       "bindsTo": "AiCapabilityMaturity",
       "columns": [
        "AiCapabilityMaturity.capabilityKey",
        "AiCapabilityMaturity.stage",
        "AiCapabilityMaturity.maturity",
        "AiCapabilityMaturity.since"
       ],
       "operation": "listAiCapabilityMaturity",
       "notes": "**Starting, learning, established, learned** (AI functions review): where each answer stands, what it is based on and what the next stage needs. A `promotionReady` alert links from the row.",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the governance untouched.",
   "emptyFirstRun": "No governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiCapabilities",
    "contract": "ai",
    "purpose": "The capability registry",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "pauseAiCapability",
    "contract": "ai",
    "purpose": "Stop a capability now",
    "trigger": "onAction",
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
    "operationId": "listAiGovernanceAlerts",
    "contract": "ai",
    "purpose": "Governance alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiCapabilityMaturity",
    "contract": "ai",
    "purpose": "Where each AI answer stands on the way to learned",
    "trigger": "onLoad",
    "provenance": "29 September pass (group A)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-519",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-519"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 4. 0 of 0 labels bound to a contract property; 10 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "capabilityKey",
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
  "id": "ADM-520",
  "name": "AI Capability Registry & Ownership",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "2",
   "page": 5
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-capability-registry-ownership-adm-520",
   "component": "apps/ticvai-web/src/routes/platform/AiCapabilityRegistryOwnership.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-519"
   ],
   "exitTo": [
    "ADM-519"
   ],
   "transitions": [
    {
     "to": "ADM-519",
     "trigger": "Back to AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "capabilityKey"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain a controlled registry of every AI capability operating within TICVAI. Nothing should become an operational AI capability without being identifiable and governed.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 5"
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
       "impliedBy": "listAiCapabilities",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "configureAiCapability",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "configureAiCapability"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capability registry ownership list.",
   "error": "Could not load. Names which read failed and leaves the capability registry ownership untouched.",
   "emptyFirstRun": "No capability registry ownership yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the capability registry ownership are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiCapabilities",
    "contract": "ai",
    "purpose": "The capability registry",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "configureAiCapability",
    "contract": "ai",
    "purpose": "Register a capability, or change its owner, risk class or autonomy",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-520",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-520"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "capabilityKey",
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
  "id": "ADM-521",
  "name": "AI Risk Classification & Assessment",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "3",
   "page": 7
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-risk-classification-assessment-adm-521",
   "component": "apps/ticvai-web/src/routes/platform/AiRiskClassificationAssessment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-519"
   ],
   "exitTo": [
    "ADM-519"
   ],
   "transitions": [
    {
     "to": "ADM-519",
     "trigger": "Back to AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "capabilityKey"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Classify AI capabilities and individual AI action types according to their potential business, customer, financial, operational, security and compliance impact. Risk should not be based only on which AI model is being used.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 7"
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
       "impliedBy": "listAiCapabilities",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "configureAiCapability",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "configureAiCapability"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The risk classification assessment list.",
   "error": "Could not load. Names which read failed and leaves the risk classification assessment untouched.",
   "emptyFirstRun": "No risk classification assessment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the risk classification assessment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiCapabilities",
    "contract": "ai",
    "purpose": "The capability registry",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "configureAiCapability",
    "contract": "ai",
    "purpose": "Register a capability, or change its owner, risk class or autonomy",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-521",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-521"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 61 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "capabilityKey",
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
  "id": "ADM-522",
  "name": "AI Autonomy Level Configuration",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "4",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-autonomy-level-configuration-adm-522",
   "component": "apps/ticvai-web/src/routes/platform/AiAutonomyLevelConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-519"
   ],
   "exitTo": [
    "ADM-519"
   ],
   "transitions": [
    {
     "to": "ADM-519",
     "trigger": "Back to AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "capabilityKey"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population",
  "purpose": "Define exactly how independently AI is permitted to operate. This is one of the most important screens in the governance module. I recommend four controlled levels plus a disabled state. Level 0 — Disabled AI capability cannot operate. Level 1 — Advisory",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack AI_Governance_Reference.pdf, page 9 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack AI_Governance_Reference.pdf, page 9 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "AI Capability",
       "provenance": "pack AI_Governance_Reference.pdf, page 9 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Module",
       "provenance": "pack AI_Governance_Reference.pdf, page 9 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Action Type",
       "provenance": "pack AI_Governance_Reference.pdf, page 9 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "User Role",
       "provenance": "pack AI_Governance_Reference.pdf, page 9 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Environment",
       "provenance": "pack AI_Governance_Reference.pdf, page 9 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Risk Level",
       "provenance": "pack AI_Governance_Reference.pdf, page 9 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Business Unit",
       "provenance": "pack AI_Governance_Reference.pdf, page 9 §Configure by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The autonomy level configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the autonomy level untouched.",
   "emptyFirstRun": "No autonomy level configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listAiCapabilities",
    "contract": "ai",
    "purpose": "The capability registry",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "configureAiCapability",
    "contract": "ai",
    "purpose": "Register a capability, or change its owner, risk class or autonomy",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getEffectiveAiPolicy",
    "contract": "ai",
    "purpose": "The policy in force for a capability at a scope",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-522",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-522"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 9 of 57 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "capabilityKey",
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
  "id": "ADM-523",
  "name": "AI Action & Permission Policy Builder",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "5",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-action-permission-policy-builder-adm-523",
   "component": "apps/ticvai-web/src/routes/platform/AiActionPermissionPolicyBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-519"
   ],
   "exitTo": [
    "ADM-519"
   ],
   "transitions": [
    {
     "to": "ADM-519",
     "trigger": "Back to AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define granular rules controlling what AI is allowed to read, recommend, prepare, modify or execute. This should work alongside TICVAI's existing RBAC/PBAC, not replace it.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 19 actions on this screen and the screen declares 0 operations.** Unserved: Analyze, Recommend, Generate, Prepare, Create, Modify, Delete, Publish …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
   },
   {
    "operation": null,
    "why": "**AI Action & Permission Policy Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 11"
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
       "label": "Analyze",
       "provenance": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend",
       "provenance": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate",
       "provenance": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
      },
      {
       "kind": "secondaryButton",
       "label": "Prepare",
       "provenance": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "provenance": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify",
       "provenance": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete",
       "provenance": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "provenance": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDelete",
    "component": "confirmDialog",
    "trigger": "Delete",
    "body": "**Delete on a action permission policy is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack AI_Governance_Reference.pdf, page 11 §Action Types"
   }
  ],
  "states": {
   "loading": "The action permission policy list.",
   "error": "Could not load. Names which read failed and leaves the action permission policy untouched.",
   "emptyFirstRun": "No action permission policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the action permission policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createAiGovernancePolicyDraft",
    "contract": "ai",
    "purpose": "Draft a governance policy, or a new version of one",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiGovernancePolicyVersions",
    "contract": "ai",
    "purpose": "Governance policies and their versions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiTools",
    "contract": "ai",
    "purpose": "The tool registry",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setAiTool",
    "contract": "ai",
    "purpose": "Register or change a tool (platform)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-523",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-523"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 19 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "toolKey",
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
  "id": "ADM-524",
  "name": "AI Data Access & Usage Policy",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "6",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-data-access-usage-policy-adm-524",
   "component": "apps/ticvai-web/src/routes/platform/AiDataAccessUsagePolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-519"
   ],
   "exitTo": [
    "ADM-519"
   ],
   "transitions": [
    {
     "to": "ADM-519",
     "trigger": "Back to AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control which data categories each AI capability is permitted to access and for what purpose. This complements privacy/consent controls but does not replace TICVAI's core privacy governance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 13"
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
       "impliedBy": "createAiGovernancePolicyDraft",
       "label": "Create",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAiGovernancePolicyVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAiGovernancePolicyDraft"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data access usage list.",
   "error": "Could not load. Names which read failed and leaves the data access usage untouched.",
   "emptyFirstRun": "No data access usage yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data access usage are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createAiGovernancePolicyDraft",
    "contract": "ai",
    "purpose": "Draft a governance policy, or a new version of one",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiGovernancePolicyVersions",
    "contract": "ai",
    "purpose": "Governance policies and their versions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listDataRetentionSettings",
    "contract": "tenancy",
    "purpose": "AI data retention (prompts, conversations, decision records, index)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setDataRetentionSetting",
    "contract": "tenancy",
    "purpose": "Set an AI class's period",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-524",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-524"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "dataClass",
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
  "id": "ADM-525",
  "name": "Environment, Tenant & Scope Governance",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "7",
   "page": 15
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/environment-tenant-scope-governance-adm-525",
   "component": "apps/ticvai-web/src/routes/platform/EnvironmentTenantScopeGovernance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-519"
   ],
   "exitTo": [
    "ADM-519"
   ],
   "transitions": [
    {
     "to": "ADM-519",
     "trigger": "Back to AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "capabilityKey"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow different AI governance rules across TICVAI's multi-tenant and multi-environment architecture. A rule suitable for a development sandbox may not be acceptable in production.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Generate Configuration Allow Allow Allow Allow, Prepare Change Allow Allow Allow Allow, Customer Data Use Synthetic Restricted Restricted Governed. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Governance_Reference.pdf, page 15 §Action Dev Sandbox UAT Production"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 15"
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
       "label": "Generate Configuration Allow Allow Allow Allow",
       "provenance": "pack AI_Governance_Reference.pdf, page 15 §Action Dev Sandbox UAT Production"
      },
      {
       "kind": "secondaryButton",
       "label": "Prepare Change Allow Allow Allow Allow",
       "provenance": "pack AI_Governance_Reference.pdf, page 15 §Action Dev Sandbox UAT Production"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Data Use Synthetic Restricted Restricted Governed",
       "provenance": "pack AI_Governance_Reference.pdf, page 15 §Action Dev Sandbox UAT Production"
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
   "loading": "The environment tenant scope list.",
   "error": "Could not load. Names which read failed and leaves the environment tenant scope untouched.",
   "emptyFirstRun": "No environment tenant scope yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the environment tenant scope are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEffectiveAiPolicy",
    "contract": "ai",
    "purpose": "The policy in force for a capability at a scope",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "createAiGovernancePolicyDraft",
    "contract": "ai",
    "purpose": "Draft a governance policy, or a new version of one",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-525",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-525"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 3 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-526",
  "name": "AI Policy Conflict, Exception & Override Management",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "8",
   "page": 17
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-policy-conflict-exception-override-management-adm-526",
   "component": "apps/ticvai-web/src/routes/platform/AiPolicyConflictExceptionOverrideManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-519"
   ],
   "exitTo": [
    "ADM-519"
   ],
   "transitions": [
    {
     "to": "ADM-519",
     "trigger": "Back to AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "capabilityKey"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Identify conflicting governance rules and manage legitimate temporary exceptions without bypassing governance silently.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 17"
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
       "impliedBy": "listAiGovernancePolicyVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "operation": "getEffectiveAiPolicy"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createAiPolicyException",
       "label": "Create AI policy exception",
       "notes": "The act the screen exists for.",
       "operation": "createAiPolicyException"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "revokeAiPolicyException",
       "label": "Revoke AI policy exception",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — which AI policy exception is affected and what goes with it, in the screen's own words; *are you sure* is not a confirmation.",
       "operation": "revokeAiPolicyException"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAiPolicyException"
      },
      {
       "kind": "dataTable",
       "label": "Policy conflicts",
       "bindsTo": "AiEffectivePolicy.conflicts",
       "operation": "getEffectiveAiPolicy",
       "notes": "**Each conflict and the more restrictive result it resolved to** (18 September minutes, M18-01; AIC-161). A plan step that fails the owning module's limit (a price above the configured maximum) is shown as governance-blocked and is never applied.",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The policy conflict exception list.",
   "error": "Could not load. Names which read failed and leaves the policy conflict exception untouched.",
   "emptyFirstRun": "No policy conflict exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the policy conflict exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEffectiveAiPolicy",
    "contract": "ai",
    "purpose": "The policy in force for a capability at a scope",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiGovernancePolicyVersions",
    "contract": "ai",
    "purpose": "Governance policies and their versions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "createAiPolicyException",
    "contract": "ai",
    "purpose": "Grant a temporary exception to a governance policy",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "revokeAiPolicyException",
    "contract": "ai",
    "purpose": "End an exception before it expires",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-526",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-526"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 17. 0 of 0 labels bound to a contract property; 0 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "exceptionId",
     "from": "navigation"
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRevokeAiPolicyException",
    "component": "confirmDialog",
    "trigger": "Revoke AI policy exception",
    "body": "**Names the exception and what the capability falls back to** once it is revoked: the stricter policy applies at once to every scope the exception covered.",
    "provenance": "29 September pass (group A)"
   }
  ],
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
  "id": "ADM-527",
  "name": "AI Policy Testing & Governance Simulation",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "9",
   "page": 18
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-policy-testing-governance-simulation-adm-527",
   "component": "apps/ticvai-web/src/routes/platform/AiPolicyTestingGovernanceSimulation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-519"
   ],
   "exitTo": [
    "ADM-519"
   ],
   "transitions": [
    {
     "to": "ADM-519",
     "trigger": "Back to AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "capabilityKey"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to test governance policies before activating them. This is extremely important because a policy mistake could either: Allow AI too much authority, or Block legitimate TICVAI operations. Simulation Scenario User Venue Administrator AI Capability AI Configuration Assistant Request Increase Adult Ticket Price Module Pricing Environment Production Risk High Policy Evaluation Step 1: User Permission ✓ Can modify pricing Step 2: AI Capability Permission ✓ Can prepare pricing change Step 3: Autonomy Level 2 — Prepare Step 4: Production Policy Approval required Step 5: Risk Policy Commercial Owner approval Final Decision ALLOW PREPARATION Execution BLOCKED UNTIL APPROVAL",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 18"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 18"
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
       "impliedBy": "simulateAiGovernancePolicy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAiGovernancePolicyVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateAiGovernancePolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The policy testing governance list.",
   "error": "Could not load. Names which read failed and leaves the policy testing governance untouched.",
   "emptyFirstRun": "No policy testing governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the policy testing governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateAiGovernancePolicy",
    "contract": "ai",
    "purpose": "Test a draft policy before it is published",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiGovernancePolicyVersions",
    "contract": "ai",
    "purpose": "Governance policies and their versions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-527",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-527"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 65 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "versionId",
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
  "id": "ADM-528",
  "name": "AI Governance Policy Publication & Effective Policy Map",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Governance_Reference.pdf",
   "board": "1",
   "number": "10",
   "page": 20
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-governance-policy-publication-effective-policy-map-adm-528",
   "component": "apps/ticvai-web/src/routes/platform/AiGovernancePolicyPublicationEffectivePolicyMap.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-519"
   ],
   "exitTo": [
    "ADM-519"
   ],
   "transitions": [
    {
     "to": "ADM-519",
     "trigger": "Back to AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "capabilityKey"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the final review, approval, versioning and publication layer for AI governance policies. No material governance policy should become active without a controlled lifecycle.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 20"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Governance_Reference.pdf, page 20"
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
       "impliedBy": "publishAiGovernancePolicy",
       "notes": "Declares `publishAiGovernancePolicy`. **The gate names what the publish will affect before it happens**: which tenants, venues or capabilities take the new version, and that the previous one stays available to roll back to.",
       "provenance": "check-screens publish rule, 29 September 2026"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "publishAiGovernancePolicy",
       "label": "Publish AI governance policy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAiGovernancePolicyVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "publishAiGovernancePolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance policy publication list.",
   "error": "Could not load. Names which read failed and leaves the governance policy publication untouched.",
   "emptyFirstRun": "No governance policy publication yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance policy publication are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEffectiveAiPolicy",
    "contract": "ai",
    "purpose": "The policy in force for a capability at a scope",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "publishAiGovernancePolicy",
    "contract": "ai",
    "purpose": "Publish a simulated policy version",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAiGovernancePolicyVersions",
    "contract": "ai",
    "purpose": "Governance policies and their versions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-528",
   "workshopBoard": "wireframes/WS14 AI Governance Board 1.dc.html#adm-528"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Governance_Reference.pdf page 20. 0 of 0 labels bound to a contract property; 0 of 266 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "versionId",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "configureAiCapability": {
  "method": "PUT",
  "path": "/governance/capabilities/{capabilityKey}",
  "contract": "ai",
  "summary": "Register a capability, or change its owner, risk class or autonomy",
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
  "requestBody": "AiCapabilityRegistration",
  "responds": "AiCapabilityRegistration"
 },
 "createAiGovernancePolicyDraft": {
  "method": "POST",
  "path": "/governance/policy-drafts",
  "contract": "ai",
  "summary": "Draft a governance policy, or a new version of one",
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
  "responds": "AiGovernancePolicyVersion"
 },
 "createAiPolicyException": {
  "method": "POST",
  "path": "/governance/policy-exceptions",
  "contract": "ai",
  "summary": "Grant a temporary exception to a governance policy",
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
  "requestBody": "AiPolicyException",
  "responds": "AiPolicyException"
 },
 "getEffectiveAiPolicy": {
  "method": "GET",
  "path": "/governance/effective-policy",
  "contract": "ai",
  "summary": "The policy in force for a capability at a scope",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "capabilityKey",
    "in": "query",
    "required": true
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "environment",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiEffectivePolicy"
 },
 "listAiCapabilities": {
  "method": "GET",
  "path": "/governance/capabilities",
  "contract": "ai",
  "summary": "The capability registry",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "family",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "riskClass",
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
 "listAiCapabilityMaturity": {
  "method": "GET",
  "path": "/capability-maturity",
  "contract": "ai",
  "summary": "Where each AI answer stands on the way from baseline to learned",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "stage",
    "in": "query",
    "required": null
   },
   {
    "name": "capabilityKey",
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
 "listAiGovernancePolicyVersions": {
  "method": "GET",
  "path": "/governance/policy-versions",
  "contract": "ai",
  "summary": "Governance policies and their versions",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "policyId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
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
 "listAiTools": {
  "method": "GET",
  "path": "/tools",
  "contract": "ai",
  "summary": "The tool registry",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "targetContract",
    "in": "query",
    "required": null
   },
   {
    "name": "effect",
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
 "publishAiGovernancePolicy": {
  "method": "POST",
  "path": "/governance/policy-versions/{versionId}/publish",
  "contract": "ai",
  "summary": "Publish a simulated policy version",
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
  "responds": "AiGovernancePolicyVersion"
 },
 "revokeAiPolicyException": {
  "method": "POST",
  "path": "/governance/policy-exceptions/{exceptionId}/revoke",
  "contract": "ai",
  "summary": "End an exception before it expires",
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
  "responds": "AiPolicyException"
 },
 "setAiTool": {
  "method": "PUT",
  "path": "/tools/{toolKey}",
  "contract": "ai",
  "summary": "Register or change a tool (platform)",
  "permission": "PLATFORM_AI_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AiTool",
  "responds": "AiTool"
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
 },
 "simulateAiGovernancePolicy": {
  "method": "POST",
  "path": "/governance/policy-versions/{versionId}/simulate",
  "contract": "ai",
  "summary": "Test a draft policy before it is published",
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
  "responds": "AiPolicySimulation"
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
 "AiCapabilityMaturity": {
  "type": "object",
  "x-ticvai-persistence": "ai.capability_maturity",
  "description": "**The stage of each question the venue's AI answers** (29 September, AI functions review). Written by the nightly re-estimate; a stage change is a new row, so the page can show when each answer moved.",
  "required": [
   "capabilityKey",
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
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ]
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producerRef": {
    "type": "string",
    "description": "The producer and version answering now."
   },
   "since": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
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
 "AiEffectivePolicy": {
  "type": "object",
  "x-ticvai-persistence": "none — resolved from published policy versions, exceptions and ai.policy",
  "description": "**The policy in force for a capability at a scope** (AIC-153, AIC-165; ADM-525, ADM-528): the intersection of the capability, governance policy and the tenant or venue AI policy, with where each part came from.",
  "required": [
   "capabilityKey",
   "autonomyLevel",
   "rules"
  ],
  "properties": {
   "capabilityKey": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "autonomyLevel": {
    "$ref": "#/components/schemas/AiAutonomyLevel"
   },
   "autonomyCeiling": {
    "$ref": "#/components/schemas/AiAutonomyLevel"
   },
   "rules": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "rule": {
       "$ref": "#/components/schemas/AiGovernanceRule"
      },
      "policyKey": {
       "type": "string"
      },
      "version": {
       "type": "integer"
      },
      "scopePath": {
       "type": "string"
      }
     }
    }
   },
   "exceptions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiPolicyException"
    }
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "description": {
       "type": "string"
      },
      "resolvedTo": {
       "$ref": "#/components/schemas/AiGovernanceOutcome"
      }
     }
    },
    "description": "Conflicting rules and the more restrictive result they resolved to (AIC-161)."
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time"
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
 "AiGovernancePolicyVersion": {
  "type": "object",
  "x-ticvai-persistence": "ai.governance_policy_version",
  "description": "One version of a governance policy. **Published versions are never edited**: a change is a new version, and the previous one becomes `superseded` in the same transaction (AIC-165).",
  "required": [
   "policyId",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "policyId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.governance_policy"
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "simulated",
     "published",
     "superseded"
    ]
   },
   "rules": {
    "$ref": "#/components/schemas/AiGovernanceRuleList"
   },
   "changeNote": {
    "type": "string",
    "nullable": true
   },
   "simulationSummary": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true,
    "description": "The last `simulateAiGovernancePolicy` result: decisions that would change, by outcome."
   },
   "draftedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "supersededAt": {
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
 "AiGovernanceRule": {
  "type": "object",
  "x-ticvai-persistence": "none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList",
  "description": "One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).",
  "required": [
   "effect"
  ],
  "properties": {
   "effect": {
    "$ref": "#/components/schemas/AiGovernanceOutcome"
   },
   "capabilityKeys": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Registered capabilities it applies to. Empty means every capability the policy names."
   },
   "actions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "read",
      "analyze",
      "recommend",
      "generate",
      "prepare",
      "create",
      "modify",
      "publish",
      "execute",
      "delete"
     ]
    },
    "description": "ADM-523: what AI may do, from reading to executing."
   },
   "dataCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Permitted purposes for those categories (AIC-156, AIR-182)."
   },
   "maxAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Above this value the effect escalates one step (for example to `approvalRequired`)."
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Roles the rule applies to; empty means every role."
   },
   "environments": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "development",
      "sandbox",
      "staging",
      "production"
     ]
    },
    "description": "ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."
   },
   "conditions": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."
   }
  }
 },
 "AiGovernanceRuleList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "The rules of one policy version, stored with the version as one `jsonb` column.",
  "items": {
   "$ref": "#/components/schemas/AiGovernanceRule"
  }
 },
 "AiMaturity": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded as jsonb on ai.suggestion and ai.forecast_version",
  "description": "**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.",
  "required": [
   "stage",
   "basedOn"
  ],
  "properties": {
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ],
    "description": "`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."
   },
   "basedOn": {
    "type": "string",
    "description": "The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "source"
     ],
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "venueSettings",
        "startingPattern",
        "calendar",
        "weather",
        "bookingsOnHand",
        "ownHistory",
        "importedHistory",
        "configuration",
        "trainedModel"
       ]
      },
      "detail": {
       "type": "string",
       "nullable": true,
       "description": "e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."
      },
      "observations": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "ownDataShare": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."
   },
   "limitedHistory": {
    "type": "boolean"
   },
   "nextStage": {
    "type": "object",
    "nullable": true,
    "description": "What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.",
    "properties": {
     "stage": {
      "type": "string",
      "enum": [
       "learning",
       "established",
       "learned"
      ]
     },
     "needs": {
      "type": "string"
     },
     "expectedBy": {
      "type": "string",
      "format": "date",
      "nullable": true
     }
    }
   }
  }
 },
 "AiPolicyException": {
  "type": "object",
  "x-ticvai-persistence": "ai.policy_exception",
  "description": "**A temporary, recorded exception to a governance policy** (AIC-162, ADM-526): an expiry, an approver and compensating controls. Governance is never bypassed silently.",
  "required": [
   "policyId",
   "reason",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "policyId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.governance_policy"
   },
   "capabilityKey": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "maxLength": 2000
   },
   "compensatingControls": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "startsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "Required. An exception with no end is a policy change, and goes through publication."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "expired",
     "revoked"
    ],
    "readOnly": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "revokedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "revokeReason": {
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
 "AiPolicySimulation": {
  "type": "object",
  "x-ticvai-persistence": "none — computed; summary kept on ai.governance_policy_version.simulationSummary",
  "description": "What a draft policy version would have decided over recorded decisions and the test cases (ADM-527).",
  "required": [
   "evaluated"
  ],
  "properties": {
   "evaluated": {
    "type": "integer"
   },
   "wouldChange": {
    "type": "integer"
   },
   "byOutcome": {
    "type": "object",
    "additionalProperties": true,
    "description": "Counts per outcome, current against draft."
   },
   "examples": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "decisionRecordId": {
       "type": "string",
       "format": "uuid"
      },
      "current": {
       "$ref": "#/components/schemas/AiGovernanceOutcome"
      },
      "draft": {
       "$ref": "#/components/schemas/AiGovernanceOutcome"
      },
      "capabilityKey": {
       "type": "string"
      }
     }
    }
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
 "AiTool": {
  "type": "object",
  "x-ticvai-persistence": "ai.tool",
  "description": "**The tool registry** (design 3.1 Registry, 3.8; AIC-088, AIC-089). The executor calls owning modules only for tools registered here: each names its target operation at a contract version, whether it reads, writes or destroys, its risk, the permission it needs, its compensation and timeout. Platform rows, replicated read-only into each tenant database with the tenant root as `scopePath`; written only by `setAiTool` (`PLATFORM_AI_MANAGE`).",
  "x-ticvai-registered-tools-note": "Registrations the release seeds through `setAiTool` for the resources and white-label assistants (29 September, build; 1.2.59, 2.6.50), so a conversational command or a configuration plan can change a resource schedule, a booking, an allocation or the storefront theme, fonts, header, navigation, homepage and pages. Each owner operation accepts `Prefer: validate-only` (added by its owner the same day). `white-label.publishTenantConfig` is deliberately not a tool: the assistant prepares, a person publishes.",
  "x-ticvai-registered-tools": [
   {
    "toolKey": "resources.setResourceSchedule",
    "targetContract": "resources",
    "targetOperation": "setResourceSchedule",
    "effect": "write",
    "riskClass": "medium",
    "permission": "RESOURCE_CONFIGURE",
    "reversible": true,
    "compensationOperation": "setResourceSchedule",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "resources.updateResourceBooking",
    "targetContract": "resources",
    "targetOperation": "updateResourceBooking",
    "effect": "write",
    "riskClass": "medium",
    "permission": "RESOURCE_BOOK",
    "reversible": true,
    "compensationOperation": "updateResourceBooking",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "resources.allocateResources",
    "targetContract": "resources",
    "targetOperation": "allocateResources",
    "effect": "write",
    "riskClass": "medium",
    "permission": "RESOURCE_BOOK",
    "reversible": true,
    "compensationOperation": "replaceResourceAllocation",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setTheme",
    "targetContract": "white-label",
    "targetOperation": "setTheme",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setFonts",
    "targetContract": "white-label",
    "targetOperation": "setFonts",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setHeader",
    "targetContract": "white-label",
    "targetOperation": "setHeader",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setNavigation",
    "targetContract": "white-label",
    "targetOperation": "setNavigation",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.setHomepageLayout",
    "targetContract": "white-label",
    "targetOperation": "setHomepageLayout",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "restoreConfigVersion",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "white-label.createContentPage",
    "targetContract": "white-label",
    "targetOperation": "createContentPage",
    "effect": "write",
    "riskClass": "low",
    "permission": "TENANT_CONFIGURE",
    "reversible": true,
    "compensationOperation": "deleteContentPage",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": true
   },
   {
    "toolKey": "venue-map.generateVisitPlan",
    "targetContract": "venue-map",
    "targetOperation": "generateVisitPlan",
    "effect": "write",
    "riskClass": "low",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": null,
    "timeoutMs": 3000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest"
   },
   {
    "toolKey": "venue-map.getVisitPlan",
    "targetContract": "venue-map",
    "targetOperation": "getVisitPlan",
    "effect": "read",
    "riskClass": "low",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": null,
    "timeoutMs": 2000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest"
   },
   {
    "toolKey": "venue-map.listVisitPlanAlternatives",
    "targetContract": "venue-map",
    "targetOperation": "listVisitPlanAlternatives",
    "effect": "read",
    "riskClass": "low",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": null,
    "timeoutMs": 2000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest"
   },
   {
    "toolKey": "venue-map.updateVisitPlan",
    "targetContract": "venue-map",
    "targetOperation": "updateVisitPlan",
    "effect": "write",
    "riskClass": "low",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": "updateVisitPlan",
    "timeoutMs": 3000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest"
   },
   {
    "toolKey": "venue-map.bookVisitPlan",
    "targetContract": "venue-map",
    "targetOperation": "bookVisitPlan",
    "effect": "write",
    "riskClass": "medium",
    "permission": null,
    "callerAudience": "guest",
    "reversible": true,
    "compensationOperation": "orders.removeCartLine",
    "timeoutMs": 5000,
    "idempotent": true,
    "validateOnly": false,
    "agent": "planner.guest",
    "requiresGuestConfirmation": true
   }
  ],
  "x-ticvai-registered-tools-planner-note": "**The planner agent's tools** (29 September, MOB-6; the assistant profile `planner.guest`, audience guest, `guestCapabilityScope` `visitPlanning`). The agent refines a rules plan by chat on GST-054 through these five `venue-map` operations, **always called as the guest whose plan it is** (permission null, the guest session's own plan), so every change is a plan version the guest can undo. `bookVisitPlan` needs the guest to press Book in the app; the agent may prepare it and never checks out. AI writes nothing outside `ai.*` (ADR-0020): the plan tables are written by the venue-map service these tools call. **Grounding** (30 September client meeting, MoM 4.7): the agent's candidates are only what these tools return for a day, i.e. the rides, dining and retail points (shops and kiosks) on the published map of that day's venue; it never proposes a point from another venue or from general knowledge, and says so when a preference is not met there (`VisitPlan.unmatchedPreferences`).",
  "required": [
   "toolKey",
   "targetContract",
   "targetOperation",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
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
   "effect": {
    "type": "string",
    "enum": [
     "read",
     "write",
     "destructive"
    ]
   },
   "riskClass": {
    "$ref": "#/components/schemas/AiRiskClass"
   },
   "permission": {
    "type": "string",
    "description": "The permission the requester must hold for the executor to call it on their behalf."
   },
   "reversible": {
    "type": "boolean",
    "description": "Non-reversible steps (a refund, a publish) need the stronger approval tier (AIC-099)."
   },
   "compensationOperation": {
    "type": "string",
    "nullable": true
   },
   "timeoutMs": {
    "type": "integer",
    "minimum": 1
   },
   "idempotent": {
    "type": "boolean",
    "default": true
   },
   "validateOnly": {
    "type": "boolean",
    "default": false,
    "description": "The owner accepts `Prefer: validate-only` on it (design 2.3)."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "disabled"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
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
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n",
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
