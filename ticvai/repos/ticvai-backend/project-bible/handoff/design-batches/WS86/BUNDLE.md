# WS86 — Game and Ride board 9

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
| `BO-474` | Reader Integration Command Center | commandCentre | 0 | 0 | — |
| `BO-475` | Reader Manufacturer & Model Profile | configEditor | 0 | 0 | — |
| `BO-476` | Communication Protocol Configuration | configEditor | 0 | 0 | — |
| `BO-477` | Reader Command & Event Mapping | listDetail | 0 | 0 | — |
| `BO-478` | Reader Configuration Deployment & Synchronization | listDetail | 0 | 0 | — |
| `BO-479` | Game Trigger & I/O Control Mapping | listDetail | 0 | 0 | — |
| `BO-480` | Reader Screen, LED & Sound Output Mapping | listDetail | 0 | 0 | — |
| `BO-481` | Edge Cache & Offline Rule Package | listDetail | 0 | 0 | — |
| `BO-482` | Device Diagnostics & Integration Logs | listDetail | 0 | 0 | — |
| `BO-483` | Integration Certification & Test Console | listDetail | 0 | 0 | — |

## Thin screens in this batch

**BO-477, BO-478, BO-479, BO-480, BO-481, BO-482, BO-483 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-474",
  "name": "Reader Integration Command Center",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "1",
   "page": 86
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-integration-command-center-bo-474",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderIntegrationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-475",
    "BO-476",
    "BO-477",
    "BO-478",
    "BO-479",
    "BO-480",
    "BO-481",
    "BO-482",
    "BO-483"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-475",
     "trigger": "Reader Manufacturer & Model Profile",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-476",
     "trigger": "Communication Protocol Configuration",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-477",
     "trigger": "Reader Command & Event Mapping",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-478",
     "trigger": "Reader Configuration Deployment & Synchronization",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-479",
     "trigger": "Game Trigger & I/O Control Mapping",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-480",
     "trigger": "Reader Screen, LED & Sound Output Mapping",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-481",
     "trigger": "Edge Cache & Offline Rule Package",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-482",
     "trigger": "Device Diagnostics & Integration Logs",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "BO-483",
     "trigger": "Integration Certification & Test Console",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Technical administrators can see the health and synchronization state of all reader integrations centrally.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide the technical team with a centralized view of every reader integration deployed across TICVAI clients and venues.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search reader integration",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Client",
        "Venue",
        "Manufacturer",
        "Model",
        "Protocol",
        "Status",
        "Configuration Version"
       ],
       "notes": "The pack filters this screen by client, venue, manufacturer, model, protocol, status and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Integrated Readers",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Online",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Offline",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Integration Errors",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Pending Configuration Sync",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Transactions Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Response Time",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Protocol Errors",
       "provenance": "pack Game_and_Ride_Module.pdf, page 86 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reader integration list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the reader integration untouched.",
   "emptyFirstRun": "No reader integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reader integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-474"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 86. 0 of 7 labels bound to a contract property; 15 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-475",
  "name": "Reader Manufacturer & Model Profile",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "2",
   "page": 87
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-manufacturer-model-profile-bo-475",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderManufacturerModelProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-474"
   ],
   "exitTo": [
    "BO-474"
   ],
   "transitions": [
    {
     "to": "BO-474",
     "trigger": "Back to Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure supported capabilities) and no display directory — it is settings, not a population",
  "purpose": "Allow TICVAI to support multiple reader manufacturers/models without building business rules specifically for one Chinese reader.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "☑ RFID",
       "provenance": "pack Game_and_Ride_Module.pdf, page 87 §Configure supported capabilities"
      },
      {
       "kind": "selectField",
       "label": "☑ NFC",
       "provenance": "pack Game_and_Ride_Module.pdf, page 87 §Configure supported capabilities"
      },
      {
       "kind": "selectField",
       "label": "☑ Screen",
       "provenance": "pack Game_and_Ride_Module.pdf, page 87 §Configure supported capabilities"
      },
      {
       "kind": "textField",
       "label": "☑ LED / RGB Lighting",
       "provenance": "pack Game_and_Ride_Module.pdf, page 87 §Configure supported capabilities"
      },
      {
       "kind": "selectField",
       "label": "☑ Sound",
       "provenance": "pack Game_and_Ride_Module.pdf, page 87 §Configure supported capabilities"
      },
      {
       "kind": "selectField",
       "label": "☑ Touch Screen",
       "provenance": "pack Game_and_Ride_Module.pdf, page 87 §Configure supported capabilities"
      },
      {
       "kind": "selectField",
       "label": "☑ Local Storage",
       "provenance": "pack Game_and_Ride_Module.pdf, page 87 §Configure supported capabilities"
      },
      {
       "kind": "selectField",
       "label": "☑ I/O Output",
       "provenance": "pack Game_and_Ride_Module.pdf, page 87 §Configure supported capabilities"
      },
      {
       "kind": "selectField",
       "label": "☑ Network Connectivity",
       "provenance": "pack Game_and_Ride_Module.pdf, page 87 §Configure supported capabilities"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reader manufacturer model configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the reader manufacturer model untouched.",
   "emptyFirstRun": "No reader manufacturer model configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-475"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 87. 0 of 0 labels bound to a contract property; 9 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-476",
  "name": "Communication Protocol Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "3",
   "page": 88
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/communication-protocol-configuration-bo-476",
   "component": "apps/venue-management-web/src/routes/games-rides/CommunicationProtocolConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-474"
   ],
   "exitTo": [
    "BO-474"
   ],
   "transitions": [
    {
     "to": "BO-474",
     "trigger": "Back to Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Technical administrators can configure and validate communication between TICVAI and supported reader hardware.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Connection Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure how TICVAI communicates with each reader/device family.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Protocol",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      },
      {
       "kind": "selectField",
       "label": "Host / IP",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      },
      {
       "kind": "selectField",
       "label": "Port",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      },
      {
       "kind": "selectField",
       "label": "Endpoint",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      },
      {
       "kind": "selectField",
       "label": "Authentication",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      },
      {
       "kind": "selectField",
       "label": "Timeout",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      },
      {
       "kind": "selectField",
       "label": "Retry Count",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      },
      {
       "kind": "selectField",
       "label": "Heartbeat Interval",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      },
      {
       "kind": "selectField",
       "label": "Encryption",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      },
      {
       "kind": "selectField",
       "label": "Connection Mode",
       "provenance": "pack Game_and_Ride_Module.pdf, page 88 §Connection Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The communication protocol configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the communication protocol untouched.",
   "emptyFirstRun": "No communication protocol configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-476"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 88. 0 of 0 labels bound to a contract property; 10 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-477",
  "name": "Reader Command & Event Mapping",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "4",
   "page": 89
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-command-event-mapping-bo-477",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderCommandEventMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-474"
   ],
   "exitTo": [
    "BO-474"
   ],
   "transitions": [
    {
     "to": "BO-474",
     "trigger": "Back to Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "reader's protocol.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Translate TICVAI's standardized commands into the specific commands understood by each reader manufacturer. This is one of the most important architectural screens. DISPLAY_PRICE DISPLAY_MESSAGE LED_COLOR APPROVE_PLAY REJECT_PLAY TRIGGER_GAME SHOW_BALANCE SYNC_CONFIG",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 89"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 89"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The reader command event list.",
   "error": "Could not load. Names which read failed and leaves the reader command event untouched.",
   "emptyFirstRun": "No reader command event yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reader command event are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-477"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 89. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-478",
  "name": "Reader Configuration Deployment & Synchronization",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "5",
   "page": 89
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-configuration-deployment-synchronization-bo-478",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderConfigurationDeploymentSynchronization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-474"
   ],
   "exitTo": [
    "BO-474"
   ],
   "transitions": [
    {
     "to": "BO-474",
     "trigger": "Back to Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Push backend configuration from TICVAI to readers where local configuration is required.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 89"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 89"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The reader deployment synchronization list.",
   "error": "Could not load. Names which read failed and leaves the reader deployment synchronization untouched.",
   "emptyFirstRun": "No reader deployment synchronization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reader deployment synchronization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-478"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 89. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-479",
  "name": "Game Trigger & I/O Control Mapping",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "6",
   "page": 90
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/game-trigger-i-o-control-mapping-bo-479",
   "component": "apps/venue-management-web/src/routes/games-rides/GameTriggerIOControlMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-474"
   ],
   "exitTo": [
    "BO-474"
   ],
   "transitions": [
    {
     "to": "BO-474",
     "trigger": "Back to Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Card Tap) and no metric row",
  "purpose": "Configure how an approved TICVAI transaction physically starts a game or ride.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 90 §Card Tap"
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
       "label": "Every game trigger mapping",
       "columns": [
        "→ TICVAI Authorization",
        "→ APPROVED",
        "→ Reader receives command",
        "→ Reader sends output",
        "→ Game Controller",
        "→ GAME START"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 90 §Card Tap"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected game trigger mapping",
       "bindsTo": null,
       "columns": [
        "→ TICVAI Authorization",
        "→ APPROVED",
        "→ Reader receives command",
        "→ Reader sends output",
        "→ Game Controller",
        "→ GAME START"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Depending on hardware”, “Page 90 of 105”, “Basketball Pro”, “Potential inputs”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 90 §Card Tap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The game trigger mapping list.",
   "error": "Could not load. Names which read failed and leaves the game trigger mapping untouched.",
   "emptyFirstRun": "No game trigger mapping yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the game trigger mapping are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "→ TICVAI Authorization",
    "→ APPROVED",
    "→ Reader receives command",
    "→ Reader sends output",
    "→ Game Controller",
    "→ GAME START"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-479"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 90. 0 of 6 labels bound to a contract property; 6 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-480",
  "name": "Reader Screen, LED & Sound Output Mapping",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "7",
   "page": 91
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-screen-led-sound-output-mapping-bo-480",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderScreenLedSoundOutputMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-474"
   ],
   "exitTo": [
    "BO-474"
   ],
   "transitions": [
    {
     "to": "BO-474",
     "trigger": "Back to Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Map TICVAI transaction results to the physical reader's screen, lighting and sound capabilities. This supports the matrix requirement for free-game color indication and custom reader themes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 91"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 91"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The reader screen led list.",
   "error": "Could not load. Names which read failed and leaves the reader screen led untouched.",
   "emptyFirstRun": "No reader screen led yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reader screen led are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-480"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 91. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-481",
  "name": "Edge Cache & Offline Rule Package",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "8",
   "page": 92
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/edge-cache-offline-rule-package-bo-481",
   "component": "apps/venue-management-web/src/routes/games-rides/EdgeCacheOfflineRulePackage.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-474"
   ],
   "exitTo": [
    "BO-474"
   ],
   "transitions": [
    {
     "to": "BO-474",
     "trigger": "Back to Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Where supported by the selected reader/gateway, controlled offline operation can continue without allowing unrestricted financial exposure.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure what information can be securely distributed to the edge/reader or local gateway for temporary offline operation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 92"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 92"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The edge cache offline list.",
   "error": "Could not load. Names which read failed and leaves the edge cache offline untouched.",
   "emptyFirstRun": "No edge cache offline yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the edge cache offline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-481"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 92. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-482",
  "name": "Device Diagnostics & Integration Logs",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "9",
   "page": 93
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/device-diagnostics-integration-logs-bo-482",
   "component": "apps/venue-management-web/src/routes/games-rides/DeviceDiagnosticsIntegrationLogs.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-474"
   ],
   "exitTo": [
    "BO-474"
   ],
   "transitions": [
    {
     "to": "BO-474",
     "trigger": "Back to Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Technical teams can trace communication from TICVAI through the reader to the game/controller and identify the point of failure.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give development team / support teams detailed technical visibility when a reader or game is not operating correctly.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 93"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 93"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The device diagnostics integration list.",
   "error": "Could not load. Names which read failed and leaves the device diagnostics integration untouched.",
   "emptyFirstRun": "No device diagnostics integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the device diagnostics integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-482"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 93. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-483",
  "name": "Integration Certification & Test Console",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "9",
   "number": "10",
   "page": 93
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/integration-certification-test-console-bo-483",
   "component": "apps/venue-management-web/src/routes/games-rides/IntegrationCertificationTestConsole.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-474"
   ],
   "exitTo": [
    "BO-474"
   ],
   "transitions": [
    {
     "to": "BO-474",
     "trigger": "Back to Reader Integration Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A reader model cannot be marked as TICVAI-certified until all mandatory integration tests have passed.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Card; Display) and no metric row",
  "purpose": "Provide a controlled environment for testing and approving a new reader model before deployment. This is particularly important for your plan because you will purchase the hardware separately and TICVAI must verify that the reader supports everything required by the platform.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 93 §Card"
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
       "label": "Every integration certification test",
       "columns": [
        "RFID Tap",
        "NFC Tap",
        "Credential Reading",
        "Text",
        "Price",
        "Balance"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 93 §Card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected integration certification test",
       "bindsTo": null,
       "columns": [
        "RFID Tap",
        "NFC Tap",
        "Credential Reading",
        "Text",
        "Price",
        "Balance"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Connectivity”, “LED”, “Gameplay”, “Transactions”, “Offline”, “GR-X20 Reader”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 93 §Card"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The integration certification test list.",
   "error": "Could not load. Names which read failed and leaves the integration certification test untouched.",
   "emptyFirstRun": "No integration certification test yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration certification test are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "RFID Tap",
    "NFC Tap",
    "Credential Reading",
    "Text",
    "Price",
    "Balance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-483"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 93. 0 of 6 labels bound to a contract property; 6 of 75 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
