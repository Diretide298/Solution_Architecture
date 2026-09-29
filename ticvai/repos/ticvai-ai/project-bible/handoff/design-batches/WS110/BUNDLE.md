# WS110 — ACCREDITATION board 3

**9 screens · 8 operations · 16 schemas · 6 permissions**

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
  `ACCREDITATION_APPROVE, ACCREDITATION_VIEW, APPROVAL_CONFIGURE, APPROVAL_REQUEST, PRICE_CONFIGURE, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-635` | Accreditation Review Queue | listDetail | 1 | 0 | — |
| `BO-636` | Application Review Workspace | listDetail | 2 | 0 | — |
| `BO-637` | Approval Workflow Builder | listDetail | 1 | 0 | — |
| `BO-638` | Approval Rules & Conditions | listDetail | 1 | 0 | — |
| `BO-639` | Reviewer Assignment & Delegation | listDetail | 1 | 0 | — |
| `BO-640` | Rejection & Resubmission Management | listDetail | 1 | 0 | — |
| `BO-641` | Escalation & Exception Management | listDetail | 1 | 0 | — |
| `BO-642` | Approval Decision History | listDetail | 1 | 0 | — |
| `BO-643` | Approval Policy Validation & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-636, BO-637, BO-638, BO-639, BO-640, BO-641, BO-642, BO-643 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-635",
  "name": "Accreditation Review Queue",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "3",
   "number": "1",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-review-queue-bo-635",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationReviewQueue.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-636",
    "BO-637",
    "BO-638",
    "BO-639",
    "BO-640",
    "BO-641",
    "BO-642",
    "BO-643"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-636",
     "trigger": "Application Review Workspace",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-637",
     "trigger": "Approval Workflow Builder",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-638",
     "trigger": "Approval Rules & Conditions",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-639",
     "trigger": "Reviewer Assignment & Delegation",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-640",
     "trigger": "Rejection & Resubmission Management",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-641",
     "trigger": "Escalation & Exception Management",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-642",
     "trigger": "Approval Decision History",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-643",
     "trigger": "Approval Policy Validation & Publication",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each record shall show) and no metric row",
  "purpose": "Central operational queue for applications requiring review.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack ACCREDITATION.pdf, page 20 §Each record shall show"
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
       "label": "Search accreditation review queue",
       "provenance": "pack ACCREDITATION.pdf, page 20 §Filters shall include"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Category",
        "Event",
        "Venue",
        "Organization",
        "Reviewer",
        "Workflow stage",
        "SLA status",
        "Verification status"
       ],
       "notes": "The pack filters this screen by category, event, venue, organization, reviewer, workflow stage and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack ACCREDITATION.pdf, page 20 §Filters shall include"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every accreditation review queue",
       "columns": [
        "Application ID",
        "Applicant name",
        "Photo",
        "Accreditation category",
        "Organization",
        "Event / venue",
        "Submission date",
        "Verification status",
        "Document status",
        "Current workflow stage",
        "Assigned reviewer",
        "SLA ageing",
        "Risk / exception indicator"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack ACCREDITATION.pdf, page 20 §Each record shall show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected accreditation review queue",
       "bindsTo": null,
       "columns": [
        "Application ID",
        "Applicant name",
        "Photo",
        "Accreditation category",
        "Organization",
        "Event / venue",
        "Submission date",
        "Verification status",
        "Document status",
        "Current workflow stage",
        "Assigned reviewer",
        "SLA ageing",
        "Risk / exception indicator"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Scope of Work”.",
       "provenance": "pack ACCREDITATION.pdf, page 20 §Each record shall show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Key requirement: 12.1.3",
       "provenance": "pack ACCREDITATION.pdf, page 20 §Actions shall include"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation review queue list.",
   "error": "Could not load. Names which read failed and leaves the accreditation review queue untouched.",
   "emptyFirstRun": "No accreditation review queue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation review queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationApplications",
    "contract": "accreditation",
    "purpose": "The review queue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Application ID",
    "Applicant name",
    "Photo",
    "Accreditation category",
    "Organization",
    "Event / venue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-635",
   "workshopBoard": "wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-635"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 20. 0 of 21 labels bound to a contract property; 22 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Key requirement: 12.1.3 are choices sent by `listAccreditationApplications` (requirement reference shown on the queue).",
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
  "id": "BO-636",
  "name": "Application Review Workspace",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "3",
   "number": "2",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/application-review-workspace-bo-636",
   "component": "apps/venue-management-web/src/routes/access-venue/ApplicationReviewWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-635"
   ],
   "exitTo": [
    "BO-635"
   ],
   "transitions": [
    {
     "to": "BO-635",
     "trigger": "Back to Accreditation Review Queue",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give reviewers a complete decision workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 21"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 21"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "decideAccreditationApplication",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAccreditationApplications",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideAccreditationApplication"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The application review list.",
   "error": "Could not load. Names which read failed and leaves the application review untouched.",
   "emptyFirstRun": "No application review yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the application review are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "decideAccreditationApplication",
    "contract": "accreditation",
    "purpose": "Decide",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationApplications",
     "listAccreditationHolders"
    ]
   },
   {
    "operationId": "listAccreditationApplications",
    "contract": "accreditation",
    "purpose": "The application",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-636",
   "workshopBoard": "wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-636"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 21. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "applicationId",
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
  "id": "BO-637",
  "name": "Approval Workflow Builder",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "3",
   "number": "3",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/approval-workflow-builder-bo-637",
   "component": "apps/venue-management-web/src/routes/access-venue/ApprovalWorkflowBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-635"
   ],
   "exitTo": [
    "BO-635"
   ],
   "transitions": [
    {
     "to": "BO-635",
     "trigger": "Back to Accreditation Review Queue",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure reusable accreditation approval workflows.",
  "gaps": [
   {
    "operation": null,
    "why": "**Approval Workflow Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 22"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "approveWorkflow",
       "label": "Approve workflow",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "approveWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval workflow list.",
   "error": "Could not load. Names which read failed and leaves the approval workflow untouched.",
   "emptyFirstRun": "No approval workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveWorkflow",
    "contract": "catalogue",
    "purpose": "Approval Workflow Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-637",
   "workshopBoard": "wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-637"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-638",
  "name": "Approval Rules & Conditions",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "3",
   "number": "4",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/approval-rules-conditions-bo-638",
   "component": "apps/venue-management-web/src/routes/access-venue/ApprovalRulesConditions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-635"
   ],
   "exitTo": [
    "BO-635"
   ],
   "transitions": [
    {
     "to": "BO-635",
     "trigger": "Back to Accreditation Review Queue",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define when a particular approval workflow is applied.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 22"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setVisualWorkflow",
       "label": "Save visual workflow",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setVisualWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval rules conditions list.",
   "error": "Could not load. Names which read failed and leaves the approval rules conditions untouched.",
   "emptyFirstRun": "No approval rules conditions yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval rules conditions are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualWorkflow",
    "contract": "approvals",
    "purpose": "Approval rules and conditions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-638",
   "workshopBoard": "wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-638"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-639",
  "name": "Reviewer Assignment & Delegation",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "3",
   "number": "5",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/reviewer-assignment-delegation-bo-639",
   "component": "apps/venue-management-web/src/routes/access-venue/ReviewerAssignmentDelegation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-635"
   ],
   "exitTo": [
    "BO-635"
   ],
   "transitions": [
    {
     "to": "BO-635",
     "trigger": "Back to Accreditation Review Queue",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage reviewers and approval responsibilities.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 23"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setApprovalMatrix",
       "label": "Save approval matrix",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApprovalMatrix"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reviewer delegation list.",
   "error": "Could not load. Names which read failed and leaves the reviewer delegation untouched.",
   "emptyFirstRun": "No reviewer delegation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reviewer delegation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Reviewer assignment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-639",
   "workshopBoard": "wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-639"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-640",
  "name": "Rejection & Resubmission Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "3",
   "number": "6",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/rejection-resubmission-management-bo-640",
   "component": "apps/venue-management-web/src/routes/access-venue/RejectionResubmissionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-635"
   ],
   "exitTo": [
    "BO-635"
   ],
   "transitions": [
    {
     "to": "BO-635",
     "trigger": "Back to Accreditation Review Queue",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control rejected applications and resubmission workflows.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 24"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 24"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "decideAccreditationApplication",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideAccreditationApplication"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rejection resubmission list.",
   "error": "Could not load. Names which read failed and leaves the rejection resubmission untouched.",
   "emptyFirstRun": "No rejection resubmission yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rejection resubmission are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "decideAccreditationApplication",
    "contract": "accreditation",
    "purpose": "Reject or return",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationApplications",
     "listAccreditationHolders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-640",
   "workshopBoard": "wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-640"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 24. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "applicationId",
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
  "id": "BO-641",
  "name": "Escalation & Exception Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "3",
   "number": "7",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/escalation-exception-management-bo-641",
   "component": "apps/venue-management-web/src/routes/access-venue/EscalationExceptionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-635"
   ],
   "exitTo": [
    "BO-635"
   ],
   "transitions": [
    {
     "to": "BO-635",
     "trigger": "Back to Accreditation Review Queue",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle applications requiring special review.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 24"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 24"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "escalateApprovalRequest",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "escalateApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The escalation exception list.",
   "error": "Could not load. Names which read failed and leaves the escalation exception untouched.",
   "emptyFirstRun": "No escalation exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the escalation exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "escalateApprovalRequest",
    "contract": "approvals",
    "purpose": "Escalate an exception",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-641",
   "workshopBoard": "wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-641"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 24. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "requestId",
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
  "id": "BO-642",
  "name": "Approval Decision History",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "3",
   "number": "9",
   "page": 25
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/approval-decision-history-bo-642",
   "component": "apps/venue-management-web/src/routes/access-venue/ApprovalDecisionHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-635"
   ],
   "exitTo": [
    "BO-635"
   ],
   "transitions": [
    {
     "to": "BO-635",
     "trigger": "Back to Accreditation Review Queue",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain a complete record of every approval decision.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 25"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 25"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "approveDecision",
       "label": "Approve decision",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "approveDecision"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval decision history list.",
   "error": "Could not load. Names which read failed and leaves the approval decision history untouched.",
   "emptyFirstRun": "No approval decision history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval decision history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveDecision",
    "contract": "promotions",
    "purpose": "Approval Inbox & Decision Workspace",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-642",
   "workshopBoard": "wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-642"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 25. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-643",
  "name": "Approval Policy Validation & Publication",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "3",
   "number": "10",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/approval-policy-validation-publication-bo-643",
   "component": "apps/venue-management-web/src/routes/access-venue/ApprovalPolicyValidationPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-635"
   ],
   "exitTo": [
    "BO-635"
   ],
   "transitions": [
    {
     "to": "BO-635",
     "trigger": "Back to Accreditation Review Queue",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Validate and publish approval workflow configurations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 26"
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
   "loading": "The approval policy validation list.",
   "error": "Could not load. Names which read failed and leaves the approval policy validation untouched.",
   "emptyFirstRun": "No approval policy validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval policy validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationAudit",
    "contract": "accreditation",
    "purpose": "Decision history",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-643",
   "workshopBoard": "wireframes/WS03 ACCREDITATION Board 3.dc.html#bo-643"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveDecision": {
  "method": "PUT",
  "path": "/decision",
  "contract": "promotions",
  "summary": "Approval Inbox & Decision Workspace",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "ApprovalInboxDecisionWorkspaceInput",
  "responds": "ApprovalInboxDecisionWorkspaceView"
 },
 "approveWorkflow": {
  "method": "PUT",
  "path": "/workflow",
  "contract": "catalogue",
  "summary": "Approval Workflow Designer",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ApprovalWorkflowDesignerInput",
  "responds": "ApprovalWorkflowDesignerView"
 },
 "decideAccreditationApplication": {
  "method": "POST",
  "path": "/accreditation-applications/{applicationId}/decide",
  "contract": "accreditation",
  "summary": "Approve, reject, return for more, or escalate",
  "permission": "ACCREDITATION_APPROVE",
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
  "requestBody": null,
  "responds": "AccreditationApplication"
 },
 "escalateApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/escalate",
  "contract": "approvals",
  "summary": "Move it up a level",
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
  "requestBody": null,
  "responds": "ApprovalRequest"
 },
 "listAccreditationApplications": {
  "method": "GET",
  "path": "/accreditation-applications",
  "contract": "accreditation",
  "summary": "Applications, by state and programme",
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
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "applicantType",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationApplication"
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
 "setApprovalMatrix": {
  "method": "PUT",
  "path": "/approval-matrices",
  "contract": "approvals",
  "summary": "Configure what requires approval",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "ApprovalMatrix",
  "responds": "ApprovalMatrix"
 },
 "setVisualWorkflow": {
  "method": "PUT",
  "path": "/visual-workflow",
  "contract": "approvals",
  "summary": "Visual Workflow Designer",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "VisualWorkflowDesignerInput",
  "responds": "VisualWorkflowDesignerView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccreditationApplication": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.application",
  "description": "Board 1.3. **Usually submitted by an organisation on behalf of its people.**",
  "required": [
   "programmeId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "reference": {
    "type": "string"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "applicantType": {
    "type": "string"
   },
   "submittedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subject": {
    "type": "object",
    "additionalProperties": true,
    "description": "Name, date of birth, nationality, contact — shaped by the requirements matrix."
   },
   "requirementStatus": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "properties": {
      "requirementCode": {
       "type": "string"
      },
      "satisfied": {
       "type": "boolean"
      },
      "documentId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "submitted",
     "underReview",
     "informationRequested",
     "approved",
     "rejected",
     "withdrawn",
     "expired"
    ]
   },
   "decisionReason": {
    "type": "string",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
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
 "ApprovalInboxDecisionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Approval Inbox & Decision Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "returnForChange",
     "requestInformation",
     "delegate"
    ],
    "description": "Approver decision"
   },
   "comment": {
    "type": "string",
    "description": "Approver comment"
   },
   "delegateTo": {
    "type": "string",
    "description": "Approver delegated to, for delegate"
   }
  }
 },
 "ApprovalInboxDecisionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Approval Inbox & Decision Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested by"
   },
   "requestDate": {
    "type": "string",
    "format": "date-time",
    "description": "Request date"
   },
   "requestedAction": {
    "type": "string",
    "description": "Requested action"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "budget": {
    "type": "string",
    "description": "Budget"
   },
   "estimatedRedemptions": {
    "type": "integer",
    "description": "Estimated redemptions"
   },
   "estimatedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated revenue"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin impact"
   },
   "customerReach": {
    "type": "string",
    "description": "Customer reach"
   },
   "riskLevel": {
    "type": "string",
    "description": "Risk level"
   },
   "aiForecast": {
    "type": "string",
    "description": "AI forecast"
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "returnForChange",
     "requestInformation",
     "delegate"
    ],
    "description": "Approver decision"
   },
   "comment": {
    "type": "string",
    "description": "Approver comment"
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
 "ApprovalMatrix": {
  "type": "object",
  "x-ticvai-persistence": "approvals.matrix",
  "required": [
   "kind",
   "scopeLevel",
   "rules"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"
   },
   "rules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalRule"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
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
 "ApprovalRule": {
  "type": "object",
  "x-ticvai-persistence": "approvals.rule",
  "required": [
   "order",
   "approverRoleIds",
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "order": {
    "type": "integer",
    "description": "**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"
   },
   "minAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "riskScoreAbove": {
    "type": "number",
    "nullable": true,
    "description": "11.1.12. **Nothing supplies this yet** — risk scoring is parked with the model-dependent AI. The field exists so adding the engine later is configuration rather than a schema change.\n"
   },
   "condition": {
    "type": "string",
    "nullable": true,
    "description": "11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"
   },
   "approverRoleIds": {
    "type": "array",
    "minItems": 1,
    "description": "Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "approverScopeLevel": {
    "type": "string",
    "enum": [
     "venue",
     "department",
     "region",
     "tenant"
    ],
    "description": "11.1.39. Which organisational level the approver must sit at."
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "levels": {
    "type": "integer",
    "default": 1,
    "description": "11.1.3. Multi-level chains ask each level in turn."
   },
   "requiresMfa": {
    "type": "boolean",
    "default": false
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.14. Null means no SLA, which is different from a long one."
   },
   "escalateAfterMinutes": {
    "type": "integer",
    "nullable": true
   },
   "escalateToRoleIds": {
    "type": "array",
    "description": "Role ids from `identity.listRoles`, as `approverRoleIds`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "expiresAfterMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.53. An unanswered request eventually stops waiting."
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
 "ApprovalWorkflowDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "workflowName": {
    "type": "string",
    "description": "Workflow name"
   },
   "applicableProductTypes": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ProductKind"
    },
    "description": "Applicable product types; empty = all"
   },
   "venue": {
    "type": "string",
    "description": "Venue id; empty = all venues",
    "nullable": true
   },
   "department": {
    "type": "string",
    "description": "Department",
    "nullable": true
   },
   "changeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "newProduct",
      "description",
      "price",
      "validity",
      "capacity",
      "entitlement",
      "eligibility",
      "tax",
      "channel",
      "media",
      "policy",
      "relationship",
      "retirement"
     ]
    },
    "description": "Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"
   },
   "approvalStages": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "order": {
       "type": "integer",
       "description": "Stage order; stages sharing an order run in parallel, otherwise sequential"
      },
      "name": {
       "type": "string"
      },
      "approverRole": {
       "type": "string",
       "nullable": true
      },
      "specificApproverId": {
       "type": "string",
       "nullable": true
      },
      "approvalGroupId": {
       "type": "string",
       "nullable": true
      },
      "mandatory": {
       "type": "boolean"
      },
      "slaHours": {
       "type": "integer",
       "description": "SLA in hours"
      },
      "escalateToRole": {
       "type": "string",
       "nullable": true,
       "description": "Escalation when the SLA is missed"
      },
      "delegationAllowed": {
       "type": "boolean"
      },
      "reminderEveryHours": {
       "type": "integer",
       "nullable": true,
       "description": "Reminder frequency"
      }
     }
    },
    "description": "Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"
   },
   "rejectionBehavior": {
    "type": "string",
    "enum": [
     "returnToDraft",
     "returnToPreviousStage",
     "closeRequest"
    ],
    "description": "What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"
   },
   "resubmissionBehavior": {
    "type": "string",
    "enum": [
     "restartFromFirstStage",
     "resumeAtRejectingStage"
    ],
    "description": "Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"
   },
   "workflowId": {
    "type": "string",
    "description": "Existing workflow to change; empty to create",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "ApprovalWorkflowDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowName": {
    "type": "string",
    "description": "Workflow name"
   },
   "applicableProductTypes": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ProductKind"
    },
    "description": "Applicable product types; empty = all"
   },
   "venue": {
    "type": "string",
    "description": "Venue id; empty = all venues",
    "nullable": true
   },
   "department": {
    "type": "string",
    "description": "Department",
    "nullable": true
   },
   "changeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "newProduct",
      "description",
      "price",
      "validity",
      "capacity",
      "entitlement",
      "eligibility",
      "tax",
      "channel",
      "media",
      "policy",
      "relationship",
      "retirement"
     ]
    },
    "description": "Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"
   },
   "approvalStages": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "order": {
       "type": "integer",
       "description": "Stage order; stages sharing an order run in parallel, otherwise sequential"
      },
      "name": {
       "type": "string"
      },
      "approverRole": {
       "type": "string",
       "nullable": true
      },
      "specificApproverId": {
       "type": "string",
       "nullable": true
      },
      "approvalGroupId": {
       "type": "string",
       "nullable": true
      },
      "mandatory": {
       "type": "boolean"
      },
      "slaHours": {
       "type": "integer",
       "description": "SLA in hours"
      },
      "escalateToRole": {
       "type": "string",
       "nullable": true,
       "description": "Escalation when the SLA is missed"
      },
      "delegationAllowed": {
       "type": "boolean"
      },
      "reminderEveryHours": {
       "type": "integer",
       "nullable": true,
       "description": "Reminder frequency"
      }
     }
    },
    "description": "Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"
   },
   "rejectionBehavior": {
    "type": "string",
    "enum": [
     "returnToDraft",
     "returnToPreviousStage",
     "closeRequest"
    ],
    "description": "What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"
   },
   "resubmissionBehavior": {
    "type": "string",
    "enum": [
     "restartFromFirstStage",
     "resumeAtRejectingStage"
    ],
    "description": "Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow id",
    "format": "uuid"
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "VisualWorkflowDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; writes approvals.workflow_definition and a draft approvals.workflow_version (data model for the agreed operations, 29 September)",
  "description": "**What Visual Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "definition": {
    "type": "string",
    "description": "The workflow graph (nodes and connections) as a JSON document"
   },
   "nodeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "start",
      "trigger",
      "task",
      "decision",
      "approval",
      "systemAction",
      "notification",
      "wait",
      "timer",
      "parallelBranch",
      "merge",
      "escalation",
      "subWorkflow",
      "end"
     ]
    },
    "description": "Node kinds used in this workflow"
   },
   "workflowName": {
    "type": "string",
    "description": "Workflow Name"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "businessProcess": {
    "type": "string",
    "description": "Business Process"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective Dates"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "deadEnds",
      "missingOutcomes",
      "circularLoops",
      "missingAssignee",
      "invalidActions"
     ]
    },
    "description": "Design problems the designer found (read-only)"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow identifier; absent on input to create a new workflow"
   },
   "trigger": {
    "type": "string",
    "description": "What starts the workflow"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "description": "Effective to"
   }
  },
  "required": [
   "workflowName",
   "module",
   "definition"
  ]
 },
 "VisualWorkflowDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_definition and its draft approvals.workflow_version (data model for the agreed operations, 29 September)",
  "description": "**What Visual Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "definition": {
    "type": "string",
    "description": "The workflow graph (nodes and connections) as a JSON document"
   },
   "nodeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "start",
      "trigger",
      "task",
      "decision",
      "approval",
      "systemAction",
      "notification",
      "wait",
      "timer",
      "parallelBranch",
      "merge",
      "escalation",
      "subWorkflow",
      "end"
     ]
    },
    "description": "Node kinds used in this workflow"
   },
   "workflowName": {
    "type": "string",
    "description": "Workflow Name"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "businessProcess": {
    "type": "string",
    "description": "Business Process"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective Dates"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "deadEnds",
      "missingOutcomes",
      "circularLoops",
      "missingAssignee",
      "invalidActions"
     ]
    },
    "description": "Design problems the designer found (read-only)"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow identifier; absent on input to create a new workflow"
   },
   "trigger": {
    "type": "string",
    "description": "What starts the workflow"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "description": "Effective to"
   }
  },
  "required": [
   "workflowName",
   "module",
   "definition"
  ]
 }
}
```
