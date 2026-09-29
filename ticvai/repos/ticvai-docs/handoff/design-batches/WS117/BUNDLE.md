# WS117 — AI Configuration Assistant board 2

**10 screens · 6 operations · 9 schemas · 2 permissions**

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
  `AI_USE, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-479` | AI Configuration Build Command Center | commandCentre | 3 | 0 | — |
| `ADM-480` | Venue & Organization Configuration | listDetail | 3 | 0 | — |
| `ADM-481` | Product Configuration Assistant | listDetail | 3 | 0 | — |
| `ADM-482` | Schedule, Capacity & Availability Configuration | listDetail | 3 | 0 | — |
| `ADM-483` | Pricing & Commercial Configuration | listDetail | 4 | 0 | — |
| `ADM-484` | Promotion, Bundle & Upsell Configuration | listDetail | 3 | 0 | — |
| `ADM-485` | Seating, Access & Operational Configuration | listDetail | 3 | 0 | — |
| `ADM-486` | Channel, Media & Fulfillment Configuration | listDetail | 3 | 0 | — |
| `ADM-487` | Cross-Module Conflict & Dependency Validation | commandCentre | 2 | 0 | — |
| `ADM-488` | Configuration Preview & Impact Analysis | configEditor | 2 | 0 | — |

## Thin screens in this batch

