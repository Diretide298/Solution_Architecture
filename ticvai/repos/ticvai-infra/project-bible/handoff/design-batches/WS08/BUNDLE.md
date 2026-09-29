# WS08 — Access Control board 8

**10 screens · 22 operations · 33 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ACCESS_POINT_CONFIGURE, MARKETING_VIEW, QUEUE_MANAGE, QUEUE_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-214` | Guest Journey Command Center | listDetail | 3 | 1 | — |
| `BO-215` | Group & B2B Admission Profile Builder | configEditor | 1 | 0 | — |
| `BO-216` | Group Leader & Fast B2B Validation | listDetail | 1 | 0 | — |
| `BO-217` | Group Attendance & Partial Entry Manager | listDetail | 1 | 0 | — |
| `BO-218` | Family, Child, POD & Companion Journey | configEditor | 2 | 0 | — |
| `BO-219` | Re-entry & Temporary Exit Journey | configEditor | 3 | 0 | — |
| `BO-220` | Multi-Park & Crossover Journey Orchestrator | listDetail | 4 | 0 | — |
| `BO-221` | Fast Pass & Attraction Access Journey | configEditor | 4 | 1 | — |
| `BO-222` | Special Event, Free View & Alternative Admission | configEditor | 4 | 1 | — |
| `BO-223` | Journey Simulation, Audit & Publication | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-216, BO-217, BO-220, BO-222 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — BO-100 declares entryState.params  and BO-214 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Journey Profiles",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.activeJourneyProfiles",
       "operation": "listGuestJourney",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Group Arrivals Today",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.groupArrivalsToday",
       "operation": "listGuestJourney",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Guests via Group Admission",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.guestsViaGroupAdmission",
       "operation": "listGuestJourney",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Family Journeys",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.familyJourneys",
       "operation": "listGuestJourney",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Re-entry Guests",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.reEntryGuests",
       "operation": "listGuestJourney",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Crossovers Today",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.crossoversToday",
       "operation": "listGuestJourney",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Fast Pass Validations",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.fastPassValidations",
       "operation": "listGuestJourney",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Special Event Admissions",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.specialEventAdmissions",
       "operation": "listGuestJourney",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "VIP Admissions",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.vipAdmissions",
       "operation": "listGuestJourney",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Journey Exceptions",
       "bindsTo": "GuestJourneyCommandCenterViewSummary.journeyExceptions",
       "operation": "listGuestJourney",
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
       "label": "Every guest journey",
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
       "notes": "The pack groups this record's detail under its own headings: “Journey Type Venue Credential Status”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 101 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save journey profile",
       "operation": "setJourneyProfile",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind the Guest Journey Command Center** (BO-214): a named journey (e.g.",
       "provenance": "contract access.yaml PUT /journey-profiles"
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
   },
   {
    "operationId": "createAdmissionRules",
    "contract": "access",
    "purpose": "Start a new guest journey from an admission profile",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listGuestJourney"
    ]
   },
   {
    "operationId": "setJourneyProfile",
    "contract": "access",
    "purpose": "Create or replace a guest journey profile",
    "trigger": "onAction",
    "invalidates": [
     "listGuestJourney"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "GuestJourneyCommandCenterViewSummary.activeJourneyProfiles",
    "GuestJourneyCommandCenterViewSummary.groupArrivalsToday",
    "GuestJourneyCommandCenterViewSummary.guestsViaGroupAdmission",
    "GuestJourneyCommandCenterViewSummary.familyJourneys",
    "GuestJourneyCommandCenterViewSummary.reEntryGuests",
    "GuestJourneyCommandCenterViewSummary.crossoversToday"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-214",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-214"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 101. 10 of 10 labels bound to a contract property; 10 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetJourneyProfile",
    "component": "modal",
    "trigger": "Save journey profile",
    "body": "**Collects what `setJourneyProfile` sends before it is called.** Required: `id`, `scopePath`, `name`, `status`. Optional: `venueId`, `journeyType`, `credentialType`, `steps`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessJourneyProfile",
    "confirm": {
     "label": "Save journey profile",
     "operation": "setJourneyProfile"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "name",
      "status",
      "venueId",
      "journeyType",
      "credentialType",
      "steps"
     ]
    },
    "provenance": "contract access.yaml PUT /journey-profiles"
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
  "purposeNote": "Group admission behavior can be configured independently from standard individual-ticket admission.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure admission for) and no display directory — it is settings, not a population",
  "purpose": "Group & B2B Admission Profile Builder",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-215",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-215"
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
  "purposeNote": "Large B2B groups can be admitted using a streamlined workflow without individually processing every credential when the configured group product allows it.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Solve the specific matrix requirement for faster entrance flow when large B2B groups have multiple tickets stored on one device.",
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
    "GroupLeaderFastB2bValidationView.groupProduct",
    "GroupLeaderFastB2bValidationView.accessRules",
    "GroupLeaderFastB2bValidationView.manifest"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-216",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-216"
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
  "purposeNote": "Attendance reflects the number of guests actually admitted rather than simply the quantity on the group ticket.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage actual attendance when fewer guests arrive than the quantity purchased. The matrix explicitly requires the scanner to show the exact group size and allow the operator to enter actual attendants so daily attendance is updated correctly.",
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
    "GroupAttendancePartialEntryManagerView.remaining"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-217",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-217"
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
  "purposeNote": "Dependent and companion credentials cannot bypass their configured relationship requirements.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure linked-person access journeys. The matrix requires child protection through adult-ticket pairing or biometric validation of the assigned adult. It also requires POD accompanying persons and nannies to be bound to a primary guest and only enter when accompanied by that guest.",
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save companion rule",
       "operation": "setGuestCompanionEligibility",
       "provenance": "contract access.yaml PUT /guest-companion-eligibility (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setGuestCompanionEligibility",
    "contract": "access",
    "purpose": "Save companion rule",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-218",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-218"
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
  "purposeNote": "Temporary exit and re-entry are tracked as distinct journey events rather than being counted as new normal admissions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage guests temporarily leaving and returning to the venue. The source matrix requires configurable re-entry and also describes a journey using a designated re-entry gate with both ticket verification and a UV stamp.",
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
   },
   {
    "operationId": "listAdmissionRules",
    "contract": "access",
    "purpose": "The admission profiles that allow a temporary exit",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "updateAdmissionRules",
    "contract": "access",
    "purpose": "Save re-entry quantity and the exit-before-re-entry rule",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listEntryTemporaryExit",
     "listAdmissionRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-219",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-219"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 106. 0 of 0 labels bound to a contract property; 4 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "profileId",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save admission rules",
       "operation": "updateAdmissionRules",
       "provenance": "contract access.yaml PUT /admission-rules/{profileId} (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "listMultiParkCrossover",
    "contract": "access",
    "purpose": "Multi-Park & Crossover Rules",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAdmissionRules",
    "contract": "access",
    "purpose": "The admission profiles that carry crossover rules",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "updateAdmissionRules",
    "contract": "access",
    "purpose": "Save the parks a crossover journey admits to",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listMultiParkCrossover2",
     "listMultiParkCrossover",
     "listAdmissionRules"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "MultiParkCrossoverJourneyOrchestratorView.eventType"
   ],
   "params": [
    {
     "name": "profileId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-220",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-220"
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
  "purposeNote": "Priority-access journeys correctly consume and display limited/unlimited entitlement usage.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select eligible) and no display directory — it is settings, not a population",
  "purpose": "Configure the operational experience for limited and unlimited priority-access entitlements. The matrix requires Silver Fast Pass to support three accesses and Gold to support unlimited access with an optional one-access-per-ride restriction.",
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save Fast Pass settings",
       "operation": "updateQueue",
       "provenance": "contract queue.yaml PATCH /queues/{queueId} (decided 29 September, VM close-out)"
      },
      {
       "kind": "secondaryButton",
       "label": "Save fast pass profile",
       "operation": "setFastPassProfile",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind Fast Pass & Attraction Access Journey** (BO-221): a Fast Pass profile (e.g.",
       "provenance": "contract access.yaml PUT /fast-pass-profiles"
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
   },
   {
    "operationId": "listQueues",
    "contract": "queue",
    "purpose": "The attraction lanes a Fast Pass is configured on",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateQueue",
    "contract": "queue",
    "purpose": "Save Fast Pass settings",
    "trigger": "onAction"
   },
   {
    "operationId": "setFastPassProfile",
    "contract": "access",
    "purpose": "Create or replace a Fast Pass profile",
    "trigger": "onAction",
    "invalidates": [
     "listFastPassAttraction",
     "listQueues"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-221",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-221"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 109. 0 of 0 labels bound to a contract property; 3 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "queueId",
     "from": "navigation"
    }
   ]
  },
  "overlays": [
   {
    "id": "formSetFastPassProfile",
    "component": "modal",
    "trigger": "Save fast pass profile",
    "body": "**Collects what `setFastPassProfile` sends before it is called.** Required: `id`, `scopePath`, `name`, `unlimited`. Optional: `venueId`, `totalUses`, `consumptionPerValidation`, `onePerRide`, `eligibleAttractionCategories`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessFastPassProfile",
    "confirm": {
     "label": "Save fast pass profile",
     "operation": "setFastPassProfile"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "name",
      "unlimited",
      "venueId",
      "totalUses",
      "consumptionPerValidation",
      "onePerRide",
      "eligibleAttractionCategories"
     ]
    },
    "provenance": "contract access.yaml PUT /fast-pass-profiles"
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
  "purposeNote": "Special admission processes can temporarily replace normal access behavior without permanent gate reconfiguration.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure temporary/special admission processes that differ from normal venue access. The matrix requires special-event products capable of capturing attendance without physical admission, N- person attendance entered through a turnstile/tablet/handheld, and Free View days where main gates are open while attraction gates continue validating tickets.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save operating calendar entry",
       "operation": "setOperatingCalendarEntry",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind Operating Calendar & Special Access Days** (BO-152) and Special Event, Free View & Alternative Admission (BO-222): one dated entry (a holiday, private event, free-entry day, special event and so on), whether tickets must be validated, and for a free-view or special-event window its admission type.",
       "provenance": "contract access.yaml PUT /operating-calendar-entries"
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
   },
   {
    "operationId": "createAdmissionRules",
    "contract": "access",
    "purpose": "Create a special-event or free-view admission profile",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listSpecialEventFree"
    ]
   },
   {
    "operationId": "setContextTimeEvent",
    "contract": "access",
    "purpose": "Tie the alternative admission to a date, event or calendar day",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listSpecialEventFree"
    ]
   },
   {
    "operationId": "setOperatingCalendarEntry",
    "contract": "access",
    "purpose": "Create or replace an operating calendar entry",
    "trigger": "onAction",
    "invalidates": [
     "listSpecialEventFree"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-222",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-222"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 110. 0 of 0 labels bound to a contract property; 2 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetOperatingCalendarEntry",
    "component": "modal",
    "trigger": "Save operating calendar entry",
    "body": "**Collects what `setOperatingCalendarEntry` sends before it is called.** Required: `id`, `venueId`, `dayType`, `startsAt`, `endsAt`, `scopePath`. Optional: `name`, `ticketValidationRequired`, `admissionType`, `attractionValidation`, `manualAttendanceRequired`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessOperatingCalendarEntry",
    "confirm": {
     "label": "Save operating calendar entry",
     "operation": "setOperatingCalendarEntry"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "dayType",
      "startsAt",
      "endsAt",
      "scopePath",
      "name",
      "ticketValidationRequired",
      "admissionType",
      "attractionValidation",
      "manualAttendanceRequired"
     ]
    },
    "provenance": "contract access.yaml PUT /operating-calendar-entries"
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
  "purposeNote": "Complex guest journeys can be simulated end-to-end, approved, deployed, audited and rolled back. Board 8 — Final 10-Screen Structure # Backend Screen Main Responsibility 8.1 Guest Journey Command Center Special journey management and monitoring 8.2 Group & B2B Admission Profile Builder Configure group-access models 8.3 Group Leader & Fast B2B Validation Accelerate large-group entry 8.4 Group Attendance & Partial Entry Manager Actual attendance and multiple arrival waves 8.5 Family, Child, POD & Companion Journey Linked-person and child-protection journeys 8.6 Re-entry & Temporary Exit Journey",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Test an entire guest journey—not merely an individual scan—before deploying it.",
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
      },
      {
       "kind": "primaryButton",
       "label": "Run journey simulation",
       "operation": "simulateGuestJourney",
       "provenance": "contract access.yaml POST /guest-journey/simulate (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "simulateGuestJourney",
    "contract": "access",
    "purpose": "Run journey simulation",
    "trigger": "onAction"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-223",
   "workshopBoard": "wireframes/WS25 Access Control Board 8.dc.html#bo-223"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 111. 0 of 6 labels bound to a contract property; 7 of 94 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `simulateGuestJourney`.",
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
 "createAdmissionRules": {
  "method": "POST",
  "path": "/admission-rules",
  "contract": "access",
  "summary": "Create an admission profile",
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
  "requestBody": "AdmissionRules",
  "responds": "AdmissionRules"
 },
 "listAdmissionRules": {
  "method": "GET",
  "path": "/admission-rules",
  "contract": "access",
  "summary": "List admission profiles",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
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
 "listEntryTemporaryExit": {
  "method": "GET",
  "path": "/entry-temporary-exit",
  "contract": "access",
  "summary": "Re-entry & Temporary Exit Journey",
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
 "listGroupLeaderFast": {
  "method": "GET",
  "path": "/group-leader-fast",
  "contract": "access",
  "summary": "Group Leader & Fast B2B Validation",
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
 "listGuestJourney": {
  "method": "GET",
  "path": "/guest-journey",
  "contract": "access",
  "summary": "Guest Journey Command Center",
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
 "listMultiParkCrossover": {
  "method": "GET",
  "path": "/multi-park-crossover",
  "contract": "access",
  "summary": "Multi-Park & Crossover Rules",
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
  "responds": "MultiParkCrossoverRulesView"
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
 "listQueues": {
  "method": "GET",
  "path": "/queues",
  "contract": "queue",
  "summary": "List queues",
  "permission": "QUEUE_VIEW",
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
    "name": "openOnly",
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
 "listSpecialEventFree": {
  "method": "GET",
  "path": "/special-event-free",
  "contract": "access",
  "summary": "Special Event, Free View & Alternative Admission",
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
  "responds": "SpecialEventFreeViewAlternativeAdmissionView"
 },
 "setContextTimeEvent": {
  "method": "PUT",
  "path": "/context-time-event",
  "contract": "access",
  "summary": "Context, Time, Event & Capacity Policy Builder",
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
  "requestBody": "ContextTimeEventCapacityPolicyBuilderInput",
  "responds": "ContextTimeEventCapacityPolicyBuilderView"
 },
 "setFastPassProfile": {
  "method": "PUT",
  "path": "/fast-pass-profiles",
  "contract": "access",
  "summary": "Create or replace a Fast Pass profile",
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
  "requestBody": "AccessFastPassProfile",
  "responds": "AccessFastPassProfile"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GroupB2bAdmissionProfileBuilderInput",
  "responds": "GroupB2bAdmissionProfileBuilderView"
 },
 "setGuestCompanionEligibility": {
  "method": "PUT",
  "path": "/guest-companion-eligibility",
  "contract": "access",
  "summary": "Save a companion eligibility rule",
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
  "requestBody": "GuestCompanionEligibilityRulesInput",
  "responds": "GuestCompanionEligibilityRulesView"
 },
 "setJourneyProfile": {
  "method": "PUT",
  "path": "/journey-profiles",
  "contract": "access",
  "summary": "Create or replace a guest journey profile",
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
  "requestBody": "AccessJourneyProfile",
  "responds": "AccessJourneyProfile"
 },
 "setOperatingCalendarEntry": {
  "method": "PUT",
  "path": "/operating-calendar-entries",
  "contract": "access",
  "summary": "Create or replace an operating calendar entry",
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
  "requestBody": "AccessOperatingCalendarEntry",
  "responds": "AccessOperatingCalendarEntry"
 },
 "simulateGuestJourney": {
  "method": "POST",
  "path": "/guest-journey/simulate",
  "contract": "access",
  "summary": "Simulate an access journey",
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
  "requestBody": "GuestJourneySimulationInput",
  "responds": "GuestJourneySimulationView"
 },
 "updateAdmissionRules": {
  "method": "PUT",
  "path": "/admission-rules/{profileId}",
  "contract": "access",
  "summary": "Update an admission profile",
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
  "requestBody": "AdmissionRules",
  "responds": "AdmissionRules"
 },
 "updateQueue": {
  "method": "PATCH",
  "path": "/queues/{queueId}",
  "contract": "queue",
  "summary": "Amend queue configuration",
  "permission": "QUEUE_MANAGE",
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
  "responds": "Queue"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessFastPassProfile": {
  "type": "object",
  "x-ticvai-persistence": "access.fast_pass_profile",
  "description": "One Fast Pass profile (e.g. Silver, Gold) - total uses or unlimited, uses consumed per validation, the one-access-per-ride restriction and the eligible attraction categories (declared 29 September, data-model close-out DM1).",
  "required": [
   "id",
   "scopePath",
   "name",
   "unlimited"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The profileId the list shows"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "unlimited": {
    "type": "boolean",
    "default": false
   },
   "totalUses": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Null when unlimited"
   },
   "consumptionPerValidation": {
    "type": "integer",
    "minimum": 1,
    "default": 1
   },
   "onePerRide": {
    "type": "boolean",
    "default": false
   },
   "eligibleAttractionCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "The list's eligibleType, e.g. rollerCoaster, dropTower, waterRide, adventureRide"
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
 "AccessJourneyProfile": {
  "type": "object",
  "x-ticvai-persistence": "access.journey_profile",
  "description": "One guest access journey profile (e.g. School Group Entry) - type, venue, credential used, status and the ordered steps a simulation walks (declared 29 September, data-model close-out DM1).",
  "required": [
   "id",
   "scopePath",
   "name",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The journeyProfileId"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null is every park of the tenant"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "journeyType": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "description": "e.g. B2B group, family"
   },
   "credentialType": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "e.g. group QR, mixed"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "inactive"
    ],
    "default": "active"
   },
   "steps": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessJsonList"
     }
    ],
    "description": "Ordered journey steps, each an accessPointId with a direction (entry or exit) and an optional local time HH:MM, as GuestJourneySimulationInput.steps"
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
 "AccessJsonList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the row that holds it.** A short list of structured entries read with its row and never queried on its own (thresholds, per-language messages, field mappings, steps), so a child table would add a join for nothing. The property that uses it says what an entry holds (declared 29 September, data-model close-out DM1).",
  "items": {
   "type": "object"
  }
 },
 "AccessOperatingCalendarEntry": {
  "type": "object",
  "x-ticvai-persistence": "access.operating_calendar_entry",
  "description": "One dated entry in a venue operating calendar (normal day, holiday, private event, free-entry day, special event and so on), with whether tickets must be validated. Merges access.special_admission_window, whose free-view and special-event windows are entries carrying an admission type (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "venueId",
   "dayType",
   "startsAt",
   "endsAt",
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
   "dayType": {
    "type": "string",
    "enum": [
     "normalOperatingDay",
     "weekend",
     "holiday",
     "seasonalSchedule",
     "privateEvent",
     "freeEntryDay",
     "maintenancePeriod",
     "specialEvent",
     "ladiesOnlySession",
     "schoolGroupSession",
     "afterHoursEvent"
    ],
    "description": "Kind of calendar entry"
   },
   "name": {
    "type": "string",
    "nullable": true
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "ticketValidationRequired": {
    "type": "boolean",
    "default": true,
    "description": "False on free-entry days"
   },
   "admissionType": {
    "type": "string",
    "enum": [
     "freeViewDay",
     "specialEvent"
    ],
    "nullable": true,
    "description": "Set on special admission windows only"
   },
   "attractionValidation": {
    "type": "boolean",
    "nullable": true,
    "description": "Special windows: attraction gates keep validating tickets"
   },
   "manualAttendanceRequired": {
    "type": "boolean",
    "nullable": true,
    "description": "Special windows: operator enters attendance count"
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
 "AdmissionRules": {
  "x-ticvai-persistence": "access.admission_rules",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "openMinutesBefore",
   "closeMinutesAfter"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Server-assigned.** Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names.\n"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "perProductRules": {
    "allOf": [
     {
      "$ref": "#/components/schemas/PerProductRuleList"
     }
    ],
    "description": "BL-059. **Transaction rules were per profile and a ticket type could not state its own.** An annual pass allowing one entry per day and a single ticket allowing one entry ever are different rules, and forcing a profile per product multiplies profiles instead.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "openMinutesBefore": {
    "type": "integer",
    "description": "How long before a performance validation opens."
   },
   "closeMinutesAfter": {
    "type": "integer"
   },
   "maxDurationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false
   },
   "maxReentries": {
    "type": "integer",
    "nullable": true
   },
   "entryLimit": {
    "type": "object",
    "description": "**How many times the credential may enter** (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). Absent means `unlimited`.",
    "required": [
     "mode"
    ],
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "unlimited",
       "once",
       "nTimes",
       "nPerDay",
       "nPerPeriod"
      ],
      "default": "unlimited"
     },
     "count": {
      "type": "integer",
      "minimum": 1,
      "description": "N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it)"
     },
     "periodDays": {
      "type": "integer",
      "minimum": 1,
      "description": "The period for nPerPeriod"
     }
    }
   },
   "exitScan": {
    "type": "string",
    "enum": [
     "required",
     "optional",
     "none"
    ],
    "default": "optional",
    "description": "(decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. `optional`: exits run in free rotation and headcount is inferred. `none`: the exit has no reader."
   },
   "maxExits": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Null is unlimited (decided 29 September, VM close-out)"
   },
   "reEntryWindowMinutes": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out)"
   },
   "sameDayOnly": {
    "type": "boolean",
    "default": true,
    "description": "Re-entry only on the day of the exit (decided 29 September, VM close-out)"
   },
   "designatedAccessPointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out)"
   },
   "validity": {
    "type": "object",
    "description": "**When the credential is valid** (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). The admission window above still applies inside it.",
    "required": [
     "anchor"
    ],
    "properties": {
     "anchor": {
      "type": "string",
      "enum": [
       "fixedRange",
       "afterSale",
       "afterActivation",
       "afterFirstUse"
      ],
      "description": "fixedRange uses from and to; the others count days from the event"
     },
     "days": {
      "type": "integer",
      "minimum": 1,
      "description": "N days after the anchor; required unless the anchor is fixedRange"
     },
     "from": {
      "type": "string",
      "format": "date"
     },
     "to": {
      "type": "string",
      "format": "date",
      "description": "Inclusive. Must not be before from (`422`)"
     },
     "endOf": {
      "type": "string",
      "enum": [
       "day",
       "week",
       "month",
       "year"
      ],
      "nullable": true,
      "description": "Validity runs to the end of the day, week, month or year the relative period ends in"
     },
     "daysOfWeek": {
      "type": "array",
      "items": {
       "type": "string",
       "enum": [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun"
       ]
      },
      "description": "Empty is every day"
     },
     "dayTypes": {
      "type": "array",
      "items": {
       "type": "string",
       "enum": [
        "peakDates",
        "offPeakDates",
        "holidays",
        "seasons",
        "eventDates"
       ]
      },
      "description": "Calendar day types on which access is allowed; empty is every day type"
     },
     "blackoutDates": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "date"
      },
      "description": "Dates on which access is refused whatever else allows it"
     }
    }
   },
   "crossover": {
    "type": "object",
    "nullable": true,
    "description": "**Crossover between parks** (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. Null means the profile admits to one park only.",
    "required": [
     "allowedParkOrgUnitIds"
    ],
    "properties": {
     "allowedParkOrgUnitIds": {
      "type": "array",
      "minItems": 2,
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "parkOrder": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      },
      "description": "Required order of parks, if any; empty is any order"
     },
     "sameDayOnly": {
      "type": "boolean",
      "default": true
     },
     "differentDayAccess": {
      "type": "boolean",
      "default": false
     },
     "dayPattern": {
      "type": "string",
      "enum": [
       "consecutiveFromFirstScan",
       "flexibleWithinValidity"
      ],
      "default": "flexibleWithinValidity"
     },
     "maxParkEntries": {
      "type": "integer",
      "minimum": 1,
      "nullable": true,
      "description": "Null is unlimited"
     },
     "crossoverQuantity": {
      "type": "integer",
      "minimum": 1,
      "nullable": true,
      "description": "How many crossovers; null is unlimited"
     },
     "crossoverAfterTime": {
      "type": "string",
      "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
      "nullable": true,
      "description": "Earliest venue-local time HH:MM a crossover is allowed"
     },
     "prerequisiteParkOrgUnitId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The park that must be entered first"
     },
     "reEntryAfterCrossover": {
      "type": "boolean",
      "default": false
     }
    }
   },
   "allowedAccessPointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Empty means any access point in the venue."
   },
   "reEntryVerification": {
    "type": "string",
    "enum": [
     "credentialOnly",
     "credentialUvStamp",
     "credentialFace",
     "credentialOperator",
     "custom"
    ],
    "default": "credentialOnly",
    "description": "What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1)."
   },
   "ruleConditions": {
    "type": "object",
    "nullable": true,
    "description": "The visual rule builder body `setVisualAccessRule` writes: `appliesTo` (products or credential types), `conditions`, `logic` (AND / OR / NOT over the conditions), `decision` (allow, deny, referToOperator, overrideEligible) and `consequences`. **One `jsonb` column on the rule row**, read with the rule and never queried on its own; the locations stay in `access.entry_rule_point` (added 29 September, data-model close-out DM1)."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ContextTimeEventCapacityPolicyBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Context, Time, Event & Capacity Policy Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "result": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ]
   },
   "conditionExpression": {
    "type": "string",
    "description": "e.g. Zone Occupancy >= 90% AND Day = Friday AND Time BETWEEN 18:00 AND 23:59"
   },
   "name": {
    "type": "string"
   },
   "policyId": {
    "type": "string"
   },
   "contextType": {
    "type": "string",
    "enum": [
     "date",
     "day",
     "time",
     "season",
     "event",
     "performance",
     "specialEvent",
     "holiday",
     "operatingCalendar",
     "occupancy",
     "attractionStatus"
    ],
    "description": "Kind of venue condition the policy reacts to"
   },
   "monitorThresholdPercent": {
    "type": "integer",
    "description": "Occupancy percent at which the band becomes Monitor"
   },
   "restrictThresholdPercent": {
    "type": "integer",
    "description": "Occupancy percent at which the band becomes Restrict"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "inactive"
    ],
    "default": "active",
    "description": "`inactive` switches the policy off at once; `active` on a new or inactive policy submits it for approval (`pendingApproval`) (decided 29 September, writers pass)"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Start of validity; null for at once (decided 29 September, writers pass)"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "End of validity: after it a timer moves the policy to `expired` (decided 29 September, writers pass)"
   }
  },
  "required": [
   "policyId",
   "name",
   "contextType",
   "conditionExpression",
   "result"
  ]
 },
 "ContextTimeEventCapacityPolicyBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Context, Time, Event & Capacity Policy Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "result": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ]
   },
   "conditionExpression": {
    "type": "string",
    "description": "e.g. Zone Occupancy >= 90% AND Day = Friday AND Time BETWEEN 18:00 AND 23:59"
   },
   "name": {
    "type": "string"
   },
   "policyId": {
    "type": "string"
   },
   "contextType": {
    "type": "string",
    "enum": [
     "date",
     "day",
     "time",
     "season",
     "event",
     "performance",
     "specialEvent",
     "holiday",
     "operatingCalendar",
     "occupancy",
     "attractionStatus"
    ],
    "description": "Kind of venue condition the policy reacts to"
   },
   "monitorThresholdPercent": {
    "type": "integer",
    "description": "Occupancy percent at which the band becomes Monitor"
   },
   "restrictThresholdPercent": {
    "type": "integer",
    "description": "Occupancy percent at which the band becomes Restrict"
   }
  },
  "required": [
   "policyId",
   "name",
   "contextType",
   "conditionExpression",
   "result"
  ]
 },
 "CreateQueueRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "capacityPerCycle",
   "cycleMinutes"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "attractionProductId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "standby",
     "singleRider",
     "fastPass",
     "virtual",
     "accessible",
     "groupOnly",
     "staffOnly"
    ],
    "default": "standby",
    "description": "5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"
   },
   "operatingWindows": {
    "type": "array",
    "description": "**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n",
    "items": {
     "type": "object",
     "required": [
      "day",
      "from",
      "to"
     ],
     "properties": {
      "day": {
       "type": "string",
       "enum": [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun"
       ]
      },
      "from": {
       "type": "string",
       "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
       "description": "Venue local time, 24-hour `HH:MM`, when the queue starts running."
      },
      "to": {
       "type": "string",
       "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
       "description": "Venue local time, 24-hour `HH:MM`, when the queue stops running."
      },
      "lastEntryMinutesBefore": {
       "type": "integer",
       "default": 0,
       "description": "**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"
      }
     }
    }
   },
   "parentQueueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"
   },
   "loadBalanceWithQueueIds": {
    "type": "array",
    "description": "BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "inQueueOfferEnabled": {
    "type": "boolean",
    "default": false,
    "description": "**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"
   },
   "notifyBeforeCallMinutes": {
    "type": "integer",
    "default": 5,
    "description": "BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"
   },
   "capacityPerCycle": {
    "type": "integer",
    "minimum": 1
   },
   "cycleMinutes": {
    "type": "number",
    "minimum": 0
   },
   "maxPartySize": {
    "type": "integer",
    "default": 6
   },
   "returnWindowMinutes": {
    "type": "integer",
    "default": 15,
    "description": "How long a called party has to arrive before the entry expires."
   },
   "heightRequirementCm": {
    "type": "integer",
    "nullable": true
   },
   "fastPassAllocationPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "default": 0,
    "description": "Share of each cycle reserved for Fast Pass holders."
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "fastPass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/QueueFastPass"
     }
    ],
    "nullable": true,
    "description": "The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"
   }
  }
 },
 "FamilyChildPodCompanionJourneyView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Family, Child, POD & Companion Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Companion rule identifier"
   },
   "relationshipType": {
    "type": "string",
    "enum": [
     "parentChild",
     "guardianMinor",
     "podCompanion",
     "primaryGuestNanny",
     "groupLeaderGroupMember",
     "other"
    ],
    "description": "Linked-person relationship this rule governs"
   },
   "verificationMethod": {
    "type": "string",
    "enum": [
     "pairedAdultCredential",
     "assignedAdultBiometric"
    ],
    "description": "How the accompanying adult is verified"
   },
   "assignedAdultRequiredForExit": {
    "type": "boolean",
    "description": "The assigned adult must be present for the dependent to exit"
   }
  },
  "required": [
   "ruleId"
  ]
 },
 "FastPassAttractionAccessJourneyView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Fast Pass & Attraction Access Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "profileId": {
    "type": "string",
    "description": "Fast Pass profile identifier"
   },
   "totalUses": {
    "type": "integer",
    "description": "Total Uses (the pack shows 3)"
   },
   "eligibleType": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Eligible attraction categories: rollerCoaster, dropTower, waterRide, adventureRide"
   },
   "name": {
    "type": "string",
    "description": "Profile name, e.g. Silver, Gold"
   },
   "unlimited": {
    "type": "boolean",
    "description": "Unlimited uses"
   },
   "consumptionPerValidation": {
    "type": "integer",
    "description": "Uses consumed per validation"
   },
   "onePerRide": {
    "type": "boolean",
    "description": "Restrict to one access per ride"
   }
  },
  "required": [
   "profileId"
  ]
 },
 "GroupAttendancePartialEntryManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Group Attendance & Partial Entry Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "waveId": {
    "type": "string",
    "description": "Admission wave identifier"
   },
   "remaining": {
    "type": "integer",
    "description": "Guests still to arrive after this wave"
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
   },
   "purchased": {
    "type": "integer",
    "description": "Guests purchased on the group booking"
   }
  },
  "required": [
   "waveId"
  ]
 },
 "GroupB2bAdmissionProfileBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Group & B2B Admission Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "name": {
    "type": "string",
    "description": "Profile name"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "profileId": {
    "type": "string",
    "description": "The rule row's key (access.group_admission_rule.id); absent creates one (decided 29 September, writers pass)",
    "format": "uuid"
   },
   "groupSegments": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "schools",
      "tourOperators",
      "corporateGroups",
      "resellers",
      "travelGroups",
      "camps",
      "families",
      "events"
     ]
    },
    "description": "Group segments this profile applies to"
   },
   "credentialMode": {
    "type": "string",
    "enum": [
     "singleGroupQr",
     "groupBarcode",
     "groupRfid",
     "groupLeaderCredential",
     "individualCredentials",
     "hybrid"
    ],
    "description": "How the group presents its credentials"
   },
   "admissionMethod": {
    "type": "string",
    "enum": [
     "entireGroup",
     "partialGroup",
     "multipleWaves",
     "individualScan",
     "leaderQuantity",
     "manifestBased"
    ],
    "description": "How the group is admitted at the gate"
   }
  },
  "required": [
   "profileId",
   "venueId",
   "name"
  ]
 },
 "GroupB2bAdmissionProfileBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Group & B2B Admission Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "name": {
    "type": "string",
    "description": "Profile name"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "profileId": {
    "type": "string",
    "description": "Group admission profile identifier"
   },
   "groupSegments": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "schools",
      "tourOperators",
      "corporateGroups",
      "resellers",
      "travelGroups",
      "camps",
      "families",
      "events"
     ]
    },
    "description": "Group segments this profile applies to"
   },
   "credentialMode": {
    "type": "string",
    "enum": [
     "singleGroupQr",
     "groupBarcode",
     "groupRfid",
     "groupLeaderCredential",
     "individualCredentials",
     "hybrid"
    ],
    "description": "How the group presents its credentials"
   },
   "admissionMethod": {
    "type": "string",
    "enum": [
     "entireGroup",
     "partialGroup",
     "multipleWaves",
     "individualScan",
     "leaderQuantity",
     "manifestBased"
    ],
    "description": "How the group is admitted at the gate"
   }
  },
  "required": [
   "profileId",
   "venueId",
   "name"
  ]
 },
 "GroupLeaderFastB2bValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Group Leader & Fast B2B Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "groupBookingId": {
    "type": "string",
    "description": "Group booking"
   },
   "attendance": {
    "type": "integer",
    "description": "Attendance (the pack shows +112)"
   },
   "remaining": {
    "type": "integer",
    "description": "Guests not yet admitted"
   },
   "payment": {
    "type": "boolean",
    "description": "Payment check passed"
   },
   "booking": {
    "type": "boolean",
    "description": "Booking check passed"
   },
   "groupProduct": {
    "type": "boolean",
    "description": "Group product check passed"
   },
   "accessRules": {
    "type": "boolean",
    "description": "Access rules check passed"
   },
   "manifest": {
    "type": "boolean",
    "description": "Manifest check passed"
   },
   "bookedGuests": {
    "type": "integer",
    "description": "Guests booked"
   },
   "visitDateValid": {
    "type": "boolean",
    "description": "Visit date check passed"
   }
  },
  "required": [
   "groupBookingId"
  ]
 },
 "GuestCompanionEligibilityRulesInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Guest, Companion & Eligibility Rules submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "venueId",
   "name",
   "guestCategory",
   "requiredCompanionCategory",
   "verifyAt"
  ],
  "properties": {
   "ruleId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent creates a rule"
   },
   "venueId": {
    "type": "string"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "guestCategory": {
    "type": "string",
    "enum": [
     "adult",
     "child",
     "junior",
     "senior",
     "pod",
     "podCompanion",
     "nanny",
     "vip",
     "member",
     "staff",
     "accreditation",
     "customerSegment"
    ]
   },
   "requiredCompanionCategory": {
    "type": "string",
    "enum": [
     "adult",
     "podCompanion",
     "nanny",
     "guardian"
    ],
    "description": "Category of the companion who must be present"
   },
   "companionVerification": {
    "type": "string",
    "enum": [
     "linkedTicket",
     "companionBiometric"
    ],
    "default": "linkedTicket"
   },
   "verifyAt": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "admission",
      "exit",
      "attraction"
     ]
    },
    "minItems": 1,
    "description": "Where the companion is checked"
   },
   "attractionIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Where verifyAt includes attraction"
   }
  }
 },
 "GuestCompanionEligibilityRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Guest, Companion & Eligibility Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "guestCategory": {
    "type": "string",
    "enum": [
     "adult",
     "child",
     "junior",
     "senior",
     "pod",
     "podCompanion",
     "nanny",
     "vip",
     "member",
     "staff",
     "accreditation",
     "customerSegment"
    ]
   },
   "name": {
    "type": "string"
   },
   "requiredCompanionCategory": {
    "type": "string",
    "description": "Category of the qualifying companion, e.g. adult"
   },
   "companionVerification": {
    "type": "string",
    "enum": [
     "linkedTicket",
     "companionBiometric"
    ]
   },
   "verifyAt": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "admission",
      "exit",
      "attraction"
     ]
    },
    "description": "Where the companion is checked (decided 29 September, VM close-out)"
   },
   "attractionIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  },
  "required": [
   "ruleId",
   "guestCategory"
  ]
 },
 "GuestJourneyCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Guest Journey Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "journeyProfileId": {
    "type": "string",
    "description": "Journey profile identifier"
   },
   "journeyName": {
    "type": "string",
    "description": "Journey, e.g. School Group Entry"
   },
   "journeyType": {
    "type": "string",
    "description": "Journey type, e.g. B2B group, family"
   },
   "venueId": {
    "type": "string",
    "description": "Venue or all parks"
   },
   "credentialType": {
    "type": "string",
    "description": "Credential used, e.g. group QR, mixed"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "inactive"
    ],
    "description": "Status"
   }
  },
  "required": [
   "journeyProfileId"
  ]
 },
 "GuestJourneyCommandCenterViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "activeJourneyProfiles": {
    "type": "integer",
    "description": "Active Journey Profiles"
   },
   "groupArrivalsToday": {
    "type": "integer",
    "description": "Group Arrivals Today"
   },
   "guestsViaGroupAdmission": {
    "type": "integer",
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
    "type": "integer",
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
   }
  }
 },
 "GuestJourneySimulationInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only (decided 29 September, VM close-out)",
  "description": "A journey to simulate against the access rules, before it is published (decided 29 September, VM close-out).",
  "required": [
   "journeyProfileId",
   "scenario"
  ],
  "properties": {
   "journeyProfileId": {
    "type": "string",
    "description": "The access journey (`GuestJourneyCommandCenterView.journeyProfileId`)"
   },
   "scenario": {
    "type": "string",
    "enum": [
     "standardDay",
     "freeViewDay",
     "specialEvent",
     "peakDay"
    ]
   },
   "simulatedDate": {
    "type": "string",
    "format": "date",
    "description": "Date the calendar rules are evaluated for; empty is today"
   },
   "entitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Entitlements the simulated guest holds"
   },
   "steps": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "accessPointId"
     ],
     "properties": {
      "accessPointId": {
       "type": "string"
      },
      "direction": {
       "type": "string",
       "enum": [
        "entry",
        "exit"
       ],
       "default": "entry"
      },
      "at": {
       "type": "string",
       "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
       "description": "Local time HH:MM"
      }
     }
    },
    "minItems": 1,
    "maxItems": 50,
    "description": "The scans, in order"
   }
  }
 },
 "GuestJourneySimulationView": {
  "type": "object",
  "x-ticvai-persistence": "none — computed; nothing is admitted or consumed (decided 29 September, VM close-out)",
  "description": "What each step of a simulated journey would decide (decided 29 September, VM close-out).",
  "required": [
   "journeyProfileId",
   "scenario",
   "steps"
  ],
  "properties": {
   "journeyProfileId": {
    "type": "string"
   },
   "scenario": {
    "type": "string",
    "enum": [
     "standardDay",
     "freeViewDay",
     "specialEvent",
     "peakDay"
    ]
   },
   "passed": {
    "type": "boolean",
    "description": "Every step produced the expected decision"
   },
   "steps": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "accessPointId": {
       "type": "string"
      },
      "decision": {
       "type": "string",
       "enum": [
        "allowed",
        "denied",
        "review"
       ]
      },
      "reasonCode": {
       "type": "string"
      },
      "entitlementConsumed": {
       "type": "string",
       "nullable": true
      },
      "decisionTrace": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
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
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MultiParkCrossoverJourneyOrchestratorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Multi-Park & Crossover Journey Orchestrator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "eventId": {
    "type": "string",
    "description": "Journey event identifier"
   },
   "eventType": {
    "type": "string",
    "enum": [
     "normalEntry",
     "reEntry",
     "crossover"
    ],
    "description": "Kind of admission, tracked separately"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential"
   },
   "fromParkId": {
    "type": "string",
    "description": "Park the guest left"
   },
   "toParkId": {
    "type": "string",
    "description": "Park entered"
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time",
    "description": "When it happened"
   }
  },
  "required": [
   "eventId"
  ]
 },
 "MultiParkCrossoverRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Multi-Park & Crossover Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "allowedParks": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "allowed parks"
   },
   "parkOrder": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Required park order, if any"
   },
   "sameDayCrossover": {
    "type": "boolean",
    "description": "same-day crossover"
   },
   "differentDayAccess": {
    "type": "boolean",
    "description": "different-day access"
   },
   "numberOfParkEntries": {
    "type": "integer",
    "description": "number of park entries"
   },
   "crossoverQuantity": {
    "type": "integer",
    "description": "crossover quantity"
   },
   "crossoverTime": {
    "type": "string",
    "description": "Earliest local time HH:MM a crossover is allowed"
   },
   "prerequisitePark": {
    "type": "string",
    "description": "prerequisite park"
   },
   "reEntryAfterCrossover": {
    "type": "boolean",
    "description": "re-entry after crossover"
   },
   "name": {
    "type": "string"
   },
   "dayPattern": {
    "type": "string",
    "enum": [
     "consecutiveFromFirstScan",
     "flexibleWithinValidity"
    ]
   }
  },
  "required": [
   "ruleId",
   "allowedParks"
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
 "PerProductRuleList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the profile row** (`access.admission_rules.per_product_rules`). The rules are read with the profile and a rule is never queried on its own, so a child table would add a join for nothing.\n",
  "items": {
   "type": "object",
   "properties": {
    "productId": {
     "type": "string",
     "format": "uuid"
    },
    "entriesPerDay": {
     "type": "integer",
     "nullable": true
    },
    "minimumGapMinutes": {
     "type": "integer",
     "nullable": true,
     "description": "**Anti-passback in minutes rather than a boolean.** A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back over a fence.\n"
    },
    "allowedAccessPointIds": {
     "type": "array",
     "items": {
      "type": "string",
      "format": "uuid"
     }
    },
    "biometricPolicy": {
     "allOf": [
      {
       "$ref": "#/components/schemas/BiometricPolicy"
      }
     ],
     "description": "BL-105, 3.2.9. **The biometric check is a property of the product, not of the venue** — memberships checked, day tickets not. It sits here rather than on the profile because `perProductRules` is already where a ticket type states its own terms, and a profile per product would multiply profiles to carry one flag.\n**Absent means `disabled`**, and `disabled` is the answer for every product until somebody chooses otherwise. **Inert while `VenueSettings.biometrics.isEnabled` is false**, so a rules profile copied to another venue cannot begin capturing faces there.\n"
    },
    "maxPassesPerBiometricIdentity": {
     "type": "integer",
     "nullable": true,
     "minimum": 1,
     "description": "BL-096, 2.14.7. **The annual-pass quota, keyed to biometric identity.** `enrolFacePass` already answers 409 where a face is on another annual pass; the constant behind that refusal was one and was invisible. **Null means unlimited** and is the answer for every product that is not an annual pass — a quota applied where nobody asked for one turns a family sharing a day ticket into a fraud alert.\n"
    }
   }
  }
 },
 "Queue": {
  "x-ticvai-persistence": "queue.queue + queue.queue_operating_window",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateQueueRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status",
     "waitingPartyCount"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "status": {
      "$ref": "#/components/schemas/QueueStatus"
     },
     "statusReason": {
      "type": "string",
      "nullable": true
     },
     "waitingPartyCount": {
      "type": "integer"
     },
     "waitingGuestCount": {
      "type": "integer"
     },
     "currentWaitMinutes": {
      "type": "integer",
      "nullable": true
     },
     "waitTimeSource": {
      "$ref": "#/components/schemas/WaitTimeSource"
     },
     "waitTimeAsOf": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"
     },
     "manualWaitExpiresAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"
     },
     "manualWaitNote": {
      "type": "string",
      "maxLength": 200,
      "nullable": true,
      "readOnly": true,
      "description": "The `note` given with the current manual figure. Cleared when it expires."
     },
     "expectedReopenAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "QueueFastPass": {
  "x-ticvai-persistence": "queue.queue",
  "type": "object",
  "description": "**Which Fast Pass entitlements this lane accepts, and how** (decided 29 September, VM close-out; pack 'Access Control Module' p.109, BO-221 Fast Pass & Attraction Access Journey). Fast Pass stays an entitlement owned by Product & Entitlement; this block is the lane's side of it: which products it honours, the return window, a per-guest daily cap and the access points that redeem it. Stored on the queue row. Only meaningful where `kind` is `fastPass` or `fastPassAllocationPercent` is above 0.\n**Four ways into priority, not one** (decided 29 September, build pass; 5.6.7 and 5.6.34). A guest joins this lane as priority when they hold an entitlement from `entitlementProductIds` (VIP, annual pass, premium package), are a member of a tier in `loyaltyTierIds`, qualify for a live promotion in `promotionIds`, or declare an accessibility need where `accessibilityPriority` is on. The first criterion met is recorded on the entry as `WaitingGuest.priorityBasis`. Every criterion is resolved by the server at join time; nothing the request asserts about a tier or a promotion is trusted. All four draw on the same reserved `fastPassAllocationPercent`, so widening who qualifies never widens the share of the ride they take.\n",
  "required": [
   "entitlementProductIds"
  ],
  "properties": {
   "entitlementProductIds": {
    "type": "array",
    "description": "Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "loyaltyTierIds": {
    "type": "array",
    "description": "5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. Read from the guest's own loyalty position at join time, never from the request, so a guest cannot claim a tier they do not hold. Empty: tier grants nothing on this lane.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "promotionIds": {
    "type": "array",
    "description": "5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. A guest qualifies when the promotion's conditions hold for them at join (the evaluation `promotions` already makes for a price), or by presenting its code in `JoinQueueRequest.promotionCode`. A paused or expired promotion grants nothing.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "accessibilityPriority": {
    "type": "boolean",
    "default": false,
    "description": "5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. **Taken on trust**, because asking for proof at a ride entrance is worse than the occasional abuse; the declaration is on the entry, so the operator at the front sees it (`listQueueEntries`). A venue that wants proof sells or issues an accessibility pass and lists it in `entitlementProductIds` instead. **Not the `accessible` lane**: that is where a guest who cannot stand in a switchback waits; this moves them ahead in the lane they chose.\n"
   },
   "returnWindowMinutes": {
    "type": "integer",
    "minimum": 1,
    "maximum": 240,
    "default": 60,
    "description": "How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan.\n"
   },
   "maxPerGuestPerDay": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Fast Pass redemptions one guest may make on this lane per day; null is no cap."
   },
   "allowedAccessPointIds": {
    "type": "array",
    "description": "Access points that redeem Fast Pass for this lane; empty is the queue's own.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "QueueStatus": {
  "type": "string",
  "enum": [
   "open",
   "paused",
   "closed",
   "atCapacity"
  ]
 },
 "ReEntryTemporaryExitJourneyView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Re-entry & Temporary Exit Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Re-entry rule identifier"
   },
   "reEntryVerification": {
    "type": "string",
    "enum": [
     "credentialOnly",
     "credentialUvStamp",
     "credentialFace",
     "credentialOperator",
     "custom"
    ],
    "description": "Verification required at re-entry"
   },
   "maximum": {
    "type": "integer",
    "description": "Maximum re-entries allowed"
   },
   "name": {
    "type": "string",
    "description": "Rule name"
   }
  },
  "required": [
   "ruleId"
  ]
 },
 "SpecialEventFreeViewAlternativeAdmissionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Special Event, Free View & Alternative Admission displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "configId": {
    "type": "string",
    "description": "Special admission configuration identifier"
   },
   "attendance": {
    "type": "integer",
    "description": "Attendance (the pack shows +85)"
   },
   "admissionType": {
    "type": "string",
    "enum": [
     "freeViewDay",
     "specialEvent"
    ],
    "description": "Kind of special admission"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time",
    "description": "Start"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "description": "End"
   },
   "attractionValidation": {
    "type": "boolean",
    "description": "Attraction gates keep validating tickets"
   },
   "manualAttendanceRequired": {
    "type": "boolean",
    "description": "Operator enters attendance count"
   }
  },
  "required": [
   "configId"
  ]
 },
 "WaitTimeSource": {
  "type": "string",
  "description": "Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n",
  "enum": [
   "sensor",
   "throughput",
   "manual",
   "unavailable"
  ]
 }
}
```
