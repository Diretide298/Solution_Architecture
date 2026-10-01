# WS25 — Customer Service board 1

**10 screens · 13 operations · 23 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_CONFIGURE, AI_USE, CASE_MANAGE, CASE_VIEW, ORDER_REFUND`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SUP-009` | Customer Service Command Center | listDetail | 2 | 0 | — |
| `SUP-010` | Customer 360° Service Profile | listDetail | 2 | 0 | — |
| `SUP-011` | Unified Interaction & Communication History | configEditor | 1 | 0 | — |
| `SUP-012` | Case Creation, Classification & Intelligent Routing | configEditor | 2 | 0 | — |
| `SUP-013` | Case Investigation & Resolution Workspace | listDetail | 1 | 0 | — |
| `SUP-014` | Order, Booking & Ticket Service Workspace | listDetail | 1 | 0 | — |
| `SUP-015` | Refund, Compensation & Service Exception Workspace | listDetail | 1 | 0 | — |
| `SUP-016` | Escalation, Collaboration & Internal Resolution | configEditor | 1 | 0 | — |
| `SUP-017` | Case Resolution, Closure & Customer Feedback | configEditor | 1 | 0 | — |
| `SUP-018` | AI Customer Service Copilot & Knowledge Workspace | listDetail | 3 | 0 | — |

## Thin screens in this batch

