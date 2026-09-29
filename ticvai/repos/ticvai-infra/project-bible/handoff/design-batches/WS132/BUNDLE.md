# WS132 — Event Management Configuration Backend Structure v1.0 board 8

**4 screens · 4 operations · 3 schemas · 3 permissions**

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
  `PERFORMANCE_CONFIGURE, PRICE_CONFIGURE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-721` | Activity Performance & Slot Template Configuration | listDetail | 2 | 0 | — |
| `BO-722` | Prepaid Minute Package & Customer Balance Configuration | listDetail | 2 | 0 | — |
| `BO-723` | Peak, Off-Peak & Super Prime Time Configuration | listDetail | 1 | 0 | — |
| `BO-724` | Walk-In / There-and-Then Booking Configuration | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-721, BO-722, BO-723, BO-724 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-721",
  "name": "Activity Performance & Slot Template Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "02",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/activity-session-slot-template-configuration-bo-721",
   "component": "apps/venue-management-web/src/routes/sell/ActivitySessionSlotTemplateConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-722",
    "BO-723",
    "BO-724"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-722",
     "trigger": "Prepaid Minute Package & Customer Balance Configuration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-723",
     "trigger": "Peak, Off-Peak & Super Prime Time Configuration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-724",
     "trigger": "Walk-In / There-and-Then Booking Configuration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
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
       "impliedBy": "setPerformanceTemplate",
       "label": "Save session template",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPerformanceTemplates",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setPerformanceTemplate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The activity session slot list.",
   "error": "Could not load. Names which read failed and leaves the activity session slot untouched.",
   "emptyFirstRun": "No activity session slot yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the activity session slot are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPerformanceTemplate",
    "contract": "catalogue",
    "purpose": "Slot templates",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPerformanceTemplates"
    ]
   },
   {
    "operationId": "listPerformanceTemplates",
    "contract": "catalogue",
    "purpose": "Templates in use",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-721",
   "workshopBoard": "wireframes/WS55 Event Management Configuration Backend Structure v1.0 Board 8.dc.html#bo-721"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 82. 0 of 0 labels bound to a contract property; 0 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-722",
  "name": "Prepaid Minute Package & Customer Balance Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "05",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/prepaid-minute-package-customer-balance-configuration-bo-722",
   "component": "apps/venue-management-web/src/routes/sell/PrepaidMinutePackageCustomerBalanceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-721"
   ],
   "exitTo": [
    "BO-721"
   ],
   "transitions": [
    {
     "to": "BO-721",
     "trigger": "Back to Activity Performance & Slot Template Configuration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure dashboards used to measure event sales, attendance and check-in performance.",
  "purposeNote": "Authorized users can monitor configured sales and attendance KPIs with current check-in information supplied by shared Ticketing and Access Control services.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 85"
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
       "impliedBy": "setPrepaidMinutePackage",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCreditTypes",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setPrepaidMinutePackage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The prepaid minute package list.",
   "error": "Could not load. Names which read failed and leaves the prepaid minute package untouched.",
   "emptyFirstRun": "No prepaid minute package yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the prepaid minute package are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPrepaidMinutePackage",
    "contract": "catalogue",
    "purpose": "Prepaid minute packages",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listCreditTypes",
    "contract": "wallet",
    "purpose": "The credit type behind them",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-722",
   "workshopBoard": "wireframes/WS55 Event Management Configuration Backend Structure v1.0 Board 8.dc.html#bo-722"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 85. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-723",
  "name": "Peak, Off-Peak & Super Prime Time Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "07",
   "page": 86
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/peak-off-peak-super-prime-time-configuration-bo-723",
   "component": "apps/venue-management-web/src/routes/sell/PeakOffPeakSuperPrimeTimeConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-721"
   ],
   "exitTo": [
    "BO-721"
   ],
   "transitions": [
    {
     "to": "BO-721",
     "trigger": "Back to Activity Performance & Slot Template Configuration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
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
       "label": "Every peak off-peak super",
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
       "label": "The selected peak off-peak super",
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
   "loading": "The peak off-peak super list.",
   "error": "Could not load. Names which read failed and leaves the peak off-peak super untouched.",
   "emptyFirstRun": "No peak off-peak super yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the peak off-peak super are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPerformanceTemplate",
    "contract": "catalogue",
    "purpose": "Peak, off-peak and super prime",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPerformanceTemplates"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Target vs Actual"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-723",
   "workshopBoard": "wireframes/WS55 Event Management Configuration Backend Structure v1.0 Board 8.dc.html#bo-723"
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
 },
 {
  "id": "BO-724",
  "name": "Walk-In / There-and-Then Booking Configuration",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Event_Management_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "08",
   "page": 87
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/walk-in-there-and-then-booking-configuration-bo-724",
   "component": "apps/venue-management-web/src/routes/sell/WalkInThereAndThenBookingConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-721"
   ],
   "exitTo": [
    "BO-721"
   ],
   "transitions": [
    {
     "to": "BO-721",
     "trigger": "Back to Activity Performance & Slot Template Configuration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure automatic invoice generation for eligible event-related customers and commercial accounts.",
  "purposeNote": "Eligible event transactions can trigger automated invoice requests with complete event and customer references while financial posting remains controlled by Finance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 87"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Event_Management_Configuration_Backend_Structure_v1.0.pdf, page 87"
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
       "impliedBy": "setPerformanceTemplate",
       "label": "Save session template",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setPerformanceTemplate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The walk-in there-and-then booking list.",
   "error": "Could not load. Names which read failed and leaves the walk-in there-and-then booking untouched.",
   "emptyFirstRun": "No walk-in there-and-then booking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the walk-in there-and-then booking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPerformanceTemplate",
    "contract": "catalogue",
    "purpose": "Walk-in policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPerformanceTemplates"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-724",
   "workshopBoard": "wireframes/WS55 Event Management Configuration Backend Structure v1.0 Board 8.dc.html#bo-724"
  },
  "apisNote": "Regenerated 9 September 2026 from Event_Management_Configuration_Backend_Structure_v1.0.pdf page 87. 0 of 0 labels bound to a contract property; 0 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listCreditTypes": {
  "method": "GET",
  "path": "/credit-types",
  "contract": "wallet",
  "summary": "The kinds of value that may sit in a wallet",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CreditType"
 },
 "listPerformanceTemplates": {
  "method": "GET",
  "path": "/performance-templates",
  "contract": "catalogue",
  "summary": "Slot templates, peak bands and walk-in rules",
  "permission": "PERFORMANCE_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PerformanceTemplate"
 },
 "setPerformanceTemplate": {
  "method": "PUT",
  "path": "/performance-templates",
  "contract": "catalogue",
  "summary": "Define slot length, capacity, bands and walk-in policy",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "requestBody": "PerformanceTemplate",
  "responds": "PerformanceTemplate"
 },
 "setPrepaidMinutePackage": {
  "method": "PUT",
  "path": "/prepaid-minute-packages",
  "contract": "catalogue",
  "summary": "Time bought in advance and drawn down per visit",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "PrepaidMinutePackage",
  "responds": "PrepaidMinutePackage"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CreditType": {
  "type": "object",
  "x-ticvai-persistence": "wallet.credit_type",
  "description": "Board 1.6. **What value sits inside a wallet** — the second vocabulary, and the one the acceptance condition requires to be a table.\n",
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
   "category": {
    "type": "string",
    "enum": [
     "cash",
     "refund",
     "bonus",
     "promotional",
     "giftCard",
     "membership",
     "loyalty",
     "ride",
     "attraction",
     "redemption",
     "fnb",
     "retail",
     "parking",
     "event",
     "other"
    ]
   },
   "monetary": {
    "type": "boolean",
    "default": true,
    "description": "**Loyalty points are not money.** A non-monetary credit has a conversion rate to money or it cannot be spent, and treating points as currency puts them on the balance sheet.\n"
   },
   "conversionRate": {
    "type": "number",
    "nullable": true
   },
   "refundable": {
    "type": "boolean",
    "default": false,
    "description": "**Promotional credit is not refundable and cash credit is.** A venue that refunds promotional credit to a card has converted marketing spend into cash.\n"
   },
   "transferable": {
    "type": "boolean",
    "default": false
   },
   "expires": {
    "type": "boolean",
    "default": false
   },
   "validityDays": {
    "type": "integer",
    "nullable": true
   },
   "breakageEligible": {
    "type": "boolean",
    "default": false
   },
   "ledgerAccountCode": {
    "type": "string",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "PerformanceTemplate": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.performance_template",
  "description": "Event board 8. **An activity venue sells time, not seats.** Each slot the template produces is a Performance. Formerly `SessionTemplate` on `catalogue.session_template`: a session is a Performance (decided 28 September, audit R165).",
  "required": [
   "code"
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
   "spaceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "slotMinutes": {
    "type": "integer"
   },
   "turnaroundMinutes": {
    "type": "integer",
    "default": 0
   },
   "concurrentCapacity": {
    "type": "integer"
   },
   "bands": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "offPeak",
        "standard",
        "peak",
        "superPrime"
       ]
      },
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "from": {
       "type": "string"
      },
      "to": {
       "type": "string"
      },
      "priceMultiplier": {
       "type": "number",
       "nullable": true
      },
      "minuteMultiplier": {
       "type": "number",
       "nullable": true
      }
     }
    }
   },
   "walkIn": {
    "type": "object",
    "description": "**Configured, not assumed.** It decides whether a family turning up on a Sunday is turned away.\n",
    "properties": {
     "allowed": {
      "type": "boolean",
      "default": true
     },
     "heldBackPercent": {
      "type": "integer",
      "default": 0
     },
     "cutoffMinutesBefore": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "PrepaidMinutePackage": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.prepaid_minutes",
  "description": "Event board 8.2. **Minutes are a `wallet` credit type; this is the product that sells them.**\n",
  "required": [
   "code",
   "minutes"
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
   "minutes": {
    "type": "integer"
   },
   "price": {
    "x-ticvai-column": "list_price",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "creditTypeId": {
    "type": "string",
    "format": "uuid",
    "description": "The `wallet` credit type the minutes are issued into."
   },
   "roundingMinutes": {
    "type": "integer",
    "default": 1
   },
   "minimumDrawMinutes": {
    "type": "integer",
    "default": 0
   },
   "bandMultipliersApply": {
    "type": "boolean",
    "default": true,
    "description": "**An hour at prime time drawing ninety minutes is a legitimate mechanic**, and a system that can only deduct elapsed time cannot express it.\n"
   },
   "validityMonths": {
    "type": "integer",
    "nullable": true
   },
   "transferableWithinHousehold": {
    "type": "boolean",
    "default": false
   },
   "applicableSpaceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
