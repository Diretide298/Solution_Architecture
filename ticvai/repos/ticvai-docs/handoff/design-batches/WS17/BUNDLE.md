# WS17 — Approval Workflows and Governance board 5

**10 screens · 11 operations · 18 schemas · 6 permissions**

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
  `APPROVAL_ACT, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW, GUEST_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-384` | Delegation & Escalation Command Center | commandCentre | 3 | 1 | — |
| `BO-385` | Delegation Management | configEditor | 4 | 0 | — |
| `BO-386` | Temporary Delegation & Availability Calendar | listDetail | 2 | 0 | — |
| `BO-387` | Out-of-Office & Substitute Routing | configEditor | 1 | 0 | — |
| `BO-388` | Approval SLA Policy Configuration | configEditor | 1 | 0 | — |
| `BO-389` | Reminder & Breach Notification Rules | listDetail | 1 | 0 | — |
| `BO-390` | Escalation Policy Builder | listDetail | 1 | 0 | — |
| `BO-391` | Live Escalation Operations Center | listDetail | 2 | 1 | — |
| `BO-392` | SLA & Escalation Performance Analytics | listDetail | 1 | 0 | — |
| `BO-393` | AI SLA & Escalation Advisor | listDetail | 3 | 0 | — |

## Thin screens in this batch