**SUP-010, SUP-013, SUP-018 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "SUP-009",
  "name": "Customer Service Command Center",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.1",
   "page": 3
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/customer-service-command-center-sup-009",
   "component": "apps/venue-support-web/src/routes/support/CustomerServiceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-001"
   ],
   "exitTo": [
    "SUP-001",
    "SUP-010",
    "SUP-011",
    "SUP-012",
    "SUP-013",
    "SUP-014",
    "SUP-015",
    "SUP-016",
    "SUP-017",
    "SUP-018"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "SUP-001",
     "trigger": "Agent Login",
     "provenance": "derived — SUP-001 declares entryState.params challengeId and SUP-009 holds none of them. The edge carries nothing: SUP-009 is opened from SUP-001, so this edge is the way back and SUP-001 keeps its own state"
    },
    {
     "to": "SUP-010",
     "trigger": "Works in Customer 360° Service Profile",
     "provenance": "flow F134 step 1→2",
     "operation": "listCustomerService"
    },
    {
     "to": "SUP-011",
     "trigger": "Works in Unified Interaction & Communication History",
     "provenance": "flow F134 step 3→4",
     "operation": "listCustomerService"
    },
    {
     "to": "SUP-012",
     "trigger": "Works in Case Creation, Classification & Intelligent Routing",
     "provenance": "flow F134 step 5→6",
     "operation": "listCustomerService"
    },
    {
     "to": "SUP-013",
     "trigger": "Works in Case Investigation & Resolution Workspace",
     "provenance": "flow F134 step 7→8",
     "operation": "listCustomerService"
    },
    {
     "to": "SUP-014",
     "trigger": "Works in Order, Booking & Ticket Service Workspace",
     "provenance": "flow F134 step 9→10",
     "operation": "listCustomerService"
    },
    {
     "to": "SUP-015",
     "trigger": "Works in Refund, Compensation & Service Exception Workspace",
     "provenance": "flow F134 step 11→12",
     "operation": "listCustomerService"
    },
    {
     "to": "SUP-016",
     "trigger": "Works in Escalation, Collaboration & Internal Resolution",
     "provenance": "flow F134 step 13→14",
     "operation": "listCustomerService"
    },
    {
     "to": "SUP-017",
     "trigger": "Works in Case Resolution, Closure & Customer Feedback",
     "provenance": "flow F134 step 15→16",
     "operation": "listCustomerService"
    },
    {
     "to": "SUP-018",
     "trigger": "Works in AI Customer Service Copilot & Knowledge Workspace",
     "provenance": "flow F134 step 17→18",
     "operation": "listCustomerService"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An agent can immediately understand their workload, priorities, SLA exposure and required actions without navigating multiple TICVAI modules.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide every customer-service agent with a personalized operational workspace showing customers, cases, tasks, SLAs, alerts and workload.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: New Case, Find Customer, Find Order, Find Ticket, Find Booking, Assign Case, Escalate, Open AI Assistant. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Customer Service_Reference.pdf, page 3 §Quick Actions"
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
       "label": "Every customer service",
       "columns": [
        "CustomerServiceCommandCenterView.myOpenCases",
        "CustomerServiceCommandCenterView.newCases",
        "CustomerServiceCommandCenterView.casesDueToday",
        "CustomerServiceCommandCenterView.slaAtRisk",
        "CustomerServiceCommandCenterView.slaBreached",
        "CustomerServiceCommandCenterView.awaitingCustomer",
        "CustomerServiceCommandCenterView.awaitingInternalTeam",
        "CustomerServiceCommandCenterView.escalatedCases",
        "CustomerServiceCommandCenterView.resolvedToday",
        "CustomerServiceCommandCenterView.averageResolutionSeconds",
        "CustomerServiceCommandCenterView.workQueue[].caseId",
        "CustomerServiceCommandCenterView.workQueue[].customer",
        "CustomerServiceCommandCenterView.workQueue[].subject",
        "CustomerServiceCommandCenterView.workQueue[].category",
        "CustomerServiceCommandCenterView.workQueue[].channel",
        "CustomerServiceCommandCenterView.workQueue[].priority",
        "CustomerServiceCommandCenterView.workQueue[].status",
        "CustomerServiceCommandCenterView.workQueue[].assignedAgentPrincipalId",
        "CustomerServiceCommandCenterView.workQueue[].slaRemainingSeconds",
        "CustomerServiceCommandCenterView.workQueue[].lastInteractionAt",
        "CustomerServiceCommandCenterView.workQueue[].nextAction",
        "CustomerServiceCommandCenterView.todaysTasks[].kind"
       ],
       "bindsTo": "CustomerServiceCommandCenterView.workQueue[]",
       "operation": "listCustomerService",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer service",
       "bindsTo": "CustomerServiceCommandCenterView",
       "columns": [
        "CustomerServiceCommandCenterView.myOpenCases",
        "CustomerServiceCommandCenterView.newCases",
        "CustomerServiceCommandCenterView.casesDueToday",
        "CustomerServiceCommandCenterView.slaAtRisk",
        "CustomerServiceCommandCenterView.slaBreached",
        "CustomerServiceCommandCenterView.awaitingCustomer",
        "CustomerServiceCommandCenterView.awaitingInternalTeam",
        "CustomerServiceCommandCenterView.escalatedCases",
        "CustomerServiceCommandCenterView.resolvedToday",
        "CustomerServiceCommandCenterView.averageResolutionSeconds",
        "CustomerServiceCommandCenterView.workQueue[].caseId",
        "CustomerServiceCommandCenterView.workQueue[].customer",
        "CustomerServiceCommandCenterView.workQueue[].subject",
        "CustomerServiceCommandCenterView.workQueue[].category",
        "CustomerServiceCommandCenterView.workQueue[].channel",
        "CustomerServiceCommandCenterView.workQueue[].priority",
        "CustomerServiceCommandCenterView.workQueue[].status",
        "CustomerServiceCommandCenterView.workQueue[].assignedAgentPrincipalId",
        "CustomerServiceCommandCenterView.workQueue[].slaRemainingSeconds",
        "CustomerServiceCommandCenterView.workQueue[].lastInteractionAt",
        "CustomerServiceCommandCenterView.workQueue[].nextAction",
        "CustomerServiceCommandCenterView.todaysTasks[].kind"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Use”, “Customer Waiting”.",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "New Case",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Find Customer",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Find Order",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Find Ticket",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Find Booking",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign Case",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Open AI Assistant",
       "provenance": "pack Customer Service_Reference.pdf, page 3 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer service list.",
   "error": "Could not load. Names which read failed and leaves the customer service untouched.",
   "emptyFirstRun": "No customer service yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer service are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerService",
    "contract": "marketing-crm",
    "purpose": "Customer Service Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCustomerServiceProfile",
    "contract": "marketing-crm",
    "purpose": "Customer 360° Service Profile",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CustomerServiceCommandCenterView.myOpenCases",
    "CustomerServiceCommandCenterView.newCases",
    "CustomerServiceCommandCenterView.casesDueToday",
    "CustomerServiceCommandCenterView.slaAtRisk",
    "CustomerServiceCommandCenterView.slaBreached",
    "CustomerServiceCommandCenterView.awaitingCustomer"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-009",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-009"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 3. 25 of 27 labels bound to a contract property; 35 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-010",
  "name": "Customer 360° Service Profile",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.2",
   "page": 5
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/customer-360-service-profile-sup-010",
   "component": "apps/venue-support-web/src/routes/support/Customer360ServiceProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-009"
   ],
   "exitTo": [
    "SUP-009"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-009, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-009",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F134 step 2→3",
     "operation": "listCustomerServiceProfile"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Agents can understand the customer's complete TICVAI relationship and relevant service context from one screen.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide the agent with a complete customer-service view of the customer. This should be one of the most important screens in the entire Customer Service module.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every customer 360° service",
       "columns": [
        "Customer360ServiceProfileView.customerName",
        "Customer360ServiceProfileView.customerId",
        "Customer360ServiceProfileView.customerType",
        "Customer360ServiceProfileView.membershipStatus",
        "Customer360ServiceProfileView.loyaltyTier",
        "Customer360ServiceProfileView.preferredLanguage",
        "Customer360ServiceProfileView.country",
        "Customer360ServiceProfileView.contactDetails",
        "Customer360ServiceProfileView.customerSince",
        "Customer360ServiceProfileView.customerValue",
        "Open Cases",
        "Customer360ServiceProfileView.riskAttentionIndicator",
        "360° Navigation",
        "Customer360ServiceProfileView.upcomingTickets",
        "Customer360ServiceProfileView.activeMembership",
        "Customer360ServiceProfileView.walletBalance",
        "Customer360ServiceProfileView.activeReservations",
        "Customer360ServiceProfileView.futureGroupBookings",
        "Open Orders"
       ],
       "bindsTo": "Customer360ServiceProfileView",
       "operation": "listCustomerServiceProfile",
       "provenance": "pack Customer Service_Reference.pdf, page 5 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer 360° service",
       "bindsTo": "Customer360ServiceProfileView",
       "columns": [
        "Customer360ServiceProfileView.customerName",
        "Customer360ServiceProfileView.customerId",
        "Customer360ServiceProfileView.customerType",
        "Customer360ServiceProfileView.membershipStatus",
        "Customer360ServiceProfileView.loyaltyTier",
        "Customer360ServiceProfileView.preferredLanguage",
        "Customer360ServiceProfileView.country",
        "Customer360ServiceProfileView.contactDetails",
        "Customer360ServiceProfileView.customerSince",
        "Customer360ServiceProfileView.customerValue",
        "Open Cases",
        "Customer360ServiceProfileView.riskAttentionIndicator",
        "360° Navigation",
        "Customer360ServiceProfileView.upcomingTickets",
        "Customer360ServiceProfileView.activeMembership",
        "Customer360ServiceProfileView.walletBalance",
        "Customer360ServiceProfileView.activeReservations",
        "Customer360ServiceProfileView.futureGroupBookings",
        "Open Orders"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Today”, “Yesterday”, “Last Month”, “Display permitted information such as”, “Sensitive information should be”, “Customer Summary”.",
       "provenance": "pack Customer Service_Reference.pdf, page 5 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer 360° service list.",
   "error": "Could not load. Names which read failed and leaves the customer 360° service untouched.",
   "emptyFirstRun": "No customer 360° service yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer 360° service are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerServiceProfile",
    "contract": "marketing-crm",
    "purpose": "Customer 360° Service Profile",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCustomerService",
    "contract": "marketing-crm",
    "purpose": "Customer Service Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Customer360ServiceProfileView.customerName",
    "Customer360ServiceProfileView.customerId",
    "Customer360ServiceProfileView.customerType",
    "Customer360ServiceProfileView.membershipStatus",
    "Customer360ServiceProfileView.loyaltyTier",
    "Customer360ServiceProfileView.preferredLanguage"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-010",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-010"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 5. 16 of 19 labels bound to a contract property; 19 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-011",
  "name": "Unified Interaction & Communication History",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.3",
   "page": 7
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/unified-interaction-communication-history-sup-011",
   "component": "apps/venue-support-web/src/routes/support/UnifiedInteractionCommunicationHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-009"
   ],
   "exitTo": [
    "SUP-009"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-009, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-009",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F134 step 4→5",
     "operation": "listUnifiedInteractionCommunication"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Agents can see the complete relevant conversation history without searching separate communication systems.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide one chronological timeline of customer interactions across supported service channels.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Date/Time",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Agent/System",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Direction",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Subject",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Related Case",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Related Order",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Related Ticket",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Attachments",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Sentiment where enabled",
       "provenance": "pack Customer Service_Reference.pdf, page 7 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The unified interaction communication configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the unified interaction communication untouched.",
   "emptyFirstRun": "No unified interaction communication configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUnifiedInteractionCommunication",
    "contract": "marketing-crm",
    "purpose": "Unified Interaction & Communication History",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-011",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-011"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 11 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-012",
  "name": "Case Creation, Classification & Intelligent Routing",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.4",
   "page": 9
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/case-creation-classification-intelligent-routing-sup-012",
   "component": "apps/venue-support-web/src/routes/support/CaseCreationClassificationIntelligentRouting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-009"
   ],
   "exitTo": [
    "SUP-009"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-009, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-009",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F134 step 6→7",
     "operation": "createCaseClassificationIntelligent"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every service request becomes a properly categorized, prioritized and routed case with the appropriate business context attached.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Create structured customer-service cases and ensure they reach the correct team.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Subject",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Source",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Category",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Subcategory",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Related Order",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Related Ticket",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Related Payment",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Related Membership",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Attachments",
       "provenance": "pack Customer Service_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "textField",
       "label": "Parent category id",
       "operation": "listCaseCategories",
       "notes": "Sends `?parentCategoryId=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "toggle",
       "label": "Top level only",
       "operation": "listCaseCategories",
       "notes": "Sends `?topLevelOnly=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listCaseCategories",
       "notes": "Sends `?isActive=` to `listCaseCategories`.",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      },
      {
       "kind": "dataTable",
       "label": "Every case category",
       "bindsTo": "CaseCategory",
       "columns": [
        "CaseCategory.id",
        "CaseCategory.code",
        "CaseCategory.name",
        "CaseCategory.parentCategoryId",
        "CaseCategory.defaultPriority",
        "CaseCategory.isActive",
        "CaseCategory.scopePath"
       ],
       "operation": "listCaseCategories",
       "provenance": "contract marketing-crm.yaml GET /case-categories"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "provenance": "contract operation createCaseClassificationIntelligent"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The case creation classification configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the case creation classification untouched.",
   "emptyFirstRun": "No case creation classification configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createCaseClassificationIntelligent",
    "contract": "marketing-crm",
    "purpose": "Case Creation, Classification & Intelligent Routing",
    "trigger": "onAction"
   },
   {
    "operationId": "listCaseCategories",
    "contract": "marketing-crm",
    "purpose": "List case categories and subcategories",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-012",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-012"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 14 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-013",
  "name": "Case Investigation & Resolution Workspace",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.5",
   "page": 11
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/case-investigation-resolution-workspace-sup-013",
   "component": "apps/venue-support-web/src/routes/support/CaseInvestigationResolutionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-009"
   ],
   "exitTo": [
    "SUP-009"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-009, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-009",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F134 step 8→9",
     "operation": "setCaseInvestigationResolution"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An agent can investigate and progress a customer case from one workspace with all required customer, transaction, policy and communication context visible.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the primary workspace in which an agent investigates and resolves a case.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Action history. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Customer Service_Reference.pdf, page 11 §Support"
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
       "label": "Every case investigation resolution",
       "columns": [
        "CaseInvestigationResolutionWorkspaceView.caseId",
        "CaseInvestigationResolutionWorkspaceView.customer",
        "CaseInvestigationResolutionWorkspaceView.subject",
        "CaseInvestigationResolutionWorkspaceView.category",
        "CaseInvestigationResolutionWorkspaceView.priority",
        "CaseInvestigationResolutionWorkspaceView.status",
        "CaseInvestigationResolutionWorkspaceView.sla",
        "CaseInvestigationResolutionWorkspaceView.owner",
        "CaseInvestigationResolutionWorkspaceView.queue",
        "CaseInvestigationResolutionWorkspaceView.created",
        "CaseInvestigationResolutionWorkspaceView.lastUpdated"
       ],
       "bindsTo": "CaseInvestigationResolutionWorkspaceView",
       "operation": "setCaseInvestigationResolution",
       "provenance": "pack Customer Service_Reference.pdf, page 11 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected case investigation resolution",
       "bindsTo": "CaseInvestigationResolutionWorkspaceView",
       "columns": [
        "CaseInvestigationResolutionWorkspaceView.caseId",
        "CaseInvestigationResolutionWorkspaceView.customer",
        "CaseInvestigationResolutionWorkspaceView.subject",
        "CaseInvestigationResolutionWorkspaceView.category",
        "CaseInvestigationResolutionWorkspaceView.priority",
        "CaseInvestigationResolutionWorkspaceView.status",
        "CaseInvestigationResolutionWorkspaceView.sla",
        "CaseInvestigationResolutionWorkspaceView.owner",
        "CaseInvestigationResolutionWorkspaceView.queue",
        "CaseInvestigationResolutionWorkspaceView.created",
        "CaseInvestigationResolutionWorkspaceView.lastUpdated"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Agents can attach”, “Case Actions”.",
       "provenance": "pack Customer Service_Reference.pdf, page 11 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Action history",
       "provenance": "pack Customer Service_Reference.pdf, page 11 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The case investigation resolution list.",
   "error": "Could not load. Names which read failed and leaves the case investigation resolution untouched.",
   "emptyFirstRun": "No case investigation resolution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the case investigation resolution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCaseInvestigationResolution",
    "contract": "marketing-crm",
    "purpose": "Case Investigation & Resolution Workspace",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "CaseInvestigationResolutionWorkspaceView.caseId",
    "CaseInvestigationResolutionWorkspaceView.customer",
    "CaseInvestigationResolutionWorkspaceView.subject",
    "CaseInvestigationResolutionWorkspaceView.category",
    "CaseInvestigationResolutionWorkspaceView.priority",
    "CaseInvestigationResolutionWorkspaceView.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-013",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-013"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 11. 11 of 11 labels bound to a contract property; 12 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-014",
  "name": "Order, Booking & Ticket Service Workspace",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.6",
   "page": 13
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/order-booking-ticket-service-workspace-sup-014",
   "component": "apps/venue-support-web/src/routes/support/OrderBookingTicketServiceWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-009"
   ],
   "exitTo": [
    "SUP-009"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-009, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-009",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F134 step 10→11",
     "operation": "setOrderBookingTicket"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Agents can perform authorized ticket and booking service actions through one customer-service interface while underlying TICVAI services remain authoritative.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow customer-service agents to perform permitted ticket/order servicing without entering the underlying technical modules.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search order booking ticket",
       "provenance": "pack Customer Service_Reference.pdf, page 13 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Order Number",
        "Ticket Number",
        "Booking Reference",
        "Customer",
        "Email",
        "Mobile",
        "QR Reference",
        "Event",
        "Payment Reference"
       ],
       "notes": "The pack filters this screen by order number, ticket number, booking reference, customer, email, mobile and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Customer Service_Reference.pdf, page 13 §Search by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every order booking ticket",
       "columns": [
        "OrderBookingTicketServiceWorkspaceView.order",
        "Customer",
        "OrderBookingTicketServiceWorkspaceView.purchaseDate",
        "OrderBookingTicketServiceWorkspaceView.channel",
        "OrderBookingTicketServiceWorkspaceView.products",
        "OrderBookingTicketServiceWorkspaceView.tickets",
        "Event",
        "OrderBookingTicketServiceWorkspaceView.dateTime",
        "OrderBookingTicketServiceWorkspaceView.amount",
        "OrderBookingTicketServiceWorkspaceView.payment",
        "OrderBookingTicketServiceWorkspaceView.fulfillment",
        "OrderBookingTicketServiceWorkspaceView.ticketStatus"
       ],
       "bindsTo": "OrderBookingTicketServiceWorkspaceView",
       "operation": "setOrderBookingTicket",
       "provenance": "pack Customer Service_Reference.pdf, page 13 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order booking ticket",
       "bindsTo": "OrderBookingTicketServiceWorkspaceView",
       "columns": [
        "OrderBookingTicketServiceWorkspaceView.order",
        "Customer",
        "OrderBookingTicketServiceWorkspaceView.purchaseDate",
        "OrderBookingTicketServiceWorkspaceView.channel",
        "OrderBookingTicketServiceWorkspaceView.products",
        "OrderBookingTicketServiceWorkspaceView.tickets",
        "Event",
        "OrderBookingTicketServiceWorkspaceView.dateTime",
        "OrderBookingTicketServiceWorkspaceView.amount",
        "OrderBookingTicketServiceWorkspaceView.payment",
        "OrderBookingTicketServiceWorkspaceView.fulfillment",
        "OrderBookingTicketServiceWorkspaceView.ticketStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Customer Entitlement”, “Current”, “Available”.",
       "provenance": "pack Customer Service_Reference.pdf, page 13 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setOrderBookingTicket"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order booking ticket list.",
   "error": "Could not load. Names which read failed and leaves the order booking ticket untouched.",
   "emptyFirstRun": "No order booking ticket yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order booking ticket are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setOrderBookingTicket",
    "contract": "marketing-crm",
    "purpose": "Order, Booking & Ticket Service Workspace",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "OrderBookingTicketServiceWorkspaceView.order",
    "Customer",
    "OrderBookingTicketServiceWorkspaceView.purchaseDate",
    "OrderBookingTicketServiceWorkspaceView.channel",
    "OrderBookingTicketServiceWorkspaceView.products",
    "OrderBookingTicketServiceWorkspaceView.tickets"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-014",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-014"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 13. 10 of 21 labels bound to a contract property; 21 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-015",
  "name": "Refund, Compensation & Service Exception Workspace",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.7",
   "page": 15
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/refund-compensation-service-exception-workspace-sup-015",
   "component": "apps/venue-support-web/src/routes/support/RefundCompensationServiceExceptionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-009"
   ],
   "exitTo": [
    "SUP-009"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-009, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-009",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F134 step 12→13",
     "operation": "setRefundCompensationService"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Refunds, compensation and service exceptions are governed by applicable policies, financial limits and approval authorities.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage cases requiring money, compensation, goodwill or policy exceptions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Full Refund, Partial Refund, Wallet Credit, Voucher, Complimentary Ticket, Fee Waiver, Policy Exception. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Customer Service_Reference.pdf, page 15 §Support"
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
       "label": "Every refund compensation service",
       "columns": [
        "RefundCompensationServiceExceptionWorkspaceView.originalTransaction",
        "RefundCompensationServiceExceptionWorkspaceView.amountPaid",
        "RefundCompensationServiceExceptionWorkspaceView.amountUsed",
        "RefundCompensationServiceExceptionWorkspaceView.refundableAmount",
        "RefundCompensationServiceExceptionWorkspaceView.previousRefund",
        "RefundCompensationServiceExceptionWorkspaceView.fees",
        "RefundCompensationServiceExceptionWorkspaceView.proposedRefund",
        "RefundCompensationServiceExceptionWorkspaceView.proposedCompensation"
       ],
       "bindsTo": "RefundCompensationServiceExceptionWorkspaceView",
       "operation": "setRefundCompensationService",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected refund compensation service",
       "bindsTo": "RefundCompensationServiceExceptionWorkspaceView",
       "columns": [
        "RefundCompensationServiceExceptionWorkspaceView.originalTransaction",
        "RefundCompensationServiceExceptionWorkspaceView.amountPaid",
        "RefundCompensationServiceExceptionWorkspaceView.amountUsed",
        "RefundCompensationServiceExceptionWorkspaceView.refundableAmount",
        "RefundCompensationServiceExceptionWorkspaceView.previousRefund",
        "RefundCompensationServiceExceptionWorkspaceView.fees",
        "RefundCompensationServiceExceptionWorkspaceView.proposedRefund",
        "RefundCompensationServiceExceptionWorkspaceView.proposedCompensation"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Requested Exception”, “Up to AED 200”, “Above AED 1,000”, “Compensation Budget”.",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Full Refund",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partial Refund",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Service Credit",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet Credit",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Voucher",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Complimentary Ticket",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Fee Waiver",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Policy Exception",
       "provenance": "pack Customer Service_Reference.pdf, page 15 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund compensation service list.",
   "error": "Could not load. Names which read failed and leaves the refund compensation service untouched.",
   "emptyFirstRun": "No refund compensation service yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refund compensation service are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRefundCompensationService",
    "contract": "marketing-crm",
    "purpose": "Refund, Compensation & Service Exception Workspace",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "RefundCompensationServiceExceptionWorkspaceView.originalTransaction",
    "RefundCompensationServiceExceptionWorkspaceView.amountPaid",
    "RefundCompensationServiceExceptionWorkspaceView.amountUsed",
    "RefundCompensationServiceExceptionWorkspaceView.refundableAmount",
    "RefundCompensationServiceExceptionWorkspaceView.previousRefund",
    "RefundCompensationServiceExceptionWorkspaceView.fees"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-015",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-015"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 15. 8 of 8 labels bound to a contract property; 16 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-016",
  "name": "Escalation, Collaboration & Internal Resolution",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.8",
   "page": 16
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/escalation-collaboration-internal-resolution-sup-016",
   "component": "apps/venue-support-web/src/routes/support/EscalationCollaborationInternalResolution.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-009"
   ],
   "exitTo": [
    "SUP-009"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-009, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-009",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F134 step 14→15",
     "operation": "listEscalationCollaborationInternal"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Agents can obtain assistance from internal departments while retaining one customer-facing case, owner and audit trail.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Allow Customer Service to collaborate with other TICVAI departments without losing ownership of the customer case.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Customer Service_Reference.pdf, page 16 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Assignee",
       "provenance": "pack Customer Service_Reference.pdf, page 16 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Request",
       "provenance": "pack Customer Service_Reference.pdf, page 16 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Customer Service_Reference.pdf, page 16 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Due Date",
       "provenance": "pack Customer Service_Reference.pdf, page 16 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Related Case",
       "provenance": "pack Customer Service_Reference.pdf, page 16 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Related Transaction",
       "provenance": "pack Customer Service_Reference.pdf, page 16 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Attachments",
       "provenance": "pack Customer Service_Reference.pdf, page 16 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The escalation collaboration internal configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the escalation collaboration internal untouched.",
   "emptyFirstRun": "No escalation collaboration internal configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEscalationCollaborationInternal",
    "contract": "marketing-crm",
    "purpose": "Escalation, Collaboration & Internal Resolution",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-016",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-016"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 8 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-017",
  "name": "Case Resolution, Closure & Customer Feedback",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.9",
   "page": 17
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/case-resolution-closure-customer-feedback-sup-017",
   "component": "apps/venue-support-web/src/routes/support/CaseResolutionClosureCustomerFeedback.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-009"
   ],
   "exitTo": [
    "SUP-009"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-009, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-009",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F134 step 16→17",
     "operation": "listCaseResolutionClosure"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every closed case has a clear resolution, root cause, customer communication and auditable outcome.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Where configured, send) and no display directory — it is settings, not a population",
  "purpose": "Govern how cases are resolved and formally closed.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Resolution Category",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Resolution Summary",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Action Taken",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Financial Impact",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Compensation",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Root Cause",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Resolved By",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Resolution Date",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer Notification",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Payment",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "System",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Integration",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Operational",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Content",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Policy",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Staff",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Unknown",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Capture"
      },
      {
       "kind": "selectField",
       "label": "CSAT survey",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Where configured, send"
      },
      {
       "kind": "selectField",
       "label": "Service rating",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Where configured, send"
      },
      {
       "kind": "selectField",
       "label": "Feedback request",
       "provenance": "pack Customer Service_Reference.pdf, page 17 §Where configured, send"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The case resolution closure configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the case resolution closure untouched.",
   "emptyFirstRun": "No case resolution closure configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCaseResolutionClosure",
    "contract": "marketing-crm",
    "purpose": "Case Resolution, Closure & Customer Feedback",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-017",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-017"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 17. 0 of 0 labels bound to a contract property; 22 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-018",
  "name": "AI Customer Service Copilot & Knowledge Workspace",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "1",
   "number": "10.1.10",
   "page": 19
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/ai-customer-service-copilot-knowledge-workspace-sup-018",
   "component": "apps/venue-support-web/src/routes/support/AiCustomerServiceCopilotKnowledgeWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-009"
   ],
   "exitTo": [
    "SUP-009"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-009, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "Agents receive explainable, context-aware AI assistance that reduces handling time and improves consistency without bypassing TICVAI's policies, permissions or transactional systems. Board 1 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create the AI intelligence layer assisting agents throughout the service journey. This should not be a simple chatbot added to the side of the screen. It should understand the customer + transaction + policy + case context. Board 1 focused on the individual customer-service agent and individual customer case. Board 2 moves one level higher and provides the supervisor, contact-center manager, operations manager and service leadership layer.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Review → Execute. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Customer Service_Reference.pdf, page 19 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Customer Service_Reference.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Customer Service_Reference.pdf, page 19"
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
       "label": "Review → Execute",
       "provenance": "pack Customer Service_Reference.pdf, page 19 §Actions"
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
       "impliedBy": "setCustomerServiceCopilot"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer service copilot list.",
   "error": "Could not load. Names which read failed and leaves the customer service copilot untouched.",
   "emptyFirstRun": "No customer service copilot yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer service copilot are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCustomerServiceCopilot",
    "contract": "marketing-crm",
    "purpose": "AI Customer Service Copilot & Knowledge Workspace",
    "trigger": "onAction"
   },
   {
    "operationId": "configureAssistantProfile",
    "contract": "ai",
    "purpose": "Define an assistant profile",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAssistantProfiles",
    "contract": "ai",
    "purpose": "Assistant profiles",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-018",
   "workshopBoard": "wireframes/WS42 Customer Service Board 1.dc.html#sup-018"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 19. 0 of 0 labels bound to a contract property; 1 of 96 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "profileKey",
     "from": "navigation"
    }
   ]
  },
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
 "configureAssistantProfile": {
  "method": "PUT",
  "path": "/assistant-profiles/{profileKey}",
  "contract": "ai",
  "summary": "Define an assistant profile",
  "permission": "AI_CONFIGURE",
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
  "requestBody": "AiAssistantProfile",
  "responds": "AiAssistantProfile"
 },
 "createCaseClassificationIntelligent": {
  "method": "POST",
  "path": "/case-classification-intelligent",
  "contract": "marketing-crm",
  "summary": "Case Creation, Classification & Intelligent Routing",
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
  "requestBody": "CaseCreationClassificationIntelligentRoutingInput",
  "responds": "CaseCreationClassificationIntelligentRoutingView"
 },
 "listAssistantProfiles": {
  "method": "GET",
  "path": "/assistant-profiles",
  "contract": "ai",
  "summary": "Assistant profiles",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "audience",
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
 "listCaseCategories": {
  "method": "GET",
  "path": "/case-categories",
  "contract": "marketing-crm",
  "summary": "List case categories and subcategories",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "parentCategoryId",
    "in": "query",
    "required": false
   },
   {
    "name": "topLevelOnly",
    "in": "query",
    "required": false
   },
   {
    "name": "isActive",
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
 "listCaseResolutionClosure": {
  "method": "GET",
  "path": "/case-resolution-closure",
  "contract": "marketing-crm",
  "summary": "Case Resolution, Closure & Customer Feedback",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "caseId",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "resolutionCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "rootCause",
    "in": "query",
    "required": false
   },
   {
    "name": "canClose",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
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
 "listCustomerService": {
  "method": "GET",
  "path": "/customer-service",
  "contract": "marketing-crm",
  "summary": "Customer Service Command Center",
  "permission": "CASE_VIEW",
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
    "name": "agentPrincipalId",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "CustomerServiceCommandCenterView"
 },
 "listCustomerServiceProfile": {
  "method": "GET",
  "path": "/customer-service-profile",
  "contract": "marketing-crm",
  "summary": "Customer 360° Service Profile",
  "permission": "CASE_VIEW",
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
    "name": "subjectId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "Customer360ServiceProfileView"
 },
 "listEscalationCollaborationInternal": {
  "method": "GET",
  "path": "/escalation-collaboration-internal",
  "contract": "marketing-crm",
  "summary": "Escalation, Collaboration & Internal Resolution",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "caseId",
    "in": "query",
    "required": false
   },
   {
    "name": "department",
    "in": "query",
    "required": false
   },
   {
    "name": "assigneePrincipalId",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "escalationType",
    "in": "query",
    "required": false
   },
   {
    "name": "overdueOnly",
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
 "listUnifiedInteractionCommunication": {
  "method": "GET",
  "path": "/unified-interaction-communication",
  "contract": "marketing-crm",
  "summary": "Unified Interaction & Communication History",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "subjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "keyword",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "agentPrincipalId",
    "in": "query",
    "required": false
   },
   {
    "name": "caseId",
    "in": "query",
    "required": false
   },
   {
    "name": "orderId",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketId",
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
 "setCaseInvestigationResolution": {
  "method": "PUT",
  "path": "/case-investigation-resolution",
  "contract": "marketing-crm",
  "summary": "Link a record to a case",
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
  "requestBody": "CaseInvestigationResolutionWorkspaceInput",
  "responds": "CaseInvestigationResolutionWorkspaceView"
 },
 "setCustomerServiceCopilot": {
  "method": "PUT",
  "path": "/customer-service-copilot",
  "contract": "marketing-crm",
  "summary": "Configure the customer-service copilot",
  "permission": "AI_CONFIGURE",
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
  "requestBody": "AiCustomerServiceCopilotKnowledgeWorkspaceInput",
  "responds": "AiCustomerServiceCopilotKnowledgeWorkspaceView"
 },
 "setOrderBookingTicket": {
  "method": "PUT",
  "path": "/order-booking-ticket",
  "contract": "marketing-crm",
  "summary": "Evaluate or perform a service action on an order from a case",
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
  "requestBody": "OrderBookingTicketServiceWorkspaceInput",
  "responds": "OrderBookingTicketServiceWorkspaceView"
 },
 "setRefundCompensationService": {
  "method": "PUT",
  "path": "/refund-compensation-service",
  "contract": "marketing-crm",
  "summary": "Raise or change a refund, compensation or policy-exception request on a case",
  "permission": "ORDER_REFUND",
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
  "requestBody": "RefundCompensationServiceExceptionWorkspaceInput",
  "responds": "RefundCompensationServiceExceptionWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiAssistantProfile": {
  "type": "object",
  "x-ticvai-persistence": "ai.assistant_profile",
  "description": "**One assistant runtime, many profiles** (design 5.10, C5; AIC-069..080). The profile decides the audience, roles, knowledge sources, tools, model task and guest scope: guest concierge, support chatbot and staff assistants by role.",
  "required": [
   "profileKey",
   "audience"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "profileKey": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "audience": {
    "type": "string",
    "enum": [
     "staff",
     "guest",
     "support"
    ]
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "module": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
     }
    ],
    "nullable": true
   },
   "collectionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Knowledge collections it retrieves from."
   },
   "toolKeys": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Registered tools it may propose (an assistant only reads; a change request goes to the configuration assistant, AIC-078)."
   },
   "modelTask": {
    "type": "string",
    "description": "The gateway task, e.g. `assistant.staff.answer`. The visit planner agent (29 September, MOB-6) is profile `planner.guest` with task `planner.guest.refine` and the five `venue-map` visit-plan tools. The app publishing guide (M24-08) is profile `guide.appPublishing` with task `assistant.staff.answer`, grounded on the platform's store-publishing collection only."
   },
   "guestCapabilityScope": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "For a guest profile: the same values as `AiPolicy.guestCapabilityScope`, narrowed."
   },
   "locales": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "handoverTarget": {
    "type": "string",
    "nullable": true,
    "description": "Where \"ask a person\" goes: a support queue or a staff role."
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiCustomerServiceCopilotKnowledgeWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.service_copilot_config",
  "description": "The customer-service copilot's configuration for one scope (pack 10.1.10). A field left out takes its default, not its old value.",
  "required": [
   "scopeLevel",
   "dataSources",
   "draftChannels"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "venue"
    ]
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005), and the upsert key: one row per scope."
   },
   "isEnabled": {
    "type": "boolean",
    "default": false
   },
   "dataSources": {
    "type": "array",
    "description": "The authorised data the copilot may read, always within the asking agent's own permissions.",
    "items": {
     "type": "string",
     "enum": [
      "customer",
      "cases",
      "orders",
      "tickets",
      "products",
      "servicePolicies",
      "pricing",
      "payments",
      "membership",
      "wallet",
      "groupBookings",
      "interactionHistory",
      "knowledgeBase"
     ]
    }
   },
   "knowledgeCollectionIds": {
    "type": "array",
    "description": "`ai.knowledge_collection` rows holding service procedures, product information, refund rules, ticket policies, venue instructions, FAQs and internal SOPs.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "draftChannels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "email",
      "chat",
      "whatsapp",
      "caseResponse",
      "internalEscalation"
     ]
    }
   },
   "brandTone": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true,
    "description": "Tone guidance applied to every draft."
   },
   "replyInCustomerLanguage": {
    "type": "boolean",
    "default": true
   },
   "autoSend": {
    "type": "array",
    "default": [],
    "description": "Channels where an approved automation may send without an agent. Empty means every customer-facing message waits for a person.",
    "items": {
     "type": "string",
     "enum": [
      "email",
      "chat",
      "whatsapp"
     ]
    }
   },
   "patternDetection": {
    "type": "object",
    "description": "Flags a systemic problem when many cases share one cause.",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": true
     },
     "minimumCases": {
      "type": "integer",
      "minimum": 2,
      "default": 25
     },
     "windowHours": {
      "type": "integer",
      "minimum": 1,
      "maximum": 720,
      "default": 168
     }
    }
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AiCustomerServiceCopilotKnowledgeWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.service_copilot_config (new), ai.policy and ai.knowledge_collection",
  "description": "The stored configuration and what is in effect at that scope after the tenant row and the AI policy are applied.",
  "required": [
   "configuration",
   "effective"
  ],
  "properties": {
   "configuration": {
    "$ref": "#/components/schemas/AiCustomerServiceCopilotKnowledgeWorkspaceInput"
   },
   "effective": {
    "type": "object",
    "description": "The narrowest of this row, its tenant row and `getAiPolicy`.",
    "properties": {
     "isEnabled": {
      "type": "boolean"
     },
     "dataSources": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "draftChannels": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "autoSend": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "aiCapabilities": {
      "type": "array",
      "description": "`AiPolicy.enabledCapabilities` at this scope.",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "knowledgeCollections": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "documentCount": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   }
  }
 },
 "CaseCategory": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_category",
  "description": "**The venue's case taxonomy**: categories and, under them, subcategories (`parentCategoryId`). `Case.categoryId` and the routing rules' `match.categoryIds` point here; `createCaseClassificationIntelligent` recommends one. Maintained by `setCaseCategoryDefinition`, read by `listCaseCategories` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n",
  "required": [
   "id",
   "code",
   "name",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 60
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "parentCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set on a subcategory; null on a top-level category."
   },
   "defaultPriority": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CasePriority"
     }
    ],
    "nullable": true,
    "description": "The priority a case in this category starts at before routing factors apply."
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
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
 "CaseCreationClassificationIntelligentRoutingInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the case itself is raised with `createCase`",
  "description": "The case as the agent has captured it so far (pack 10.1.4 Case Creation). Every field maps onto `CreateCaseRequest` or onto a linked record.",
  "required": [
   "subject",
   "description",
   "channel"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "The customer."
   },
   "subject": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 10000
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "description": "The source, as on `CreateCaseRequest.channel`."
   },
   "kind": {
    "$ref": "#/components/schemas/CaseKind"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "description": "Where the agent has already chosen one."
   },
   "subcategoryId": {
    "type": "string",
    "format": "uuid"
   },
   "customerSelectedPriority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "language": {
    "type": "string",
    "maxLength": 10
   },
   "relatedRecords": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "type": "object",
     "required": [
      "kind",
      "referenceId"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "order",
        "ticket",
        "payment",
        "refund",
        "membership",
        "walletTransaction",
        "groupBooking",
        "accessEvent"
       ]
      },
      "referenceId": {
       "type": "string"
      }
     }
    }
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "CaseCreationClassificationIntelligentRoutingView": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from marketing.case, marketing.sla_policy, marketing.agent_availability, marketing.case_category (new) and the routing rules; nothing is stored",
  "description": "The recommendation for one case. Every recommended value names why.",
  "required": [
   "recommendedPriority",
   "routingFactors",
   "duplicateCandidates"
  ],
  "properties": {
   "recommendedCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recommendedSubcategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recommendedPriority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "priorityBasis": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "customerSelected",
      "businessRule",
      "slaPolicy",
      "aiAssessment"
     ]
    }
   },
   "recommendedQueue": {
    "type": "string",
    "nullable": true,
    "description": "The queue's code, e.g. `eventDaySupport`."
   },
   "recommendedAssigneePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The preview; null when nobody with the skill is available."
   },
   "slaPolicyCode": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "routingFactors": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "factor"
     ],
     "properties": {
      "factor": {
       "type": "string",
       "enum": [
        "category",
        "venue",
        "product",
        "language",
        "customerType",
        "agentSkill",
        "workload",
        "priority",
        "eventProximity"
       ]
      },
      "value": {
       "type": "string"
      }
     }
    }
   },
   "aiAssessment": {
    "type": "object",
    "nullable": true,
    "description": "Where the AI policy enables `assist`; AI-derived and labelled as such.",
    "properties": {
     "signals": {
      "type": "array",
      "items": {
       "type": "string",
       "maxLength": 80
      },
      "description": "e.g. ticket issue, upcoming event, high urgency."
     },
     "explanation": {
      "type": "string",
      "maxLength": 1000
     }
    }
   },
   "duplicateCandidates": {
    "type": "array",
    "maxItems": 10,
    "description": "Open cases for the same customer and related records, best match first.",
    "items": {
     "type": "object",
     "required": [
      "caseId",
      "caseNumber",
      "status"
     ],
     "properties": {
      "caseId": {
       "type": "string",
       "format": "uuid"
      },
      "caseNumber": {
       "type": "string"
      },
      "subject": {
       "type": "string"
      },
      "status": {
       "$ref": "#/components/schemas/CaseStatus"
      },
      "matchedOn": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "customer",
         "relatedRecord",
         "subjectText"
        ]
       }
      }
     }
    }
   }
  }
 },
 "CaseInvestigationResolutionWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_linked_record",
  "x-ticvai-record-definition": "Related Records (agents can attach)",
  "description": "One link between a case and a record another contract owns. The reference is a pointer, never a copy.",
  "required": [
   "caseId",
   "kind",
   "referenceId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "caseId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "order",
     "ticket",
     "payment",
     "refund",
     "membership",
     "walletTransaction",
     "groupBooking",
     "accessEvent"
    ]
   },
   "referenceId": {
    "type": "string",
    "maxLength": 64,
    "description": "The record's id in its owning contract (orders, payments, access, wallet)."
   },
   "note": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "isActive": {
    "type": "boolean",
    "default": true,
    "description": "False unlinks; the row stays for the audit trail."
   },
   "linkedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "CaseInvestigationResolutionWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case, marketing.case_message, marketing.case_linked_record (new), marketing.sla_policy and ai.suggestion",
  "description": "The case workspace (pack 10.1.5). Recommended actions and the summary keep verified data, policy and AI recommendation apart.",
  "required": [
   "caseId",
   "caseNumber",
   "subject",
   "priority",
   "status",
   "created",
   "lastUpdated",
   "linkedRecords",
   "recommendedActions"
  ],
  "properties": {
   "caseId": {
    "type": "string",
    "format": "uuid"
   },
   "caseNumber": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "customer": {
    "type": "string",
    "nullable": true,
    "description": "The guest's name, as `Case.guestName`; null unless the caller holds GUEST_VIEW_PII."
   },
   "subject": {
    "type": "string"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "category": {
    "type": "string",
    "nullable": true,
    "description": "The category's display name."
   },
   "priority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "status": {
    "$ref": "#/components/schemas/CaseStatus"
   },
   "sla": {
    "type": "object",
    "properties": {
     "policyCode": {
      "type": "string",
      "nullable": true
     },
     "dueAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "remainingSeconds": {
      "type": "integer",
      "nullable": true,
      "description": "Negative once breached."
     },
     "isBreached": {
      "type": "boolean"
     },
     "isPaused": {
      "type": "boolean",
      "description": "True while `awaitingGuest`."
     }
    }
   },
   "owner": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The assigned agent's principal id (`Case.assignedToPrincipalId`)."
   },
   "queue": {
    "type": "string",
    "nullable": true
   },
   "created": {
    "type": "string",
    "format": "date-time",
    "description": "`Case.createdAt`."
   },
   "lastUpdated": {
    "type": "string",
    "format": "date-time"
   },
   "linkedRecords": {
    "type": "array",
    "description": "Active links, newest first.",
    "items": {
     "$ref": "#/components/schemas/CaseInvestigationResolutionWorkspaceInput"
    }
   },
   "recommendedActions": {
    "type": "array",
    "maxItems": 10,
    "items": {
     "type": "object",
     "required": [
      "action",
      "basis"
     ],
     "properties": {
      "action": {
       "type": "string",
       "enum": [
        "reply",
        "call",
        "reschedule",
        "exchange",
        "reissue",
        "requestRefund",
        "requestCompensation",
        "raiseInternalRequest",
        "escalate",
        "resolve"
       ]
      },
      "basis": {
       "type": "string",
       "enum": [
        "verifiedData",
        "policy",
        "aiRecommendation"
       ]
      },
      "reason": {
       "type": "string",
       "maxLength": 500
      },
      "policyReference": {
       "type": "string",
       "nullable": true,
       "description": "The policy the action rests on; an AI recommendation never invents one."
      }
     }
    }
   },
   "aiSummary": {
    "type": "object",
    "nullable": true,
    "description": "Where the AI policy enables `summarise`; AI-derived and labelled as such.",
    "properties": {
     "issue": {
      "type": "string"
     },
     "policy": {
      "type": "string",
      "nullable": true
     },
     "currentStatus": {
      "type": "string",
      "nullable": true
     },
     "commercialImpact": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true
     },
     "recommendedAction": {
      "type": "string",
      "nullable": true
     },
     "generatedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
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
 "CaseResolutionClosureCustomerFeedbackView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_resolution",
  "description": "One case's resolution record (pack 10.1.9), with closure checks, feedback and reopen history computed on read from marketing.case, marketing.case_message, marketing.case_internal_request, marketing.case_compensation_request, approvals.request and marketing.form_submission.",
  "required": [
   "caseId",
   "resolutionCategory",
   "resolutionSummary",
   "rootCause"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "caseId": {
    "type": "string",
    "format": "uuid"
   },
   "caseNumber": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false
   },
   "caseStatus": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CaseStatus"
     }
    ],
    "readOnly": true,
    "x-ticvai-persisted": false
   },
   "resolutionCategory": {
    "type": "string",
    "enum": [
     "informationProvided",
     "ticketReissued",
     "bookingChanged",
     "refundProcessed",
     "compensationIssued",
     "technicalIssueResolved",
     "customerError",
     "policyApplied",
     "duplicate",
     "noActionRequired",
     "other"
    ]
   },
   "resolutionSummary": {
    "type": "string",
    "minLength": 3,
    "maxLength": 2000
   },
   "actionTaken": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true
   },
   "financialImpact": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Net money refunded or credited; zero when none."
   },
   "compensationRequestIds": {
    "type": "array",
    "description": "The case's compensation requests (`setRefundCompensationService`) this resolution relied on.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "rootCause": {
    "type": "string",
    "enum": [
     "customer",
     "product",
     "payment",
     "system",
     "integration",
     "operational",
     "content",
     "policy",
     "staff",
     "unknown"
    ]
   },
   "duplicateOfCaseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `resolutionCategory` is `duplicate`."
   },
   "customerNotification": {
    "type": "object",
    "nullable": true,
    "description": "How the customer was told; the message itself is a `CaseMessage` or a `MessageDispatch`.",
    "properties": {
     "channel": {
      "$ref": "#/components/schemas/MessageChannel"
     },
     "messageId": {
      "type": "string",
      "nullable": true
     },
     "sentAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   },
   "resolvedBy": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The principal who recorded it."
   },
   "resolutionDate": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "closureChecks": {
    "type": "object",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "properties": {
     "requiredCustomerResponseSent": {
      "type": "boolean"
     },
     "financialActionCompleteOrTracked": {
      "type": "boolean"
     },
     "internalTasksCompleted": {
      "type": "boolean"
     },
     "requiredApprovalsComplete": {
      "type": "boolean"
     },
     "resolutionDocumented": {
      "type": "boolean"
     }
    }
   },
   "canClose": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false
   },
   "feedback": {
    "type": "object",
    "readOnly": true,
    "nullable": true,
    "x-ticvai-persisted": false,
    "description": "Null where no survey is configured for case resolution.",
    "properties": {
     "surveyStatus": {
      "type": "string",
      "enum": [
       "scheduled",
       "sent",
       "responded",
       "expired"
      ]
     },
     "formSubmissionId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "score": {
      "type": "number",
      "nullable": true
     },
     "scaleMax": {
      "type": "integer",
      "nullable": true
     },
     "respondedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   },
   "reopenCount": {
    "type": "integer",
    "minimum": 0,
    "readOnly": true,
    "x-ticvai-persisted": false
   },
   "lastReopenReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "`reopenCase`'s reason; `refundFailed` when the system reopened it after a refund failed."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
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
 "ConsentDecision": {
  "type": "string",
  "enum": [
   "granted",
   "withdrawn",
   "notAsked"
  ]
 },
 "Customer360ServiceProfileView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.guest_profile, pii.subject, pii.subject_contact, marketing.loyalty_position, marketing.guest_preference, marketing.consent_record, marketing.suppression, marketing.case, orders.sales_order, orders.reservation, orders.group_booking, access.entitlement and wallet.balance",
  "description": "The service view of one guest. Fields the caller may not see are null, never omitted.",
  "required": [
   "customerId",
   "customerSince",
   "openCases",
   "serviceAlerts"
  ],
  "properties": {
   "customerId": {
    "type": "string",
    "format": "uuid",
    "description": "The guest's `subjectId`."
   },
   "customerName": {
    "type": "string",
    "nullable": true,
    "description": "Null unless the caller holds GUEST_VIEW_PII."
   },
   "customerType": {
    "type": "string",
    "enum": [
     "individual",
     "member",
     "groupOrganiser",
     "corporate",
     "partner"
    ]
   },
   "membershipStatus": {
    "type": "string",
    "enum": [
     "none",
     "active",
     "expiring",
     "lapsed"
    ]
   },
   "loyaltyTier": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "maxLength": 10,
    "nullable": true
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "contactDetails": {
    "type": "object",
    "description": "Masked (e.g. `j***@example.com`, `+971 ** *** 4821`) unless the caller holds GUEST_VIEW_PII.",
    "properties": {
     "email": {
      "type": "string",
      "nullable": true
     },
     "phone": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "customerSince": {
    "type": "string",
    "format": "date-time"
   },
   "customerValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Lifetime net spend across the tenant."
   },
   "openCases": {
    "type": "integer",
    "minimum": 0
   },
   "riskAttentionIndicator": {
    "type": "string",
    "enum": [
     "none",
     "attention",
     "risk"
    ],
    "description": "`attention` with an open complaint or an unresolved refund case; `risk` with a breached SLA or a repeat contact on the same issue."
   },
   "upcomingTickets": {
    "type": "integer",
    "minimum": 0
   },
   "activeMembership": {
    "type": "object",
    "nullable": true,
    "properties": {
     "membershipId": {
      "type": "string"
     },
     "planName": {
      "type": "string"
     },
     "expiresAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   },
   "walletBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "activeReservations": {
    "type": "integer",
    "minimum": 0
   },
   "futureGroupBookings": {
    "type": "integer",
    "minimum": 0
   },
   "openOrders": {
    "type": "integer",
    "minimum": 0
   },
   "serviceAlerts": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "type": "object",
     "required": [
      "kind",
      "message"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "eventSoon",
        "unresolvedRefundCase",
        "membershipExpiring",
        "openComplaint",
        "communicationRestricted"
       ]
      },
      "message": {
       "type": "string"
      },
      "referenceId": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "preferredCommunicationChannel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "nullable": true
   },
   "marketingConsent": {
    "$ref": "#/components/schemas/ConsentDecision"
   },
   "accessibilityRequirements": {
    "type": "array",
    "nullable": true,
    "description": "Null unless the caller holds GUEST_VIEW_PII.",
    "items": {
     "type": "string"
    }
   },
   "communicationRestrictions": {
    "type": "array",
    "description": "Channels the guest must not be contacted on (`getSuppressionList`).",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "aiSummary": {
    "type": "object",
    "nullable": true,
    "description": "Where the AI policy enables `summarise`. AI-derived and labelled as such.",
    "properties": {
     "text": {
      "type": "string",
      "maxLength": 2000
     },
     "generatedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "CustomerServiceCommandCenterView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case, marketing.case_message, marketing.case_internal_request (new), marketing.case_compensation_request (new), marketing.sla_policy and approvals.request",
  "description": "One agent's workload for the filters given. \"Today\" is the venue's local day. Counts are of cases assigned to the agent unless the name says otherwise.",
  "required": [
   "myOpenCases",
   "slaAtRisk",
   "slaBreached",
   "workQueue",
   "todaysTasks",
   "liveAlerts"
  ],
  "properties": {
   "myOpenCases": {
    "type": "integer",
    "minimum": 0,
    "description": "Status not `resolved` or `closed`."
   },
   "newCases": {
    "type": "integer",
    "minimum": 0,
    "description": "Assigned to the agent and still `open` (not yet picked up)."
   },
   "casesDueToday": {
    "type": "integer",
    "minimum": 0,
    "description": "Open, with `slaDueAt` falling today."
   },
   "slaAtRisk": {
    "type": "integer",
    "minimum": 0,
    "description": "Open, not breached, with less than 25% of the SLA window left."
   },
   "slaBreached": {
    "type": "integer",
    "minimum": 0,
    "description": "Open with `Case.isSlaBreached` true."
   },
   "awaitingCustomer": {
    "type": "integer",
    "minimum": 0,
    "description": "Status `awaitingGuest`."
   },
   "awaitingInternalTeam": {
    "type": "integer",
    "minimum": 0,
    "description": "Open, with at least one open internal request."
   },
   "escalatedCases": {
    "type": "integer",
    "minimum": 0
   },
   "resolvedToday": {
    "type": "integer",
    "minimum": 0
   },
   "averageResolutionSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Mean of `resolvedAt - recordedAt - slaPausedSeconds` over the agent's cases resolved in the last 30 days; null when none."
   },
   "workQueue": {
    "type": "array",
    "maxItems": 50,
    "description": "The agent's 50 most urgent open cases.",
    "items": {
     "type": "object",
     "required": [
      "caseId",
      "caseNumber",
      "subject",
      "status",
      "priority"
     ],
     "properties": {
      "caseId": {
       "type": "string",
       "format": "uuid"
      },
      "caseNumber": {
       "type": "string"
      },
      "customer": {
       "type": "string",
       "nullable": true,
       "description": "The guest's name, resolved from `pii.subject` as `Case.guestName` is; null unless the caller holds GUEST_VIEW_PII."
      },
      "subjectId": {
       "type": "string",
       "format": "uuid",
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
      "category": {
       "type": "string",
       "nullable": true,
       "description": "The category's display name."
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "priority": {
       "$ref": "#/components/schemas/CasePriority"
      },
      "status": {
       "$ref": "#/components/schemas/CaseStatus"
      },
      "assignedAgentPrincipalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "slaDueAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "slaRemainingSeconds": {
       "type": "integer",
       "nullable": true,
       "description": "Negative once breached."
      },
      "lastInteractionAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true,
       "description": "The latest `CaseMessage.recordedAt`."
      },
      "nextAction": {
       "type": "string",
       "nullable": true,
       "enum": [
        "respondToCustomer",
        "followUpInternalRequest",
        "awaitApproval",
        "proposeResolution",
        "closeCase"
       ]
      },
      "aiPriorityRank": {
       "type": "integer",
       "minimum": 1,
       "nullable": true,
       "description": "Where AI prioritisation is enabled (`getAiPolicy`), the case's rank in the queue."
      },
      "aiPriorityFactors": {
       "type": "array",
       "description": "What raised the rank; AI-derived and labelled as such on screen.",
       "items": {
        "type": "string",
        "enum": [
         "sla",
         "customerImpact",
         "transactionValue",
         "eventProximity",
         "customerSentiment",
         "caseAge",
         "operationalUrgency"
        ]
       }
      }
     }
    }
   },
   "todaysTasks": {
    "type": "array",
    "maxItems": 100,
    "description": "Work due today derived from the agent's cases, earliest `dueAt` first.",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "caseId"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "callCustomer",
        "respondToComplaint",
        "reviewRefundRequest",
        "followUpFinance",
        "followUpInternalRequest",
        "reissueTicket",
        "requestSupervisorApproval"
       ]
      },
      "caseId": {
       "type": "string",
       "format": "uuid"
      },
      "referenceId": {
       "type": "string",
       "nullable": true,
       "description": "The internal request, compensation request or approval request behind it."
      },
      "dueAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "liveAlerts": {
    "type": "array",
    "maxItems": 50,
    "description": "Newest first.",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "caseId",
      "raisedAt"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "slaRisk",
        "slaBreached",
        "customerWaiting",
        "internalRequestOverdue",
        "approvalDecided"
       ]
      },
      "caseId": {
       "type": "string",
       "format": "uuid"
      },
      "message": {
       "type": "string"
      },
      "raisedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
 },
 "EscalationCollaborationInternalResolutionView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_internal_request",
  "description": "One internal request from a case to a department (pack 10.1.8 Internal Request). The case keeps its owner; this is the department's piece of work.",
  "required": [
   "id",
   "caseId",
   "department",
   "request",
   "priority",
   "escalationType"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7; equals the `Idempotency-Key` header on the write."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "caseId": {
    "type": "string",
    "format": "uuid"
   },
   "department": {
    "type": "string",
    "enum": [
     "ticketing",
     "finance",
     "operations",
     "accessControl",
     "membership",
     "crm",
     "fnb",
     "retail",
     "groupSales",
     "technicalSupport",
     "venueManagement",
     "management"
    ]
   },
   "assigneePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "request": {
    "type": "string",
    "minLength": 3,
    "maxLength": 2000
   },
   "priority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "escalationType": {
    "type": "string",
    "enum": [
     "functional",
     "supervisor",
     "management",
     "technical",
     "financial",
     "emergencyEventDay"
    ]
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "relatedTransaction": {
    "type": "object",
    "nullable": true,
    "properties": {
     "kind": {
      "type": "string",
      "enum": [
       "order",
       "payment",
       "refund",
       "walletTransaction",
       "groupBooking"
      ]
     },
     "referenceId": {
      "type": "string"
     }
    }
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "inProgress",
     "completed",
     "cancelled"
    ],
    "default": "open"
   },
   "response": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true,
    "description": "The department's answer; required to complete."
   },
   "isOverdue": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "Computed on read; open or in progress past `dueAt`."
   },
   "aiRecommendedDepartment": {
    "type": "string",
    "readOnly": true,
    "nullable": true,
    "x-ticvai-persisted": false,
    "description": "Where the AI policy enables `assist`; the department AI suggests from the case context."
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "nullable": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
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
 "OrderBookingTicketServiceWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_service_action",
  "x-ticvai-record-definition": "Permitted Service Actions (one per executed action)",
  "description": "One service action on an order, taken from a case. Only an `execute` stores a row.",
  "required": [
   "id",
   "mode",
   "orderId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7; equals the `Idempotency-Key` header."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "mode": {
    "type": "string",
    "enum": [
     "evaluate",
     "execute"
    ]
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "description": "Required with `execute`; the action is recorded on this case."
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Omit for the whole order."
   },
   "action": {
    "type": "string",
    "description": "Required with `execute`.",
    "enum": [
     "resendTicket",
     "downloadTicket",
     "reissue",
     "transfer",
     "changeName",
     "reschedule",
     "exchange",
     "upgrade",
     "cancel"
    ]
   },
   "targetPerformanceId": {
    "type": "string",
    "format": "uuid",
    "description": "For `reschedule` and `exchange`, the option chosen from the evaluation."
   },
   "targetProductId": {
    "type": "string",
    "format": "uuid",
    "description": "For `exchange` and `upgrade`."
   },
   "recipientSubjectId": {
    "type": "string",
    "format": "uuid",
    "description": "For `transfer` and `changeName`, the new ticket holder."
   },
   "deliveryChannel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "description": "For `resendTicket`."
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "completed",
     "pendingPayment",
     "refused",
     "failed"
    ]
   },
   "downstreamOperation": {
    "type": "string",
    "readOnly": true,
    "description": "The operation that performed it, e.g. `rescheduleOrder`."
   },
   "downstreamReference": {
    "type": "string",
    "readOnly": true,
    "nullable": true
   },
   "performedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "OrderBookingTicketServiceWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over orders.sales_order, orders.order_line, orders.payment, access.entitlement, marketing.case_service_action (new) and the policies each owning operation reads",
  "description": "The order as a service agent sees it, what may be done to it, and what was done.",
  "required": [
   "orderId",
   "order",
   "availableActions"
  ],
  "properties": {
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "order": {
    "type": "string",
    "description": "The order number shown to the guest."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "purchaseDate": {
    "type": "string",
    "format": "date-time"
   },
   "channel": {
    "type": "string",
    "description": "The sales channel the order came through."
   },
   "products": {
    "type": "integer",
    "minimum": 0
   },
   "tickets": {
    "type": "integer",
    "minimum": 0
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The performance start."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "payment": {
    "type": "string",
    "enum": [
     "paid",
     "partiallyPaid",
     "unpaid",
     "partiallyRefunded",
     "refunded"
    ]
   },
   "fulfillment": {
    "type": "string",
    "enum": [
     "pending",
     "issued",
     "delivered",
     "failed"
    ]
   },
   "ticketStatus": {
    "type": "string",
    "enum": [
     "valid",
     "partiallyUsed",
     "used",
     "expired",
     "cancelled"
    ]
   },
   "availableActions": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "action",
      "isPermitted"
     ],
     "properties": {
      "action": {
       "type": "string",
       "enum": [
        "resendTicket",
        "downloadTicket",
        "reissue",
        "transfer",
        "changeName",
        "reschedule",
        "exchange",
        "upgrade",
        "cancel",
        "requestRefund"
       ]
      },
      "isPermitted": {
       "type": "boolean"
      },
      "refusedBy": {
       "type": "string",
       "nullable": true,
       "enum": [
        "ticketPolicy",
        "servicePolicy",
        "orderStatus",
        "eventDate",
        "customerEntitlement",
        "permission"
       ]
      },
      "policyReference": {
       "type": "string",
       "nullable": true
      },
      "options": {
       "type": "array",
       "description": "Alternatives for `reschedule`, `exchange` and `upgrade`, earliest first.",
       "items": {
        "type": "object",
        "properties": {
         "performanceId": {
          "type": "string",
          "format": "uuid",
          "nullable": true
         },
         "productId": {
          "type": "string",
          "format": "uuid",
          "nullable": true
         },
         "startsAt": {
          "type": "string",
          "format": "date-time",
          "nullable": true
         },
         "available": {
          "type": "boolean"
         },
         "priceDifferencePerTicket": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         },
         "priceDifferenceTotal": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         }
        }
       }
      }
     }
    }
   },
   "lastAction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderBookingTicketServiceWorkspaceInput"
     }
    ],
    "nullable": true,
    "description": "The action just executed; null on `evaluate`."
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
 "RefundCompensationServiceExceptionWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_compensation_request",
  "x-ticvai-record-definition": "Request Types",
  "description": "One refund, compensation or policy-exception request raised from a case. The order, refund and approval are references, never copies.",
  "required": [
   "id",
   "caseId",
   "requestType",
   "value",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7; equals the `Idempotency-Key` header."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "caseId": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "Required for `fullRefund`, `partialRefund`, `feeWaiver`, `upgrade` and `discount`."
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requestType": {
    "type": "string",
    "enum": [
     "fullRefund",
     "partialRefund",
     "serviceCredit",
     "walletCredit",
     "voucher",
     "complimentaryTicket",
     "feeWaiver",
     "upgrade",
     "discount",
     "policyException"
    ]
   },
   "value": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "The money value requested; for a complimentary ticket or upgrade, its face value. This is what the approval thresholds are compared with."
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 1000
   },
   "isPolicyException": {
    "type": "boolean",
    "default": false,
    "description": "True when the standard policy would not allow it; always needs approval."
   },
   "exceptionReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true,
    "description": "Required when `isPolicyException` is true."
   },
   "submit": {
    "type": "boolean",
    "default": false,
    "description": "False saves a draft; true routes it.",
    "writeOnly": true
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "draft",
     "pendingApproval",
     "approved",
     "declined",
     "fulfilled",
     "failed",
     "withdrawn"
    ]
   },
   "approvalRequestId": {
    "type": "string",
    "readOnly": true,
    "nullable": true
   },
   "fulfilmentOperation": {
    "type": "string",
    "readOnly": true,
    "nullable": true,
    "description": "e.g. `createRefund`, `topUpWallet`."
   },
   "fulfilmentReference": {
    "type": "string",
    "readOnly": true,
    "nullable": true,
    "description": "The refund, wallet transaction or voucher it produced."
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "RefundCompensationServiceExceptionWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case_compensation_request (new), orders.sales_order, orders.refund, orders.order_fee, orders.refund_policy and approvals.request",
  "description": "The request, the order's financial context, the policy evaluation and who must approve.",
  "required": [
   "request",
   "approvalLevel"
  ],
  "properties": {
   "request": {
    "$ref": "#/components/schemas/RefundCompensationServiceExceptionWorkspaceInput"
   },
   "originalTransaction": {
    "type": "string",
    "nullable": true,
    "description": "The order number."
   },
   "amountPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "amountUsed": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Value of tickets already scanned or consumed."
   },
   "refundableAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "What the refund policy's time bands allow now, less previous refunds."
   },
   "previousRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "fees": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "proposedRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "proposedCompensation": {
    "type": "object",
    "nullable": true,
    "properties": {
     "requestType": {
      "type": "string"
     },
     "value": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    }
   },
   "policyEvaluation": {
    "type": "object",
    "properties": {
     "standardPolicy": {
      "type": "string",
      "description": "The rule that applies, as the venue's refund policy states it."
     },
     "isWithinPolicy": {
      "type": "boolean"
     },
     "policyReference": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "approvalLevel": {
    "type": "string",
    "enum": [
     "agent",
     "secondUser",
     "approver"
    ],
    "description": "From the venue's `selfAuthoriseLimit`, `requiresSecondUserAbove` and `requiresApprovalAbove`; a policy exception is always `approver`."
   },
   "aiExplanation": {
    "type": "string",
    "nullable": true,
    "maxLength": 1000,
    "description": "AI-derived and labelled as such; cites a recorded policy or says none applies."
   }
  }
 },
 "UnifiedInteractionCommunicationHistoryView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case_message, marketing.conversation_message, marketing.conversation (telephony), marketing.message_dispatch and marketing.kiosk_assist_session",
  "description": "One interaction on the timeline. `social` and `whatsapp` appear only where that channel is integrated.",
  "required": [
   "id",
   "occurredAt",
   "channel",
   "direction",
   "actorKind",
   "source",
   "recordId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "description": "Stable across pages; the source and record id combined."
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "channel": {
    "type": "string",
    "enum": [
     "email",
     "phone",
     "liveChat",
     "whatsapp",
     "sms",
     "webForm",
     "mobileApp",
     "b2cPortal",
     "social",
     "posFrontDesk",
     "internalNote",
     "automatedNotification"
    ]
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest; the name is resolved on screen through `getGuestProfile` under GUEST_VIEW_PII."
   },
   "actorKind": {
    "type": "string",
    "enum": [
     "guest",
     "agent",
     "system",
     "ai"
    ]
   },
   "actorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "direction": {
    "type": "string",
    "enum": [
     "inbound",
     "outbound",
     "internal"
    ]
   },
   "subject": {
    "type": "string",
    "nullable": true
   },
   "excerpt": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "relatedCaseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "relatedOrderId": {
    "type": "string",
    "nullable": true
   },
   "relatedTicketId": {
    "type": "string",
    "nullable": true
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "sentiment": {
    "type": "string",
    "nullable": true,
    "enum": [
     "positive",
     "neutral",
     "negative"
    ],
    "description": "Where sentiment analysis is enabled; AI-derived."
   },
   "source": {
    "type": "string",
    "enum": [
     "caseMessage",
     "conversationMessage",
     "call",
     "messageDispatch",
     "kioskAssist"
    ]
   },
   "recordId": {
    "type": "string",
    "description": "The row in the source table."
   }
  }
 }
}
```
