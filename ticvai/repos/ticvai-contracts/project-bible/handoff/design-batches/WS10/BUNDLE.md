# WS10 — Access Control board 10

**10 screens · 18 operations · 27 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `ACCESS_POINT_CONFIGURE, ACCREDITATION_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-234` | Dynamic Access Policy Command Center | listDetail | 2 | 0 | — |
| `BO-235` | Access Attribute Catalog | listDetail | 2 | 0 | — |
| `BO-236` | Visual Dynamic Policy Builder | listDetail | 1 | 0 | — |
| `BO-237` | Context, Time, Event & Capacity Policy Builder | commandCentre | 1 | 0 | — |
| `BO-238` | Identity, Membership & Accreditation Policies | listDetail | 3 | 0 | — |
| `BO-239` | Policy Scope, Hierarchy & Inheritance | configEditor | 2 | 0 | — |
| `BO-240` | Authorization Governance & Temporary Access | listDetail | 1 | 0 | — |
| `BO-241` | Policy Evaluation Architecture & Offline Distribution | listDetail | 3 | 0 | — |
| `BO-242` | Policy Simulation, Conflict & Impact Analysis | listDetail | 1 | 0 | — |
| `BO-243` | Policy Approval, Audit, Analytics & AI Optimization | listDetail | 5 | 1 | — |

## Thin screens in this batch

