# WS13 — Approval Workflows and Governance board 1

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
| `BO-364` | Approval Command Center Dashboard | listDetail | 0 | 0 | — |
| `BO-365` | My Approval Inbox | listDetail | 0 | 0 | — |
| `BO-366` | Team / Shared Approval Queue | listDetail | 0 | 0 | — |
| `BO-367` | Approval Request Detail | listDetail | 0 | 0 | — |
| `BO-368` | AI Decision Support | listDetail | 0 | 0 | — |
| `BO-369` | High Priority & Risk Queue | listDetail | 0 | 0 | — |
| `BO-370` | Escalated Approval Center | listDetail | 0 | 0 | — |
| `BO-371` | Completed Approval History | listDetail | 0 | 0 | — |
| `BO-372` | Approval SLA & Workload Monitor | commandCentre | 0 | 0 | — |
| `BO-373` | Approval Activity & Notification Center | listDetail | 0 | 0 | — |

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
  "apis": [],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-364"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 3. 0 of 20 labels bound to a contract property; 20 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "BO-368",
     "trigger": "AI Decision Support",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "BO-369",
     "trigger": "High Priority & Risk Queue",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
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
  "apis": [],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-365"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 4. 0 of 11 labels bound to a contract property; 11 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-366"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-367"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-368"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-369"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 5 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "entryState": {
   "preloaded": [
    "Original approver",
    "Current approver",
    "Escalation level",
    "Escalation reason",
    "Time waiting",
    "SLA status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-370"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 8. 0 of 8 labels bound to a contract property; 8 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-371"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 8. 0 of 11 labels bound to a contract property; 11 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-372"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 4 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-373"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
