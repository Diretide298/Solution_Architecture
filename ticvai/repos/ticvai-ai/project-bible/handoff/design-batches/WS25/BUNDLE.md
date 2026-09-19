# WS25 — Customer Service board 1

**10 screens · 10 operations · 15 schemas · 2 permissions**

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
  `MARKETING_MANAGE, MARKETING_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SUP-009` | Customer Service Command Center | listDetail | 1 | 0 | — |
| `SUP-010` | Customer 360° Service Profile | listDetail | 1 | 0 | — |
| `SUP-011` | Unified Interaction & Communication History | configEditor | 1 | 0 | — |
| `SUP-012` | Case Creation, Classification & Intelligent Routing | configEditor | 1 | 0 | — |
| `SUP-013` | Case Investigation & Resolution Workspace | listDetail | 1 | 0 | — |
| `SUP-014` | Order, Booking & Ticket Service Workspace | listDetail | 1 | 0 | — |
| `SUP-015` | Refund, Compensation & Service Exception Workspace | listDetail | 1 | 0 | — |
| `SUP-016` | Escalation, Collaboration & Internal Resolution | configEditor | 1 | 0 | — |
| `SUP-017` | Case Resolution, Closure & Customer Feedback | configEditor | 1 | 0 | — |
| `SUP-018` | AI Customer Service Copilot & Knowledge Workspace | listDetail | 1 | 0 | — |

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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — SUP-001 declares entryState.params sessionId, so an edge into it must carry them"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide every customer-service agent with a personalized operational workspace showing customers, cases, tasks, SLAs, alerts and workload.",
  "purposeNote": "An agent can immediately understand their workload, priorities, SLA exposure and required actions without navigating multiple TICVAI modules.",
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
        "CustomerServiceCommandCenterView.averageResolutionTime",
        "CustomerServiceCommandCenterView.caseId",
        "CustomerServiceCommandCenterView.customer",
        "CustomerServiceCommandCenterView.subject",
        "CustomerServiceCommandCenterView.category",
        "CustomerServiceCommandCenterView.channel",
        "CustomerServiceCommandCenterView.priority",
        "CustomerServiceCommandCenterView.status",
        "CustomerServiceCommandCenterView.assignedAgent",
        "CustomerServiceCommandCenterView.slaRemaining",
        "CustomerServiceCommandCenterView.lastInteraction",
        "CustomerServiceCommandCenterView.nextAction",
        "CustomerServiceCommandCenterView.callCustomer",
        "Review refund request",
        "CustomerServiceCommandCenterView.followUpFinance",
        "Reissue ticket",
        "CustomerServiceCommandCenterView.respondToComplaint",
        "CustomerServiceCommandCenterView.requestSupervisorApproval"
       ],
       "bindsTo": "CustomerServiceCommandCenterView",
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
        "CustomerServiceCommandCenterView.averageResolutionTime",
        "CustomerServiceCommandCenterView.caseId",
        "CustomerServiceCommandCenterView.customer",
        "CustomerServiceCommandCenterView.subject",
        "CustomerServiceCommandCenterView.category",
        "CustomerServiceCommandCenterView.channel",
        "CustomerServiceCommandCenterView.priority",
        "CustomerServiceCommandCenterView.status",
        "CustomerServiceCommandCenterView.assignedAgent",
        "CustomerServiceCommandCenterView.slaRemaining",
        "CustomerServiceCommandCenterView.lastInteraction",
        "CustomerServiceCommandCenterView.nextAction",
        "CustomerServiceCommandCenterView.callCustomer",
        "Review refund request",
        "CustomerServiceCommandCenterView.followUpFinance",
        "Reissue ticket",
        "CustomerServiceCommandCenterView.respondToComplaint",
        "CustomerServiceCommandCenterView.requestSupervisorApproval"
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-009"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide the agent with a complete customer-service view of the customer. This should be one of the most important screens in the entire Customer Service module.",
  "purposeNote": "Agents can understand the customer's complete TICVAI relationship and relevant service context from one screen.",
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
        "Customer360ServiceProfileView.futureGroupBookingWhereApplicable",
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
        "Customer360ServiceProfileView.futureGroupBookingWhereApplicable",
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-010"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide one chronological timeline of customer interactions across supported service channels.",
  "purposeNote": "Agents can see the complete relevant conversation history without searching separate communication systems.",
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-011"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Create structured customer-service cases and ensure they reach the correct team.",
  "purposeNote": "Every service request becomes a properly categorized, prioritized and routed case with the appropriate business context attached.",
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
    "trigger": "onAction",
    "invalidates": [
     "createCaseClassificationIntelligent"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-012"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the primary workspace in which an agent investigates and resolves a case.",
  "purposeNote": "An agent can investigate and progress a customer case from one workspace with all required customer, transaction, policy and communication context visible.",
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
       "label": "Save changes",
       "provenance": "contract operation setCaseInvestigationResolution"
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
    "trigger": "onAction",
    "invalidates": [
     "setCaseInvestigationResolution"
    ]
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-013"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 11. 11 of 11 labels bound to a contract property; 11 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow customer-service agents to perform permitted ticket/order servicing without entering the underlying technical modules.",
  "purposeNote": "Agents can perform authorized ticket and booking service actions through one customer-service interface while underlying TICVAI services remain authoritative.",
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
    "trigger": "onAction",
    "invalidates": [
     "setOrderBookingTicket"
    ]
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-014"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage cases requiring money, compensation, goodwill or policy exceptions.",
  "purposeNote": "Refunds, compensation and service exceptions are governed by applicable policies, financial limits and approval authorities.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Complimentary Ticket, Fee Waiver, Policy Exception. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
    "trigger": "onAction",
    "invalidates": [
     "setRefundCompensationService"
    ]
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-015"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 15. 8 of 8 labels bound to a contract property; 11 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Allow Customer Service to collaborate with other TICVAI departments without losing ownership of the customer case.",
  "purposeNote": "Agents can obtain assistance from internal departments while retaining one customer-facing case, owner and audit trail.",
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-016"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Where configured, send) and no display directory — it is settings, not a population",
  "purpose": "Govern how cases are resolved and formally closed.",
  "purposeNote": "Every closed case has a clear resolution, root cause, customer communication and auditable outcome.",
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-017"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create the AI intelligence layer assisting agents throughout the service journey. This should not be a simple chatbot added to the side of the screen. It should understand the customer + transaction + policy + case context. Board 1 focused on the individual customer-service agent and individual customer case. Board 2 moves one level higher and provides the supervisor, contact-center manager, operations manager and service leadership layer.",
  "purposeNote": "Agents receive explainable, context-aware AI assistance that reduces handling time and improves consistency without bypassing TICVAI's policies, permissions or transactional systems. Board 1 — Final Screen Register",
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
    "trigger": "onAction",
    "invalidates": [
     "setCustomerServiceCopilot"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-018"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 19. 0 of 0 labels bound to a contract property; 1 of 96 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createCaseClassificationIntelligent": {
  "method": "POST",
  "path": "/case-classification-intelligent",
  "contract": "marketing-crm",
  "summary": "Case Creation, Classification & Intelligent Routing",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "CaseCreationClassificationIntelligentRoutingInput",
  "responds": "CaseCreationClassificationIntelligentRoutingView"
 },
 "listCaseResolutionClosure": {
  "method": "GET",
  "path": "/case-resolution-closure",
  "contract": "marketing-crm",
  "summary": "Case Resolution, Closure & Customer Feedback",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CaseResolutionClosureCustomerFeedbackView"
 },
 "listCustomerService": {
  "method": "GET",
  "path": "/customer-service",
  "contract": "marketing-crm",
  "summary": "Customer Service Command Center",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CustomerServiceCommandCenterView"
 },
 "listCustomerServiceProfile": {
  "method": "GET",
  "path": "/customer-service-profile",
  "contract": "marketing-crm",
  "summary": "Customer 360° Service Profile",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Customer360ServiceProfileView"
 },
 "listEscalationCollaborationInternal": {
  "method": "GET",
  "path": "/escalation-collaboration-internal",
  "contract": "marketing-crm",
  "summary": "Escalation, Collaboration & Internal Resolution",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EscalationCollaborationInternalResolutionView"
 },
 "listUnifiedInteractionCommunication": {
  "method": "GET",
  "path": "/unified-interaction-communication",
  "contract": "marketing-crm",
  "summary": "Unified Interaction & Communication History",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "keyword",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "agent",
    "in": "query",
    "required": false
   },
   {
    "name": "case",
    "in": "query",
    "required": false
   },
   {
    "name": "order",
    "in": "query",
    "required": false
   },
   {
    "name": "ticket",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "UnifiedInteractionCommunicationHistoryView"
 },
 "setCaseInvestigationResolution": {
  "method": "PUT",
  "path": "/case-investigation-resolution",
  "contract": "marketing-crm",
  "summary": "Case Investigation & Resolution Workspace",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "CaseInvestigationResolutionWorkspaceInput",
  "responds": "CaseInvestigationResolutionWorkspaceView"
 },
 "setCustomerServiceCopilot": {
  "method": "PUT",
  "path": "/customer-service-copilot",
  "contract": "marketing-crm",
  "summary": "AI Customer Service Copilot & Knowledge Workspace",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "AiCustomerServiceCopilotKnowledgeWorkspaceInput",
  "responds": "AiCustomerServiceCopilotKnowledgeWorkspaceView"
 },
 "setOrderBookingTicket": {
  "method": "PUT",
  "path": "/order-booking-ticket",
  "contract": "marketing-crm",
  "summary": "Order, Booking & Ticket Service Workspace",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "OrderBookingTicketServiceWorkspaceInput",
  "responds": "OrderBookingTicketServiceWorkspaceView"
 },
 "setRefundCompensationService": {
  "method": "PUT",
  "path": "/refund-compensation-service",
  "contract": "marketing-crm",
  "summary": "Refund, Compensation & Service Exception Workspace",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "RefundCompensationServiceExceptionWorkspaceInput",
  "responds": "RefundCompensationServiceExceptionWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiCustomerServiceCopilotKnowledgeWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is marketing.guest_profile at 5%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What AI Customer Service Copilot & Knowledge Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "whyCanTThisCustomerReschedule": {
    "type": "string",
    "description": "“Why can't this customer reschedule?”"
   },
   "findSundaySAvailableAlternatives": {
    "type": "string",
    "description": "“Find Sunday's available alternatives.”"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "chat": {
    "type": "string",
    "description": "Chat"
   },
   "whatsapp": {
    "type": "string",
    "description": "WhatsApp"
   },
   "caseResponse": {
    "type": "string",
    "description": "Case response"
   },
   "internalEscalation": {
    "type": "string",
    "description": "Internal escalation"
   },
   "takingIntoAccount": {
    "type": "string",
    "description": "taking into account"
   },
   "customerLanguage": {
    "type": "string",
    "description": "Customer language"
   },
   "brandTone": {
    "type": "string",
    "description": "Brand tone"
   },
   "caseContext": {
    "type": "string",
    "description": "Case context"
   },
   "applicablePolicy": {
    "type": "string",
    "description": "Applicable policy"
   },
   "availability": {
    "type": "string",
    "description": "Availability"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment status"
   },
   "ticketValidity": {
    "type": "string",
    "description": "Ticket validity"
   },
   "customerBalances": {
    "type": "string",
    "description": "Customer balances"
   },
   "timeline": {
    "type": "string",
    "description": "timeline"
   },
   "caseCreationClassificationIntelligent": {
    "type": "string",
    "description": "Case Creation, Classification & Intelligent"
   },
   "collaboration": {
    "type": "string",
    "description": "collaboration"
   },
   "paymentFinanceServices": {
    "type": "string",
    "description": "Payment + Finance services"
   }
  }
 },
 "AiCustomerServiceCopilotKnowledgeWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What AI Customer Service Copilot & Knowledge Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "whyCanTThisCustomerReschedule": {
    "type": "string",
    "description": "“Why can't this customer reschedule?”"
   },
   "findSundaySAvailableAlternatives": {
    "type": "string",
    "description": "“Find Sunday's available alternatives.”"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "chat": {
    "type": "string",
    "description": "Chat"
   },
   "whatsapp": {
    "type": "string",
    "description": "WhatsApp"
   },
   "caseResponse": {
    "type": "string",
    "description": "Case response"
   },
   "internalEscalation": {
    "type": "string",
    "description": "Internal escalation"
   },
   "takingIntoAccount": {
    "type": "string",
    "description": "taking into account"
   },
   "customerLanguage": {
    "type": "string",
    "description": "Customer language"
   },
   "brandTone": {
    "type": "string",
    "description": "Brand tone"
   },
   "caseContext": {
    "type": "string",
    "description": "Case context"
   },
   "applicablePolicy": {
    "type": "string",
    "description": "Applicable policy"
   },
   "availability": {
    "type": "string",
    "description": "Availability"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment status"
   },
   "ticketValidity": {
    "type": "string",
    "description": "Ticket validity"
   },
   "customerBalances": {
    "type": "string",
    "description": "Customer balances"
   },
   "timeline": {
    "type": "string",
    "description": "timeline"
   },
   "caseCreationClassificationIntelligent": {
    "type": "string",
    "description": "Case Creation, Classification & Intelligent"
   },
   "collaboration": {
    "type": "string",
    "description": "collaboration"
   },
   "paymentFinanceServices": {
    "type": "string",
    "description": "Payment + Finance services"
   }
  }
 },
 "CaseCreationClassificationIntelligentRoutingInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is marketing.message_trigger at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Case Creation, Classification & Intelligent Routing submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "subject": {
    "type": "string",
    "description": "Subject"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "subcategory": {
    "type": "string",
    "description": "Subcategory"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "relatedOrder": {
    "type": "string",
    "description": "Related Order"
   },
   "relatedTicket": {
    "type": "string",
    "description": "Related Ticket"
   },
   "relatedPayment": {
    "type": "string",
    "description": "Related Payment"
   },
   "relatedMembership": {
    "type": "string",
    "description": "Related Membership"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "ticketIssue": {
    "type": "string",
    "description": "Ticket Issue"
   },
   "bookingIssue": {
    "type": "string",
    "description": "Booking Issue"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "reschedule": {
    "type": "string",
    "description": "Reschedule"
   },
   "exchange": {
    "type": "string",
    "description": "Exchange"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyalty": {
    "type": "string",
    "description": "Loyalty"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "accessProblem": {
    "type": "string",
    "description": "Access Problem"
   },
   "complaint": {
    "type": "string",
    "description": "Complaint"
   },
   "technicalIssue": {
    "type": "string",
    "description": "Technical Issue"
   },
   "groupBooking": {
    "type": "string",
    "description": "Group Booking"
   },
   "lostTicket": {
    "type": "string",
    "description": "Lost Ticket"
   },
   "generalEnquiry": {
    "type": "string",
    "description": "General Enquiry"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "customerType": {
    "type": "string",
    "description": "Customer type"
   },
   "agentSkill": {
    "type": "string",
    "description": "Agent skill"
   },
   "workload": {
    "type": "string",
    "description": "Workload"
   },
   "eventProximity": {
    "type": "string",
    "description": "Event proximity"
   }
  }
 },
 "CaseCreationClassificationIntelligentRoutingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Case Creation, Classification & Intelligent Routing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "subject": {
    "type": "string",
    "description": "Subject"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "subcategory": {
    "type": "string",
    "description": "Subcategory"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "relatedOrder": {
    "type": "string",
    "description": "Related Order"
   },
   "relatedTicket": {
    "type": "string",
    "description": "Related Ticket"
   },
   "relatedPayment": {
    "type": "string",
    "description": "Related Payment"
   },
   "relatedMembership": {
    "type": "string",
    "description": "Related Membership"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "ticketIssue": {
    "type": "string",
    "description": "Ticket Issue"
   },
   "bookingIssue": {
    "type": "string",
    "description": "Booking Issue"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "reschedule": {
    "type": "string",
    "description": "Reschedule"
   },
   "exchange": {
    "type": "string",
    "description": "Exchange"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyalty": {
    "type": "string",
    "description": "Loyalty"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "accessProblem": {
    "type": "string",
    "description": "Access Problem"
   },
   "complaint": {
    "type": "string",
    "description": "Complaint"
   },
   "technicalIssue": {
    "type": "string",
    "description": "Technical Issue"
   },
   "groupBooking": {
    "type": "string",
    "description": "Group Booking"
   },
   "lostTicket": {
    "type": "string",
    "description": "Lost Ticket"
   },
   "generalEnquiry": {
    "type": "string",
    "description": "General Enquiry"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "customerType": {
    "type": "string",
    "description": "Customer type"
   },
   "agentSkill": {
    "type": "string",
    "description": "Agent skill"
   },
   "workload": {
    "type": "string",
    "description": "Workload"
   },
   "eventProximity": {
    "type": "string",
    "description": "Event proximity"
   }
  }
 },
 "CaseInvestigationResolutionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Case Investigation & Resolution Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "leftCustomerContext": {
    "type": "string",
    "description": "Left — Customer Context"
   },
   "customerProfileAndRelatedProducts": {
    "type": "string",
    "description": "Customer profile and related products"
   },
   "centerCaseTimeline": {
    "type": "string",
    "description": "Center — Case Timeline"
   },
   "conversationNotesActionsAndInvestigation": {
    "type": "string",
    "description": "Conversation, notes, actions and investigation"
   },
   "rightRecommendedActions": {
    "type": "string",
    "description": "Right — Recommended Actions"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "walletTransaction": {
    "type": "string",
    "description": "Wallet Transaction"
   },
   "groupBooking": {
    "type": "string",
    "description": "Group Booking"
   },
   "accessEvent": {
    "type": "string",
    "description": "Access Event"
   },
   "privateNotes": {
    "type": "string",
    "description": "Private notes"
   },
   "mentions": {
    "type": "string",
    "description": "Mentions"
   },
   "departmentNotes": {
    "type": "string",
    "description": "Department notes"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "actionHistory": {
    "type": "string",
    "description": "Action history"
   },
   "reply": {
    "type": "string",
    "description": "Reply"
   },
   "call": {
    "type": "string",
    "description": "Call"
   },
   "changeStatus": {
    "type": "string",
    "description": "Change Status"
   },
   "requestApproval": {
    "type": "string",
    "description": "Request Approval"
   }
  }
 },
 "CaseInvestigationResolutionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Case Investigation & Resolution Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "caseId": {
    "type": "string",
    "description": "Case ID"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "subject": {
    "type": "string",
    "description": "Subject"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "queue": {
    "type": "string",
    "description": "Queue"
   },
   "created": {
    "type": "string",
    "format": "date-time",
    "description": "Created"
   },
   "lastUpdated": {
    "type": "string",
    "format": "date-time",
    "description": "Last Updated"
   },
   "leftCustomerContext": {
    "type": "string",
    "description": "Left — Customer Context"
   },
   "customerProfileAndRelatedProducts": {
    "type": "string",
    "description": "Customer profile and related products"
   },
   "centerCaseTimeline": {
    "type": "string",
    "description": "Center — Case Timeline"
   },
   "conversationNotesActionsAndInvestigation": {
    "type": "string",
    "description": "Conversation, notes, actions and investigation"
   },
   "rightRecommendedActions": {
    "type": "string",
    "description": "Right — Recommended Actions"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "walletTransaction": {
    "type": "string",
    "description": "Wallet Transaction"
   },
   "groupBooking": {
    "type": "string",
    "description": "Group Booking"
   },
   "accessEvent": {
    "type": "string",
    "description": "Access Event"
   },
   "privateNotes": {
    "type": "string",
    "description": "Private notes"
   },
   "mentions": {
    "type": "string",
    "description": "Mentions"
   },
   "departmentNotes": {
    "type": "string",
    "description": "Department notes"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "actionHistory": {
    "type": "string",
    "description": "Action history"
   },
   "reply": {
    "type": "string",
    "description": "Reply"
   },
   "call": {
    "type": "string",
    "description": "Call"
   },
   "changeStatus": {
    "type": "string",
    "description": "Change Status"
   },
   "requestApproval": {
    "type": "string",
    "description": "Request Approval"
   }
  }
 },
 "CaseResolutionClosureCustomerFeedbackView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Case Resolution, Closure & Customer Feedback displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "resolutionCategory": {
    "type": "string",
    "description": "Resolution Category"
   },
   "resolutionSummary": {
    "type": "string",
    "description": "Resolution Summary"
   },
   "actionTaken": {
    "type": "string",
    "description": "Action Taken"
   },
   "financialImpact": {
    "type": "string",
    "description": "Financial Impact"
   },
   "compensation": {
    "type": "string",
    "description": "Compensation"
   },
   "rootCause": {
    "type": "string",
    "description": "Root Cause"
   },
   "resolvedBy": {
    "type": "string",
    "description": "Resolved By"
   },
   "resolutionDate": {
    "type": "string",
    "format": "date-time",
    "description": "Resolution Date"
   },
   "customerNotification": {
    "type": "string",
    "description": "Customer Notification"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "system": {
    "type": "string",
    "description": "System"
   },
   "integration": {
    "type": "string",
    "description": "Integration"
   },
   "operational": {
    "type": "string",
    "description": "Operational"
   },
   "content": {
    "type": "string",
    "description": "Content"
   },
   "policy": {
    "type": "string",
    "description": "Policy"
   },
   "staff": {
    "type": "string",
    "description": "Staff"
   },
   "unknown": {
    "type": "string",
    "description": "Unknown"
   },
   "requiredCustomerResponseSent": {
    "type": "string",
    "description": "Required customer response sent"
   },
   "financialActionCompleteOrTracked": {
    "type": "string",
    "description": "Financial action complete or tracked"
   },
   "internalTasksCompleted": {
    "type": "string",
    "description": "Internal tasks completed"
   },
   "requiredApprovalsComplete": {
    "type": "string",
    "description": "Required approvals complete"
   },
   "resolutionDocumented": {
    "type": "string",
    "description": "Resolution documented"
   },
   "csatSurvey": {
    "type": "string",
    "description": "CSAT survey"
   },
   "serviceRating": {
    "type": "string",
    "description": "Service rating"
   },
   "feedbackRequest": {
    "type": "string",
    "description": "Feedback request"
   },
   "customerReplies": {
    "type": "string",
    "description": "Customer replies"
   },
   "resolutionFails": {
    "type": "string",
    "description": "Resolution fails"
   },
   "supervisorReopens": {
    "type": "string",
    "description": "Supervisor reopens"
   }
  }
 },
 "Customer360ServiceProfileView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Customer 360° Service Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "customerName": {
    "type": "string",
    "description": "Customer Name"
   },
   "customerId": {
    "type": "string",
    "description": "Customer ID"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "membershipStatus": {
    "type": "integer",
    "description": "Membership Status"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty Tier"
   },
   "preferredLanguage": {
    "type": "string",
    "description": "Preferred Language"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "contactDetails": {
    "type": "integer",
    "description": "Contact Details"
   },
   "customerSince": {
    "type": "string",
    "description": "Customer Since"
   },
   "customerValue": {
    "type": "string",
    "description": "Customer Value"
   },
   "riskAttentionIndicator": {
    "type": "string",
    "description": "Risk/Attention Indicator"
   },
   "membershipRenewed": {
    "type": "string",
    "description": "Membership renewed"
   },
   "upcomingTickets": {
    "type": "integer",
    "description": "Upcoming Tickets"
   },
   "activeMembership": {
    "type": "integer",
    "description": "Active Membership"
   },
   "walletBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Wallet Balance"
   },
   "activeReservations": {
    "type": "integer",
    "description": "Active Reservations"
   },
   "futureGroupBookingWhereApplicable": {
    "type": "string",
    "description": "Future Group Booking where applicable"
   },
   "preferredCommunicationChannel": {
    "type": "string",
    "description": "Preferred Communication Channel"
   },
   "marketingConsent": {
    "type": "boolean",
    "description": "Marketing Consent"
   },
   "accessibilityRequirementsWhereAppropriatelyAuthorized": {
    "type": "string",
    "description": "Accessibility Requirements where appropriately authorized"
   },
   "communicationRestrictions": {
    "type": "integer",
    "description": "Communication restrictions"
   },
   "roleRestricted": {
    "type": "string",
    "description": "Role restricted"
   },
   "maskedWhereAppropriate": {
    "type": "string",
    "description": "Masked where appropriate"
   },
   "disputesRecorded": {
    "type": "string",
    "description": "disputes recorded"
   }
  }
 },
 "CustomerServiceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Customer Service Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "myOpenCases": {
    "type": "integer",
    "description": "My Open Cases"
   },
   "newCases": {
    "type": "integer",
    "description": "New Cases"
   },
   "casesDueToday": {
    "type": "string",
    "description": "Cases Due Today"
   },
   "slaAtRisk": {
    "type": "string",
    "description": "SLA At Risk"
   },
   "slaBreached": {
    "type": "string",
    "description": "SLA Breached"
   },
   "awaitingCustomer": {
    "type": "string",
    "description": "Awaiting Customer"
   },
   "awaitingInternalTeam": {
    "type": "string",
    "description": "Awaiting Internal Team"
   },
   "escalatedCases": {
    "type": "integer",
    "description": "Escalated Cases"
   },
   "resolvedToday": {
    "type": "string",
    "description": "Resolved Today"
   },
   "averageResolutionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Resolution Time"
   },
   "caseId": {
    "type": "string",
    "description": "Case ID"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "subject": {
    "type": "string",
    "description": "Subject"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "assignedAgent": {
    "type": "string",
    "description": "Assigned Agent"
   },
   "slaRemaining": {
    "type": "string",
    "description": "SLA Remaining"
   },
   "lastInteraction": {
    "type": "string",
    "format": "date-time",
    "description": "Last Interaction"
   },
   "nextAction": {
    "type": "string",
    "format": "date-time",
    "description": "Next Action"
   },
   "callCustomer": {
    "type": "string",
    "description": "Call customer"
   },
   "followUpFinance": {
    "type": "string",
    "description": "Follow up Finance"
   },
   "respondToComplaint": {
    "type": "string",
    "description": "Respond to complaint"
   },
   "requestSupervisorApproval": {
    "type": "string",
    "description": "Request supervisor approval"
   },
   "newCase": {
    "type": "integer",
    "description": "New Case"
   },
   "findCustomer": {
    "type": "string",
    "description": "Find Customer"
   },
   "findOrder": {
    "type": "string",
    "description": "Find Order"
   },
   "findTicket": {
    "type": "string",
    "description": "Find Ticket"
   },
   "findBooking": {
    "type": "string",
    "description": "Find Booking"
   }
  }
 },
 "EscalationCollaborationInternalResolutionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Escalation, Collaboration & Internal Resolution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketing": {
    "type": "string",
    "description": "Ticketing"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "operations": {
    "type": "string",
    "description": "Operations"
   },
   "accessControl": {
    "type": "string",
    "description": "Access Control"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "crm": {
    "type": "string",
    "description": "CRM"
   },
   "fB": {
    "type": "string",
    "description": "F&B"
   },
   "retail": {
    "type": "string",
    "description": "Retail"
   },
   "groupSales": {
    "type": "string",
    "description": "Group Sales"
   },
   "technicalSupport": {
    "type": "boolean",
    "description": "Technical Support"
   },
   "venueManagement": {
    "type": "string",
    "description": "Venue Management"
   },
   "management": {
    "type": "string",
    "description": "Management"
   },
   "confirmRefundTransactionStatus": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Confirm refund transaction status"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "assignee": {
    "type": "string",
    "description": "Assignee"
   },
   "request": {
    "type": "string",
    "description": "Request"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "dueDate": {
    "type": "string",
    "format": "date-time",
    "description": "Due Date"
   },
   "relatedCase": {
    "type": "string",
    "description": "Related Case"
   },
   "relatedTransaction": {
    "type": "string",
    "description": "Related Transaction"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
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
    ],
    "description": "Vocabulary listed under Escalation Types."
   }
  }
 },
 "OrderBookingTicketServiceWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Order, Booking & Ticket Service Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "changeName": {
    "type": "string",
    "description": "Change Name"
   },
   "reschedule": {
    "type": "string",
    "description": "Reschedule"
   },
   "exchange": {
    "type": "string",
    "description": "Exchange"
   },
   "requestRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Request Refund"
   },
   "saturday1600": {
    "type": "string",
    "description": "Saturday 16:00"
   },
   "sunday1400Aed0": {
    "type": "string",
    "description": "Sunday 14:00 — +AED 0"
   },
   "sunday1600Aed20Ticket": {
    "type": "string",
    "description": "Sunday 16:00 — +AED 20/ticket"
   },
   "inCustomerService": {
    "type": "string",
    "description": "in Customer Service"
   }
  }
 },
 "OrderBookingTicketServiceWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Order, Booking & Ticket Service Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "order": {
    "type": "string",
    "description": "Order"
   },
   "purchaseDate": {
    "type": "string",
    "format": "date-time",
    "description": "Purchase Date"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "products": {
    "type": "integer",
    "description": "Products"
   },
   "tickets": {
    "type": "integer",
    "description": "Tickets"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/Time"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "fulfillment": {
    "type": "string",
    "description": "Fulfillment"
   },
   "ticketStatus": {
    "type": "integer",
    "description": "Ticket Status"
   },
   "changeName": {
    "type": "string",
    "description": "Change Name"
   },
   "reschedule": {
    "type": "string",
    "description": "Reschedule"
   },
   "exchange": {
    "type": "string",
    "description": "Exchange"
   },
   "requestRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Request Refund"
   },
   "saturday1600": {
    "type": "string",
    "description": "Saturday 16:00"
   },
   "sunday1400Aed0": {
    "type": "string",
    "description": "Sunday 14:00 — +AED 0"
   },
   "sunday1600Aed20Ticket": {
    "type": "string",
    "description": "Sunday 16:00 — +AED 20/ticket"
   },
   "inCustomerService": {
    "type": "string",
    "description": "in Customer Service"
   }
  }
 },
 "RefundCompensationServiceExceptionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Refund, Compensation & Service Exception Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "fullRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Full Refund"
   },
   "partialRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partial Refund"
   },
   "serviceCredit": {
    "type": "string",
    "description": "Service Credit"
   },
   "walletCredit": {
    "type": "string",
    "description": "Wallet Credit"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "complimentaryTicket": {
    "type": "string",
    "description": "Complimentary Ticket"
   },
   "feeWaiver": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Waiver"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "policyException": {
    "type": "string",
    "description": "Policy Exception"
   },
   "agentPermitted": {
    "type": "string",
    "description": "Agent permitted"
   },
   "aed2011000": {
    "type": "string",
    "description": "AED 201–1,000"
   },
   "supervisorApproval": {
    "type": "string",
    "description": "Supervisor approval"
   },
   "managerFinanceApproval": {
    "type": "string",
    "description": "Manager/Finance approval"
   }
  }
 },
 "RefundCompensationServiceExceptionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Refund, Compensation & Service Exception Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fullRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Full Refund"
   },
   "partialRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partial Refund"
   },
   "serviceCredit": {
    "type": "string",
    "description": "Service Credit"
   },
   "walletCredit": {
    "type": "string",
    "description": "Wallet Credit"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "complimentaryTicket": {
    "type": "string",
    "description": "Complimentary Ticket"
   },
   "feeWaiver": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Waiver"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "policyException": {
    "type": "string",
    "description": "Policy Exception"
   },
   "originalTransaction": {
    "type": "string",
    "description": "Original Transaction"
   },
   "amountPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount Paid"
   },
   "amountUsed": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount Used"
   },
   "refundableAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Refundable Amount"
   },
   "previousRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Previous Refund"
   },
   "fees": {
    "type": "integer",
    "description": "Fees"
   },
   "proposedRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Proposed Refund"
   },
   "proposedCompensation": {
    "type": "string",
    "description": "Proposed Compensation"
   },
   "agentPermitted": {
    "type": "string",
    "description": "Agent permitted"
   },
   "aed2011000": {
    "type": "string",
    "description": "AED 201–1,000"
   },
   "supervisorApproval": {
    "type": "string",
    "description": "Supervisor approval"
   },
   "managerFinanceApproval": {
    "type": "string",
    "description": "Manager/Finance approval"
   }
  }
 },
 "UnifiedInteractionCommunicationHistoryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Unified Interaction & Communication History displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "email": {
    "type": "string",
    "description": "Email"
   },
   "phone": {
    "type": "string",
    "description": "Phone"
   },
   "liveChat": {
    "type": "string",
    "description": "Live Chat"
   },
   "whatsappWhereIntegrated": {
    "type": "string",
    "description": "WhatsApp where integrated"
   },
   "webForm": {
    "type": "string",
    "description": "Web Form"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "b2cPortal": {
    "type": "string",
    "description": "B2C Portal"
   },
   "socialChannelWhereIntegrated": {
    "type": "string",
    "description": "Social channel where integrated"
   },
   "posFrontDesk": {
    "type": "string",
    "description": "POS/Front Desk"
   },
   "internalNotes": {
    "type": "string",
    "description": "Internal Notes"
   },
   "automatedNotifications": {
    "type": "string",
    "description": "Automated Notifications"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/Time"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "agentSystem": {
    "type": "string",
    "description": "Agent/System"
   },
   "direction": {
    "type": "string",
    "description": "Direction"
   },
   "subject": {
    "type": "string",
    "description": "Subject"
   },
   "relatedCase": {
    "type": "string",
    "description": "Related Case"
   },
   "relatedOrder": {
    "type": "string",
    "description": "Related Order"
   },
   "relatedTicket": {
    "type": "string",
    "description": "Related Ticket"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "sentimentWhereEnabled": {
    "type": "boolean",
    "description": "Sentiment where enabled"
   }
  }
 }
}
```
