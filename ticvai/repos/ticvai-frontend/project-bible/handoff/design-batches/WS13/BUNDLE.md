# WS13 — Approval Workflows and Governance board 1

**10 screens · 9 operations · 16 schemas · 3 permissions**

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
  `APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-364` | Approval Command Center Dashboard | listDetail | 2 | 0 | — |
| `BO-365` | My Approval Inbox | listDetail | 1 | 0 | — |
| `BO-366` | Team / Shared Approval Queue | listDetail | 1 | 0 | — |
| `BO-367` | Approval Request Detail | listDetail | 3 | 0 | — |
| `BO-368` | AI Decision Support | listDetail | 2 | 0 | — |
| `BO-369` | High Priority & Risk Queue | listDetail | 2 | 0 | — |
| `BO-370` | Escalated Approval Center | listDetail | 2 | 0 | — |
| `BO-371` | Completed Approval History | listDetail | 1 | 0 | — |
| `BO-372` | Approval SLA & Workload Monitor | commandCentre | 2 | 0 | — |
| `BO-373` | Approval Activity & Notification Center | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-364, BO-365, BO-366, BO-367, BO-368, BO-369, BO-370, BO-371, BO-373 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-364",
  "name": "Approval Command Center Dashboard",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "1",
   "page": 3
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/approval-command-center-dashboard-bo-364",
   "component": "apps/venue-management-web/src/routes/venue-operations/ApprovalCommandCenterDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-365",
    "BO-366",
    "BO-367",
    "BO-368",
    "BO-369",
    "BO-370",
    "BO-371",
    "BO-372",
    "BO-373"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "BO-373",
     "trigger": "Approval Activity & Notification Center",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "BO-365",
     "trigger": "My Approval Inbox",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "BO-366",
     "trigger": "Team / Shared Approval Queue",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "BO-367",
     "trigger": "Approval Request Detail",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "carries": [
      "approvalRequestId"
     ]
    },
    {
     "to": "BO-368",
     "trigger": "AI Decision Support",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "BO-369",
     "trigger": "High Priority & Risk Queue",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "carries": [
      "approvalRequestId"
     ]
    },
    {
     "to": "BO-370",
     "trigger": "Escalated Approval Center",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "BO-371",
     "trigger": "Completed Approval History",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "BO-372",
     "trigger": "Approval SLA & Workload Monitor",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Key Functions) and no metric row",
  "purpose": "Provide management and approvers with a real-time overview of approval activity.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 3 §Key Functions"
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
       "label": "Every approval",
       "columns": [
        "Pending approvals",
        "Awaiting my approval",
        "Approved today",
        "Rejected",
        "Escalated",
        "SLA breached",
        "High-risk requests",
        "AI-prioritized requests",
        "Average approval time",
        "Approval volume",
        "Approval trend",
        "o Tenant",
        "o Venue",
        "o Department",
        "o Module",
        "o Request type",
        "o Priority",
        "o Risk",
        "o Status",
        "o Date"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 3 §Key Functions"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval",
       "bindsTo": null,
       "columns": [
        "Pending approvals",
        "Awaiting my approval",
        "Approved today",
        "Rejected",
        "Escalated",
        "SLA breached",
        "High-risk requests",
        "AI-prioritized requests",
        "Average approval time",
        "Approval volume",
        "Approval trend",
        "o Tenant",
        "o Venue",
        "o Department",
        "o Module",
        "o Request type",
        "o Priority",
        "o Risk",
        "o Status",
        "o Date"
       ],
       "notes": null,
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 3 §Key Functions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval list.",
   "error": "Could not load. Names which read failed and leaves the approval untouched.",
   "emptyFirstRun": "No approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Volume, outcome and SLA",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "What is waiting",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Pending approvals",
    "Awaiting my approval",
    "Approved today",
    "Rejected",
    "Escalated",
    "SLA breached"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-364",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-364"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 3. 0 of 20 labels bound to a contract property; 20 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-365",
  "name": "My Approval Inbox",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "2",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/my-approval-inbox-bo-365",
   "component": "apps/venue-management-web/src/routes/venue-operations/MyApprovalInbox.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-364"
   ],
   "exitTo": [
    "BO-364"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Back to Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide each approver with their personal actionable queue.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 4 §Display"
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
       "label": "Every approval",
       "columns": [
        "Request ID",
        "Request type",
        "Requested by",
        "Venue",
        "Department",
        "Requested value",
        "Submitted time",
        "SLA remaining",
        "Risk level",
        "Priority",
        "Current approval stage"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 4 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval",
       "bindsTo": null,
       "columns": [
        "Request ID",
        "Request type",
        "Requested by",
        "Venue",
        "Department",
        "Requested value",
        "Submitted time",
        "SLA remaining",
        "Risk level",
        "Priority",
        "Current approval stage"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Tabs”.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 4 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval list.",
   "error": "Could not load. Names which read failed and leaves the approval untouched.",
   "emptyFirstRun": "No approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "Mine to decide",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Request ID",
    "Request type",
    "Requested by",
    "Venue",
    "Department",
    "Requested value"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-365",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-365"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 4. 0 of 11 labels bound to a contract property; 11 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-366",
  "name": "Team / Shared Approval Queue",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "3",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/team-shared-approval-queue-bo-366",
   "component": "apps/venue-management-web/src/routes/venue-operations/TeamSharedApprovalQueue.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-364"
   ],
   "exitTo": [
    "BO-364"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Back to Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow managers and centralized approval teams to manage approvals belonging to their team or department.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 5"
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
   "loading": "The team shared approval list.",
   "error": "Could not load. Names which read failed and leaves the team shared approval untouched.",
   "emptyFirstRun": "No team shared approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the team shared approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "The shared queue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-366",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-366"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-367",
  "name": "Approval Request Detail",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "4",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/approval-request-detail-bo-367",
   "component": "apps/venue-management-web/src/routes/venue-operations/ApprovalRequestDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-364"
   ],
   "exitTo": [
    "BO-364"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Back to Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Approval Request Detail",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 6"
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "decideApprovalRequest",
       "notes": "The act the screen exists for."
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
   "loading": "The approval request detail list.",
   "error": "Could not load. Names which read failed and leaves the approval request detail untouched.",
   "emptyFirstRun": "No approval request detail yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval request detail are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "The request",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Approve or reject",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalRequests",
     "getApprovalRecord",
     "getApprovalAnalytics"
    ]
   },
   {
    "operationId": "getApprovalRequestScore",
    "contract": "ai",
    "purpose": "Risk band, priority and suggested escalation for the request, as context only (no approve/reject suggestion)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-367",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-367"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "requestId",
     "from": "navigation"
    },
    {
     "name": "approvalRequestId",
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
  "id": "BO-368",
  "name": "AI Decision Support",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "5",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/ai-decision-support-bo-368",
   "component": "apps/venue-management-web/src/routes/venue-operations/AiDecisionSupport.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-364"
   ],
   "exitTo": [
    "BO-364"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Back to Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "AI Decision Support",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 6"
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
       "impliedBy": "evaluateApprovalRequirement",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "evaluateApprovalRequirement"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The decision support list.",
   "error": "Could not load. Names which read failed and leaves the decision support untouched.",
   "emptyFirstRun": "No decision support yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the decision support are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "evaluateApprovalRequirement",
    "contract": "approvals",
    "purpose": "What the rules say",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "Requests with their AI context (aiAssessment: risk, priority, escalation suggestion) for the reviewer; context only",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-368",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-368"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-369",
  "name": "High Priority & Risk Queue",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "6",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/high-priority-risk-queue-bo-369",
   "component": "apps/venue-management-web/src/routes/venue-operations/HighPriorityRiskQueue.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-364"
   ],
   "exitTo": [
    "BO-364"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Back to Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a dedicated operational screen for approvals requiring immediate attention.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 7"
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
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getApprovalRequestScore",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The high priority risk list.",
   "error": "Could not load. Names which read failed and leaves the high priority risk untouched.",
   "emptyFirstRun": "No high priority risk yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the high priority risk are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "High priority and risk",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getApprovalRequestScore",
    "contract": "ai",
    "purpose": "Risk band, priority and suggested escalation for the request, as context only (no approve/reject suggestion)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-369",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-369"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 5 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "approvalRequestId",
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
  "id": "BO-370",
  "name": "Escalated Approval Center",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "7",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/escalated-approval-center-bo-370",
   "component": "apps/venue-management-web/src/routes/venue-operations/EscalatedApprovalCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-364"
   ],
   "exitTo": [
    "BO-364"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Back to Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage requests that were escalated because of SLA breaches, risk conditions, unavailable approvers or configured escalation rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 8 §Display"
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
       "label": "Every escalated approval",
       "columns": [
        "Original approver",
        "Current approver",
        "Escalation level",
        "Escalation reason",
        "Time waiting",
        "SLA status",
        "Previous actions",
        "Next escalation level"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 8 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected escalated approval",
       "bindsTo": null,
       "columns": [
        "Original approver",
        "Current approver",
        "Escalation level",
        "Escalation reason",
        "Time waiting",
        "SLA status",
        "Previous actions",
        "Next escalation level"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Escalation Timeline”.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 8 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The escalated approval list.",
   "error": "Could not load. Names which read failed and leaves the escalated approval untouched.",
   "emptyFirstRun": "No escalated approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the escalated approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSlaEscalationBottleneck",
    "contract": "approvals",
    "purpose": "What escalated and why",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "escalateApprovalRequest",
    "contract": "approvals",
    "purpose": "Escalate",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalRequests",
     "listSlaEscalationBottleneck"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Original approver",
    "Current approver",
    "Escalation level",
    "Escalation reason",
    "Time waiting",
    "SLA status"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-370",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-370"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 8. 0 of 8 labels bound to a contract property; 8 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-371",
  "name": "Completed Approval History",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "8",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/completed-approval-history-bo-371",
   "component": "apps/venue-management-web/src/routes/venue-operations/CompletedApprovalHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-364"
   ],
   "exitTo": [
    "BO-364"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Back to Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide searchable historical records of completed approval decisions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 8"
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
       "label": "Search completed approval history",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 8 §Search By"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Request ID",
        "Transaction",
        "Customer",
        "Requester",
        "Approver",
        "Venue",
        "Department",
        "Module",
        "Date",
        "Decision",
        "Approval amount"
       ],
       "notes": "The pack filters this screen by request id, transaction, customer, requester, approver, venue and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 8 §Search By"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The completed approval history list.",
   "error": "Could not load. Names which read failed and leaves the completed approval history untouched.",
   "emptyFirstRun": "No completed approval history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the completed approval history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "Completed history",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-371",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-371"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 8. 0 of 11 labels bound to a contract property; 11 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-372",
  "name": "Approval SLA & Workload Monitor",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "9",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/approval-sla-workload-monitor-bo-372",
   "component": "apps/venue-management-web/src/routes/venue-operations/ApprovalSlaWorkloadMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-364"
   ],
   "exitTo": [
    "BO-364"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Back to Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Give managers visibility into operational performance before approvals become bottlenecks.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Within SLA — 92%",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 9 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "At Risk — 17",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 9 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Breached — 6",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 9 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Approval — 34 min",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 9 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval sla workload list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the approval sla workload untouched.",
   "emptyFirstRun": "No approval sla workload yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval sla workload are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSlaEscalationReminder",
    "contract": "approvals",
    "purpose": "SLA and workload",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Where the time goes",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Within SLA — 92%",
    "At Risk — 17",
    "Breached — 6",
    "Average Approval — 34 min"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-372",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-372"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 4 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-373",
  "name": "Approval Activity & Notification Center",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "1",
   "number": "10",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/approval-activity-notification-center-bo-373",
   "component": "apps/venue-management-web/src/routes/venue-operations/ApprovalActivityNotificationCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-364"
   ],
   "exitTo": [
    "BO-364"
   ],
   "transitions": [
    {
     "to": "BO-364",
     "trigger": "Back to Approval Command Center Dashboard",
     "provenance": "structural — pack board 1 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a unified chronological feed of important approval events.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 9"
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
       "impliedBy": "listWorkflowInstanceProcess",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval activity notification list.",
   "error": "Could not load. Names which read failed and leaves the approval activity notification untouched.",
   "emptyFirstRun": "No approval activity notification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval activity notification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkflowInstanceProcess",
    "contract": "approvals",
    "purpose": "Activity across workflows",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-373",
   "workshopBoard": "wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-373"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "evaluateApprovalRequirement": {
  "method": "POST",
  "path": "/approval-requests/evaluate",
  "contract": "approvals",
  "summary": "Does this need approval, and from whom",
  "permission": "APPROVAL_VIEW",
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
  "responds": "ApprovalRequirement"
 },
 "getApprovalAnalytics": {
  "method": "GET",
  "path": "/approval-analytics",
  "contract": "approvals",
  "summary": "Volumes, times, rejections and bottlenecks",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ApprovalAnalytics"
 },
 "getApprovalRequestScore": {
  "method": "GET",
  "path": "/approval-requests/{approvalRequestId}/score",
  "contract": "ai",
  "summary": "The latest context score of an approval request",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiApprovalRequestScore"
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
 "listSlaEscalationBottleneck": {
  "method": "GET",
  "path": "/sla-escalation-bottleneck",
  "contract": "approvals",
  "summary": "SLA, Escalation & Bottleneck Monitor",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workflow",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
    "in": "query",
    "required": false
   },
   {
    "name": "escalationLevel",
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
 "listSlaEscalationReminder": {
  "method": "GET",
  "path": "/sla-escalation-reminder",
  "contract": "approvals",
  "summary": "SLA, Escalation, Reminder & Timeout Rules",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SlaEscalationReminderTimeoutRulesView"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiApprovalRequestScore": {
  "type": "object",
  "x-ticvai-persistence": "ai.approval_request_score",
  "description": "**Context for an approval reviewer** (11.1.73..75): risk, priority and a suggested escalation for one pending request, the latest per request. **There is no approve or reject field, by design** (minutes of 8 September: AI in approvals never recommends or influences approve or reject).",
  "required": [
   "approvalRequestId",
   "riskScore",
   "riskBand",
   "priorityScore",
   "escalationSuggestion"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "approvals.request"
   },
   "trigger": {
    "type": "string",
    "enum": [
     "submitted",
     "resubmitted",
     "slaTick",
     "escalated"
    ]
   },
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
    ],
    "description": "Design 5.6: a risk score and band, never a probability."
   },
   "priorityScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "description": "For ordering work in an inbox; higher first."
   },
   "escalationSuggestion": {
    "type": "object",
    "required": [
     "action"
    ],
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
    },
    "description": "A suggestion for an SLA problem, carried out if at all by a person or the tenant's SLA policy."
   },
   "signals": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "description": "e.g. `amountAboveRequesterNorm`, `requesterEntityRisk`, `outOfHours`, `irreversibleAction`, `slaDueSoon`, `stepBreachRate`, `approverUnavailable`."
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
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scoredAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "ApprovalAnalytics": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from approvals.request",
  "properties": {
   "from": {
    "type": "string",
    "format": "date"
   },
   "to": {
    "type": "string",
    "format": "date"
   },
   "groupBy": {
    "type": "string",
    "description": "The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it.",
    "enum": [
     "kind",
     "approver",
     "venue",
     "day",
     "week"
    ]
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "raised": {
       "type": "integer"
      },
      "approved": {
       "type": "integer"
      },
      "rejected": {
       "type": "integer"
      },
      "withdrawn": {
       "type": "integer"
      },
      "expired": {
       "type": "integer",
       "description": "**Requests nobody answered.** Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person.\n"
      },
      "escalated": {
       "type": "integer"
      },
      "slaBreached": {
       "type": "integer"
      },
      "medianMinutes": {
       "type": "number"
      },
      "p95Minutes": {
       "type": "number"
      }
     }
    }
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
 "ApprovalRequirement": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "description": "The answer to \"does this need approval\", returned before the action.",
  "required": [
   "isRequired"
  ],
  "properties": {
   "isRequired": {
    "type": "boolean"
   },
   "matchedRule": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ApprovalRule"
     }
    ],
    "nullable": true
   },
   "matrixVersion": {
    "type": "integer",
    "nullable": true
   },
   "approvers": {
    "type": "array",
    "description": "Resolved, with delegations applied. **Named so the caller can say \"this needs Sara\"** rather than \"this needs approval\".\n",
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
      "level": {
       "type": "integer"
      },
      "isDelegate": {
       "type": "boolean"
      },
      "delegatedFrom": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true
   },
   "noApproverAvailable": {
    "type": "boolean",
    "description": "**The case that must not fail silently.** A rule requiring a role nobody at this venue holds means the action is blocked forever, and the caller needs to know that now rather than after raising a request nobody can decide.\n"
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
    "description": "11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"
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
   },
   "externalProviderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"
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
 "SlaEscalationBottleneckMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_instance, whose SLA and reminder timestamps it lists (data model for the agreed operations, 29 September)",
  "description": "**What SLA, Escalation & Bottleneck Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflow": {
    "type": "string",
    "description": "Workflow"
   },
   "instance": {
    "type": "string",
    "description": "Instance"
   },
   "currentStep": {
    "type": "string",
    "description": "Current Step"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "started": {
    "type": "string",
    "format": "date-time",
    "description": "Started"
   },
   "target": {
    "type": "string",
    "format": "date-time",
    "description": "SLA deadline"
   },
   "timeRemaining": {
    "type": "integer",
    "description": "Minutes until breach; negative once breached"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "escalationLevel": {
    "type": "string",
    "description": "Escalation Level"
   },
   "firstReminder": {
    "type": "string",
    "format": "date-time",
    "description": "First Reminder"
   },
   "secondReminder": {
    "type": "string",
    "format": "date-time",
    "description": "Second Reminder"
   },
   "managerEscalation": {
    "type": "string",
    "format": "date-time",
    "description": "Manager Escalation"
   },
   "executiveEscalation": {
    "type": "string",
    "format": "date-time",
    "description": "Executive Escalation"
   },
   "finalOutcome": {
    "type": "string",
    "description": "Final Outcome"
   }
  },
  "required": [
   "instance"
  ]
 },
 "SlaEscalationBottleneckMonitorViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "withinSla": {
    "type": "integer",
    "description": "Within SLA"
   },
   "atRisk": {
    "type": "integer",
    "description": "At Risk"
   },
   "breached": {
    "type": "integer",
    "description": "Breached"
   },
   "escalated": {
    "type": "integer",
    "description": "Escalated"
   },
   "averageProcessingTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "averageApprovalTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "longestWaitingStep": {
    "type": "string",
    "description": "Longest Waiting Step"
   }
  }
 },
 "SlaEscalationReminderTimeoutRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.sla_policy (schema ApprovalSlaPolicy), including its reminder-percentage columns (data model for the agreed operations, 29 September)",
  "description": "**What SLA, Escalation, Reminder & Timeout Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "code": {
    "type": "string",
    "description": "Policy code, the same key setApprovalSlaPolicy upserts by"
   },
   "slaType": {
    "type": "string",
    "enum": [
     "responseSla",
     "approvalSla",
     "taskSla",
     "resolutionSla",
     "systemActionTimeout"
    ],
    "description": "Which clock this policy governs"
   },
   "calendarBasis": {
    "type": "string",
    "enum": [
     "calendarHours",
     "businessHours",
     "workingDays",
     "venueCalendar",
     "holidayCalendar"
    ],
    "description": "How elapsed time is counted"
   },
   "escalationActions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "notify",
      "reassign",
      "escalate",
      "addApprover",
      "createTask",
      "raisePriority",
      "triggerBackupWorkflow"
     ]
    },
    "description": "What happens on escalation"
   },
   "channelsType": {
    "type": "string",
    "enum": [
     "email",
     "push",
     "inApp",
     "smsWhereAppropriate"
    ],
    "description": "Vocabulary listed under Reminder Channels."
   },
   "targetMinutes": {
    "type": "integer",
    "description": "SLA target in minutes"
   },
   "onBreach": {
    "type": "string",
    "enum": [
     "notifyOnly",
     "escalate",
     "autoApprove",
     "autoReject"
    ],
    "description": "Outcome at breach; auto outcomes only where explicitly permitted"
   },
   "autoActionAllowed": {
    "type": "boolean",
    "description": "Auto-approve or auto-reject on breach is explicitly permitted; default false"
   },
   "firstReminderAtPercent": {
    "type": "integer",
    "description": "Percent of target at which the first reminder goes"
   },
   "secondReminderAtPercent": {
    "type": "integer",
    "description": "Percent of target at which the second reminder goes"
   },
   "escalateAtPercent": {
    "type": "integer",
    "description": "Percent of target at which the request escalates"
   }
  },
  "required": [
   "code"
  ]
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
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
