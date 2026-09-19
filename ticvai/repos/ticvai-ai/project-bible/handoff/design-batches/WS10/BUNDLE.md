# WS10 — Access Control board 10

**10 screens · 10 operations · 15 schemas · 3 permissions**

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
  `ACCESS_POINT_CONFIGURE, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-234` | Dynamic Access Policy Command Center | listDetail | 1 | 0 | — |
| `BO-235` | Access Attribute Catalog | listDetail | 1 | 0 | — |
| `BO-236` | Visual Dynamic Policy Builder | listDetail | 1 | 0 | — |
| `BO-237` | Context, Time, Event & Capacity Policy Builder | commandCentre | 1 | 0 | — |
| `BO-238` | Identity, Membership & Accreditation Policies | listDetail | 1 | 0 | — |
| `BO-239` | Policy Scope, Hierarchy & Inheritance | configEditor | 1 | 0 | — |
| `BO-240` | Authorization Governance & Temporary Access | listDetail | 1 | 0 | — |
| `BO-241` | Policy Evaluation Architecture & Offline Distribution | listDetail | 1 | 0 | — |
| `BO-242` | Policy Simulation, Conflict & Impact Analysis | listDetail | 1 | 0 | — |
| `BO-243` | Policy Approval, Audit, Analytics & AI Optimization | listDetail | 1 | 1 | — |

## Thin screens in this batch