**ADM-480, ADM-481, ADM-482, ADM-483, ADM-484, ADM-485, ADM-486 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-479",
  "name": "AI Configuration Build Command Center",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "1",
   "page": 24
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-configuration-build-command-center-adm-479",
   "component": "apps/ticvai-web/src/routes/platform/AiConfigurationBuildCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-480",
    "ADM-481",
    "ADM-482",
    "ADM-483",
    "ADM-484",
    "ADM-485",
    "ADM-486",
    "ADM-487",
    "ADM-488"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-480",
     "trigger": "Venue & Organization Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "decisionKey",
      "planId"
     ]
    },
    {
     "to": "ADM-481",
     "trigger": "Product Configuration Assistant",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "decisionKey",
      "planId"
     ]
    },
    {
     "to": "ADM-482",
     "trigger": "Schedule, Capacity & Availability Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "decisionKey",
      "planId"
     ]
    },
    {
     "to": "ADM-483",
     "trigger": "Pricing & Commercial Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "decisionKey",
      "planId"
     ]
    },
    {
     "to": "ADM-484",
     "trigger": "Promotion, Bundle & Upsell Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "decisionKey",
      "planId"
     ]
    },
    {
     "to": "ADM-485",
     "trigger": "Seating, Access & Operational Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "decisionKey",
      "planId"
     ]
    },
    {
     "to": "ADM-486",
     "trigger": "Channel, Media & Fulfillment Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "decisionKey",
      "planId"
     ]
    },
    {
     "to": "ADM-487",
     "trigger": "Cross-Module Conflict & Dependency Validation",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    },
    {
     "to": "ADM-488",
     "trigger": "Configuration Preview & Impact Analysis",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a central workspace showing how the Board 1 blueprint is being converted into actual TICVAI configuration objects.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Configuration Areas",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 24 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Objects Proposed",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 24 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Ready",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 24 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Warnings",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 24 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Conflicts",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 24 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Missing Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 24 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "AI Recommendations",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 24 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Approval Required",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 24 §Header KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The build list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the build untouched.",
   "emptyFirstRun": "No build yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the build are still there. The pack's own statuses are Building Configuration — the state names which is selected.",
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
    "operationId": "getConfigurationBlueprint",
    "contract": "ai",
    "purpose": "The blueprint so far",
    "trigger": "onLoad",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-479",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-479"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 12 of 62 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "planId",
     "from": "navigation"
    },
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
  "id": "ADM-480",
  "name": "Venue & Organization Configuration",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "2",
   "page": 26
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/venue-organization-configuration-adm-480",
   "component": "apps/ticvai-web/src/routes/platform/VenueOrganizationConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-479"
   ],
   "exitTo": [
    "ADM-479"
   ],
   "transitions": [
    {
     "to": "ADM-479",
     "trigger": "Back to AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
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
  "purpose": "Convert the discovered business structure into the actual organizational and venue configuration required by TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 26"
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
       "impliedBy": "decideBlueprintRecommendation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideBlueprintRecommendation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue organization list.",
   "error": "Could not load. Names which read failed and leaves the venue organization untouched.",
   "emptyFirstRun": "No venue organization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue organization are still there. Names the active filter and offers to clear it.",
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-480",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-480"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "planId",
     "from": "navigation"
    },
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
  "id": "ADM-481",
  "name": "Product Configuration Assistant",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "3",
   "page": 27
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/product-configuration-assistant-adm-481",
   "component": "apps/ticvai-web/src/routes/platform/ProductConfigurationAssistant.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-479"
   ],
   "exitTo": [
    "ADM-479"
   ],
   "transitions": [
    {
     "to": "ADM-479",
     "trigger": "Back to AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
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
  "purpose": "Convert Board 1 product requirements into actual proposed TICVAI ticket products and associated product rules. This screen should connect directly to the existing Ticketing module architecture, not create a separate AI product model.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 27"
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
       "impliedBy": "decideBlueprintRecommendation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideBlueprintRecommendation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product assistant list.",
   "error": "Could not load. Names which read failed and leaves the product assistant untouched.",
   "emptyFirstRun": "No product assistant yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product assistant are still there. Names the active filter and offers to clear it.",
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-481",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-481"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "planId",
     "from": "navigation"
    },
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
  "id": "ADM-482",
  "name": "Schedule, Capacity & Availability Configuration",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "4",
   "page": 29
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/schedule-capacity-availability-configuration-adm-482",
   "component": "apps/ticvai-web/src/routes/platform/ScheduleCapacityAvailabilityConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-479"
   ],
   "exitTo": [
    "ADM-479"
   ],
   "transitions": [
    {
     "to": "ADM-479",
     "trigger": "Back to AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
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
  "purpose": "Translate operating requirements into actual schedules, timeslots, reservation windows, and capacity structures.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 29"
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
       "impliedBy": "decideBlueprintRecommendation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideBlueprintRecommendation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The schedule capacity availability list.",
   "error": "Could not load. Names which read failed and leaves the schedule capacity availability untouched.",
   "emptyFirstRun": "No schedule capacity availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the schedule capacity availability are still there. Names the active filter and offers to clear it.",
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-482",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-482"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 0 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "planId",
     "from": "navigation"
    },
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
  "id": "ADM-483",
  "name": "Pricing & Commercial Configuration",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "5",
   "page": 30
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/pricing-commercial-configuration-adm-483",
   "component": "apps/ticvai-web/src/routes/platform/PricingCommercialConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-479"
   ],
   "exitTo": [
    "ADM-479"
   ],
   "transitions": [
    {
     "to": "ADM-479",
     "trigger": "Back to AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
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
  "purpose": "Convert commercial requirements into proposed pricing, tax, fee, and commercial rules using TICVAI's existing Pricing architecture.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 30 §Show"
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
       "label": "Every pricing commercial",
       "columns": [
        "Dynamic Pricing Configuration Required →",
        "Price Simulation",
        "Adult / Saturday / B2C",
        "AED 120",
        "AED 20"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 30 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing commercial",
       "bindsTo": null,
       "columns": [
        "Dynamic Pricing Configuration Required →",
        "Price Simulation",
        "Adult / Saturday / B2C",
        "AED 120",
        "AED 20"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Child AED 80 AED 95”, “Customer Eligibility”, “Dynamic Pricing”.",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 30 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing commercial list.",
   "error": "Could not load. Names which read failed and leaves the pricing commercial untouched.",
   "emptyFirstRun": "No pricing commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setChannelPricingCommercial",
    "contract": "catalogue",
    "purpose": "Channel Pricing & Commercial Profile Assignment",
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
    "Dynamic Pricing Configuration Required →",
    "Price Simulation",
    "Adult / Saturday / B2C",
    "AED 120",
    "AED 20"
   ],
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "planId",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-483",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-483"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 30. 0 of 5 labels bound to a contract property; 12 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-484",
  "name": "Promotion, Bundle & Upsell Configuration",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "6",
   "page": 32
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/promotion-bundle-upsell-configuration-adm-484",
   "component": "apps/ticvai-web/src/routes/platform/PromotionBundleUpsellConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-479"
   ],
   "exitTo": [
    "ADM-479"
   ],
   "transitions": [
    {
     "to": "ADM-479",
     "trigger": "Back to AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
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
  "purpose": "Convert identified commercial opportunities into proposed promotion, package, bundle, upsell, and cross- sell configuration. This screen should only become prominent when relevant.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 32"
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
       "impliedBy": "decideBlueprintRecommendation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideBlueprintRecommendation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion bundle upsell list.",
   "error": "Could not load. Names which read failed and leaves the promotion bundle upsell untouched.",
   "emptyFirstRun": "No promotion bundle upsell yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion bundle upsell are still there. Names the active filter and offers to clear it.",
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-484",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-484"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "planId",
     "from": "navigation"
    },
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
  "id": "ADM-485",
  "name": "Seating, Access & Operational Configuration",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "7",
   "page": 33
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/seating-access-operational-configuration-adm-485",
   "component": "apps/ticvai-web/src/routes/platform/SeatingAccessOperationalConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-479"
   ],
   "exitTo": [
    "ADM-479"
   ],
   "transitions": [
    {
     "to": "ADM-479",
     "trigger": "Back to AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
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
  "purpose": "Configure the operational rules required to fulfill and validate the products. The screen should adapt depending on venue type. For the museum example, seating is irrelevant and should not consume UI attention.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 33"
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
       "impliedBy": "decideBlueprintRecommendation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideBlueprintRecommendation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seating access operational list.",
   "error": "Could not load. Names which read failed and leaves the seating access operational untouched.",
   "emptyFirstRun": "No seating access operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seating access operational are still there. Names the active filter and offers to clear it.",
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-485",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-485"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "planId",
     "from": "navigation"
    },
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
  "id": "ADM-486",
  "name": "Channel, Media & Fulfillment Configuration",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "8",
   "page": 34
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/channel-media-fulfillment-configuration-adm-486",
   "component": "apps/ticvai-web/src/routes/platform/ChannelMediaFulfillmentConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-479"
   ],
   "exitTo": [
    "ADM-479"
   ],
   "transitions": [
    {
     "to": "ADM-479",
     "trigger": "Back to AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
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
  "purpose": "Determine how the proposed products are sold, delivered, and fulfilled across TICVAI channels.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 34"
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
       "impliedBy": "decideBlueprintRecommendation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideBlueprintRecommendation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel media fulfillment list.",
   "error": "Could not load. Names which read failed and leaves the channel media fulfillment untouched.",
   "emptyFirstRun": "No channel media fulfillment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel media fulfillment are still there. Names the active filter and offers to clear it.",
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-486",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-486"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionKey",
     "from": "navigation"
    },
    {
     "name": "planId",
     "from": "navigation"
    },
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
  "id": "ADM-487",
  "name": "Cross-Module Conflict & Dependency Validation",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "9",
   "page": 36
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/cross-module-conflict-dependency-validation-adm-487",
   "component": "apps/ticvai-web/src/routes/platform/CrossModuleConflictDependencyValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-479"
   ],
   "exitTo": [
    "ADM-479"
   ],
   "transitions": [
    {
     "to": "ADM-479",
     "trigger": "Back to AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Perform a comprehensive validation of the proposed configuration across all TICVAI modules before it is presented for approval. This should be one of the most important screens in Board 2.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Link Existing, Configure Later, Ask AI. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Actions"
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
       "label": "Configuration Objects",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Passed",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Warnings",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Conflicts",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Missing Dependencies",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Approval Requirements",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Header KPIs"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Link Existing",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Configure Later",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask AI",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 36 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-module conflict dependency list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the cross-module conflict dependency untouched.",
   "emptyFirstRun": "No cross-module conflict dependency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-module conflict dependency are still there. Names the active filter and offers to clear it.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-487",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-487"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 36. 0 of 0 labels bound to a contract property; 9 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-488",
  "name": "Configuration Preview & Impact Analysis",
  "module": "Platform",
  "requiresModule": "ai",
  "wave": 3,
  "source": {
   "pack": "AI_Configuration_Assistant_Reference.pdf",
   "board": "2",
   "number": "10",
   "page": 37
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/configuration-preview-impact-analysis-adm-488",
   "component": "apps/ticvai-web/src/routes/platform/ConfigurationPreviewImpactAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-479"
   ],
   "exitTo": [
    "ADM-479"
   ],
   "transitions": [
    {
     "to": "ADM-479",
     "trigger": "Back to AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "planId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Critical AI Configuration Object Model; Three Sources of Configuration; AI Configuration Builder & Validation) and no display directory — it is settings, not a population",
  "purpose": "Present the complete proposed configuration in business and technical terms before moving to approval and execution in Board 3. This is the final output of Board 2.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "👤 User Provided",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §Three Sources of Configuration"
      },
      {
       "kind": "textField",
       "label": "1. AI Configuration Build Command Center",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "2. Venue & Organization Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "3. Product Configuration Assistant",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "4. Schedule, Capacity & Availability Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "5. Pricing & Commercial Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "6. Promotion, Bundle & Upsell Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "7. Seating, Access & Operational Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "8. Channel, Media & Fulfillment Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "9. Cross-Module Conflict & Dependency Validation",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "10. Configuration Preview & Impact Analysis",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "“Tell TICVAI what your business needs.”",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "selectField",
       "label": "↓",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "“Govern, approve, and safely execute those changes.”",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "selectField",
       "label": "& Continuous Configuration",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "Module: AI Configuration Assistant",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "textField",
       "label": "Board: 3 of 3",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      },
      {
       "kind": "selectField",
       "label": "Screens: 10",
       "provenance": "pack AI_Configuration_Assistant_Reference.pdf, page 37 §AI Configuration Builder & Validation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The preview impact analysis configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the preview impact analysis untouched.",
   "emptyFirstRun": "No preview impact analysis configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-488",
   "workshopBoard": "wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-488"
  },
  "apisNote": "Regenerated 9 September 2026 from AI_Configuration_Assistant_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 24 of 195 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
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
 "setChannelPricingCommercial": {
  "method": "PUT",
  "path": "/channel-pricing-commercial",
  "contract": "catalogue",
  "summary": "Channel Pricing & Commercial Profile Assignment",
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
  "requestBody": "ChannelPricingCommercialProfileAssignmentInput",
  "responds": "ChannelPricingCommercialProfileAssignmentView"
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
 "ChannelPricingCommercialProfileAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Channel Pricing & Commercial Profile Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each assignment* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "priceProfile": {
    "type": "string",
    "description": "Price Profile: the ID of the approved price list or profile consumed (the Pricing Engine calculates the price)"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue ID",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event ID",
    "nullable": true
   },
   "product": {
    "type": "string",
    "description": "Product ID",
    "nullable": true
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment ID",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "description": "Priority: when several assignments match, the lower number wins",
    "minimum": 1
   },
   "channelId": {
    "type": "string",
    "description": "Channel ID"
   },
   "pricingSource": {
    "type": "string",
    "enum": [
     "standardPriceList",
     "channelPriceList",
     "b2bRate",
     "resellerRate",
     "otaRate",
     "posPrice",
     "promotionalPriceProfile",
     "dynamicPricingProfile"
    ],
    "description": "Pricing Association (pack p.8): which kind of approved pricing this assignment consumes"
   },
   "overridePermission": {
    "type": "string",
    "description": "Override Permission: the permission a user needs to override price on this channel",
    "nullable": true
   },
   "fixedPriceOnly": {
    "type": "boolean",
    "description": "Price Override Governance: use fixed price only"
   },
   "promotionAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: apply promotion"
   },
   "discountAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: apply discount"
   },
   "priceOverrideAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: override price"
   },
   "overrideRequiresApproval": {
    "type": "boolean",
    "description": "Price Override Governance: require approval for override"
   },
   "dynamicPricingAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: use dynamic pricing"
   }
  },
  "x-ticvai-record-definition": "For each assignment"
 },
 "ChannelPricingCommercialProfileAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Pricing & Commercial Profile Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "priceProfile": {
    "type": "string",
    "description": "Price Profile: the ID of the approved price list or profile consumed (the Pricing Engine calculates the price)"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue ID",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event ID",
    "nullable": true
   },
   "product": {
    "type": "string",
    "description": "Product ID",
    "nullable": true
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment ID",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "description": "Priority: when several assignments match, the lower number wins",
    "minimum": 1
   },
   "channelId": {
    "type": "string",
    "description": "Channel ID"
   },
   "pricingSource": {
    "type": "string",
    "enum": [
     "standardPriceList",
     "channelPriceList",
     "b2bRate",
     "resellerRate",
     "otaRate",
     "posPrice",
     "promotionalPriceProfile",
     "dynamicPricingProfile"
    ],
    "description": "Pricing Association (pack p.8): which kind of approved pricing this assignment consumes"
   },
   "overridePermission": {
    "type": "string",
    "description": "Override Permission: the permission a user needs to override price on this channel",
    "nullable": true
   },
   "fixedPriceOnly": {
    "type": "boolean",
    "description": "Price Override Governance: use fixed price only"
   },
   "promotionAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: apply promotion"
   },
   "discountAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: apply discount"
   },
   "priceOverrideAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: override price"
   },
   "overrideRequiresApproval": {
    "type": "boolean",
    "description": "Price Override Governance: require approval for override"
   },
   "dynamicPricingAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: use dynamic pricing"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "missingPrice",
        "expiredPrice",
        "currencyMismatch",
        "conflictingProfiles",
        "invalidOverride"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Price Validation (pack p.9)"
   }
  }
 }
}
```
