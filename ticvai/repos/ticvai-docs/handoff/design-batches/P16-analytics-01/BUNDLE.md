# P16-analytics-01 — P16 · Analytics

**10 screens · 20 operations · 26 schemas · 11 permissions**

Platform P16 Venue Analytics · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `AI_APPROVE, AI_USE, DEVICE_VIEW, LEDGER_VIEW, MARKETING_MANAGE, MARKETING_VIEW, ORDER_VIEW, PRODUCT_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **5 of these operations work offline**: getCountVariance, listDevices, listExpiringBatches, listOrders, listProducts
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ANL-001` | Executive Command Center | listDetail | 4 | 0 | — |
| `ANL-002` | Sales, Revenue & Channel | statusTracker | 2 | 0 | — |
| `ANL-003` | Operational Performance | listDetail | 5 | 0 | — |
| `ANL-004` | Product Performance | listDetail | 3 | 0 | — |
| `ANL-005` | Cost, Margin & Profitability | statusTracker | 3 | 0 | — |
| `ANL-006` | Inventory & Waste Intelligence | listDetail | 4 | 0 | — |
| `ANL-007` | Guest & Conversion Intelligence | listDetail | 5 | 0 | — |
| `ANL-008` | Demand Forecasting | statusTracker | 2 | 0 | — |
| `ANL-009` | AI Assistant & Action Center | approvalInbox | 8 | 0 | — |
| `ANL-010` | Suggestions & Advice | configEditor | 2 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ANL-001",
  "name": "Executive Command Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/executive-command-center",
   "component": "apps/venue-management-web/src/routes/analytics/ExecutiveCommandCenterDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "exitTo": [
    "ANL-002",
    "ANL-003",
    "ANL-004",
    "ANL-005",
    "ANL-006",
    "ANL-007",
    "ANL-008",
    "ANL-009",
    "ANL-010",
    "ANL-012",
    "ANL-013",
    "ANL-014",
    "ANL-015",
    "ANL-016",
    "ANL-017",
    "ANL-018",
    "ANL-019",
    "ANL-020",
    "ANL-021",
    "ANL-031",
    "ANL-041",
    "ANL-051",
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "ANL-061",
     "trigger": "BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-021",
     "trigger": "Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ANL-031",
     "trigger": "Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-041",
     "trigger": "Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-051",
     "trigger": "AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-002",
     "trigger": "Sales, Revenue & Channel",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-003",
     "trigger": "Operational Performance",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-004",
     "trigger": "Product Performance",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-005",
     "trigger": "Cost, Margin & Profitability",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-006",
     "trigger": "Inventory & Waste Intelligence",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-007",
     "trigger": "Guest & Conversion Intelligence",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-008",
     "trigger": "Demand Forecasting",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-009",
     "trigger": "AI Assistant & Action Center",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-010",
     "trigger": "Suggestions & Advice",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-012",
     "trigger": "Live Operations Dashboard",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-013",
     "trigger": "Revenue Pulse",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-014",
     "trigger": "Attendance & Footfall Intelligence",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-015",
     "trigger": "Capacity & Utilization Monitor",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-016",
     "trigger": "Sales & Channel Performance",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-017",
     "trigger": "Customer, Membership & Loyalty Pulse",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-018",
     "trigger": "Alerts & Exception Center",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-019",
     "trigger": "AI Management Insights",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 3 board screens**: F&B Executive Command Center; Retail Executive Command Center; Enterprise Frontline Operations Dashboard. **Three board screens, one screen with a domain selector.** F&B, Retail and POS each drew an executive command centre and they differ only in which numbers fill the tiles. **Owns POS board frame(s) POS-6A** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6a` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **`wireframe.status` corrected 25 August.** When these screens were repointed from the client pack to their own board on 24 August, the status stayed `designed` — **which claimed a client had drawn a board this package generated.** `derivedFrom` keeps the pack frame, which is where the design came from; `status` describes the file being pointed at, and those are different facts.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6a",
   "POS Board 6.dc.html#pos-6a",
   "Retail Board 6.dc.html#ret-6a"
  ],
  "pattern": "listDetail",
  "patternReason": "`listAlerts` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Executive Command Center — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every executive",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected executive",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Request",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "secondaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What is currently raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "requestSuggestion",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not.",
   "preloaded": [
    "DashboardData.tileData"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-001",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn as POS-6A in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/POS Board 6.dc.html#pos-6a"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "purposeNote": "Provide senior management with an immediate consolidated view of overall organizational performance.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 3 §The system shall display"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-002",
  "name": "Sales, Revenue & Channel",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/sales-revenue-channel",
   "component": "apps/venue-management-web/src/routes/analytics/SalesRevenueChannelDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Sales, Revenue & Channel Analytics; Sales, Revenue & Channel Analytics. **The same screen twice in the client set, word for word.** Revenue by channel is revenue by channel whether the line is a burger or a t-shirt. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6l` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6b",
   "Retail Board 6.dc.html#ret-6l"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getDashboard` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Sales, Revenue & Channel — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected sales revenue channel",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-002",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6L in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6l"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-003",
  "name": "Operational Performance",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/operational-performance",
   "component": "apps/venue-management-web/src/routes/analytics/OperationalPerformanceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 4 board screens**: Outlet, Service & Guest Performance; Store & Operational Performance; Venue Operations Dashboard and 1 more. **Four board screens.** Outlet, store, venue and department are the same question at four levels of `scope_path` — which is a filter, not four screens. **Owns POS board frame(s) POS-6B, POS-6C, POS-6D** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6b` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4k",
   "FnB Board 6.dc.html#fnb-6c",
   "FnB Board 6.dc.html#fnb-6g",
   "POS Board 6.dc.html#pos-6b",
   "POS Board 6.dc.html#pos-6c",
   "POS Board 6.dc.html#pos-6d",
   "Retail Board 6.dc.html#ret-6b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listAlerts` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Operational Performance — across F&B, retail, ticketing and frontline, filtered by domain.",
  "gaps": [
   {
    "operation": "listDevices",
    "why": "**2 declared operations reach no component on this screen**: listDevices, listPrincipals. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every operational performance",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected operational performance",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What is currently raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDevices",
    "contract": "tenancy",
    "purpose": "List registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPrincipals",
    "contract": "identity",
    "purpose": "List principals",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not.",
   "preloaded": [
    "DashboardData.tileData"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-003",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn as POS-6B, POS-6C, POS-6D in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/POS Board 6.dc.html#pos-6b"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-004",
  "name": "Product Performance",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/product-performance",
   "component": "apps/venue-management-web/src/routes/analytics/ProductPerformanceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-007"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-006"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-006",
     "trigger": "Inventory & Waste Intelligence",
     "provenance": "flow F82 step 3→4"
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Product Performance & Menu Engineering; Product, SKU & Merchandise Performance. **Menu engineering and SKU performance are one analysis.** Both rank products by margin against volume; only the vocabulary differs. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6c` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6d",
   "Retail Board 6.dc.html#ret-6c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Product Performance — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every product performance",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product performance",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not.",
   "preloaded": [
    "DashboardData.tileData"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-004",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6C in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6c"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-005",
  "name": "Cost, Margin & Profitability",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/cost-margin-profitability",
   "component": "apps/venue-management-web/src/routes/analytics/CostMarginProfitabilityDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-007"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-007",
     "trigger": "Guest & Conversion Intelligence",
     "provenance": "flow F82 step 1→2",
     "operation": "getStockValuation"
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Food Cost, Margin & Profitability Intelligence; Promotion, Pricing & Margin Intelligence. Cost against price against what actually sold. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6f` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6e",
   "Retail Board 6.dc.html#ret-6f"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getDashboard` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Cost, Margin & Profitability — across F&B, retail, ticketing and frontline, filtered by domain.",
  "gaps": [
   {
    "operation": "getStockValuation",
    "why": "**1 declared operation reach no component on this screen**: getStockValuation. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cost margin profitability",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction"
   },
   {
    "operationId": "getStockValuation",
    "contract": "inventory",
    "purpose": "Stock value by location and category",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-005",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6F in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6f"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-006",
  "name": "Inventory & Waste Intelligence",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/inventory-waste-intelligence",
   "component": "apps/venue-management-web/src/routes/analytics/InventoryWasteIntelligenceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-004"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-058",
     "trigger": "Reporting Home",
     "provenance": "flow F82 step 4→5",
     "operation": "listExpiringBatches",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Inventory, Waste & Production Intelligence; Inventory, Sell-Through & Stock Intelligence. **Theoretical against actual is the whole analysis** — a recipe says 400 portions, the run says 380, and the gap is waste, theft or a wrong recipe. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6d` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `Retail Board 6.dc.html` frame `ret-6d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Inventory &amp; Stock Intelligence* matched at 0.89. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6f",
   "Retail Board 6.dc.html#ret-6d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listExpiringBatches` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Inventory & Waste Intelligence — across F&B, retail, ticketing and frontline, filtered by domain.",
  "gaps": [
   {
    "operation": "getCountVariance",
    "why": "**1 declared operation reach no component on this screen**: getCountVariance. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every inventory waste intelligence",
       "bindsTo": "StockBatch",
       "columns": [
        "StockBatch.id",
        "StockBatch.itemId",
        "StockBatch.locationId",
        "StockBatch.batchCode",
        "StockBatch.lotNumber",
        "StockBatch.quantity",
        "StockBatch.receivedAt",
        "StockBatch.expiresAt",
        "StockBatch.supplierId",
        "StockBatch.status"
       ],
       "operation": "listExpiringBatches",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected inventory waste intelligence",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listExpiringBatches"
    ]
   },
   {
    "operationId": "getCountVariance",
    "contract": "inventory",
    "purpose": "Variance between counted and expected",
    "trigger": "onLoad"
   },
   {
    "operationId": "listExpiringBatches",
    "contract": "inventory",
    "purpose": "What is about to go out of date",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "countId",
     "from": "deepLink"
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not.",
   "preloaded": [
    "DashboardData.tileData"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-006",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 6.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing.",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6d"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-007",
  "name": "Guest & Conversion Intelligence",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/guest-conversion-intelligence",
   "component": "apps/venue-management-web/src/routes/analytics/GuestConversionIntelligenceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-005"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-004"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-004",
     "trigger": "Product Performance",
     "provenance": "flow F82 step 2→3"
    },
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Guest, Conversion & Basket Intelligence; Kitchen, Service & Fulfilment Performance. Who bought, what else they nearly bought, and how long they waited. **Retail board operations wired 24 August.** **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6e` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 6.dc.html#ret-6e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSegments` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Guest & Conversion Intelligence — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every guest conversion intelligence",
       "bindsTo": "Segment",
       "columns": [
        "Segment.name",
        "Segment.description",
        "Segment.venueId",
        "Segment.match",
        "Segment.criteria",
        "Segment.excludeSegmentIds",
        "Segment.id",
        "Segment.lastEvaluatedSize",
        "Segment.lastEvaluatedAt"
       ],
       "operation": "listSegments",
       "provenance": "contract marketing-crm.yaml GET /segments"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected guest conversion intelligence",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createSegment",
       "provenance": "contract marketing-crm.yaml POST /segments"
      },
      {
       "kind": "secondaryButton",
       "label": "Preview",
       "operation": "previewSegment",
       "provenance": "contract marketing-crm.yaml POST /segments/{segmentId}/preview"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listSegments"
    ]
   },
   {
    "operationId": "listSegments",
    "contract": "marketing-crm",
    "purpose": "List segments",
    "trigger": "onLoad"
   },
   {
    "operationId": "createSegment",
    "contract": "marketing-crm",
    "purpose": "Create a segment",
    "trigger": "onAction",
    "invalidates": [
     "listSegments"
    ]
   },
   {
    "operationId": "previewSegment",
    "contract": "marketing-crm",
    "purpose": "Estimate segment size and reachability",
    "trigger": "onAction",
    "invalidates": [
     "listSegments"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    },
    {
     "name": "segmentId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not. A segment opened from the list.",
   "preloaded": [
    "DashboardData.tileData"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-007",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6E in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6e"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-008",
  "name": "Demand Forecasting",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/demand-forecasting",
   "component": "apps/venue-management-web/src/routes/analytics/DemandForecastingDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Demand Forecasting & Operational Planning; Demand Forecasting & Merchandise Planning. **A forecast is an input to a requisition, not a report.** Its value is that somebody orders differently because of it. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6g` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6h",
   "Retail Board 6.dc.html#ret-6g"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getDashboard` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Demand Forecasting — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected demand forecasting",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ask",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction"
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-008",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6G in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6g"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-009",
  "name": "AI Assistant & Action Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-assistant-action-center",
   "component": "apps/venue-management-web/src/routes/analytics/AiAssistantActionCenterDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-010",
     "trigger": "Promotions & Coupons",
     "provenance": "flow F77 step 3→4",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "**Built 20 August. Answers 5 board screens**: AI Recommendation, Simulation & Optimization Center; AI Assistant, Alerts & Management Action Center; Transaction & Exception Monitoring and 2 more. **Five board screens, and the collapse is the point.** Every domain drew an AI centre and an alert centre; **an alert nobody can act on from the screen showing it is a notification**, so recommendation and action are one place. **Owns POS board frame(s) POS-6E** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Retail board operations wired 24 August.** **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6e` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5k",
   "FnB Board 6.dc.html#fnb-6j",
   "FnB Board 6.dc.html#fnb-6k",
   "POS Board 6.dc.html#pos-6e",
   "Retail Board 5.dc.html#ret-5k",
   "Retail Board 6.dc.html#ret-6k"
  ],
  "pattern": "approvalInbox",
  "patternReason": "`decideProposedAction` decides items that `listAlerts` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "AI Assistant & Action Center — across F&B, retail, ticketing and frontline, filtered by domain.",
  "gaps": [
   {
    "operation": "listOrders",
    "why": "**2 declared operations reach no component on this screen**: listOrders, listProposedActions. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected assistant action",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ask",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Acknowledge",
       "operation": "acknowledgeAlert",
       "provenance": "contract reporting.yaml POST /alerts/{alertId}/acknowledge"
      },
      {
       "kind": "secondaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAlertRule",
       "provenance": "contract reporting.yaml PUT /alert-rules"
      },
      {
       "kind": "secondaryButton",
       "label": "Decide",
       "operation": "decideProposedAction",
       "provenance": "contract ai.yaml POST /proposed-actions/{actionId}/decide"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What is currently raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "acknowledgeAlert",
    "contract": "reporting",
    "purpose": "Take responsibility for it",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "setAlertRule",
    "contract": "reporting",
    "purpose": "Raise an alert when a number leaves a range",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "listProposedActions",
    "contract": "ai",
    "purpose": "What the assistant has proposed and nobody has decided",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideProposedAction",
    "contract": "ai",
    "purpose": "Approve or reject a proposal",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "alertId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    },
    {
     "name": "actionId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not. A proposed action opened from the queue or an alert.",
   "preloaded": [
    "Alert.id",
    "Alert.ruleId",
    "Alert.raisedAt",
    "Alert.severity",
    "Alert.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-009",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn as POS-6E in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/POS Board 6.dc.html#pos-6e"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-010",
  "name": "Suggestions & Advice",
  "module": "Analytics",
  "requiresModule": "ai",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/suggestions",
   "component": "apps/venue-management-web/src/routes/analytics/SuggestionsDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "domain",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, domain, reportId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Built 24 August.** The client F&B boards drew six suggestion endpoints — price, requisition, replenishment, scenario, SLA, demand plan. **One screen and one operation answer all six**, because a suggestion surface that differs per domain is six screens to change when the model changes. **Owns POS board frame(s) POS-6F** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6f` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "POS Board 6.dc.html#pos-6f"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`requestSuggestion`, `recordSuggestionOutcome`) and no read of a population — it is settings, not a list",
  "purpose": "Every open suggestion, what it is based on, and whether the venue took it.",
  "gaps": [
   {
    "operation": "requestSuggestion",
    "why": "**`requestSuggestion` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract ai.yaml POST /ai/suggestions"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Request",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordSuggestionOutcome",
       "provenance": "contract ai.yaml POST /ai/suggestions/{suggestionId}/outcome"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Kind",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "bindsTo": "Suggestion[]",
       "notes": "**The basis is on the card, not behind a tap.** A manager must see that today’s answer is a margin rule and next quarter’s is a model — the same screen, a different basis.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "notes": "The explanation in plain words and the inputs it used. **Advice computed from data the manager cannot see is advice they will not trust.**",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Take it",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Do something else",
       "notes": "**Records the outcome either way.** A rejected suggestion is the case the current rule got wrong, which is exactly what a model is trained to beat.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Open suggestions, newest first, grouped by kind.",
   "error": "Could not load. **Trading is unaffected** — this advises and does not act.",
   "emptyFirstRun": "**A venue with no history has nothing to suggest from**, and the screen says so rather than showing a rule dressed as advice. Names when there will be enough data.",
   "emptyNoAccess": "You do not have AI permission at this venue."
  },
  "apis": [
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "Ask for an answer",
    "trigger": "onAction"
   },
   {
    "operationId": "recordSuggestionOutcome",
    "contract": "ai",
    "purpose": "What the venue did",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "suggestionId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "A bookmarked view opened weekly, or **a link from an alert naming one suggestion** — an alert that cannot take a manager to the thing it is about is a notification."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-010",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn as POS-6F in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/POS Board 6.dc.html#pos-6f"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
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
 "acknowledgeAlert": {
  "method": "POST",
  "path": "/alerts/{alertId}/acknowledge",
  "contract": "reporting",
  "summary": "Mark it seen",
  "permission": "REPORT_VIEW_VENUE",
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
  "responds": "Alert"
 },
 "askReportingQuestion": {
  "method": "POST",
  "path": "/reports/ask",
  "contract": "reporting",
  "summary": "Natural-language reporting query",
  "permission": "REPORT_VIEW_VENUE",
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
  "responds": "NaturalLanguageAnswer"
 },
 "createSegment": {
  "method": "POST",
  "path": "/segments",
  "contract": "marketing-crm",
  "summary": "Create a segment",
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
  "requestBody": "CreateSegmentRequest",
  "responds": "Segment"
 },
 "decideProposedAction": {
  "method": "POST",
  "path": "/proposed-actions/{actionId}/decide",
  "contract": "ai",
  "summary": "Approve or reject a proposal",
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
  "responds": "ProposedAction"
 },
 "getCountVariance": {
  "method": "GET",
  "path": "/stock-counts/{countId}/variance",
  "contract": "inventory",
  "summary": "Variance between counted and expected",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CountVariance"
 },
 "getDashboard": {
  "method": "GET",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Read a dashboard with tile data",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "refresh",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DashboardData"
 },
 "getStockValuation": {
  "method": "GET",
  "path": "/stock/valuation",
  "contract": "inventory",
  "summary": "Stock value by location and category",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "asAt",
    "in": "query",
    "required": null
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "StockValuation"
 },
 "listAlerts": {
  "method": "GET",
  "path": "/alerts",
  "contract": "reporting",
  "summary": "What is currently wrong",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Alert"
 },
 "listDevices": {
  "method": "GET",
  "path": "/devices",
  "contract": "tenancy",
  "summary": "List registered devices",
  "permission": "DEVICE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workstationId",
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
 "listExpiringBatches": {
  "method": "GET",
  "path": "/stock-batches/expiring",
  "contract": "inventory",
  "summary": "What is about to go out of date",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "withinDays",
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
  "responds": "StockBatch"
 },
 "listOrders": {
  "method": "GET",
  "path": "/orders",
  "contract": "orders",
  "summary": "List orders",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "createdFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "createdTo",
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
 "listPrincipals": {
  "method": "GET",
  "path": "/principals",
  "contract": "identity",
  "summary": "List principals",
  "permission": "USER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "isActive",
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
 "listProducts": {
  "method": "GET",
  "path": "/products",
  "contract": "catalogue",
  "summary": "List products",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "isSellable",
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
  "permission": "AI_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProposedAction"
 },
 "listSegments": {
  "method": "GET",
  "path": "/segments",
  "contract": "marketing-crm",
  "summary": "List segments",
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
 "previewSegment": {
  "method": "POST",
  "path": "/segments/{segmentId}/preview",
  "contract": "marketing-crm",
  "summary": "Estimate segment size and reachability",
  "permission": "MARKETING_VIEW",
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
  "responds": "SegmentPreview"
 },
 "recordSuggestionOutcome": {
  "method": "POST",
  "path": "/ai/suggestions/{suggestionId}/outcome",
  "contract": "ai",
  "summary": "What the venue actually did",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SuggestionOutcome",
  "responds": "SuggestionOutcome"
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
 "runReport": {
  "method": "POST",
  "path": "/reports/{reportId}/run",
  "contract": "reporting",
  "summary": "Run a report",
  "permission": "REPORT_VIEW_VENUE",
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
  "requestBody": "RunReportRequest",
  "responds": "ReportResult"
 },
 "setAlertRule": {
  "method": "PUT",
  "path": "/alert-rules",
  "contract": "reporting",
  "summary": "Watch a metric and tell somebody",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "AlertRule",
  "responds": "AlertRule"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Alert": {
  "type": "object",
  "x-ticvai-persistence": "reporting.alert",
  "description": "A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n",
  "required": [
   "id",
   "ruleId",
   "raisedAt",
   "severity",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "ruleId": {
    "type": "string",
    "format": "uuid"
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "severity": {
    "type": "string",
    "enum": [
     "info",
     "warning",
     "critical"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "raised",
     "acknowledged",
     "resolved",
     "expired"
    ]
   },
   "observedValue": {
    "type": "number"
   },
   "threshold": {
    "type": "number"
   },
   "scopePath": {
    "type": "string"
   },
   "acknowledgedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "acknowledgedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"
   }
  }
 },
 "AlertRule": {
  "type": "object",
  "x-ticvai-persistence": "reporting.alert_rule",
  "description": "BL-152, CF-134. **Six contracts detect their own trouble and none told a person.**\nFive sections ask for this and it is the same gap as `MessageTrigger`, seen from the operational side — **that one tells a guest something happened; this one tells an operator something is wrong.**\n**A threshold that nobody is watching is a threshold nobody set.** 6.1.57 wants an exception when a KPI leaves range, and an exception that arrives in a nightly report is an exception nobody acted on.\n",
  "required": [
   "id",
   "name",
   "metric",
   "comparator",
   "threshold",
   "severity",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "metric": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricSource"
     }
    ],
    "description": "**From the closed set**, so a rule cannot watch something nothing produces — the same discipline `MetricSource` exists for.\n"
   },
   "comparator": {
    "type": "string",
    "enum": [
     "above",
     "below",
     "outsideRange",
     "changesBy",
     "equals"
    ]
   },
   "threshold": {
    "type": "number"
   },
   "thresholdUpper": {
    "type": "number",
    "nullable": true
   },
   "windowMinutes": {
    "type": "integer",
    "default": 15,
    "description": "**The window is what stops an alert firing on noise.** A queue that spikes for ninety seconds is not a queue that needs a manager, and a rule with no window is a rule somebody mutes within a week.\n"
   },
   "severity": {
    "type": "string",
    "enum": [
     "info",
     "warning",
     "critical"
    ]
   },
   "deliverTo": {
    "type": "array",
    "description": "CF-134. **The dashboard panel is the default and the only one that always applies.** Email or WhatsApp where the matrix names them — an operational alert arriving by email is an alert nobody sees in time.\n",
    "items": {
     "type": "string",
     "enum": [
      "dashboardPanel",
      "email",
      "whatsapp",
      "sms"
     ]
    }
   },
   "recipientRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "cooldownMinutes": {
    "type": "integer",
    "default": 30,
    "description": "**How long before the same rule may fire again.** Without it, a metric hovering on a threshold produces forty alerts an hour and the panel becomes something people close.\n"
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "CountVariance": {
  "x-ticvai-persistence": "none — computed at close",
  "type": "object",
  "required": [
   "countId",
   "totalVarianceValue",
   "lines"
  ],
  "properties": {
   "countId": {
    "type": "string"
   },
   "totalVarianceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exceptionCount": {
    "type": "integer",
    "description": "Lines beyond tolerance, requiring review before posting."
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "itemId",
      "expectedQuantity",
      "countedQuantity",
      "variance",
      "isException"
     ],
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "itemName": {
       "type": "string"
      },
      "sku": {
       "type": "string"
      },
      "expectedQuantity": {
       "type": "number"
      },
      "countedQuantity": {
       "type": "number"
      },
      "variance": {
       "type": "number"
      },
      "variancePercentage": {
       "type": "number"
      },
      "varianceValue": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "isException": {
       "type": "boolean"
      },
      "recountCount": {
       "type": "integer",
       "description": "A line counted several times is itself a finding."
      },
      "note": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "CreateSegmentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "criteria"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "match": {
    "type": "string",
    "enum": [
     "all",
     "any"
    ],
    "default": "all"
   },
   "criteria": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/SegmentCriterion"
    }
   },
   "excludeSegmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "Dashboard": {
  "x-ticvai-persistence": "reporting.dashboard + reporting.dashboard_tile",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateDashboardRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "aggregateCost",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "aggregateCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Combined refresh load of every tile."
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "DashboardData": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/Dashboard"
   },
   {
    "type": "object",
    "properties": {
     "tileData": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "tileId": {
         "type": "string",
         "format": "uuid"
        },
        "result": {
         "$ref": "#/components/schemas/ReportResult"
        },
        "isCached": {
         "type": "boolean"
        },
        "error": {
         "type": "string",
         "nullable": true
        }
       }
      }
     }
    }
   }
  ]
 },
 "DataSource": {
  "type": "string",
  "description": "What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n",
  "enum": [
   "orders",
   "orderLines",
   "payments",
   "refunds",
   "shifts",
   "scanEvents",
   "entitlements",
   "products",
   "inventory",
   "stockMovements",
   "stockCounts",
   "waste",
   "workstations",
   "devices",
   "principals",
   "loyalty",
   "reviews",
   "queueEntries",
   "guests",
   "campaigns",
   "cases",
   "ledgerEntries",
   "workOrders",
   "approvals",
   "purchaseOrders",
   "receipts",
   "requisitions",
   "stockBatches",
   "resourceBookings",
   "delegations",
   "forms",
   "challenges",
   "wallets",
   "resaleListings"
  ]
 },
 "FieldType": {
  "type": "string",
  "enum": [
   "string",
   "integer",
   "decimal",
   "money",
   "boolean",
   "date",
   "dateTime",
   "uuid",
   "enum"
  ]
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
 },
 "MetricSource": {
  "type": "string",
  "description": "**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` is deliberately absent.** It needs the staff-assignment link that CL-01 covers, and naming a metric with no source is the defect this enum exists to prevent.\n",
  "enum": [
   "occupancy",
   "capacityUtilisation",
   "admissionRate",
   "noShowRate",
   "conversion",
   "salesByOperator",
   "salesByWorkstation",
   "waitTime",
   "throughput",
   "abandonmentRate",
   "inventoryValuation",
   "stockTurnover",
   "stockAgeing",
   "wastageRate",
   "resaleVolume",
   "resaleCommission",
   "salesByInstructor",
   "resourceUtilisation",
   "allocationUtilisation",
   "channelAllocationBurn",
   "membershipChurn",
   "membershipRenewalRate",
   "supplierDeliveryPerformance",
   "revenuePerEntitlement",
   "revenuePerVisitor",
   "assetDowntime",
   "meanTimeToRepair",
   "challengeCompletionRate",
   "attributedRevenue"
  ],
  "x-ticvai-extended": "18 August 2026",
  "x-ticvai-extension-note": "**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"
 },
 "NaturalLanguageAnswer": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "conversationId",
   "question",
   "interpretation",
   "result",
   "confidence"
  ],
  "properties": {
   "conversationId": {
    "type": "string"
   },
   "question": {
    "type": "string"
   },
   "interpretation": {
    "type": "string",
    "description": "What the question was understood to mean, in plain language."
   },
   "generatedQuery": {
    "type": "object",
    "description": "The structured query produced — data source, columns, filters, grouping. Returned so the answer can be checked. An answer nobody can verify is worse than no answer.\n",
    "properties": {
     "dataSource": {
      "$ref": "#/components/schemas/DataSource"
     },
     "columns": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ReportColumn"
      }
     },
     "filters": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ReportFilter"
      }
     },
     "groupBy": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "result": {
    "$ref": "#/components/schemas/ReportResult"
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "suggestedFollowUps": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modelVersion": {
    "type": "string"
   },
   "tokensUsed": {
    "type": "integer"
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
     "configuration"
    ]
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
    "description": "The request body a person would submit, ready to review."
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "proposed",
     "approved",
     "rejected",
     "applied",
     "expired"
    ]
   },
   "approvalLevel": {
    "type": "integer",
    "description": "8.3.65. Multi-level, because a discount and a pricing change differ in authority."
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
   }
  }
 },
 "ReportColumn": {
  "x-ticvai-persistence": "reporting.report_column",
  "type": "object",
  "required": [
   "field"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "aggregation": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Aggregation"
     }
    ],
    "default": "none"
   },
   "sortOrder": {
    "type": "integer"
   },
   "sortDirection": {
    "type": "string",
    "enum": [
     "asc",
     "desc"
    ]
   },
   "format": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "ReportFilter": {
  "x-ticvai-persistence": "reporting.report_filter",
  "type": "object",
  "required": [
   "field",
   "operator"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "in",
     "notIn",
     "contains",
     "isNull",
     "isNotNull"
    ]
   },
   "value": {},
   "values": {
    "type": "array",
    "items": {}
   },
   "isParameter": {
    "type": "boolean",
    "default": false,
    "description": "Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"
   }
  }
 },
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
   }
  }
 },
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date"
   },
   "dateTo": {
    "type": "string",
    "format": "date"
   },
   "forceAsync": {
    "type": "boolean",
    "default": false,
    "description": "Queue regardless of size, for a result to be collected later."
   }
  }
 },
 "Segment": {
  "x-ticvai-persistence": "marketing.segment + marketing.segment_criterion",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateSegmentRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "lastEvaluatedSize": {
      "type": "integer",
      "nullable": true
     },
     "lastEvaluatedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "SegmentCriterion": {
  "x-ticvai-persistence": "marketing.segment_criterion",
  "type": "object",
  "required": [
   "attribute",
   "operator"
  ],
  "properties": {
   "attribute": {
    "type": "string",
    "description": "Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language.\n**Free-form rather than an enum, which is why 22.14.8, 5.3.19 and 5.5.17b were readable as gaps and are not.** `walletBalance`, `engagementTier` and `portfolioScope` are expressible today; what was missing was anybody saying so.\n**Three that need saying, because the naive reading is wrong:**\n`walletBalance` should segment on **`cash` credit only**. A guest with 200 dirhams of promotional credit expiring Friday is a different campaign from one with 200 of their own money, and treating them alike sends a spend-it-now message to somebody who was given it.\n`walletBalance.expiringWithinDays` is the segment that earns the attribute — **credit about to expire unspent is a guest about to be disappointed and a venue about to book breakage**, and only one of those is worth a message.\n`portfolioScope` aggregates across a `DelegatedAccess` delegation (CF-132) and **must not message every member about a household total** — that is how a venue tells a teenager what their parent spends.\n"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "in",
     "notIn",
     "exists",
     "notExists",
     "withinDays"
    ]
   },
   "value": {},
   "values": {
    "type": "array",
    "items": {}
   }
  }
 },
 "SegmentPreview": {
  "x-ticvai-persistence": "none — evaluated live",
  "type": "object",
  "required": [
   "segmentId",
   "matchingCount",
   "reachable"
  ],
  "properties": {
   "segmentId": {
    "type": "string",
    "format": "uuid"
   },
   "matchingCount": {
    "type": "integer"
   },
   "reachable": {
    "type": "array",
    "description": "Per channel, after consent and suppression. A segment of 50,000 with 3,000 email consents is a 3,000-person campaign.\n",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "reachableCount": {
       "type": "integer"
      },
      "excludedNoConsent": {
       "type": "integer"
      },
      "excludedSuppressed": {
       "type": "integer"
      },
      "excludedNoAddress": {
       "type": "integer"
      }
     }
    }
   },
   "evaluatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "StockBatch": {
  "type": "object",
  "x-ticvai-persistence": "inventory.stock_batch",
  "description": "BL-122. **`isPerishable` and `shelfLifeDays` are on the item, so a shelf life is declared and never instantiated.** Two deliveries of the same milk arriving a week apart are one stock level with one implied expiry, and the older one is invisible.\n**A batch is the instance that actually expires.** Without it, first-expiry-first-out is not computable and a venue discovers the problem by smell.\n",
  "required": [
   "id",
   "itemId",
   "locationId",
   "quantity",
   "receivedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "itemId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "batchCode": {
    "type": "string",
    "nullable": true
   },
   "lotNumber": {
    "type": "string",
    "nullable": true,
    "description": "The supplier's own reference. **A recall names a lot number**, and an inventory that cannot resolve one has to discard everything.\n"
   },
   "quantity": {
    "type": "number"
   },
   "receivedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "supplierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "quarantined",
     "expired",
     "recalled",
     "consumed",
     "written-off"
    ]
   }
  }
 },
 "StockValuation": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asAt",
   "total",
   "byLocation"
  ],
  "properties": {
   "asAt": {
    "type": "string",
    "format": "date"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "byLocation": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "locationId": {
       "type": "string",
       "format": "uuid"
      },
      "locationName": {
       "type": "string"
      },
      "value": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "itemCount": {
       "type": "integer"
      }
     }
    }
   },
   "byCategory": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "categoryId": {
       "type": "string",
       "format": "uuid"
      },
      "categoryName": {
       "type": "string"
      },
      "value": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
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
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n",
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
   "scenario"
  ]
 },
 "SuggestionOutcome": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion_outcome",
  "description": "**What actually happened, and this is the table that makes the swap possible at all.**\nA model needs labelled data and **the only source of labels is whether the venue took the advice and whether it worked.** A platform that suggests and never records the outcome has no training set a year later, and the swap he is planning for never happens.\n**Captured whether or not the suggestion was taken.** A rejected suggestion is a stronger signal than an accepted one — it is the case the rule got wrong.\n",
  "required": [
   "id",
   "suggestionId",
   "decision"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "suggestionId": {
    "type": "string",
    "format": "uuid"
   },
   "decision": {
    "type": "string",
    "enum": [
     "accepted",
     "modified",
     "rejected",
     "ignored",
     "expired"
    ]
   },
   "actualValue": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "What the venue did instead. **The label.** A suggestion of 400 units, an order of 250, and a stockout on Saturday is one training example worth more than a hundred accepted ones.\n"
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   },
   "realisedOutcome": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "**Filled in later by a job, not by a person.** Whether the stockout happened, whether the covers arrived, whether the margin held — nobody comes back to record this by hand, so nothing that depends on them doing so should be designed.\n"
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 }
}
```
