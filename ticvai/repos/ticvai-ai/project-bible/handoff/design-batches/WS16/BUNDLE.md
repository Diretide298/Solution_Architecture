# WS16 — Approval Workflows and Governance board 4

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
| `BO-374` | Approval Decision Workspace | listDetail | 0 | 0 | — |
| `BO-375` | Business Context & Evidence Viewer | listDetail | 0 | 0 | — |
| `BO-376` | Approval Timeline & Decision Chain | listDetail | 0 | 0 | — |
| `BO-377` | Approve & Sensitive Action Confirmation | listDetail | 0 | 0 | — |
| `BO-378` | Reject / Return / Request Information | listDetail | 0 | 0 | — |
| `BO-379` | Requester Modification & Resubmission | listDetail | 0 | 0 | — |
| `BO-380` | Withdrawal, Cancellation, Expiration & Reopening | listDetail | 0 | 0 | — |
| `BO-381` | Segregation of Duties & Four-Eyes Control | listDetail | 0 | 0 | — |
| `BO-382` | Approved Action Execution & Status | listDetail | 0 | 0 | — |
| `BO-383` | Decision Record & Immutable Audit View | listDetail | 0 | 0 | — |

## Thin screens in this batch

**BO-374, BO-375, BO-376, BO-377, BO-378, BO-379, BO-380, BO-381, BO-382, BO-383 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-374"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-375"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "entryState": {
   "preloaded": [
    "Request created",
    "Workflow triggered",
    "Routing decision",
    "Assignment",
    "Reassignment",
    "Delegation"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-376"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 33. 0 of 12 labels bound to a contract property; 12 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-377"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-378"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-379"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 35. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-380"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 36. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-381"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 36. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Separate approval of the request from execution of the underlying business transaction. This distinction is extremely important. An approval being completed does not automatically mean the underlying transaction executed successfully.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Retry | Investigate | Escalate. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 37 §Actions"
   },
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
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 37 §Actions"
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
   "loading": "The approved action execution list.",
   "error": "Could not load. Names which read failed and leaves the approved action execution untouched.",
   "emptyFirstRun": "No approved action execution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approved action execution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-382"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 1 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "components": []
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-383"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
