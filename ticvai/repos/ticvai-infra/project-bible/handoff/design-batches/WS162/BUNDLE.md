# WS162 — Resource Management Configuration board 8

**10 screens · 2 operations · 2 schemas · 1 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `RESOURCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-923` | AI Resource Intelligence Command Center | listDetail | 1 | 0 | — |
| `BO-924` | Optimal Resource Recommendation Engine | listDetail | 1 | 0 | — |
| `BO-925` | AI Staff Recommendation & Workforce Matching | listDetail | 0 | 0 | — |
| `BO-926` | Resource Demand Forecasting | listDetail | 0 | 0 | — |
| `BO-927` | AI Staffing Requirement Forecast | configEditor | 0 | 0 | — |
| `BO-928` | AI Conflict Resolution Assistant | listDetail | 0 | 0 | — |
| `BO-929` | Automatic Schedule Optimization | listDetail | 0 | 0 | — |
| `BO-930` | Alternative & Replacement Resource | listDetail | 1 | 0 | — |
| `BO-931` | Operational Scenario Simulator & Digital Twin | listDetail | 0 | 0 | — |
| `BO-932` | Conversational AI Resource Copilot | listDetail | 0 | 0 | — |

## Thin screens in this batch

**BO-923, BO-924, BO-925, BO-926, BO-927, BO-929, BO-930, BO-931, BO-932 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-923",
  "name": "AI Resource Intelligence Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "01",
   "page": 117
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/ai-resource-intelligence-command-center-bo-923",
   "component": "apps/venue-management-web/src/routes/rentals/AiResourceIntelligenceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-924",
    "BO-925",
    "BO-926",
    "BO-927",
    "BO-928",
    "BO-929",
    "BO-930",
    "BO-931",
    "BO-932"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-924",
     "trigger": "Optimal Resource Recommendation Engine",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-925",
     "trigger": "AI Staff Recommendation & Workforce Matching",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-926",
     "trigger": "Resource Demand Forecasting",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-927",
     "trigger": "AI Staffing Requirement Forecast",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-928",
     "trigger": "AI Conflict Resolution Assistant",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-929",
     "trigger": "Automatic Schedule Optimization",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-930",
     "trigger": "Alternative & Replacement Resource",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-931",
     "trigger": "Operational Scenario Simulator & Digital Twin",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-932",
     "trigger": "Conversational AI Resource Copilot",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide management with a centralized AI-generated overview of current and future resource conditions across the organization.",
  "purposeNote": "Authorized managers can immediately understand current and forecast resource conditions and see prioritized AI-generated actions from one command center.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 117 §Display"
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
       "label": "Every resource intelligence",
       "columns": [
        "Resource readiness",
        "Today's utilization",
        "Forecast utilization",
        "Predicted shortages",
        "Predicted excess capacity",
        "Staffing gaps",
        "Equipment gaps",
        "Resource conflicts",
        "Overtime risk",
        "Maintenance risk",
        "AI recommendations awaiting action",
        "Estimated optimization opportunity",
        "Time Horizons"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 117 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource intelligence",
       "bindsTo": null,
       "columns": [
        "Resource readiness",
        "Today's utilization",
        "Forecast utilization",
        "Predicted shortages",
        "Predicted excess capacity",
        "Staffing gaps",
        "Equipment gaps",
        "Resource conflicts",
        "Overtime risk",
        "Maintenance risk",
        "AI recommendations awaiting action",
        "Estimated optimization opportunity",
        "Time Horizons"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Users shall switch between”, “Underutilized”, “Overutilized”, “Shortage Risk”, “Resources affected by”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 117 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource intelligence list.",
   "error": "Could not load. Names which read failed and leaves the resource intelligence untouched.",
   "emptyFirstRun": "No resource intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResources",
    "contract": "resources",
    "purpose": "Resources at this venue",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Resource readiness",
    "Today's utilization",
    "Forecast utilization",
    "Predicted shortages",
    "Predicted excess capacity",
    "Staffing gaps"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-923",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-923"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 117. 0 of 13 labels bound to a contract property; 13 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-924",
  "name": "Optimal Resource Recommendation Engine",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "02",
   "page": 118
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/optimal-resource-recommendation-engine-bo-924",
   "component": "apps/venue-management-web/src/routes/rentals/OptimalResourceRecommendationEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-923"
   ],
   "exitTo": [
    "BO-923"
   ],
   "transitions": [
    {
     "to": "BO-923",
     "trigger": "Back to AI Resource Intelligence Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Recommend the best available resource for any operational requirement.",
  "purposeNote": "The AI engine can rank suitable resources for a defined operational requirement and clearly explain why each resource was recommended.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 118"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 118"
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
   "loading": "The optimal resource recommendation list.",
   "error": "Could not load. Names which read failed and leaves the optimal resource recommendation untouched.",
   "emptyFirstRun": "No optimal resource recommendation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the optimal resource recommendation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "suggestResources",
    "contract": "resources",
    "purpose": "Rank the resources that fit a requirement",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-924",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-924"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 118. 0 of 0 labels bound to a contract property; 0 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-925",
  "name": "AI Staff Recommendation & Workforce Matching",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "03",
   "page": 120
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/ai-staff-recommendation-workforce-matching-bo-925",
   "component": "apps/venue-management-web/src/routes/rentals/AiStaffRecommendationWorkforceMatching.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-923"
   ],
   "exitTo": [
    "BO-923"
   ],
   "transitions": [
    {
     "to": "BO-923",
     "trigger": "Back to AI Resource Intelligence Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide advanced AI-assisted selection specifically for human resources. This screen consumes the staff rules established in Boards 3 and 4.",
  "purposeNote": "availability, compliance, skills, and workforce governance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 120"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 120"
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
   "loading": "The staff recommendation workforce list.",
   "error": "Could not load. Names which read failed and leaves the staff recommendation workforce untouched.",
   "emptyFirstRun": "No staff recommendation workforce yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the staff recommendation workforce are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-925",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-925"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 120. 0 of 0 labels bound to a contract property; 0 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-926",
  "name": "Resource Demand Forecasting",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "04",
   "page": 121
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-demand-forecasting-bo-926",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceDemandForecasting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-923"
   ],
   "exitTo": [
    "BO-923"
   ],
   "transitions": [
    {
     "to": "BO-923",
     "trigger": "Back to AI Resource Intelligence Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Predict future demand for resources before shortages occur.",
  "purposeNote": "or excess capacity before the operating date.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 121 §Display"
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
       "label": "Every resource demand forecasting",
       "columns": [
        "Historical",
        "Forecast",
        "Actual"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 121 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource demand forecasting",
       "bindsTo": null,
       "columns": [
        "Historical",
        "Forecast",
        "Actual"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Expected Visitors”, “Expected Lesson Participants”, “Available”, “Confidence”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 121 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource demand forecasting list.",
   "error": "Could not load. Names which read failed and leaves the resource demand forecasting untouched.",
   "emptyFirstRun": "No resource demand forecasting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource demand forecasting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Historical",
    "Forecast",
    "Actual"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-926",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-926"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 121. 0 of 3 labels bound to a contract property; 3 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-927",
  "name": "AI Staffing Requirement Forecast",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "05",
   "page": 122
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/ai-staffing-requirement-forecast-bo-927",
   "component": "apps/venue-management-web/src/routes/rentals/AiStaffingRequirementForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-923"
   ],
   "exitTo": [
    "BO-923"
   ],
   "transitions": [
    {
     "to": "BO-923",
     "trigger": "Back to AI Resource Intelligence Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configured rule) and no display directory — it is settings, not a population",
  "purpose": "Translate forecast operational demand into specific workforce requirements.",
  "purposeNote": "Forecast demand is automatically translated into role, skill, certification, quantity, and time-specific workforce requirements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "1 Lifeguard / 250 guests",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 122 §Configured rule"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staffing requirement forecast configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the staffing requirement forecast untouched.",
   "emptyFirstRun": "No staffing requirement forecast configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-927",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-927"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 122. 0 of 0 labels bound to a contract property; 1 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-928",
  "name": "AI Conflict Resolution Assistant",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "06",
   "page": 123
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/ai-conflict-resolution-assistant-bo-928",
   "component": "apps/venue-management-web/src/routes/rentals/AiConflictResolutionAssistant.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-923"
   ],
   "exitTo": [
    "BO-923"
   ],
   "transitions": [
    {
     "to": "BO-923",
     "trigger": "Back to AI Resource Intelligence Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Automatically analyze resource conflicts and recommend the most operationally appropriate resolution.",
  "purposeNote": "AI can analyze operational conflicts, identify viable alternatives, rank resolutions, and explain the expected operational impact before execution.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 123"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 123"
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
       "label": "Double booking",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 123 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Certification expiry",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 123 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Equipment maintenance",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 123 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue conflict",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 123 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Capacity conflict",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 123 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Dependency conflict",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 123 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Travel-time conflict",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 123 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Setup conflict",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 123 §Support"
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
   "loading": "The conflict resolution assistant list.",
   "error": "Could not load. Names which read failed and leaves the conflict resolution assistant untouched.",
   "emptyFirstRun": "No conflict resolution assistant yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the conflict resolution assistant are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-928",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-928"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 123. 0 of 0 labels bound to a contract property; 17 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Double booking, Certification expiry, Equipment maintenance, Venue conflict, Capacity conflict, Dependency conflict, Travel-time conflict, Setup conflict … dropped (AI design pending review).",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-929",
  "name": "Automatic Schedule Optimization",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "07",
   "page": 125
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/automatic-schedule-optimization-bo-929",
   "component": "apps/venue-management-web/src/routes/rentals/AutomaticScheduleOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-923"
   ],
   "exitTo": [
    "BO-923"
   ],
   "transitions": [
    {
     "to": "BO-923",
     "trigger": "Back to AI Resource Intelligence Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Optimize resource schedules across multiple assignments while respecting operational constraints.",
  "purposeNote": "and maintaining human approval over execution.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 125"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 125"
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
   "loading": "The automatic schedule optimization list.",
   "error": "Could not load. Names which read failed and leaves the automatic schedule optimization untouched.",
   "emptyFirstRun": "No automatic schedule optimization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the automatic schedule optimization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-929",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-929"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 125. 0 of 0 labels bound to a contract property; 0 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-930",
  "name": "Alternative & Replacement Resource",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "08",
   "page": 126
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/alternative-replacement-resource-bo-930",
   "component": "apps/venue-management-web/src/routes/rentals/AlternativeReplacementResource.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-923"
   ],
   "exitTo": [
    "BO-923"
   ],
   "transitions": [
    {
     "to": "BO-923",
     "trigger": "Back to AI Resource Intelligence Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide intelligent alternatives when the preferred resource cannot be used.",
  "purposeNote": "When a preferred resource is unavailable, TICVAI can automatically identify operationally compatible alternatives and rank them by suitability and impact.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 126"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 126"
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
   "loading": "The alternative replacement resource list.",
   "error": "Could not load. Names which read failed and leaves the alternative replacement resource untouched.",
   "emptyFirstRun": "No alternative replacement resource yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the alternative replacement resource are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "suggestResources",
    "contract": "resources",
    "purpose": "Suggest a replacement resource that fits",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-930",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-930"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 126. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-931",
  "name": "Operational Scenario Simulator & Digital Twin",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "09",
   "page": 128
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/operational-scenario-simulator-digital-twin-bo-931",
   "component": "apps/venue-management-web/src/routes/rentals/OperationalScenarioSimulatorDigitalTwin.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-923"
   ],
   "exitTo": [
    "BO-923"
   ],
   "transitions": [
    {
     "to": "BO-923",
     "trigger": "Back to AI Resource Intelligence Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow managers to test operational scenarios before changing the live resource plan. This should be one of Board 8's signature AI capabilities.",
  "purposeNote": "Managers can safely simulate operational changes and understand resource, workforce, capacity, and financial consequences before modifying live schedules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 128"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 128"
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
   "loading": "The operational scenario simulator list.",
   "error": "Could not load. Names which read failed and leaves the operational scenario simulator untouched.",
   "emptyFirstRun": "No operational scenario simulator yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational scenario simulator are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-931",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-931"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 128. 0 of 0 labels bound to a contract property; 0 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-932",
  "name": "Conversational AI Resource Copilot",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "8",
   "number": "10",
   "page": 129
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/conversational-ai-resource-copilot-bo-932",
   "component": "apps/venue-management-web/src/routes/rentals/ConversationalAiResourceCopilot.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-923"
   ],
   "exitTo": [
    "BO-923"
   ],
   "transitions": [
    {
     "to": "BO-923",
     "trigger": "Back to AI Resource Intelligence Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow managers to interact with the complete Resource Management module using natural- language questions and commands. Provide TICVAI employees and operational managers with a mobile-first Resource Operations Workspace where they can see their schedules and assignments, receive operational instructions, check in and out, manage resource handovers, submit workforce requests, approve operational actions, and receive real-time notifications. Board 9 shall expose the appropriate functions through the TICVAI Employee App rather than creating a separate Resource Management mobile application. The mobile experience shall consume the same centralized services used by the TICVAI backend: Resource Master → Calendar → Workforce → Assignment → Attendance → Assets → Events → AI → Mobile Therefore, an assignment changed in the backend must immediately appear in the employee's application, subject to synchronization and connectivity. The experience must be designed for frontline operations: Minimal typing Large touch targets Scan-first workflows Clear status Fast confirmation Mobile notifications Offline support where required Role-specific interfaces Real-time synchronization Arabic and English Primary matrix coverage: 1.2.60–1.2.66. Supporting coverage: 1.2.11, 1.2.17, 1.2.30–1.2.38, 1.2.52, 1.2.60–1.2.66, 1.2.80–1.2.81.",
  "purposeNote": "Authorized users can query, analyze, simulate, and initiate governed resource-management actions conversationally without bypassing normal platform permissions or approval controls. Board 8 — AI Decision Architecture Board 8 should operate through a common Resource Intelligence Layer consuming trusted operational data from the Resource Management domain.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 129"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 129"
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
   "loading": "The conversational resource copilot list.",
   "error": "Could not load. Names which read failed and leaves the conversational resource copilot untouched.",
   "emptyFirstRun": "No conversational resource copilot yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the conversational resource copilot are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-932",
   "workshopBoard": "wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-932"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 129. 0 of 0 labels bound to a contract property; 0 of 168 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
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
 "listResources": {
  "method": "GET",
  "path": "/resources",
  "contract": "resources",
  "summary": "Resources at this venue",
  "permission": "RESOURCE_VIEW",
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
    "name": "availableFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "availableTo",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Resource"
 },
 "suggestResources": {
  "method": "GET",
  "path": "/resource-suggestions",
  "contract": "resources",
  "summary": "Resources matching a requirement, by attribute",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "resourceTypeId",
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
    "name": "attributes",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Resource"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Resource": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource",
  "description": "**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ResourceKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "parentResourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true,
    "description": "Configurable per kind — capacity, size, shade, power, poolside."
   },
   "setupMinutes": {
    "type": "integer",
    "default": 0,
    "description": "**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"
   },
   "teardownMinutes": {
    "type": "integer",
    "default": 0
   },
   "requiresQualification": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Qualification codes a person must hold to be assigned to this."
   },
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "booked",
     "checkedOut",
     "maintenance",
     "retired"
    ]
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ResourceKind": {
  "type": "string",
  "description": "BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n",
  "enum": [
   "cabana",
   "lounger",
   "locker",
   "wheelchair",
   "stroller",
   "equipment",
   "room",
   "auditorium",
   "vehicle",
   "instructor",
   "staff",
   "table",
   "pitch",
   "studio",
   "other"
  ],
  "x-ticvai-refuses": {
   "mealPlan": "**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."
  }
 }
}
```
