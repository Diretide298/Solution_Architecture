# WS115 — ACCREDITATION board 8

**10 screens · 6 operations · 7 schemas · 3 permissions**

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
  `ACCREDITATION_VIEW, DEVELOPER_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-684` | Accreditation Executive Dashboard | listDetail | 1 | 0 | — |
| `BO-685` | Accreditation Status & Portfolio Reporting | listDetail | 1 | 0 | — |
| `BO-686` | Accreditation Utilization Analytics | listDetail | 1 | 0 | — |
| `BO-687` | Accreditation Access Activity Reporting | listDetail | 1 | 0 | — |
| `BO-688` | Accreditation Trend & Comparative Analysis | listDetail | 1 | 0 | — |
| `BO-689` | Accreditation Audit Reporting | listDetail | 1 | 0 | — |
| `BO-690` | Immutable Accreditation Audit Log | configEditor | 1 | 0 | — |
| `BO-691` | Accreditation API Management | listDetail | 1 | 0 | — |
| `BO-692` | Accreditation Webhook Management | configEditor | 1 | 0 | — |
| `BO-693` | Integration & Data Exchange Monitor | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-684, BO-685, BO-686, BO-687, BO-689, BO-691, BO-693 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-684",
  "name": "Accreditation Executive Dashboard",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "1",
   "page": 65
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-executive-dashboard-bo-684",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationExecutiveDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-685",
    "BO-686",
    "BO-687",
    "BO-688",
    "BO-689",
    "BO-690",
    "BO-691",
    "BO-692",
    "BO-693"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-685",
     "trigger": "Accreditation Status & Portfolio Reporting",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-686",
     "trigger": "Accreditation Utilization Analytics",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-687",
     "trigger": "Accreditation Access Activity Reporting",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-688",
     "trigger": "Accreditation Trend & Comparative Analysis",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-689",
     "trigger": "Accreditation Audit Reporting",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-690",
     "trigger": "Immutable Accreditation Audit Log",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-691",
     "trigger": "Accreditation API Management",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-692",
     "trigger": "Accreditation Webhook Management",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-693",
     "trigger": "Integration & Data Exchange Monitor",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Dashboard filters shall include) and no metric row",
  "purpose": "Provide management with a real-time overview of the complete accreditation operation.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack ACCREDITATION.pdf, page 65 §Dashboard filters shall include"
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
       "label": "Every accreditation executive",
       "columns": [
        "Tenant",
        "Event",
        "Venue",
        "Accreditation program",
        "Category",
        "Organization",
        "Date range"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack ACCREDITATION.pdf, page 65 §Dashboard filters shall include"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected accreditation executive",
       "bindsTo": null,
       "columns": [
        "Tenant",
        "Event",
        "Venue",
        "Accreditation program",
        "Category",
        "Organization",
        "Date range"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Scope of Work”, “Visualizations should include”, “Key requirements”.",
       "provenance": "pack ACCREDITATION.pdf, page 65 §Dashboard filters shall include"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation executive list.",
   "error": "Could not load. Names which read failed and leaves the accreditation executive untouched.",
   "emptyFirstRun": "No accreditation executive yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation executive are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationHolders",
    "contract": "accreditation",
    "purpose": "The executive view",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Tenant",
    "Event",
    "Venue",
    "Accreditation program",
    "Category",
    "Organization"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-684",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-684"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 65. 0 of 7 labels bound to a contract property; 7 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-685",
  "name": "Accreditation Status & Portfolio Reporting",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "2",
   "page": 66
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-status-portfolio-reporting-bo-685",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationStatusPortfolioReporting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-684"
   ],
   "exitTo": [
    "BO-684"
   ],
   "transitions": [
    {
     "to": "BO-684",
     "trigger": "Back to Accreditation Executive Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Report on active, expired, suspended and revoked accreditation records.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 66"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 66"
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
       "impliedBy": "listAccreditationHolders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation status portfolio list.",
   "error": "Could not load. Names which read failed and leaves the accreditation status portfolio untouched.",
   "emptyFirstRun": "No accreditation status portfolio yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation status portfolio are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationHolders",
    "contract": "accreditation",
    "purpose": "Status and portfolio",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-685",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-685"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 66. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-686",
  "name": "Accreditation Utilization Analytics",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "3",
   "page": 67
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-utilization-analytics-bo-686",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationUtilizationAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-684"
   ],
   "exitTo": [
    "BO-684"
   ],
   "transitions": [
    {
     "to": "BO-684",
     "trigger": "Back to Accreditation Executive Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Metrics shall include) and no metric row",
  "purpose": "Determine whether issued accreditations are actually being used.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack ACCREDITATION.pdf, page 67 §Metrics shall include"
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
       "label": "Every accreditation utilization analytics",
       "columns": [
        "Accreditations issued",
        "Accreditations activated",
        "Accreditations used",
        "Never-used accreditations",
        "First-use date/time",
        "Last-use date/time",
        "Number of access transactions",
        "Utilization percentage",
        "Utilization by category",
        "Utilization by venue",
        "Utilization by event"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack ACCREDITATION.pdf, page 67 §Metrics shall include"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected accreditation utilization analytics",
       "bindsTo": null,
       "columns": [
        "Accreditations issued",
        "Accreditations activated",
        "Accreditations used",
        "Never-used accreditations",
        "First-use date/time",
        "Last-use date/time",
        "Number of access transactions",
        "Utilization percentage",
        "Utilization by category",
        "Utilization by venue",
        "Utilization by event"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Scope of Work”.",
       "provenance": "pack ACCREDITATION.pdf, page 67 §Metrics shall include"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation utilization analytics list.",
   "error": "Could not load. Names which read failed and leaves the accreditation utilization analytics untouched.",
   "emptyFirstRun": "No accreditation utilization analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation utilization analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationAccessActivity",
    "contract": "accreditation",
    "purpose": "Utilisation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Accreditations issued",
    "Accreditations activated",
    "Accreditations used",
    "Never-used accreditations",
    "First-use date/time",
    "Last-use date/time"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-686",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-686"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 67. 0 of 11 labels bound to a contract property; 11 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-687",
  "name": "Accreditation Access Activity Reporting",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "4",
   "page": 68
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-access-activity-reporting-bo-687",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationAccessActivityReporting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-684"
   ],
   "exitTo": [
    "BO-684"
   ],
   "transitions": [
    {
     "to": "BO-684",
     "trigger": "Back to Accreditation Executive Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide detailed reporting of accreditation access activity.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 68"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 68"
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
       "impliedBy": "listAccreditationAccessActivity",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation access activity list.",
   "error": "Could not load. Names which read failed and leaves the accreditation access activity untouched.",
   "emptyFirstRun": "No accreditation access activity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation access activity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationAccessActivity",
    "contract": "accreditation",
    "purpose": "Access activity",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-687",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-687"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 68. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-688",
  "name": "Accreditation Trend & Comparative Analysis",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "5",
   "page": 68
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-trend-comparative-analysis-bo-688",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationTrendComparativeAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-684"
   ],
   "exitTo": [
    "BO-684"
   ],
   "transitions": [
    {
     "to": "BO-684",
     "trigger": "Back to Accreditation Executive Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Analyze accreditation behavior over time.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 68"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Measures",
       "operation": "getKpiValues",
       "notes": "Sends `?kpiCodes=`; each pack trend is a KPI code.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Compare",
       "operation": "getKpiValues",
       "notes": "Sends `?scopePath=`: event, venue, category or organisation.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Period",
       "operation": "getKpiValues",
       "notes": "Sends `?period=`: daily, weekly, monthly, seasonal or event-level.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "selectField",
       "label": "Compare to",
       "operation": "getKpiValues",
       "notes": "Sends `?compareTo=` (previousPeriod, samePeriodLastYear, target, benchmark).",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Approval rate",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "`kpiCodes` must include an approval-rate code; only takings and admissions are seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "metricTile",
       "label": "Average approval time",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.value",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "Needs an average-approval-time KPI code, which is not seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "chart",
       "label": "Accreditation trends",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.period",
        "KpiValue.value",
        "KpiValue.comparison"
       ],
       "operation": "getKpiValues",
       "notes": "One point per period; a trend needs one read per period, because `getKpiValues` returns a single period.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "dataTable",
       "label": "Comparative analysis",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.name",
        "KpiValue.scopePath",
        "KpiValue.period",
        "KpiValue.value",
        "KpiValue.comparison",
        "KpiValue.variancePercent",
        "KpiValue.direction",
        "KpiValue.status",
        "KpiValue.asOf",
        "KpiValue.stale"
       ],
       "operation": "getKpiValues",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation trend comparative list.",
   "error": "Could not load. Names which read failed and leaves the accreditation trend comparative untouched.",
   "emptyFirstRun": "No accreditation trend comparative yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation trend comparative are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Trend and comparison",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-688",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-688"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 68. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from contract reporting.yaml GET /kpi-values. Pack labels with no schema field yet (shown as plain labels): KPI codes not seeded: application volume, approval rate, rejection rate, average approval time, credential issuance, accreditation utilization, suspension rate, revocation rate, renewal rate, expiration volume, access activity, Series over time in one read, Organisation as a comparison scope.",
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
  "id": "BO-689",
  "name": "Accreditation Audit Reporting",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "6",
   "page": 69
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-audit-reporting-bo-689",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationAuditReporting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-684"
   ],
   "exitTo": [
    "BO-684"
   ],
   "transitions": [
    {
     "to": "BO-684",
     "trigger": "Back to Accreditation Executive Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide compliance and management reporting across accreditation actions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 69"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 69"
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
       "impliedBy": "listAccreditationAudit",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation audit reporting list.",
   "error": "Could not load. Names which read failed and leaves the accreditation audit reporting untouched.",
   "emptyFirstRun": "No accreditation audit reporting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation audit reporting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationAudit",
    "contract": "accreditation",
    "purpose": "Audit reporting",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-689",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-689"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 69. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-690",
  "name": "Immutable Accreditation Audit Log",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "7",
   "page": 70
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/immutable-accreditation-audit-log-bo-690",
   "component": "apps/venue-management-web/src/routes/access-venue/ImmutableAccreditationAuditLog.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-684"
   ],
   "exitTo": [
    "BO-684"
   ],
   "transitions": [
    {
     "to": "BO-684",
     "trigger": "Back to Accreditation Executive Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Audit records shall capture) and no display directory — it is settings, not a population",
  "purpose": "Maintain the authoritative security record of all accreditation actions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Audit ID",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Timestamp",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "User/service identity",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Action",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Entity type",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Entity ID",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Previous value",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "New value",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Source application/API",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Correlation/reference ID",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Result",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Reason where applicable",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      },
      {
       "kind": "selectField",
       "label": "Key requirement: 12.1.58",
       "provenance": "pack ACCREDITATION.pdf, page 70 §Audit records shall capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The immutable accreditation audit configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the immutable accreditation audit untouched.",
   "emptyFirstRun": "No immutable accreditation audit configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listAccreditationAudit",
    "contract": "accreditation",
    "purpose": "The immutable log",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-690",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-690"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 70. 0 of 0 labels bound to a contract property; 14 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-691",
  "name": "Accreditation API Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "8",
   "page": 71
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-api-management-bo-691",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationApiManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-684"
   ],
   "exitTo": [
    "BO-684"
   ],
   "transitions": [
    {
     "to": "BO-684",
     "trigger": "Back to Accreditation Executive Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Expose accreditation functionality securely to approved external systems.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 71"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 71"
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
       "impliedBy": "listApiClients",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation api list.",
   "error": "Could not load. Names which read failed and leaves the accreditation api untouched.",
   "emptyFirstRun": "No accreditation api yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation api are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "API management",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-691",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-691"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 71. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-692",
  "name": "Accreditation Webhook Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "9",
   "page": 71
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-webhook-management-bo-692",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationWebhookManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-684"
   ],
   "exitTo": [
    "BO-684"
   ],
   "transitions": [
    {
     "to": "BO-684",
     "trigger": "Back to Accreditation Executive Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Webhook configuration shall include) and no display directory — it is settings, not a population",
  "purpose": "Notify external systems when accreditation events occur.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Endpoint",
       "provenance": "pack ACCREDITATION.pdf, page 71 §Webhook configuration shall include"
      },
      {
       "kind": "selectField",
       "label": "Event subscriptions",
       "provenance": "pack ACCREDITATION.pdf, page 71 §Webhook configuration shall include"
      },
      {
       "kind": "selectField",
       "label": "Authentication/security",
       "provenance": "pack ACCREDITATION.pdf, page 71 §Webhook configuration shall include"
      },
      {
       "kind": "selectField",
       "label": "Secret/signature",
       "provenance": "pack ACCREDITATION.pdf, page 71 §Webhook configuration shall include"
      },
      {
       "kind": "selectField",
       "label": "Retry policy",
       "provenance": "pack ACCREDITATION.pdf, page 71 §Webhook configuration shall include"
      },
      {
       "kind": "selectField",
       "label": "Active/inactive",
       "provenance": "pack ACCREDITATION.pdf, page 71 §Webhook configuration shall include"
      },
      {
       "kind": "selectField",
       "label": "Delivery history",
       "provenance": "pack ACCREDITATION.pdf, page 71 §Webhook configuration shall include"
      },
      {
       "kind": "selectField",
       "label": "Key requirement: 12.1.53",
       "provenance": "pack ACCREDITATION.pdf, page 71 §Webhook configuration shall include"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation webhook configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the accreditation webhook untouched.",
   "emptyFirstRun": "No accreditation webhook configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listWebhookSubscriptions",
    "contract": "public-api",
    "purpose": "Webhooks",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-692",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-692"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 71. 0 of 0 labels bound to a contract property; 8 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-693",
  "name": "Integration & Data Exchange Monitor",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "8",
   "number": "10",
   "page": 72
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/integration-data-exchange-monitor-bo-693",
   "component": "apps/venue-management-web/src/routes/access-venue/IntegrationDataExchangeMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-684"
   ],
   "exitTo": [
    "BO-684"
   ],
   "transitions": [
    {
     "to": "BO-684",
     "trigger": "Back to Accreditation Executive Dashboard",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor accreditation APIs, webhooks and external-system synchronization.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 72"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 72"
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
       "impliedBy": "listAccreditationAudit",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The integration data exchange list.",
   "error": "Could not load. Names which read failed and leaves the integration data exchange untouched.",
   "emptyFirstRun": "No integration data exchange yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration data exchange are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationAudit",
    "contract": "accreditation",
    "purpose": "Integration audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-693",
   "workshopBoard": "wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-693"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 72. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getKpiValues": {
  "method": "GET",
  "path": "/kpi-values",
  "contract": "reporting",
  "summary": "Current values, against target, with movement",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kpiIds",
    "in": "query",
    "required": null
   },
   {
    "name": "kpiCodes",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "period",
    "in": "query",
    "required": null
   },
   {
    "name": "compareTo",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KpiValue"
 },
 "listAccreditationAccessActivity": {
  "method": "GET",
  "path": "/accreditation-access-activity",
  "contract": "accreditation",
  "summary": "Where accredited people actually went",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "holderId",
    "in": "query",
    "required": null
   },
   {
    "name": "zoneId",
    "in": "query",
    "required": null
   },
   {
    "name": "deniedOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationAccessEvent"
 },
 "listAccreditationAudit": {
  "method": "GET",
  "path": "/accreditation-audit",
  "contract": "accreditation",
  "summary": "The immutable record of who granted what to whom",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "holderId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationAuditRecord"
 },
 "listAccreditationHolders": {
  "method": "GET",
  "path": "/accreditation-holders",
  "contract": "accreditation",
  "summary": "Everybody accredited, and what state they are in",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "programmeId",
    "in": "query",
    "required": null
   },
   {
    "name": "organisationId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "expiringWithinDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationHolder"
 },
 "listApiClients": {
  "method": "GET",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Registered clients for this developer",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ApiClient"
 },
 "listWebhookSubscriptions": {
  "method": "GET",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "The tenant's webhook subscriptions, filterable by API client",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "clientId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WebhookSubscription"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccreditationAccessEvent": {
  "type": "object",
  "description": "Board 8.4. **Granted access against used access is the whole of the annual review.**\n",
  "properties": {
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "holderId": {
    "type": "string",
    "format": "uuid"
   },
   "holderName": {
    "type": "string"
   },
   "zoneId": {
    "type": "string",
    "format": "uuid"
   },
   "zoneName": {
    "type": "string"
   },
   "credentialId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "outcome": {
    "type": "string",
    "enum": [
     "admitted",
     "denied",
     "escorted"
    ]
   },
   "deniedReason": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "AccreditationAuditRecord": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.audit",
  "description": "Board 8.7. **Who gave this person access to that place, when, and on whose authority.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "holderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "action": {
    "type": "string"
   },
   "actorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "previousValue": {
    "nullable": true
   },
   "newValue": {
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "previousRecordHash": {
    "type": "string",
    "nullable": true
   },
   "recordHash": {
    "type": "string"
   },
   "integrity": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "intact",
     "broken",
     "unverifiable"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationHolder": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.holder",
  "description": "**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n",
  "required": [
   "id",
   "fullName"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accreditationNumber": {
    "type": "string"
   },
   "fullName": {
    "type": "string"
   },
   "photoAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "nationality": {
    "type": "string",
    "nullable": true
   },
   "identityDocumentVerified": {
    "type": "boolean",
    "default": false
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "affiliationRole": {
    "type": "string",
    "nullable": true
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked",
     "expired",
     "archived"
    ]
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "completenessPercent": {
    "type": "integer",
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ApiClient": {
  "type": "object",
  "x-ticvai-persistence": "control.api_client",
  "description": "CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n",
  "required": [
   "id",
   "developerId",
   "name",
   "environment",
   "scopes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "clientId": {
    "type": "string",
    "readOnly": true
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "production"
    ],
    "description": "**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"
   },
   "scopes": {
    "type": "array",
    "description": "**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing.\n",
    "items": {
     "type": "string"
    }
   },
   "allowedTenantIds": {
    "type": "array",
    "description": "13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "ipAllowList": {
    "type": "array",
    "description": "13.1.38. Optional, and the strongest control available where an integrator has fixed egress.",
    "items": {
     "type": "string"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked"
    ],
    "readOnly": true
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**A credential unused for a year is a credential nobody will notice being stolen.**\n"
   }
  }
 },
 "KpiValue": {
  "type": "object",
  "description": "BI board 10.3. **Value, target, variance, direction and freshness in one read.**",
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "period": {
    "type": "string"
   },
   "value": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "target": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "comparison": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "variancePercent": {
    "type": "number",
    "nullable": true
   },
   "direction": {
    "type": "string",
    "enum": [
     "up",
     "down",
     "flat"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "green",
     "amber",
     "red",
     "noTarget"
    ]
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "stale": {
    "type": "boolean",
    "description": "**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"
   }
  }
 },
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  ]
 },
 "WebhookSubscription": {
  "type": "object",
  "x-ticvai-persistence": "control.webhook_subscription",
  "description": "13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n",
  "required": [
   "id",
   "clientId",
   "endpointUrl",
   "eventTypes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "clientId": {
    "type": "string",
    "format": "uuid"
   },
   "endpointUrl": {
    "type": "string"
   },
   "eventTypes": {
    "type": "array",
    "description": "**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to.\n",
    "items": {
     "type": "string"
    }
   },
   "filters": {
    "type": "object",
    "nullable": true,
    "description": "13.3.22. Tenant, venue, or a business condition on the payload.",
    "additionalProperties": true
   },
   "signingSecret": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "description": "**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingVerification",
     "active",
     "paused",
     "failing",
     "disabled"
    ],
    "readOnly": true
   },
   "consecutiveFailures": {
    "type": "integer",
    "readOnly": true
   },
   "disabledReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"
   }
  }
 }
}
```