**BO-385, BO-386, BO-389, BO-390, BO-391, BO-392 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-384",
  "name": "Delegation & Escalation Command Center",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "1",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/delegation-escalation-command-center-bo-384",
   "component": "apps/venue-management-web/src/routes/venue-operations/DelegationEscalationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-385",
    "BO-386",
    "BO-387",
    "BO-388",
    "BO-389",
    "BO-390",
    "BO-391",
    "BO-392",
    "BO-393"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "BO-393",
     "trigger": "AI SLA & Escalation Advisor",
     "provenance": "structural — pack board 5 wiring, 9 September 2026"
    },
    {
     "to": "BO-385",
     "trigger": "Delegation Management",
     "provenance": "structural — pack board 5 wiring, 9 September 2026"
    },
    {
     "to": "BO-386",
     "trigger": "Temporary Delegation & Availability Calendar",
     "provenance": "structural — pack board 5 wiring, 9 September 2026"
    },
    {
     "to": "BO-387",
     "trigger": "Out-of-Office & Substitute Routing",
     "provenance": "structural — pack board 5 wiring, 9 September 2026"
    },
    {
     "to": "BO-388",
     "trigger": "Approval SLA Policy Configuration",
     "provenance": "structural — pack board 5 wiring, 9 September 2026"
    },
    {
     "to": "BO-389",
     "trigger": "Reminder & Breach Notification Rules",
     "provenance": "structural — pack board 5 wiring, 9 September 2026"
    },
    {
     "to": "BO-390",
     "trigger": "Escalation Policy Builder",
     "provenance": "structural — pack board 5 wiring, 9 September 2026"
    },
    {
     "to": "BO-391",
     "trigger": "Live Escalation Operations Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "carries": [
      "instanceId"
     ]
    },
    {
     "to": "BO-392",
     "trigger": "SLA & Escalation Performance Analytics",
     "provenance": "structural — pack board 5 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide administrators and managers with a real-time overview of delegation, SLA and escalation conditions across TICVAI.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Delegations",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 40 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Approvers Unavailable",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 40 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approvals",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 40 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "SLA At Risk",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 40 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "SLA Breached",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 40 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Escalated Today",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 40 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Unassigned Requests",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 40 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Critical Escalations",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 40 §KPI Cards"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Act on workflow instance",
       "operation": "actOnWorkflowInstance",
       "permission": "APPROVAL_ACT",
       "notes": "**The monitors' action buttons, as one operation** (decided 29 September, writers pass).",
       "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The delegation escalation list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the delegation escalation untouched.",
   "emptyFirstRun": "No delegation escalation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the delegation escalation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalDelegations",
    "contract": "approvals",
    "purpose": "Delegations in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSlaEscalationBottleneck",
    "contract": "approvals",
    "purpose": "Live escalations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "actOnWorkflowInstance",
    "contract": "approvals",
    "purpose": "An operator's intervention in a running workflow",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalDelegations",
     "listSlaEscalationBottleneck"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Active Delegations",
    "Approvers Unavailable",
    "Pending Approvals",
    "SLA At Risk",
    "SLA Breached",
    "Escalated Today"
   ],
   "params": [
    {
     "name": "instanceId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-384",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-384"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 40. 0 of 0 labels bound to a contract property; 8 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formActOnWorkflowInstance",
    "component": "modal",
    "trigger": "Act on workflow instance",
    "body": "**Collects what `actOnWorkflowInstance` sends before it is called.** Required: `action`, `reason`. Optional: `workflowStepExecutionId`, `workflowExceptionId`, `assigneePrincipalId`, `alternativeNodeId`, `correctedInput`, `extendByMinutes`, `priority`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "WorkflowInstanceActionInput",
    "confirm": {
     "label": "Act on workflow instance",
     "operation": "actOnWorkflowInstance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "reason",
      "workflowStepExecutionId",
      "workflowExceptionId",
      "assigneePrincipalId",
      "alternativeNodeId",
      "correctedInput",
      "extendByMinutes",
      "priority"
     ]
    },
    "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
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
  "id": "BO-385",
  "name": "Delegation Management",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "2",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/delegation-management-bo-385",
   "component": "apps/venue-management-web/src/routes/venue-operations/DelegationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-384"
   ],
   "exitTo": [
    "BO-384"
   ],
   "transitions": [
    {
     "to": "BO-384",
     "trigger": "Back to Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Delegation Setup) and no display directory — it is settings, not a population",
  "purpose": "Allow an authorized approver or administrator to delegate approval authority to another eligible user. The source specifically requires approvers to be able to delegate their approval authority.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Delegator: Ahmed Raza",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 41 §Delegation Setup"
      },
      {
       "kind": "textField",
       "label": "Delegate To: Sara Khan",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 41 §Delegation Setup"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save Draft | Activate Delegation | Cancel",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 41 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The delegation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the delegation untouched.",
   "emptyFirstRun": "No delegation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDelegations",
    "contract": "identity",
    "purpose": "Who may act for this guest, and for whom they may act",
    "trigger": "onAction"
   },
   {
    "operationId": "createApprovalDelegation",
    "contract": "approvals",
    "purpose": "Save or activate an approval delegation",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Save Draft | Activate Delegation | Cancel"
   },
   {
    "operationId": "listApprovalDelegations",
    "contract": "approvals",
    "purpose": "List approval delegations (screen currently binds guest delegations)",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Save Draft | Activate Delegation | Cancel"
   },
   {
    "operationId": "revokeApprovalDelegation",
    "contract": "approvals",
    "purpose": "Cancel an active delegation",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Save Draft | Activate Delegation | Cancel",
    "invalidates": [
     "listApprovalDelegations"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-385",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-385"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 41. 0 of 0 labels bound to a contract property; 3 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Save Draft | Activate Delegation | Cancel: `createApprovalDelegation`.",
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "navigation"
    },
    {
     "name": "delegationId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that list — never an empty form that looks configurable."
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
  "id": "BO-386",
  "name": "Temporary Delegation & Availability Calendar",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "3",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/temporary-delegation-availability-calendar-bo-386",
   "component": "apps/venue-management-web/src/routes/venue-operations/TemporaryDelegationAvailabilityCalendar.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-384"
   ],
   "exitTo": [
    "BO-384"
   ],
   "transitions": [
    {
     "to": "BO-384",
     "trigger": "Back to Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage time-limited delegation caused by annual leave, business travel, training, sickness, or other planned absence. The matrix requires temporary delegation periods with automatic expiration.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 42"
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
       "impliedBy": "setApproverAvailability",
       "label": "Save approver availability",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listApprovalDelegations",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApproverAvailability"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The temporary delegation availability list.",
   "error": "Could not load. Names which read failed and leaves the temporary delegation availability untouched.",
   "emptyFirstRun": "No temporary delegation availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the temporary delegation availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApproverAvailability",
    "contract": "approvals",
    "purpose": "Dated, so nobody forgets to turn it off",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalDelegations"
    ]
   },
   {
    "operationId": "listApprovalDelegations",
    "contract": "approvals",
    "purpose": "Existing delegations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-386",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-386"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 4 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-387",
  "name": "Out-of-Office & Substitute Routing",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "4",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/out-of-office-substitute-routing-bo-387",
   "component": "apps/venue-management-web/src/routes/venue-operations/OutOfOfficeSubstituteRouting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-384"
   ],
   "exitTo": [
    "BO-384"
   ],
   "transitions": [
    {
     "to": "BO-384",
     "trigger": "Back to Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure automatic routing when the primary approver is unavailable. The matrix specifically requires automatic rerouting when approvers are unavailable.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Immediate rerouting",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wait X minutes",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Route to deputy",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Route to manager",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "textField",
       "label": "Route to shared queue",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Escalate",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "textField",
       "label": "Keep original approver informed",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The out-of-office substitute routing configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the out-of-office substitute routing untouched.",
   "emptyFirstRun": "No out-of-office substitute routing configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApproverAvailability",
    "contract": "approvals",
    "purpose": "Out of office and substitute",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalDelegations"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-387",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-387"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 43. 0 of 0 labels bound to a contract property; 7 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-388",
  "name": "Approval SLA Policy Configuration",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "5",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/approval-sla-policy-configuration-bo-388",
   "component": "apps/venue-management-web/src/routes/venue-operations/ApprovalSlaPolicyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-384"
   ],
   "exitTo": [
    "BO-384"
   ],
   "transitions": [
    {
     "to": "BO-384",
     "trigger": "Back to Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define how quickly different approval types must be processed. The matrix explicitly requires configurable approval response-time targets.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "SLA duration",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "textField",
       "label": "Business hours / calendar hours",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Working days",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Weekends",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Public holidays",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue operating hours",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Priority-based SLA",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Risk-based SLA",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 43 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval sla policy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval sla policy untouched.",
   "emptyFirstRun": "No approval sla policy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalSlaPolicy",
    "contract": "approvals",
    "purpose": "Target, reminders and breach behaviour",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSlaEscalationReminder"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-388",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-388"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 43. 0 of 0 labels bound to a contract property; 8 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-389",
  "name": "Reminder & Breach Notification Rules",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "6",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/reminder-breach-notification-rules-bo-389",
   "component": "apps/venue-management-web/src/routes/venue-operations/ReminderBreachNotificationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-384"
   ],
   "exitTo": [
    "BO-384"
   ],
   "transitions": [
    {
     "to": "BO-384",
     "trigger": "Back to Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure proactive notifications before and after SLA breaches. The source requires reminders for pending approvals and alerts when SLA thresholds are exceeded.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 44"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 44"
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
       "impliedBy": "setApprovalSlaPolicy",
       "label": "Save approval SLA policy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApprovalSlaPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reminder breach notification list.",
   "error": "Could not load. Names which read failed and leaves the reminder breach notification untouched.",
   "emptyFirstRun": "No reminder breach notification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reminder breach notification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalSlaPolicy",
    "contract": "approvals",
    "purpose": "Reminder and breach rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSlaEscalationReminder"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-389",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-389"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 44. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-390",
  "name": "Escalation Policy Builder",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "7",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/escalation-policy-builder-bo-390",
   "component": "apps/venue-management-web/src/routes/venue-operations/EscalationPolicyBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-384"
   ],
   "exitTo": [
    "BO-384"
   ],
   "transitions": [
    {
     "to": "BO-384",
     "trigger": "Back to Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define what TICVAI should do when an approval remains unresolved or meets another escalation condition.",
  "gaps": [
   {
    "operation": null,
    "why": "**Escalation Policy Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 45"
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
       "impliedBy": "setApprovalSlaPolicy",
       "label": "Save approval SLA policy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApprovalSlaPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The escalation policy list.",
   "error": "Could not load. Names which read failed and leaves the escalation policy untouched.",
   "emptyFirstRun": "No escalation policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the escalation policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalSlaPolicy",
    "contract": "approvals",
    "purpose": "Escalation on breach",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSlaEscalationReminder"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-390",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-390"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 45. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-391",
  "name": "Live Escalation Operations Center",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "8",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/live-escalation-operations-center-bo-391",
   "component": "apps/venue-management-web/src/routes/venue-operations/LiveEscalationOperationsCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-384"
   ],
   "exitTo": [
    "BO-384"
   ],
   "transitions": [
    {
     "to": "BO-384",
     "trigger": "Back to Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true,
     "carries": [
      "instanceId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow managers to monitor and intervene in currently escalated approvals.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 46"
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
       "impliedBy": "listSlaEscalationBottleneck",
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
       "label": "Act on workflow instance",
       "operation": "actOnWorkflowInstance",
       "permission": "APPROVAL_ACT",
       "notes": "**The monitors' action buttons, as one operation** (decided 29 September, writers pass).",
       "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The live escalation operations list.",
   "error": "Could not load. Names which read failed and leaves the live escalation operations untouched.",
   "emptyFirstRun": "No live escalation operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the live escalation operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSlaEscalationBottleneck",
    "contract": "approvals",
    "purpose": "What is escalating now",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "actOnWorkflowInstance",
    "contract": "approvals",
    "purpose": "An operator's intervention in a running workflow",
    "trigger": "onAction",
    "invalidates": [
     "listSlaEscalationBottleneck"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-391",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-391"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formActOnWorkflowInstance",
    "component": "modal",
    "trigger": "Act on workflow instance",
    "body": "**Collects what `actOnWorkflowInstance` sends before it is called.** Required: `action`, `reason`. Optional: `workflowStepExecutionId`, `workflowExceptionId`, `assigneePrincipalId`, `alternativeNodeId`, `correctedInput`, `extendByMinutes`, `priority`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "WorkflowInstanceActionInput",
    "confirm": {
     "label": "Act on workflow instance",
     "operation": "actOnWorkflowInstance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "reason",
      "workflowStepExecutionId",
      "workflowExceptionId",
      "assigneePrincipalId",
      "alternativeNodeId",
      "correctedInput",
      "extendByMinutes",
      "priority"
     ]
    },
    "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "instanceId",
     "from": "navigation",
     "optional": true
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
  "id": "BO-392",
  "name": "SLA & Escalation Performance Analytics",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "9",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/sla-escalation-performance-analytics-bo-392",
   "component": "apps/venue-management-web/src/routes/venue-operations/SlaEscalationPerformanceAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-384"
   ],
   "exitTo": [
    "BO-384"
   ],
   "transitions": [
    {
     "to": "BO-384",
     "trigger": "Back to Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify) and no metric row",
  "purpose": "Provide management with analytics about where approval delays and escalations occur. The source explicitly requires escalation reporting and escalation trend analytics.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 47 §Identify"
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
       "label": "Every sla escalation performance",
       "columns": [
        "Slowest approvers",
        "Slowest stages",
        "Slowest workflows",
        "High-escalation venues",
        "High-escalation departments",
        "Peak approval periods"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 47 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected sla escalation performance",
       "bindsTo": null,
       "columns": [
        "Slowest approvers",
        "Slowest stages",
        "Slowest workflows",
        "High-escalation venues",
        "High-escalation departments",
        "Peak approval periods"
       ],
       "notes": "The pack groups this record's detail under its own headings: “SLA Compliance”, “Average Response”, “Escalation Rate”, “Breach Rate”, “SLA by Department”, “Escalations by Reason”.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 47 §Identify"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sla escalation performance list.",
   "error": "Could not load. Names which read failed and leaves the sla escalation performance untouched.",
   "emptyFirstRun": "No sla escalation performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sla escalation performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "SLA and escalation performance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Slowest approvers",
    "Slowest stages",
    "Slowest workflows",
    "High-escalation venues",
    "High-escalation departments",
    "Peak approval periods"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-392",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-392"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 47. 0 of 6 labels bound to a contract property; 6 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-393",
  "name": "AI SLA & Escalation Advisor",
  "module": "Venue Operations",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "5",
   "number": "10",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/ai-sla-escalation-advisor-bo-393",
   "component": "apps/venue-management-web/src/routes/venue-operations/AiSlaEscalationAdvisor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-384"
   ],
   "exitTo": [
    "BO-384"
   ],
   "transitions": [
    {
     "to": "BO-384",
     "trigger": "Back to Delegation & Escalation Command Center",
     "provenance": "structural — pack board 5 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use AI to predict approval bottlenecks and recommend preventive actions before SLAs are breached. The matrix specifically requires AI escalation recommendations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 48"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "datePicker",
       "label": "Analyse from",
       "operation": "getApprovalAnalytics",
       "notes": "Sends `?from=`; the window runs to now.",
       "provenance": "contract approvals.yaml GET /approval-analytics"
      },
      {
       "kind": "selectField",
       "label": "Group by",
       "operation": "getApprovalAnalytics",
       "notes": "Sends `?groupBy=` (kind, approver, venue, day, week). The pack's slowest stages, workflows, venues and departments (page 47) are these groupings; stage and department are not among them.",
       "provenance": "contract approvals.yaml GET /approval-analytics"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "SLA breaches",
       "bindsTo": "ApprovalAnalytics.rows",
       "columns": [
        "ApprovalAnalytics.rows[].slaBreached"
       ],
       "operation": "getApprovalAnalytics",
       "notes": "Summed across the returned rows.",
       "provenance": "contract approvals.yaml GET /approval-analytics"
      },
      {
       "kind": "metricTile",
       "label": "Escalated",
       "bindsTo": "ApprovalAnalytics.rows",
       "columns": [
        "ApprovalAnalytics.rows[].escalated"
       ],
       "operation": "getApprovalAnalytics",
       "notes": "Summed across the returned rows.",
       "provenance": "contract approvals.yaml GET /approval-analytics"
      },
      {
       "kind": "metricTile",
       "label": "Predicted SLA breaches (next 60 min)",
       "columns": [
        "Predicted SLA breaches (next 60 min)"
       ],
       "notes": "The pack's headline prediction (\"16 requests likely to breach\"); nothing in the contract forecasts breaches.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 48"
      },
      {
       "kind": "metricTile",
       "label": "Predicted average wait time",
       "columns": [
        "Predicted average wait time"
       ],
       "notes": "The pack's expected-impact figure (48 min to 27 min); the contract reports only observed median and p95.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 48"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Approval throughput by group",
       "bindsTo": "ApprovalAnalytics.rows",
       "columns": [
        "ApprovalAnalytics.rows[].key",
        "ApprovalAnalytics.rows[].raised",
        "ApprovalAnalytics.rows[].approved",
        "ApprovalAnalytics.rows[].rejected",
        "ApprovalAnalytics.rows[].withdrawn",
        "ApprovalAnalytics.rows[].expired",
        "ApprovalAnalytics.rows[].escalated",
        "ApprovalAnalytics.rows[].slaBreached",
        "ApprovalAnalytics.rows[].medianMinutes",
        "ApprovalAnalytics.rows[].p95Minutes"
       ],
       "operation": "getApprovalAnalytics",
       "notes": "One row per `groupBy` key; the advisor ranks the slowest first.",
       "provenance": "contract approvals.yaml GET /approval-analytics"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected AI recommendation",
       "columns": [
        "Predicted SLA risk",
        "Pending approvals",
        "Predicted breaches",
        "Recommendation",
        "Expected impact: predicted breaches",
        "Expected impact: average wait time"
       ],
       "notes": "No operation returns AI recommendations; every field here is a pack label.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 48"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Simulate recommendation",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 48"
      },
      {
       "kind": "secondaryButton",
       "label": "Create draft change",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 48"
      },
      {
       "kind": "primaryButton",
       "label": "Send for approval",
       "notes": "The pack's governance rule: AI recommends, an authorised user reviews, governance approves. No write operation is bound.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 48"
      },
      {
       "kind": "destructiveButton",
       "label": "Dismiss",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 48"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sla escalation advisor list.",
   "error": "Could not load. Names which read failed and leaves the sla escalation advisor untouched.",
   "emptyFirstRun": "No sla escalation advisor yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sla escalation advisor are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Where the SLA is failing",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "Pending requests with AI escalation suggestions (sort=aiPriority)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "escalateApprovalRequest",
    "contract": "approvals",
    "purpose": "A person acts on an escalation suggestion",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-393",
   "workshopBoard": "wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-393"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 48. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Approval_Workflows_and_Governance_Reference.pdf p.48; contract approvals.yaml GET /approval-analytics. Pack labels with no schema field yet (shown as plain labels): Predicted SLA breaches (next 60 min), Predicted average wait time, Recommendation text, Expected impact (before/after), Risk level (HIGH/...), Bottleneck share of breaches (e.g. 38%), Grouping by approval stage or department.",
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
 "actOnWorkflowInstance": {
  "method": "POST",
  "path": "/workflow-instances/{instanceId}/actions",
  "contract": "approvals",
  "summary": "An operator's intervention in a running workflow",
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
  "requestBody": "WorkflowInstanceActionInput",
  "responds": "WorkflowInstance"
 },
 "createApprovalDelegation": {
  "method": "POST",
  "path": "/delegations",
  "contract": "approvals",
  "summary": "Delegate approval authority",
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
  "requestBody": "ApprovalDelegation",
  "responds": "ApprovalDelegation"
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
 "listApprovalDelegations": {
  "method": "GET",
  "path": "/delegations",
  "contract": "approvals",
  "summary": "Who is standing in for whom",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ApprovalDelegation"
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
 "listDelegations": {
  "method": "GET",
  "path": "/guests/{subjectId}/delegations",
  "contract": "identity",
  "summary": "Who may act for this guest, and for whom they may act",
  "permission": "GUEST_VIEW",
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
 "revokeApprovalDelegation": {
  "method": "DELETE",
  "path": "/delegations/{delegationId}",
  "contract": "approvals",
  "summary": "End a delegation early",
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
  "responds": null
 },
 "setApprovalSlaPolicy": {
  "method": "PUT",
  "path": "/approval-sla-policies",
  "contract": "approvals",
  "summary": "How long a decision may take, and what happens when it does not",
  "permission": "APPROVAL_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ApprovalSlaPolicy",
  "responds": "ApprovalSlaPolicy"
 },
 "setApproverAvailability": {
  "method": "PUT",
  "path": "/approval-delegations/availability",
  "contract": "approvals",
  "summary": "Out of office, and who decides instead",
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
  "requestBody": "ApproverAvailability",
  "responds": "ApproverAvailability"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "ApprovalDelegation": {
  "type": "object",
  "x-ticvai-persistence": "approvals.delegation",
  "required": [
   "delegatorPrincipalId",
   "delegatePrincipalId",
   "from",
   "to"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "delegatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and `identity.getPrincipal`.\n"
   },
   "delegatePrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "A principal id, resolved to a name the same way as `delegatorPrincipalId`."
   },
   "kinds": {
    "type": "array",
    "description": "Absent means everything the delegator may approve.",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "maxAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "A delegate may be given less authority than the delegator, never more."
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time",
    "description": "**Required.** An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it.\n"
   },
   "reason": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
 "ApprovalSlaPolicy": {
  "type": "object",
  "x-ticvai-persistence": "approvals.sla_policy",
  "description": "Approvals boards 5.5 and 5.6. **A target with no consequence is a number in a table**, so the reminder and breach behaviour are part of the policy.\n",
  "required": [
   "code"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "appliesToRequestKinds": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "targetMinutes": {
    "type": "integer"
   },
   "businessHoursOnly": {
    "type": "boolean",
    "default": true,
    "description": "**A four-hour SLA starting at five in the afternoon is breached by nine the next morning with nobody having done anything wrong.**\n"
   },
   "calendarId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reminders": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "atPercentOfTarget": {
       "type": "integer"
      },
      "notify": {
       "type": "string",
       "enum": [
        "approver",
        "approverManager",
        "requester",
        "escalationGroup"
       ]
      }
     }
    }
   },
   "firstReminderAtPercent": {
    "type": "integer",
    "minimum": 1,
    "maximum": 100,
    "nullable": true,
    "description": "**Percent of `targetMinutes` at which the first reminder goes** (decided 29 September, readiness close-out: the reminder steps are percentages of target). A column so the SLA, Escalation, Reminder & Timeout Rules screen reads it rather than unpacking `reminders`; the reminder in `reminders` at this percentage says whom it notifies (data model for the agreed operations, 29 September)."
   },
   "secondReminderAtPercent": {
    "type": "integer",
    "minimum": 1,
    "maximum": 100,
    "nullable": true,
    "description": "Percent of `targetMinutes` at which the second reminder goes; above `firstReminderAtPercent`"
   },
   "escalateAtPercent": {
    "type": "integer",
    "minimum": 1,
    "maximum": 100,
    "nullable": true,
    "description": "Percent of `targetMinutes` at which the request or workflow escalates; at or above `secondReminderAtPercent`"
   },
   "onBreach": {
    "type": "string",
    "enum": [
     "notifyOnly",
     "escalate",
     "autoApprove",
     "autoReject"
    ],
    "default": "escalate"
   },
   "autoActionAllowed": {
    "type": "boolean",
    "default": false,
    "description": "**Auto-approval on breach is off unless somebody says otherwise, in writing.** A queue that approves itself when nobody looks is not an approval process.\n"
   },
   "escalationGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
 "ApproverAvailability": {
  "type": "object",
  "x-ticvai-persistence": "approvals.approver_availability",
  "description": "Approvals boards 5.3 and 5.4. **Dated, so nobody has to remember to turn it off.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "One period of absence. The key `setApproverAvailability` replaces by; absent on input to record a new period. Already the table's key (`approvals.approver_availability.id`), and until 26 September missing from the wire, so no period could be addressed.\n"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "unavailableFrom": {
    "type": "string",
    "format": "date-time"
   },
   "unavailableTo": {
    "type": "string",
    "format": "date-time"
   },
   "substitutePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "delegationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "appliesToRequestKinds": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "DelegatedAccess": {
  "x-ticvai-persistence": "identity.delegated_access",
  "type": "object",
  "required": [
   "id",
   "permission",
   "scopePath",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "roleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "permission": {
    "type": "string",
    "description": "From the permission enum. `*` permitted on DENY only."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "CF-132, CL-05. **A grant held by a guest rather than a staff principal.**\nSection 5.5 asks for portfolios — a primary holder assigning entitlements, transfer between linked accounts, shared wallets with individual tracking — and it appears ten times across ten sections. **Every one of those reduces to the same question: who may act on whose behalf, over what, and until when.**\n**That is a grant, not a household table.** A primary holder assigning an entitlement is a grant. A group leader holding tickets for twelve is a grant. A corporate account enrolling members is a grant with a quota. **A shared wallet with individual tracking is a grant over a balance, and the transaction log already records who spent.**\n**A household table would answer one of those four.**\n"
   },
   "overSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Whose behalf. **Null for a staff grant, which is the existing behaviour** — every grant written before 18 August means exactly what it meant before.\n"
   },
   "overObjectRef": {
    "type": "string",
    "nullable": true,
    "description": "**Where the authority is over a thing rather than a scope** — a wallet, an entitlement, a booking. `scopePath` answers *where*; this answers *what*, and a guest's authority is almost always over a specific object rather than a branch of the tree.\n"
   },
   "delegationKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "primaryHolder",
     "familyMember",
     "groupLeader",
     "attendee",
     "corporateAdmin",
     "corporateMember",
     "carer"
    ],
    "description": "**What kind of relationship this expresses**, for display and for reporting. The mechanism does not branch on it — a family member and a group attendee are the same grant with different words around them, which is the point.\n"
   },
   "quota": {
    "type": "integer",
    "nullable": true,
    "description": "2.14.15 and 4.3.11. **How many the holder may assign.** A corporate account with fifty allocations and a family with four are the same structure with different numbers.\n"
   },
   "isRevocableBySubject": {
    "type": "boolean",
    "default": true,
    "description": "**Whether the person it is over can end it.** A guest who linked a family member should be able to unlink them; a corporate member should not be able to revoke their employer's oversight — and **a delegation nobody can end is a delegation somebody will regret.**\n"
   },
   "scopePath": {
    "type": "string"
   },
   "effect": {
    "type": "string",
    "enum": [
     "ALLOW",
     "DENY"
    ]
   },
   "permissionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from `identity.user_access`, 20 September, when that table was collapsed into this one.** `permission` above is free text; this names a row in `identity.permission`, the catalogue wired the same day. A grant that names a catalogue row can be checked against the keys the contracts actually enforce — which is the whole point of a catalogue that reported *154 on operations, 35 in roles.yaml, 0 shared*.\nNullable because a role grant carries no permission at all.\n"
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "Taken from `identity.user_access`. This table recorded `revokedBy` and not when, so it could say who revoked a grant and not whether it was before or after the thing somebody is asking about.\n"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
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
 "WorkflowInstance": {
  "type": "object",
  "x-ticvai-persistence": "approvals.workflow_instance",
  "description": "**One running workflow** (pack 13.2.1, 13.2.3 and 13.2.5; data model for the agreed operations, 29 September). Started by a `WorkflowTrigger`, on the version in force at that moment and kept on it to the end (audit R129). Its steps are `WorkflowStepExecution` rows, keyed by the same `correlationId` the participating services trace with. **The SLA clock and its reminder and escalation timestamps are held here**, not in a table of their own: there is one clock per instance, and the SLA, Escalation & Bottleneck Monitor lists instances. Lifecycle in `states/workflow-instance.yaml`. The engine writes this row; an operator changes it only through `actOnWorkflowInstance`, which keeps each change as a `WorkflowIntervention` (decided 29 September, writers pass).",
  "required": [
   "id",
   "workflowDefinitionId",
   "workflowVersionId",
   "sourceModule",
   "status",
   "correlationId",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "workflowDefinitionId": {
    "type": "string",
    "format": "uuid"
   },
   "workflowVersionId": {
    "type": "string",
    "format": "uuid",
    "description": "The version the instance started on; never changes"
   },
   "workflowTriggerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceModule": {
    "$ref": "#/components/schemas/WorkflowModule"
   },
   "businessObjectType": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "businessObjectId": {
    "type": "string",
    "nullable": true,
    "description": "**A reference, never a copy**, as `ApprovalRequest.subjectId`"
   },
   "initiatedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null when a system event or schedule started it"
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "priority": {
    "type": "string",
    "maxLength": 30,
    "nullable": true
   },
   "currentNodeId": {
    "type": "string",
    "nullable": true,
    "description": "The node of the version's graph the instance is at"
   },
   "status": {
    "$ref": "#/components/schemas/WorkflowInstanceStatus"
   },
   "correlationId": {
    "type": "string",
    "maxLength": 100,
    "description": "The shared correlation id every participating service logs, for distributed tracing"
   },
   "slaPolicyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ApprovalSlaPolicy` whose clock runs on this instance"
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean",
    "default": false
   },
   "escalationLevel": {
    "type": "integer",
    "minimum": 0,
    "default": 0
   },
   "firstReminderAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "secondReminderAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "managerEscalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "executiveEscalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaOutcome": {
    "type": "string",
    "enum": [
     "metWithinTarget",
     "metAfterReminder",
     "metAfterEscalation",
     "breached"
    ],
    "nullable": true,
    "description": "How the instance finished against its SLA; set on completion (the monitor's Final Outcome)"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005). Written at venue scope"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "WorkflowInstanceActionInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; writes approvals.workflow_intervention (schema WorkflowIntervention) (decided 29 September, writers pass)",
  "description": "One operator action on a running workflow instance (decided 29 September, writers pass).",
  "required": [
   "action",
   "reason"
  ],
  "properties": {
   "action": {
    "$ref": "#/components/schemas/WorkflowInterventionAction"
   },
   "reason": {
    "type": "string",
    "minLength": 1,
    "maxLength": 500,
    "description": "Mandatory for every action (pack 13.2.5, \"actions capture a mandatory reason\")"
   },
   "workflowStepExecutionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The step acted on; for `retryStep` the step to retry from. Defaults to the instance's current step"
   },
   "workflowExceptionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The exception the action is taken from; required for `escalateException`"
   },
   "assigneePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for `reassign`, `addBackupApprover` and `escalateException`"
   },
   "alternativeNodeId": {
    "type": "string",
    "nullable": true,
    "description": "For `skipStep`, the node to continue at instead of the next one (Use Approved Alternative)"
   },
   "correctedInput": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "For `resume`, the corrected input of the failed step (Correct Data)"
   },
   "extendByMinutes": {
    "type": "integer",
    "minimum": 1,
    "maximum": 43200,
    "nullable": true,
    "description": "Required for `extendSla`"
   },
   "priority": {
    "type": "string",
    "maxLength": 30,
    "nullable": true,
    "description": "Required for `changePriority`"
   }
  }
 },
 "WorkflowInstanceStatus": {
  "type": "string",
  "description": "Where one running workflow stands (pack 13.2.1 and 13.2.3; decided 29 September, readiness close-out). Modelled in `states/workflow-instance.yaml`.",
  "enum": [
   "running",
   "waitingApproval",
   "waitingTask",
   "waitingSystem",
   "escalated",
   "failed",
   "completed",
   "cancelled"
  ]
 },
 "WorkflowInterventionAction": {
  "type": "string",
  "description": "What an operator did to a running workflow instance (pack 13.2.3, 13.2.4 and 13.2.5; decided 29 September, writers pass). The effect of each is on `actOnWorkflowInstance`.",
  "enum": [
   "reassign",
   "retryStep",
   "skipStep",
   "resume",
   "cancel",
   "extendSla",
   "addBackupApprover",
   "changePriority",
   "escalateException"
  ]
 },
 "WorkflowModule": {
  "type": "string",
  "description": "The module a workflow, rule or automation belongs to and a workflow instance originates from. The same values as `WorkflowOperationsCommandCenterView.module` (decided 29 September, readiness close-out), named so the workflow engine's tables share one vocabulary (data model for the agreed operations, 29 September).",
  "enum": [
   "ticketing",
   "pricing",
   "finance",
   "procurement",
   "crm",
   "resourceManagement",
   "fnb",
   "retail",
   "groupSales",
   "customerService",
   "membership",
   "wallet",
   "waiver",
   "subscriptionLicensing"
  ]
 }
}
```
