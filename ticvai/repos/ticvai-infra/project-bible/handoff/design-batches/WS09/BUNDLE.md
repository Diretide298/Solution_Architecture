# WS09 — Access Control board 9

**10 screens · 10 operations · 12 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ACCESS_POINT_CONFIGURE, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-224` | Live Access Operations Command Center | listDetail | 1 | 0 | — |
| `BO-225` | Podium Operations Console | listDetail | 1 | 0 | — |
| `BO-226` | Ticket & Credential Investigation Console | listDetail | 1 | 0 | — |
| `BO-227` | Validation Exception & Reason Code Manager | listDetail | 1 | 0 | — |
| `BO-228` | Manual Override & Supervisor Approval | configEditor | 1 | 0 | — |
| `BO-229` | Credential Disable, Blacklist & Whitelist Operations | listDetail | 1 | 0 | — |
| `BO-230` | Live Gate Mode & Lane Control | listDetail | 1 | 0 | — |
| `BO-231` | Queue, Throughput & Lane Optimization | listDetail | 1 | 0 | — |
| `BO-232` | Operational Incident & Exception Workspace | listDetail | 1 | 0 | — |
| `BO-233` | Operations Audit, Shift Handover & Control Summary | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-224, BO-225, BO-226, BO-227, BO-229, BO-230, BO-231, BO-232, BO-233 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
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
     "to": "BO-230",
     "trigger": "Works in Live Gate Mode & Lane Control",
     "provenance": "flow F119 step 11→12",
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
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the venue control room with a real-time view of access operations across all gates, parks, zones, and attractions.",
  "purposeNote": "Operations can understand the live access state of the entire venue without opening individual device screens.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every live access operations",
       "columns": [
        "LiveAccessOperationsCommandCenterView.guestsEnteredToday",
        "LiveAccessOperationsCommandCenterView.guestsExited",
        "LiveAccessOperationsCommandCenterView.guestsCurrentlyInPark",
        "LiveAccessOperationsCommandCenterView.validScans",
        "LiveAccessOperationsCommandCenterView.rejectedScans",
        "LiveAccessOperationsCommandCenterView.yellowInterventionScans",
        "LiveAccessOperationsCommandCenterView.overrides",
        "LiveAccessOperationsCommandCenterView.activeGates",
        "LiveAccessOperationsCommandCenterView.offlineGates",
        "LiveAccessOperationsCommandCenterView.averageValidationTime",
        "LiveAccessOperationsCommandCenterView.guestsMinute",
        "LiveAccessOperationsCommandCenterView.activeOperationalAlerts"
       ],
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
       "columns": [
        "LiveAccessOperationsCommandCenterView.guestsEnteredToday",
        "LiveAccessOperationsCommandCenterView.guestsExited",
        "LiveAccessOperationsCommandCenterView.guestsCurrentlyInPark",
        "LiveAccessOperationsCommandCenterView.validScans",
        "LiveAccessOperationsCommandCenterView.rejectedScans",
        "LiveAccessOperationsCommandCenterView.yellowInterventionScans",
        "LiveAccessOperationsCommandCenterView.overrides",
        "LiveAccessOperationsCommandCenterView.activeGates",
        "LiveAccessOperationsCommandCenterView.offlineGates",
        "LiveAccessOperationsCommandCenterView.averageValidationTime",
        "LiveAccessOperationsCommandCenterView.guestsMinute",
        "LiveAccessOperationsCommandCenterView.activeOperationalAlerts"
       ],
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
    "LiveAccessOperationsCommandCenterView.guestsEnteredToday",
    "LiveAccessOperationsCommandCenterView.guestsExited",
    "LiveAccessOperationsCommandCenterView.guestsCurrentlyInPark",
    "LiveAccessOperationsCommandCenterView.validScans",
    "LiveAccessOperationsCommandCenterView.rejectedScans",
    "LiveAccessOperationsCommandCenterView.yellowInterventionScans"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-224"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the operational interface described in the matrix for attendants controlling one or more turnstiles.",
  "purposeNote": "Authorized attendants can control assigned access devices from one operational interface.",
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
       "columns": [
        "PodiumOperationsConsoleView.gate01Entry",
        "PodiumOperationsConsoleView.gate02Entry",
        "PodiumOperationsConsoleView.gate03Entry",
        "PodiumOperationsConsoleView.gate04Entry",
        "PodiumOperationsConsoleView.gate05Closed",
        "PodiumOperationsConsoleView.gate06Group"
       ],
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
       "columns": [
        "PodiumOperationsConsoleView.gate01Entry",
        "PodiumOperationsConsoleView.gate02Entry",
        "PodiumOperationsConsoleView.gate03Entry",
        "PodiumOperationsConsoleView.gate04Entry",
        "PodiumOperationsConsoleView.gate05Closed",
        "PodiumOperationsConsoleView.gate06Group"
       ],
       "notes": "The pack groups this record's detail under its own headings: “The podium may be”, “Controls”, “Operator”, “Shift”, “Authorized actions”, “Important”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 117 §Display"
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
   }
  ],
  "entryState": {
   "preloaded": [
    "PodiumOperationsConsoleView.gate01Entry",
    "PodiumOperationsConsoleView.gate02Entry",
    "PodiumOperationsConsoleView.gate03Entry",
    "PodiumOperationsConsoleView.gate04Entry",
    "PodiumOperationsConsoleView.gate05Closed",
    "PodiumOperationsConsoleView.gate06Group"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-225"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 117. 6 of 6 labels bound to a contract property; 6 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow operators to quickly investigate why a guest cannot enter.",
  "purposeNote": "An operator can understand the ticket's complete operational access state from one screen without navigating across multiple modules.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-226"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Standardize what happens when access is not automatically granted. The matrix requires the scanner to display a reason code when a ticket is invalid.",
  "purposeNote": "Every validation failure returns a standardized reason and configured operational response.",
  "gaps": [
   {
    "operation": null,
    "why": "**Validation Exception & Reason Code Manager declares no operation that writes anything** — its only declared call is `listValidationExceptionReason`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
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
   }
  ],
  "entryState": {
   "preloaded": [
    "ValidationExceptionReasonCodeManagerView.ticketDate02Sep2026",
    "ValidationExceptionReasonCodeManagerView.deny",
    "ValidationExceptionReasonCodeManagerView.operatorReview",
    "ValidationExceptionReasonCodeManagerView.supervisorRequired",
    "ValidationExceptionReasonCodeManagerView.allowWithWarning"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-227"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 120. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "operation": "approveManualOverrideSupervisor"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configured Date; Select) and no display directory — it is settings, not a population",
  "purpose": "Allow authorized staff to bypass selected access restrictions when operationally justified. The matrix explicitly requires Allow Override and operator-based ticket override.",
  "purposeNote": "Only authorized users can override eligible rules, with reason, approval, timestamp, operator, device and original decision retained.",
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
       "provenance": "contract operation approveManualOverrideSupervisor"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The manual override supervisor configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the manual override supervisor untouched.",
   "emptyFirstRun": "No manual override supervisor configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveManualOverrideSupervisor",
    "contract": "access",
    "purpose": "Manual Override & Supervisor Approval",
    "trigger": "onAction",
    "invalidates": [
     "approveManualOverrideSupervisor"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-228"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide immediate operational security control over individual credentials.",
  "purposeNote": "Authorized users can immediately restrict credential access across the configured venue environment.",
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
    "CredentialDisableBlacklistWhitelistOperationsView.blacklistWhitelistCapability",
    "CredentialDisableBlacklistWhitelistOperationsView.manualTicketInvalidation",
    "CredentialDisableBlacklistWhitelistOperationsView.reason",
    "CredentialDisableBlacklistWhitelistOperationsView.entireCredential",
    "CredentialDisableBlacklistWhitelistOperationsView.venueAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-229"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow operations to change access-point modes during live operations without entering the Board 6 engineering configuration. Board 6 defines which modes a device can support. Board 9 controls which permitted mode it is currently running.",
  "purposeNote": "Operations can change the active mode of one or multiple authorized gates without modifying their underlying hardware configuration.",
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
        "LiveGateModeLaneControlView.affectedGates",
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
        "LiveGateModeLaneControlView.affectedGates",
        "LiveGateModeLaneControlView.currentMode",
        "LiveGateModeLaneControlView.targetMode",
        "LiveGateModeLaneControlView.operator",
        "LiveGateModeLaneControlView.reason"
       ],
       "notes": "The pack groups this record's detail under its own headings: “ENTRY”, “Available”, “Bulk Command”, “Optional”, “Emergency”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 124 §Show"
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
   }
  ],
  "entryState": {
   "preloaded": [
    "LiveGateModeLaneControlView.affectedGates",
    "LiveGateModeLaneControlView.currentMode",
    "LiveGateModeLaneControlView.targetMode",
    "LiveGateModeLaneControlView.operator",
    "LiveGateModeLaneControlView.reason"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-230"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 124. 5 of 5 labels bound to a contract property; 9 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Manage entrance flow in real time. This addresses the matrix requirement to improve entrance flow and queuing, particularly for large B2B groups.",
  "purposeNote": "Operations can monitor throughput and proactively adjust available lane capacity.",
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
        "QueueThroughputLaneOptimizationView.standard",
        "QueueThroughputLaneOptimizationView.family",
        "QueueThroughputLaneOptimizationView.groupB2b",
        "QueueThroughputLaneOptimizationView.vip",
        "QueueThroughputLaneOptimizationView.podAccessible",
        "QueueThroughputLaneOptimizationView.reEntry"
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
        "QueueThroughputLaneOptimizationView.standard",
        "QueueThroughputLaneOptimizationView.family",
        "QueueThroughputLaneOptimizationView.groupB2b",
        "QueueThroughputLaneOptimizationView.vip",
        "QueueThroughputLaneOptimizationView.podAccessible",
        "QueueThroughputLaneOptimizationView.reEntry"
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
    "QueueThroughputLaneOptimizationView.standard",
    "QueueThroughputLaneOptimizationView.family",
    "QueueThroughputLaneOptimizationView.groupB2b",
    "QueueThroughputLaneOptimizationView.vip",
    "QueueThroughputLaneOptimizationView.podAccessible",
    "QueueThroughputLaneOptimizationView.reEntry"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-231"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage access incidents that require more than a simple override.",
  "purposeNote": "Complex access exceptions can be formally investigated and resolved with complete operational evidence.",
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
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setOperationalIncidentException",
    "contract": "access",
    "purpose": "Operational Incident & Exception Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setOperationalIncidentException"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-232"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide full accountability for everything operators and supervisors changed during live access operations.",
  "purposeNote": "Every operational intervention is attributable to a user and can be reviewed during audit, investigation and shift handover. Board 9 — Final 10-Screen Structure # Backend Screen Main Responsibility 9.1 Live Access Operations Command Center Real-time venue admission operations 9.2 Podium Operations Console Operator control of gates/turnstiles 9.3 Ticket & Credential Investigation Console Investigate guest access state",
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
   }
  ],
  "entryState": {
   "preloaded": [
    "OperationsAuditShiftHandoverControlSummaryView.operator",
    "OperationsAuditShiftHandoverControlSummaryView.role",
    "OperationsAuditShiftHandoverControlSummaryView.podium",
    "OperationsAuditShiftHandoverControlSummaryView.device",
    "OperationsAuditShiftHandoverControlSummaryView.login"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-233"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 128. 0 of 0 labels bound to a contract property; 0 of 88 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveManualOverrideSupervisor": {
  "method": "PUT",
  "path": "/manual-override-supervisor",
  "contract": "access",
  "summary": "Manual Override & Supervisor Approval",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ManualOverrideSupervisorApprovalInput",
  "responds": "ManualOverrideSupervisorApprovalView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialDisableBlacklistWhitelistOperationsView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "LiveAccessOperationsCommandCenterView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "LiveGateModeLaneControlView"
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
  "parameters": [],
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
  "parameters": [],
  "requestBody": null,
  "responds": "QueueThroughputLaneOptimizationView"
 },
 "listShiftHandoverSummary": {
  "method": "GET",
  "path": "/shift-handover-summary",
  "contract": "access",
  "summary": "Operations Audit, Shift Handover & Control Summary",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OperationsAuditShiftHandoverControlSummaryView"
 },
 "listTicketCredentialInvestigation": {
  "method": "GET",
  "path": "/ticket-credential-investigation",
  "contract": "access",
  "summary": "Ticket & Credential Investigation Console",
  "permission": "SCOPE_VIEW",
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
   }
  ],
  "requestBody": null,
  "responds": "TicketCredentialInvestigationConsoleView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ValidationExceptionReasonCodeManagerView"
 },
 "setOperationalIncidentException": {
  "method": "PUT",
  "path": "/operational-incident-exception",
  "contract": "access",
  "summary": "Operational Incident & Exception Workspace",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "OperationalIncidentExceptionWorkspaceInput",
  "responds": "OperationalIncidentExceptionWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CredentialDisableBlacklistWhitelistOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Disable, Blacklist & Whitelist Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "blacklistWhitelistCapability": {
    "type": "string",
    "description": "blacklist/whitelist capability"
   },
   "manualTicketInvalidation": {
    "type": "string",
    "description": "manual ticket invalidation"
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
     "managementInstruction"
    ],
    "description": "Vocabulary listed under Reason."
   },
   "entireCredential": {
    "type": "string",
    "description": "Entire Credential"
   },
   "venueAccess": {
    "type": "string",
    "description": "Venue Access"
   },
   "attractionAccess": {
    "type": "string",
    "description": "Attraction Access"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "fastPass": {
    "type": "string",
    "description": "Fast Pass"
   },
   "specificEntitlement": {
    "type": "string",
    "description": "Specific Entitlement"
   },
   "permanent": {
    "type": "string",
    "description": "Permanent"
   },
   "untilEndOfDay": {
    "type": "string",
    "format": "date-time",
    "description": "Until End of Day"
   },
   "untilDate": {
    "type": "string",
    "format": "date-time",
    "description": "Until Date"
   },
   "untilTime": {
    "type": "string",
    "format": "date-time",
    "description": "Until Time"
   },
   "untilManuallyRestored": {
    "type": "string",
    "format": "date-time",
    "description": "Until Manually Restored"
   },
   "to": {
    "type": "string",
    "description": "to"
   },
   "centralPlatform": {
    "type": "string",
    "description": "✓ Central Platform"
   },
   "venueEdge": {
    "type": "string",
    "description": "✓ Venue Edge"
   },
   "onlineGates": {
    "type": "string",
    "description": "✓ Online Gates"
   },
   "offlineRevocationPackage": {
    "type": "string",
    "description": "✓ Offline Revocation Package"
   },
   "exceptions": {
    "type": "string",
    "description": "exceptions"
   },
   "dependingOnPolicy": {
    "type": "string",
    "description": "depending on policy"
   }
  }
 },
 "LiveAccessOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Live Access Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestsEnteredToday": {
    "type": "string",
    "description": "Guests Entered Today"
   },
   "guestsExited": {
    "type": "string",
    "description": "Guests Exited"
   },
   "guestsCurrentlyInPark": {
    "type": "string",
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
    "type": "string",
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
    "type": "string",
    "format": "date-time",
    "description": "Average Validation Time"
   },
   "guestsMinute": {
    "type": "string",
    "description": "Guests / Minute"
   },
   "activeOperationalAlerts": {
    "type": "integer",
    "description": "Active Operational Alerts"
   },
   "mainGate01": {
    "type": "string",
    "description": "🟢 Main Gate 01"
   },
   "mainGate02": {
    "type": "string",
    "description": "🟢 Main Gate 02"
   },
   "mainGate03": {
    "type": "string",
    "description": "🟡 Main Gate 03"
   },
   "mainGate04": {
    "type": "string",
    "description": "🔴 Main Gate 04"
   },
   "vipGate": {
    "type": "string",
    "description": "🟢 VIP Gate"
   },
   "groupGate": {
    "type": "string",
    "description": "🟢 Group Gate"
   },
   "reEntryGate": {
    "type": "string",
    "description": "🟢 Re-entry Gate"
   },
   "modeEntry": {
    "type": "string",
    "description": "Mode: ENTRY"
   },
   "statusOnline": {
    "type": "integer",
    "description": "Status: ONLINE"
   },
   "queueModerate": {
    "type": "string",
    "description": "Queue: Moderate"
   },
   "throughput31GuestsMin": {
    "type": "string",
    "description": "Throughput: 31 Guests/min"
   },
   "lastScan4SecAgo": {
    "type": "string",
    "format": "date-time",
    "description": "Last Scan: 4 sec ago"
   },
   "valid92": {
    "type": "number",
    "description": "Valid: 92%"
   },
   "yellow5": {
    "type": "number",
    "description": "Yellow: 5%"
   },
   "rejected3": {
    "type": "integer",
    "description": "Rejected: 3%"
   }
  }
 },
 "LiveGateModeLaneControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Live Gate Mode & Lane Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "selectType": {
    "type": "string",
    "enum": [
     "gate01",
     "gate02",
     "gate03",
     "gate04"
    ],
    "description": "Vocabulary listed under Select."
   },
   "entry": {
    "type": "string",
    "description": "Entry"
   },
   "exit": {
    "type": "string",
    "description": "Exit"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "crossover": {
    "type": "string",
    "description": "Crossover"
   },
   "group": {
    "type": "string",
    "description": "Group"
   },
   "fastPass": {
    "type": "string",
    "description": "Fast Pass"
   },
   "freeSpin": {
    "type": "string",
    "description": "Free Spin"
   },
   "countOnly": {
    "type": "integer",
    "description": "Count Only"
   },
   "closed": {
    "type": "integer",
    "description": "Closed"
   },
   "affectedGates": {
    "type": "integer",
    "description": "affected gates"
   },
   "currentMode": {
    "type": "string",
    "description": "current mode"
   },
   "targetMode": {
    "type": "string",
    "description": "target mode"
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
   },
   "safetyControls": {
    "type": "string",
    "description": "safety controls"
   }
  }
 },
 "ManualOverrideSupervisorApprovalInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Manual Override & Supervisor Approval submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "guestScans": {
    "type": "string",
    "description": "Guest scans"
   },
   "selectType": {
    "type": "string",
    "enum": [
     "guestService",
     "ticketingError",
     "operationalException",
     "managementAuthorization",
     "technicalFailure",
     "eventException"
    ],
    "description": "Vocabulary listed under Select."
   },
   "ahmedK": {
    "type": "string",
    "description": "Ahmed K"
   },
   "gateOpens": {
    "type": "string",
    "description": "Gate opens"
   },
   "originalResultDenied": {
    "type": "string",
    "description": "Original Result: DENIED"
   },
   "overrideApproved": {
    "type": "string",
    "description": "Override: APPROVED"
   }
  }
 },
 "ManualOverrideSupervisorApprovalView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Manual Override & Supervisor Approval displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestScans": {
    "type": "string",
    "description": "Guest scans"
   },
   "selectType": {
    "type": "string",
    "enum": [
     "guestService",
     "ticketingError",
     "operationalException",
     "managementAuthorization",
     "technicalFailure",
     "eventException"
    ],
    "description": "Vocabulary listed under Select."
   },
   "ahmedK": {
    "type": "string",
    "description": "Ahmed K"
   },
   "gateOpens": {
    "type": "string",
    "description": "Gate opens"
   },
   "originalResultDenied": {
    "type": "string",
    "description": "Original Result: DENIED"
   },
   "overrideApproved": {
    "type": "string",
    "description": "Override: APPROVED"
   }
  }
 },
 "OperationalIncidentExceptionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Operational Incident & Exception Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
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
   "scanHistory": {
    "type": "string",
    "description": "Scan history"
   },
   "reasonCodes": {
    "type": "string",
    "description": "reason codes"
   },
   "gateDevice": {
    "type": "string",
    "description": "gate/device"
   },
   "operator": {
    "type": "string",
    "description": "operator"
   },
   "ticketStatus": {
    "type": "string",
    "description": "ticket status"
   },
   "credentialHistory": {
    "type": "string",
    "description": "credential history"
   },
   "accessJourney": {
    "type": "string",
    "description": "access journey"
   },
   "relevantSecurityAlerts": {
    "type": "integer",
    "description": "relevant security alerts"
   },
   "accessSupervisor": {
    "type": "string",
    "description": "Access Supervisor"
   },
   "guestServices": {
    "type": "string",
    "description": "Guest Services"
   },
   "security": {
    "type": "string",
    "description": "Security"
   },
   "ticketing": {
    "type": "string",
    "description": "Ticketing"
   },
   "technicalSupport": {
    "type": "boolean",
    "description": "Technical Support"
   }
  }
 },
 "OperationalIncidentExceptionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Operational Incident & Exception Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "scanHistory": {
    "type": "string",
    "description": "Scan history"
   },
   "reasonCodes": {
    "type": "string",
    "description": "reason codes"
   },
   "gateDevice": {
    "type": "string",
    "description": "gate/device"
   },
   "operator": {
    "type": "string",
    "description": "operator"
   },
   "ticketStatus": {
    "type": "string",
    "description": "ticket status"
   },
   "credentialHistory": {
    "type": "string",
    "description": "credential history"
   },
   "accessJourney": {
    "type": "string",
    "description": "access journey"
   },
   "relevantSecurityAlerts": {
    "type": "integer",
    "description": "relevant security alerts"
   },
   "accessSupervisor": {
    "type": "string",
    "description": "Access Supervisor"
   },
   "guestServices": {
    "type": "string",
    "description": "Guest Services"
   },
   "security": {
    "type": "string",
    "description": "Security"
   },
   "ticketing": {
    "type": "string",
    "description": "Ticketing"
   },
   "technicalSupport": {
    "type": "boolean",
    "description": "Technical Support"
   }
  }
 },
 "OperationsAuditShiftHandoverControlSummaryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Operations Audit, Shift Handover & Control Summary displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "description": "Login"
   },
   "logout": {
    "type": "string",
    "description": "Logout"
   },
   "ticketLookups": {
    "type": "string",
    "description": "Ticket lookups"
   },
   "overrides": {
    "type": "string",
    "description": "Overrides"
   },
   "manualOpenings": {
    "type": "string",
    "description": "Manual openings"
   },
   "modeChanges": {
    "type": "string",
    "description": "Mode changes"
   },
   "credentialDisables": {
    "type": "string",
    "description": "Credential disables"
   },
   "blacklistChanges": {
    "type": "string",
    "description": "Blacklist changes"
   },
   "groupAdjustments": {
    "type": "string",
    "description": "Group adjustments"
   },
   "incidents": {
    "type": "string",
    "description": "incidents"
   },
   "gate08RfidIntermittent": {
    "type": "string",
    "description": "Gate 08 RFID intermittent"
   },
   "schoolGroupExpected1615": {
    "type": "string",
    "description": "School group expected 16:15"
   },
   "credentialFraudIncidentUnderInvestigation": {
    "type": "string",
    "description": "Credential fraud incident under investigation"
   },
   "reEntryGate02TemporarilyClosed": {
    "type": "integer",
    "description": "Re-entry Gate 02 temporarily closed"
   },
   "unusualOverrideVolumes": {
    "type": "string",
    "description": "unusual override volumes"
   },
   "unresolvedIncidents": {
    "type": "string",
    "description": "unresolved incidents"
   },
   "disabledGates": {
    "type": "string",
    "description": "disabled gates"
   },
   "blacklistedCredentials": {
    "type": "string",
    "description": "blacklisted credentials"
   },
   "offlineDevices": {
    "type": "integer",
    "description": "offline devices"
   },
   "abnormalRejectionRates": {
    "type": "string",
    "description": "abnormal rejection rates"
   },
   "shiftReport": {
    "type": "string",
    "description": "Shift Report"
   },
   "operatorActivityReport": {
    "type": "string",
    "description": "Operator Activity Report"
   },
   "gateModeChangeReport": {
    "type": "string",
    "description": "Gate Mode Change Report"
   },
   "incidentReport": {
    "type": "string",
    "description": "Incident Report"
   },
   "exceptionReport": {
    "type": "string",
    "description": "Exception Report"
   },
   "outcomes": {
    "type": "string",
    "description": "outcomes"
   },
   "permissionAware": {
    "type": "string",
    "description": "permission-aware"
   },
   "grantedRightNow": {
    "type": "string",
    "description": "granted right now?”"
   }
  }
 },
 "PodiumOperationsConsoleView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Podium Operations Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "physicalKeyboardControlPanel": {
    "type": "string",
    "description": "physical keyboard/control panel"
   },
   "tablet": {
    "type": "string",
    "description": "tablet"
   },
   "workstation": {
    "type": "string",
    "description": "workstation"
   },
   "handheld": {
    "type": "string",
    "description": "handheld"
   },
   "otherAuthorizedOperationalInterface": {
    "type": "string",
    "description": "other authorized operational interface"
   },
   "gates0106": {
    "type": "string",
    "description": "Gates 01–06"
   },
   "saraM": {
    "type": "string",
    "description": "Sara M"
   },
   "gate01Entry": {
    "type": "string",
    "description": "Gate 01 — ENTRY 🟢"
   },
   "gate02Entry": {
    "type": "string",
    "description": "Gate 02 — ENTRY 🟢"
   },
   "gate03Entry": {
    "type": "string",
    "description": "Gate 03 — ENTRY 🟡"
   },
   "gate04Entry": {
    "type": "string",
    "description": "Gate 04 — ENTRY 🟢"
   },
   "gate05Closed": {
    "type": "string",
    "description": "Gate 05 — CLOSED 🔴"
   },
   "gate06Group": {
    "type": "string",
    "description": "Gate 06 — GROUP 🟢"
   },
   "ticketLookup": {
    "type": "string",
    "description": "Ticket Lookup"
   },
   "rescan": {
    "type": "string",
    "description": "Rescan"
   },
   "manualValidate": {
    "type": "string",
    "description": "Manual Validate"
   },
   "changeGateMode": {
    "type": "string",
    "description": "Change Gate Mode"
   },
   "groupAdmission": {
    "type": "string",
    "description": "Group Admission"
   }
  }
 },
 "QueueThroughputLaneOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Queue, Throughput & Lane Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestsWaiting": {
    "type": "string",
    "description": "Guests Waiting (the pack shows 486)"
   },
   "activeLanes": {
    "type": "integer",
    "description": "Active Lanes (the pack shows 12 / 16)"
   },
   "g01Standard2821Healthy": {
    "type": "number",
    "description": "G01 Standard 28 2.1% Healthy"
   },
   "g02Standard3118Healthy": {
    "type": "number",
    "description": "G02 Standard 31 1.8% Healthy"
   },
   "g03Group4709Healthy": {
    "type": "number",
    "description": "G03 Group 47 0.9% Healthy"
   },
   "g04Standard12142Investigate": {
    "type": "number",
    "description": "G04 Standard 12 14.2% Investigate"
   },
   "standard": {
    "type": "string",
    "description": "Standard"
   },
   "family": {
    "type": "string",
    "description": "Family"
   },
   "groupB2b": {
    "type": "string",
    "description": "Group/B2B"
   },
   "vip": {
    "type": "string",
    "description": "VIP"
   },
   "podAccessible": {
    "type": "string",
    "description": "POD/Accessible"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "fastPass": {
    "type": "string",
    "description": "Fast Pass"
   }
  }
 },
 "TicketCredentialInvestigationConsoleView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Ticket & Credential Investigation Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestJohnSmith": {
    "type": "string",
    "description": "Guest: John Smith"
   },
   "visitDate01Sep2026": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date: 01 Sep 2026"
   },
   "parkEntryUsed": {
    "type": "string",
    "description": "Park Entry: USED"
   },
   "mealVoucherAvailable": {
    "type": "string",
    "description": "Meal Voucher: AVAILABLE"
   },
   "lockerL284": {
    "type": "string",
    "description": "Locker: L-284"
   },
   "dynamicQrLocked": {
    "type": "string",
    "description": "Dynamic QR — LOCKED"
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
   }
  }
 },
 "ValidationExceptionReasonCodeManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Validation Exception & Reason Code Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketDate02Sep2026": {
    "type": "string",
    "format": "date-time",
    "description": "Ticket date: 02 Sep 2026"
   },
   "deny": {
    "type": "string",
    "description": "🔴 Deny"
   },
   "operatorReview": {
    "type": "string",
    "description": "🟡 Operator Review"
   },
   "supervisorRequired": {
    "type": "boolean",
    "description": "🟡 Supervisor Required"
   },
   "allowWithWarning": {
    "type": "string",
    "description": "🟢 Allow with Warning"
   },
   "alreadyUsed": {
    "type": "string",
    "description": "Already Used →"
   },
   "verificationMismatch": {
    "type": "string",
    "description": "Verification Mismatch →"
   }
  }
 }
}
```
