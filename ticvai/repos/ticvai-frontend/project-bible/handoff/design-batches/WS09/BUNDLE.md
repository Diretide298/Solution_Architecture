# WS09 — Access Control board 9

**10 screens · 19 operations · 28 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_POINT_CONFIGURE, AUDIT_VIEW, DEVICE_CONFIGURE, INCIDENT_MANAGE, SCOPE_VIEW, TICKET_LOOKUP, TURNSTILE_MODE_SET`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-224` | Live Access Operations Command Center | listDetail | 1 | 0 | — |
| `BO-225` | Podium Operations Console | listDetail | 5 | 4 | — |
| `BO-226` | Ticket & Credential Investigation Console | listDetail | 1 | 0 | — |
| `BO-227` | Validation Exception & Reason Code Manager | listDetail | 3 | 2 | — |
| `BO-228` | Manual Override & Supervisor Approval | configEditor | 1 | 0 | — |
| `BO-229` | Credential Disable, Blacklist & Whitelist Operations | listDetail | 1 | 0 | — |
| `BO-230` | Live Gate Mode & Lane Control | listDetail | 4 | 1 | — |
| `BO-231` | Queue, Throughput & Lane Optimization | listDetail | 1 | 0 | — |
| `BO-232` | Operational Incident & Exception Workspace | listDetail | 1 | 0 | — |
| `BO-233` | Operations Audit, Shift Handover & Control Summary | listDetail | 2 | 1 | — |

## Thin screens in this batch

