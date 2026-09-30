# WS130 — Event Management Configuration Backend Structure v1.0 board 6

**6 screens · 5 operations · 5 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `EVENT_CONFIGURE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-710` | Event Resource Command Center | listDetail | 1 | 0 | — |
| `BO-711` | Event Resource Requirement Configuration | listDetail | 1 | 0 | — |
| `BO-712` | Staff & Role Assignment Configuration | listDetail | 2 | 0 | — |
| `BO-713` | Contractor & External Workforce Configuration | listDetail | 1 | 0 | — |
| `BO-714` | Event Shift & Roster Configuration | listDetail | 2 | 0 | — |
| `BO-715` | Resource Location & Deployment Configuration | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-710, BO-711, BO-712, BO-713, BO-714, BO-715 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-710",
  "name": "Event Resource Command Center",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "01",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/event-resource-command-center-bo-710",
   "component": "apps/venue-management-web/src/routes/sell/EventResourceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-711",
    "BO-712",
    "BO-713",
    "BO-714",
    "BO-715"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-711",
     "trigger": "Event Resource Requirement Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-712",
     "trigger": "Staff & Role Assignment Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-713",
     "trigger": "Contractor & External Workforce Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-714",
     "trigger": "Event Shift & Roster Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-715",
     "trigger": "Resource Location & Deployment Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide management with a consolidated backend view of the financial, commercial, sponsorship, attendance and operational performance of events.",
  "purposeNote": "Authorized users can obtain a consolidated view of event commercial and operational performance while data visibility remains controlled by tenant, entity and role permissions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 81"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 81"
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
       "impliedBy": "getEventResourcePlan",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event resource list.",
   "error": "Could not load. Names which read failed and leaves the event resource untouched.",
   "emptyFirstRun": "No event resource yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event resource are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEventResourcePlan",
    "contract": "catalogue",
    "purpose": "The resource plan",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-710",
   "workshopBoard": "wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-710"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 81. 0 of 0 labels bound to a contract property; 0 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "eventId",
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
  "id": "BO-711",
  "name": "Event Resource Requirement Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "02",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/event-resource-requirement-configuration-bo-711",
   "component": "apps/venue-management-web/src/routes/sell/EventResourceRequirementConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-710"
   ],
   "exitTo": [
    "BO-710"
   ],
   "transitions": [
    {
     "to": "BO-710",
     "trigger": "Back to Event Resource Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the financial plan and budget against which event performance will be measured.",
  "purposeNote": "Administrators can create an event-level financial plan and compare budget, commitments, actuals and forecasts using data referenced from the shared Finance services.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 82"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 82"
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
       "impliedBy": "setEventResourcePlan",
       "label": "Save event resource plan",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventResourcePlan"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event resource requirement list.",
   "error": "Could not load. Names which read failed and leaves the event resource requirement untouched.",
   "emptyFirstRun": "No event resource requirement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event resource requirement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventResourcePlan",
    "contract": "catalogue",
    "purpose": "What the event needs",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getEventResourcePlan"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-711",
   "workshopBoard": "wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-711"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 82. 0 of 0 labels bound to a contract property; 0 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "eventId",
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
  "id": "BO-712",
  "name": "Staff & Role Assignment Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "03",
   "page": 83
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/staff-role-assignment-configuration-bo-712",
   "component": "apps/venue-management-web/src/routes/sell/StaffRoleAssignmentConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-710"
   ],
   "exitTo": [
    "BO-710"
   ],
   "transitions": [
    {
     "to": "BO-710",
     "trigger": "Back to Event Resource Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define how financial performance should be measured and attributed to an event.",
  "purposeNote": "The system provides traceable event profitability using configured financial attribution rules without duplicating the underlying accounting ledger.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 83"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 83"
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
       "impliedBy": "setEventResourcePlan",
       "label": "Save event resource plan",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEventResourcePlan"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staff role list.",
   "error": "Could not load. Names which read failed and leaves the staff role untouched.",
   "emptyFirstRun": "No staff role yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the staff role are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventResourcePlan",
    "contract": "catalogue",
    "purpose": "Staff and roles",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getEventResourcePlan"
    ]
   },
   {
    "operationId": "createRotaAssignment",
    "contract": "workforce",
    "purpose": "Roster them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRotaAssignments",
     "getStaffingCoverage"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-712",
   "workshopBoard": "wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-712"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 83. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "eventId",
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
  "id": "BO-713",
  "name": "Contractor & External Workforce Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "04",
   "page": 84
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/contractor-external-workforce-configuration-bo-713",
   "component": "apps/venue-management-web/src/routes/sell/ContractorExternalWorkforceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-710"
   ],
   "exitTo": [
    "BO-710"
   ],
   "transitions": [
    {
     "to": "BO-710",
     "trigger": "Back to Event Resource Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Manage sponsors and sponsorship agreements associated with events.",
  "purposeNote": "Administrators can associate sponsorship agreements and deliverables with an event and track fulfillment against contractual commitments.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 84 §Track"
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
       "label": "Every contractor external workforce",
       "columns": [
        "Contracted → Scheduled → Delivered → Verified"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 84 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected contractor external workforce",
       "bindsTo": null,
       "columns": [
        "Contracted → Scheduled → Delivered → Verified"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Sponsorship levels may include”.",
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 84 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The contractor external workforce list.",
   "error": "Could not load. Names which read failed and leaves the contractor external workforce untouched.",
   "emptyFirstRun": "No contractor external workforce yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the contractor external workforce are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventResourcePlan",
    "contract": "catalogue",
    "purpose": "Contractors and external workforce",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getEventResourcePlan"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Contracted → Scheduled → Delivered → Verified"
   ],
   "params": [
    {
     "name": "eventId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-713",
   "workshopBoard": "wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-713"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 84. 0 of 1 labels bound to a contract property; 1 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-714",
  "name": "Event Shift & Roster Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "06",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/event-shift-roster-configuration-bo-714",
   "component": "apps/venue-management-web/src/routes/sell/EventShiftRosterConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-710"
   ],
   "exitTo": [
    "BO-710"
   ],
   "transitions": [
    {
     "to": "BO-710",
     "trigger": "Back to Event Resource Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow authorized administrators to use AI to accelerate creation of event configuration from natural-language instructions or existing templates.",
  "purposeNote": "AI can accelerate event setup while every proposed configuration remains reviewable, editable, permission-controlled and subject to normal approval workflows.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85 §Display"
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
       "label": "Every event shift roster",
       "columns": [
        "AI Proposal",
        "Existing / Approved Configuration"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected event shift roster",
       "bindsTo": null,
       "columns": [
        "AI Proposal",
        "Existing / Approved Configuration"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Administrators can”, “Critical Governance Principle”.",
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event shift roster list.",
   "error": "Could not load. Names which read failed and leaves the event shift roster untouched.",
   "emptyFirstRun": "No event shift roster yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event shift roster are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setShiftTemplate",
    "contract": "workforce",
    "purpose": "Event shifts",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listShiftTemplates"
    ]
   },
   {
    "operationId": "getStaffingCoverage",
    "contract": "workforce",
    "purpose": "Where it is short",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "AI Proposal",
    "Existing / Approved Configuration"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-714",
   "workshopBoard": "wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-714"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 85. 0 of 2 labels bound to a contract property; 2 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-715",
  "name": "Resource Location & Deployment Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "07",
   "page": 86
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/resource-location-deployment-configuration-bo-715",
   "component": "apps/venue-management-web/src/routes/sell/ResourceLocationDeploymentConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-710"
   ],
   "exitTo": [
    "BO-710"
   ],
   "transitions": [
    {
     "to": "BO-710",
     "trigger": "Back to Event Resource Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Configure KPI by; Display) and no metric row",
  "purpose": "Configure measurable operational KPIs for staff, instructors and activity operators.",
  "purposeNote": "Administrators can define measurable operator/instructor KPIs and calculate performance using traceable operational records from completed sessions.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 86 §Display"
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
       "label": "Every resource location deployment",
       "columns": [
        "Target vs Actual"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 86 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource location deployment",
       "bindsTo": null,
       "columns": [
        "Target vs Actual"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Set”.",
       "provenance": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 86 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource location deployment list.",
   "error": "Could not load. Names which read failed and leaves the resource location deployment untouched.",
   "emptyFirstRun": "No resource location deployment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource location deployment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventResourcePlan",
    "contract": "catalogue",
    "purpose": "Deployment by location",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getEventResourcePlan"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Target vs Actual"
   ],
   "params": [
    {
     "name": "eventId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-715",
   "workshopBoard": "wireframes/WS53 Event Management Configuration Backend Structure v1.0 Board 6.dc.html#bo-715"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 86. 0 of 1 labels bound to a contract property; 1 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createRotaAssignment": {
  "method": "POST",
  "path": "/rota-assignments",
  "contract": "workforce",
  "summary": "Put someone on the rota",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "RotaAssignment",
  "responds": "RotaAssignment"
 },
 "getEventResourcePlan": {
  "method": "GET",
  "path": "/events/{eventId}/resource-plan",
  "contract": "catalogue",
  "summary": "Everything an event needs, and whether it has been secured",
  "permission": "EVENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EventResourcePlan"
 },
 "getStaffingCoverage": {
  "method": "GET",
  "path": "/staffing-coverage",
  "contract": "workforce",
  "summary": "Where the rota is short, and by how much",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "basis",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "StaffingCoverage"
 },
 "setEventResourcePlan": {
  "method": "PUT",
  "path": "/events/{eventId}/resource-plan",
  "contract": "catalogue",
  "summary": "State what the event needs, by role and by kind",
  "permission": "EVENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "EventResourcePlan",
  "responds": "EventResourcePlan"
 },
 "setShiftTemplate": {
  "method": "PUT",
  "path": "/shift-templates",
  "contract": "workforce",
  "summary": "Define a shift pattern, its breaks and its qualifications",
  "permission": "WORKFORCE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ShiftTemplate",
  "responds": "ShiftTemplate"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "EventResourcePlan": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.event_resource_plan",
  "description": "Event board 6. **Secured against required is the only number an event manager wants.**\n",
  "properties": {
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "requirements": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "kind": {
       "type": "string",
       "enum": [
        "space",
        "equipment",
        "staff",
        "contractor",
        "vehicle",
        "service"
       ]
      },
      "resourceTypeId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "roleCode": {
       "type": "string",
       "nullable": true
      },
      "quantity": {
       "type": "integer"
      },
      "from": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "to": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "locationScopePath": {
       "type": "string",
       "nullable": true
      },
      "securedCount": {
       "type": "integer",
       "readOnly": true
      },
      "status": {
       "type": "string",
       "enum": [
        "required",
        "partiallySecured",
        "secured",
        "atRisk"
       ]
      },
      "bookingIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "contractors": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "organisationId": {
       "type": "string",
       "format": "uuid"
      },
      "role": {
       "type": "string"
      },
      "headcount": {
       "type": "integer"
      },
      "accreditationProgrammeId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "insuranceVerified": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "readiness": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "notPlanned",
     "planning",
     "atRisk",
     "ready"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RotaAssignment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.rota_assignment",
  "required": [
   "principalId",
   "venueId",
   "startsAt",
   "endsAt",
   "position"
  ],
  "properties": {
   "overtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"
   },
   "restPeriodBefore": {
    "type": "integer",
    "nullable": true,
    "description": "Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"
   },
   "breachesWorkingHourLimit": {
    "type": "boolean",
    "default": false,
    "readOnly": true,
    "description": "**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"
   },
   "labourCost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "position": {
    "type": "string",
    "description": "What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"
   },
   "requiredRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "$ref": "#/components/schemas/RotaStatus"
   },
   "breakMinutes": {
    "type": "integer",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "RotaStatus": {
  "type": "string",
  "enum": [
   "planned",
   "published",
   "confirmed",
   "swapPending",
   "cancelled",
   "completed",
   "noShow"
  ]
 },
 "ShiftTemplate": {
  "type": "object",
  "x-ticvai-persistence": "workforce.shift_template",
  "description": "Resource board 3.7. **The unit a manager actually thinks in.**",
  "required": [
   "code",
   "name"
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
    "type": "string",
    "enum": [
     "early",
     "late",
     "middle",
     "split",
     "double",
     "night",
     "onCall",
     "overtime"
    ]
   },
   "startsAt": {
    "type": "string"
   },
   "endsAt": {
    "type": "string"
   },
   "breaks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "afterMinutes": {
       "type": "integer"
      },
      "minutes": {
       "type": "integer"
      },
      "paid": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "requiredQualifications": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "roleCode": {
    "type": "string",
    "nullable": true
   },
   "costCentre": {
    "type": "string",
    "nullable": true
   },
   "hourlyRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "StaffingCoverage": {
  "type": "object",
  "description": "Resource board 4.4. **The gap is the product.**",
  "properties": {
   "date": {
    "type": "string",
    "format": "date"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "positionCode": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "from": {
    "type": "string"
   },
   "to": {
    "type": "string"
   },
   "required": {
    "type": "integer"
   },
   "rostered": {
    "type": "integer"
   },
   "qualified": {
    "type": "integer",
    "description": "**A position filled by somebody not qualified for it is still a gap.**"
   },
   "gap": {
    "type": "integer"
   },
   "severity": {
    "type": "string",
    "enum": [
     "covered",
     "tight",
     "short",
     "blocking"
    ]
   },
   "openShiftIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "basisApplied": {
    "type": "string",
    "enum": [
     "minimum",
     "forecastRequirement"
    ],
    "description": "Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the period, `minimum`."
   },
   "minimumRequired": {
    "type": "integer",
    "nullable": true,
    "description": "The configured minimum for the position and window."
   },
   "forecastRequired": {
    "type": "number",
    "nullable": true,
    "description": "The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. Null where none was handed over."
   },
   "forecastRequiredP90": {
    "type": "number",
    "nullable": true,
    "description": "The busy-case requirement, for planning to the busy case."
   },
   "forecastVersionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it."
   }
  }
 }
}
```
