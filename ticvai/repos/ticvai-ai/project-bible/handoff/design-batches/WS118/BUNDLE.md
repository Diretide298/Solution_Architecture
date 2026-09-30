# WS118 — AI Configuration Assistant board 3

**10 screens · 21 operations · 26 schemas · 5 permissions**

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
  `AI_APPROVE, AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-489` | AI Configuration Readiness Center | commandCentre | 4 | 1 | — |
| `ADM-490` | Configuration Validation Results | listDetail | 2 | 0 | — |
| `ADM-491` | AI Recommendations & Best-Practice Review | listDetail | 2 | 0 | — |
| `ADM-492` | Configuration Approval Workflow | listDetail | 4 | 0 | — |
| `ADM-493` | AI Configuration Execution Center | listDetail | 3 | 0 | — |
| `ADM-494` | Execution Progress & Dependency Monitor | listDetail | 4 | 0 | — |
| `ADM-495` | Configuration Results & Object Mapping | listDetail | 2 | 0 | — |
| `ADM-496` | Configuration Change & Modification Assistant | listDetail | 3 | 0 | — |
| `ADM-497` | Configuration History, Versions & Rollback | listDetail | 3 | 0 | — |
| `ADM-498` | AI Configuration Audit & Governance | commandCentre | 2 | 0 | — |

## Thin screens in this batch