**BO-226, BO-227, BO-229, BO-230, BO-231, BO-232, BO-233 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-224",
  "name": "Live Access Operations Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.1",
   "page": 116
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/live-access-operations-command-center-bo-224",
   "component": "apps/venue-management-web/src/routes/access-venue/LiveAccessOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-225",
    "BO-226",
    "BO-227",
    "BO-228",
    "BO-229",
    "BO-230",
    "BO-231",
    "BO-232",
    "BO-233"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "provenance": "derived — BO-100 declares entryState.params  and BO-224 holds none of them, so the edge carries nothing and BO-100 opens cold"
    },
    {
     "to": "BO-225",
     "trigger": "Works in Podium Operations Console",
     "provenance": "flow F119 step 1→2",
     "operation": "listLiveAccess"
    },
    {
     "to": "BO-226",
     "trigger": "Works in Ticket & Credential Investigation Console",
     "provenance": "flow F119 step 3→4",
     "operation": "listLiveAccess"
    },
    {
     "to": "BO-227",
     "trigger": "Works in Validation Exception & Reason Code Manager",
     "provenance": "flow F119 step 5→6",
     "operation": "listLiveAccess"
    },
    {
     "to": "BO-228",
     "trigger": "Works in Manual Override & Supervisor Approval",
     "provenance": "flow F119 step 7→8",
     "operation": "listLiveAccess"
    },
    {
     "to": "BO-229",
     "trigger": "Works in Credential Disable, Blacklist & Whitelist Operations",
     "provenance": "flow F119 step 9→10",
     "operation": "listLiveAccess"
    },
    {
     "to": "BO-231",
     "trigger": "Works in Queue, Throughput & Lane Optimization",
     "provenance": "flow F119 step 13→14",
     "operation": "listLiveAccess"
    },
    {
     "to": "BO-232",
     "trigger": "Works in Operational Incident & Exception Workspace",
     "provenance": "flow F119 step 15→16",
     "operation": "listLiveAccess"
    },
    {
     "to": "BO-233",
     "trigger": "Works in Operations Audit, Shift Handover & Control Summary",
     "provenance": "flow F119 step 17→18",
     "operation": "listLiveAccess"
    },
    {
     "to": "BO-230",
     "trigger": "Works in Live Gate Mode & Lane Control",
     "provenance": "flow F119 step 11→12",
     "operation": "listLiveAccess",
     "carries": [
      "accessPointId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can understand the live access state of the entire venue without opening individual device screens.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the venue control room with a real-time view of access operations across all gates, parks, zones, and attractions.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Guests Entered Today",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.guestsEnteredToday",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Guests Exited",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.guestsExited",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Guests Currently In Park",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.guestsCurrentlyInPark",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Valid Scans",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.validScans",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Rejected Scans",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.rejectedScans",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Yellow / Intervention Scans",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.yellowInterventionScans",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Overrides",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.overrides",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Active Gates",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.activeGates",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Offline Gates",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.offlineGates",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Average validation time in seconds",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.averageValidationTime",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Guests per minute",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.guestsMinute",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Active Operational Alerts",
       "bindsTo": "LiveAccessOperationsCommandCenterViewSummary.activeOperationalAlerts",
       "operation": "listLiveAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every live access operations",
       "bindsTo": "LiveAccessOperationsCommandCenterView",
       "operation": "listLiveAccess",
       "provenance": "pack Access Control Module_Reference.pdf, page 116 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected live access operations",
       "bindsTo": "LiveAccessOperationsCommandCenterView",
       "notes": "The pack groups this record's detail under its own headings: “Live Venue Map”, “Adventure Park”, “MAIN GATE 03”, “QUEUE WARNING”, “REJECTION SPIKE”, “DEVICE WARNING”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 116 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The live access operations list.",
   "error": "Could not load. Names which read failed and leaves the live access operations untouched.",
   "emptyFirstRun": "No live access operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the live access operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listLiveAccess",
    "contract": "access",
    "purpose": "Live Access Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "LiveAccessOperationsCommandCenterViewSummary.guestsEnteredToday",
    "LiveAccessOperationsCommandCenterViewSummary.guestsExited",
    "LiveAccessOperationsCommandCenterViewSummary.guestsCurrentlyInPark",
    "LiveAccessOperationsCommandCenterViewSummary.validScans",
    "LiveAccessOperationsCommandCenterViewSummary.rejectedScans",
    "LiveAccessOperationsCommandCenterViewSummary.yellowInterventionScans"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-224",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-224"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 116. 12 of 12 labels bound to a contract property; 12 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-225",
  "name": "Podium Operations Console",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.2",
   "page": 117
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/podium-operations-console-bo-225",
   "component": "apps/venue-management-web/src/routes/access-venue/PodiumOperationsConsole.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-224"
   ],
   "exitTo": [
    "BO-224"
   ],
   "inferred": false,
   "notes": "**Reached from BO-224, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-224",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F119 step 2→3",
     "operation": "listPodiumConsole"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized attendants can control assigned access devices from one operational interface.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the operational interface described in the matrix for attendants controlling one or more turnstiles.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every podium operations console",
       "bindsTo": "PodiumOperationsConsoleView",
       "operation": "listPodiumConsole",
       "provenance": "pack Access Control Module_Reference.pdf, page 117 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected podium operations console",
       "bindsTo": "PodiumOperationsConsoleView",
       "notes": "The pack groups this record's detail under its own headings: “The podium may be”, “Controls”, “Operator”, “Shift”, “Authorized actions”, “Important”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 117 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save podium",
       "operation": "setPodium",
       "permission": "DEVICE_CONFIGURE",
       "notes": "**A podium is an attendant interface that controls one or more access points** (BO-225 Podium Operations Console): a physical panel, tablet, workstation or handheld.",
       "provenance": "contract access.yaml PUT /podiums"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete podium",
       "operation": "deletePodium",
       "permission": "DEVICE_CONFIGURE",
       "notes": "Deletes a podium.",
       "provenance": "contract access.yaml DELETE /podiums/{podiumId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Start podium shift",
       "operation": "startPodiumShift",
       "permission": "TURNSTILE_MODE_SET",
       "notes": "**The operator signs in to a podium** (BO-225; P07 SCN-002 where the scanner picks its access point).",
       "provenance": "contract access.yaml POST /podiums/{podiumId}/shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "End podium shift",
       "operation": "endPodiumShift",
       "permission": "TURNSTILE_MODE_SET",
       "notes": "**The operator signs out of the podium**: sets `logoutAt`.",
       "provenance": "contract access.yaml POST /podium-shifts/{shiftId}/end"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The podium operations console list.",
   "error": "Could not load. Names which read failed and leaves the podium operations console untouched.",
   "emptyFirstRun": "No podium operations console yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the podium operations console are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPodiumConsole",
    "contract": "access",
    "purpose": "Podium Operations Console",
    "trigger": "onLoad"
   },
   {
    "operationId": "setPodium",
    "contract": "access",
    "purpose": "Create or replace a podium",
    "trigger": "onAction",
    "invalidates": [
     "listPodiumConsole"
    ]
   },
   {
    "operationId": "deletePodium",
    "contract": "access",
    "purpose": "Delete a podium",
    "trigger": "onAction",
    "invalidates": [
     "listPodiumConsole"
    ]
   },
   {
    "operationId": "startPodiumShift",
    "contract": "access",
    "purpose": "Start an operator shift on a podium",
    "trigger": "onAction",
    "invalidates": [
     "listPodiumConsole"
    ]
   },
   {
    "operationId": "endPodiumShift",
    "contract": "access",
    "purpose": "End an operator shift on a podium",
    "trigger": "onAction",
    "invalidates": [
     "listPodiumConsole"
    ]
   }
  ],
  "entryState": {
   "preloaded": [],
   "params": [
    {
     "name": "shiftId",
     "from": "navigation",
     "optional": true
    },
    {
     "name": "podiumId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-225",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-225"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 117. 6 of 6 labels bound to a contract property; 6 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPodium",
    "component": "modal",
    "trigger": "Save podium",
    "body": "**Collects what `setPodium` sends before it is called.** Required: `id`, `venueId`, `podiumType`, `name`, `scopePath`. Optional: `accessPointIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessPodium",
    "confirm": {
     "label": "Save podium",
     "operation": "setPodium"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "podiumType",
      "name",
      "scopePath",
      "accessPointIds"
     ]
    },
    "provenance": "contract access.yaml PUT /podiums"
   },
   {
    "id": "confirmDeletePodium",
    "component": "confirmDialog",
    "trigger": "Delete podium",
    "body": "**Names what `deletePodium` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml DELETE /podiums/{podiumId}"
   },
   {
    "id": "formStartPodiumShift",
    "component": "modal",
    "trigger": "Start podium shift",
    "body": "**Collects what `startPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `role`, `accessDeviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Start podium shift",
     "operation": "startPodiumShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "role",
      "accessDeviceId"
     ]
    },
    "provenance": "contract access.yaml POST /podiums/{podiumId}/shifts"
   },
   {
    "id": "formEndPodiumShift",
    "component": "modal",
    "trigger": "End podium shift",
    "body": "**Collects what `endPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `handoverNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "End podium shift",
     "operation": "endPodiumShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "handoverNote"
     ]
    },
    "provenance": "contract access.yaml POST /podium-shifts/{shiftId}/end"
   }
  ],
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
  "id": "BO-226",
  "name": "Ticket & Credential Investigation Console",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.3",
   "page": 118
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ticket-credential-investigation-console-bo-226",
   "component": "apps/venue-management-web/src/routes/access-venue/TicketCredentialInvestigationConsole.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-224"
   ],
   "exitTo": [
    "BO-224"
   ],
   "inferred": false,
   "notes": "**Reached from BO-224, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-224",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F119 step 4→5",
     "operation": "listTicketCredentialInvestigation"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An operator can understand the ticket's complete operational access state from one screen without navigating across multiple modules.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow operators to quickly investigate why a guest cannot enter.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 118"
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
       "label": "Search ticket credential investigation",
       "provenance": "pack Access Control Module_Reference.pdf, page 118 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Ticket ID",
        "QR",
        "Barcode",
        "RFID",
        "NFC",
        "Virtual Credential ID",
        "Order Number",
        "Membership",
        "Guest Name",
        "Email",
        "Mobile"
       ],
       "notes": "The pack filters this screen by ticket id, qr, barcode, rfid, nfc, virtual credential id and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Access Control Module_Reference.pdf, page 118 §Search by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket credential investigation list.",
   "error": "Could not load. Names which read failed and leaves the ticket credential investigation untouched.",
   "emptyFirstRun": "No ticket credential investigation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket credential investigation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTicketCredentialInvestigation",
    "contract": "access",
    "purpose": "Ticket & Credential Investigation Console",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-226",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-226"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 118. 0 of 11 labels bound to a contract property; 11 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-227",
  "name": "Validation Exception & Reason Code Manager",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.4",
   "page": 120
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/validation-exception-reason-code-manager-bo-227",
   "component": "apps/venue-management-web/src/routes/access-venue/ValidationExceptionReasonCodeManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-224"
   ],
   "exitTo": [
    "BO-224"
   ],
   "inferred": false,
   "notes": "**Reached from BO-224, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-224",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F119 step 6→7",
     "operation": "listValidationExceptionReason"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every validation failure returns a standardized reason and configured operational response.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Standardize what happens when access is not automatically granted. The matrix requires the scanner to display a reason code when a ticket is invalid.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 120"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 120"
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
       "impliedBy": "listValidationExceptionReason",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save reason code",
       "operation": "setReasonCode",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind the Validation Exception & Reason Code Manager** (BO-227): one reason code (e.g.",
       "provenance": "contract access.yaml PUT /reason-codes"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete reason code",
       "operation": "deleteReasonCode",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "Deletes a reason code no scan has used.",
       "provenance": "contract access.yaml DELETE /reason-codes/{reasonCodeId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The validation exception reason list.",
   "error": "Could not load. Names which read failed and leaves the validation exception reason untouched.",
   "emptyFirstRun": "No validation exception reason yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the validation exception reason are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listValidationExceptionReason",
    "contract": "access",
    "purpose": "Validation Exception & Reason Code Manager",
    "trigger": "onLoad"
   },
   {
    "operationId": "setReasonCode",
    "contract": "access",
    "purpose": "Create or replace a validation reason code",
    "trigger": "onAction",
    "invalidates": [
     "listValidationExceptionReason"
    ]
   },
   {
    "operationId": "deleteReasonCode",
    "contract": "access",
    "purpose": "Delete a validation reason code",
    "trigger": "onAction",
    "invalidates": [
     "listValidationExceptionReason"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ValidationExceptionReasonCodeManagerView.operationalResponse"
   ],
   "params": [
    {
     "name": "reasonCodeId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-227",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-227"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 120. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetReasonCode",
    "component": "modal",
    "trigger": "Save reason code",
    "body": "**Collects what `setReasonCode` sends before it is called.** Required: `id`, `code`, `name`, `operationalResponse`, `scopePath`. Optional: `venueId`, `guestMessage`, `operatorMessage`, `followUpAction`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessReasonCode",
    "confirm": {
     "label": "Save reason code",
     "operation": "setReasonCode"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "operationalResponse",
      "scopePath",
      "venueId",
      "guestMessage",
      "operatorMessage",
      "followUpAction"
     ]
    },
    "provenance": "contract access.yaml PUT /reason-codes"
   },
   {
    "id": "confirmDeleteReasonCode",
    "component": "confirmDialog",
    "trigger": "Delete reason code",
    "body": "**Names what `deleteReasonCode` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml DELETE /reason-codes/{reasonCodeId}"
   }
  ],
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
  "id": "BO-228",
  "name": "Manual Override & Supervisor Approval",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.5",
   "page": 121
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/manual-override-supervisor-approval-bo-228",
   "component": "apps/venue-management-web/src/routes/access-venue/ManualOverrideSupervisorApproval.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-224"
   ],
   "exitTo": [
    "BO-224"
   ],
   "inferred": false,
   "notes": "**Reached from BO-224, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-224",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F119 step 8→9",
     "operation": "overrideAccess"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Only authorized users can override eligible rules, with reason, approval, timestamp, operator, device and original decision retained.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configured Date; Select) and no display directory — it is settings, not a population",
  "purpose": "Allow authorized staff to bypass selected access restrictions when operationally justified. The matrix explicitly requires Allow Override and operator-based ticket override.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "02 Sep",
       "provenance": "pack Access Control Module_Reference.pdf, page 121 §Configured Date"
      },
      {
       "kind": "selectField",
       "label": "Guest Service",
       "provenance": "pack Access Control Module_Reference.pdf, page 121 §Select"
      },
      {
       "kind": "selectField",
       "label": "Ticketing Error",
       "provenance": "pack Access Control Module_Reference.pdf, page 121 §Select"
      },
      {
       "kind": "selectField",
       "label": "Operational Exception",
       "provenance": "pack Access Control Module_Reference.pdf, page 121 §Select"
      },
      {
       "kind": "selectField",
       "label": "Management Authorization",
       "provenance": "pack Access Control Module_Reference.pdf, page 121 §Select"
      },
      {
       "kind": "selectField",
       "label": "Technical Failure",
       "provenance": "pack Access Control Module_Reference.pdf, page 121 §Select"
      },
      {
       "kind": "selectField",
       "label": "Event Exception",
       "provenance": "pack Access Control Module_Reference.pdf, page 121 §Select"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approve",
       "operation": "overrideAccess",
       "permission": "ACCESS_OVERRIDE",
       "provenance": "contract operation overrideAccess (decided 29 September, readiness close-out (QA wiring note))"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The manual override supervisor configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the manual override supervisor untouched.",
   "emptyFirstRun": "No manual override supervisor configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission, **ACCESS_OVERRIDE** (was ACCESS_POINT_CONFIGURE until 29 September, K1: recording an admission against a failed validation is an override, not gate configuration). Never an empty table."
  },
  "apis": [
   {
    "operationId": "overrideAccess",
    "contract": "access",
    "purpose": "Record a supervisor-approved manual override",
    "trigger": "onAction",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-228",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-228"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 121. 0 of 0 labels bound to a contract property; 7 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-229",
  "name": "Credential Disable, Blacklist & Whitelist Operations",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.6",
   "page": 122
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-disable-blacklist-whitelist-operations-bo-229",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialDisableBlacklistWhitelistOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-224"
   ],
   "exitTo": [
    "BO-224"
   ],
   "inferred": false,
   "notes": "**Reached from BO-224, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-224",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F119 step 10→11",
     "operation": "listCredentialDisableBlacklist"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can immediately restrict credential access across the configured venue environment.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide immediate operational security control over individual credentials.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 122"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 122"
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
       "impliedBy": "listCredentialDisableBlacklist",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential disable blacklist list.",
   "error": "Could not load. Names which read failed and leaves the credential disable blacklist untouched.",
   "emptyFirstRun": "No credential disable blacklist yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential disable blacklist are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialDisableBlacklist",
    "contract": "access",
    "purpose": "Credential Disable, Blacklist & Whitelist Operations",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialDisableBlacklistWhitelistOperationsView.reason",
    "CredentialDisableBlacklistWhitelistOperationsView.disableScope"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-229",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-229"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 122. 0 of 0 labels bound to a contract property; 0 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-230",
  "name": "Live Gate Mode & Lane Control",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.7",
   "page": 124
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/live-gate-mode-lane-control-bo-230",
   "component": "apps/venue-management-web/src/routes/access-venue/LiveGateModeLaneControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-224"
   ],
   "exitTo": [
    "BO-224"
   ],
   "inferred": false,
   "notes": "**Reached from BO-224, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-224",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F119 step 12→13",
     "operation": "listLiveGateMode"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can change the active mode of one or multiple authorized gates without modifying their underlying hardware configuration.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow operations to change access-point modes during live operations without entering the Board 6 engineering configuration. Board 6 defines which modes a device can support. Board 9 controls which permitted mode it is currently running.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every live gate mode",
       "columns": [
        "LiveGateModeLaneControlView.currentMode",
        "LiveGateModeLaneControlView.targetMode",
        "LiveGateModeLaneControlView.operator",
        "LiveGateModeLaneControlView.reason"
       ],
       "bindsTo": "LiveGateModeLaneControlView",
       "operation": "listLiveGateMode",
       "provenance": "pack Access Control Module_Reference.pdf, page 124 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected live gate mode",
       "bindsTo": "LiveGateModeLaneControlView",
       "columns": [
        "LiveGateModeLaneControlView.currentMode",
        "LiveGateModeLaneControlView.targetMode",
        "LiveGateModeLaneControlView.operator",
        "LiveGateModeLaneControlView.reason"
       ],
       "notes": "The pack groups this record's detail under its own headings: “ENTRY”, “Available”, “Bulk Command”, “Optional”, “Emergency”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 124 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Cancel gate mode change",
       "operation": "cancelGateModeChange",
       "permission": "TURNSTILE_MODE_SET",
       "notes": "Cancels a `pending` gate mode change, one `setTurnstileMode` scheduled with a future `effectiveAt`.",
       "provenance": "contract access.yaml POST /gate-mode-changes/{changeId}/cancel"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The live gate mode list.",
   "error": "Could not load. Names which read failed and leaves the live gate mode untouched.",
   "emptyFirstRun": "No live gate mode yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the live gate mode are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listLiveGateMode",
    "contract": "access",
    "purpose": "Live Gate Mode & Lane Control",
    "trigger": "onLoad"
   },
   {
    "operationId": "setTurnstileMode",
    "contract": "access",
    "purpose": "Switch a gate or lane mode live (entry, exit, free spin, closed)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listLiveGateMode"
    ]
   },
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "The gates and lanes whose mode is set",
    "trigger": "onLoad"
   },
   {
    "operationId": "cancelGateModeChange",
    "contract": "access",
    "purpose": "Cancel a scheduled gate mode change",
    "trigger": "onAction",
    "invalidates": [
     "listLiveGateMode",
     "listAccessPoints"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "LiveGateModeLaneControlView.currentMode",
    "LiveGateModeLaneControlView.targetMode",
    "LiveGateModeLaneControlView.operator",
    "LiveGateModeLaneControlView.reason"
   ],
   "params": [
    {
     "name": "accessPointId",
     "from": "navigation"
    },
    {
     "name": "changeId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-230",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-230"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 124. 5 of 5 labels bound to a contract property; 9 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "confirmCancelGateModeChange",
    "component": "confirmDialog",
    "trigger": "Cancel gate mode change",
    "body": "**Names what `cancelGateModeChange` changes and what it leaves alone**, in the consequence rather than the verb. A access gate mode change this affects should be identified in the dialog, not just counted. **Collects what `cancelGateModeChange` sends before it is called.** Nothing in the body is required. Optional: `reason`.",
    "provenance": "contract access.yaml POST /gate-mode-changes/{changeId}/cancel"
   }
  ],
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
  "id": "BO-231",
  "name": "Queue, Throughput & Lane Optimization",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.8",
   "page": 125
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/queue-throughput-lane-optimization-bo-231",
   "component": "apps/venue-management-web/src/routes/access-venue/QueueThroughputLaneOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-224"
   ],
   "exitTo": [
    "BO-224"
   ],
   "inferred": false,
   "notes": "**Reached from BO-224, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-224",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F119 step 14→15",
     "operation": "listQueueThroughputLane"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can monitor throughput and proactively adjust available lane capacity.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Manage entrance flow in real time. This addresses the matrix requirement to improve entrance flow and queuing, particularly for large B2B groups.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every queue throughput lane",
       "columns": [
        "QueueThroughputLaneOptimizationView.laneType"
       ],
       "bindsTo": "QueueThroughputLaneOptimizationView",
       "operation": "listQueueThroughputLane",
       "provenance": "pack Access Control Module_Reference.pdf, page 125 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected queue throughput lane",
       "bindsTo": "QueueThroughputLaneOptimizationView",
       "columns": [
        "QueueThroughputLaneOptimizationView.laneType"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Guests Waiting”, “Active Lanes”, “Current Throughput”, “Estimated Wait”, “Lane Performance”, “Reason”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 125 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The queue throughput lane list.",
   "error": "Could not load. Names which read failed and leaves the queue throughput lane untouched.",
   "emptyFirstRun": "No queue throughput lane yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the queue throughput lane are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQueueThroughputLane",
    "contract": "access",
    "purpose": "Queue, Throughput & Lane Optimization",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "QueueThroughputLaneOptimizationView.laneType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-231",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-231"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 125. 6 of 6 labels bound to a contract property; 6 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-232",
  "name": "Operational Incident & Exception Workspace",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.9",
   "page": 127
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/operational-incident-exception-workspace-bo-232",
   "component": "apps/venue-management-web/src/routes/access-venue/OperationalIncidentExceptionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-224"
   ],
   "exitTo": [
    "BO-224"
   ],
   "inferred": false,
   "notes": "**Reached from BO-224, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-224",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F119 step 16→17",
     "operation": "setOperationalIncidentException"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Complex access exceptions can be formally investigated and resolved with complete operational evidence.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage access incidents that require more than a simple override.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 127"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 127"
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
       "label": "Save changes",
       "operation": "setOperationalIncidentException",
       "permission": "INCIDENT_MANAGE",
       "provenance": "contract operation setOperationalIncidentException"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setOperationalIncidentException"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operational incident exception list.",
   "error": "Could not load. Names which read failed and leaves the operational incident exception untouched.",
   "emptyFirstRun": "No operational incident exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational incident exception are still there. The pack's own statuses are Open → Investigating → Resolved → Closed — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission, **INCIDENT_MANAGE** (was ACCESS_POINT_CONFIGURE until 29 September, K1: investigating, assigning and closing an incident is incident management, as for F&B and maintenance incidents). Never an empty table."
  },
  "apis": [
   {
    "operationId": "setOperationalIncidentException",
    "contract": "access",
    "purpose": "Operational Incident & Exception Workspace",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-232",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-232"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 127. 0 of 0 labels bound to a contract property; 1 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-233",
  "name": "Operations Audit, Shift Handover & Control Summary",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "9",
   "number": "9.10",
   "page": 128
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/operations-audit-shift-handover-control-summary-bo-233",
   "component": "apps/venue-management-web/src/routes/access-venue/OperationsAuditShiftHandoverControlSummary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-224"
   ],
   "exitTo": [
    "BO-224"
   ],
   "inferred": false,
   "notes": "**Reached from BO-224, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "Every operational intervention is attributable to a user and can be reviewed during audit, investigation and shift handover. Board 9 — Final 10-Screen Structure # Backend Screen Main Responsibility 9.1 Live Access Operations Command Center Real-time venue admission operations 9.2 Podium Operations Console Operator control of gates/turnstiles 9.3 Ticket & Credential Investigation Console Investigate guest access state",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide full accountability for everything operators and supervisors changed during live access operations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 128"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 128"
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
       "label": "Operations Audit, Shift Handover & Control",
       "provenance": "pack Access Control Module_Reference.pdf, page 128 §Operations"
      },
      {
       "kind": "secondaryButton",
       "label": "End podium shift",
       "operation": "endPodiumShift",
       "permission": "TURNSTILE_MODE_SET",
       "notes": "**The operator signs out of the podium**: sets `logoutAt`.",
       "provenance": "contract access.yaml POST /podium-shifts/{shiftId}/end"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listShiftHandoverSummary",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operations audit shift list.",
   "error": "Could not load. Names which read failed and leaves the operations audit shift untouched.",
   "emptyFirstRun": "No operations audit shift yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operations audit shift are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listShiftHandoverSummary",
    "contract": "access",
    "purpose": "Operations Audit, Shift Handover & Control Summary",
    "trigger": "onLoad"
   },
   {
    "operationId": "endPodiumShift",
    "contract": "access",
    "purpose": "End an operator shift on a podium",
    "trigger": "onAction",
    "invalidates": [
     "listShiftHandoverSummary"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "OperationsAuditShiftHandoverControlSummaryView.operator",
    "OperationsAuditShiftHandoverControlSummaryView.role",
    "OperationsAuditShiftHandoverControlSummaryView.podium",
    "OperationsAuditShiftHandoverControlSummaryView.device",
    "OperationsAuditShiftHandoverControlSummaryView.login"
   ],
   "params": [
    {
     "name": "shiftId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-233",
   "workshopBoard": "wireframes/WS26 Access Control Board 9.dc.html#bo-233"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 128. 0 of 0 labels bound to a contract property; 1 of 88 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Operations Audit, Shift Handover & Control dropped (heading (screen title fragment)).",
  "overlays": [
   {
    "id": "formEndPodiumShift",
    "component": "modal",
    "trigger": "End podium shift",
    "body": "**Collects what `endPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `handoverNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "End podium shift",
     "operation": "endPodiumShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "handoverNote"
     ]
    },
    "provenance": "contract access.yaml POST /podium-shifts/{shiftId}/end"
   }
  ],
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
 "cancelGateModeChange": {
  "method": "POST",
  "path": "/gate-mode-changes/{changeId}/cancel",
  "contract": "access",
  "summary": "Cancel a scheduled gate mode change",
  "permission": "TURNSTILE_MODE_SET",
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
  "responds": "AccessGateModeChange"
 },
 "deletePodium": {
  "method": "DELETE",
  "path": "/podiums/{podiumId}",
  "contract": "access",
  "summary": "Delete a podium",
  "permission": "DEVICE_CONFIGURE",
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
  "responds": null
 },
 "deleteReasonCode": {
  "method": "DELETE",
  "path": "/reason-codes/{reasonCodeId}",
  "contract": "access",
  "summary": "Delete a validation reason code",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "responds": null
 },
 "endPodiumShift": {
  "method": "POST",
  "path": "/podium-shifts/{shiftId}/end",
  "contract": "access",
  "summary": "End an operator shift on a podium",
  "permission": "TURNSTILE_MODE_SET",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccessPodiumShift"
 },
 "listAccessPoints": {
  "method": "GET",
  "path": "/access-points",
  "contract": "access",
  "summary": "List access points",
  "permission": "SCOPE_VIEW",
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
 "listCredentialDisableBlacklist": {
  "method": "GET",
  "path": "/credential-disable-blacklist",
  "contract": "access",
  "summary": "Credential Disable, Blacklist & Whitelist Operations",
  "permission": "SCOPE_VIEW",
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
 "listLiveAccess": {
  "method": "GET",
  "path": "/live-access",
  "contract": "access",
  "summary": "Live Access Operations Command Center",
  "permission": "SCOPE_VIEW",
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
 "listLiveGateMode": {
  "method": "GET",
  "path": "/live-gate-mode",
  "contract": "access",
  "summary": "Live Gate Mode & Lane Control",
  "permission": "SCOPE_VIEW",
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
 "listPodiumConsole": {
  "method": "GET",
  "path": "/podium-console",
  "contract": "access",
  "summary": "Podium Operations Console",
  "permission": "SCOPE_VIEW",
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
  "responds": "PodiumOperationsConsoleView"
 },
 "listQueueThroughputLane": {
  "method": "GET",
  "path": "/queue-throughput-lane",
  "contract": "access",
  "summary": "Queue, Throughput & Lane Optimization",
  "permission": "SCOPE_VIEW",
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
 "listShiftHandoverSummary": {
  "method": "GET",
  "path": "/shift-handover-summary",
  "contract": "access",
  "summary": "Operations Audit, Shift Handover & Control Summary",
  "permission": "AUDIT_VIEW",
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
 "listTicketCredentialInvestigation": {
  "method": "GET",
  "path": "/ticket-credential-investigation",
  "contract": "access",
  "summary": "Ticket & Credential Investigation Console",
  "permission": "TICKET_LOOKUP",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ticketId",
    "in": "query",
    "required": false
   },
   {
    "name": "qr",
    "in": "query",
    "required": false
   },
   {
    "name": "barcode",
    "in": "query",
    "required": false
   },
   {
    "name": "rfid",
    "in": "query",
    "required": false
   },
   {
    "name": "nfc",
    "in": "query",
    "required": false
   },
   {
    "name": "virtualCredentialId",
    "in": "query",
    "required": false
   },
   {
    "name": "orderNumber",
    "in": "query",
    "required": false
   },
   {
    "name": "membership",
    "in": "query",
    "required": false
   },
   {
    "name": "guestName",
    "in": "query",
    "required": false
   },
   {
    "name": "email",
    "in": "query",
    "required": false
   },
   {
    "name": "mobile",
    "in": "query",
    "required": false
   },
   {
    "name": "externalPartnerReference",
    "in": "query",
    "required": false
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
 "listValidationExceptionReason": {
  "method": "GET",
  "path": "/validation-exception-reason",
  "contract": "access",
  "summary": "Validation Exception & Reason Code Manager",
  "permission": "SCOPE_VIEW",
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
  "responds": "ValidationExceptionReasonCodeManagerView"
 },
 "overrideAccess": {
  "method": "POST",
  "path": "/access/override",
  "contract": "access",
  "summary": "Admit against a failed validation",
  "permission": "ACCESS_OVERRIDE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ValidationResult"
 },
 "setOperationalIncidentException": {
  "method": "PUT",
  "path": "/operational-incident-exception",
  "contract": "access",
  "summary": "Operational Incident & Exception Workspace",
  "permission": "INCIDENT_MANAGE",
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
  "requestBody": "OperationalIncidentExceptionWorkspaceInput",
  "responds": "OperationalIncidentExceptionWorkspaceView"
 },
 "setPodium": {
  "method": "PUT",
  "path": "/podiums",
  "contract": "access",
  "summary": "Create or replace a podium",
  "permission": "DEVICE_CONFIGURE",
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
  "requestBody": "AccessPodium",
  "responds": "AccessPodium"
 },
 "setReasonCode": {
  "method": "PUT",
  "path": "/reason-codes",
  "contract": "access",
  "summary": "Create or replace a validation reason code",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "AccessReasonCode",
  "responds": "AccessReasonCode"
 },
 "setTurnstileMode": {
  "method": "PUT",
  "path": "/access-points/{accessPointId}/mode",
  "contract": "access",
  "summary": "Set the operating mode of an access point",
  "permission": "TURNSTILE_MODE_SET",
  "offlineCapable": true,
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
  "responds": "AccessPoint"
 },
 "startPodiumShift": {
  "method": "POST",
  "path": "/podiums/{podiumId}/shifts",
  "contract": "access",
  "summary": "Start an operator shift on a podium",
  "permission": "TURNSTILE_MODE_SET",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccessPodiumShift"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessGateModeChange": {
  "type": "object",
  "x-ticvai-persistence": "access.gate_mode_change",
  "description": "One gate mode change on an access point, pending or applied: from and target mode, operator, reason and effective time. Append-only history (declared 29 September, data-model close-out DM1) Written by setTurnstileMode (applied at once, or pending until a future effectiveAt) and cancelGateModeChange; a timer applies a pending change at its effective time (decided 29 September, writers pass).",
  "required": [
   "id",
   "venueId",
   "accessPointId",
   "targetMode",
   "status",
   "changedByPrincipalId",
   "changedAt",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "fromMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ],
    "nullable": true
   },
   "targetMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "applied",
     "cancelled"
    ]
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "effectiveAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "changedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "Operator"
   },
   "changedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
   }
  }
 },
 "AccessPodium": {
  "type": "object",
  "x-ticvai-persistence": "access.podium",
  "description": "One podium: an attendant interface in a venue that controls one or more access points (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "venueId",
   "podiumType",
   "name",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "podiumType": {
    "type": "string",
    "enum": [
     "physicalControlPanel",
     "tablet",
     "workstation",
     "handheld",
     "other"
    ]
   },
   "name": {
    "type": "string",
    "description": "e.g. Main Entrance A"
   },
   "accessPointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Gates this podium controls"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AccessPodiumShift": {
  "type": "object",
  "x-ticvai-persistence": "access.podium_shift",
  "description": "One operator session on a podium or device: who, in what role, where, and login and logout times. Logout is null while the shift is open (declared 29 September, data-model close-out DM1) Written by startPodiumShift and endPodiumShift; an identity sign-out ends the open shift (decided 29 September, writers pass).",
  "required": [
   "id",
   "venueId",
   "operatorPrincipalId",
   "loginAt",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "role": {
    "type": "string",
    "nullable": true
   },
   "podiumId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accessDeviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Device used (access.access_device)"
   },
   "loginAt": {
    "type": "string",
    "format": "date-time"
   },
   "logoutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
   }
  }
 },
 "AccessPoint": {
  "x-ticvai-persistence": "access.access_point",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "operatingMode",
   "isActive"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "externalCredentialSources": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExternalCredentialSourceList"
     }
    ],
    "description": "BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"
   },
   "scanAnomalyRules": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ScanAnomalyRuleList"
     }
    ],
    "description": "BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"
   },
   "operatingMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ],
    "default": "normal",
    "description": "**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"
   },
   "vehicleLocationCapture": {
    "type": "boolean",
    "default": false,
    "description": "BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"
   },
   "mode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TurnstileMode"
     }
    ],
    "nullable": true,
    "description": "Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"
   },
   "direction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Direction"
     }
    ],
    "description": "**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"
   },
   "antiPassbackEnabled": {
    "type": "boolean"
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false,
    "description": "Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."
   },
   "driver": {
    "type": "string",
    "nullable": true,
    "description": "Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"
   },
   "geofence": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointGeofence"
     }
    ],
    "nullable": true,
    "description": "Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"
   },
   "isActive": {
    "type": "boolean"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "AccessPointGeofence": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n",
  "required": [
   "enforcement"
  ],
  "properties": {
   "latitude": {
    "type": "number"
   },
   "longitude": {
    "type": "number"
   },
   "radiusMetres": {
    "type": "integer",
    "minimum": 5,
    "maximum": 5000
   },
   "enforcement": {
    "type": "string",
    "enum": [
     "off",
     "warn",
     "deny"
    ],
    "description": "`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"
   },
   "allowProximityBeacon": {
    "type": "boolean",
    "description": "Accept a BLE proximity assertion in place of GPS. Better indoors."
   }
  }
 },
 "AccessPointOperatingMode": {
  "type": "string",
  "description": "BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n",
  "enum": [
   "normal",
   "freeFlow",
   "dropArm",
   "closed",
   "podium",
   "maintenance"
  ]
 },
 "AccessReasonCode": {
  "type": "object",
  "x-ticvai-persistence": "access.reason_code",
  "description": "One validation reason code in the catalogue: its name, guest and operator messages, the configured operational response and a follow-up hint (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "code",
   "name",
   "operationalResponse",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for a tenant-wide code"
   },
   "code": {
    "type": "string",
    "maxLength": 32,
    "description": "e.g. AC-002"
   },
   "name": {
    "type": "string",
    "description": "e.g. Wrong Visit Date"
   },
   "guestMessage": {
    "type": "string",
    "nullable": true
   },
   "operatorMessage": {
    "type": "string",
    "nullable": true
   },
   "operationalResponse": {
    "type": "string",
    "enum": [
     "deny",
     "operatorReview",
     "supervisorRequired",
     "allowWithWarning"
    ]
   },
   "followUpAction": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "CredentialDisableBlacklistWhitelistOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Disable, Blacklist & Whitelist Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "entryId": {
    "type": "string",
    "description": "List entry identifier"
   },
   "reason": {
    "type": "string",
    "enum": [
     "lostTicket",
     "stolenCredential",
     "fraudSuspected",
     "guestRemoval",
     "securityIncident",
     "duplicateCredential",
     "managementInstruction",
     "other"
    ],
    "description": "Reason"
   },
   "disableScope": {
    "type": "string",
    "enum": [
     "entireCredential",
     "venueAccess",
     "attractionAccess",
     "reEntry",
     "fastPass",
     "specificEntitlement"
    ],
    "description": "What is disabled"
   },
   "durationType": {
    "type": "string",
    "enum": [
     "permanent",
     "untilEndOfDay",
     "untilDateTime",
     "untilManuallyRestored"
    ],
    "description": "How long the restriction lasts"
   },
   "distributedTo": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "centralPlatform",
      "venueEdge",
      "onlineGates",
      "offlineRevocationPackage"
     ]
    },
    "description": "Where the restriction has been distributed"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential"
   },
   "listType": {
    "type": "string",
    "enum": [
     "blacklist",
     "whitelist"
    ],
    "description": "Blacklist or approved whitelist exception"
   },
   "until": {
    "type": "string",
    "format": "date-time",
    "description": "End of restriction when durationType is untilDateTime"
   },
   "createdBy": {
    "type": "string",
    "description": "Who applied it"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "description": "When it was applied"
   }
  },
  "required": [
   "entryId"
  ]
 },
 "DenyReason": {
  "type": "string",
  "description": "Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n",
  "enum": [
   "notFound",
   "notYetValid",
   "expired",
   "alreadyUsed",
   "reentryLimitReached",
   "exitRequiredBeforeReentry",
   "wrongAccessPoint",
   "wrongPerformance",
   "outsideAdmissionWindow",
   "entitlementSuspended",
   "blacklisted",
   "capacityReached",
   "waiverRequired",
   "accompanimentRequired",
   "mediaDeactivated",
   "unpaid",
   "delegatedRightExhausted",
   "delegatedRightRevoked",
   "journeyNotCovered"
  ]
 },
 "Direction": {
  "type": "string",
  "enum": [
   "entry",
   "exit",
   "reentry",
   "crossover"
  ]
 },
 "ExternalCredentialSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n",
  "items": {
   "type": "object",
   "properties": {
    "kind": {
     "type": "string",
     "enum": [
      "hotelRoomCard",
      "corporateBadge",
      "cityPass",
      "transitCard",
      "partnerToken"
     ]
    },
    "providerName": {
     "type": "string"
    },
    "endpoint": {
     "type": "string"
    },
    "credentialRef": {
     "type": "string"
    },
    "grantsProductId": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "LiveAccessOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Live Access Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "accessPointId": {
    "type": "string",
    "description": "Gate"
   },
   "name": {
    "type": "string",
    "description": "Gate name"
   },
   "mode": {
    "type": "string",
    "description": "Current gate mode"
   },
   "status": {
    "type": "string",
    "enum": [
     "online",
     "offline",
     "degraded"
    ],
    "description": "Gate status"
   },
   "queueLevel": {
    "type": "string",
    "enum": [
     "low",
     "moderate",
     "high"
    ],
    "description": "Queue level"
   },
   "throughputPerMinute": {
    "type": "number",
    "description": "Guests per minute at this gate"
   },
   "lastScanAt": {
    "type": "string",
    "format": "date-time",
    "description": "Last scan"
   },
   "validPercent": {
    "type": "number",
    "description": "Valid scans percentage"
   },
   "yellowPercent": {
    "type": "number",
    "description": "Intervention scans percentage"
   },
   "rejectedPercent": {
    "type": "number",
    "description": "Rejected scans percentage"
   }
  },
  "required": [
   "accessPointId"
  ]
 },
 "LiveAccessOperationsCommandCenterViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "guestsEnteredToday": {
    "type": "integer",
    "description": "Guests Entered Today"
   },
   "guestsExited": {
    "type": "integer",
    "description": "Guests Exited"
   },
   "guestsCurrentlyInPark": {
    "type": "integer",
    "description": "Guests Currently In Park"
   },
   "validScans": {
    "type": "integer",
    "description": "Valid Scans"
   },
   "rejectedScans": {
    "type": "integer",
    "description": "Rejected Scans"
   },
   "yellowInterventionScans": {
    "type": "integer",
    "description": "Yellow / Intervention Scans"
   },
   "overrides": {
    "type": "integer",
    "description": "Overrides"
   },
   "activeGates": {
    "type": "integer",
    "description": "Active Gates"
   },
   "offlineGates": {
    "type": "integer",
    "description": "Offline Gates"
   },
   "averageValidationTime": {
    "type": "number",
    "description": "Average validation time in seconds"
   },
   "guestsMinute": {
    "type": "number",
    "description": "Guests per minute"
   },
   "activeOperationalAlerts": {
    "type": "integer",
    "description": "Active Operational Alerts"
   }
  }
 },
 "LiveGateModeLaneControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Live Gate Mode & Lane Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "accessPointId": {
    "type": "string",
    "description": "Gate"
   },
   "availableModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "normal",
      "freeFlow",
      "dropArm",
      "closed",
      "podium",
      "maintenance"
     ]
    },
    "description": "Operating modes this gate permits, in the AccessPointOperatingMode vocabulary (R221): derived at read time from `access.device_configuration.permittedOperatingModes` of the devices at the gate, the modes every one of them permits (decided 29 September, writers pass)"
   },
   "currentMode": {
    "type": "string",
    "enum": [
     "normal",
     "freeFlow",
     "dropArm",
     "closed",
     "podium",
     "maintenance"
    ],
    "description": "current mode"
   },
   "targetMode": {
    "type": "string",
    "enum": [
     "normal",
     "freeFlow",
     "dropArm",
     "closed",
     "podium",
     "maintenance"
    ],
    "description": "Target mode of the pending `access.gate_mode_change`, if any; with operator, reason and effective time from the same row (decided 29 September, writers pass)"
   },
   "operator": {
    "type": "string",
    "description": "operator"
   },
   "reason": {
    "type": "string",
    "description": "reason"
   },
   "effectiveTime": {
    "type": "string",
    "format": "date-time",
    "description": "effective time"
   }
  },
  "required": [
   "accessPointId"
  ]
 },
 "OperationalIncidentExceptionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Operational Incident & Exception Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "incidentId": {
    "type": "string",
    "description": "Incident identifier"
   },
   "typesType": {
    "type": "string",
    "enum": [
     "credentialFraud",
     "duplicateUse",
     "biometricMismatch",
     "lostWristband",
     "gateFailure",
     "guestDispute",
     "childGuardianIssue",
     "groupAdmissionIssue",
     "securityEvent",
     "offlineConflict",
     "partnerTicketFailure",
     "emergencyAccessEvent"
    ],
    "description": "Vocabulary listed under Incident Types."
   },
   "assignedTo": {
    "type": "string",
    "enum": [
     "accessSupervisor",
     "guestServices",
     "security",
     "ticketing",
     "technicalSupport"
    ],
    "description": "Team the incident is assigned to"
   },
   "ticketId": {
    "type": "string",
    "description": "Ticket or credential concerned"
   },
   "description": {
    "type": "string",
    "description": "What happened"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "resolved",
     "closed"
    ],
    "description": "Incident status"
   }
  },
  "required": [
   "incidentId",
   "venueId",
   "typesType"
  ]
 },
 "OperationalIncidentExceptionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Operational Incident & Exception Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "incidentId": {
    "type": "string",
    "description": "Incident identifier"
   },
   "typesType": {
    "type": "string",
    "enum": [
     "credentialFraud",
     "duplicateUse",
     "biometricMismatch",
     "lostWristband",
     "gateFailure",
     "guestDispute",
     "childGuardianIssue",
     "groupAdmissionIssue",
     "securityEvent",
     "offlineConflict",
     "partnerTicketFailure",
     "emergencyAccessEvent"
    ],
    "description": "Vocabulary listed under Incident Types."
   },
   "assignedTo": {
    "type": "string",
    "enum": [
     "accessSupervisor",
     "guestServices",
     "security",
     "ticketing",
     "technicalSupport"
    ],
    "description": "Team the incident is assigned to"
   },
   "ticketId": {
    "type": "string",
    "description": "Ticket or credential concerned"
   },
   "description": {
    "type": "string",
    "description": "What happened"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "resolved",
     "closed"
    ],
    "description": "Incident status"
   }
  },
  "required": [
   "incidentId",
   "venueId",
   "typesType"
  ]
 },
 "OperationsAuditShiftHandoverControlSummaryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Operations Audit, Shift Handover & Control Summary displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "shiftId": {
    "type": "string",
    "description": "Shift identifier"
   },
   "operator": {
    "type": "string",
    "description": "Operator"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "podium": {
    "type": "string",
    "description": "Podium"
   },
   "device": {
    "type": "string",
    "description": "Device"
   },
   "login": {
    "type": "string",
    "format": "date-time",
    "description": "Login"
   },
   "logout": {
    "type": "string",
    "format": "date-time",
    "description": "Logout"
   },
   "ticketLookups": {
    "type": "integer",
    "description": "Ticket lookups"
   },
   "overrides": {
    "type": "integer",
    "description": "Overrides"
   },
   "manualOpenings": {
    "type": "integer",
    "description": "Manual openings"
   },
   "modeChanges": {
    "type": "integer",
    "description": "Mode changes"
   },
   "credentialDisables": {
    "type": "integer",
    "description": "Credential disables"
   },
   "blacklistChanges": {
    "type": "integer",
    "description": "Blacklist changes"
   },
   "groupAdjustments": {
    "type": "integer",
    "description": "Group adjustments"
   },
   "incidents": {
    "type": "integer",
    "description": "incidents"
   }
  },
  "required": [
   "shiftId",
   "operator"
  ]
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
 "PodiumOperationsConsoleView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Podium Operations Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "podiumId": {
    "type": "string",
    "description": "Podium identifier"
   },
   "podiumType": {
    "type": "string",
    "enum": [
     "physicalControlPanel",
     "tablet",
     "workstation",
     "handheld",
     "other"
    ],
    "description": "Kind of podium interface"
   },
   "name": {
    "type": "string",
    "description": "Podium name, e.g. Main Entrance A"
   },
   "accessPointIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Gates this podium controls"
   },
   "operatorId": {
    "type": "string",
    "description": "Operator on shift"
   },
   "shiftStart": {
    "type": "string",
    "format": "date-time",
    "description": "Shift start"
   },
   "shiftEnd": {
    "type": "string",
    "format": "date-time",
    "description": "Shift end"
   }
  },
  "required": [
   "podiumId"
  ]
 },
 "QueueThroughputLaneOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Queue, Throughput & Lane Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "accessPointId": {
    "type": "string",
    "description": "Lane / gate"
   },
   "laneType": {
    "type": "string",
    "enum": [
     "standard",
     "family",
     "groupB2b",
     "vip",
     "podAccessible",
     "reEntry",
     "fastPass"
    ],
    "description": "Lane type"
   },
   "guestsPerMinute": {
    "type": "number",
    "description": "Guests per minute"
   },
   "rejectPercent": {
    "type": "number",
    "description": "Reject percentage"
   },
   "status": {
    "type": "string",
    "enum": [
     "healthy",
     "investigate"
    ],
    "description": "Lane status"
   }
  },
  "required": [
   "accessPointId"
  ]
 },
 "QueueThroughputLaneOptimizationViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "guestsWaiting": {
    "type": "integer",
    "description": "Guests Waiting (the pack shows 486)"
   },
   "activeLanes": {
    "type": "integer",
    "description": "Active Lanes (the pack shows 12 / 16)"
   },
   "lanesTotal": {
    "type": "integer",
    "description": "Total lanes"
   },
   "throughputPer10Min": {
    "type": "integer",
    "description": "Guests admitted in the last 10 minutes"
   },
   "estimatedWaitMinutes": {
    "type": "integer",
    "description": "Estimated wait"
   }
  }
 },
 "ScanAnomalyRuleList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n",
  "items": {
   "type": "object",
   "properties": {
    "rule": {
     "type": "string",
     "enum": [
      "simultaneousEntry",
      "impossibleTravelTime",
      "rapidReentry",
      "sharedDevice",
      "velocityBreach"
     ]
    },
    "action": {
     "type": "string",
     "enum": [
      "log",
      "flag",
      "requireSupervisor",
      "deny"
     ]
    },
    "thresholdSeconds": {
     "type": "integer",
     "nullable": true
    }
   }
  }
 },
 "ScanOutcome": {
  "type": "string",
  "enum": [
   "admitted",
   "denied",
   "overridden"
  ]
 },
 "TicketCredentialInvestigationConsoleView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Ticket & Credential Investigation Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketId": {
    "type": "string",
    "description": "Ticket"
   },
   "transactionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Transaction time"
   },
   "salesChannel": {
    "type": "string",
    "description": "Sales channel"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "clerk": {
    "type": "string",
    "description": "Clerk"
   },
   "paymentReference": {
    "type": "string",
    "description": "Payment reference"
   },
   "paymentMethod": {
    "type": "string",
    "description": "Payment method"
   },
   "guestName": {
    "type": "string",
    "description": "Guest"
   },
   "visitDate": {
    "type": "string",
    "format": "date",
    "description": "Visit date"
   },
   "firstEntryAt": {
    "type": "string",
    "format": "date-time",
    "description": "First entry"
   },
   "reEntriesRemaining": {
    "type": "integer",
    "description": "Re-entries remaining"
   },
   "verificationMethod": {
    "type": "string",
    "description": "Verification method, e.g. dynamic QR locked"
   }
  },
  "required": [
   "ticketId"
  ]
 },
 "TicketStatus": {
  "x-ticvai-persistence": "none — computed from entitlement and scans",
  "description": "**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n",
  "type": "object",
  "required": [
   "ticketId",
   "isValid"
  ],
  "properties": {
   "ticketId": {
    "type": "string",
    "format": "uuid",
    "description": "Stable for the life of the ticket, independent of the media carrying it."
   },
   "mediaCode": {
    "type": "string",
    "nullable": true
   },
   "productName": {
    "type": "string"
   },
   "holderName": {
    "type": "string",
    "nullable": true,
    "description": "Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"
   },
   "isValid": {
    "type": "boolean"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "entriesUsed": {
    "type": "integer"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true,
    "description": "Null means unlimited."
   },
   "reentryAllowed": {
    "type": "boolean"
   },
   "isInsideVenue": {
    "type": "boolean",
    "description": "Derived from the last scan. Drives anti-passback evaluation."
   },
   "issuingCellId": {
    "type": "string",
    "nullable": true,
    "description": "Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   }
  }
 },
 "TurnstileMode": {
  "type": "string",
  "description": "**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n",
  "enum": [
   "freeRotation",
   "closed"
  ]
 },
 "ValidationExceptionReasonCodeManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Validation Exception & Reason Code Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "reasonCode": {
    "type": "string",
    "description": "Reason code, e.g. AC-002"
   },
   "operationalResponse": {
    "type": "string",
    "enum": [
     "deny",
     "operatorReview",
     "supervisorRequired",
     "allowWithWarning"
    ],
    "description": "Configured response when this reason occurs"
   },
   "name": {
    "type": "string",
    "description": "Reason, e.g. Wrong Visit Date"
   },
   "guestMessage": {
    "type": "string",
    "description": "Message shown to the guest"
   },
   "operatorMessage": {
    "type": "string",
    "description": "Message shown to the operator"
   },
   "followUpAction": {
    "type": "string",
    "description": "Suggested operator follow-up, e.g. check reschedule eligibility"
   }
  },
  "required": [
   "reasonCode"
  ]
 },
 "ValidationResult": {
  "x-ticvai-persistence": "none — computed, persisted as scan_event",
  "type": "object",
  "required": [
   "scanId",
   "outcome",
   "accessPointId",
   "recordedAt"
  ],
  "properties": {
   "scanId": {
    "type": "string",
    "format": "uuid"
   },
   "outcome": {
    "$ref": "#/components/schemas/ScanOutcome"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   },
   "denyDetail": {
    "type": "string",
    "description": "Human-readable, localised. For operator display, never for logic."
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "ticket": {
    "$ref": "#/components/schemas/TicketStatus"
   },
   "admittedCount": {
    "type": "integer",
    "description": "Holders admitted on this read. Differs from groupSize on partial admission."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "serverEvaluatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "advisory": {
    "type": "object",
    "nullable": true,
    "description": "BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n",
    "properties": {
     "genderClassification": {
      "type": "string",
      "enum": [
       "women",
       "men",
       "undetermined"
      ],
      "description": "**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"
     },
     "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"
     },
     "reportedByDeviceId": {
      "type": "string",
      "format": "uuid",
      "description": "**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"
     }
    }
   }
  }
 }
}
```