**BO-235, BO-236, BO-237, BO-238, BO-240, BO-241, BO-242 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — BO-100 declares entryState.params  and BO-234 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
     "operation": "listDynamicAccessPolicy",
     "carries": [
      "policyId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can centrally understand the status, scope, performance and conflicts of all dynamic access policies.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide central governance and visibility over all dynamic access policies.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Policies",
       "bindsTo": "DynamicAccessPolicyCommandCenterViewSummary.activePolicies",
       "operation": "listDynamicAccessPolicy",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Draft Policies",
       "bindsTo": "DynamicAccessPolicyCommandCenterViewSummary.draftPolicies",
       "operation": "listDynamicAccessPolicy",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Policies Pending Approval",
       "bindsTo": "DynamicAccessPolicyCommandCenterViewSummary.policiesPendingApproval",
       "operation": "listDynamicAccessPolicy",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Policies Triggered Today",
       "bindsTo": "DynamicAccessPolicyCommandCenterViewSummary.policiesTriggeredToday",
       "operation": "listDynamicAccessPolicy",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Allow Decisions",
       "bindsTo": "DynamicAccessPolicyCommandCenterViewSummary.allowDecisions",
       "operation": "listDynamicAccessPolicy",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Deny Decisions",
       "bindsTo": "DynamicAccessPolicyCommandCenterViewSummary.denyDecisions",
       "operation": "listDynamicAccessPolicy",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Policy Conflicts",
       "bindsTo": "DynamicAccessPolicyCommandCenterViewSummary.policyConflicts",
       "operation": "listDynamicAccessPolicy",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Policies",
       "bindsTo": "DynamicAccessPolicyCommandCenterViewSummary.expiringPolicies",
       "operation": "listDynamicAccessPolicy",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "AI Recommendations",
       "bindsTo": "DynamicAccessPolicyCommandCenterViewSummary.aiRecommendations",
       "operation": "listDynamicAccessPolicy",
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
       "label": "Every dynamic access policy",
       "columns": [
        "Review Decisions"
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
        "Review Decisions"
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
   },
   {
    "operationId": "setVisualDynamicPolicy",
    "contract": "access",
    "purpose": "Create or change a dynamic access policy from the command centre",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listDynamicAccessPolicy"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "DynamicAccessPolicyCommandCenterViewSummary.activePolicies",
    "DynamicAccessPolicyCommandCenterViewSummary.draftPolicies",
    "DynamicAccessPolicyCommandCenterViewSummary.policiesPendingApproval",
    "DynamicAccessPolicyCommandCenterViewSummary.policiesTriggeredToday",
    "DynamicAccessPolicyCommandCenterViewSummary.allowDecisions",
    "DynamicAccessPolicyCommandCenterViewSummary.denyDecisions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-234",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-234"
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
  "purposeNote": "Policy designers use governed attributes rather than manually creating inconsistent fields in individual policies.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the attributes available to the TICVAI policy engine. This becomes the reusable data dictionary for dynamic access decisions.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save attribute",
       "operation": "setAccessAttributeCatalog",
       "provenance": "contract access.yaml PUT /access-attribute-catalog (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setAccessAttributeCatalog",
    "contract": "access",
    "purpose": "Save attribute",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-235",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-235"
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
  "purposeNote": "Business administrators can create sophisticated contextual access policies without development work.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a no-code interface for constructing contextual access policies.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-236",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-236"
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
  "purposeNote": "Access behavior can dynamically respond to operating calendars, events, capacity, occupancy and venue status.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§MONITOR) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Configure policies driven by changing venue conditions rather than only guest attributes.",
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
       "label": "Event",
       "provenance": "pack Access Control Module_Reference.pdf, page 137 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Special Event",
       "provenance": "pack Access Control Module_Reference.pdf, page 137 §Support"
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-237",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-237"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 137. 0 of 0 labels bound to a contract property; 3 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Special Event are choices sent by `setContextTimeEvent`.",
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
  "purposeNote": "Memberships, staff identities and accreditations can participate directly in access-policy decisions.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure policies based on who the requesting person is.",
  "gaps": [
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
   },
   {
    "operationId": "setVisualDynamicPolicy",
    "contract": "access",
    "purpose": "Save a policy whose conditions are identity, membership or accreditation attributes",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listIdentityMembershipAccreditation"
    ]
   },
   {
    "operationId": "setAccessProfile",
    "contract": "accreditation",
    "purpose": "Map an accreditation category to the zones it opens",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "preloaded": [
    "IdentityMembershipAccreditationPoliciesView.identityType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-238",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-238"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 139. 0 of 0 labels bound to a contract property; 2 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Guest, Security are choices sent by `setVisualDynamicPolicy` (identity categories the policy condition tests).",
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
  "purposeNote": "Policies behave predictably across tenants, venues and access hierarchies.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrator defines) and no display directory — it is settings, not a population",
  "purpose": "Govern how policies apply across TICVAI's multi-tenant and multi-venue architecture.",
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save scope placement",
       "operation": "setPolicyScopeHierarchy",
       "provenance": "contract access.yaml PUT /policy-scope-hierarchy (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setPolicyScopeHierarchy",
    "contract": "access",
    "purpose": "Save scope placement",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-239",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-239"
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
  "purposeNote": "Privileged and temporary access follows controlled authorization rather than informal manual permissions.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Apply enterprise governance principles to privileged and temporary access.",
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
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Temporary Access",
       "provenance": "pack Access Control Module_Reference.pdf, page 142 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Expiring Grants",
       "provenance": "pack Access Control Module_Reference.pdf, page 142 §Support"
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
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-240",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-240"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 142. 0 of 0 labels bound to a contract property; 2 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Expiring Grants are choices sent by `listAuthorizationGovernanceTemporary`.",
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
  "purposeNote": "Every policy has a defined evaluation location and predictable behavior when connectivity or data sources are unavailable.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define where and how policies are evaluated. This screen connects Board 10 with the offline/edge architecture already configured in Board 7.",
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setEdgeNodeLocal",
       "label": "Save edge node local",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setEdgeNodeLocal"
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
   },
   {
    "operationId": "setEdgeNodeLocal",
    "contract": "access",
    "purpose": "Save where a policy is evaluated at the edge",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listPolicyEvaluationArchitecture"
    ]
   },
   {
    "operationId": "setOfflinePolicy",
    "contract": "tenancy",
    "purpose": "Save what the edge may decide while central services are unreachable",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-241",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-241"
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
  "purposeNote": "No policy reaches production without visibility into conflicts and potential operational impact.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Test policies before they affect live guest admission.",
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
    "trigger": "onAction"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-242",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-242"
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
  "purposeNote": "Dynamic access policies are versioned, approved, measurable, auditable and continuously optimizable. Board 10 — Final 10-Screen Structure # Backend Screen Main Responsibility 10.1 Dynamic Access Policy Command Center Policy estate and health 10.2 Access Attribute Catalog Govern reusable decision attributes 10.3 Visual Dynamic Policy Builder Build ABAC policies without code 10.4 Context, Time, Event & Capacity Policy Builder Context-aware operational policies 10.5 Identity, Membership & Accreditation Policies Identity-based authorization 10.6 Policy Scope, Hierarchy & Inheritance Multi-venue po",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor; Measure) and no metric row",
  "purpose": "Govern the complete policy lifecycle and continuously measure policy effectiveness.",
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
       "operation": "rollbackAccessPolicy",
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
   },
   {
    "operationId": "listDynamicAccessPolicy",
    "contract": "access",
    "purpose": "The access policies awaiting approval, with their versions",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "createApprovalRequest",
    "contract": "approvals",
    "purpose": "Send a policy version for business, security and technical approval",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Approve or reject a policy version",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "rollbackAccessPolicy",
    "contract": "access",
    "purpose": "Roll back policy",
    "trigger": "onAction"
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
   ],
   "params": [
    {
     "name": "policyId",
     "from": "navigation"
    },
    {
     "name": "requestId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-243",
   "workshopBoard": "wireframes/WS27 Access Control Board 10.dc.html#bo-243"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 146. 0 of 7 labels bound to a contract property; 12 of 89 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Policy Owner, Business Approval, Security Approval, Technical Approval: `decideApprovalRequest`; still owed by a contract change: `rollbackAccessPolicy`.",
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
 "createApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Raise a request",
  "permission": "APPROVAL_REQUEST",
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
  "requestBody": "CreateApprovalRequest",
  "responds": "ApprovalRequest"
 },
 "decideApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/decide",
  "contract": "approvals",
  "summary": "Approve, reject, return or ask for information",
  "permission": "APPROVAL_DECIDE",
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
  "responds": "ApprovalRequest"
 },
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
 "listDynamicAccessPolicy": {
  "method": "GET",
  "path": "/dynamic-access-policy",
  "contract": "access",
  "summary": "Dynamic Access Policy Command Center",
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
  "parameters": [
   {
    "name": "includeHistory",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   }
  ],
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
 "rollbackAccessPolicy": {
  "method": "POST",
  "path": "/dynamic-access-policy/{policyId}/rollback",
  "contract": "access",
  "summary": "Put a previous policy version back",
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
  "responds": "DynamicAccessPolicyCommandCenterView"
 },
 "setAccessAttributeCatalog": {
  "method": "PUT",
  "path": "/access-attribute-catalog",
  "contract": "access",
  "summary": "Add or amend an access attribute",
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
  "requestBody": "AccessAttributeCatalogInput",
  "responds": "AccessAttributeCatalogView"
 },
 "setAccessProfile": {
  "method": "PUT",
  "path": "/accreditation-access-profiles",
  "contract": "accreditation",
  "summary": "Define which zones, on which dates, at which times",
  "permission": "ACCREDITATION_CONFIGURE",
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
  "requestBody": "AccessProfile",
  "responds": "AccessProfile"
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
 "setEdgeNodeLocal": {
  "method": "PUT",
  "path": "/edge-node-local",
  "contract": "access",
  "summary": "Edge Node & Local Processing Configuration",
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
  "requestBody": "EdgeNodeLocalProcessingConfigurationInput",
  "responds": "EdgeNodeLocalProcessingConfigurationView"
 },
 "setOfflinePolicy": {
  "method": "PUT",
  "path": "/offline-policy",
  "contract": "tenancy",
  "summary": "What a workstation may do with no network, and for how long",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "OfflinePolicy",
  "responds": "OfflinePolicy"
 },
 "setPolicyScopeHierarchy": {
  "method": "PUT",
  "path": "/policy-scope-hierarchy",
  "contract": "access",
  "summary": "Place a policy in the scope hierarchy",
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
  "requestBody": "PolicyScopeHierarchyInheritanceInput",
  "responds": "PolicyScopeHierarchyInheritanceView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PolicySimulationConflictImpactAnalysisInput",
  "responds": "PolicySimulationConflictImpactAnalysisView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessAttributeCatalogInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Access Attribute Catalog submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "attributeKey",
   "category",
   "label",
   "dataType"
  ],
  "properties": {
   "attributeKey": {
    "type": "string",
    "pattern": "^[a-z][a-zA-Z0-9]*(\\.[a-z][a-zA-Z0-9]*)*$",
    "maxLength": 100,
    "description": "Stable key a policy condition names, e.g. guest.tier. Unique within the tenant"
   },
   "category": {
    "type": "string",
    "enum": [
     "guest",
     "credential",
     "employee",
     "location",
     "time",
     "operational",
     "device",
     "risk"
    ]
   },
   "label": {
    "type": "string",
    "maxLength": 200
   },
   "dataType": {
    "type": "string",
    "enum": [
     "string",
     "integer",
     "number",
     "boolean",
     "date",
     "dateTime",
     "enum"
    ]
   },
   "allowedValues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Required when dataType is enum"
   },
   "enabled": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "AccessAttributeCatalogView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Attribute Catalog displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "category": {
    "type": "string",
    "enum": [
     "guest",
     "credential",
     "employee",
     "location",
     "time",
     "operational",
     "device",
     "risk"
    ]
   },
   "attributeKey": {
    "type": "string",
    "description": "Dotted governed key, e.g. membership.tier"
   },
   "label": {
    "type": "string"
   },
   "dataType": {
    "type": "string",
    "enum": [
     "string",
     "integer",
     "number",
     "boolean",
     "date",
     "dateTime",
     "enum"
    ]
   },
   "allowedValues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "For enum attributes, e.g. Standard, Silver, Gold, Platinum"
   },
   "enabled": {
    "type": "boolean",
    "description": "Whether the venue may use this attribute in policies (e.g. gender or residency only where legally and business permitted)"
   }
  },
  "required": [
   "attributeKey",
   "category"
  ]
 },
 "AccessProfile": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.access_profile",
  "description": "Board 5.2. **How an estate stays governable.**",
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
   "zoneIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "operationalAreas": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "schedule": {
    "type": "array",
    "description": "**Zone, date and time are three dimensions and all three are needed.**",
    "items": {
     "type": "object",
     "properties": {
      "zoneId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "dateFrom": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "dateTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "from": {
       "type": "string",
       "nullable": true
      },
      "to": {
       "type": "string",
       "nullable": true
      },
      "eventPhase": {
       "type": "string",
       "nullable": true,
       "enum": [
        "build",
        "rehearsal",
        "doorsOpen",
        "liveShow",
        "breakdown"
       ]
      }
     }
    }
   },
   "escortRequired": {
    "type": "boolean",
    "default": false
   },
   "holderCount": {
    "type": "integer",
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ApprovalDecision": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision",
  "required": [
   "level",
   "principalId",
   "decision",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "level": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "isDelegate": {
    "type": "boolean"
   },
   "delegatedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject"
    ]
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "usedMfa": {
    "type": "boolean"
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration",
   "productChange",
   "pricingChange"
  ]
 },
 "ApprovalMode": {
  "type": "string",
  "description": "11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n",
  "enum": [
   "sequential",
   "parallel",
   "consensus",
   "majority"
  ]
 },
 "ApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "approvals.request",
  "required": [
   "id",
   "kind",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "rerouteOnNoApprover": {
    "type": "boolean",
    "default": true,
    "description": "BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"
   },
   "outOfOfficeDelegateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "allowEmailApproval": {
    "type": "boolean",
    "default": false,
    "description": "**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"
   },
   "reopenedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ApprovalStatus"
   },
   "subjectContract": {
    "type": "string"
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "matrixVersion": {
    "type": "integer"
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "currentLevel": {
    "type": "integer"
   },
   "totalLevels": {
    "type": "integer"
   },
   "pendingApprovers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "isDelegate": {
       "type": "boolean"
      }
     }
    }
   },
   "decisions": {
    "type": "array",
    "description": "Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n",
    "items": {
     "$ref": "#/components/schemas/ApprovalDecision"
    }
   },
   "escalations": {
    "type": "array",
    "description": "11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "fromLevel": {
       "type": "integer"
      },
      "toLevel": {
       "type": "integer"
      },
      "wasAutomatic": {
       "type": "boolean"
      }
     }
    }
   },
   "resubmittedFromId": {
    "type": "string",
    "nullable": true
   },
   "reopenedFromId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "returned",
   "informationRequested",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
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
 "CreateApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "kind",
   "subjectContract",
   "subjectType",
   "subjectId",
   "scopePath",
   "summary"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "subjectContract": {
    "type": "string",
    "description": "Which contract owns the thing being approved."
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "description": "**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string",
    "maxLength": 300,
    "description": "What the approver sees in their queue before opening it."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true
   },
   "justification": {
    "type": "string",
    "maxLength": 1000
   },
   "isDraft": {
    "type": "boolean",
    "default": false,
    "description": "True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"
   }
  }
 },
 "DynamicAccessPolicyCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Access Policy Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "version": {
    "type": "integer",
    "minimum": 1,
    "description": "Current version. `rollbackAccessPolicy` restores an earlier one as a new version (decided 29 September, VM close-out)"
   },
   "policyId": {
    "type": "string"
   },
   "policyName": {
    "type": "string",
    "description": "e.g. VIP Backstage Event"
   },
   "scope": {
    "type": "string",
    "description": "Where the policy applies, e.g. a venue, park or all venues"
   },
   "policyType": {
    "type": "string",
    "enum": [
     "guestAttribute",
     "accreditation",
     "occupancy",
     "employee",
     "risk",
     "membership",
     "timeEvent"
    ]
   },
   "priority": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "inactive",
     "expired"
    ]
   }
  },
  "required": [
   "policyId"
  ]
 },
 "EdgeNodeLocalProcessingConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Edge Node & Local Processing Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "nodeType": {
    "type": "string",
    "enum": [
     "venueEdgeNode",
     "gateController",
     "turnstileLocalEngine",
     "handheldLocalEngine"
    ],
    "description": "Which edge component makes local access decisions"
   },
   "edgeNodeId": {
    "type": "string",
    "description": "Edge Node ID"
   },
   "tenantId": {
    "type": "string",
    "description": "Tenant"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "network": {
    "type": "string",
    "description": "Network"
   },
   "deviceGroup": {
    "type": "string",
    "description": "Device Group"
   },
   "processingMode": {
    "type": "string",
    "description": "Processing Mode"
   },
   "storageAllocation": {
    "type": "string",
    "description": "Storage allocation"
   },
   "redundancy": {
    "type": "string",
    "description": "redundancy"
   },
   "lastHeartbeat": {
    "type": "string",
    "format": "date-time",
    "description": "Last heartbeat, set by the node, read only"
   },
   "softwareVersion": {
    "type": "string",
    "description": "software version"
   },
   "securityStatus": {
    "type": "string",
    "description": "security status"
   }
  },
  "required": [
   "edgeNodeId",
   "venueId",
   "nodeType"
  ]
 },
 "EdgeNodeLocalProcessingConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Edge Node & Local Processing Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "nodeType": {
    "type": "string",
    "enum": [
     "venueEdgeNode",
     "gateController",
     "turnstileLocalEngine",
     "handheldLocalEngine"
    ],
    "description": "Which edge component makes local access decisions"
   },
   "edgeNodeId": {
    "type": "string",
    "description": "Edge Node ID"
   },
   "tenantId": {
    "type": "string",
    "description": "Tenant"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "network": {
    "type": "string",
    "description": "Network"
   },
   "deviceGroup": {
    "type": "string",
    "description": "Device Group"
   },
   "processingMode": {
    "type": "string",
    "description": "Processing Mode"
   },
   "storageAllocation": {
    "type": "string",
    "description": "Storage allocation"
   },
   "redundancy": {
    "type": "string",
    "description": "redundancy"
   },
   "lastHeartbeat": {
    "type": "string",
    "format": "date-time",
    "description": "Last heartbeat, set by the node, read only"
   },
   "softwareVersion": {
    "type": "string",
    "description": "software version"
   },
   "securityStatus": {
    "type": "string",
    "description": "security status"
   }
  },
  "required": [
   "edgeNodeId",
   "venueId",
   "nodeType"
  ]
 },
 "IdentityMembershipAccreditationPoliciesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Identity, Membership & Accreditation Policies displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "policyId": {
    "type": "string"
   },
   "identityType": {
    "type": "string",
    "enum": [
     "guest",
     "member",
     "annualPassHolder",
     "employee",
     "contractor",
     "vendor",
     "performer",
     "media",
     "vip",
     "security",
     "emergencyServices",
     "eventStaff"
    ],
    "description": "Who the requesting person is"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "until"
   },
   "name": {
    "type": "string",
    "description": "e.g. Event Crew, Level 3"
   },
   "allowedZones": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "deniedZones": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "conditionExpression": {
    "type": "string",
    "description": "e.g. Employee Status = Active AND Current Shift = Active"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   }
  },
  "required": [
   "policyId",
   "identityType"
  ]
 },
 "LocalisedRichText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "description": "Keyed by language code. Values are sanitised HTML.",
  "additionalProperties": {
   "type": "string"
  }
 },
 "OfflinePolicy": {
  "type": "object",
  "x-ticvai-persistence": "platform.offline_policy",
  "description": "Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n**One per scope node, keyed on `scopePath`** (pull audit R162). `id` is server-owned and absent where `getOfflinePolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them is refused `400`, `errors[]` naming the field.\n",
  "required": [
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$",
    "description": "**The node this policy is for, and the key `setOfflinePolicy` upserts on.** The body names its target here, because the path does not.\n"
   },
   "maxOfflineHours": {
    "type": "integer",
    "default": 24,
    "minimum": 1,
    "maximum": 72,
    "description": "**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect. Bounds 1 to 72 hours: proposed, client to correct (audit R129).\n"
   },
   "allowedOffline": {
    "type": "array",
    "description": "**What may happen with no network**, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified.\n",
    "items": {
     "type": "string",
     "enum": [
      "sale",
      "refund",
      "exchange",
      "entitlementIssue",
      "entitlementValidate",
      "loyaltyAccrual",
      "loyaltyRedemption",
      "walletSpend",
      "priceOverride",
      "discount",
      "voidLine",
      "noSale"
     ]
    }
   },
   "offlineValueCeiling": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129).\n"
   },
   "offlineTransactionCeiling": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 5000,
    "description": "**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. Bounds 1 to 5,000: proposed, client to correct (audit R129).\n"
   },
   "onCeilingBreach": {
    "type": "string",
    "enum": [
     "warn",
     "blockNewSales",
     "blockAll"
    ],
    "default": "blockNewSales"
   },
   "requiresManagerToExtend": {
    "type": "boolean",
    "default": true
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
   "title": {
    "type": "string",
    "description": "The heading a guest sees, and the field a refund question retrieves against.\n"
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
    "readOnly": true,
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
   "evaluationMode": {
    "type": "string",
    "enum": [
     "central",
     "edge",
     "device",
     "hybrid"
    ]
   },
   "policyCategory": {
    "type": "string",
    "description": "e.g. Ticket Status, Time Rule, Membership Tier, Live Occupancy, Live Fraud AI"
   },
   "supportedLocations": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Any of central, edge, device"
   },
   "offlineBehaviour": {
    "type": "string",
    "enum": [
     "available",
     "conditional",
     "unavailable"
    ]
   },
   "maxDataAgeMinutes": {
    "type": "integer",
    "description": "Oldest cached data an offline evaluation may use"
   }
  },
  "required": [
   "policyCategory",
   "evaluationMode"
  ]
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
 "PolicyScopeHierarchyInheritanceInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Policy Scope, Hierarchy & Inheritance submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "policyId",
   "scopeLevel",
   "scopeId",
   "policyCategory",
   "conflictResolution"
  ],
  "properties": {
   "policyId": {
    "type": "string",
    "description": "The dynamic access policy placed in the hierarchy"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "venue",
     "park",
     "zone",
     "attraction",
     "accessPoint"
    ]
   },
   "scopeId": {
    "type": "string"
   },
   "policyCategory": {
    "type": "string",
    "enum": [
     "emergency",
     "securityFraud",
     "regulatorySafety",
     "venueRestriction",
     "accreditation",
     "membership",
     "standardAccess"
    ]
   },
   "categoryRank": {
    "type": "integer",
    "minimum": 1,
    "description": "Lower wins; emergency is 1"
   },
   "conflictResolution": {
    "type": "string",
    "enum": [
     "highestPriorityWins",
     "denyOverridesAllow",
     "mostSpecificWins",
     "mandatoryParentWins",
     "explicitResolution"
    ],
    "default": "denyOverridesAllow"
   },
   "mandatory": {
    "type": "boolean",
    "default": false,
    "description": "A child scope cannot override a mandatory policy"
   }
  }
 },
 "PolicyScopeHierarchyInheritanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Policy Scope, Hierarchy & Inheritance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "scopeId": {
    "type": "string"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "venue",
     "park",
     "zone",
     "attraction",
     "accessPoint"
    ]
   },
   "policyId": {
    "type": "string"
   },
   "conflictResolution": {
    "type": "string",
    "enum": [
     "highestPriorityWins",
     "denyOverridesAllow",
     "mostSpecificWins",
     "mandatoryParentWins",
     "explicitResolution"
    ],
    "description": "How a conflict with another policy is resolved"
   },
   "policyCategory": {
    "type": "string",
    "enum": [
     "emergency",
     "securityFraud",
     "regulatorySafety",
     "venueRestriction",
     "accreditation",
     "membership",
     "standardAccess"
    ]
   },
   "categoryRank": {
    "type": "integer",
    "description": "Configurable precedence of the category; 1 wins"
   },
   "mandatory": {
    "type": "boolean",
    "description": "Parent policy that overrides local permissions below it"
   }
  },
  "required": [
   "policyId",
   "scopeLevel",
   "scopeId"
  ]
 },
 "PolicySimulationConflictImpactAnalysisInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Policy Simulation, Conflict & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "policyId": {
    "type": "string"
   },
   "policyVersion": {
    "type": "string"
   },
   "scenarioTime": {
    "type": "string",
    "format": "date-time",
    "description": "Simulated moment of the scan"
   },
   "credentialId": {
    "type": "string",
    "description": "Optional credential to simulate"
   },
   "runSavedScenarios": {
    "type": "boolean",
    "description": "Regression: run saved scenarios against this policy version"
   },
   "scenarioCount": {
    "type": "integer"
   },
   "passedCount": {
    "type": "integer"
   },
   "changedOutcomeCount": {
    "type": "integer"
   },
   "affectedCredentials": {
    "type": "integer"
   }
  },
  "required": [
   "policyId"
  ]
 },
 "PolicySimulationConflictImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Policy Simulation, Conflict & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "policyId": {
    "type": "string"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy (the pack shows 82%)"
   },
   "policiesInvolved": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "policies involved"
   },
   "hierarchy": {
    "type": "string",
    "description": "hierarchy"
   },
   "priority": {
    "type": "integer",
    "description": "priority"
   },
   "resultingDecision": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ],
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
    "type": "integer",
    "description": "estimated guests impacted"
   },
   "policyVersion": {
    "type": "string"
   },
   "scenarioTime": {
    "type": "string",
    "format": "date-time",
    "description": "Simulated moment of the scan"
   },
   "credentialId": {
    "type": "string",
    "description": "Optional credential to simulate"
   },
   "runSavedScenarios": {
    "type": "boolean",
    "description": "Regression: run saved scenarios against this policy version"
   },
   "scenarioCount": {
    "type": "integer"
   },
   "passedCount": {
    "type": "integer"
   },
   "changedOutcomeCount": {
    "type": "integer"
   },
   "affectedCredentials": {
    "type": "integer"
   }
  },
  "required": [
   "policyId"
  ]
 },
 "VisualDynamicPolicyBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Visual Dynamic Policy Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "conditionExpression": {
    "type": "string",
    "description": "Condition tree over catalogue attributes using AND, OR, NOT, IN and BETWEEN, e.g. Accreditation = VIP AND Zone = Backstage"
   },
   "name": {
    "type": "string",
    "description": "e.g. VIP Backstage Access"
   },
   "policyId": {
    "type": "string"
   },
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
    ],
    "description": "Decision the policy returns when its condition holds"
   },
   "priority": {
    "type": "integer"
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
   "conditionExpression",
   "result"
  ]
 },
 "VisualDynamicPolicyBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Visual Dynamic Policy Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "conditionExpression": {
    "type": "string",
    "description": "Condition tree over catalogue attributes using AND, OR, NOT, IN and BETWEEN, e.g. Accreditation = VIP AND Zone = Backstage"
   },
   "name": {
    "type": "string",
    "description": "e.g. VIP Backstage Access"
   },
   "policyId": {
    "type": "string"
   },
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
    ],
    "description": "Decision the policy returns when its condition holds"
   },
   "priority": {
    "type": "integer"
   }
  },
  "required": [
   "policyId",
   "name",
   "conditionExpression",
   "result"
  ]
 }
}
```
