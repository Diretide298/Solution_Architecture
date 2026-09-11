# WS08 — Access Control board 8

**10 screens · 10 operations · 12 schemas · 3 permissions**

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
  `ACCESS_POINT_CONFIGURE, MARKETING_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-214` | Guest Journey Command Center | listDetail | 1 | 0 | — |
| `BO-215` | Group & B2B Admission Profile Builder | configEditor | 1 | 0 | — |
| `BO-216` | Group Leader & Fast B2B Validation | listDetail | 1 | 0 | — |
| `BO-217` | Group Attendance & Partial Entry Manager | listDetail | 1 | 0 | — |
| `BO-218` | Family, Child, POD & Companion Journey | configEditor | 1 | 0 | — |
| `BO-219` | Re-entry & Temporary Exit Journey | configEditor | 1 | 0 | — |
| `BO-220` | Multi-Park & Crossover Journey Orchestrator | listDetail | 1 | 0 | — |
| `BO-221` | Fast Pass & Attraction Access Journey | configEditor | 1 | 0 | — |
| `BO-222` | Special Event, Free View & Alternative Admission | configEditor | 1 | 0 | — |
| `BO-223` | Journey Simulation, Audit & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-214, BO-216, BO-217, BO-220, BO-221, BO-222, BO-223 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-214",
  "name": "Guest Journey Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.1",
   "page": 101
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/guest-journey-command-center-bo-214",
   "component": "apps/venue-management-web/src/routes/access-venue/GuestJourneyCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-215",
    "BO-216",
    "BO-217",
    "BO-218",
    "BO-219",
    "BO-220",
    "BO-221",
    "BO-222",
    "BO-223"
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
     "to": "BO-215",
     "trigger": "Works in Group & B2B Admission Profile Builder",
     "provenance": "flow F118 step 1→2",
     "operation": "listGuestJourney"
    },
    {
     "to": "BO-216",
     "trigger": "Works in Group Leader & Fast B2B Validation",
     "provenance": "flow F118 step 3→4",
     "operation": "listGuestJourney"
    },
    {
     "to": "BO-217",
     "trigger": "Works in Group Attendance & Partial Entry Manager",
     "provenance": "flow F118 step 5→6",
     "operation": "listGuestJourney"
    },
    {
     "to": "BO-218",
     "trigger": "Works in Family, Child, POD & Companion Journey",
     "provenance": "flow F118 step 7→8",
     "operation": "listGuestJourney"
    },
    {
     "to": "BO-219",
     "trigger": "Works in Re-entry & Temporary Exit Journey",
     "provenance": "flow F118 step 9→10",
     "operation": "listGuestJourney"
    },
    {
     "to": "BO-220",
     "trigger": "Works in Multi-Park & Crossover Journey Orchestrator",
     "provenance": "flow F118 step 11→12",
     "operation": "listGuestJourney"
    },
    {
     "to": "BO-221",
     "trigger": "Works in Fast Pass & Attraction Access Journey",
     "provenance": "flow F118 step 13→14",
     "operation": "listGuestJourney"
    },
    {
     "to": "BO-222",
     "trigger": "Works in Special Event, Free View & Alternative Admission",
     "provenance": "flow F118 step 15→16",
     "operation": "listGuestJourney"
    },
    {
     "to": "BO-223",
     "trigger": "Works in Journey Simulation, Audit & Publication",
     "provenance": "flow F118 step 17→18",
     "operation": "listGuestJourney"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Central configuration and monitoring screen for all special and multi-person admission journeys.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every guest journey",
       "columns": [
        "GuestJourneyCommandCenterView.activeJourneyProfiles",
        "GuestJourneyCommandCenterView.groupArrivalsToday",
        "GuestJourneyCommandCenterView.guestsViaGroupAdmission",
        "GuestJourneyCommandCenterView.familyJourneys",
        "GuestJourneyCommandCenterView.reEntryGuests",
        "GuestJourneyCommandCenterView.crossoversToday",
        "GuestJourneyCommandCenterView.fastPassValidations",
        "GuestJourneyCommandCenterView.specialEventAdmissions",
        "GuestJourneyCommandCenterView.vipAdmissions",
        "GuestJourneyCommandCenterView.journeyExceptions"
       ],
       "bindsTo": "GuestJourneyCommandCenterView",
       "operation": "listGuestJourney",
       "provenance": "pack Access Control Module_Reference.pdf, page 101 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected guest journey",
       "bindsTo": "GuestJourneyCommandCenterView",
       "columns": [
        "GuestJourneyCommandCenterView.activeJourneyProfiles",
        "GuestJourneyCommandCenterView.groupArrivalsToday",
        "GuestJourneyCommandCenterView.guestsViaGroupAdmission",
        "GuestJourneyCommandCenterView.familyJourneys",
        "GuestJourneyCommandCenterView.reEntryGuests",
        "GuestJourneyCommandCenterView.crossoversToday",
        "GuestJourneyCommandCenterView.fastPassValidations",
        "GuestJourneyCommandCenterView.specialEventAdmissions",
        "GuestJourneyCommandCenterView.vipAdmissions",
        "GuestJourneyCommandCenterView.journeyExceptions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Journey Type Venue Credential Status”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 101 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest journey list.",
   "error": "Could not load. Names which read failed and leaves the guest journey untouched.",
   "emptyFirstRun": "No guest journey yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest journey are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGuestJourney",
    "contract": "access",
    "purpose": "Guest Journey Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GuestJourneyCommandCenterView.activeJourneyProfiles",
    "GuestJourneyCommandCenterView.groupArrivalsToday",
    "GuestJourneyCommandCenterView.guestsViaGroupAdmission",
    "GuestJourneyCommandCenterView.familyJourneys",
    "GuestJourneyCommandCenterView.reEntryGuests",
    "GuestJourneyCommandCenterView.crossoversToday"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-214"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 101. 10 of 10 labels bound to a contract property; 10 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-215",
  "name": "Group & B2B Admission Profile Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.2",
   "page": 102
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/group-b2b-admission-profile-builder-bo-215",
   "component": "apps/venue-management-web/src/routes/access-venue/GroupB2bAdmissionProfileBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-214"
   ],
   "exitTo": [
    "BO-214"
   ],
   "inferred": false,
   "notes": "**Reached from BO-214, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-214",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F118 step 2→3",
     "operation": "setGroupAdmissionProfile"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure admission for) and no display directory — it is settings, not a population",
  "purpose": "Group & B2B Admission Profile Builder",
  "purposeNote": "Group admission behavior can be configured independently from standard individual-ticket admission.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Schools",
       "provenance": "pack Access Control Module_Reference.pdf, page 102 §Configure admission for"
      },
      {
       "kind": "selectField",
       "label": "Tour Operators",
       "provenance": "pack Access Control Module_Reference.pdf, page 102 §Configure admission for"
      },
      {
       "kind": "selectField",
       "label": "Corporate Groups",
       "provenance": "pack Access Control Module_Reference.pdf, page 102 §Configure admission for"
      },
      {
       "kind": "selectField",
       "label": "Resellers",
       "provenance": "pack Access Control Module_Reference.pdf, page 102 §Configure admission for"
      },
      {
       "kind": "selectField",
       "label": "Travel Groups",
       "provenance": "pack Access Control Module_Reference.pdf, page 102 §Configure admission for"
      },
      {
       "kind": "selectField",
       "label": "Camps",
       "provenance": "pack Access Control Module_Reference.pdf, page 102 §Configure admission for"
      },
      {
       "kind": "selectField",
       "label": "Families",
       "provenance": "pack Access Control Module_Reference.pdf, page 102 §Configure admission for"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setGroupAdmissionProfile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group b2b admission configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the group b2b admission untouched.",
   "emptyFirstRun": "No group b2b admission configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGroupAdmissionProfile",
    "contract": "access",
    "purpose": "Group & B2B Admission Profile Builder",
    "trigger": "onAction",
    "invalidates": [
     "setGroupAdmissionProfile"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-215"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 102. 0 of 0 labels bound to a contract property; 7 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-216",
  "name": "Group Leader & Fast B2B Validation",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.3",
   "page": 103
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/group-leader-fast-b2b-validation-bo-216",
   "component": "apps/venue-management-web/src/routes/access-venue/GroupLeaderFastB2bValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-214"
   ],
   "exitTo": [
    "BO-214"
   ],
   "inferred": false,
   "notes": "**Reached from BO-214, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-214",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F118 step 4→5",
     "operation": "listGroupLeaderFast"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Solve the specific matrix requirement for faster entrance flow when large B2B groups have multiple tickets stored on one device.",
  "purposeNote": "Large B2B groups can be admitted using a streamlined workflow without individually processing every credential when the configured group product allows it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group leader fast",
       "columns": [
        "GroupLeaderFastB2bValidationView.payment",
        "GroupLeaderFastB2bValidationView.booking",
        "GroupLeaderFastB2bValidationView.visitDate",
        "GroupLeaderFastB2bValidationView.groupProduct",
        "GroupLeaderFastB2bValidationView.accessRules",
        "GroupLeaderFastB2bValidationView.manifest"
       ],
       "bindsTo": "GroupLeaderFastB2bValidationView",
       "operation": "listGroupLeaderFast",
       "provenance": "pack Access Control Module_Reference.pdf, page 103 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group leader fast",
       "bindsTo": "GroupLeaderFastB2bValidationView",
       "columns": [
        "GroupLeaderFastB2bValidationView.payment",
        "GroupLeaderFastB2bValidationView.booking",
        "GroupLeaderFastB2bValidationView.visitDate",
        "GroupLeaderFastB2bValidationView.groupProduct",
        "GroupLeaderFastB2bValidationView.accessRules",
        "GroupLeaderFastB2bValidationView.manifest"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Booked”, “SCAN LEADER QR”, “Admit All 120”, “Enter Actual Attendance”, “CONFIRM”, “Attendance”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 103 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group leader fast list.",
   "error": "Could not load. Names which read failed and leaves the group leader fast untouched.",
   "emptyFirstRun": "No group leader fast yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group leader fast are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupLeaderFast",
    "contract": "access",
    "purpose": "Group Leader & Fast B2B Validation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupLeaderFastB2bValidationView.payment",
    "GroupLeaderFastB2bValidationView.booking",
    "GroupLeaderFastB2bValidationView.visitDate",
    "GroupLeaderFastB2bValidationView.groupProduct",
    "GroupLeaderFastB2bValidationView.accessRules",
    "GroupLeaderFastB2bValidationView.manifest"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-216"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 103. 6 of 6 labels bound to a contract property; 6 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-217",
  "name": "Group Attendance & Partial Entry Manager",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.4",
   "page": 104
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/group-attendance-partial-entry-manager-bo-217",
   "component": "apps/venue-management-web/src/routes/access-venue/GroupAttendancePartialEntryManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-214"
   ],
   "exitTo": [
    "BO-214"
   ],
   "inferred": false,
   "notes": "**Reached from BO-214, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-214",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F118 step 6→7",
     "operation": "listGroupAttendancePartial"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage actual attendance when fewer guests arrive than the quantity purchased. The matrix explicitly requires the scanner to show the exact group size and allow the operator to enter actual attendants so daily attendance is updated correctly.",
  "purposeNote": "Attendance reflects the number of guests actually admitted rather than simply the quantity on the group ticket.",
  "gaps": [
   {
    "operation": null,
    "why": "**Group Attendance & Partial Entry Manager declares no operation that writes anything** — its only declared call is `listGroupAttendancePartial`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 104"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 104"
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
       "impliedBy": "listGroupAttendancePartial",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group attendance partial list.",
   "error": "Could not load. Names which read failed and leaves the group attendance partial untouched.",
   "emptyFirstRun": "No group attendance partial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group attendance partial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupAttendancePartial",
    "contract": "access",
    "purpose": "Group Attendance & Partial Entry Manager",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupAttendancePartialEntryManagerView.purchased50",
    "GroupAttendancePartialEntryManagerView.previouslyEntered0",
    "GroupAttendancePartialEntryManagerView.entered43",
    "GroupAttendancePartialEntryManagerView.remaining7",
    "GroupAttendancePartialEntryManagerView.remaining"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-217"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 104. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-218",
  "name": "Family, Child, POD & Companion Journey",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.5",
   "page": 105
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/family-child-pod-companion-journey-bo-218",
   "component": "apps/venue-management-web/src/routes/access-venue/FamilyChildPodCompanionJourney.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-214"
   ],
   "exitTo": [
    "BO-214"
   ],
   "inferred": false,
   "notes": "**Reached from BO-214, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-214",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F118 step 8→9",
     "operation": "listFamilyChildPod"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure linked-person access journeys. The matrix requires child protection through adult-ticket pairing or biometric validation of the assigned adult. It also requires POD accompanying persons and nannies to be bound to a primary guest and only enter when accompanied by that guest.",
  "purposeNote": "Dependent and companion credentials cannot bypass their configured relationship requirements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Parent → Child",
       "provenance": "pack Access Control Module_Reference.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Guardian → Minor",
       "provenance": "pack Access Control Module_Reference.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "POD → Companion",
       "provenance": "pack Access Control Module_Reference.pdf, page 105 §Configure"
      },
      {
       "kind": "textField",
       "label": "Primary Guest → Nanny",
       "provenance": "pack Access Control Module_Reference.pdf, page 105 §Configure"
      },
      {
       "kind": "textField",
       "label": "Group Leader → Group Member",
       "provenance": "pack Access Control Module_Reference.pdf, page 105 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The family child pod configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the family child pod untouched.",
   "emptyFirstRun": "No family child pod configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFamilyChildPod",
    "contract": "access",
    "purpose": "Family, Child, POD & Companion Journey",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-218"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 105. 0 of 0 labels bound to a contract property; 5 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-219",
  "name": "Re-entry & Temporary Exit Journey",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.6",
   "page": 106
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/re-entry-temporary-exit-journey-bo-219",
   "component": "apps/venue-management-web/src/routes/access-venue/ReEntryTemporaryExitJourney.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-214"
   ],
   "exitTo": [
    "BO-214"
   ],
   "inferred": false,
   "notes": "**Reached from BO-214, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-214",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F118 step 10→11",
     "operation": "listEntryTemporaryExit"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage guests temporarily leaving and returning to the venue. The source matrix requires configurable re-entry and also describes a journey using a designated re-entry gate with both ticket verification and a UV stamp.",
  "purposeNote": "Temporary exit and re-entry are tracked as distinct journey events rather than being counted as new normal admissions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Credential only",
       "provenance": "pack Access Control Module_Reference.pdf, page 106 §Configure"
      },
      {
       "kind": "textField",
       "label": "Credential + UV stamp",
       "provenance": "pack Access Control Module_Reference.pdf, page 106 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential + Face",
       "provenance": "pack Access Control Module_Reference.pdf, page 106 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential + operator",
       "provenance": "pack Access Control Module_Reference.pdf, page 106 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The re-entry temporary exit configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the re-entry temporary exit untouched.",
   "emptyFirstRun": "No re-entry temporary exit configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEntryTemporaryExit",
    "contract": "access",
    "purpose": "Re-entry & Temporary Exit Journey",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-219"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 106. 0 of 0 labels bound to a contract property; 4 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-220",
  "name": "Multi-Park & Crossover Journey Orchestrator",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.7",
   "page": 108
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/multi-park-crossover-journey-orchestrator-bo-220",
   "component": "apps/venue-management-web/src/routes/access-venue/MultiParkCrossoverJourneyOrchestrator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-214"
   ],
   "exitTo": [
    "BO-214"
   ],
   "inferred": false,
   "notes": "**Reached from BO-214, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-214",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F118 step 12→13",
     "operation": "listMultiParkCrossover2"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Operationalize the multi-park rules configured in Board 2. The matrix specifically distinguishes crossover from normal entry and re-entry and requires crossover to be tracked separately.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 108"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 108"
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
       "impliedBy": "listMultiParkCrossover2",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-park crossover journey list.",
   "error": "Could not load. Names which read failed and leaves the multi-park crossover journey untouched.",
   "emptyFirstRun": "No multi-park crossover journey yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-park crossover journey are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMultiParkCrossover2",
    "contract": "access",
    "purpose": "Multi-Park & Crossover Journey Orchestrator",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MultiParkCrossoverJourneyOrchestratorView.maximum",
    "MultiParkCrossoverJourneyOrchestratorView.adventureParkInside",
    "MultiParkCrossoverJourneyOrchestratorView.waterParkCrossoverAvailable",
    "MultiParkCrossoverJourneyOrchestratorView.normalEntry",
    "MultiParkCrossoverJourneyOrchestratorView.reEntry"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-220"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 108. 0 of 0 labels bound to a contract property; 0 of 6 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-221",
  "name": "Fast Pass & Attraction Access Journey",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.8",
   "page": 109
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/fast-pass-attraction-access-journey-bo-221",
   "component": "apps/venue-management-web/src/routes/access-venue/FastPassAttractionAccessJourney.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-214"
   ],
   "exitTo": [
    "BO-214"
   ],
   "inferred": false,
   "notes": "**Reached from BO-214, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-214",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F118 step 14→15",
     "operation": "listFastPassAttraction"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select eligible) and no display directory — it is settings, not a population",
  "purpose": "Configure the operational experience for limited and unlimited priority-access entitlements. The matrix requires Silver Fast Pass to support three accesses and Gold to support unlimited access with an optional one-access-per-ride restriction.",
  "purposeNote": "Priority-access journeys correctly consume and display limited/unlimited entitlement usage.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Roller Coaster",
       "provenance": "pack Access Control Module_Reference.pdf, page 109 §Select eligible"
      },
      {
       "kind": "selectField",
       "label": "Drop Tower",
       "provenance": "pack Access Control Module_Reference.pdf, page 109 §Select eligible"
      },
      {
       "kind": "selectField",
       "label": "Water Ride",
       "provenance": "pack Access Control Module_Reference.pdf, page 109 §Select eligible"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fast pass attraction configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the fast pass attraction untouched.",
   "emptyFirstRun": "No fast pass attraction configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFastPassAttraction",
    "contract": "access",
    "purpose": "Fast Pass & Attraction Access Journey",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-221"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 109. 0 of 0 labels bound to a contract property; 3 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-222",
  "name": "Special Event, Free View & Alternative Admission",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.9",
   "page": 110
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/special-event-free-view-alternative-admission-bo-222",
   "component": "apps/venue-management-web/src/routes/access-venue/SpecialEventFreeViewAlternativeAdmission.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-214"
   ],
   "exitTo": [
    "BO-214"
   ],
   "inferred": false,
   "notes": "**Reached from BO-214, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-214",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F118 step 16→17",
     "operation": "listSpecialEventFree"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure temporary/special admission processes that differ from normal venue access. The matrix requires special-event products capable of capturing attendance without physical admission, N- person attendance entered through a turnstile/tablet/handheld, and Free View days where main gates are open while attraction gates continue validating tickets.",
  "purposeNote": "Special admission processes can temporarily replace normal access behavior without permanent gate reconfiguration.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "15 Sep 2026",
       "provenance": "pack Access Control Module_Reference.pdf, page 110 §Configure"
      },
      {
       "kind": "selectField",
       "label": "08:00–18:00",
       "provenance": "pack Access Control Module_Reference.pdf, page 110 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The special event free configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the special event free untouched.",
   "emptyFirstRun": "No special event free configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSpecialEventFree",
    "contract": "access",
    "purpose": "Special Event, Free View & Alternative Admission",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-222"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 110. 0 of 0 labels bound to a contract property; 2 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-223",
  "name": "Journey Simulation, Audit & Publication",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "8",
   "number": "8.10",
   "page": 111
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/journey-simulation-audit-publication-bo-223",
   "component": "apps/venue-management-web/src/routes/access-venue/JourneySimulationAuditPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-214"
   ],
   "exitTo": [
    "BO-214"
   ],
   "inferred": false,
   "notes": "**Reached from BO-214, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Test an entire guest journey—not merely an individual scan—before deploying it.",
  "purposeNote": "Complex guest journeys can be simulated end-to-end, approved, deployed, audited and rolled back. Board 8 — Final 10-Screen Structure # Backend Screen Main Responsibility 8.1 Guest Journey Command Center Special journey management and monitoring 8.2 Group & B2B Admission Profile Builder Configure group-access models 8.3 Group Leader & Fast B2B Validation Accelerate large-group entry 8.4 Group Attendance & Partial Entry Manager Actual attendance and multiple arrival waves 8.5 Family, Child, POD & Companion Journey Linked-person and child-protection journeys 8.6 Re-entry & Temporary Exit Journey",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Free View Day. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Access Control Module_Reference.pdf, page 111 §Support"
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
       "label": "Every journey simulation audit",
       "columns": [
        "impossible journey sequences",
        "missing gates",
        "incompatible hardware",
        "missing companion relationship",
        "conflicting quantities",
        "duplicate attendance"
       ],
       "bindsTo": "Journey",
       "operation": "listJourneys",
       "provenance": "pack Access Control Module_Reference.pdf, page 111 §Detect"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected journey simulation audit",
       "bindsTo": "Journey",
       "columns": [
        "impossible journey sequences",
        "missing gates",
        "incompatible hardware",
        "missing companion relationship",
        "conflicting quantities",
        "duplicate attendance"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Purchased”, “Arrive”, “Simulation Trace”, “Attendance”, “Remaining”, “Journey Audit”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 111 §Detect"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Free View Day",
       "provenance": "pack Access Control Module_Reference.pdf, page 111 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The journey simulation audit list.",
   "error": "Could not load. Names which read failed and leaves the journey simulation audit untouched.",
   "emptyFirstRun": "No journey simulation audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the journey simulation audit are still there. Names the active filter and offers to clear it.",
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
  "entryState": {
   "preloaded": [
    "impossible journey sequences",
    "missing gates",
    "incompatible hardware",
    "missing companion relationship",
    "conflicting quantities",
    "duplicate attendance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-223"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 111. 0 of 6 labels bound to a contract property; 7 of 94 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listEntryTemporaryExit": {
  "method": "GET",
  "path": "/entry-temporary-exit",
  "contract": "access",
  "summary": "Re-entry & Temporary Exit Journey",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReEntryTemporaryExitJourneyView"
 },
 "listFamilyChildPod": {
  "method": "GET",
  "path": "/family-child-pod",
  "contract": "access",
  "summary": "Family, Child, POD & Companion Journey",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FamilyChildPodCompanionJourneyView"
 },
 "listFastPassAttraction": {
  "method": "GET",
  "path": "/fast-pass-attraction",
  "contract": "access",
  "summary": "Fast Pass & Attraction Access Journey",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FastPassAttractionAccessJourneyView"
 },
 "listGroupAttendancePartial": {
  "method": "GET",
  "path": "/group-attendance-partial",
  "contract": "access",
  "summary": "Group Attendance & Partial Entry Manager",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupAttendancePartialEntryManagerView"
 },
 "listGroupLeaderFast": {
  "method": "GET",
  "path": "/group-leader-fast",
  "contract": "access",
  "summary": "Group Leader & Fast B2B Validation",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupLeaderFastB2bValidationView"
 },
 "listGuestJourney": {
  "method": "GET",
  "path": "/guest-journey",
  "contract": "access",
  "summary": "Guest Journey Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestJourneyCommandCenterView"
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
  "responds": "Journey"
 },
 "listMultiParkCrossover2": {
  "method": "GET",
  "path": "/multi-park-crossover-2",
  "contract": "access",
  "summary": "Multi-Park & Crossover Journey Orchestrator",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MultiParkCrossoverJourneyOrchestratorView"
 },
 "listSpecialEventFree": {
  "method": "GET",
  "path": "/special-event-free",
  "contract": "access",
  "summary": "Special Event, Free View & Alternative Admission",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SpecialEventFreeViewAlternativeAdmissionView"
 },
 "setGroupAdmissionProfile": {
  "method": "PUT",
  "path": "/group-admission-profile",
  "contract": "access",
  "summary": "Group & B2B Admission Profile Builder",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "GroupB2bAdmissionProfileBuilderInput",
  "responds": "GroupB2bAdmissionProfileBuilderView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "FamilyChildPodCompanionJourneyView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Family, Child, POD & Companion Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "parentChild": {
    "type": "string",
    "description": "Parent → Child"
   },
   "guardianMinor": {
    "type": "string",
    "description": "Guardian → Minor"
   },
   "podCompanion": {
    "type": "string",
    "description": "POD → Companion"
   },
   "primaryGuestNanny": {
    "type": "string",
    "description": "Primary Guest → Nanny"
   },
   "groupLeaderGroupMember": {
    "type": "string",
    "description": "Group Leader → Group Member"
   },
   "otherAuthorizedRelationships": {
    "type": "string",
    "description": "other authorized relationships"
   }
  }
 },
 "FastPassAttractionAccessJourneyView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Fast Pass & Attraction Access Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalUses": {
    "type": "integer",
    "description": "Total Uses (the pack shows 3)"
   },
   "rideCoaster": {
    "type": "string",
    "description": "Ride: Coaster"
   },
   "previousUse1032": {
    "type": "string",
    "description": "Previous Use: 10:32"
   },
   "eligibleYes": {
    "type": "string",
    "description": "Eligible: YES"
   },
   "eligibleType": {
    "type": "string",
    "enum": [
     "rollerCoaster",
     "dropTower",
     "waterRide",
     "adventureRide"
    ],
    "description": "Vocabulary listed under Select eligible."
   }
  }
 },
 "GroupAttendancePartialEntryManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Group Attendance & Partial Entry Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "purchased50": {
    "type": "string",
    "description": "Purchased: 50"
   },
   "previouslyEntered0": {
    "type": "string",
    "description": "Previously Entered: 0"
   },
   "entered43": {
    "type": "string",
    "description": "Entered: 43"
   },
   "remaining7": {
    "type": "string",
    "description": "Remaining: 7"
   },
   "remaining": {
    "type": "string",
    "description": "Remaining (the pack shows 7, 2)"
   },
   "guestsArriving": {
    "type": "string",
    "description": "Guests arriving (the pack shows 104 | Pa ge, 5)"
   },
   "totalEntered": {
    "type": "integer",
    "description": "Total Entered (the pack shows 48)"
   },
   "group": {
    "type": "string",
    "description": "Group"
   },
   "leader": {
    "type": "string",
    "description": "Leader"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "operator": {
    "type": "string",
    "description": "Operator"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "device": {
    "type": "string",
    "description": "Device"
   }
  }
 },
 "GroupB2bAdmissionProfileBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Group & B2B Admission Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "schools": {
    "type": "string",
    "description": "Schools"
   },
   "tourOperators": {
    "type": "string",
    "description": "Tour Operators"
   },
   "corporateGroups": {
    "type": "string",
    "description": "Corporate Groups"
   },
   "resellers": {
    "type": "string",
    "description": "Resellers"
   },
   "travelGroups": {
    "type": "string",
    "description": "Travel Groups"
   },
   "camps": {
    "type": "string",
    "description": "Camps"
   },
   "families": {
    "type": "string",
    "description": "Families"
   },
   "events": {
    "type": "string",
    "description": "Events"
   },
   "singleGroupQr": {
    "type": "string",
    "description": "Single Group QR"
   },
   "groupBarcode": {
    "type": "string",
    "description": "Group Barcode"
   },
   "groupRfid": {
    "type": "string",
    "description": "Group RFID"
   },
   "groupLeaderCredential": {
    "type": "string",
    "description": "Group Leader Credential"
   },
   "individualCredentials": {
    "type": "string",
    "description": "Individual Credentials"
   },
   "hybrid": {
    "type": "string",
    "description": "Hybrid"
   },
   "entireGroup": {
    "type": "string",
    "description": "Entire Group"
   },
   "partialGroup": {
    "type": "string",
    "description": "Partial Group"
   },
   "multipleWaves": {
    "type": "string",
    "description": "Multiple Waves"
   },
   "individualScan": {
    "type": "string",
    "description": "Individual Scan"
   },
   "leaderQuantity": {
    "type": "integer",
    "description": "Leader + Quantity"
   },
   "manifestBased": {
    "type": "string",
    "description": "Manifest-Based"
   }
  }
 },
 "GroupB2bAdmissionProfileBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Group & B2B Admission Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "schools": {
    "type": "string",
    "description": "Schools"
   },
   "tourOperators": {
    "type": "string",
    "description": "Tour Operators"
   },
   "corporateGroups": {
    "type": "string",
    "description": "Corporate Groups"
   },
   "resellers": {
    "type": "string",
    "description": "Resellers"
   },
   "travelGroups": {
    "type": "string",
    "description": "Travel Groups"
   },
   "camps": {
    "type": "string",
    "description": "Camps"
   },
   "families": {
    "type": "string",
    "description": "Families"
   },
   "events": {
    "type": "string",
    "description": "Events"
   },
   "singleGroupQr": {
    "type": "string",
    "description": "Single Group QR"
   },
   "groupBarcode": {
    "type": "string",
    "description": "Group Barcode"
   },
   "groupRfid": {
    "type": "string",
    "description": "Group RFID"
   },
   "groupLeaderCredential": {
    "type": "string",
    "description": "Group Leader Credential"
   },
   "individualCredentials": {
    "type": "string",
    "description": "Individual Credentials"
   },
   "hybrid": {
    "type": "string",
    "description": "Hybrid"
   },
   "purchasedGuests": {
    "type": "integer",
    "description": "Purchased Guests (the pack shows 50)"
   },
   "entireGroup": {
    "type": "string",
    "description": "Entire Group"
   },
   "partialGroup": {
    "type": "string",
    "description": "Partial Group"
   },
   "multipleWaves": {
    "type": "string",
    "description": "Multiple Waves"
   },
   "individualScan": {
    "type": "string",
    "description": "Individual Scan"
   },
   "leaderQuantity": {
    "type": "integer",
    "description": "Leader + Quantity"
   },
   "manifestBased": {
    "type": "string",
    "description": "Manifest-Based"
   }
  }
 },
 "GroupLeaderFastB2bValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Group Leader & Fast B2B Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "group120Guests": {
    "type": "string",
    "description": "GROUP: 120 GUESTS"
   },
   "attendance": {
    "type": "integer",
    "description": "Attendance (the pack shows +112)"
   },
   "remaining": {
    "type": "string",
    "description": "Remaining (the pack shows 8)"
   },
   "payment": {
    "type": "string",
    "description": "Payment ✓"
   },
   "booking": {
    "type": "string",
    "description": "Booking ✓"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date ✓"
   },
   "groupProduct": {
    "type": "string",
    "description": "Group Product ✓"
   },
   "accessRules": {
    "type": "string",
    "description": "Access Rules ✓"
   },
   "manifest": {
    "type": "string",
    "description": "Manifest ✓"
   }
  }
 },
 "GuestJourneyCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Guest Journey Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeJourneyProfiles": {
    "type": "integer",
    "description": "Active Journey Profiles"
   },
   "groupArrivalsToday": {
    "type": "string",
    "description": "Group Arrivals Today"
   },
   "guestsViaGroupAdmission": {
    "type": "string",
    "description": "Guests via Group Admission"
   },
   "familyJourneys": {
    "type": "integer",
    "description": "Family Journeys"
   },
   "reEntryGuests": {
    "type": "integer",
    "description": "Re-entry Guests"
   },
   "crossoversToday": {
    "type": "string",
    "description": "Crossovers Today"
   },
   "fastPassValidations": {
    "type": "integer",
    "description": "Fast Pass Validations"
   },
   "specialEventAdmissions": {
    "type": "integer",
    "description": "Special Event Admissions"
   },
   "vipAdmissions": {
    "type": "integer",
    "description": "VIP Admissions"
   },
   "journeyExceptions": {
    "type": "integer",
    "description": "Journey Exceptions"
   },
   "delayedGroups": {
    "type": "string",
    "description": "delayed groups"
   },
   "unusuallyHighManualIntervention": {
    "type": "string",
    "description": "unusually high manual intervention"
   },
   "incompleteGroupEntry": {
    "type": "string",
    "description": "incomplete group entry"
   },
   "companionViolations": {
    "type": "string",
    "description": "companion violations"
   },
   "crossoverExceptions": {
    "type": "string",
    "description": "crossover exceptions"
   },
   "fastPassAnomalies": {
    "type": "string",
    "description": "Fast Pass anomalies"
   }
  }
 },
 "Journey": {
  "type": "object",
  "x-ticvai-persistence": "marketing.journey",
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
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
    "description": "For `send`. Channel is resolved from the guest's preference at the moment of sending."
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
    "nullable": true
   },
   "goalEvent": {
    "type": "string",
    "nullable": true,
    "description": "For `goal`. **The event that means this journey worked and the guest should leave it** — a purchase for abandoned cart, a renewal for membership. **Reaching a goal exits immediately**, which is what stops a recovered cart from being chased.\n"
   }
  }
 },
 "MultiParkCrossoverJourneyOrchestratorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Multi-Park & Crossover Journey Orchestrator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximum": {
    "type": "string",
    "description": "Maximum (the pack shows 1)"
   },
   "adventureParkInside": {
    "type": "string",
    "description": "Adventure Park — INSIDE"
   },
   "waterParkCrossoverAvailable": {
    "type": "string",
    "description": "Water Park — CROSSOVER AVAILABLE"
   },
   "normalEntry": {
    "type": "string",
    "description": "Normal Entry"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "crossover": {
    "type": "string",
    "description": "Crossover"
   }
  }
 },
 "ReEntryTemporaryExitJourneyView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Re-entry & Temporary Exit Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "credentialOnly": {
    "type": "string",
    "description": "Credential only"
   },
   "credentialUvStamp": {
    "type": "string",
    "description": "Credential + UV stamp"
   },
   "credentialFace": {
    "type": "string",
    "description": "Credential + Face"
   },
   "credentialOperator": {
    "type": "string",
    "description": "Credential + operator"
   },
   "customSupportedMethod": {
    "type": "string",
    "description": "custom supported method"
   },
   "maximum": {
    "type": "string",
    "description": "Maximum (the pack shows 1)"
   },
   "previousEntry": {
    "type": "string",
    "description": "✓ Previous entry"
   },
   "validExit": {
    "type": "string",
    "description": "✓ Valid exit"
   },
   "reEntryEntitlement": {
    "type": "string",
    "description": "✓ Re-entry entitlement"
   },
   "reEntryQuantity": {
    "type": "integer",
    "description": "✓ Re-entry quantity"
   },
   "correctGate": {
    "type": "string",
    "description": "✓ Correct gate"
   },
   "antiPassback": {
    "type": "string",
    "description": "✓ Anti-passback"
   },
   "additionalVerification": {
    "type": "string",
    "description": "✓ Additional verification"
   }
  }
 },
 "SpecialEventFreeViewAlternativeAdmissionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Special Event, Free View & Alternative Admission displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "exampleFreeViewDay": {
    "type": "string",
    "description": "Example — Free View Day"
   },
   "on": {
    "type": "string",
    "description": "ON"
   },
   "attendance": {
    "type": "integer",
    "description": "Attendance (the pack shows +85)"
   },
   "exampleSpecialEvent": {
    "type": "string",
    "description": "Example — Special Event"
   }
  }
 }
}
```