**ADM-490, ADM-491, ADM-492, ADM-494, ADM-495, ADM-496 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-489",
  "name": "AI Configuration Readiness Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "1",
   "page": 44
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-configuration-readiness-center-adm-489",
   "component": "apps/ticvai-web/src/routes/platform/AiConfigurationReadinessCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-490",
    "ADM-491",
    "ADM-492",
    "ADM-493",
    "ADM-494",
    "ADM-495",
    "ADM-496",
    "ADM-497",
    "ADM-498"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-490",
     "trigger": "Configuration Validation Results",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-491",
     "trigger": "AI Recommendations & Best-Practice Review",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-492",
     "trigger": "Configuration Approval Workflow",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-493",
     "trigger": "AI Configuration Execution Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-494",
     "trigger": "Execution Progress & Dependency Monitor",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "planId",
      "stepNumber"
     ]
    },
    {
     "to": "ADM-495",
     "trigger": "Configuration Results & Object Mapping",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-496",
     "trigger": "Configuration Change & Modification Assistant",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-497",
     "trigger": "Configuration History, Versions & Rollback",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-498",
     "trigger": "AI Configuration Audit & Governance",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a final readiness assessment before the proposed Configuration Plan can enter approval or execution. This is the first governance gate.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Configuration Objects",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 44 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Ready",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 44 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Warnings",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 44 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Blocking Issues",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 44 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Approval Requirements",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 44 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "AI Recommendations",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 44 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Modules Affected",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 44 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Production Impact",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 44 §Header KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Venue AI profile",
       "bindsTo": "AiVenueSettings",
       "columns": [
        "AiVenueSettings.venueType",
        "AiVenueSettings.capacity",
        "AiVenueSettings.openingHours",
        "AiVenueSettings.typicalWeekdayAttendance",
        "AiVenueSettings.typicalWeekendAttendance",
        "AiVenueSettings.peakMonths",
        "AiVenueSettings.averageSpend",
        "AiVenueSettings.fnbAttachRate"
       ],
       "operation": "getAiVenueSettings",
       "notes": "**What every AI answer stands on before the venue has history** (29 September, AI functions review). Collected at onboarding, here or by the configuration assistant in conversation.",
       "provenance": "29 September pass (group A)"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save venue AI profile",
       "operation": "setAiVenueSettings",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The readiness list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the readiness untouched.",
   "emptyFirstRun": "No readiness yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the readiness are still there. Names the active filter and offers to clear it.",
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
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getAiVenueSettings",
    "contract": "ai",
    "purpose": "The venue AI profile the baselines use",
    "trigger": "onLoad",
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "setAiVenueSettings",
    "contract": "ai",
    "purpose": "Set it at onboarding",
    "trigger": "onAction",
    "invalidates": [
     "getAiVenueSettings"
    ],
    "provenance": "29 September pass (group A)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-489",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-489"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 44. 0 of 0 labels bound to a contract property; 8 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "planId",
     "from": "navigation"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ]
  },
  "overlays": [
   {
    "id": "formSetAiVenueSettings",
    "component": "modal",
    "trigger": "Save venue AI profile",
    "body": "**Collects what `setAiVenueSettings` sends before it is called.** Required: `venueId`, `venueType`. Every other figure is optional and defaults to the starting pattern for the venue type, so a venue that knows only its type still gets answers.",
    "bindsTo": "AiVenueSettings",
    "confirm": {
     "label": "Save venue AI profile",
     "operation": "setAiVenueSettings"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueType",
      "isOutdoor",
      "capacity",
      "openingHours",
      "typicalWeekdayAttendance",
      "typicalWeekendAttendance",
      "peakMonths",
      "averageSpend",
      "fnbAttachRate",
      "staffProductivity"
     ]
    },
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
  "id": "ADM-490",
  "name": "Configuration Validation Results",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "2",
   "page": 45
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/configuration-validation-results-adm-490",
   "component": "apps/ticvai-web/src/routes/platform/ConfigurationValidationResults.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-489"
   ],
   "exitTo": [
    "ADM-489"
   ],
   "transitions": [
    {
     "to": "ADM-489",
     "trigger": "Back to AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide detailed evidence that the proposed configuration has passed all required TICVAI validation layers. Screen 1 provides the summary; Screen 2 provides the technical and business evidence.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 45"
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "simulateActionPlan",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateActionPlan"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The validation results list.",
   "error": "Could not load. Names which read failed and leaves the validation results untouched.",
   "emptyFirstRun": "No validation results yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the validation results are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "simulateActionPlan",
    "contract": "ai",
    "purpose": "Validate and simulate a plan without changing anything",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-490",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-490"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 45. 0 of 0 labels bound to a contract property; 0 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
  "id": "ADM-491",
  "name": "AI Recommendations & Best-Practice Review",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "3",
   "page": 47
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-recommendations-best-practice-review-adm-491",
   "component": "apps/ticvai-web/src/routes/platform/AiRecommendationsBestPracticeReview.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-489"
   ],
   "exitTo": [
    "ADM-489"
   ],
   "transitions": [
    {
     "to": "ADM-489",
     "trigger": "Back to AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Separate mandatory configuration from AI recommendations so the administrator understands what This is important for trust and governance.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 47 §Track"
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
       "label": "Every recommendations best-practice review",
       "columns": [
        "Recommendation",
        "Family Package",
        "Decision",
        "Rejected",
        "By",
        "Administrator",
        "Reason"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 47 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected recommendations best-practice review",
       "bindsTo": null,
       "columns": [
        "Recommendation",
        "Family Package",
        "Decision",
        "Rejected",
        "By",
        "Administrator",
        "Reason"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Where available”.",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 47 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendations best-practice review list.",
   "error": "Could not load. Names which read failed and leaves the recommendations best-practice review untouched.",
   "emptyFirstRun": "No recommendations best-practice review yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendations best-practice review are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideBlueprintRecommendation",
    "contract": "ai",
    "purpose": "Accept, modify, reject or defer a blueprint decision",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Recommendation",
    "Family Package",
    "Decision",
    "Rejected",
    "By",
    "Administrator"
   ],
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "sessionId",
     "from": "session"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-491",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-491"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 47. 0 of 7 labels bound to a contract property; 16 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-492",
  "name": "Configuration Approval Workflow",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "4",
   "page": 48
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/configuration-approval-workflow-adm-492",
   "component": "apps/ticvai-web/src/routes/platform/ConfigurationApprovalWorkflow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-489"
   ],
   "exitTo": [
    "ADM-489"
   ],
   "transitions": [
    {
     "to": "ADM-489",
     "trigger": "Back to AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Route the proposed AI configuration through TICVAI's existing RBAC/PBAC and approval governance before execution. The AI Assistant should reuse the central TICVAI approval engine, not create an independent approval system.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 48"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 48"
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
       "impliedBy": "approveWorkflow",
       "label": "Approve workflow",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "approveWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval workflow list.",
   "error": "Could not load. Names which read failed and leaves the approval workflow untouched.",
   "emptyFirstRun": "No approval workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveWorkflow",
    "contract": "catalogue",
    "purpose": "Approval Workflow Designer",
    "trigger": "onAction"
   },
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listProposedActions",
    "contract": "ai",
    "purpose": "What the assistant has proposed and nobody has decided",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideProposedAction",
    "contract": "ai",
    "purpose": "Approve or reject a proposal (tier 1 here; tier 2 routed to Approvals)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-492",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-492"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 48. 0 of 0 labels bound to a contract property; 0 of 61 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "actionId",
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
  "id": "ADM-493",
  "name": "AI Configuration Execution Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "5",
   "page": 50
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-configuration-execution-center-adm-493",
   "component": "apps/ticvai-web/src/routes/platform/AiConfigurationExecutionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-489"
   ],
   "exitTo": [
    "ADM-489"
   ],
   "transitions": [
    {
     "to": "ADM-489",
     "trigger": "Back to AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Execute the approved Configuration Plan against the appropriate TICVAI modules in a controlled and traceable sequence. This is where proposed configuration becomes real TICVAI configuration.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 50"
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "pauseActionPlan",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelActionPlan",
       "label": "Cancel action plan",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — which action plan is affected and what goes with it, in the screen's own words; *are you sure* is not a confirmation."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "pauseActionPlan"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The execution list.",
   "error": "Could not load. Names which read failed and leaves the execution untouched.",
   "emptyFirstRun": "No execution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the execution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "pauseActionPlan",
    "contract": "ai",
    "purpose": "Pause an executing plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "cancelActionPlan",
    "contract": "ai",
    "purpose": "Cancel a plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-493",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-493"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
  "id": "ADM-494",
  "name": "Execution Progress & Dependency Monitor",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "6",
   "page": 51
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/execution-progress-dependency-monitor-adm-494",
   "component": "apps/ticvai-web/src/routes/platform/ExecutionProgressDependencyMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-489"
   ],
   "exitTo": [
    "ADM-489"
   ],
   "transitions": [
    {
     "to": "ADM-489",
     "trigger": "Back to AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide a detailed real-time view of execution dependencies, failures, retries, and downstream configuration status.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 51 §Show"
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
       "label": "Every execution progress dependency",
       "columns": [
        "Venue ✓",
        "↓",
        "Operating Calendar ✓",
        "Products ✓",
        "Timeslots ✓",
        "Capacity ●",
        "Pricing ○",
        "Channels ○",
        "Media ○",
        "Access ○",
        "Status",
        "Waiting",
        "Executing",
        "Success",
        "Warning",
        "Failed",
        "Skipped",
        "Rolled Back",
        "Failure Example",
        "🔴 Pricing Profile Creation Failed",
        "Weekend Adult Pricing"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 51 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected execution progress dependency",
       "bindsTo": null,
       "columns": [
        "Venue ✓",
        "↓",
        "Operating Calendar ✓",
        "Products ✓",
        "Timeslots ✓",
        "Capacity ●",
        "Pricing ○",
        "Channels ○",
        "Media ○",
        "Access ○",
        "Status",
        "Waiting",
        "Executing",
        "Success",
        "Warning",
        "Failed",
        "Skipped",
        "Rolled Back",
        "Failure Example",
        "🔴 Pricing Profile Creation Failed",
        "Weekend Adult Pricing"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Blocked”, “Retry History”, “Resolution Applied”.",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 51 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The execution progress dependency list.",
   "error": "Could not load. Names which read failed and leaves the execution progress dependency untouched.",
   "emptyFirstRun": "No execution progress dependency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the execution progress dependency are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "pauseActionPlan",
    "contract": "ai",
    "purpose": "Pause an executing plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "resumeActionPlan",
    "contract": "ai",
    "purpose": "Resume a paused plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "retryActionStep",
    "contract": "ai",
    "purpose": "Retry a failed step",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Venue ✓",
    "↓",
    "Operating Calendar ✓",
    "Products ✓",
    "Timeslots ✓",
    "Capacity ●"
   ],
   "params": [
    {
     "name": "planId",
     "from": "navigation"
    },
    {
     "name": "stepNumber",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-494",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-494"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 51. 0 of 21 labels bound to a contract property; 21 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-495",
  "name": "Configuration Results & Object Mapping",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "7",
   "page": 53
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/configuration-results-object-mapping-adm-495",
   "component": "apps/ticvai-web/src/routes/platform/ConfigurationResultsObjectMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-489"
   ],
   "exitTo": [
    "ADM-489"
   ],
   "transitions": [
    {
     "to": "ADM-489",
     "trigger": "Back to AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Show exactly what TICVAI objects were created or changed after successful execution.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 53 §Show"
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
       "label": "Every results object mapping",
       "columns": [
        "VEN-1028",
        "↓",
        "TKT-4012",
        "SCH-0291",
        "CAP-0218",
        "PRC-3002",
        "MED-0082",
        "ACC-0142"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 53 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected results object mapping",
       "bindsTo": null,
       "columns": [
        "VEN-1028",
        "↓",
        "TKT-4012",
        "SCH-0291",
        "CAP-0218",
        "PRC-3002",
        "MED-0082",
        "ACC-0142"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Object Mapping”, “Created does not necessarily mean”, “Pending”.",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 53 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The results object mapping list.",
   "error": "Could not load. Names which read failed and leaves the results object mapping untouched.",
   "emptyFirstRun": "No results object mapping yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the results object mapping are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "rollbackActionPlan",
    "contract": "ai",
    "purpose": "Plan a rollback",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "VEN-1028",
    "↓",
    "TKT-4012",
    "SCH-0291",
    "CAP-0218",
    "PRC-3002"
   ],
   "params": [
    {
     "name": "planId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-495",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-495"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 53. 0 of 8 labels bound to a contract property; 12 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-496",
  "name": "Configuration Change & Modification Assistant",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "8",
   "page": 54
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/configuration-change-modification-assistant-adm-496",
   "component": "apps/ticvai-web/src/routes/platform/ConfigurationChangeModificationAssistant.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-489"
   ],
   "exitTo": [
    "ADM-489"
   ],
   "transitions": [
    {
     "to": "ADM-489",
     "trigger": "Back to AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to return later and modify existing TICVAI configuration through natural-language AI. This is what transforms the feature from an onboarding wizard into a permanent AI configuration capability.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Prepare Change | Ask More | Cancel. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 54 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 54"
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
       "label": "Prepare Change | Ask More | Cancel",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 54 §Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "startConfigurationSession"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The change modification assistant list.",
   "error": "Could not load. Names which read failed and leaves the change modification assistant untouched.",
   "emptyFirstRun": "No change modification assistant yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the change modification assistant are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "startConfigurationSession",
    "contract": "ai",
    "purpose": "Start the configuration assistant",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "answerConfigurationQuestion",
    "contract": "ai",
    "purpose": "Answer the current question",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "buildConfigurationPlan",
    "contract": "ai",
    "purpose": "Compile the blueprint into a plan",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-496",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-496"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 54. 0 of 0 labels bound to a contract property; 1 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
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
  "id": "ADM-497",
  "name": "Configuration History, Versions & Rollback",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "9",
   "page": 55
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/configuration-history-versions-rollback-adm-497",
   "component": "apps/ticvai-web/src/routes/platform/ConfigurationHistoryVersionsRollback.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-489"
   ],
   "exitTo": [
    "ADM-489"
   ],
   "transitions": [
    {
     "to": "ADM-489",
     "trigger": "Back to AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain complete version history for AI-created and AI-modified configuration and provide governed rollback capability where technically possible.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 55"
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "rollbackActionPlan",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listConfigurationSessions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "rollbackActionPlan"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The history versions rollback list.",
   "error": "Could not load. Names which read failed and leaves the history versions rollback untouched.",
   "emptyFirstRun": "No history versions rollback yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the history versions rollback are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "rollbackActionPlan",
    "contract": "ai",
    "purpose": "Plan a rollback",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listConfigurationSessions",
    "contract": "ai",
    "purpose": "Configuration-assistant sessions",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-497",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-497"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 55. 0 of 0 labels bound to a contract property; 0 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
  "id": "ADM-498",
  "name": "AI Configuration Audit & Governance",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "3",
   "number": "10",
   "page": 57
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-configuration-audit-governance-adm-498",
   "component": "apps/ticvai-web/src/routes/platform/AiConfigurationAuditGovernance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-489"
   ],
   "exitTo": [
    "ADM-489"
   ],
   "transitions": [
    {
     "to": "ADM-489",
     "trigger": "Back to AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Header KPIs; Show) and a per-row directory (§For each configuration value show) — counts over a population, then the population",
  "purpose": "Provide an immutable governance record showing how AI participated in every configuration decision and execution. This is essential for an enterprise AI system.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §For each configuration value show"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search audit governance",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "User",
        "Date",
        "Session",
        "Configuration Plan",
        "Object",
        "Module",
        "AI Action",
        "Approval",
        "Execution Status",
        "Audit Record",
        "Timestamp",
        "12 Sep 2026 — 14:32",
        "Platform Administrator",
        "Action",
        "Approved AI Configuration Plan",
        "Plan",
        "CFG-PLAN-000128"
       ],
       "notes": "The pack filters this screen by tenant, venue, user, date, session, configuration plan and 13 more — which are present is a decision the pack already made.",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "AI Configuration Sessions",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "AI Recommendations",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Accepted",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Rejected",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Executed Changes",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Rollbacks",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Approval Overrides",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Failed Executions",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "User Request",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "↓",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "AI Interpretation",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Blueprint Decision",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Configuration Object",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Validation",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Approval",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Execution",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Audit Requirements",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Original User Intent",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "AI Recommendation",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "User Decision",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Configuration Plan",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Before / After",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Validation Results",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Failure / Retry",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Rollback",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Timestamp",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Actor",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Correlation / Trace ID",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §Show"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every audit governance",
       "columns": [
        "Source",
        "👤 User Provided",
        "🤖 AI Recommended",
        "⚙ System Derived",
        "📋 Existing Configuration"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §For each configuration value show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected audit governance",
       "bindsTo": null,
       "columns": [
        "Source",
        "👤 User Provided",
        "🤖 AI Recommended",
        "⚙ System Derived",
        "📋 Existing Configuration"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Objects”, “Timeslots 24 System Derived Operations”, “Critical Execution Architecture”, “The architecture should be”, “Owning TICVAI Modules”, “Execution Dependency Engine”.",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 57 §For each configuration value show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audit governance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the audit governance untouched.",
   "emptyFirstRun": "No audit governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the audit governance are still there. Names the active filter and offers to clear it.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-498",
   "workshopBoard": "wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-498"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 57. 0 of 24 labels bound to a contract property; 61 of 192 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "answerConfigurationQuestion": {
  "method": "POST",
  "path": "/configuration-sessions/{sessionId}/answers",
  "contract": "ai",
  "summary": "Answer the current question",
  "permission": "AI_USE",
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
  "responds": "AiConfigurationTurn"
 },
 "approveWorkflow": {
  "method": "PUT",
  "path": "/workflow",
  "contract": "catalogue",
  "summary": "Approval Workflow Designer",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ApprovalWorkflowDesignerInput",
  "responds": "ApprovalWorkflowDesignerView"
 },
 "buildConfigurationPlan": {
  "method": "POST",
  "path": "/configuration-sessions/{sessionId}/plan",
  "contract": "ai",
  "summary": "Compile the blueprint into a plan",
  "permission": "AI_USE",
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
  "responds": "AiActionPlanDetail"
 },
 "cancelActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/cancel",
  "contract": "ai",
  "summary": "Cancel a plan",
  "permission": "AI_USE",
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
  "responds": "AiActionPlan"
 },
 "decideBlueprintRecommendation": {
  "method": "POST",
  "path": "/configuration-sessions/{sessionId}/decisions/{decisionKey}",
  "contract": "ai",
  "summary": "Accept, modify, reject or defer a blueprint decision",
  "permission": "AI_USE",
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
  "responds": "AiBlueprintDecision"
 },
 "decideProposedAction": {
  "method": "POST",
  "path": "/proposed-actions/{actionId}/decide",
  "contract": "ai",
  "summary": "Approve or reject a proposal",
  "permission": "AI_USE",
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
  "responds": "ProposedAction"
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
 "getAiVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/ai-settings",
  "contract": "ai",
  "summary": "The venue AI profile the baselines stand on",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiVenueSettings"
 },
 "getConfigurationBlueprint": {
  "method": "GET",
  "path": "/configuration-sessions/{sessionId}/blueprint",
  "contract": "ai",
  "summary": "The blueprint so far",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "module",
    "in": "query",
    "required": null
   },
   {
    "name": "decisionClass",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiBlueprintView"
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
 "listConfigurationSessions": {
  "method": "GET",
  "path": "/configuration-sessions",
  "contract": "ai",
  "summary": "Configuration-assistant sessions",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "intent",
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
 "listProposedActions": {
  "method": "GET",
  "path": "/proposed-actions",
  "contract": "ai",
  "summary": "What the assistant has proposed and nobody has decided",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProposedAction"
 },
 "pauseActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/pause",
  "contract": "ai",
  "summary": "Pause an executing plan",
  "permission": "AI_APPROVE",
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
  "responds": "AiActionPlan"
 },
 "resumeActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/resume",
  "contract": "ai",
  "summary": "Resume a paused plan",
  "permission": "AI_APPROVE",
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
  "responds": "AiActionPlan"
 },
 "retryActionStep": {
  "method": "POST",
  "path": "/action-plans/{planId}/steps/{stepNumber}/retry",
  "contract": "ai",
  "summary": "Retry a failed step",
  "permission": "AI_APPROVE",
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
  "responds": "AiActionStep"
 },
 "rollbackActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/rollback",
  "contract": "ai",
  "summary": "Plan a rollback",
  "permission": "AI_APPROVE",
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
 },
 "setAiVenueSettings": {
  "method": "PUT",
  "path": "/venues/{venueId}/ai-settings",
  "contract": "ai",
  "summary": "Set the venue AI profile",
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
  "requestBody": "AiVenueSettings",
  "responds": "AiVenueSettings"
 },
 "simulateActionPlan": {
  "method": "POST",
  "path": "/action-plans/{planId}/simulate",
  "contract": "ai",
  "summary": "Validate and simulate a plan without changing anything",
  "permission": "AI_USE",
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
  "responds": "AiActionPlanDetail"
 },
 "startConfigurationSession": {
  "method": "POST",
  "path": "/configuration-sessions",
  "contract": "ai",
  "summary": "Start the configuration assistant",
  "permission": "AI_USE",
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
  "responds": "AiConfigurationSession"
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
 "AiAutonomyLevel": {
  "type": "integer",
  "minimum": 0,
  "maximum": 4,
  "description": "**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."
 },
 "AiBlueprintDecision": {
  "type": "object",
  "x-ticvai-persistence": "ai.blueprint_decision",
  "description": "One decision in a blueprint and what the administrator did with it. **Scoped through its blueprint** (`platform.apply_parent_rls`).",
  "required": [
   "blueprintId",
   "decisionKey",
   "decisionClass",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "blueprintId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.blueprint"
   },
   "decisionKey": {
    "type": "string"
   },
   "module": {
    "type": "string"
   },
   "decisionClass": {
    "type": "string",
    "enum": [
     "required",
     "recommended",
     "optional"
    ]
   },
   "question": {
    "type": "string",
    "nullable": true
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "provenance": {
    "$ref": "#/components/schemas/AiProvenance"
   },
   "sourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.config_source",
    "description": "The attached document the value was extracted from (29 September, build; `attachConfigurationSource`)."
   },
   "sourceCitation": {
    "type": "string",
    "nullable": true,
    "maxLength": 200,
    "description": "Where in it, e.g. `page 4`, `sheet Prices!B7`, `logo region`."
   },
   "recommendation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "What the assistant recommends and why (ADM-491): mandatory configuration and best practice kept apart."
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "accepted",
     "modified",
     "rejected",
     "deferred"
    ]
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
    "nullable": true
   }
  }
 },
 "AiBlueprintView": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.blueprint with its ai.blueprint_decision rows",
  "description": "A blueprint with its decisions.",
  "required": [
   "blueprint",
   "decisions"
  ],
  "properties": {
   "blueprint": {
    "$ref": "#/components/schemas/AiConfigurationBlueprint"
   },
   "decisions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiBlueprintDecision"
    }
   }
  }
 },
 "AiConfigurationBlueprint": {
  "type": "object",
  "x-ticvai-persistence": "ai.blueprint",
  "description": "**The blueprint** (design 2.2 D step 2, ADM-478): decisions, severity-graded issues and a dependency map. **Never `ready` while a required decision is deferred** (AIC-115).",
  "required": [
   "sessionId",
   "version",
   "readiness"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "sessionId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.config_session"
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "readiness": {
    "type": "string",
    "enum": [
     "notReady",
     "readyWithWarnings",
     "ready"
    ],
    "readOnly": true
   },
   "requiredOpen": {
    "type": "integer",
    "minimum": 0,
    "readOnly": true,
    "description": "Required decisions not yet accepted or modified."
   },
   "issues": {
    "$ref": "#/components/schemas/AiBlueprintIssueList"
   },
   "dependencyMap": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "Configuration objects and the order they depend on each other, by module."
   },
   "summary": {
    "type": "string",
    "nullable": true
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
 "AiConfigurationQuestion": {
  "type": "object",
  "x-ticvai-persistence": "none — chosen per turn from the configuration knowledge model",
  "description": "**The next question, chosen by the configuration knowledge model, not by the language model** (design 2.2 D, AIC-111). The model only extracts a structured answer against `answerSchema`.",
  "required": [
   "questionKey",
   "text",
   "decisionClass"
  ],
  "properties": {
   "questionKey": {
    "type": "string"
   },
   "text": {
    "type": "string"
   },
   "module": {
    "type": "string",
    "nullable": true
   },
   "decisionClass": {
    "type": "string",
    "enum": [
     "required",
     "recommended",
     "optional"
    ]
   },
   "answerType": {
    "type": "string",
    "enum": [
     "freeText",
     "singleChoice",
     "multiChoice",
     "number",
     "date",
     "confirm"
    ]
   },
   "options": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "why": {
    "type": "string",
    "nullable": true,
    "description": "Why it is asked: which configuration branch it opens or closes."
   },
   "answerSchema": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "JSON Schema the extracted answer must satisfy."
   }
  }
 },
 "AiConfigurationSession": {
  "type": "object",
  "x-ticvai-persistence": "ai.config_session",
  "description": "**A configuration-assistant session** (design 2.2 D steps 1-2, C7; ADM-469..478). Discovery runs from the configuration knowledge model; every value carries provenance.",
  "required": [
   "intent",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "intent": {
    "type": "string",
    "enum": [
     "create",
     "modify",
     "extend",
     "clone"
    ]
   },
   "venueType": {
    "type": "string",
    "nullable": true,
    "description": "Museum, theme park, water park, zoo, aquarium, theatre, stadium, festival, conference..."
   },
   "sourceScopePath": {
    "type": "string",
    "nullable": true,
    "description": "The setup being cloned or extended."
   },
   "status": {
    "type": "string",
    "enum": [
     "discovering",
     "blueprintReady",
     "planned",
     "executing",
     "completed",
     "abandoned"
    ],
    "readOnly": true
   },
   "progressPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "readOnly": true
   },
   "nextQuestion": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiConfigurationQuestion"
     }
    ],
    "nullable": true,
    "readOnly": true
   },
   "conversationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.conversation"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan"
   },
   "locale": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "lastActivityAt": {
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
 "AiConfigurationTurn": {
  "type": "object",
  "x-ticvai-persistence": "none — the answer is written to ai.blueprint_decision and the session",
  "description": "The result of one answer: what was extracted with its provenance, the next question and progress.",
  "required": [
   "session"
  ],
  "properties": {
   "session": {
    "$ref": "#/components/schemas/AiConfigurationSession"
   },
   "extracted": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "decisionKey": {
       "type": "string"
      },
      "value": {
       "type": "object",
       "additionalProperties": true,
       "nullable": true
      },
      "provenance": {
       "$ref": "#/components/schemas/AiProvenance"
      }
     }
    }
   },
   "nextQuestion": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiConfigurationQuestion"
     }
    ],
    "nullable": true
   },
   "clarificationsNeeded": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
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
 "AiProvenance": {
  "type": "string",
  "enum": [
   "confirmed",
   "aiRecommended",
   "inferred",
   "unknown"
  ],
  "description": "**Where a configuration value came from** (design 2.2 D, AIC-111): said by the administrator, recommended by the assistant, inferred from other answers, or not known yet. Shown beside every value; no confidence number is shown for configuration (design 5.6)."
 },
 "AiVenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "ai.venue_settings",
  "description": "**The venue AI profile** (29 September, AI functions review): the figures a venue gives at onboarding so every data-driven answer is useful before it has history. One row per venue; configuration, not history. Defaults come from the starting pattern for `venueType`, which TICVAI writes from published sources and made-up example curves, **never from another tenant's data** (AI-D01, AIP-149).",
  "required": [
   "venueId",
   "venueType"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "venueType": {
    "type": "string",
    "enum": [
     "waterPark",
     "themePark",
     "familyEntertainmentCentre",
     "museum",
     "arena",
     "zooAquarium",
     "other"
    ]
   },
   "isOutdoor": {
    "type": "boolean",
    "default": true,
    "description": "Outdoor venues take the summer-heat and weather effects."
   },
   "capacity": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "openingHours": {
    "type": "array",
    "description": "The usual week. Exceptions come from the venue calendar.",
    "items": {
     "type": "object",
     "properties": {
      "dayOfWeek": {
       "type": "integer",
       "minimum": 1,
       "maximum": 7
      },
      "opensAt": {
       "type": "string"
      },
      "closesAt": {
       "type": "string"
      }
     }
    }
   },
   "typicalWeekdayAttendance": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "typicalWeekendAttendance": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "peakMonths": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 1,
     "maximum": 12
    }
   },
   "averageSpend": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "fnbAttachRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "staffProductivity": {
    "type": "object",
    "additionalProperties": {
     "type": "number"
    },
    "description": "Per role, units per staff hour, e.g. `{\"cashier\": 40, \"gate\": 300}`. Defaults from the pattern."
   },
   "startingPatternKey": {
    "type": "string",
    "readOnly": true,
    "description": "The pattern and version in use, e.g. `waterPark@3`."
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
 "ApprovalWorkflowDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "workflowName": {
    "type": "string",
    "description": "Workflow name"
   },
   "applicableProductTypes": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ProductKind"
    },
    "description": "Applicable product types; empty = all"
   },
   "venue": {
    "type": "string",
    "description": "Venue id; empty = all venues",
    "nullable": true
   },
   "department": {
    "type": "string",
    "description": "Department",
    "nullable": true
   },
   "changeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "newProduct",
      "description",
      "price",
      "validity",
      "capacity",
      "entitlement",
      "eligibility",
      "tax",
      "channel",
      "media",
      "policy",
      "relationship",
      "retirement"
     ]
    },
    "description": "Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"
   },
   "approvalStages": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "order": {
       "type": "integer",
       "description": "Stage order; stages sharing an order run in parallel, otherwise sequential"
      },
      "name": {
       "type": "string"
      },
      "approverRole": {
       "type": "string",
       "nullable": true
      },
      "specificApproverId": {
       "type": "string",
       "nullable": true
      },
      "approvalGroupId": {
       "type": "string",
       "nullable": true
      },
      "mandatory": {
       "type": "boolean"
      },
      "slaHours": {
       "type": "integer",
       "description": "SLA in hours"
      },
      "escalateToRole": {
       "type": "string",
       "nullable": true,
       "description": "Escalation when the SLA is missed"
      },
      "delegationAllowed": {
       "type": "boolean"
      },
      "reminderEveryHours": {
       "type": "integer",
       "nullable": true,
       "description": "Reminder frequency"
      }
     }
    },
    "description": "Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"
   },
   "rejectionBehavior": {
    "type": "string",
    "enum": [
     "returnToDraft",
     "returnToPreviousStage",
     "closeRequest"
    ],
    "description": "What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"
   },
   "resubmissionBehavior": {
    "type": "string",
    "enum": [
     "restartFromFirstStage",
     "resumeAtRejectingStage"
    ],
    "description": "Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"
   },
   "workflowId": {
    "type": "string",
    "description": "Existing workflow to change; empty to create",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "ApprovalWorkflowDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowName": {
    "type": "string",
    "description": "Workflow name"
   },
   "applicableProductTypes": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ProductKind"
    },
    "description": "Applicable product types; empty = all"
   },
   "venue": {
    "type": "string",
    "description": "Venue id; empty = all venues",
    "nullable": true
   },
   "department": {
    "type": "string",
    "description": "Department",
    "nullable": true
   },
   "changeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "newProduct",
      "description",
      "price",
      "validity",
      "capacity",
      "entitlement",
      "eligibility",
      "tax",
      "channel",
      "media",
      "policy",
      "relationship",
      "retirement"
     ]
    },
    "description": "Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"
   },
   "approvalStages": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "order": {
       "type": "integer",
       "description": "Stage order; stages sharing an order run in parallel, otherwise sequential"
      },
      "name": {
       "type": "string"
      },
      "approverRole": {
       "type": "string",
       "nullable": true
      },
      "specificApproverId": {
       "type": "string",
       "nullable": true
      },
      "approvalGroupId": {
       "type": "string",
       "nullable": true
      },
      "mandatory": {
       "type": "boolean"
      },
      "slaHours": {
       "type": "integer",
       "description": "SLA in hours"
      },
      "escalateToRole": {
       "type": "string",
       "nullable": true,
       "description": "Escalation when the SLA is missed"
      },
      "delegationAllowed": {
       "type": "boolean"
      },
      "reminderEveryHours": {
       "type": "integer",
       "nullable": true,
       "description": "Reminder frequency"
      }
     }
    },
    "description": "Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"
   },
   "rejectionBehavior": {
    "type": "string",
    "enum": [
     "returnToDraft",
     "returnToPreviousStage",
     "closeRequest"
    ],
    "description": "What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"
   },
   "resubmissionBehavior": {
    "type": "string",
    "enum": [
     "restartFromFirstStage",
     "resumeAtRejectingStage"
    ],
    "description": "Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow id",
    "format": "uuid"
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
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "ProposedAction": {
  "type": "object",
  "x-ticvai-persistence": "ai.proposed_action",
  "required": [
   "id",
   "kind",
   "targetContract",
   "targetOperation",
   "payload",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "interactionId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "pricing",
     "promotion",
     "operational",
     "financial",
     "configuration",
     "content",
     "audience"
    ],
    "description": "`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."
   },
   "targetContract": {
    "type": "string",
    "description": "Which contract would perform it. The assistant never performs it itself."
   },
   "targetOperation": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "description": "**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n",
    "enum": [
     "proposed",
     "approved",
     "rejected",
     "applied",
     "expired"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."
   },
   "approvalLevel": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decisionReason": {
    "type": "string",
    "nullable": true,
    "description": "Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"
   },
   "proposedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan",
    "description": "The plan this action presents for a decision (AI design 2.2 D, 3.8)."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."
   },
   "changeSetHash": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."
   }
  }
 }
}
```
