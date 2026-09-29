# P02-engagement-support-02 — P02 · Engagement & Support (2 of 2)

**2 screens · 7 operations · 17 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `AI_USE, CASE_MANAGE, CASE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **3 of these operations work offline**: createCase, getVisitPlan, getWaitTimes
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-059` | Plan in Progress | listDetail | 4 | 0 | — |
| `GST-068` | Help & My Cases | listDetail | 3 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-059",
  "name": "Plan in Progress",
  "module": "Engagement & Support",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/plan-my-day-in-progress",
   "component": "apps/guest-app/src/routes/general/PlanMyDayInProgressDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": false,
   "entryFrom": [
    "GST-022",
    "GST-041",
    "GST-053",
    "GST-054"
   ],
   "exitTo": [
    "GST-053",
    "GST-038",
    "GST-001"
   ],
   "transitions": [
    {
     "to": "GST-053",
     "trigger": "See the whole plan",
     "carries": [
      "planId"
     ],
     "provenance": "decided 29 September 2026 (P29), MOB-6"
    },
    {
     "to": "GST-038",
     "trigger": "Directions (At the Venue, Map)",
     "provenance": "decided 29 September 2026 (P29), MOB-6"
    },
    {
     "to": "GST-001",
     "trigger": "Home tab",
     "provenance": "decided 29 September 2026 (P29), MOB-1"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. **The in-visit half of GST-051** — one capability, two moments. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Itinerary suggestion removed 28 September** (decided 28 September, audit R209): the planner is deferred (R187) and `requestSuggestion` refuses a guest anything but prepPlan, upsell and waitTime, so this screen no longer asks for a day plan.\n\n**Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below.\n\n**Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1.\n\n**Mobile v4 role (MOB-6): \"Plan in Progress\".** Today's plan against live waits (`getWaitTimes`); rules-based, AI not required.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "Today's plan while you are in the venue, re-ordered against live waits.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "timeline",
       "label": "Today",
       "bindsTo": "VisitPlanItem",
       "operation": "getVisitPlan",
       "notes": "Today's items with done, now and next; each ride with its live wait.",
       "provenance": "decided 29 September 2026 (P29), MOB-6"
      },
      {
       "kind": "banner",
       "label": "Waits changed",
       "operation": "getWaitTimes",
       "notes": "When a wait makes the next item late, proposes a re-order or a swap (`listVisitPlanAlternatives`); the guest decides.",
       "provenance": "decided 29 September 2026 (P29), MOB-6"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Re-order my day",
       "operation": "updateVisitPlan",
       "notes": "Saves the proposed order as a new plan version.",
       "provenance": "decided 29 September 2026 (P29), MOB-6"
      },
      {
       "kind": "secondaryButton",
       "label": "Swap",
       "operation": "listVisitPlanAlternatives",
       "notes": "Candidates that suit everyone, nearest first.",
       "provenance": "decided 29 September 2026 (P29), MOB-6"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The plan builds in place; the inputs stay on screen.",
   "error": "Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing.",
   "emptyFirstRun": "No plan for today: offers to make one (GST-051).",
   "emptyNoResults": "Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers.",
   "emptyNoAccess": "A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.",
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
    "operationId": "getVisitPlan",
    "contract": "venue-map",
    "purpose": "The plan: days, timed items and add-on suggestions, at its current version",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026 (P29), MOB-6"
   },
   {
    "operationId": "updateVisitPlan",
    "contract": "venue-map",
    "purpose": "Swap, remove, add or undo: each change is a new version, so undo goes back one",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026 (P29), MOB-6"
   },
   {
    "operationId": "listVisitPlanAlternatives",
    "contract": "venue-map",
    "purpose": "Swap candidates for one item that suit everyone in the party",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026 (P29), MOB-6"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "planId",
     "from": "GST-053"
    },
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "itemId",
     "from": "navigation",
     "optional": true
    }
   ],
   "coldEntry": "Opened from a reminder on the visit day: today's plan, or an offer to make one when there is none. `itemId` is the plan item the guest taps Swap on, picked on this screen."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-059",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 3 → Plan my day – in progress",
    "differences": "Mobile v4 draws no in-progress view of the plan; built from this definition in the v4 style."
   }
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
     "provenance": "derived — GST-039 declares entryState.params subjectId and GST-068 holds subjectId, so an edge into it carries them"
    }
   ]
  },
  "notes": "**A guest could not raise a complaint.** Twelve case operations existed and every one of them was staff-side — a guest with a problem had to find somebody.\n\n**The AI concierge and a human case are one thread here.** A conversation that could not answer becomes a case rather than a dead end, which is what `listAiConversations` beside `listCases` is for.",
  "density": "comfortable",
  "offline": false,
  "pattern": "listDetail",
  "patternReason": "`listCases` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "**A guest could not raise a complaint.** Twelve case operations existed and every one of them was staff-side — a guest with a problem had to find somebody.",
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
       "label": "Every AI conversation",
       "bindsTo": "AiConversation",
       "columns": [
        "AiConversation.id",
        "AiConversation.principalId",
        "AiConversation.scopePath",
        "AiConversation.module",
        "AiConversation.locale",
        "AiConversation.messageCount",
        "AiConversation.startedAt",
        "AiConversation.lastMessageAt"
       ],
       "operation": "listAiConversations",
       "provenance": "contract ai.yaml GET /conversations"
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
       "label": "Create case",
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
   "emptyNoAccess": "Shown when the caller lacks `CASE_VIEW`, which `listCases` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Cases already loaded stay read-only with their age, so a guest can see what they raised without believing a reply arrived. **Raising a case and replying are disabled offline** — both need the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff."
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
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-068",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → Help & my cases",
    "differences": "The YAML lists AI conversations here (listAiConversations); the prototype shows them on the concierge home instead."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
    "provenance": "client-verified"
   }
  ],
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
 "getVisitPlan": {
  "method": "GET",
  "path": "/visit-plans/{planId}",
  "contract": "venue-map",
  "summary": "A visit plan, at its current version or an earlier one",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "version",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "VisitPlan"
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
  "responds": "Page"
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
 "listVisitPlanAlternatives": {
  "method": "GET",
  "path": "/visit-plans/{planId}/items/{itemId}/alternatives",
  "contract": "venue-map",
  "summary": "What could take this item's place",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
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
 "updateVisitPlan": {
  "method": "PUT",
  "path": "/visit-plans/{planId}",
  "contract": "venue-map",
  "summary": "Swap, remove, add, move or undo, as a new version",
  "permission": null,
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
  "requestBody": "VisitPlanUpdate",
  "responds": "VisitPlan"
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
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a ULID."
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
 "VisitPlan": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.visit_plan",
  "description": "**A guest's visit plan** (29 September, MOB-6): the Plan tab. One row per plan; its items are `venuemap.visit_plan_item` rows carrying the version they belong to, so every earlier version stays readable and undo is a new version equal to an old one. **Owned by the guest session**, like a cart: `subjectId` when signed in, `sessionRef` for an anonymous device session, claimed on sign-in.\n",
  "required": [
   "id",
   "venueId",
   "status",
   "version",
   "days"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "Derived from `venueId`."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "marketing.guest_profile",
    "description": "The signed-in guest. From the session, never from the body."
   },
   "sessionRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The anonymous device session that owns the plan until sign-in."
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "booked",
     "archived"
    ],
    "readOnly": true,
    "description": "`booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date."
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true,
    "description": "The current version. Every `updateVisitPlan` adds one."
   },
   "source": {
    "type": "string",
    "enum": [
     "rules",
     "preset",
     "aiAgent"
    ],
    "readOnly": true,
    "description": "What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. **The guest sees which**, as every AI answer says what it is based on.\n"
   },
   "inputs": {
    "$ref": "#/components/schemas/VisitPlanRequest"
   },
   "mapVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "The published map version the plan was laid out on."
   },
   "cartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "orders.cart",
    "description": "The cart `bookVisitPlan` filled."
   },
   "excluded": {
    "type": "array",
    "readOnly": true,
    "description": "**What was left out and why**, e.g. a coaster excluded because one of the party is under its 120 cm minimum. Shown on GST-053, so the planner never looks as if it forgot.\n",
    "items": {
     "type": "object",
     "properties": {
      "pointId": {
       "type": "string",
       "format": "uuid"
      },
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "reason": {
       "type": "string",
       "enum": [
        "heightRule",
        "ageRule",
        "closedOnDate",
        "notInInterests",
        "noTime"
       ]
      }
     }
    }
   },
   "days": {
    "type": "array",
    "readOnly": true,
    "description": "One per date, in order. The items of the version read.",
    "items": {
     "type": "object",
     "required": [
      "date",
      "items"
     ],
     "properties": {
      "date": {
       "type": "string",
       "format": "date"
      },
      "opensAt": {
       "type": "string",
       "nullable": true
      },
      "closesAt": {
       "type": "string",
       "nullable": true
      },
      "items": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/VisitPlanItem"
       }
      }
     }
    }
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "VisitPlanAlternative": {
  "type": "object",
  "x-ticvai-persistence": "none — computed on read",
  "description": "One candidate for a swap (29 September, MOB-6).",
  "required": [
   "kind",
   "startsAt",
   "reason"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "attraction",
     "show",
     "meal",
     "shop",
     "rest"
    ]
   },
   "pointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "name": {
    "type": "string"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "durationMinutes": {
    "type": "integer"
   },
   "walkMinutes": {
    "type": "integer",
    "nullable": true
   },
   "expectedWaitMinutes": {
    "type": "integer",
    "nullable": true
   },
   "matchedInterests": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "type": "string",
    "description": "Why it is offered, in words the sheet shows, e.g. *Same thrill level, 4 minutes closer*."
   }
  }
 },
 "VisitPlanItem": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.visit_plan_item",
  "description": "**One timed stop on a plan day** (29 September, MOB-6). Rows are kept per `planVersion`: a change writes the day's items again under the new version, and an older version's rows are never updated.\n",
  "required": [
   "id",
   "planId",
   "planVersion",
   "date",
   "sequence",
   "kind",
   "startsAt",
   "endsAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "venuemap.visit_plan"
   },
   "planVersion": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true
   },
   "date": {
    "type": "string",
    "format": "date"
   },
   "sequence": {
    "type": "integer",
    "minimum": 1
   },
   "kind": {
    "type": "string",
    "enum": [
     "attraction",
     "show",
     "meal",
     "shop",
     "rest",
     "travel"
    ]
   },
   "pointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "venuemap.point"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "catalogue.product",
    "description": "What is bought for this stop, where it is bought. Null for a free stop."
   },
   "bundleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "promotions.bundle",
    "description": "A meal combo or package, from the point's `featuredOffer`."
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "catalogue.performance"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "walkMinutesBefore": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "expectedWaitMinutes": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "The typical wait at that hour when the plan was laid out; GST-059 replaces it with the live one."
   },
   "addOnSuggestion": {
    "type": "object",
    "nullable": true,
    "description": "A suggested add-on for this stop, e.g. Fast Track where the wait is long. Never added by itself.",
    "properties": {
     "productId": {
      "type": "string",
      "format": "uuid"
     },
     "reason": {
      "type": "string"
     }
    }
   },
   "addOnAccepted": {
    "type": "boolean",
    "default": false
   },
   "pinned": {
    "type": "boolean",
    "default": false,
    "description": "The guest fixed this stop; a re-lay moves other stops around it."
   },
   "note": {
    "type": "string",
    "nullable": true,
    "maxLength": 200
   }
  }
 },
 "VisitPlanRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; kept as `inputs` on venuemap.visit_plan",
  "description": "What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050.\n",
  "required": [
   "venueId",
   "dates",
   "party"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "dates": {
    "type": "array",
    "minItems": 1,
    "maxItems": 7,
    "items": {
     "type": "string",
     "format": "date"
    }
   },
   "party": {
    "type": "array",
    "minItems": 1,
    "maxItems": 20,
    "description": "One entry per person. **Height where the guest knows it, age otherwise**: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. Nothing here identifies a person.\n",
    "items": {
     "type": "object",
     "properties": {
      "heightCm": {
       "type": "integer",
       "minimum": 40,
       "maximum": 230,
       "nullable": true
      },
      "ageYears": {
       "type": "integer",
       "minimum": 0,
       "maximum": 120,
       "nullable": true
      }
     }
    }
   },
   "pace": {
    "type": "string",
    "enum": [
     "packed",
     "relaxed"
    ],
    "default": "relaxed"
   },
   "interestTags": {
    "type": "array",
    "maxItems": 12,
    "description": "The same closed list as `VenuePoint.interestTags`.",
    "items": {
     "type": "string"
    }
   },
   "cuisineTags": {
    "type": "array",
    "maxItems": 8,
    "items": {
     "type": "string"
    }
   },
   "mustIncludePointIds": {
    "type": "array",
    "maxItems": 10,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "preset": {
    "type": "string",
    "nullable": true,
    "enum": [
     "highlights",
     "family",
     "thrillSeeker",
     "waterDay",
     "relaxed",
     "showsAndDining"
    ],
    "description": "A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility.\n"
   },
   "presetKey": {
    "type": "string",
    "nullable": true,
    "maxLength": 64,
    "pattern": "^[a-z][a-zA-Z0-9]*$",
    "description": "The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan the venue defines. **The same rules planner runs**: the preset only supplies interests, pace and must-include points, and the party still decides eligibility. When both `preset` and `presetKey` are sent they must name the same plan; `presetKey` is the field new clients send. An unknown key is refused 422 `unknown-preset`.\n"
   },
   "startTime": {
    "type": "string",
    "nullable": true,
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "description": "When the party arrives. Null means opening time."
   },
   "locale": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "VisitPlanUpdate": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; lands as a new version of venuemap.visit_plan_item rows",
  "description": "What `updateVisitPlan` takes (29 September, MOB-6).",
  "required": [
   "baseVersion",
   "changes"
  ],
  "properties": {
   "baseVersion": {
    "type": "integer",
    "minimum": 1
   },
   "changes": {
    "type": "array",
    "minItems": 1,
    "maxItems": 20,
    "items": {
     "type": "object",
     "required": [
      "op"
     ],
     "properties": {
      "op": {
       "type": "string",
       "enum": [
        "swap",
        "remove",
        "add",
        "move",
        "pin",
        "acceptAddOn",
        "declineAddOn",
        "revertTo"
       ]
      },
      "itemId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "date": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "pointId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "startsAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "version": {
       "type": "integer",
       "nullable": true,
       "description": "For `revertTo`, the earlier version to restore (undo)."
      }
     }
    }
   }
  }
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
   "attractionCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"
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
    "description": "The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"
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
    "format": "date-time",
    "description": "When the figure was produced — the queue's `waitTimeAsOf`."
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
