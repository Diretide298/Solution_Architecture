# WS143 — Marketing CRM Configuration Reference v1.0 board 9

**10 screens · 7 operations · 10 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `CASE_VIEW, MARKETING_MANAGE, MARKETING_VIEW, ORDER_REFUND`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-814` | Voice of Customer Center | listDetail | 1 | 0 | — |
| `BO-815` | Survey Builder | listDetail | 1 | 0 | — |
| `BO-816` | Survey Triggers & Distribution | listDetail | 1 | 0 | — |
| `BO-817` | NPS, CSAT & CES Configuration | listDetail | 1 | 0 | — |
| `BO-818` | Survey Responses & Insights | listDetail | 1 | 0 | — |
| `BO-819` | Review Collection & Rating Rules | listDetail | 1 | 0 | — |
| `BO-820` | Moderation & Publishing | listDetail | 1 | 0 | — |
| `BO-821` | AI Sentiment & Topic Analysis | listDetail | 1 | 0 | — |
| `BO-822` | Service Recovery Automation | listDetail | 1 | 0 | — |
| `BO-823` | VOC Analytics & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-814, BO-815, BO-816, BO-817, BO-818, BO-819, BO-820, BO-821, BO-822, BO-823 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-814",
  "name": "Voice of Customer Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "01",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/voice-of-customer-center-bo-814",
   "component": "apps/venue-management-web/src/routes/engagement-support/VoiceOfCustomerCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-815",
    "BO-816",
    "BO-817",
    "BO-818",
    "BO-819",
    "BO-820",
    "BO-821",
    "BO-822",
    "BO-823"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-815",
     "trigger": "Survey Builder",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-816",
     "trigger": "Survey Triggers & Distribution",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-817",
     "trigger": "NPS, CSAT & CES Configuration",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-818",
     "trigger": "Survey Responses & Insights",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-819",
     "trigger": "Review Collection & Rating Rules",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-820",
     "trigger": "Moderation & Publishing",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-821",
     "trigger": "AI Sentiment & Topic Analysis",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-822",
     "trigger": "Service Recovery Automation",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-823",
     "trigger": "VOC Analytics & Audit",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a consolidated view of guest feedback and recovery performance. Show surveys sent, response rate, NPS, CSAT, CES, review count, average rating and negative- feedback volume. Visualize metric, rating, sentiment, topic and recovery trends by brand, venue, product, event and channel. Surface urgent detractors, repeated issues, moderation backlog and recovery cases at risk. Provide AI summaries with links to underlying responses and explainable topic evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 45"
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
       "impliedBy": "listCustomerSatisfactionFeedback",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The voice customer list.",
   "error": "Could not load. Names which read failed and leaves the voice customer untouched.",
   "emptyFirstRun": "No voice customer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the voice customer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerSatisfactionFeedback",
    "contract": "marketing-crm",
    "purpose": "Feedback at a glance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-814",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-814"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 45. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-815",
  "name": "Survey Builder",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "02",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/survey-builder-bo-815",
   "component": "apps/venue-management-web/src/routes/engagement-support/SurveyBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-814"
   ],
   "exitTo": [
    "BO-814"
   ],
   "transitions": [
    {
     "to": "BO-814",
     "trigger": "Back to Voice of Customer Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create multilingual, accessible surveys without development. Provide rating, NPS, single choice, multiple choice, text, matrix, date, media and information- section elements. Support question library, templates, required fields, validation, page/section layout and conditional branching. Configure identified or anonymous response, consent statement, incentive and completion behavior. Preview by channel and language and version, approve and test before publication. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**Survey Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 45"
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
       "impliedBy": "createForm",
       "label": "Create form",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createForm"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The survey list.",
   "error": "Could not load. Names which read failed and leaves the survey untouched.",
   "emptyFirstRun": "No survey yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the survey are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createForm",
    "contract": "marketing-crm",
    "purpose": "Build a survey",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-815",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-815"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 45. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-816",
  "name": "Survey Triggers & Distribution",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "03",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/survey-triggers-distribution-bo-816",
   "component": "apps/venue-management-web/src/routes/engagement-support/SurveyTriggersDistribution.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-814"
   ],
   "exitTo": [
    "BO-814"
   ],
   "transitions": [
    {
     "to": "BO-814",
     "trigger": "Back to Voice of Customer Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control when, where and to whom a survey is sent. Trigger after purchase, visit, event, reservation, membership interaction, case closure or inactivity. Distribute through email, SMS, WhatsApp, push, mobile app, web, kiosk and QR where supported. Configuration Scope of Work | Version 1.0 45 Configure delay, expiry, reminder, sample, quota, frequency cap, exclusions and incentive. Validate consent and eligibility and prevent duplicate or excessive survey requests. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 45"
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
       "impliedBy": "setMessageTrigger",
       "label": "Save message trigger",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMessageTrigger"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The survey triggers distribution list.",
   "error": "Could not load. Names which read failed and leaves the survey triggers distribution untouched.",
   "emptyFirstRun": "No survey triggers distribution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the survey triggers distribution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMessageTrigger",
    "contract": "marketing-crm",
    "purpose": "Survey triggers and distribution",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-816",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-816"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 45. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-817",
  "name": "NPS, CSAT & CES Configuration",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "04",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/nps-csat-ces-configuration-bo-817",
   "component": "apps/venue-management-web/src/routes/engagement-support/NpsCsatCesConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-814"
   ],
   "exitTo": [
    "BO-814"
   ],
   "transitions": [
    {
     "to": "BO-814",
     "trigger": "Back to Voice of Customer Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define standardized experience metrics and follow-up thresholds. Configure metric definition, scale, labels, score bands, calculation and rounding. Set targets, benchmarks, venue/category mappings and reporting periods. Define detractor, low-CSAT and high-effort follow-up actions and case priority. Version metric rules and prevent historical results from being silently recalculated. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 46"
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
       "impliedBy": "createForm",
       "label": "Create form",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createForm"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The nps csat ces list.",
   "error": "Could not load. Names which read failed and leaves the nps csat ces untouched.",
   "emptyFirstRun": "No nps csat ces yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the nps csat ces are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createForm",
    "contract": "marketing-crm",
    "purpose": "NPS, CSAT and CES configuration",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-817",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-817"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 7 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-818",
  "name": "Survey Responses & Insights",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "05",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/survey-responses-insights-bo-818",
   "component": "apps/venue-management-web/src/routes/engagement-support/SurveyResponsesInsights.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-814"
   ],
   "exitTo": [
    "BO-814"
   ],
   "transitions": [
    {
     "to": "BO-814",
     "trigger": "Back to Voice of Customer Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Review individual responses and their calculated insight. Show respondent/profile or anonymous status, survey/version, answers, channel, timestamps and incentive outcome. Display NPS, CSAT, CES, sentiment, topics, urgency and linked guest/transaction where permitted. Filter, search, export, tag, assign follow-up and open a service-recovery case. Protect anonymity and sensitive free text and preserve the submitted response unchanged. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 46"
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
       "impliedBy": "listCustomerSatisfactionFeedback",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The survey responses insights list.",
   "error": "Could not load. Names which read failed and leaves the survey responses insights untouched.",
   "emptyFirstRun": "No survey responses insights yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the survey responses insights are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerSatisfactionFeedback",
    "contract": "marketing-crm",
    "purpose": "Responses and insight",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-818",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-818"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-819",
  "name": "Review Collection & Rating Rules",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "06",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/review-collection-rating-rules-bo-819",
   "component": "apps/venue-management-web/src/routes/engagement-support/ReviewCollectionRatingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-814"
   ],
   "exitTo": [
    "BO-814"
   ],
   "transitions": [
    {
     "to": "BO-814",
     "trigger": "Back to Voice of Customer Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure verified review and rating capture. Define review entities including attraction, event, ticket, product, membership, venue, dining and employee/service. Configure overall and category ratings, minimum/maximum scale, required comments and media support. Validate verified visits or purchases, identity, submission window, duplicates and fraud/spam signals. Map capture channels and decide which reviews require moderation before publication. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 46"
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
       "impliedBy": "listReviews",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The review collection rating list.",
   "error": "Could not load. Names which read failed and leaves the review collection rating untouched.",
   "emptyFirstRun": "No review collection rating yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the review collection rating are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReviews",
    "contract": "marketing-crm",
    "purpose": "Reviews collected",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-819",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-819"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-820",
  "name": "Moderation & Publishing",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "07",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/moderation-publishing-bo-820",
   "component": "apps/venue-management-web/src/routes/engagement-support/ModerationPublishing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-814"
   ],
   "exitTo": [
    "BO-814"
   ],
   "transitions": [
    {
     "to": "BO-814",
     "trigger": "Back to Voice of Customer Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Review and publish guest feedback safely and consistently. Provide moderation queue with channel, rating, text, media, flags, sentiment, topic and SLA. Approve, reject, redact, escalate or request follow-up using reason codes and permission controls. Configure profanity, personal-data, fraud and policy checks and public response templates. Configuration Scope of Work | Version 1.0 46 Publish to approved TICVAI and external channels and retain original, moderated and published versions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 46"
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
       "impliedBy": "respondToReview",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "respondToReview"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The moderation publishing list.",
   "error": "Could not load. Names which read failed and leaves the moderation publishing untouched.",
   "emptyFirstRun": "No moderation publishing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the moderation publishing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "respondToReview",
    "contract": "marketing-crm",
    "purpose": "Moderate and publish",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-820",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-820"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "reviewId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-821",
  "name": "AI Sentiment & Topic Analysis",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "08",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/ai-sentiment-topic-analysis-bo-821",
   "component": "apps/venue-management-web/src/routes/engagement-support/AiSentimentTopicAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-814"
   ],
   "exitTo": [
    "BO-814"
   ],
   "transitions": [
    {
     "to": "BO-814",
     "trigger": "Back to Voice of Customer Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Analyze feedback at scale using explainable AI. Classify sentiment, emotion, urgency, topics, issue type and intent across survey and review text. Cluster recurring issues and summarize themes by venue, product, event, language and time period. Show confidence, supporting excerpts, model/version and correction controls for reviewers. Monitor quality, bias and drift and restrict use of sensitive data or unsupported inference. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 47"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 47"
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
       "impliedBy": "listCustomerSatisfactionFeedback",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sentiment topic analysis list.",
   "error": "Could not load. Names which read failed and leaves the sentiment topic analysis untouched.",
   "emptyFirstRun": "No sentiment topic analysis yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sentiment topic analysis are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerSatisfactionFeedback",
    "contract": "marketing-crm",
    "purpose": "Sentiment and topics",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-821",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-821"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-822",
  "name": "Service Recovery Automation",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "09",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/service-recovery-automation-bo-822",
   "component": "apps/venue-management-web/src/routes/engagement-support/ServiceRecoveryAutomation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-814"
   ],
   "exitTo": [
    "BO-814"
   ],
   "transitions": [
    {
     "to": "BO-814",
     "trigger": "Back to Voice of Customer Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Turn negative feedback into governed service action. Create rules for detractors, low CSAT, high effort, negative review, urgent topic and repeated issue. Create and route a case, select priority, notify the owner and recommend an approved recovery offer. Require approval based on compensation amount, guest tier, issue severity and fraud risk. Schedule follow-up, capture resolution and measure recovery, rating change, satisfaction and retention. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 47"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 47"
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
       "impliedBy": "setRefundCompensationService",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setRefundCompensationService"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The service recovery automation list.",
   "error": "Could not load. Names which read failed and leaves the service recovery automation untouched.",
   "emptyFirstRun": "No service recovery automation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the service recovery automation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRefundCompensationService",
    "contract": "marketing-crm",
    "purpose": "Automated service recovery",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-822",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-822"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-823",
  "name": "VOC Analytics & Audit",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "9",
   "number": "10",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/voc-analytics-audit-bo-823",
   "component": "apps/venue-management-web/src/routes/engagement-support/VocAnalyticsAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-814"
   ],
   "exitTo": [
    "BO-814"
   ],
   "transitions": [
    {
     "to": "BO-814",
     "trigger": "Back to Voice of Customer Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide cross-source performance and governance reporting. Combine NPS, CSAT, CES, ratings, sentiment, topics and response rates without double-counting guests. Benchmark venues, products, events, categories, channels and periods and expose root-cause drivers. Measure moderation SLA, recovery volume, recovery success, compensation cost and guest impact. Audit survey/review setup, AI analysis, moderation, publishing, case creation, exports and administrative actions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 47 Board 10 - Gamification & Loyalty Engagement Figure 10. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 48",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 47"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 47"
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
       "impliedBy": "listServiceRootCause",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The voc analytics audit list.",
   "error": "Could not load. Names which read failed and leaves the voc analytics audit untouched.",
   "emptyFirstRun": "No voc analytics audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the voc analytics audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listServiceRootCause",
    "contract": "marketing-crm",
    "purpose": "Analytics and root cause",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-823",
   "workshopBoard": "wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-823"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createForm": {
  "method": "POST",
  "path": "/forms",
  "contract": "marketing-crm",
  "summary": "Define a waiver, survey or capture form",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "FormDefinition",
  "responds": "FormDefinition"
 },
 "listCustomerSatisfactionFeedback": {
  "method": "GET",
  "path": "/customer-satisfaction-feedback",
  "contract": "marketing-crm",
  "summary": "Customer Satisfaction, Feedback & Voice of Customer",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "source",
    "in": "query",
    "required": false
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "agentPrincipalId",
    "in": "query",
    "required": false
   },
   {
    "name": "sentiment",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "CustomerSatisfactionFeedbackVoiceOfCustomerView"
 },
 "listReviews": {
  "method": "GET",
  "path": "/reviews",
  "contract": "marketing-crm",
  "summary": "List guest reviews and ratings",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "minRating",
    "in": "query",
    "required": null
   },
   {
    "name": "hasResponse",
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
 "listServiceRootCause": {
  "method": "GET",
  "path": "/service-root-cause",
  "contract": "marketing-crm",
  "summary": "Service Analytics & Root-Cause Intelligence",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
    "in": "query",
    "required": false
   },
   {
    "name": "compare",
    "in": "query",
    "required": false
   },
   {
    "name": "compareId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ServiceAnalyticsRootCauseIntelligenceView"
 },
 "respondToReview": {
  "method": "POST",
  "path": "/reviews/{reviewId}/respond",
  "contract": "marketing-crm",
  "summary": "Respond to a review",
  "permission": "MARKETING_MANAGE",
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
  "responds": "Review"
 },
 "setMessageTrigger": {
  "method": "POST",
  "path": "/message-triggers",
  "contract": "marketing-crm",
  "summary": "Fire a message from a platform event",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "MessageTrigger",
  "responds": "MessageTrigger"
 },
 "setRefundCompensationService": {
  "method": "PUT",
  "path": "/refund-compensation-service",
  "contract": "marketing-crm",
  "summary": "Raise or change a refund, compensation or policy-exception request on a case",
  "permission": "ORDER_REFUND",
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
  "requestBody": "RefundCompensationServiceExceptionWorkspaceInput",
  "responds": "RefundCompensationServiceExceptionWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CustomerSatisfactionFeedbackVoiceOfCustomerView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.form_submission and marketing.form_definition (survey forms), marketing.review, marketing.case and marketing.feedback_classification (new, the AI sentiment and topic per feedback item)",
  "description": "Voice-of-customer figures for the filters given. Rates are shares of feedback items in the period.",
  "required": [
   "responses",
   "breakdown",
   "comments"
  ],
  "properties": {
   "responses": {
    "type": "integer",
    "minimum": 0,
    "description": "Feedback items in the period."
   },
   "csat": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Share of CSAT answers in the top two points of the scale."
   },
   "nps": {
    "type": "integer",
    "minimum": -100,
    "maximum": 100,
    "nullable": true,
    "description": "Null where the tenant runs no NPS survey."
   },
   "surveyResponseRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Surveys answered over surveys sent."
   },
   "positiveRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "neutralRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "negativeRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "complaints": {
    "type": "integer",
    "minimum": 0
   },
   "repeatContactRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Customers with a second case within 7 days of the first, over customers with a case."
   },
   "customerEffortScore": {
    "type": "number",
    "minimum": 1,
    "maximum": 7,
    "nullable": true,
    "description": "Mean CES answer; null where effort is not measured."
   },
   "csatChangeRate": {
    "type": "number",
    "nullable": true,
    "description": "Relative change in `csat` against the previous period of equal length."
   },
   "breakdown": {
    "type": "array",
    "description": "One row per value of the `groupBy` dimension, most responses first.",
    "items": {
     "type": "object",
     "required": [
      "key",
      "label",
      "responses"
     ],
     "properties": {
      "key": {
       "type": "string",
       "description": "The id or enum value of the group."
      },
      "label": {
       "type": "string"
      },
      "responses": {
       "type": "integer",
       "minimum": 0
      },
      "csat": {
       "type": "number",
       "minimum": 0,
       "maximum": 1,
       "nullable": true
      },
      "negativeRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "themes": {
    "type": "array",
    "maxItems": 20,
    "description": "AI topic themes, largest share first. Empty when AI is disabled for the tenant.",
    "items": {
     "type": "object",
     "required": [
      "topic",
      "shareRate"
     ],
     "properties": {
      "topic": {
       "type": "string",
       "maxLength": 100
      },
      "shareRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "negativeRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "changeRate": {
       "type": "number",
       "nullable": true,
       "description": "Relative change in the theme's volume against the previous period."
      }
     }
    }
   },
   "trendAlerts": {
    "type": "array",
    "maxItems": 10,
    "items": {
     "type": "string",
     "maxLength": 300
    },
    "description": "AI-detected shifts, e.g. negative feedback on ticket delivery rising after a release."
   },
   "comments": {
    "type": "array",
    "maxItems": 50,
    "description": "The 50 latest comments with text, newest first.",
    "items": {
     "type": "object",
     "required": [
      "feedbackId",
      "source",
      "receivedAt"
     ],
     "properties": {
      "feedbackId": {
       "type": "string",
       "format": "uuid"
      },
      "source": {
       "type": "string",
       "enum": [
        "csatSurvey",
        "serviceRating",
        "nps",
        "postCaseSurvey",
        "complaint",
        "appFeedback",
        "webFeedback",
        "directComment"
       ]
      },
      "receivedAt": {
       "type": "string",
       "format": "date-time"
      },
      "comment": {
       "type": "string",
       "maxLength": 4000,
       "nullable": true
      },
      "rating": {
       "type": "number",
       "nullable": true,
       "description": "The answer on its survey's own scale."
      },
      "ratingScale": {
       "type": "string",
       "nullable": true,
       "enum": [
        "nps",
        "csat",
        "ces",
        "likert5",
        "likert7",
        "stars"
       ]
      },
      "sentiment": {
       "type": "string",
       "nullable": true,
       "enum": [
        "positive",
        "neutral",
        "negative"
       ]
      },
      "topic": {
       "type": "string",
       "nullable": true
      },
      "caseId": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
       "nullable": true
      },
      "agentPrincipalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "eventId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "followUpCaseId": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "FormDefinition": {
  "type": "object",
  "x-ticvai-persistence": "marketing.form_definition + marketing.form_definition_field",
  "description": "CF-129, CL-04. **A waiver, a survey and a data-capture form are one mechanism.**\nA waiver is this form with a signature. A survey is this form with a scale. A demographic capture is this form at the point of sale. They were raised as three separate gaps and share every part: field configuration, conditional display, versioning, an acceptance record and a stored artefact.\n**Three implementations would drift on the version rule first.** A waiver signed against version 3 must stay bound to version 3, and that is the same requirement a survey has when question wording changes mid-campaign — **an NPS score means nothing if you cannot say which question produced it.**\n",
  "required": [
   "id",
   "name",
   "kind",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "waiver",
     "survey",
     "dataCapture",
     "consentForm",
     "incidentReport",
     "registration"
    ]
   },
   "version": {
    "readOnly": true,
    "type": "integer",
    "description": "**Set by the server** — 1 on `createForm`, the next number on every change. **Immutable once anything is submitted against it.** A change creates a new version, and the old one stays readable forever — 2.15.13 requires the exact accepted version retained, which is legal evidence rather than a nicety.\n"
   },
   "fields": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FormField"
    }
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false,
    "description": "**What makes it a waiver.** And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it.\n"
   },
   "signatureKind": {
    "type": "string",
    "enum": [
     "drawn",
     "typed",
     "checkbox",
     "none"
    ],
    "default": "none"
   },
   "scoreScale": {
    "type": "string",
    "nullable": true,
    "enum": [
     "nps",
     "csat",
     "ces",
     "likert5",
     "likert7",
     "stars"
    ],
    "description": "**What makes it a survey.** Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's.\n"
   },
   "appliesToProductIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "validForMonths": {
    "type": "integer",
    "nullable": true,
    "description": "**How long an acceptance lasts.** A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to sign again — which only works if the expiry is stated.\n"
   },
   "minimumAge": {
    "type": "integer",
    "nullable": true
   },
   "requiresGuardianForMinors": {
    "type": "boolean",
    "default": true,
    "description": "**A minor cannot waive their own rights.** A guardian signs, and the record has to name them — an unsigned or self-signed minor waiver is worth nothing at the moment it matters.\n"
   },
   "status": {
    "readOnly": true,
    "type": "string",
    "enum": [
     "draft",
     "published",
     "superseded",
     "retired"
    ]
   },
   "legalReviewedBy": {
    "type": "string",
    "nullable": true
   },
   "legalReviewedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "FormField": {
  "type": "object",
  "description": "One field. **Conditional display is the shared requirement** — a survey branching on an answer and a waiver revealing a medical question on a yes are the same mechanism.\n",
  "required": [
   "key",
   "label",
   "type"
  ],
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "labelLocalised": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "type": {
    "type": "string",
    "enum": [
     "text",
     "longText",
     "number",
     "date",
     "select",
     "multiSelect",
     "boolean",
     "scale",
     "signature",
     "file",
     "phone",
     "email"
    ]
   },
   "options": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "isRequired": {
    "type": "boolean",
    "default": false
   },
   "isPersonalData": {
    "type": "boolean",
    "default": false,
    "description": "**Marked at the field, because retention is decided at the field.** A survey answer and a medical condition on the same form have different lifetimes, and a form-level flag makes the whole thing as sensitive as its most sensitive field.\n"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "showWhen": {
    "type": "object",
    "nullable": true,
    "properties": {
     "field": {
      "type": "string"
     },
     "equals": {
      "type": "string"
     }
    }
   }
  }
 },
 "MessageTrigger": {
  "type": "object",
  "x-ticvai-persistence": "marketing.message_trigger",
  "description": "**What fires a message.** Before, during and after a visit are one mechanism with a different sign on the offset.\n",
  "required": [
   "id",
   "event",
   "templateId",
   "isActive"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "event": {
    "type": "string",
    "description": "The platform event that fires it — `order.completed`, `access.validated`, `queue.turnApproaching`. **Named from the event catalogue** (`BusinessEvent.eventType`), so a trigger cannot bind to something nothing publishes. Its conditions are `MessageTriggerCondition` rows.\n"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "offsetMinutes": {
    "type": "integer",
    "default": 0,
    "description": "Negative fires before the anchor, positive after. **A reminder the day before a visit is -1440 against the performance**, not a separate concept.\n"
   },
   "anchor": {
    "type": "string",
    "enum": [
     "eventTime",
     "performanceStart",
     "visitEnd"
    ],
    "default": "eventTime"
   },
   "priority": {
    "type": "string",
    "enum": [
     "operational",
     "transactional",
     "marketing"
    ],
    "default": "transactional",
    "description": "**A queue-turn alert and a monthly newsletter are not the same urgency and were the same dispatch.** `operational` bypasses batching and quiet hours; `marketing` never does.\n"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
 "RefundCompensationServiceExceptionWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_compensation_request",
  "x-ticvai-record-definition": "Request Types",
  "description": "One refund, compensation or policy-exception request raised from a case. The order, refund and approval are references, never copies.",
  "required": [
   "id",
   "caseId",
   "requestType",
   "value",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID; equals the `Idempotency-Key` header."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "caseId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Required for `fullRefund`, `partialRefund`, `feeWaiver`, `upgrade` and `discount`."
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "requestType": {
    "type": "string",
    "enum": [
     "fullRefund",
     "partialRefund",
     "serviceCredit",
     "walletCredit",
     "voucher",
     "complimentaryTicket",
     "feeWaiver",
     "upgrade",
     "discount",
     "policyException"
    ]
   },
   "value": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "The money value requested; for a complimentary ticket or upgrade, its face value. This is what the approval thresholds are compared with."
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 1000
   },
   "isPolicyException": {
    "type": "boolean",
    "default": false,
    "description": "True when the standard policy would not allow it; always needs approval."
   },
   "exceptionReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true,
    "description": "Required when `isPolicyException` is true."
   },
   "submit": {
    "type": "boolean",
    "default": false,
    "description": "False saves a draft; true routes it.",
    "writeOnly": true
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "draft",
     "pendingApproval",
     "approved",
     "declined",
     "fulfilled",
     "failed",
     "withdrawn"
    ]
   },
   "approvalRequestId": {
    "type": "string",
    "readOnly": true,
    "nullable": true
   },
   "fulfilmentOperation": {
    "type": "string",
    "readOnly": true,
    "nullable": true,
    "description": "e.g. `createRefund`, `topUpWallet`."
   },
   "fulfilmentReference": {
    "type": "string",
    "readOnly": true,
    "nullable": true,
    "description": "The refund, wallet transaction or voucher it produced."
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "RefundCompensationServiceExceptionWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case_compensation_request (new), orders.sales_order, orders.refund, orders.order_fee, orders.refund_policy and approvals.request",
  "description": "The request, the order's financial context, the policy evaluation and who must approve.",
  "required": [
   "request",
   "approvalLevel"
  ],
  "properties": {
   "request": {
    "$ref": "#/components/schemas/RefundCompensationServiceExceptionWorkspaceInput"
   },
   "originalTransaction": {
    "type": "string",
    "nullable": true,
    "description": "The order number."
   },
   "amountPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "amountUsed": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Value of tickets already scanned or consumed."
   },
   "refundableAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "What the refund policy's time bands allow now, less previous refunds."
   },
   "previousRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "fees": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "proposedRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "proposedCompensation": {
    "type": "object",
    "nullable": true,
    "properties": {
     "requestType": {
      "type": "string"
     },
     "value": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    }
   },
   "policyEvaluation": {
    "type": "object",
    "properties": {
     "standardPolicy": {
      "type": "string",
      "description": "The rule that applies, as the venue's refund policy states it."
     },
     "isWithinPolicy": {
      "type": "boolean"
     },
     "policyReference": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "approvalLevel": {
    "type": "string",
    "enum": [
     "agent",
     "secondUser",
     "approver"
    ],
    "description": "From the venue's `selfAuthoriseLimit`, `requiresSecondUserAbove` and `requiresApprovalAbove`; a policy exception is always `approver`."
   },
   "aiExplanation": {
    "type": "string",
    "nullable": true,
    "maxLength": 1000,
    "description": "AI-derived and labelled as such; cites a recorded policy or says none applies."
   }
  }
 },
 "Review": {
  "x-ticvai-persistence": "marketing.review",
  "allOf": [
   {
    "$ref": "#/components/schemas/SubmitReviewRequest"
   },
   {
    "type": "object",
    "required": [
     "status"
    ],
    "properties": {
     "status": {
      "type": "string",
      "enum": [
       "pendingModeration",
       "published",
       "hidden",
       "rejected"
      ]
     },
     "response": {
      "type": "string",
      "nullable": true
     },
     "responseIsPublic": {
      "type": "boolean"
     },
     "respondedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "openedCaseId": {
      "type": "string",
      "nullable": true,
      "description": "Case raised automatically where the rating fell below the venue's threshold. Feedback that goes nowhere is worse than no feedback mechanism.\n"
     }
    }
   }
  ]
 },
 "ServiceAnalyticsRootCauseIntelligenceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case, marketing.conversation, marketing.form_submission (CSAT) and the related orders and payments",
  "description": "Service analytics for the filters given, with the comparison asked for.",
  "required": [
   "contactVolume",
   "cases",
   "drivers",
   "comparison"
  ],
  "properties": {
   "contactVolume": {
    "type": "integer",
    "minimum": 0,
    "description": "Conversations and cases opened, a conversation that became a case counted once."
   },
   "cases": {
    "type": "integer",
    "minimum": 0
   },
   "averageFirstResponseSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "averageResolutionSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "firstContactResolutionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "reopenRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "escalationRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "slaComplianceRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "costPerCase": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "csat": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "refundRequests": {
    "type": "integer",
    "minimum": 0
   },
   "complaintRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "comparison": {
    "type": "object",
    "required": [
     "basis",
     "kpis"
    ],
    "properties": {
     "basis": {
      "type": "string",
      "enum": [
       "previousDay",
       "previousWeek",
       "previousMonth",
       "event",
       "venue",
       "product"
      ]
     },
     "compareId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "kpis": {
      "type": "array",
      "items": {
       "type": "object",
       "required": [
        "kpi"
       ],
       "properties": {
        "kpi": {
         "type": "string",
         "description": "The KPI's property name above, e.g. `contactVolume`."
        },
        "current": {
         "type": "number",
         "nullable": true
        },
        "previous": {
         "type": "number",
         "nullable": true
        },
        "changeRate": {
         "type": "number",
         "nullable": true
        }
       }
      }
     }
    }
   },
   "drivers": {
    "type": "array",
    "description": "Contact drivers, most cases first.",
    "items": {
     "type": "object",
     "required": [
      "driver",
      "cases",
      "shareRate"
     ],
     "properties": {
      "driver": {
       "type": "string",
       "enum": [
        "ticketDelivery",
        "refund",
        "reschedule",
        "paymentFailure",
        "membership",
        "accessIssue",
        "groupBooking",
        "generalInformation",
        "other"
       ]
      },
      "cases": {
       "type": "integer",
       "minimum": 0
      },
      "shareRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "changeRate": {
       "type": "number",
       "nullable": true
      }
     }
    }
   },
   "rootCauses": {
    "type": "array",
    "maxItems": 20,
    "description": "Case surges traced to one cause, largest first. Empty when AI is disabled for the tenant.",
    "items": {
     "type": "object",
     "required": [
      "summary",
      "cases"
     ],
     "properties": {
      "summary": {
       "type": "string",
       "maxLength": 500
      },
      "driver": {
       "type": "string",
       "nullable": true
      },
      "cases": {
       "type": "integer",
       "minimum": 0
      },
      "causeType": {
       "type": "string",
       "enum": [
        "paymentProvider",
        "event",
        "product",
        "release",
        "incident",
        "venueArea",
        "other"
       ]
      },
      "causeRef": {
       "type": "string",
       "nullable": true,
       "description": "The id of the provider, event, product or incident, where there is one."
      },
      "windowStart": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "windowEnd": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "avoidableContacts": {
    "type": "array",
    "description": "AI estimate of cases that could have been prevented, by remedy.",
    "items": {
     "type": "object",
     "required": [
      "preventableBy",
      "cases"
     ],
     "properties": {
      "preventableBy": {
       "type": "string",
       "enum": [
        "betterB2cInformation",
        "selfService",
        "productConfiguration",
        "improvedNotifications",
        "technicalFixes",
        "betterTicketDelivery"
       ]
      },
      "cases": {
       "type": "integer",
       "minimum": 0
      },
      "recommendation": {
       "type": "string",
       "maxLength": 500,
       "nullable": true
      }
     }
    }
   }
  }
 },
 "SubmitReviewRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "rating",
   "venueId",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "relatedOrderId": {
    "type": "string"
   },
   "rating": {
    "type": "integer",
    "minimum": 1,
    "maximum": 5
   },
   "body": {
    "type": "string",
    "maxLength": 5000
   },
   "aspects": {
    "type": "array",
    "description": "Aspect chips — the closed set the description always named.",
    "uniqueItems": true,
    "items": {
     "type": "string",
     "enum": [
      "exhibitions",
      "staff",
      "cleanliness",
      "food",
      "value"
     ]
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 }
}
```
