# P12-conversations-01 — P12 · Conversations

**2 screens · 13 operations · 13 schemas · 2 permissions**

Platform P12 Venue Support · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `CASE_MANAGE, CASE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SUP-004` | Conversation Queue | listDetail | 10 | 6 | — |
| `SUP-005` | Live Chat Workspace | listDetail | 11 | 8 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "SUP-004",
  "name": "Conversation Queue",
  "module": "Conversations",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C32",
  "implementation": {
   "app": "venue-support-web",
   "route": "/general/conversation-queue",
   "component": "apps/venue-support-web/src/routes/general/ConversationQueueList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-001"
   ],
   "exitTo": [
    "SUP-001",
    "SUP-002",
    "SUP-003",
    "SUP-005"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "SUP-001",
     "trigger": "Agent Login",
     "provenance": "derived — SUP-001 declares entryState.params challengeId and SUP-004 holds none of them, so the edge carries nothing and SUP-001 opens cold"
    },
    {
     "to": "SUP-002",
     "trigger": "Agent Dashboard",
     "carries": [
      "caseId"
     ],
     "provenance": "derived — SUP-002 declares entryState.params caseId and SUP-004 holds caseId, so an edge into it carries them"
    },
    {
     "to": "SUP-005",
     "trigger": "Reads the history and replies",
     "provenance": "flow F05 step 1→2, F24 step 3→4",
     "carries": [
      "caseId",
      "conversationId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Pulled to Wave 2 (CF-101). **The guest concierge is Phase 1 and a handover needs somewhere to land** — the queue and the workspace move; the rest of the console stays Wave 3.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCases` reads the population and `getCase` reads one of them — list, select, act",
  "purpose": "Find the right one quickly, and act on it without opening it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listCases",
       "notes": "Sends `?status=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Assigned to principal id",
       "operation": "listCases",
       "notes": "Sends `?assignedToPrincipalId=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "toggle",
       "label": "Breached sla",
       "operation": "listCases",
       "notes": "Sends `?breachedSla=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Priority",
       "operation": "listCases",
       "notes": "Sends `?priority=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "dataTable",
       "label": "Every case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "dataTable",
       "label": "Every conversation",
       "bindsTo": "Conversation",
       "columns": [
        "Conversation.id",
        "Conversation.telephony",
        "Conversation.assistSessionId",
        "Conversation.channel",
        "Conversation.state",
        "Conversation.subjectId",
        "Conversation.venueId",
        "Conversation.assignedPrincipalId",
        "Conversation.queueId",
        "Conversation.queuePosition",
        "Conversation.estimatedWaitSeconds",
        "Conversation.handoverReason"
       ],
       "operation": "listConversations",
       "provenance": "contract marketing-crm.yaml GET /conversations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.kind",
        "Case.channel",
        "Case.recordedAt",
        "Case.syncedAt",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "detailPanel",
       "label": "The case",
       "bindsTo": "CaseDetail",
       "columns": [
        "CaseDetail.id",
        "CaseDetail.caseNumber",
        "CaseDetail.subjectId",
        "CaseDetail.guestName",
        "CaseDetail.subject",
        "CaseDetail.kind",
        "CaseDetail.channel",
        "CaseDetail.recordedAt",
        "CaseDetail.syncedAt",
        "CaseDetail.categoryId",
        "CaseDetail.status",
        "CaseDetail.priority",
        "CaseDetail.assignedToPrincipalId",
        "CaseDetail.venueId",
        "CaseDetail.relatedOrderId",
        "CaseDetail.slaDueAt"
       ],
       "operation": "getCase",
       "provenance": "contract marketing-crm.yaml GET /cases/{caseId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add case message",
       "operation": "addCaseMessage",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Create case",
       "operation": "createCase",
       "provenance": "contract marketing-crm.yaml POST /cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate case",
       "operation": "escalateCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen case",
       "operation": "reopenCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Save case",
       "operation": "updateCase",
       "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Claim conversation",
       "operation": "claimConversation",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/claim"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer conversation",
       "operation": "transferConversation",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/transfer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The conversation queue list.",
   "error": "Could not load. Names which read failed and leaves the conversation queue untouched.",
   "emptyFirstRun": "No conversation queue yet. Offers Add case message (`addCaseMessage`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, assignedToPrincipalId, breachedSla, priority and the conversation queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `CASE_VIEW`, which `listCases` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCases",
    "contract": "marketing-crm",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "addCaseMessage",
    "contract": "marketing-crm",
    "purpose": "Add a message or internal note",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "createCase",
    "contract": "marketing-crm",
    "purpose": "Raise a service case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "escalateCase",
    "contract": "marketing-crm",
    "purpose": "Escalate a case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "getCase",
    "contract": "marketing-crm",
    "purpose": "Read a case with its thread",
    "trigger": "onAction"
   },
   {
    "operationId": "reopenCase",
    "contract": "marketing-crm",
    "purpose": "Reopen a resolved case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "updateCase",
    "contract": "marketing-crm",
    "purpose": "Assign, reprioritise or resolve a case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "listConversations",
    "contract": "marketing-crm",
    "purpose": "The omnichannel inbox",
    "trigger": "onLoad"
   },
   {
    "operationId": "claimConversation",
    "contract": "marketing-crm",
    "purpose": "An agent takes it",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "transferConversation",
    "contract": "marketing-crm",
    "purpose": "Pass it to another agent or queue",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "caseId",
     "from": "deepLink"
    },
    {
     "name": "conversationId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom.",
   "preloaded": [
    "Case.id",
    "Case.caseNumber",
    "Case.subjectId",
    "Case.guestName",
    "Case.subject"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-004"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAddCaseMessage",
    "component": "modal",
    "trigger": "Add case message",
    "body": "**Collects what `addCaseMessage` sends before it is called.** Required: `id`, `body`, `isInternal`, `recordedAt`. Optional: `channel`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add case message",
     "operation": "addCaseMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "body",
      "isInternal",
      "recordedAt",
      "channel",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
   },
   {
    "id": "formCreateCase",
    "component": "modal",
    "trigger": "Create case",
    "body": "**Collects what `createCase` sends before it is called.** Required: `id`, `subject`, `description`, `channel`, `recordedAt`. Optional: `subjectId`, `categoryId`, `priority`, `kind`, `venueId`, `relatedOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCaseRequest",
    "confirm": {
     "label": "Create case",
     "operation": "createCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "subject",
      "description",
      "channel",
      "recordedAt",
      "subjectId",
      "categoryId",
      "priority",
      "kind",
      "venueId",
      "relatedOrderId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases"
   },
   {
    "id": "formEscalateCase",
    "component": "modal",
    "trigger": "Escalate case",
    "body": "**Collects what `escalateCase` sends before it is called.** Required: `reason`. Optional: `assignToPrincipalId`, `newPriority`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Escalate case",
     "operation": "escalateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "assignToPrincipalId",
      "newPriority"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
   },
   {
    "id": "formReopenCase",
    "component": "modal",
    "trigger": "Reopen case",
    "body": "**Collects what `reopenCase` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen case",
     "operation": "reopenCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
   },
   {
    "id": "formUpdateCase",
    "component": "modal",
    "trigger": "Save case",
    "body": "**Collects what `updateCase` sends before it is called.** Nothing in the body is required. Optional: `status`, `priority`, `assignedToPrincipalId`, `categoryId`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save case",
     "operation": "updateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "priority",
      "assignedToPrincipalId",
      "categoryId",
      "resolutionNote"
     ]
    },
    "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
   },
   {
    "id": "formTransferConversation",
    "component": "modal",
    "trigger": "Transfer conversation",
    "body": "**Collects what `transferConversation` sends before it is called.** Nothing in the body is required. Optional: `toPrincipalId`, `toQueueId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer conversation",
     "operation": "transferConversation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "toPrincipalId",
      "toQueueId",
      "note"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/transfer"
   }
  ],
  "_platform": {
   "code": "P12",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Support",
   "name": "Venue Support — Agent Console",
   "offlineCapable": false,
   "app": "venue-support-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SUP-005",
  "name": "Live Chat Workspace",
  "module": "Conversations",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C32",
  "implementation": {
   "app": "venue-support-web",
   "route": "/general/live-chat-workspace",
   "component": "apps/venue-support-web/src/routes/general/LiveChatWorkspaceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-001",
    "SUP-004",
    "SUP-005"
   ],
   "inferred": true,
   "exitTo": [
    "SUP-001",
    "SUP-002",
    "SUP-003"
   ],
   "flowDerived": true,
   "transitions": [
    {
     "to": "SUP-001",
     "trigger": "Agent Login",
     "provenance": "derived — SUP-001 declares entryState.params challengeId and SUP-005 holds none of them, so the edge carries nothing and SUP-001 opens cold"
    },
    {
     "to": "SUP-002",
     "trigger": "Agent Dashboard",
     "carries": [
      "caseId"
     ],
     "provenance": "derived — SUP-002 declares entryState.params caseId and SUP-005 holds caseId, so an edge into it carries them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Pulled to Wave 2 (CF-101) with SUP-004. An agent needs a queue and a place to answer from; canned responses and SLA reporting can wait.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCases` reads the population and `getCase` reads one of them — list, select, act",
  "purpose": "Work with live chat workspace for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listCases",
       "notes": "Sends `?status=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Assigned to principal id",
       "operation": "listCases",
       "notes": "Sends `?assignedToPrincipalId=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "toggle",
       "label": "Breached sla",
       "operation": "listCases",
       "notes": "Sends `?breachedSla=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "textField",
       "label": "Priority",
       "operation": "listCases",
       "notes": "Sends `?priority=` to `listCases`.",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "dataTable",
       "label": "Every case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected case",
       "bindsTo": "Case",
       "columns": [
        "Case.id",
        "Case.caseNumber",
        "Case.subjectId",
        "Case.guestName",
        "Case.subject",
        "Case.kind",
        "Case.channel",
        "Case.recordedAt",
        "Case.syncedAt",
        "Case.categoryId",
        "Case.status",
        "Case.priority",
        "Case.assignedToPrincipalId",
        "Case.venueId",
        "Case.relatedOrderId",
        "Case.slaDueAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
      },
      {
       "kind": "detailPanel",
       "label": "The conversation",
       "bindsTo": "Conversation",
       "columns": [
        "Conversation.id",
        "Conversation.telephony",
        "Conversation.assistSessionId",
        "Conversation.channel",
        "Conversation.state",
        "Conversation.subjectId",
        "Conversation.venueId",
        "Conversation.assignedPrincipalId",
        "Conversation.queueId",
        "Conversation.queuePosition",
        "Conversation.estimatedWaitSeconds",
        "Conversation.handoverReason",
        "Conversation.handoverSummary",
        "Conversation.sentiment",
        "Conversation.intent",
        "Conversation.locale"
       ],
       "operation": "getConversation",
       "provenance": "contract marketing-crm.yaml GET /conversations/{conversationId}"
      },
      {
       "kind": "detailPanel",
       "label": "The case",
       "bindsTo": "CaseDetail",
       "columns": [
        "CaseDetail.id",
        "CaseDetail.caseNumber",
        "CaseDetail.subjectId",
        "CaseDetail.guestName",
        "CaseDetail.subject",
        "CaseDetail.kind",
        "CaseDetail.channel",
        "CaseDetail.recordedAt",
        "CaseDetail.syncedAt",
        "CaseDetail.categoryId",
        "CaseDetail.status",
        "CaseDetail.priority",
        "CaseDetail.assignedToPrincipalId",
        "CaseDetail.venueId",
        "CaseDetail.relatedOrderId",
        "CaseDetail.slaDueAt"
       ],
       "operation": "getCase",
       "provenance": "contract marketing-crm.yaml GET /cases/{caseId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add case message",
       "operation": "addCaseMessage",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Save case",
       "operation": "updateCase",
       "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate case",
       "operation": "escalateCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
      },
      {
       "kind": "secondaryButton",
       "label": "Create case",
       "operation": "createCase",
       "provenance": "contract marketing-crm.yaml POST /cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen case",
       "operation": "reopenCase",
       "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Send conversation message",
       "operation": "sendConversationMessage",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/messages"
      },
      {
       "kind": "destructiveButton",
       "label": "Close conversation",
       "operation": "closeConversation",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer conversation",
       "operation": "transferConversation",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/transfer"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseConversation",
    "component": "confirmDialog",
    "trigger": "Close conversation",
    "body": "**Names what `closeConversation` changes and what it leaves alone**, in the consequence rather than the verb. A live chat this affects should be identified in the dialog, not just counted. **Collects what `closeConversation` sends before it is called.** Required: `outcome`. Optional: `caseId`.",
    "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/close"
   },
   {
    "id": "formAddCaseMessage",
    "component": "modal",
    "trigger": "Add case message",
    "body": "**Collects what `addCaseMessage` sends before it is called.** Required: `id`, `body`, `isInternal`, `recordedAt`. Optional: `channel`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add case message",
     "operation": "addCaseMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "body",
      "isInternal",
      "recordedAt",
      "channel",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/messages"
   },
   {
    "id": "formUpdateCase",
    "component": "modal",
    "trigger": "Save case",
    "body": "**Collects what `updateCase` sends before it is called.** Nothing in the body is required. Optional: `status`, `priority`, `assignedToPrincipalId`, `categoryId`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save case",
     "operation": "updateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "priority",
      "assignedToPrincipalId",
      "categoryId",
      "resolutionNote"
     ]
    },
    "provenance": "contract marketing-crm.yaml PATCH /cases/{caseId}"
   },
   {
    "id": "formEscalateCase",
    "component": "modal",
    "trigger": "Escalate case",
    "body": "**Collects what `escalateCase` sends before it is called.** Required: `reason`. Optional: `assignToPrincipalId`, `newPriority`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Escalate case",
     "operation": "escalateCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "assignToPrincipalId",
      "newPriority"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/escalate"
   },
   {
    "id": "formCreateCase",
    "component": "modal",
    "trigger": "Create case",
    "body": "**Collects what `createCase` sends before it is called.** Required: `id`, `subject`, `description`, `channel`, `recordedAt`. Optional: `subjectId`, `categoryId`, `priority`, `kind`, `venueId`, `relatedOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCaseRequest",
    "confirm": {
     "label": "Create case",
     "operation": "createCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "subject",
      "description",
      "channel",
      "recordedAt",
      "subjectId",
      "categoryId",
      "priority",
      "kind",
      "venueId",
      "relatedOrderId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases"
   },
   {
    "id": "formReopenCase",
    "component": "modal",
    "trigger": "Reopen case",
    "body": "**Collects what `reopenCase` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen case",
     "operation": "reopenCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /cases/{caseId}/reopen"
   },
   {
    "id": "formSendConversationMessage",
    "component": "modal",
    "trigger": "Send conversation message",
    "body": "**Collects what `sendConversationMessage` sends before it is called.** Required: `body`. Optional: `attachments`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Send conversation message",
     "operation": "sendConversationMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "body",
      "attachments"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/messages"
   },
   {
    "id": "formTransferConversation",
    "component": "modal",
    "trigger": "Transfer conversation",
    "body": "**Collects what `transferConversation` sends before it is called.** Nothing in the body is required. Optional: `toPrincipalId`, `toQueueId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer conversation",
     "operation": "transferConversation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "toPrincipalId",
      "toQueueId",
      "note"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/transfer"
   }
  ],
  "states": {
   "loading": "The live chat list.",
   "error": "Could not load. Names which read failed and leaves the live chat untouched.",
   "emptyFirstRun": "No live chat yet. Offers Add case message (`addCaseMessage`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status, assignedToPrincipalId, breachedSla, priority and the live chat are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `CASE_VIEW`, which `getCase` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "addCaseMessage",
    "contract": "marketing-crm",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "getCase",
    "contract": "marketing-crm",
    "purpose": "Case with its thread",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateCase",
    "contract": "marketing-crm",
    "purpose": "Assign, reprioritise, resolve",
    "trigger": "onAction"
   },
   {
    "operationId": "escalateCase",
    "contract": "marketing-crm",
    "purpose": "Escalate with a reason",
    "trigger": "onAction"
   },
   {
    "operationId": "createCase",
    "contract": "marketing-crm",
    "purpose": "Raise a service case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "listCases",
    "contract": "marketing-crm",
    "purpose": "List service cases",
    "trigger": "onLoad"
   },
   {
    "operationId": "reopenCase",
    "contract": "marketing-crm",
    "purpose": "Reopen a resolved case",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "getConversation",
    "contract": "marketing-crm",
    "purpose": "One conversation and everything before it",
    "trigger": "onLoad"
   },
   {
    "operationId": "sendConversationMessage",
    "contract": "marketing-crm",
    "purpose": "Say something, as a guest or an agent",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "closeConversation",
    "contract": "marketing-crm",
    "purpose": "End it",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   },
   {
    "operationId": "transferConversation",
    "contract": "marketing-crm",
    "purpose": "Pass it to another agent or queue",
    "trigger": "onAction",
    "invalidates": [
     "listCases"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "caseId",
     "from": "SUP-004"
    },
    {
     "name": "conversationId",
     "from": "SUP-004"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Case.id",
    "Case.caseNumber",
    "Case.subjectId",
    "Case.guestName",
    "Case.subject"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-005"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 11 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P12",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Support",
   "name": "Venue Support — Agent Console",
   "offlineCapable": false,
   "app": "venue-support-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
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
 "addCaseMessage": {
  "method": "POST",
  "path": "/cases/{caseId}/messages",
  "contract": "marketing-crm",
  "summary": "Add a message or internal note",
  "permission": "CASE_MANAGE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CaseMessage"
 },
 "claimConversation": {
  "method": "POST",
  "path": "/conversations/{conversationId}/claim",
  "contract": "marketing-crm",
  "summary": "An agent takes it",
  "permission": "CASE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Conversation"
 },
 "closeConversation": {
  "method": "POST",
  "path": "/conversations/{conversationId}/close",
  "contract": "marketing-crm",
  "summary": "End it",
  "permission": "CASE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Conversation"
 },
 "createCase": {
  "method": "POST",
  "path": "/cases",
  "contract": "marketing-crm",
  "summary": "Raise a service case",
  "permission": "CASE_MANAGE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateCaseRequest",
  "responds": "Case"
 },
 "escalateCase": {
  "method": "POST",
  "path": "/cases/{caseId}/escalate",
  "contract": "marketing-crm",
  "summary": "Escalate a case",
  "permission": "CASE_MANAGE",
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
  "responds": "Case"
 },
 "getCase": {
  "method": "GET",
  "path": "/cases/{caseId}",
  "contract": "marketing-crm",
  "summary": "Read a case with its thread",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CaseDetail"
 },
 "getConversation": {
  "method": "GET",
  "path": "/conversations/{conversationId}",
  "contract": "marketing-crm",
  "summary": "One conversation and everything before it",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Conversation"
 },
 "listCases": {
  "method": "GET",
  "path": "/cases",
  "contract": "marketing-crm",
  "summary": "List service cases",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "assignedToPrincipalId",
    "in": "query",
    "required": null
   },
   {
    "name": "breachedSla",
    "in": "query",
    "required": null
   },
   {
    "name": "priority",
    "in": "query",
    "required": null
   },
   {
    "name": "membershipId",
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
 "listConversations": {
  "method": "GET",
  "path": "/conversations",
  "contract": "marketing-crm",
  "summary": "The omnichannel inbox",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "state",
    "in": "query",
    "required": null
   },
   {
    "name": "assignedToMe",
    "in": "query",
    "required": null
   },
   {
    "name": "channel",
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
 "reopenCase": {
  "method": "POST",
  "path": "/cases/{caseId}/reopen",
  "contract": "marketing-crm",
  "summary": "Reopen a resolved case",
  "permission": "CASE_MANAGE",
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
  "responds": "Case"
 },
 "sendConversationMessage": {
  "method": "POST",
  "path": "/conversations/{conversationId}/messages",
  "contract": "marketing-crm",
  "summary": "Say something, as a guest or an agent",
  "permission": "CASE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ConversationMessage"
 },
 "transferConversation": {
  "method": "POST",
  "path": "/conversations/{conversationId}/transfer",
  "contract": "marketing-crm",
  "summary": "Pass it to another agent or queue",
  "permission": "CASE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Conversation"
 },
 "updateCase": {
  "method": "PATCH",
  "path": "/cases/{caseId}",
  "contract": "marketing-crm",
  "summary": "Assign, reprioritise or resolve a case",
  "permission": "CASE_MANAGE",
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
  "responds": "Case"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Case": {
  "x-ticvai-persistence": "marketing.case",
  "x-ticvai-retired-columns": [
   "guest_name",
   "subject",
   "is_sla_breached"
  ],
  "type": "object",
  "required": [
   "id",
   "caseNumber",
   "subject",
   "status",
   "priority",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."
   },
   "caseNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"
   },
   "subject": {
    "type": "string",
    "x-ticvai-column": "title",
    "description": "**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CaseKind"
     }
    ],
    "nullable": true,
    "description": "What the guest said it was about, where the guest raised it."
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "description": "How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time the case was raised — the start of the SLA clock."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the case arrived. Equal to `recordedAt` for a case raised online."
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"
   },
   "status": {
    "$ref": "#/components/schemas/CaseStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "relatedOrderId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isSlaBreached": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"
   },
   "slaPausedSeconds": {
    "type": "integer",
    "description": "Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"
   },
   "escalationCount": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "CaseDetail": {
  "x-ticvai-persistence": "marketing.case",
  "allOf": [
   {
    "$ref": "#/components/schemas/Case"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string"
     },
     "resolutionNote": {
      "type": "string",
      "nullable": true
     },
     "messages": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CaseMessage"
      }
     }
    }
   }
  ]
 },
 "CaseKind": {
  "type": "string",
  "description": "**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n",
  "enum": [
   "lostProperty",
   "complaint",
   "question",
   "accessibility",
   "refundRequest",
   "other"
  ]
 },
 "CaseMessage": {
  "x-ticvai-persistence": "marketing.case_message",
  "type": "object",
  "required": [
   "id",
   "body",
   "isInternal",
   "authorKind",
   "recordedAt"
  ],
  "properties": {
   "resolution": {
    "type": "string",
    "description": "**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"
   },
   "id": {
    "type": "string"
   },
   "body": {
    "type": "string"
   },
   "isInternal": {
    "type": "boolean"
   },
   "authorKind": {
    "type": "string",
    "enum": [
     "agent",
     "guest",
     "system",
     "ai"
    ]
   },
   "authorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time — `addCaseMessage` is offline-capable."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the message arrived."
   }
  }
 },
 "CasePriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent"
  ]
 },
 "CaseStatus": {
  "type": "string",
  "enum": [
   "open",
   "inProgress",
   "awaitingGuest",
   "escalated",
   "resolved",
   "closed"
  ]
 },
 "Conversation": {
  "type": "object",
  "x-ticvai-persistence": "marketing.conversation",
  "description": "22.8. **A conversation is not a case.** A case is a ticket measured in hours; a conversation is a live session measured in seconds, with somebody waiting. A conversation may create a case; it is not one.\n",
  "required": [
   "id",
   "channel",
   "state"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "telephony": {
    "type": "object",
    "nullable": true,
    "description": "BL-083. **`ConversationChannel` included `voice` with nothing behind it** — the model anticipated telephony and stopped at the enum.\n**Not an integration, a binding.** Genesys, Avaya, Amazon Connect, Teams and 3CX all do call control themselves; what the platform needs is the call bound to the guest and the case, so **an agent who answers already knows who is calling and what about.**\n",
    "properties": {
     "providerCallId": {
      "type": "string"
     },
     "direction": {
      "type": "string",
      "enum": [
       "inbound",
       "outbound",
       "transferred"
      ]
     },
     "fromNumberMasked": {
      "type": "string",
      "nullable": true,
      "description": "**Masked, and it is still personal data.** A phone number identifies a person more reliably than a name does.\n"
     },
     "recordingRef": {
      "type": "string",
      "nullable": true,
      "description": "Held by the provider, referenced here. **Recording consent is jurisdictional and the platform does not assume it** — a reference with no consent record is a recording nobody may play.\n"
     },
     "agentState": {
      "type": "string",
      "enum": [
       "available",
       "onCall",
       "wrapUp",
       "away",
       "offline"
      ],
      "nullable": true
     }
    }
   },
   "assistSessionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-094. **`startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced the other** — so the traceability 2.13.20 asks for had no link to follow.\n**The link is here rather than on the assist session**, because a case may span several assists and an assist belongs to at most one case.\n"
   },
   "channel": {
    "$ref": "#/components/schemas/ConversationChannel"
   },
   "state": {
    "$ref": "#/components/schemas/ConversationState"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "22.8.3. Resolved from phone, email, membership number or a signed-in session. **A conversation with none of those stays anonymous rather than being guessed at.**\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assignedPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queuePosition": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). Null once claimed."
   },
   "estimatedWaitSeconds": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). Null once claimed."
   },
   "handoverReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "guestRequested",
     "assistantRefused",
     "assistantFailed",
     "outOfScope",
     "negativeSentiment",
     "complexIntent",
     "paymentIssue"
    ]
   },
   "handoverSummary": {
    "type": "string",
    "nullable": true,
    "description": "**The assistant's own account of what the guest wants**, so an agent opens with context rather than reading a transcript while somebody waits.\n"
   },
   "sentiment": {
    "type": "string",
    "nullable": true,
    "enum": [
     "positive",
     "neutral",
     "negative",
     "escalating"
    ],
    "description": "22.8.16. **`escalating` is a routing signal**, not a report line."
   },
   "intent": {
    "type": "string",
    "nullable": true,
    "description": "22.8.13. What the guest appears to want, used for routing."
   },
   "locale": {
    "type": "string"
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "22.8.12. Where the conversation raised one."
   },
   "messages": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ConversationMessage"
    }
   },
   "firstResponseSeconds": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "outcome": {
    "type": "string",
    "nullable": true,
    "enum": [
     "resolved",
     "caseRaised",
     "abandonedByGuest",
     "timedOut",
     "spam"
    ]
   }
  }
 },
 "ConversationChannel": {
  "type": "string",
  "enum": [
   "webChat",
   "inAppChat",
   "whatsapp",
   "sms",
   "email",
   "kiosk",
   "voice"
  ]
 },
 "ConversationMessage": {
  "type": "object",
  "x-ticvai-persistence": "marketing.conversation_message + marketing.conversation_message_attachment",
  "required": [
   "id",
   "sender",
   "body",
   "sentAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "sender": {
    "type": "string",
    "enum": [
     "guest",
     "agent",
     "assistant",
     "system"
    ],
    "description": "**Resolved, never declared.** The assistant is labelled as one — a guest talking to a bot that presents as a person is a complaint waiting for the moment they find out.\n"
   },
   "senderPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "body": {
    "type": "string"
   },
   "attachments": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "assetId": {
       "type": "string",
       "format": "uuid"
      },
      "kind": {
       "type": "string",
       "enum": [
        "image",
        "video",
        "document",
        "ticket",
        "qr",
        "paymentLink"
       ]
      }
     }
    }
   },
   "aiInteractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the assistant sent it. **Links the message to its tokens and cost**, so a conversation's spend is attributable (CF-14).\n"
   },
   "sentAt": {
    "type": "string",
    "format": "date-time"
   },
   "readAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ConversationState": {
  "type": "string",
  "description": "**`withAssistant` and `queued` are different, and the second has a person waiting.** Merging them makes the service level unmeasurable, because time with a bot is not time in a queue.\n",
  "enum": [
   "withAssistant",
   "queued",
   "withAgent",
   "waitingOnGuest",
   "resolved",
   "abandoned",
   "timedOut"
  ]
 },
 "CreateCaseRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "subject",
   "description",
   "channel",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "subject": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 10000
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. Must belong to `subjectId` when both are given (422). (decided 29 September, coordinator decision DM4, writers pass)"
   },
   "priority": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CasePriority"
     }
    ],
    "default": "normal"
   },
   "kind": {
    "$ref": "#/components/schemas/CaseKind"
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "relatedOrderId": {
    "type": "string"
   },
   "attachmentRefs": {
    "type": "array",
    "description": "Stored on the opening `CaseMessage`, not on the case.",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time the case was raised. The server stamps `Case.syncedAt` on arrival."
   }
  }
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
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
 }
}
```
