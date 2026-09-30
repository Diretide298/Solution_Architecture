# WS139 — Marketing CRM Configuration Reference v1.0 board 5

**10 screens · 10 operations · 13 schemas · 4 permissions**

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
  `AI_USE, MARKETING_MANAGE, MARKETING_SEND, MARKETING_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-774` | Journey Automation Center | listDetail | 1 | 0 | — |
| `BO-775` | Visual Journey Builder | listDetail | 2 | 0 | — |
| `BO-776` | Trigger Event Catalog | listDetail | 2 | 0 | — |
| `BO-777` | Decision Logic & Timing | listDetail | 1 | 0 | — |
| `BO-778` | Abandoned Cart Recovery | listDetail | 1 | 0 | — |
| `BO-779` | Lifecycle Journeys | listDetail | 1 | 0 | — |
| `BO-780` | Guest Engagement Journeys | listDetail | 1 | 0 | — |
| `BO-781` | Cross-Sell & Service Recovery | listDetail | 1 | 0 | — |
| `BO-782` | AI Journey Optimization | listDetail | 4 | 0 | — |
| `BO-783` | Journey Analytics & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-774, BO-775, BO-776, BO-777, BO-778, BO-779, BO-780, BO-781, BO-782, BO-783 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-774",
  "name": "Journey Automation Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "01",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/journey-automation-center-bo-774",
   "component": "apps/venue-management-web/src/routes/engagement-support/JourneyAutomationCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-775",
    "BO-776",
    "BO-777",
    "BO-778",
    "BO-779",
    "BO-780",
    "BO-781",
    "BO-782",
    "BO-783"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-775",
     "trigger": "Visual Journey Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "carries": [
      "journeyId"
     ]
    },
    {
     "to": "BO-776",
     "trigger": "Trigger Event Catalog",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-777",
     "trigger": "Decision Logic & Timing",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-778",
     "trigger": "Abandoned Cart Recovery",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-779",
     "trigger": "Lifecycle Journeys",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-780",
     "trigger": "Guest Engagement Journeys",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-781",
     "trigger": "Cross-Sell & Service Recovery",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "carries": [
      "journeyId"
     ]
    },
    {
     "to": "BO-782",
     "trigger": "AI Journey Optimization",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-783",
     "trigger": "Journey Analytics & Audit",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor the health and value of automated customer journeys. Show active journeys, enrolled guests, conversions, recovered revenue, exits, errors and upcoming actions. Compare journey performance by objective, lifecycle, brand, venue, audience, channel and owner. Surface paused nodes, delivery failures, SLA risk and data or consent problems requiring intervention. Provide drill-down and explainable optimization opportunities without automatically changing live flows. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 26"
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
       "impliedBy": "listJourneys",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The journey automation list.",
   "error": "Could not load. Names which read failed and leaves the journey automation untouched.",
   "emptyFirstRun": "No journey automation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the journey automation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listJourneys",
    "contract": "marketing-crm",
    "purpose": "Journeys running",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-774",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-774"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-775",
  "name": "Visual Journey Builder",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "02",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/visual-journey-builder-bo-775",
   "component": "apps/venue-management-web/src/routes/engagement-support/VisualJourneyBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-774"
   ],
   "exitTo": [
    "BO-774"
   ],
   "transitions": [
    {
     "to": "BO-774",
     "trigger": "Back to Journey Automation Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create multi-step journeys through a visual no-code canvas. Provide trigger, audience, decision, wait, message, offer, case, task, webhook and goal nodes. Support branches, merges, reusable subflows, annotations, zoom, validation and realistic test execution. Show node configuration, eligible count, dependencies and errors without leaving the canvas. Version drafts, compare changes and require approval before a published journey is replaced. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**Visual Journey Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 26"
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
       "impliedBy": "createJourney",
       "label": "Create journey",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createJourney"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Starts enrolling guests who match**, from now. Guests already in the journey continue on the version they entered.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The visual journey list.",
   "error": "Could not load. Names which read failed and leaves the visual journey untouched.",
   "emptyFirstRun": "No visual journey yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visual journey are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createJourney",
    "contract": "marketing-crm",
    "purpose": "Build a journey",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "activateJourney",
    "contract": "marketing-crm",
    "purpose": "Activate it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-775",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-775"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "journeyId",
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
  "id": "BO-776",
  "name": "Trigger Event Catalog",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "03",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/trigger-event-catalog-bo-776",
   "component": "apps/venue-management-web/src/routes/engagement-support/TriggerEventCatalog.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-774"
   ],
   "exitTo": [
    "BO-774"
   ],
   "transitions": [
    {
     "to": "BO-774",
     "trigger": "Back to Journey Automation Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern the events that can start, update or stop a journey. Configure purchase, cart abandonment, first visit, membership expiry, loyalty milestone, wallet top-up, birthday, reservation and case events. Configuration Scope of Work | Version 1.0 26 Define source, event schema, required attributes, deduplication, freshness, eligibility and sample payload. Support API/webhook events and scheduled conditions with authentication and retry controls. Version and test event definitions and display consuming journeys before deactivation or change. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 26"
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
       "impliedBy": "listMessageTriggers",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
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
   "loading": "The trigger event catalog list.",
   "error": "Could not load. Names which read failed and leaves the trigger event catalog untouched.",
   "emptyFirstRun": "No trigger event catalog yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the trigger event catalog are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMessageTriggers",
    "contract": "marketing-crm",
    "purpose": "The trigger catalogue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setMessageTrigger",
    "contract": "marketing-crm",
    "purpose": "Define one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-776",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-776"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-777",
  "name": "Decision Logic & Timing",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "04",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/decision-logic-timing-bo-777",
   "component": "apps/venue-management-web/src/routes/engagement-support/DecisionLogicTiming.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-774"
   ],
   "exitTo": [
    "BO-774"
   ],
   "transitions": [
    {
     "to": "BO-774",
     "trigger": "Back to Journey Automation Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control journey branching, timing and re-entry. Build nested AND/OR conditions using guest, event, segment, transaction, product, channel and engagement data. Configure waits, dates, timezones, send windows, blackout periods, frequency limits and expiry. Define re-entry, concurrency, suppression, exit and goal conditions and behavior when data is missing. Simulate paths for representative guests and block publication when a branch has no safe outcome. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 27"
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
       "impliedBy": "createJourney",
       "label": "Create journey",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createJourney"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The decision logic timing list.",
   "error": "Could not load. Names which read failed and leaves the decision logic timing untouched.",
   "emptyFirstRun": "No decision logic timing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the decision logic timing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createJourney",
    "contract": "marketing-crm",
    "purpose": "Decision logic and timing",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-777",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-777"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-778",
  "name": "Abandoned Cart Recovery",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "05",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/abandoned-cart-recovery-bo-778",
   "component": "apps/venue-management-web/src/routes/engagement-support/AbandonedCartRecovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-774"
   ],
   "exitTo": [
    "BO-774"
   ],
   "transitions": [
    {
     "to": "BO-774",
     "trigger": "Back to Journey Automation Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure automated recovery of incomplete ticketing and commerce transactions. Define abandonment event, cart-value threshold, product/inventory checks, eligibility and recovery window. Configure staged reminders across email, SMS, WhatsApp and push with fallback and frequency limits. Apply approved incentives through the Promotion Engine and prevent discount leakage or expired inventory offers. Track recovered cart, revenue, margin, attribution and exit when purchase or cancellation occurs. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 27"
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
       "impliedBy": "listAbandonedCarts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The abandoned cart recovery list.",
   "error": "Could not load. Names which read failed and leaves the abandoned cart recovery untouched.",
   "emptyFirstRun": "No abandoned cart recovery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the abandoned cart recovery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAbandonedCarts",
    "contract": "orders",
    "purpose": "Carts that lapsed without checking out",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-778",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-778"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-779",
  "name": "Lifecycle Journeys",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "06",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/lifecycle-journeys-bo-779",
   "component": "apps/venue-management-web/src/routes/engagement-support/LifecycleJourneys.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-774"
   ],
   "exitTo": [
    "BO-774"
   ],
   "transitions": [
    {
     "to": "BO-774",
     "trigger": "Back to Journey Automation Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage reusable membership, loyalty and wallet lifecycle automations. Provide onboarding, benefit-awareness, renewal, expiry, lapse, freeze and upgrade membership journeys. Provide loyalty enrollment, tier movement, milestone, reward availability and points-expiry journeys. Provide wallet onboarding, top-up, low-balance, dormancy and bonus-credit journeys. Configure eligibility, channels, goals, stop conditions, ownership, versions and lifecycle-specific KPIs. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 27",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 27"
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
       "impliedBy": "createJourney",
       "label": "Create journey",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createJourney"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lifecycle journeys list.",
   "error": "Could not load. Names which read failed and leaves the lifecycle journeys untouched.",
   "emptyFirstRun": "No lifecycle journeys yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the lifecycle journeys are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createJourney",
    "contract": "marketing-crm",
    "purpose": "Lifecycle journeys",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-779",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-779"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-780",
  "name": "Guest Engagement Journeys",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "07",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/guest-engagement-journeys-bo-780",
   "component": "apps/venue-management-web/src/routes/engagement-support/GuestEngagementJourneys.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-774"
   ],
   "exitTo": [
    "BO-774"
   ],
   "transitions": [
    {
     "to": "BO-774",
     "trigger": "Back to Journey Automation Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure recurring guest relationship journeys. Support birthdays, anniversaries, welcome/onboarding, first-visit follow-up, inactivity and re- engagement. Personalize by profile, language, interests, visit history, loyalty, membership and preferred channel. Apply quiet hours, consent, frequency and household/minor rules before every communication. Measure engagement, conversion, return visits, retention and incremental value by journey. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 28"
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
       "bindsTo": "Journey",
       "operation": "listJourneys",
       "derived": true,
       "impliedBy": "listJourneys",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest engagement journeys list.",
   "error": "Could not load. Names which read failed and leaves the guest engagement journeys untouched.",
   "emptyFirstRun": "No guest engagement journeys yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest engagement journeys are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listJourneys",
    "contract": "marketing-crm",
    "purpose": "Every guest engagement journey",
    "trigger": "onLoad",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-780",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-780"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-781",
  "name": "Cross-Sell & Service Recovery",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "08",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/cross-sell-service-recovery-bo-781",
   "component": "apps/venue-management-web/src/routes/engagement-support/CrossSellServiceRecovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-774"
   ],
   "exitTo": [
    "BO-774"
   ],
   "transitions": [
    {
     "to": "BO-774",
     "trigger": "Back to Journey Automation Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Coordinate revenue-growth and recovery actions after guest events. Recommend and automate eligible cross-sell or upsell offers after purchase, booking or visit. Trigger reservation follow-up, survey request, complaint recovery and post-case resolution journeys. Create cases, tasks, refunds, vouchers, loyalty points or wallet credit subject to approval limits. Stop or alter a journey when sentiment, case status, refund, opt-out or service outcome changes. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 28"
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
       "impliedBy": "getJourneyPerformance",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-sell service recovery list.",
   "error": "Could not load. Names which read failed and leaves the cross-sell service recovery untouched.",
   "emptyFirstRun": "No cross-sell service recovery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-sell service recovery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getJourneyPerformance",
    "contract": "marketing-crm",
    "purpose": "Journey analytics",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-781",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-781"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "journeyId",
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
  "id": "BO-782",
  "name": "AI Journey Optimization",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "09",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/ai-journey-optimization-bo-782",
   "component": "apps/venue-management-web/src/routes/engagement-support/AiJourneyOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-774"
   ],
   "exitTo": [
    "BO-774"
   ],
   "transitions": [
    {
     "to": "BO-774",
     "trigger": "Back to Journey Automation Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use explainable AI to improve paths, content, offers and timing. Recommend branch order, wait duration, channel, message, offer and send time with expected uplift. Display supporting evidence, confidence, affected audience, risks and policy constraints. Allow scenario comparison, selective approval and rollback and prevent AI from editing live journeys directly. Monitor applied recommendation results and retain model/version, reviewer feedback and realized impact. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 28"
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
       "impliedBy": "listJourneys",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "decideAiInsight",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideAiInsight"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The journey optimization list.",
   "error": "Could not load. Names which read failed and leaves the journey optimization untouched.",
   "emptyFirstRun": "No journey optimization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the journey optimization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listJourneys",
    "contract": "marketing-crm",
    "purpose": "Automated journeys",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMarketingRecommendations",
    "contract": "ai",
    "purpose": "AI recommendations on this campaign or journey, with expected impact and evidence",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideAiInsight",
    "contract": "ai",
    "purpose": "Accept, reject or mark a campaign or journey recommendation actioned",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "Send-time suggestion (kind sendTime): best hour and channel per recipient",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-782",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-782"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "insightId",
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
  "id": "BO-783",
  "name": "Journey Analytics & Audit",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "5",
   "number": "10",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/journey-analytics-audit-bo-783",
   "component": "apps/venue-management-web/src/routes/engagement-support/JourneyAnalyticsAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-774"
   ],
   "exitTo": [
    "BO-774"
   ],
   "transitions": [
    {
     "to": "BO-774",
     "trigger": "Back to Journey Automation Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure journey behavior at node and end-goal level. Show triggered, eligible, enrolled, reached, clicked, converted, exited and failed stages. Analyze node drop-off, branch performance, time-to-conversion, revenue, attribution and cost. Provide error log, delivery trace, suppression reason, version comparison and guest-level path where authorized. Audit creation, edits, approvals, publication, pauses, AI recommendations and administrative actions. Configuration Scope of Work | Version 1.0 28 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 29 Board 6 - Newsletter, Notifications & Message Delivery Figure 6. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 30",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 28"
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
       "impliedBy": "listJourneys",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The journey analytics audit list.",
   "error": "Could not load. Names which read failed and leaves the journey analytics audit untouched.",
   "emptyFirstRun": "No journey analytics audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the journey analytics audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listJourneys",
    "contract": "marketing-crm",
    "purpose": "Automated journeys",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-783",
   "workshopBoard": "wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-783"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "activateJourney": {
  "method": "POST",
  "path": "/journeys/{journeyId}/activate",
  "contract": "marketing-crm",
  "summary": "Start it, or stop it",
  "permission": "MARKETING_SEND",
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
  "responds": "Journey"
 },
 "createJourney": {
  "method": "POST",
  "path": "/journeys",
  "contract": "marketing-crm",
  "summary": "Define an automated journey",
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
  "requestBody": "Journey",
  "responds": "Journey"
 },
 "decideAiInsight": {
  "method": "POST",
  "path": "/insights/{insightId}/decide",
  "contract": "ai",
  "summary": "Review, accept, reject or mark an insight actioned",
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
  "responds": "AiInsight"
 },
 "getJourneyPerformance": {
  "method": "GET",
  "path": "/journeys/{journeyId}/performance",
  "contract": "marketing-crm",
  "summary": "Entrants, completions, goals reached",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "JourneyPerformance"
 },
 "listAbandonedCarts": {
  "method": "GET",
  "path": "/carts/abandoned",
  "contract": "orders",
  "summary": "Carts that lapsed without checking out",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "since",
    "in": "query",
    "required": null
   },
   {
    "name": "minValue",
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
 "listJourneys": {
  "method": "GET",
  "path": "/journeys",
  "contract": "marketing-crm",
  "summary": "Automated journeys",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "listMarketingRecommendations": {
  "method": "GET",
  "path": "/marketing-recommendations",
  "contract": "ai",
  "summary": "Recommendations on marketing campaigns and journeys",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "targetKind",
    "in": "query",
    "required": true
   },
   {
    "name": "targetRef",
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
 "listMessageTriggers": {
  "method": "GET",
  "path": "/message-triggers",
  "contract": "marketing-crm",
  "summary": "What fires a message, and when",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "requestSuggestion": {
  "method": "POST",
  "path": "/ai/suggestions",
  "contract": "ai",
  "summary": "Ask for an answer, however it is currently produced",
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
  "responds": "Suggestion"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AbandonedCart": {
  "type": "object",
  "x-ticvai-persistence": "none — a projection of orders.cart",
  "properties": {
   "cartId": {
    "type": "string",
    "format": "uuid"
   },
   "token": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "hasContactPoint": {
    "type": "boolean",
    "description": "**An anonymous cart with no email cannot be recovered.** Worth counting, because it sizes what a sign-in prompt earlier in the journey would be worth.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "lineCount": {
    "type": "integer"
   },
   "value": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "topProductName": {
    "type": "string"
   },
   "abandonedAt": {
    "type": "string",
    "format": "date-time"
   },
   "remindersSent": {
    "type": "integer"
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
 "AiInsight": {
  "type": "object",
  "x-ticvai-persistence": "ai.insight",
  "description": "**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).",
  "required": [
   "kind",
   "title",
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
     "anomaly",
     "forecastDeviation",
     "trend",
     "opportunity",
     "executiveSummary",
     "rootCause",
     "forecastThreshold",
     "marketingRecommendation"
    ]
   },
   "detectorId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.anomaly_detector"
   },
   "metricKey": {
    "type": "string",
    "nullable": true
   },
   "subjectKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "campaign",
     "journey",
     "forecastDefinition",
     "venue"
    ],
    "description": "What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."
   },
   "subjectRef": {
    "type": "string",
    "nullable": true
   },
   "recommendedAction": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."
   },
   "expectedImpact": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."
   },
   "title": {
    "type": "string"
   },
   "narrative": {
    "type": "string",
    "nullable": true
   },
   "evidence": {
    "$ref": "#/components/schemas/AiEvidenceItemList"
   },
   "magnitude": {
    "type": "number",
    "nullable": true
   },
   "priority": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "correlationKey": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "new",
     "reviewed",
     "accepted",
     "rejected",
     "actioned",
     "measured"
    ],
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
   "actionRef": {
    "type": "string",
    "nullable": true
   },
   "measuredImpact": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "detectedAt": {
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
 "AiMarketingRecommendation": {
  "type": "object",
  "x-ticvai-persistence": "none — read from ai.insight (kind marketingRecommendation)",
  "description": "One recommendation on a campaign or journey (22.1.16, 22.3.17), decided through `decideAiInsight` and applied by a person in marketing-crm.",
  "required": [
   "insightId",
   "targetKind",
   "targetRef",
   "recommendation",
   "status"
  ],
  "properties": {
   "insightId": {
    "type": "string",
    "format": "uuid",
    "description": "The `ai.insight` row; `decideAiInsight` takes it."
   },
   "targetKind": {
    "type": "string",
    "enum": [
     "campaign",
     "journey"
    ]
   },
   "targetRef": {
    "type": "string"
   },
   "recommendation": {
    "type": "string",
    "enum": [
     "changeSegment",
     "changeChannel",
     "changeTiming",
     "changeOffer",
     "changeContent",
     "addStep",
     "removeStep",
     "reorderSteps",
     "startJourneyFromTemplate"
    ]
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "What to change to, e.g. the channel, the send hour, the step to drop."
   },
   "expectedImpact": {
    "type": "object",
    "nullable": true,
    "properties": {
     "metric": {
      "type": "string"
     },
     "low": {
      "type": "number"
     },
     "high": {
      "type": "number"
     }
    },
    "description": "A range on the named metric (conversion, open rate, revenue), never a single number (design 5.6)."
   },
   "rationale": {
    "type": "string"
   },
   "evidence": {
    "$ref": "#/components/schemas/AiEvidenceItemList"
   },
   "priority": {
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
     "new",
     "reviewed",
     "accepted",
     "rejected",
     "actioned",
     "measured"
    ]
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time"
   }
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
 "Journey": {
  "type": "object",
  "x-ticvai-persistence": "marketing.journey + marketing.journey_step",
  "description": "22.3.1b to 22.3.10b, CF-137. **A journey is a sequence with branches; a `MessageTrigger` is one step of it.** The trigger already handles *\"send this when that happens\"* — a journey is what you need when the next message depends on what the guest did about the last one.\nFive of the ten requirements are named lifecycles — abandoned cart, membership, loyalty, wallet, birthday. **They are not five features.** Each is a journey with a different entry event and a different set of steps, which is why this is one entity and a template library rather than five contracts.\n**Consent is checked at every send, not at entry.** A guest who opts out mid-journey stops receiving, and the journey does not need to know — the same rule `MessageTrigger` follows and the one PDPL Article 17(1) makes unconditional.\n",
  "required": [
   "id",
   "name",
   "entryEvent",
   "status",
   "steps"
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
   "templateKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "abandonedCart",
     "membershipLifecycle",
     "loyaltyLifecycle",
     "walletLifecycle",
     "birthday",
     "onboarding",
     "winBack",
     "custom"
    ],
    "description": "Which named lifecycle this implements. **Set for reporting and for the library**, not for behaviour — the steps decide what happens.\n"
   },
   "entryEvent": {
    "type": "string",
    "description": "22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes.\n"
   },
   "entryConditions": {
    "type": "object",
    "nullable": true,
    "description": "Narrows entry — a segment, a tier, a venue. **Evaluated once at entry**, unlike step conditions.\n"
   },
   "steps": {
    "type": "array",
    "description": "22.3.1b. What the builder produces. **The visual builder is a frontend over this** — the contract holds the graph and the canvas is a rendering of it.\n",
    "items": {
     "$ref": "#/components/schemas/JourneyStep"
    }
   },
   "status": {
    "readOnly": true,
    "type": "string",
    "enum": [
     "draft",
     "active",
     "paused",
     "archived"
    ]
   },
   "maxDurationDays": {
    "type": "integer",
    "default": 30,
    "description": "**A journey with no end is a guest who never leaves it.** After this, entrants exit wherever they are.\n"
   },
   "reentryPolicy": {
    "type": "string",
    "enum": [
     "never",
     "afterCompletion",
     "always"
    ],
    "default": "afterCompletion",
    "description": "22.3.6b. **Abandoned cart is the case that needs this.** A guest who abandons three carts in an hour should not get three recovery sequences, and `never` is wrong too — they may genuinely abandon one next month.\n"
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "JourneyPerformance": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from marketing.journey_enrollment",
  "required": [
   "journeyId",
   "entrants"
  ],
  "properties": {
   "journeyId": {
    "type": "string",
    "format": "uuid"
   },
   "entrants": {
    "type": "integer",
    "description": "Everyone who entered, in any status."
   },
   "byStatus": {
    "type": "object",
    "description": "Entrants per `JourneyEntrant.status`.",
    "properties": {
     "active": {
      "type": "integer"
     },
     "paused": {
      "type": "integer"
     },
     "completed": {
      "type": "integer"
     },
     "exited": {
      "type": "integer"
     },
     "suppressed": {
      "type": "integer"
     }
    }
   },
   "goalReached": {
    "type": "integer",
    "description": "**The number that matters.** Entrants who left at a step of kind `goal` — their `JourneyEntrant.stepId` when they exited.\n"
   },
   "goalRate": {
    "type": "number",
    "nullable": true,
    "description": "`goalReached` over `entrants`. Null while there are no entrants."
   }
  }
 },
 "JourneyStep": {
  "type": "object",
  "description": "One node. **A step either sends, waits, or branches** — three kinds rather than a general graph, because a marketing user drawing an arbitrary graph draws a loop.\n",
  "required": [
   "id",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "x-ticvai-column": "type",
    "enum": [
     "send",
     "wait",
     "branch",
     "exit",
     "goal"
    ]
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-column": "message_template_id",
    "description": "For `send`. Channel is resolved from the guest's preference at the moment of sending."
   },
   "sendTimeMode": {
    "type": "string",
    "enum": [
     "fixed",
     "optimised"
    ],
    "default": "fixed",
    "description": "For `send` (29 September, build pass, group G2; 22.3.19). `optimised` delays the send, after the step is reached, to the recipient's suggested hour from `ai.requestSuggestion` (kind `sendTime`) within the next 24 hours and inside `waitUntil`; no suggestion or AI off sends at once, as `fixed`."
   },
   "channelMode": {
    "type": "string",
    "enum": [
     "preference",
     "optimised"
    ],
    "default": "preference",
    "description": "For `send`. `optimised` tries first the consented channel the send-time suggestion names, then `channelPreference` in order (22.9.16)."
   },
   "channelPreference": {
    "type": "array",
    "nullable": true,
    "description": "22.3.3b. Ordered fallback — email, then SMS, then push. **A guest with no email address does not get an email step**, and the step does not fail, it moves down the list.\n",
    "items": {
     "type": "string",
     "enum": [
      "email",
      "sms",
      "whatsapp",
      "push",
      "inApp"
     ]
    }
   },
   "waitMinutes": {
    "type": "integer",
    "nullable": true
   },
   "waitUntil": {
    "type": "object",
    "nullable": true,
    "description": "22.3.5b. **Business hours, time zone and blackout windows** — a wallet low-balance alert at 3am is a complaint, and the venue's quiet hours are venue configuration rather than a property of this step.\n",
    "properties": {
     "businessHoursOnly": {
      "type": "boolean",
      "default": false
     },
     "timezone": {
      "type": "string",
      "nullable": true
     },
     "respectQuietHours": {
      "type": "boolean",
      "default": true
     },
     "notBefore": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "condition": {
    "type": "object",
    "nullable": true,
    "description": "22.3.4b. IF/THEN over guest profile, behaviour and prior steps. **The most common condition is whether the previous message worked** — a recovery sequence must stop when the guest buys.\n",
    "properties": {
     "field": {
      "type": "string"
     },
     "operator": {
      "type": "string",
      "enum": [
       "eq",
       "neq",
       "gt",
       "lt",
       "contains",
       "exists",
       "notExists"
      ]
     },
     "value": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "onTrue": {
    "type": "string",
    "nullable": true,
    "description": "Next step id."
   },
   "onFalse": {
    "type": "string",
    "nullable": true
   },
   "next": {
    "type": "string",
    "nullable": true,
    "x-ticvai-column": "next_journey_step_id"
   },
   "goalEvent": {
    "type": "string",
    "nullable": true,
    "description": "For `goal`. **The event that means this journey worked and the guest should leave it** — a purchase for abandoned cart, a renewal for membership. **Reaching a goal exits immediately**, which is what stops a recovered cart from being chased.\n"
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
    "description": "The platform event that fires it — `order.completed`, `access.validated`, `queue.turnApproaching`. **Named from the event catalogue** (`BusinessEvent.eventType`), so a trigger cannot bind to something nothing publishes. Its conditions are `MessageTriggerCondition` rows.\n**`entitlement.expiringSoon` is in the catalogue since 29 September** (build pass, group G2; 5.5.30): the pre-expiry reminder for a ticket or pass. Its anchor is the event time; the notice period is the template's `expiryNoticeDays`, so `offsetMinutes` is normally 0.\n"
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
   "sendTimeMode": {
    "type": "string",
    "enum": [
     "fixed",
     "optimised"
    ],
    "default": "fixed",
    "description": "**Only for `priority` `marketing`** (29 September, build pass, group G2; 22.9.16): `optimised` holds the notification to the recipient's suggested hour from `ai.requestSuggestion` (kind `sendTime`) within the next 24 hours, on the suggested consented channel. `operational` and `transactional` messages are never delayed for it, and a `setMessageTrigger` asking for it on them is refused (400)."
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
 "Suggestion": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion",
  "description": "One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n",
  "required": [
   "id",
   "kind",
   "basis",
   "maturity",
   "producedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/SuggestionKind"
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "scopePath": {
    "type": "string"
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "What it is about — a product, an outlet, an item, a party."
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "description": "The suggestion itself. Shape depends on `kind`."
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1,
    "description": "**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"
   },
   "explanation": {
    "type": "string",
    "description": "**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"
   },
   "inputs": {
    "type": "object",
    "additionalProperties": true,
    "description": "What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"
   },
   "producerRef": {
    "type": "string",
    "description": "The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"
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
