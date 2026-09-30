# WS16 — Approval Workflows and Governance board 4

**10 screens · 12 operations · 17 schemas · 6 permissions**

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
  `APPROVAL_ACT, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW, PRICE_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-374` | Approval Decision Workspace | listDetail | 1 | 0 | — |
| `BO-375` | Business Context & Evidence Viewer | listDetail | 1 | 0 | — |
| `BO-376` | Approval Timeline & Decision Chain | listDetail | 1 | 0 | — |
| `BO-377` | Approve & Sensitive Action Confirmation | listDetail | 3 | 0 | — |
| `BO-378` | Reject / Return / Request Information | listDetail | 1 | 0 | — |
| `BO-379` | Requester Modification & Resubmission | listDetail | 1 | 0 | — |
| `BO-380` | Withdrawal, Cancellation, Expiration & Reopening | listDetail | 1 | 0 | — |
| `BO-381` | Segregation of Duties & Four-Eyes Control | listDetail | 1 | 0 | — |
| `BO-382` | Approved Action Execution & Status | listDetail | 3 | 0 | — |
| `BO-383` | Decision Record & Immutable Audit View | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-374, BO-375, BO-376, BO-377, BO-379, BO-380, BO-381, BO-382, BO-383 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-374",
  "name": "Approval Decision Workspace",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "1",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/approval-decision-workspace-bo-374",
   "component": "apps/venue-management-web/src/routes/venue-operations/ApprovalDecisionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-375",
    "BO-376",
    "BO-377",
    "BO-378",
    "BO-379",
    "BO-380",
    "BO-381",
    "BO-382",
    "BO-383"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "BO-383",
     "trigger": "Decision Record & Immutable Audit View",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "BO-375",
     "trigger": "Business Context & Evidence Viewer",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "BO-376",
     "trigger": "Approval Timeline & Decision Chain",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "BO-377",
     "trigger": "Approve & Sensitive Action Confirmation",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "BO-378",
     "trigger": "Reject / Return / Request Information",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "BO-379",
     "trigger": "Requester Modification & Resubmission",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "BO-380",
     "trigger": "Withdrawal, Cancellation, Expiration & Reopening",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "BO-381",
     "trigger": "Segregation of Duties & Four-Eyes Control",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "BO-382",
     "trigger": "Approved Action Execution & Status",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the approver with one comprehensive workspace to evaluate and action a request.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 31"
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
   "loading": "The approval decision list.",
   "error": "Could not load. Names which read failed and leaves the approval decision untouched.",
   "emptyFirstRun": "No approval decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval decision are still there. Names the active filter and offers to clear it.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-374",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-374"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-375",
  "name": "Business Context & Evidence Viewer",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "2",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/business-context-evidence-viewer-bo-375",
   "component": "apps/venue-management-web/src/routes/venue-operations/BusinessContextEvidenceViewer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-374"
   ],
   "exitTo": [
    "BO-374"
   ],
   "transitions": [
    {
     "to": "BO-374",
     "trigger": "Back to Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the business evidence required to make an informed decision. For example, for a refund approval:",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 32"
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
       "impliedBy": "listApprovalRequests",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The business context evidence list.",
   "error": "Could not load. Names which read failed and leaves the business context evidence untouched.",
   "emptyFirstRun": "No business context evidence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the business context evidence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "The request and its evidence",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-375",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-375"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-376",
  "name": "Approval Timeline & Decision Chain",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "3",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/approval-timeline-decision-chain-bo-376",
   "component": "apps/venue-management-web/src/routes/venue-operations/ApprovalTimelineDecisionChain.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-374"
   ],
   "exitTo": [
    "BO-374"
   ],
   "transitions": [
    {
     "to": "BO-374",
     "trigger": "Back to Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a visual representation of the complete approval journey.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 33 §Display"
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
       "label": "Every approval timeline decision",
       "columns": [
        "Request created",
        "Workflow triggered",
        "Routing decision",
        "Assignment",
        "Reassignment",
        "Delegation",
        "Comments",
        "Approval",
        "Rejection",
        "Escalation",
        "Notification",
        "Execution"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 33 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval timeline decision",
       "bindsTo": null,
       "columns": [
        "Request created",
        "Workflow triggered",
        "Routing decision",
        "Assignment",
        "Reassignment",
        "Delegation",
        "Comments",
        "Approval",
        "Rejection",
        "Escalation",
        "Notification",
        "Execution"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Current”.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 33 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval timeline decision list.",
   "error": "Could not load. Names which read failed and leaves the approval timeline decision untouched.",
   "emptyFirstRun": "No approval timeline decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval timeline decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getApprovalRecord",
    "contract": "approvals",
    "purpose": "The decision chain, verified",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Request created",
    "Workflow triggered",
    "Routing decision",
    "Assignment",
    "Reassignment",
    "Delegation"
   ],
   "params": [
    {
     "name": "requestId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-376",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-376"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 33. 0 of 12 labels bound to a contract property; 12 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-377",
  "name": "Approve & Sensitive Action Confirmation",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "4",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/approve-sensitive-action-confirmation-bo-377",
   "component": "apps/venue-management-web/src/routes/venue-operations/ApproveSensitiveActionConfirmation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-374"
   ],
   "exitTo": [
    "BO-374"
   ],
   "transitions": [
    {
     "to": "BO-374",
     "trigger": "Back to Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control the final approval action before it becomes binding.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 34"
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
       "impliedBy": "decideApprovalRequest",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listStepUpPolicies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approve sensitive action list.",
   "error": "Could not load. Names which read failed and leaves the approve sensitive action untouched.",
   "emptyFirstRun": "No approve sensitive action yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approve sensitive action are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Approve",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalRequests",
     "getApprovalRecord",
     "getApprovalAnalytics"
    ]
   },
   {
    "operationId": "signApprovalDecision",
    "contract": "approvals",
    "purpose": "Sign it where required",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getApprovalRecord"
    ]
   },
   {
    "operationId": "listStepUpPolicies",
    "contract": "approvals",
    "purpose": "Whether step-up is required",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-377",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-377"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-378",
  "name": "Reject / Return / Request Information",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "5",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/reject-return-request-information-bo-378",
   "component": "apps/venue-management-web/src/routes/venue-operations/RejectReturnRequestInformation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-374"
   ],
   "exitTo": [
    "BO-374"
   ],
   "transitions": [
    {
     "to": "BO-374",
     "trigger": "Back to Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage situations where an approver cannot or should not approve the request.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 34"
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
       "label": "Reject",
       "operation": "decideApprovalRequest",
       "notes": "Sends `decision=reject` to `decideApprovalRequest`.",
       "provenance": "MoM 10 Aug 2026 §5.5 (Approve, Reject, Return, Request More Information); decided 29 September, readiness close-out (QA wiring note)"
      },
      {
       "kind": "secondaryButton",
       "label": "Return for changes",
       "operation": "decideApprovalRequest",
       "notes": "Sends `decision=return` to `decideApprovalRequest`.",
       "provenance": "MoM 10 Aug 2026 §5.5 (Approve, Reject, Return, Request More Information); decided 29 September, readiness close-out (QA wiring note)"
      },
      {
       "kind": "secondaryButton",
       "label": "Request more information",
       "operation": "decideApprovalRequest",
       "notes": "Sends `decision=requestInformation` to `decideApprovalRequest`.",
       "provenance": "MoM 10 Aug 2026 §5.5 (Approve, Reject, Return, Request More Information); decided 29 September, readiness close-out (QA wiring note)"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reject return request list.",
   "error": "Could not load. Names which read failed and leaves the reject return request untouched.",
   "emptyFirstRun": "No reject return request yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reject return request are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Reject, return or ask for more",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalRequests",
     "getApprovalRecord",
     "getApprovalAnalytics"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-378",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-378"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-379",
  "name": "Requester Modification & Resubmission",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "6",
   "page": 35
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/requester-modification-resubmission-bo-379",
   "component": "apps/venue-management-web/src/routes/venue-operations/RequesterModificationResubmission.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-374"
   ],
   "exitTo": [
    "BO-374"
   ],
   "transitions": [
    {
     "to": "BO-374",
     "trigger": "Back to Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow rejected or returned requests to be corrected and submitted again. The source specifically requires rejected requests to be modified and resubmitted.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 35"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 35"
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
       "impliedBy": "resubmitApprovalRequest",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "resubmitApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The requester modification resubmission list.",
   "error": "Could not load. Names which read failed and leaves the requester modification resubmission untouched.",
   "emptyFirstRun": "No requester modification resubmission yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the requester modification resubmission are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "resubmitApprovalRequest",
    "contract": "approvals",
    "purpose": "Amend and resubmit",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalRequests"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-379",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-379"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 35. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-380",
  "name": "Withdrawal, Cancellation, Expiration & Reopening",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "7",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/withdrawal-cancellation-expiration-reopening-bo-380",
   "component": "apps/venue-management-web/src/routes/venue-operations/WithdrawalCancellationExpirationReopening.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-374"
   ],
   "exitTo": [
    "BO-374"
   ],
   "transitions": [
    {
     "to": "BO-374",
     "trigger": "Back to Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage non-standard approval lifecycle actions. The matrix explicitly covers draft requests, cancellation, expiration and reopening.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 36"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 36"
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
       "impliedBy": "withdrawApprovalRequest",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "withdrawApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The withdrawal cancellation expiration list.",
   "error": "Could not load. Names which read failed and leaves the withdrawal cancellation expiration untouched.",
   "emptyFirstRun": "No withdrawal cancellation expiration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the withdrawal cancellation expiration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "withdrawApprovalRequest",
    "contract": "approvals",
    "purpose": "Withdraw or cancel",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalRequests"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-380",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-380"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 36. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-381",
  "name": "Segregation of Duties & Four-Eyes Control",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "8",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/segregation-of-duties-four-eyes-control-bo-381",
   "component": "apps/venue-management-web/src/routes/venue-operations/SegregationOfDutiesFourEyesControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-374"
   ],
   "exitTo": [
    "BO-374"
   ],
   "transitions": [
    {
     "to": "BO-374",
     "trigger": "Back to Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Prevent inappropriate or conflicting approval actions. This is a critical governance screen. The matrix requires the system to prevent users from approving their own requests and supports dual approval for sensitive operations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 36"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 36"
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
       "impliedBy": "listApprovalControlPolicies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The segregation duties four-eyes list.",
   "error": "Could not load. Names which read failed and leaves the segregation duties four-eyes untouched.",
   "emptyFirstRun": "No segregation duties four-eyes yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the segregation duties four-eyes are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalControlPolicies",
    "contract": "approvals",
    "purpose": "Four-eyes and dual control in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-381",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-381"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 36. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-382",
  "name": "Approved Action Execution & Status",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "9",
   "page": 37
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/approved-action-execution-status-bo-382",
   "component": "apps/venue-management-web/src/routes/venue-operations/ApprovedActionExecutionStatus.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-374"
   ],
   "exitTo": [
    "BO-374"
   ],
   "transitions": [
    {
     "to": "BO-374",
     "trigger": "Back to Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Separate approval of the request from execution of the underlying business transaction. This distinction is extremely important. An approval being completed does not automatically mean the underlying transaction executed successfully.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 37"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 37"
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
       "label": "Retry | Investigate | Escalate",
       "operation": "resolveApprovedActionExecution",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 37 §Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listWorkflowInstanceProcess",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approved action execution list.",
   "error": "Could not load. Names which read failed and leaves the approved action execution untouched.",
   "emptyFirstRun": "No approved action execution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approved action execution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkflowInstanceProcess",
    "contract": "approvals",
    "purpose": "Whether the approved action ran",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listApprovedActionExecutions",
    "contract": "approvals",
    "purpose": "Approved actions and whether they ran",
    "trigger": "onLoad"
   },
   {
    "operationId": "resolveApprovedActionExecution",
    "contract": "approvals",
    "purpose": "Retry, investigate or escalate",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-382",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-382"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 1 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `resolveApprovedActionExecution`.",
  "entryState": {
   "params": [
    {
     "name": "executionId",
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
  "id": "BO-383",
  "name": "Decision Record & Immutable Audit View",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "4",
   "number": "10",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/decision-record-immutable-audit-view-bo-383",
   "component": "apps/venue-management-web/src/routes/venue-operations/DecisionRecordImmutableAuditView.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-374"
   ],
   "exitTo": [
    "BO-374"
   ],
   "transitions": [
    {
     "to": "BO-374",
     "trigger": "Back to Approval Decision Workspace",
     "provenance": "structural — pack board 4 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the authoritative record of a completed approval.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 38"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getApprovalRecord",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The decision record immutable list.",
   "error": "Could not load. Names which read failed and leaves the decision record immutable untouched.",
   "emptyFirstRun": "No decision record immutable yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the decision record immutable are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getApprovalRecord",
    "contract": "approvals",
    "purpose": "The immutable record, and whether it is intact",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-383",
   "workshopBoard": "wireframes/WS33 Approval Workflows and Governance Board 4.dc.html#bo-383"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getApprovalRecord": {
  "method": "GET",
  "path": "/approval-requests/{requestId}/record",
  "contract": "approvals",
  "summary": "The immutable decision record, and whether it is intact",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ApprovalRecord"
 },
 "listApprovalControlPolicies": {
  "method": "GET",
  "path": "/approval-control-policies",
  "contract": "approvals",
  "summary": "Segregation of duties, four-eyes and dual control",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ApprovalControlPolicy"
 },
 "listApprovalRequests": {
  "method": "GET",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Requests awaiting a decision, or already decided",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assignedToMe",
    "in": "query",
    "required": null
   },
   {
    "name": "raisedByMe",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "breachingWithinMinutes",
    "in": "query",
    "required": null
   },
   {
    "name": "sort",
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
 "listApprovedActionExecutions": {
  "method": "GET",
  "path": "/approved-action-executions",
  "contract": "approvals",
  "summary": "Approved actions and whether they ran",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "sourceModule",
    "in": "query",
    "required": false
   },
   {
    "name": "approvalRequestId",
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
 "listStepUpPolicies": {
  "method": "GET",
  "path": "/step-up-policies",
  "contract": "approvals",
  "summary": "What needs a second factor here",
  "permission": "APPROVAL_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "effective",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "StepUpPolicy"
 },
 "listWorkflowInstanceProcess": {
  "method": "GET",
  "path": "/workflow-instance-process",
  "contract": "approvals",
  "summary": "Workflow Instance Monitor & Process Timeline",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workflowInstance",
    "in": "query",
    "required": false
   },
   {
    "name": "sourceModule",
    "in": "query",
    "required": false
   },
   {
    "name": "currentStatus",
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
 "resolveApprovedActionExecution": {
  "method": "POST",
  "path": "/approved-action-executions/{executionId}/resolve",
  "contract": "approvals",
  "summary": "Retry, investigate or escalate an approved action that failed",
  "permission": "APPROVAL_ACT",
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
  "requestBody": "ApprovedActionExecutionActionInput",
  "responds": "ApprovedActionExecutionView"
 },
 "resubmitApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/resubmit",
  "contract": "approvals",
  "summary": "Amend a rejected request and try again",
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
 "signApprovalDecision": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/signature",
  "contract": "approvals",
  "summary": "Sign a decision, so it can be proved later",
  "permission": "APPROVAL_DECIDE",
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
  "responds": "ApprovalSignature"
 },
 "withdrawApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/withdraw",
  "contract": "approvals",
  "summary": "The requester takes it back",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalControlPolicy": {
  "type": "object",
  "x-ticvai-persistence": "approvals.control_policy",
  "description": "Approvals boards 6.2 and 6.3. **Which decisions one person may not take alone** — distinct from which roles one person may not hold, which is `identity.setSegregationRules`.\n",
  "required": [
   "code",
   "control"
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
   "appliesToRequestKinds": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "appliesAboveValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "control": {
    "type": "string",
    "enum": [
     "fourEyes",
     "dualControl",
     "separationFromRequester",
     "separationFromExecutor"
    ],
    "description": "**`fourEyes` is two different people; `dualControl` is two people from different groups.** The second is stronger and is what a finance auditor means, and collapsing them makes the stronger control unexpressible.\n"
   },
   "requiredApproverGroupIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "minimumApprovers": {
    "type": "integer",
    "default": 2
   },
   "requiresStepUp": {
    "type": "boolean",
    "default": false
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false
   },
   "breakGlassAllowed": {
    "type": "boolean",
    "default": false,
    "description": "**Whether the control may be overridden in an emergency**, and if so it raises an alert rather than passing quietly. A control with no break-glass will be worked around by hand at three in the morning, which is worse.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
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
 "ApprovalRecord": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision_record",
  "description": "Approvals boards 4.10 and 6.6. **Tamper evidence, not tamper prevention** — each record chains to the one before it, so a changed entry breaks every hash after it.\n",
  "properties": {
   "requestId": {
    "type": "string",
    "format": "uuid"
   },
   "sequence": {
    "type": "integer"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decision": {
    "type": "string"
   },
   "decidedBy": {
    "type": "string",
    "format": "uuid"
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "policyVersions": {
    "type": "array",
    "description": "**What the rules were at the time**, because they have changed since.",
    "items": {
     "type": "object",
     "properties": {
      "policyId": {
       "type": "string",
       "format": "uuid"
      },
      "version": {
       "type": "integer"
      }
     }
    }
   },
   "payloadHash": {
    "type": "string"
   },
   "previousRecordHash": {
    "type": "string",
    "nullable": true
   },
   "recordHash": {
    "type": "string"
   },
   "signatures": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalSignature"
    }
   },
   "integrity": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "intact",
     "broken",
     "unverifiable"
    ],
    "description": "**Verified on read.** A tamper check nobody runs reports the breach years late."
   },
   "scopePath": {
    "type": "string"
   }
  }
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
   },
   "aiAssessment": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.",
    "properties": {
     "riskScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "riskBand": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high",
       "critical"
      ]
     },
     "priorityScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "escalationSuggestion": {
      "type": "object",
      "description": "A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.",
      "properties": {
       "action": {
        "type": "string",
        "enum": [
         "escalate",
         "addBackupApprover",
         "none"
        ]
       },
       "reason": {
        "type": "string",
        "nullable": true
       }
      }
     },
     "signals": {
      "type": "array",
      "maxItems": 10,
      "description": "The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.",
      "items": {
       "type": "object",
       "properties": {
        "code": {
         "type": "string"
        },
        "contribution": {
         "type": "number"
        },
        "detail": {
         "type": "string",
         "nullable": true
        }
       }
      }
     },
     "scoreId": {
      "type": "string",
      "format": "uuid",
      "description": "The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."
     },
     "decisionRecordId": {
      "type": "string",
      "description": "The ai decision record, for the audit of what the AI said and why."
     },
     "assessedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "ApprovalSignature": {
  "type": "object",
  "x-ticvai-persistence": "approvals.signature",
  "description": "Approvals board 6.5. **What is signed is the request as it stood at the moment of decision**, so a later edit breaks its own signature.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "requestId": {
    "type": "string",
    "format": "uuid"
   },
   "signedBy": {
    "type": "string",
    "format": "uuid"
   },
   "signedAt": {
    "type": "string",
    "format": "date-time"
   },
   "method": {
    "type": "string",
    "enum": [
     "platformKey",
     "uaePass",
     "externalCertificate",
     "drawnSignature"
    ]
   },
   "payloadHash": {
    "type": "string"
   },
   "signature": {
    "type": "string"
   },
   "certificateSubject": {
    "type": "string",
    "nullable": true
   },
   "stepUpVerified": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
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
 "ApprovedActionExecutionActionInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only (decided 29 September, VM close-out)",
  "description": "One action on an approved action whose execution failed (decided 29 September, VM close-out).",
  "required": [
   "action"
  ],
  "properties": {
   "action": {
    "type": "string",
    "enum": [
     "retry",
     "investigate",
     "escalate"
    ]
   },
   "assigneeId": {
    "type": "string",
    "format": "uuid",
    "description": "Required for investigate and escalate"
   },
   "note": {
    "type": "string",
    "maxLength": 500
   }
  }
 },
 "ApprovedActionExecutionView": {
  "type": "object",
  "x-ticvai-persistence": "approvals.approved_action_execution",
  "description": "**One approved action and whether it ran** (decided 29 September, VM close-out). Written when a request is approved and updated by the requesting contract as it executes; the approval request itself stays immutable (11.1.56).",
  "required": [
   "id",
   "approvalRequestId",
   "sourceModule",
   "actionType",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid"
   },
   "sourceModule": {
    "type": "string",
    "description": "The contract that owns and executes the action"
   },
   "actionType": {
    "type": "string",
    "description": "What was approved, e.g. refund, price change"
   },
   "subjectRef": {
    "type": "string",
    "description": "The record the action applies to"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "executing",
     "succeeded",
     "failed",
     "investigating",
     "escalated"
    ]
   },
   "attempts": {
    "type": "integer",
    "minimum": 0
   },
   "lastAttemptAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "failureReason": {
    "type": "string",
    "nullable": true
   },
   "assigneeId": {
    "type": "string",
    "nullable": true
   },
   "lastAction": {
    "type": "string",
    "enum": [
     "retry",
     "investigate",
     "escalate"
    ],
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005). Written at venue scope"
   }
  }
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
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
 "StepUpPolicy": {
  "x-ticvai-persistence": "approvals.step_up_policy",
  "type": "object",
  "required": [
   "operationId",
   "required"
  ],
  "properties": {
   "operationId": {
    "type": "string",
    "description": "The action governed. Names an operation, never a screen."
   },
   "required": {
    "allOf": [
     {
      "$ref": "#/components/schemas/StepUpStrength"
     }
    ],
    "description": "The strength in force at this scope."
   },
   "contractFloor": {
    "allOf": [
     {
      "$ref": "#/components/schemas/StepUpStrength"
     }
    ],
    "description": "What `x-ticvai-step-up` sets on the operation. Read only, and the value `required` may not go below.\n"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ],
    "description": "Where this rule was set, not where it applies."
   },
   "reason": {
    "type": "string",
    "maxLength": 512,
    "description": "Why it was raised. **An unexplained control is one somebody removes** the first time it is inconvenient.\n"
   },
   "setBy": {
    "type": "string",
    "format": "uuid"
   },
   "setAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "StepUpStrength": {
  "type": "string",
  "description": "**Ordered, weakest first, and that ordering is what makes *raise only* checkable.** `pin` is a supervisor PIN captured in place — `roles.yaml` already resolves escalation that way and it is right for an action taken several times a shift. `mfa` is a challenge against an enrolled method and is right for an action taken a few times a month.\n",
  "enum": [
   "none",
   "pin",
   "mfa"
  ]
 },
 "WorkflowInstanceMonitorProcessTimelineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_instance and approvals.workflow_step_execution (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Instance Monitor & Process Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowInstance": {
    "type": "string",
    "description": "Workflow Instance"
   },
   "workflowName": {
    "type": "string",
    "description": "Workflow Name"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "sourceModule": {
    "type": "string",
    "description": "Source Module"
   },
   "businessObject": {
    "type": "string",
    "description": "Business Object"
   },
   "initiatedBy": {
    "type": "string",
    "description": "Initiated By"
   },
   "startTime": {
    "type": "string",
    "format": "date-time",
    "description": "Start Time"
   },
   "currentStatus": {
    "type": "string",
    "enum": [
     "running",
     "waitingApproval",
     "waitingTask",
     "waitingSystem",
     "escalated",
     "failed",
     "completed",
     "cancelled"
    ],
    "description": "Current Status"
   },
   "currentStep": {
    "type": "string",
    "description": "Current Step"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "step": {
    "type": "string",
    "description": "Step"
   },
   "type": {
    "type": "string",
    "description": "Type"
   },
   "started": {
    "type": "string",
    "format": "date-time",
    "description": "Started"
   },
   "completed": {
    "type": "string",
    "format": "date-time",
    "description": "Completed"
   },
   "assignedTo": {
    "type": "string",
    "description": "Assigned To"
   },
   "input": {
    "type": "string",
    "description": "Input"
   },
   "output": {
    "type": "string",
    "description": "Output"
   },
   "decision": {
    "type": "string",
    "description": "Decision"
   },
   "duration": {
    "type": "integer",
    "description": "Seconds"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "ruleEvaluations": {
    "type": "integer",
    "description": "Rule evaluations"
   },
   "assignments": {
    "type": "integer",
    "description": "Assignments"
   },
   "approvals": {
    "type": "integer",
    "description": "Approvals"
   },
   "rejections": {
    "type": "integer",
    "description": "Rejections"
   },
   "escalations": {
    "type": "integer",
    "description": "Escalations"
   },
   "notifications": {
    "type": "integer",
    "description": "Notifications"
   },
   "apiCalls": {
    "type": "integer",
    "description": "API calls"
   },
   "systemActions": {
    "type": "integer",
    "description": "System actions"
   },
   "errors": {
    "type": "integer",
    "description": "Errors"
   }
  },
  "required": [
   "workflowInstance"
  ]
 }
}
```