**BO-234, BO-235, BO-236, BO-237, BO-238, BO-240, BO-241, BO-242 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-234",
  "name": "Dynamic Access Policy Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.1",
   "page": 133
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/dynamic-access-policy-command-center-bo-234",
   "component": "apps/venue-management-web/src/routes/access-venue/DynamicAccessPolicyCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-235",
    "BO-236",
    "BO-237",
    "BO-238",
    "BO-239",
    "BO-240",
    "BO-241",
    "BO-242",
    "BO-243"
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
     "to": "BO-235",
     "trigger": "Works in Access Attribute Catalog",
     "provenance": "flow F120 step 1→2",
     "operation": "listDynamicAccessPolicy"
    },
    {
     "to": "BO-236",
     "trigger": "Works in Visual Dynamic Policy Builder",
     "provenance": "flow F120 step 3→4",
     "operation": "listDynamicAccessPolicy"
    },
    {
     "to": "BO-237",
     "trigger": "Works in Context, Time, Event & Capacity Policy Builder",
     "provenance": "flow F120 step 5→6",
     "operation": "listDynamicAccessPolicy"
    },
    {
     "to": "BO-238",
     "trigger": "Works in Identity, Membership & Accreditation Policies",
     "provenance": "flow F120 step 7→8",
     "operation": "listDynamicAccessPolicy"
    },
    {
     "to": "BO-239",
     "trigger": "Works in Policy Scope, Hierarchy & Inheritance",
     "provenance": "flow F120 step 9→10",
     "operation": "listDynamicAccessPolicy"
    },
    {
     "to": "BO-240",
     "trigger": "Works in Authorization Governance & Temporary Access",
     "provenance": "flow F120 step 11→12",
     "operation": "listDynamicAccessPolicy"
    },
    {
     "to": "BO-241",
     "trigger": "Works in Policy Evaluation Architecture & Offline Distribution",
     "provenance": "flow F120 step 13→14",
     "operation": "listDynamicAccessPolicy"
    },
    {
     "to": "BO-242",
     "trigger": "Works in Policy Simulation, Conflict & Impact Analysis",
     "provenance": "flow F120 step 15→16",
     "operation": "listDynamicAccessPolicy"
    },
    {
     "to": "BO-243",
     "trigger": "Works in Policy Approval, Audit, Analytics & AI Optimization",
     "provenance": "flow F120 step 17→18",
     "operation": "listDynamicAccessPolicy"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide central governance and visibility over all dynamic access policies.",
  "purposeNote": "Administrators can centrally understand the status, scope, performance and conflicts of all dynamic access policies.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every dynamic access policy",
       "columns": [
        "DynamicAccessPolicyCommandCenterView.activePolicies",
        "DynamicAccessPolicyCommandCenterView.draftPolicies",
        "DynamicAccessPolicyCommandCenterView.policiesPendingApproval",
        "DynamicAccessPolicyCommandCenterView.policiesTriggeredToday",
        "DynamicAccessPolicyCommandCenterView.allowDecisions",
        "DynamicAccessPolicyCommandCenterView.denyDecisions",
        "Review Decisions",
        "DynamicAccessPolicyCommandCenterView.policyConflicts",
        "DynamicAccessPolicyCommandCenterView.expiringPolicies",
        "DynamicAccessPolicyCommandCenterView.aiRecommendations"
       ],
       "bindsTo": "DynamicAccessPolicyCommandCenterView",
       "operation": "listDynamicAccessPolicy",
       "provenance": "pack Access Control Module_Reference.pdf, page 133 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dynamic access policy",
       "bindsTo": "DynamicAccessPolicyCommandCenterView",
       "columns": [
        "DynamicAccessPolicyCommandCenterView.activePolicies",
        "DynamicAccessPolicyCommandCenterView.draftPolicies",
        "DynamicAccessPolicyCommandCenterView.policiesPendingApproval",
        "DynamicAccessPolicyCommandCenterView.policiesTriggeredToday",
        "DynamicAccessPolicyCommandCenterView.allowDecisions",
        "DynamicAccessPolicyCommandCenterView.denyDecisions",
        "Review Decisions",
        "DynamicAccessPolicyCommandCenterView.policyConflicts",
        "DynamicAccessPolicyCommandCenterView.expiringPolicies",
        "DynamicAccessPolicyCommandCenterView.aiRecommendations"
       ],
       "notes": null,
       "provenance": "pack Access Control Module_Reference.pdf, page 133 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic access policy list.",
   "error": "Could not load. Names which read failed and leaves the dynamic access policy untouched.",
   "emptyFirstRun": "No dynamic access policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic access policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicAccessPolicy",
    "contract": "access",
    "purpose": "Dynamic Access Policy Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DynamicAccessPolicyCommandCenterView.activePolicies",
    "DynamicAccessPolicyCommandCenterView.draftPolicies",
    "DynamicAccessPolicyCommandCenterView.policiesPendingApproval",
    "DynamicAccessPolicyCommandCenterView.policiesTriggeredToday",
    "DynamicAccessPolicyCommandCenterView.allowDecisions",
    "DynamicAccessPolicyCommandCenterView.denyDecisions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-234"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 133. 9 of 10 labels bound to a contract property; 10 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-235",
  "name": "Access Attribute Catalog",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.2",
   "page": 134
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-attribute-catalog-bo-235",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessAttributeCatalog.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-234"
   ],
   "exitTo": [
    "BO-234"
   ],
   "inferred": false,
   "notes": "**Reached from BO-234, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-234",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F120 step 2→3",
     "operation": "listAccessAttributeCatalog"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the attributes available to the TICVAI policy engine. This becomes the reusable data dictionary for dynamic access decisions.",
  "purposeNote": "Policy designers use governed attributes rather than manually creating inconsistent fields in individual policies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 134"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 134"
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
       "impliedBy": "listAccessAttributeCatalog",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access attribute catalog list.",
   "error": "Could not load. Names which read failed and leaves the access attribute catalog untouched.",
   "emptyFirstRun": "No access attribute catalog yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access attribute catalog are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessAttributeCatalog",
    "contract": "access",
    "purpose": "Access Attribute Catalog",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AccessAttributeCatalogView.age",
    "AccessAttributeCatalogView.genderWhereLegallyBusinessPermitted",
    "AccessAttributeCatalogView.customerSegment",
    "AccessAttributeCatalogView.guestCategory",
    "AccessAttributeCatalogView.countryResidencyWhereApplicable"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-235"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 134. 0 of 0 labels bound to a contract property; 0 of 62 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-236",
  "name": "Visual Dynamic Policy Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.3",
   "page": 136
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/visual-dynamic-policy-builder-bo-236",
   "component": "apps/venue-management-web/src/routes/access-venue/VisualDynamicPolicyBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-234"
   ],
   "exitTo": [
    "BO-234"
   ],
   "inferred": false,
   "notes": "**Reached from BO-234, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-234",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F120 step 4→5",
     "operation": "setVisualDynamicPolicy"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a no-code interface for constructing contextual access policies.",
  "purposeNote": "Business administrators can create sophisticated contextual access policies without development work.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 136"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 136"
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
       "provenance": "contract operation setVisualDynamicPolicy"
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
       "impliedBy": "setVisualDynamicPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The visual dynamic policy list.",
   "error": "Could not load. Names which read failed and leaves the visual dynamic policy untouched.",
   "emptyFirstRun": "No visual dynamic policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visual dynamic policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualDynamicPolicy",
    "contract": "access",
    "purpose": "Visual Dynamic Policy Builder",
    "trigger": "onAction",
    "invalidates": [
     "setVisualDynamicPolicy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-236"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 136. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-237",
  "name": "Context, Time, Event & Capacity Policy Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.4",
   "page": 137
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/context-time-event-capacity-policy-builder-bo-237",
   "component": "apps/venue-management-web/src/routes/access-venue/ContextTimeEventCapacityPolicyBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-234"
   ],
   "exitTo": [
    "BO-234"
   ],
   "inferred": false,
   "notes": "**Reached from BO-234, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-234",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F120 step 6→7",
     "operation": "setContextTimeEvent"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§MONITOR) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Configure policies driven by changing venue conditions rather than only guest attributes.",
  "purposeNote": "Access behavior can dynamically respond to operating calendars, events, capacity, occupancy and venue status.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "90–94%",
       "provenance": "pack Access Control Module_Reference.pdf, page 137 §MONITOR"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setContextTimeEvent"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The context time event list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the context time event untouched.",
   "emptyFirstRun": "No context time event yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the context time event are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setContextTimeEvent",
    "contract": "access",
    "purpose": "Context, Time, Event & Capacity Policy Builder",
    "trigger": "onAction",
    "invalidates": [
     "setContextTimeEvent"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-237"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 137. 0 of 0 labels bound to a contract property; 1 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-238",
  "name": "Identity, Membership & Accreditation Policies",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.5",
   "page": 139
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/identity-membership-accreditation-policies-bo-238",
   "component": "apps/venue-management-web/src/routes/access-venue/IdentityMembershipAccreditationPolicies.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-234"
   ],
   "exitTo": [
    "BO-234"
   ],
   "inferred": false,
   "notes": "**Reached from BO-234, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-234",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F120 step 8→9",
     "operation": "listIdentityMembershipAccreditation"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure policies based on who the requesting person is.",
  "purposeNote": "Memberships, staff identities and accreditations can participate directly in access-policy decisions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Guest, Security. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Access Control Module_Reference.pdf, page 139 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 139"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 139"
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
       "label": "Guest",
       "provenance": "pack Access Control Module_Reference.pdf, page 139 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Security",
       "provenance": "pack Access Control Module_Reference.pdf, page 139 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The identity membership accreditation list.",
   "error": "Could not load. Names which read failed and leaves the identity membership accreditation untouched.",
   "emptyFirstRun": "No identity membership accreditation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the identity membership accreditation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listIdentityMembershipAccreditation",
    "contract": "access",
    "purpose": "Identity, Membership & Accreditation Policies",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "IdentityMembershipAccreditationPoliciesView.guest",
    "IdentityMembershipAccreditationPoliciesView.member",
    "IdentityMembershipAccreditationPoliciesView.annualPassHolder",
    "IdentityMembershipAccreditationPoliciesView.employee",
    "IdentityMembershipAccreditationPoliciesView.contractor"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-238"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 139. 0 of 0 labels bound to a contract property; 2 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-239",
  "name": "Policy Scope, Hierarchy & Inheritance",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.6",
   "page": 140
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/policy-scope-hierarchy-inheritance-bo-239",
   "component": "apps/venue-management-web/src/routes/access-venue/PolicyScopeHierarchyInheritance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-234"
   ],
   "exitTo": [
    "BO-234"
   ],
   "inferred": false,
   "notes": "**Reached from BO-234, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-234",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F120 step 10→11",
     "operation": "listPolicyScopeHierarchy"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrator defines) and no display directory — it is settings, not a population",
  "purpose": "Govern how policies apply across TICVAI's multi-tenant and multi-venue architecture.",
  "purposeNote": "Policies behave predictably across tenants, venues and access hierarchies.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Highest Priority Wins",
       "provenance": "pack Access Control Module_Reference.pdf, page 140 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Deny Overrides Allow",
       "provenance": "pack Access Control Module_Reference.pdf, page 140 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Most Specific Wins",
       "provenance": "pack Access Control Module_Reference.pdf, page 140 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Mandatory Parent Wins",
       "provenance": "pack Access Control Module_Reference.pdf, page 140 §Administrator defines"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The policy scope hierarchy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the policy scope hierarchy untouched.",
   "emptyFirstRun": "No policy scope hierarchy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPolicyScopeHierarchy",
    "contract": "access",
    "purpose": "Policy Scope, Hierarchy & Inheritance",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-239"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 140. 0 of 0 labels bound to a contract property; 4 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-240",
  "name": "Authorization Governance & Temporary Access",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.7",
   "page": 142
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/authorization-governance-temporary-access-bo-240",
   "component": "apps/venue-management-web/src/routes/access-venue/AuthorizationGovernanceTemporaryAccess.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-234"
   ],
   "exitTo": [
    "BO-234"
   ],
   "inferred": false,
   "notes": "**Reached from BO-234, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-234",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F120 step 12→13",
     "operation": "listAuthorizationGovernanceTemporary"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Apply enterprise governance principles to privileged and temporary access.",
  "purposeNote": "Privileged and temporary access follows controlled authorization rather than informal manual permissions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 142"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 142"
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
       "impliedBy": "listAuthorizationGovernanceTemporary",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The authorization governance temporary list.",
   "error": "Could not load. Names which read failed and leaves the authorization governance temporary untouched.",
   "emptyFirstRun": "No authorization governance temporary yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the authorization governance temporary are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAuthorizationGovernanceTemporary",
    "contract": "access",
    "purpose": "Authorization Governance & Temporary Access",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AuthorizationGovernanceTemporaryAccessView.leastPrivilege",
    "AuthorizationGovernanceTemporaryAccessView.segregationOfDuties",
    "AuthorizationGovernanceTemporaryAccessView.temporaryAccess",
    "AuthorizationGovernanceTemporaryAccessView.expiringGrants",
    "AuthorizationGovernanceTemporaryAccessView.delegatedAdministration"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-240"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 142. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-241",
  "name": "Policy Evaluation Architecture & Offline Distribution",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.8",
   "page": 143
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/policy-evaluation-architecture-offline-distribution-bo-241",
   "component": "apps/venue-management-web/src/routes/access-venue/PolicyEvaluationArchitectureOfflineDistribution.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-234"
   ],
   "exitTo": [
    "BO-234"
   ],
   "inferred": false,
   "notes": "**Reached from BO-234, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-234",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F120 step 14→15",
     "operation": "listPolicyEvaluationArchitecture"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define where and how policies are evaluated. This screen connects Board 10 with the offline/edge architecture already configured in Board 7.",
  "purposeNote": "Every policy has a defined evaluation location and predictable behavior when connectivity or data sources are unavailable.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 143"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 143"
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
       "impliedBy": "listPolicyEvaluationArchitecture",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The policy evaluation architecture list.",
   "error": "Could not load. Names which read failed and leaves the policy evaluation architecture untouched.",
   "emptyFirstRun": "No policy evaluation architecture yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the policy evaluation architecture are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPolicyEvaluationArchitecture",
    "contract": "access",
    "purpose": "Policy Evaluation Architecture & Offline Distribution",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PolicyEvaluationArchitectureOfflineDistributionView.evaluatedAtVenueEdge",
    "PolicyEvaluationArchitectureOfflineDistributionView.evaluatedLocallyWhereSupported",
    "PolicyEvaluationArchitectureOfflineDistributionView.centralUnavailable"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-241"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 143. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-242",
  "name": "Policy Simulation, Conflict & Impact Analysis",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.9",
   "page": 144
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/policy-simulation-conflict-impact-analysis-bo-242",
   "component": "apps/venue-management-web/src/routes/access-venue/PolicySimulationConflictImpactAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-234"
   ],
   "exitTo": [
    "BO-234"
   ],
   "inferred": false,
   "notes": "**Reached from BO-234, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-234",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F120 step 16→17",
     "operation": "simulatePolicyConflictImpact"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Test policies before they affect live guest admission.",
  "purposeNote": "No policy reaches production without visibility into conflicts and potential operational impact.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every policy simulation conflict",
       "columns": [
        "PolicySimulationConflictImpactAnalysisView.policiesInvolved",
        "PolicySimulationConflictImpactAnalysisView.hierarchy",
        "PolicySimulationConflictImpactAnalysisView.priority",
        "PolicySimulationConflictImpactAnalysisView.resultingDecision",
        "PolicySimulationConflictImpactAnalysisView.affectedProducts",
        "PolicySimulationConflictImpactAnalysisView.affectedVenues"
       ],
       "bindsTo": "PolicySimulationConflictImpactAnalysisView",
       "operation": "simulatePolicyConflictImpact",
       "provenance": "pack Access Control Module_Reference.pdf, page 144 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected policy simulation conflict",
       "bindsTo": "PolicySimulationConflictImpactAnalysisView",
       "columns": [
        "PolicySimulationConflictImpactAnalysisView.policiesInvolved",
        "PolicySimulationConflictImpactAnalysisView.hierarchy",
        "PolicySimulationConflictImpactAnalysisView.priority",
        "PolicySimulationConflictImpactAnalysisView.resultingDecision",
        "PolicySimulationConflictImpactAnalysisView.affectedProducts",
        "PolicySimulationConflictImpactAnalysisView.affectedVenues"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Time”, “Occupancy”, “Credential Active”, “Gold Membership”, “VIP Lounge Access”, “Capacity Restriction”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 144 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run simulation",
       "provenance": "contract operation simulatePolicyConflictImpact"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The policy simulation conflict list.",
   "error": "Could not load. Names which read failed and leaves the policy simulation conflict untouched.",
   "emptyFirstRun": "No policy simulation conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the policy simulation conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulatePolicyConflictImpact",
    "contract": "access",
    "purpose": "Policy Simulation, Conflict & Impact Analysis",
    "trigger": "onAction",
    "invalidates": [
     "simulatePolicyConflictImpact"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PolicySimulationConflictImpactAnalysisView.policiesInvolved",
    "PolicySimulationConflictImpactAnalysisView.hierarchy",
    "PolicySimulationConflictImpactAnalysisView.priority",
    "PolicySimulationConflictImpactAnalysisView.resultingDecision",
    "PolicySimulationConflictImpactAnalysisView.affectedProducts",
    "PolicySimulationConflictImpactAnalysisView.affectedVenues"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-242"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 144. 6 of 6 labels bound to a contract property; 6 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-243",
  "name": "Policy Approval, Audit, Analytics & AI Optimization",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "10",
   "number": "10.10",
   "page": 146
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/policy-approval-audit-analytics-ai-optimization-bo-243",
   "component": "apps/venue-management-web/src/routes/access-venue/PolicyApprovalAuditAnalyticsAiOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-234"
   ],
   "exitTo": [
    "BO-234"
   ],
   "inferred": false,
   "notes": "**Reached from BO-234, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor; Measure) and no metric row",
  "purpose": "Govern the complete policy lifecycle and continuously measure policy effectiveness.",
  "purposeNote": "Dynamic access policies are versioned, approved, measurable, auditable and continuously optimizable. Board 10 — Final 10-Screen Structure # Backend Screen Main Responsibility 10.1 Dynamic Access Policy Command Center Policy estate and health 10.2 Access Attribute Catalog Govern reusable decision attributes 10.3 Visual Dynamic Policy Builder Build ABAC policies without code 10.4 Context, Time, Event & Capacity Policy Builder Context-aware operational policies 10.5 Identity, Membership & Accreditation Policies Identity-based authorization 10.6 Policy Scope, Hierarchy & Inheritance Multi-venue po",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Policy Owner, Business Approval, Security Approval, Technical Approval, ROLLBACK TO V3.4. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Access Control Module_Reference.pdf, page 146 §Support"
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
       "label": "Every policy approval audit",
       "columns": [
        "→",
        "Denial Rate",
        "Override Rate",
        "False-Positive Indicators",
        "Operator Review Rate",
        "Guest Impact",
        "Security Incidents"
       ],
       "bindsTo": "Policy",
       "operation": "listPolicies",
       "provenance": "pack Access Control Module_Reference.pdf, page 146 §Monitor"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected policy approval audit",
       "bindsTo": "Policy",
       "columns": [
        "→",
        "Denial Rate",
        "Override Rate",
        "False-Positive Indicators",
        "Operator Review Rate",
        "Guest Impact",
        "Security Incidents"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Draft”, “Test”, “Impact Analysis”, “Approval”, “Schedule”, “Publish”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 146 §Monitor"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Policy Owner",
       "provenance": "pack Access Control Module_Reference.pdf, page 146 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Business Approval",
       "provenance": "pack Access Control Module_Reference.pdf, page 146 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Security Approval",
       "provenance": "pack Access Control Module_Reference.pdf, page 146 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Technical Approval",
       "provenance": "pack Access Control Module_Reference.pdf, page 146 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "ROLLBACK TO V3.4",
       "provenance": "pack Access Control Module_Reference.pdf, page 146 §Allow"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRollbackToV",
    "component": "confirmDialog",
    "trigger": "ROLLBACK TO V3.4",
    "body": "**ROLLBACK TO V3.4 on a policy approval audit is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Access Control Module_Reference.pdf, page 146 §Allow"
   }
  ],
  "states": {
   "loading": "The policy approval audit list.",
   "error": "Could not load. Names which read failed and leaves the policy approval audit untouched.",
   "emptyFirstRun": "No policy approval audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the policy approval audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPolicies",
    "contract": "white-label",
    "purpose": "List legal policies",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "→",
    "Denial Rate",
    "Override Rate",
    "False-Positive Indicators",
    "Operator Review Rate",
    "Guest Impact"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-243"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 146. 0 of 7 labels bound to a contract property; 12 of 89 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listAccessAttributeCatalog": {
  "method": "GET",
  "path": "/access-attribute-catalog",
  "contract": "access",
  "summary": "Access Attribute Catalog",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessAttributeCatalogView"
 },
 "listAuthorizationGovernanceTemporary": {
  "method": "GET",
  "path": "/authorization-governance-temporary",
  "contract": "access",
  "summary": "Authorization Governance & Temporary Access",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AuthorizationGovernanceTemporaryAccessView"
 },
 "listDynamicAccessPolicy": {
  "method": "GET",
  "path": "/dynamic-access-policy",
  "contract": "access",
  "summary": "Dynamic Access Policy Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicAccessPolicyCommandCenterView"
 },
 "listIdentityMembershipAccreditation": {
  "method": "GET",
  "path": "/identity-membership-accreditation",
  "contract": "access",
  "summary": "Identity, Membership & Accreditation Policies",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "IdentityMembershipAccreditationPoliciesView"
 },
 "listPolicies": {
  "method": "GET",
  "path": "/tenant-config/policies",
  "contract": "white-label",
  "summary": "List legal policies",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Policy"
 },
 "listPolicyEvaluationArchitecture": {
  "method": "GET",
  "path": "/policy-evaluation-architecture",
  "contract": "access",
  "summary": "Policy Evaluation Architecture & Offline Distribution",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PolicyEvaluationArchitectureOfflineDistributionView"
 },
 "listPolicyScopeHierarchy": {
  "method": "GET",
  "path": "/policy-scope-hierarchy",
  "contract": "access",
  "summary": "Policy Scope, Hierarchy & Inheritance",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PolicyScopeHierarchyInheritanceView"
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
  "parameters": [],
  "requestBody": "ContextTimeEventCapacityPolicyBuilderInput",
  "responds": "ContextTimeEventCapacityPolicyBuilderView"
 },
 "setVisualDynamicPolicy": {
  "method": "PUT",
  "path": "/visual-dynamic-policy",
  "contract": "access",
  "summary": "Visual Dynamic Policy Builder",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "VisualDynamicPolicyBuilderInput",
  "responds": "VisualDynamicPolicyBuilderView"
 },
 "simulatePolicyConflictImpact": {
  "method": "PUT",
  "path": "/policy-conflict-impact",
  "contract": "access",
  "summary": "Policy Simulation, Conflict & Impact Analysis",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PolicySimulationConflictImpactAnalysisInput",
  "responds": "PolicySimulationConflictImpactAnalysisView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessAttributeCatalogView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Attribute Catalog displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "age": {
    "type": "string",
    "description": "Age"
   },
   "genderWhereLegallyBusinessPermitted": {
    "type": "string",
    "description": "Gender where legally/business permitted"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "guestCategory": {
    "type": "string",
    "description": "Guest Category"
   },
   "countryResidencyWhereApplicable": {
    "type": "string",
    "description": "Country/Residency where applicable"
   },
   "groupType": {
    "type": "string",
    "description": "Group Type"
   },
   "companionRelationship": {
    "type": "string",
    "description": "Companion Relationship"
   },
   "podStatus": {
    "type": "string",
    "description": "POD status"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "credentialStatus": {
    "type": "string",
    "description": "Credential Status"
   },
   "mediaType": {
    "type": "string",
    "description": "Media Type"
   },
   "verificationMethod": {
    "type": "string",
    "description": "Verification Method"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "accreditation": {
    "type": "string",
    "description": "Accreditation"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty Tier"
   },
   "employee": {
    "type": "string",
    "description": "Employee"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "jobFunction": {
    "type": "string",
    "description": "Job Function"
   },
   "shift": {
    "type": "string",
    "description": "Shift"
   },
   "securityClearance": {
    "type": "string",
    "description": "Security Clearance"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "resource": {
    "type": "string",
    "description": "Resource"
   },
   "restrictedArea": {
    "type": "string",
    "description": "Restricted Area"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "day": {
    "type": "string",
    "description": "Day"
   },
   "season": {
    "type": "string",
    "description": "Season"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "operatingCalendar": {
    "type": "string",
    "description": "Operating Calendar"
   },
   "specialDay": {
    "type": "string",
    "description": "Special Day"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy"
   }
  }
 },
 "AuthorizationGovernanceTemporaryAccessView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Authorization Governance & Temporary Access displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "leastPrivilege": {
    "type": "string",
    "description": "Least Privilege"
   },
   "segregationOfDuties": {
    "type": "string",
    "description": "Segregation of Duties"
   },
   "temporaryAccess": {
    "type": "string",
    "description": "Temporary Access"
   },
   "expiringGrants": {
    "type": "string",
    "description": "Expiring Grants"
   },
   "delegatedAdministration": {
    "type": "string",
    "description": "Delegated Administration"
   },
   "approvalRequirements": {
    "type": "string",
    "description": "Approval Requirements"
   },
   "at": {
    "type": "string",
    "description": "At"
   },
   "cannot": {
    "type": "string",
    "description": "cannot"
   },
   "resortGlobalSecurityPolicy": {
    "type": "string",
    "description": "✕ Resort Global Security Policy"
   },
   "adventureParkPolicies": {
    "type": "string",
    "description": "✕ Adventure Park Policies"
   },
   "with": {
    "type": "string",
    "description": "with"
   },
   "scope": {
    "type": "string",
    "description": "scope"
   },
   "duration": {
    "type": "string",
    "format": "date-time",
    "description": "duration"
   },
   "reason": {
    "type": "string",
    "description": "reason"
   },
   "approver": {
    "type": "string",
    "description": "approver"
   },
   "fullAudit": {
    "type": "string",
    "description": "full audit"
   }
  }
 },
 "ContextTimeEventCapacityPolicyBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Context, Time, Event & Capacity Policy Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "day": {
    "type": "string",
    "description": "Day"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "season": {
    "type": "string",
    "description": "Season"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "specialEvent": {
    "type": "string",
    "description": "Special Event"
   },
   "holiday": {
    "type": "string",
    "description": "Holiday"
   },
   "operatingCalendar": {
    "type": "string",
    "description": "Operating Calendar"
   },
   "mayEnterSpecifiedZones": {
    "type": "string",
    "description": "may enter specified zones"
   }
  }
 },
 "ContextTimeEventCapacityPolicyBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Context, Time, Event & Capacity Policy Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "day": {
    "type": "string",
    "description": "Day"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "season": {
    "type": "string",
    "description": "Season"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "specialEvent": {
    "type": "string",
    "description": "Special Event"
   },
   "holiday": {
    "type": "string",
    "description": "Holiday"
   },
   "operatingCalendar": {
    "type": "string",
    "description": "Operating Calendar"
   },
   "mayEnterSpecifiedZones": {
    "type": "string",
    "description": "may enter specified zones"
   },
   "normal": {
    "type": "string",
    "description": "NORMAL (the pack shows 80–89%)"
   },
   "monitor": {
    "type": "string",
    "description": "MONITOR (the pack shows 90–94%)"
   },
   "restrict": {
    "type": "string",
    "description": "RESTRICT (the pack shows 95%+)"
   }
  }
 },
 "DynamicAccessPolicyCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Access Policy Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activePolicies": {
    "type": "integer",
    "description": "Active Policies"
   },
   "draftPolicies": {
    "type": "integer",
    "description": "Draft Policies"
   },
   "policiesPendingApproval": {
    "type": "string",
    "description": "Policies Pending Approval"
   },
   "policiesTriggeredToday": {
    "type": "string",
    "description": "Policies Triggered Today"
   },
   "allowDecisions": {
    "type": "boolean",
    "description": "Allow Decisions"
   },
   "denyDecisions": {
    "type": "integer",
    "description": "Deny Decisions"
   },
   "policyConflicts": {
    "type": "integer",
    "description": "Policy Conflicts"
   },
   "expiringPolicies": {
    "type": "integer",
    "description": "Expiring Policies"
   },
   "aiRecommendations": {
    "type": "integer",
    "description": "AI Recommendations"
   }
  }
 },
 "IdentityMembershipAccreditationPoliciesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Identity, Membership & Accreditation Policies displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guest": {
    "type": "string",
    "description": "Guest"
   },
   "member": {
    "type": "string",
    "description": "Member"
   },
   "annualPassHolder": {
    "type": "string",
    "description": "Annual Pass Holder"
   },
   "employee": {
    "type": "string",
    "description": "Employee"
   },
   "contractor": {
    "type": "string",
    "description": "Contractor"
   },
   "vendor": {
    "type": "string",
    "description": "Vendor"
   },
   "performer": {
    "type": "string",
    "description": "Performer"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "vip": {
    "type": "string",
    "description": "VIP"
   },
   "security": {
    "type": "string",
    "description": "Security"
   },
   "emergencyServices": {
    "type": "string",
    "description": "Emergency Services"
   },
   "eventStaff": {
    "type": "string",
    "description": "Event Staff"
   },
   "priorityEntrance": {
    "type": "string",
    "description": "✓ Priority Entrance"
   },
   "memberLounge": {
    "type": "string",
    "description": "✓ Member Lounge"
   },
   "selectedAttractions": {
    "type": "string",
    "description": "✓ Selected Attractions"
   },
   "productionZone": {
    "type": "string",
    "description": "✓ Production Zone"
   },
   "backstage": {
    "type": "string",
    "description": "✓ Backstage"
   },
   "staffEntrance": {
    "type": "string",
    "description": "✓ Staff Entrance"
   },
   "vipHospitality": {
    "type": "string",
    "description": "✕ VIP Hospitality"
   },
   "financeOffice": {
    "type": "string",
    "description": "✕ Finance Office"
   },
   "until": {
    "type": "string",
    "format": "date-time",
    "description": "until"
   },
   "automaticallyExpiresAfterward": {
    "type": "string",
    "format": "date-time",
    "description": "Automatically expires afterward"
   }
  }
 },
 "LocalisedRichText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "description": "Keyed by language code. Values are sanitised HTML.",
  "additionalProperties": {
   "type": "string"
  }
 },
 "Policy": {
  "x-ticvai-persistence": "whitelabel.policy",
  "type": "object",
  "required": [
   "kind",
   "version",
   "body",
   "effectiveFrom",
   "publishedAt"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/PolicyKind"
   },
   "version": {
    "type": "string",
    "description": "Immutable. A guest who consented to version 3 consented to version 3, and a policy that changes under a recorded consent is a compliance failure.\n"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedRichText"
   },
   "requiresReconsent": {
    "type": "boolean"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "PolicyEvaluationArchitectureOfflineDistributionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Policy Evaluation Architecture & Offline Distribution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "evaluatedAtVenueEdge": {
    "type": "string",
    "description": "Evaluated at venue edge"
   },
   "evaluatedLocallyWhereSupported": {
    "type": "string",
    "description": "Evaluated locally where supported"
   },
   "centralUnavailable": {
    "type": "string",
    "description": "Central unavailable"
   }
  }
 },
 "PolicyKind": {
  "type": "string",
  "enum": [
   "privacy",
   "termsAndConditions",
   "refund",
   "cookie",
   "accessibility"
  ]
 },
 "PolicyScopeHierarchyInheritanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Policy Scope, Hierarchy & Inheritance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "appliesTo": {
    "type": "string",
    "description": "applies to"
   },
   "appliesOnly": {
    "type": "string",
    "description": "applies only"
   },
   "applies": {
    "type": "string",
    "description": "applies"
   },
   "highestPriorityWins": {
    "type": "string",
    "description": "Highest Priority Wins"
   },
   "denyOverridesAllow": {
    "type": "string",
    "description": "Deny Overrides Allow"
   },
   "mostSpecificWins": {
    "type": "string",
    "description": "Most Specific Wins"
   },
   "mandatoryParentWins": {
    "type": "string",
    "description": "Mandatory Parent Wins"
   },
   "explicitResolution": {
    "type": "string",
    "description": "Explicit Resolution"
   }
  }
 },
 "PolicySimulationConflictImpactAnalysisInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Policy Simulation, Conflict & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "pass": {
    "type": "string",
    "description": "✓ PASS"
   },
   "accessAllowed": {
    "type": "boolean",
    "description": "🟢 ACCESS ALLOWED"
   },
   "goldMembersAllow": {
    "type": "string",
    "description": "Gold Members → Allow"
   }
  }
 },
 "PolicySimulationConflictImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Policy Simulation, Conflict & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "occupancy": {
    "type": "integer",
    "description": "Occupancy (the pack shows 82%)"
   },
   "pass": {
    "type": "string",
    "description": "✓ PASS"
   },
   "accessAllowed": {
    "type": "boolean",
    "description": "🟢 ACCESS ALLOWED"
   },
   "goldMembersAllow": {
    "type": "string",
    "description": "Gold Members → Allow"
   },
   "policiesInvolved": {
    "type": "string",
    "description": "policies involved"
   },
   "hierarchy": {
    "type": "string",
    "description": "hierarchy"
   },
   "priority": {
    "type": "string",
    "description": "priority"
   },
   "resultingDecision": {
    "type": "string",
    "description": "resulting decision"
   },
   "affectedProducts": {
    "type": "integer",
    "description": "affected products"
   },
   "affectedVenues": {
    "type": "integer",
    "description": "affected venues"
   },
   "estimatedGuestsImpacted": {
    "type": "string",
    "description": "estimated guests impacted"
   }
  }
 },
 "VisualDynamicPolicyBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Visual Dynamic Policy Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "allow": {
    "type": "string",
    "description": "🟢 ALLOW"
   },
   "deny": {
    "type": "string",
    "description": "🔴 DENY"
   },
   "review": {
    "type": "string",
    "description": "🟡 REVIEW"
   },
   "requireId": {
    "type": "string",
    "description": "🟡 REQUIRE ID"
   },
   "requireBiometric": {
    "type": "string",
    "description": "🟡 REQUIRE BIOMETRIC"
   },
   "requireCompanion": {
    "type": "string",
    "description": "🟡 REQUIRE COMPANION"
   },
   "requireSupervisor": {
    "type": "string",
    "description": "🟡 REQUIRE SUPERVISOR"
   }
  }
 },
 "VisualDynamicPolicyBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Visual Dynamic Policy Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "allow": {
    "type": "string",
    "description": "🟢 ALLOW"
   },
   "deny": {
    "type": "string",
    "description": "🔴 DENY"
   },
   "review": {
    "type": "string",
    "description": "🟡 REVIEW"
   },
   "requireId": {
    "type": "string",
    "description": "🟡 REQUIRE ID"
   },
   "requireBiometric": {
    "type": "string",
    "description": "🟡 REQUIRE BIOMETRIC"
   },
   "requireCompanion": {
    "type": "string",
    "description": "🟡 REQUIRE COMPANION"
   },
   "requireSupervisor": {
    "type": "string",
    "description": "🟡 REQUIRE SUPERVISOR"
   }
  }
 }
}
```
