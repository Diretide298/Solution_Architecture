# P02-engagement-support-02 — P02 · Engagement & Support (2 of 2)

**2 screens · 6 operations · 14 schemas · 4 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_USE, CASE_MANAGE, CASE_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **3 of these operations work offline**: createCase, getWaitTimes, listProducts
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-059` | Plan My Day – In Progress | listDetail | 3 | 0 | — |
| `GST-068` | Help & My Cases | listDetail | 3 | 0 | — |

## Thin screens in this batch

**GST-059, GST-068 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-059",
  "name": "Plan My Day – In Progress",
  "module": "Engagement & Support",
  "requiresModule": "ai",
  "wave": 3,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/plan-my-day-in-progress",
   "component": "apps/guest-app/src/routes/general/PlanMyDayInProgressDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-054"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. **The in-visit half of GST-051** — one capability, two moments. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared.",
  "openQuestions": [
   "Inventory cites `GET /itineraries/{id}` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "The plan while you are in the venue, against live waits.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every plan day progress",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected plan day progress",
       "bindsTo": "WaitTime",
       "columns": [
        "WaitTime.queueId",
        "WaitTime.queueName",
        "WaitTime.attractionProductId",
        "WaitTime.status",
        "WaitTime.waitMinutes",
        "WaitTime.source",
        "WaitTime.isStale",
        "WaitTime.heightRequirementCm",
        "WaitTime.zone",
        "WaitTime.asOf"
       ],
       "operation": "getWaitTimes",
       "provenance": "contract queue.yaml GET /queues/wait-times"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Request",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The plan day progress list.",
   "error": "Could not load. Names which read failed and leaves the plan day progress untouched.",
   "emptyFirstRun": "No plan day progress yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the plan day progress are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "suggestionId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "A suggestion opened from a saved plan.",
   "preloaded": [
    "WaitTime.queueId",
    "WaitTime.queueName",
    "WaitTime.attractionProductId",
    "WaitTime.status",
    "WaitTime.waitMinutes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-059"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-068",
  "name": "Help & My Cases",
  "module": "Engagement & Support",
  "requiresModule": "core",
  "wave": 2,
  "capability": "read-write",
  "implementation": {
   "app": "guest-app",
   "route": "/account/help-my-cases",
   "component": "apps/guest-app/src/routes/account/HelpMyCases.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "GST-039"
   ],
   "entryFrom": [
    "GST-001"
   ],
   "inferred": false,
   "notes": "**Reached from GST-001** — a top-level section of the app. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "GST-039",
     "trigger": "Profile",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-039 declares entryState.params subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**A guest could not raise a complaint.** Twelve case operations existed and every one of them was staff-side — a guest with a problem had to find somebody.\n\n**The AI concierge and a human case are one thread here.** A conversation that could not answer becomes a case rather than a dead end, which is what `listAiConversations` beside `listCases` is for.",
  "density": "comfortable",
  "offline": false,
  "pattern": "listDetail",
  "patternReason": "`listCases` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "**A guest could not raise a complaint.** Twelve case operations existed and every one of them was staff-side — a guest with a problem had to find somebody.",
  "gaps": [
   {
    "operation": "listAiConversations",
    "why": "**1 declared operation reach no component on this screen**: listAiConversations. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every help cases",
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
       "label": "The selected help cases",
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
        "Case.slaDueAt",
        "Case.isSlaBreached",
        "Case.slaPausedSeconds",
        "Case.escalationCount",
        "Case.resolvedAt"
       ],
       "operation": "listCases",
       "provenance": "contract marketing-crm.yaml GET /cases"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createCase",
       "provenance": "contract marketing-crm.yaml POST /cases"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**No cases open.** The concierge sits here too — most questions never become a case, and that is the intent.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Cases already loaded stay read-only with their age, so a guest can see what they raised without believing a reply arrived. Raising and replying need the connection."
  },
  "apis": [
   {
    "operationId": "createCase",
    "contract": "marketing-crm",
    "purpose": "Raise a service case",
    "trigger": "onAction",
    "offline": false,
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
    "operationId": "listAiConversations",
    "contract": "ai",
    "purpose": "A principal's conversation history",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030).",
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
   "board": "wireframes/P02 Guest App.dc.html#gst-068"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
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
 "getWaitTimes": {
  "method": "GET",
  "path": "/queues/wait-times",
  "contract": "queue",
  "summary": "Wait times across a venue",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": true
   },
   {
    "name": "category",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WaitTime"
 },
 "listAiConversations": {
  "method": "GET",
  "path": "/conversations",
  "contract": "ai",
  "summary": "A principal's conversation history",
  "permission": "AI_USE",
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
  "responds": "AiConversation"
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
 "listProducts": {
  "method": "GET",
  "path": "/products",
  "contract": "catalogue",
  "summary": "List products",
  "permission": "PRODUCT_VIEW",
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
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "isSellable",
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
 "requestSuggestion": {
  "method": "POST",
  "path": "/ai/suggestions",
  "contract": "ai",
  "summary": "Ask for an answer, however it is currently produced",
  "permission": "AI_USE",
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
  "responds": "Suggestion"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiConversation": {
  "type": "object",
  "x-ticvai-persistence": "ai.conversation",
  "required": [
   "id",
   "principalId",
   "module",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "module": {
    "type": "string"
   },
   "locale": {
    "type": "string"
   },
   "messageCount": {
    "type": "integer"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastMessageAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Case": {
  "x-ticvai-persistence": "marketing.case",
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
    "type": "string"
   },
   "caseNumber": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string",
    "nullable": true
   },
   "subject": {
    "type": "string"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
    "type": "boolean"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
   "priority": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CasePriority"
     }
    ],
    "default": "normal"
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
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
 "Suggestion": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion",
  "description": "One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n",
  "required": [
   "id",
   "kind",
   "basis",
   "producedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/SuggestionKind"
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "scopePath": {
    "type": "string"
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "What it is about — a product, an outlet, an item, a party."
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "description": "The suggestion itself. Shape depends on `kind`."
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1,
    "description": "**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"
   },
   "explanation": {
    "type": "string",
    "description": "**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"
   },
   "inputs": {
    "type": "object",
    "additionalProperties": true,
    "description": "What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"
   },
   "producerRef": {
    "type": "string",
    "description": "The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"
   },
   "producedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"
   }
  }
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
 "SuggestionKind": {
  "type": "string",
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n",
  "enum": [
   "price",
   "replenishment",
   "requisition",
   "demandForecast",
   "prepPlan",
   "menuEngineering",
   "staffing",
   "slaTarget",
   "waitTime",
   "upsell",
   "segmentation",
   "anomaly",
   "scenario"
  ]
 },
 "WaitTime": {
  "x-ticvai-persistence": "none — computed from readings and throughput",
  "type": "object",
  "required": [
   "queueId",
   "waitMinutes",
   "source",
   "asOf",
   "isStale"
  ],
  "properties": {
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "queueName": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "attractionProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/QueueStatus"
   },
   "waitMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "Null where the queue is closed or no estimate is available."
   },
   "source": {
    "$ref": "#/components/schemas/WaitTimeSource"
   },
   "isStale": {
    "type": "boolean",
    "description": "The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current.\n"
   },
   "heightRequirementCm": {
    "type": "integer",
    "nullable": true
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   }
  }
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
