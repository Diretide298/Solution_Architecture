# WS85 — Game and Ride board 8

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-464` | Game & Ride Operations Control Center | listDetail | 0 | 0 | — |
| `BO-465` | Live Gameplay Transaction Monitor | listDetail | 0 | 0 | — |
| `BO-466` | Reader & Device Health Monitor | listDetail | 0 | 0 | — |
| `BO-467` | Tap Validation & Decision Trace | listDetail | 0 | 0 | — |
| `BO-468` | Rejected Transaction & Reason Analysis | commandCentre | 0 | 0 | — |
| `BO-469` | Wallet & Deduction Transaction Monitor | listDetail | 0 | 0 | — |
| `BO-470` | Entitlement & Free-Play Consumption Monitor | commandCentre | 0 | 0 | — |
| `BO-471` | Offline, Synchronization & Recovery Monitor | listDetail | 0 | 0 | — |
| `BO-472` | Operational Alerts & Exception Center | listDetail | 0 | 0 | — |
| `BO-473` | Operational Analytics & Reconciliation Dashboard | listDetail | 0 | 0 | — |

## Thin screens in this batch

**BO-464, BO-465, BO-466, BO-467, BO-469, BO-471, BO-472, BO-473 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-464",
  "name": "Game & Ride Operations Control Center",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "1",
   "page": 74
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/game-ride-operations-control-center-bo-464",
   "component": "apps/venue-management-web/src/routes/games-rides/GameRideOperationsControlCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-465",
    "BO-466",
    "BO-467",
    "BO-468",
    "BO-469",
    "BO-470",
    "BO-471",
    "BO-472",
    "BO-473"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-465",
     "trigger": "Live Gameplay Transaction Monitor",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-466",
     "trigger": "Reader & Device Health Monitor",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-467",
     "trigger": "Tap Validation & Decision Trace",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-468",
     "trigger": "Rejected Transaction & Reason Analysis",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-469",
     "trigger": "Wallet & Deduction Transaction Monitor",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-470",
     "trigger": "Entitlement & Free-Play Consumption Monitor",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-471",
     "trigger": "Offline, Synchronization & Recovery Monitor",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-472",
     "trigger": "Operational Alerts & Exception Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-473",
     "trigger": "Operational Analytics & Reconciliation Dashboard",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can determine overall system health and transaction activity from one screen.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the main real-time operational dashboard for the entire game/ride ecosystem.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 74"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search game ride operations",
       "provenance": "pack Game_and_Ride_Module.pdf, page 74 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Client",
        "Venue",
        "Zone",
        "Attraction Type",
        "Attraction",
        "Reader",
        "Status"
       ],
       "notes": "The pack filters this screen by client, venue, zone, attraction type, attraction, reader and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 74 §Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The game ride operations list.",
   "error": "Could not load. Names which read failed and leaves the game ride operations untouched.",
   "emptyFirstRun": "No game ride operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the game ride operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-464"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 74. 0 of 7 labels bound to a contract property; 7 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-465",
  "name": "Live Gameplay Transaction Monitor",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "2",
   "page": 75
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/live-gameplay-transaction-monitor-bo-465",
   "component": "apps/venue-management-web/src/routes/games-rides/LiveGameplayTransactionMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-464"
   ],
   "exitTo": [
    "BO-464"
   ],
   "transitions": [
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized operators can monitor gameplay transactions in near real time and open an individual transaction for investigation.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Selecting a transaction should show) and no metric row",
  "purpose": "Display gameplay transactions as they occur across all connected readers.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 75 §Selecting a transaction should show"
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
       "label": "Every live gameplay transaction",
       "columns": [
        "Transaction ID",
        "Card/credential",
        "Wallet",
        "Reader",
        "Attraction",
        "Price rule",
        "Funding source",
        "Before balance",
        "Deduction",
        "After balance",
        "Authorization result",
        "Response time"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 75 §Selecting a transaction should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected live gameplay transaction",
       "bindsTo": null,
       "columns": [
        "Transaction ID",
        "Card/credential",
        "Wallet",
        "Reader",
        "Attraction",
        "Price rule",
        "Funding source",
        "Before balance",
        "Deduction",
        "After balance",
        "Authorization result",
        "Response time"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Live Transaction Feed”, “Transaction Sources”, “Live Status”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 75 §Selecting a transaction should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The live gameplay transaction list.",
   "error": "Could not load. Names which read failed and leaves the live gameplay transaction untouched.",
   "emptyFirstRun": "No live gameplay transaction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the live gameplay transaction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Transaction ID",
    "Card/credential",
    "Wallet",
    "Reader",
    "Attraction",
    "Price rule"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-465"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 75. 0 of 12 labels bound to a contract property; 12 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-466",
  "name": "Reader & Device Health Monitor",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "3",
   "page": 76
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-device-health-monitor-bo-466",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderDeviceHealthMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-464"
   ],
   "exitTo": [
    "BO-464"
   ],
   "transitions": [
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can immediately identify reader/device communication failures and configuration synchronization problems.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor communication and operational status of the physical Chinese readers and other connected devices.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 76"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 76"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The reader device health list.",
   "error": "Could not load. Names which read failed and leaves the reader device health untouched.",
   "emptyFirstRun": "No reader device health yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reader device health are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-466"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 76. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-467",
  "name": "Tap Validation & Decision Trace",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "4",
   "page": 77
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/tap-validation-decision-trace-bo-467",
   "component": "apps/venue-management-web/src/routes/games-rides/TapValidationDecisionTrace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-464"
   ],
   "exitTo": [
    "BO-464"
   ],
   "transitions": [
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operators can trace every major rule evaluated during an authorization decision.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow operations to understand exactly how TICVAI reached an approval or rejection decision for an individual customer tap. This relates directly to the requirement that balance, bonus and entitlements be validated in real time before gameplay.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 77"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 77"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The tap validation decision list.",
   "error": "Could not load. Names which read failed and leaves the tap validation decision untouched.",
   "emptyFirstRun": "No tap validation decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tap validation decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-467"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 77. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-468",
  "name": "Rejected Transaction & Reason Analysis",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "5",
   "page": 78
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/rejected-transaction-reason-analysis-bo-468",
   "component": "apps/venue-management-web/src/routes/games-rides/RejectedTransactionReasonAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-464"
   ],
   "exitTo": [
    "BO-464"
   ],
   "transitions": [
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can identify whether rejection spikes originate from customer conditions, configuration errors or technical problems.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Rejection KPIs) and a per-row directory (§Time Attraction Card Reason Reader; Show) — counts over a population, then the population",
  "purpose": "Centralize all rejected gameplay transactions and identify why customers are being denied.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 78 §Time Attraction Card Reason Reader"
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
       "label": "Rejections Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 78 §Rejection KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Rejection Rate",
       "provenance": "pack Game_and_Ride_Module.pdf, page 78 §Rejection KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Insufficient Balance",
       "provenance": "pack Game_and_Ride_Module.pdf, page 78 §Rejection KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Invalid/Expired Card",
       "provenance": "pack Game_and_Ride_Module.pdf, page 78 §Rejection KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Entitlement Failure",
       "provenance": "pack Game_and_Ride_Module.pdf, page 78 §Rejection KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Retap Protection",
       "provenance": "pack Game_and_Ride_Module.pdf, page 78 §Rejection KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Reader/Technical Failure",
       "provenance": "pack Game_and_Ride_Module.pdf, page 78 §Rejection KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every rejected transaction reason",
       "columns": [
        "10:42 VR Racing ****3321 Insufficient Balance R-014",
        "10:40 Bumper Cars ****2178 Card Expired R-007",
        "10:38 Basketball ****6621 Retap Too Soon R-023",
        "Rejections by attraction",
        "Rejections by reader",
        "Rejections by reason",
        "Rejection trend"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 78 §Time Attraction Card Reason Reader"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rejected transaction reason",
       "bindsTo": null,
       "columns": [
        "10:42 VR Racing ****3321 Insufficient Balance R-014",
        "10:40 Bumper Cars ****2178 Card Expired R-007",
        "10:38 Basketball ****6621 Retap Too Soon R-023",
        "Rejections by attraction",
        "Rejections by reader",
        "Rejections by reason",
        "Rejection trend"
       ],
       "notes": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 78 §Time Attraction Card Reason Reader"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rejected transaction reason list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rejected transaction reason untouched.",
   "emptyFirstRun": "No rejected transaction reason yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rejected transaction reason are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Rejections Today",
    "Rejection Rate",
    "Insufficient Balance",
    "Invalid/Expired Card",
    "Entitlement Failure",
    "Retap Protection"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-468"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 78. 0 of 7 labels bound to a contract property; 14 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-469",
  "name": "Wallet & Deduction Transaction Monitor",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "6",
   "page": 79
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/wallet-deduction-transaction-monitor-bo-469",
   "component": "apps/venue-management-web/src/routes/games-rides/WalletDeductionTransactionMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-464"
   ],
   "exitTo": [
    "BO-464"
   ],
   "transitions": [
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every gameplay authorization involving wallet value can be traced to its corresponding deduction.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor the financial/value movement generated by game and ride activity. The source requires the customer's amount to be deducted after the card tap based on available balance and the remaining balance to be updated.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 79"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 79"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The wallet deduction transaction list.",
   "error": "Could not load. Names which read failed and leaves the wallet deduction transaction untouched.",
   "emptyFirstRun": "No wallet deduction transaction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet deduction transaction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-469"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 79. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-470",
  "name": "Entitlement & Free-Play Consumption Monitor",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "7",
   "page": 80
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/entitlement-free-play-consumption-monitor-bo-470",
   "component": "apps/venue-management-web/src/routes/games-rides/EntitlementFreePlayConsumptionMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-464"
   ],
   "exitTo": [
    "BO-464"
   ],
   "transitions": [
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can trace entitlement consumption and remaining usage without changing the entitlement configuration.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Monitor consumption of packages, passes, limited plays, unlimited entitlements and free-game credits.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Entitlement Plays Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 80 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Free Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 80 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Package Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 80 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Unlimited Pass Uses",
       "provenance": "pack Game_and_Ride_Module.pdf, page 80 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Limited Plays Remaining",
       "provenance": "pack Game_and_Ride_Module.pdf, page 80 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Failed Entitlement Attempts",
       "provenance": "pack Game_and_Ride_Module.pdf, page 80 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entitlement free-play consumption list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the entitlement free-play consumption untouched.",
   "emptyFirstRun": "No entitlement free-play consumption yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entitlement free-play consumption are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Entitlement Plays Today",
    "Free Plays",
    "Package Plays",
    "Unlimited Pass Uses",
    "Limited Plays Remaining",
    "Failed Entitlement Attempts"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-470"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 80. 0 of 0 labels bound to a contract property; 6 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-471",
  "name": "Offline, Synchronization & Recovery Monitor",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "8",
   "page": 80
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/offline-synchronization-recovery-monitor-bo-471",
   "component": "apps/venue-management-web/src/routes/games-rides/OfflineSynchronizationRecoveryMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-464"
   ],
   "exitTo": [
    "BO-464"
   ],
   "transitions": [
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Where supported by the selected reader/gateway architecture, TICVAI can identify offline devices and reconcile transactions after connectivity returns. The exact offline capability must ultimately depend on the Chinese reader's SDK, local storage and communication architecture.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor readers or edge components that temporarily lose connectivity with TICVAI and manage recovery/synchronization. This is a TICVAI Recommended Enhancement, based on the architecture we agreed for physical readers.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 80"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 80"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The offline synchronization recovery list.",
   "error": "Could not load. Names which read failed and leaves the offline synchronization recovery untouched.",
   "emptyFirstRun": "No offline synchronization recovery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline synchronization recovery are still there. The pack's own statuses are Online — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-471"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 80. 0 of 0 labels bound to a contract property; 7 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-472",
  "name": "Operational Alerts & Exception Center",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "9",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/operational-alerts-exception-center-bo-472",
   "component": "apps/venue-management-web/src/routes/games-rides/OperationalAlertsExceptionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-464"
   ],
   "exitTo": [
    "BO-464"
   ],
   "transitions": [
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operational exceptions can be prioritized, assigned and resolved through a central operational queue.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Card) and no metric row",
  "purpose": "Provide one central queue for operational problems requiring attention.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 81 §Card"
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
       "label": "Every operational alerts exception",
       "columns": [
        "Expiry/Status Issue"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 81 §Card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected operational alerts exception",
       "bindsTo": null,
       "columns": [
        "Expiry/Status Issue"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Reader”, “Transaction”, “Wallet”, “Pricing”, “Redemption”, “Severity Alert Attraction Age Status”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 81 §Card"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operational alerts exception list.",
   "error": "Could not load. Names which read failed and leaves the operational alerts exception untouched.",
   "emptyFirstRun": "No operational alerts exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational alerts exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Expiry/Status Issue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-472"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 81. 0 of 1 labels bound to a contract property; 1 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-473",
  "name": "Operational Analytics & Reconciliation Dashboard",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "8",
   "number": "10",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/operational-analytics-reconciliation-dashboard-bo-473",
   "component": "apps/venue-management-web/src/routes/games-rides/OperationalAnalyticsReconciliationDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-464"
   ],
   "exitTo": [
    "BO-464"
   ],
   "transitions": [
    {
     "to": "BO-464",
     "trigger": "Back to Game & Ride Operations Control Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can evaluate the operational and financial performance of the game/ride ecosystem and identify reconciliation discrepancies. Board 8 — Exact Screen Mapping The Board 8 visual must contain exactly these 10 screens in this order: # Screen 1 Game & Ride Operations Control Center 2 Live Gameplay Transaction Monitor 3 Reader & Device Health Monitor 4 Tap Validation & Decision Trace 5 Rejected Transaction & Reason Analysis 6 Wallet & Deduction Transaction Monitor 7 Entitlement & Free-Play Consumption Monitor 8 Offline, Synchronization & Recovery Monitor 9 Operational Alerts & Exception Ce",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide management and operations with consolidated performance analytics across gameplay, readers, wallets and redemption.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 82"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 82"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The operational analytics reconciliation list.",
   "error": "Could not load. Names which read failed and leaves the operational analytics reconciliation untouched.",
   "emptyFirstRun": "No operational analytics reconciliation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational analytics reconciliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-473"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 82. 0 of 0 labels bound to a contract property; 0 of 83 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
