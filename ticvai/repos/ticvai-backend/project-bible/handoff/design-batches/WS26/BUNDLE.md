# WS26 — Customer Service board 2

**10 screens · 13 operations · 22 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `CASE_MANAGE, CASE_VIEW, QUEUE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SUP-019` | Contact Center Operations Command Center | commandCentre | 1 | 0 | — |
| `SUP-020` | Queue Configuration & Management | configEditor | 3 | 1 | — |
| `SUP-021` | Intelligent Routing, Skills & Assignment Engine | listDetail | 3 | 0 | — |
| `SUP-022` | SLA Policy & Service-Level Management | configEditor | 1 | 0 | — |
| `SUP-023` | Agent Workload, Availability & Workforce Control | listDetail | 1 | 0 | — |
| `SUP-024` | Escalation & Critical Case Monitor | listDetail | 1 | 0 | — |
| `SUP-025` | Quality Management & Agent Evaluation | listDetail | 1 | 0 | — |
| `SUP-026` | Customer Satisfaction, Feedback & Voice of Customer | commandCentre | 1 | 0 | — |
| `SUP-027` | Service Analytics & Root-Cause Intelligence | commandCentre | 1 | 0 | — |
| `SUP-028` | AI Contact Center Intelligence & Automation Studio | listDetail | 1 | 0 | — |

## Thin screens in this batch

**SUP-023, SUP-024, SUP-025, SUP-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "SUP-019",
  "name": "Contact Center Operations Command Center",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.1",
   "page": 24
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/contact-center-operations-command-center-sup-019",
   "component": "apps/venue-support-web/src/routes/support/ContactCenterOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-001"
   ],
   "exitTo": [
    "SUP-001",
    "SUP-020",
    "SUP-021",
    "SUP-022",
    "SUP-023",
    "SUP-024",
    "SUP-025",
    "SUP-026",
    "SUP-027",
    "SUP-028"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "SUP-001",
     "trigger": "Agent Login",
     "provenance": "derived — SUP-001 declares entryState.params challengeId and SUP-019 holds none of them. The edge carries nothing: SUP-019 is opened from SUP-001, so this edge is the way back and SUP-001 keeps its own state"
    },
    {
     "to": "SUP-020",
     "trigger": "Works in Queue Configuration & Management",
     "provenance": "flow F135 step 1→2",
     "operation": "listContact"
    },
    {
     "to": "SUP-021",
     "trigger": "Works in Intelligent Routing, Skills & Assignment Engine",
     "provenance": "flow F135 step 3→4",
     "operation": "listContact"
    },
    {
     "to": "SUP-022",
     "trigger": "Works in SLA Policy & Service-Level Management",
     "provenance": "flow F135 step 5→6",
     "operation": "listContact"
    },
    {
     "to": "SUP-023",
     "trigger": "Works in Agent Workload, Availability & Workforce Control",
     "provenance": "flow F135 step 7→8",
     "operation": "listContact"
    },
    {
     "to": "SUP-024",
     "trigger": "Works in Escalation & Critical Case Monitor",
     "provenance": "flow F135 step 9→10",
     "operation": "listContact"
    },
    {
     "to": "SUP-025",
     "trigger": "Works in Quality Management & Agent Evaluation",
     "provenance": "flow F135 step 11→12",
     "operation": "listContact"
    },
    {
     "to": "SUP-026",
     "trigger": "Works in Customer Satisfaction, Feedback & Voice of Customer",
     "provenance": "flow F135 step 13→14",
     "operation": "listContact"
    },
    {
     "to": "SUP-027",
     "trigger": "Works in Service Analytics & Root-Cause Intelligence",
     "provenance": "flow F135 step 15→16",
     "operation": "listContact"
    },
    {
     "to": "SUP-028",
     "trigger": "Works in AI Contact Center Intelligence & Automation Studio",
     "provenance": "flow F135 step 17→18",
     "operation": "listContact"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Supervisors can understand the real-time operational state of Customer Service and identify the queues, channels and issues requiring immediate intervention.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide supervisors and management with a real-time view of customer-service operations across",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search contact operations",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Drill-Down"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Channel → Queue → Agent → Case"
       ],
       "notes": "The pack filters this screen by channel → queue → agent → case — which are present is a decision the pack already made.",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Drill-Down"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Cases Today",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.casesToday"
      },
      {
       "kind": "metricTile",
       "label": "Open Cases",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Unassigned Cases",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.unassignedCases"
      },
      {
       "kind": "metricTile",
       "label": "Customers Waiting",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.customersWaiting"
      },
      {
       "kind": "metricTile",
       "label": "Critical Cases",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.criticalCases"
      },
      {
       "kind": "metricTile",
       "label": "SLA At Risk",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.slaAtRisk"
      },
      {
       "kind": "metricTile",
       "label": "SLA Breached",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.slaBreached"
      },
      {
       "kind": "metricTile",
       "label": "Cases Resolved Today",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.casesResolvedToday"
      },
      {
       "kind": "metricTile",
       "label": "First Response Time",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.averageFirstResponseSeconds"
      },
      {
       "kind": "metricTile",
       "label": "Average Resolution Time",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.averageResolutionSeconds"
      },
      {
       "kind": "metricTile",
       "label": "First Contact Resolution",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.firstContactResolutionRate"
      },
      {
       "kind": "metricTile",
       "label": "CSAT",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.csat"
      },
      {
       "kind": "metricTile",
       "label": "Active Agents",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.activeAgents"
      },
      {
       "kind": "metricTile",
       "label": "Agent Utilization",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.agentUtilization"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The contact operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the contact operations untouched.",
   "emptyFirstRun": "No contact operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the contact operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listContact",
    "contract": "marketing-crm",
    "purpose": "Contact Center Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ContactCenterOperationsCommandCenterView.casesToday",
    "Open Cases",
    "ContactCenterOperationsCommandCenterView.unassignedCases",
    "ContactCenterOperationsCommandCenterView.customersWaiting",
    "ContactCenterOperationsCommandCenterView.criticalCases",
    "ContactCenterOperationsCommandCenterView.slaAtRisk"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-019",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-019"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 24. 13 of 14 labels bound to a contract property; 15 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-020",
  "name": "Queue Configuration & Management",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.2",
   "page": 25
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/queue-configuration-management-sup-020",
   "component": "apps/venue-support-web/src/routes/support/QueueConfigurationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-019"
   ],
   "exitTo": [
    "SUP-019"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-019, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-019",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F135 step 2→3",
     "operation": "listQueues"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can configure specialized service queues and supervisors can operationally adjust them without changing application code.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure and operate the queues through which customer-service cases are organized.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Payments, Membership, Wallet, Group Sales Support, Access Control. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Customer Service_Reference.pdf, page 25 §Support configurable queues such as"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Queue Name",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Queue Code",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Languages",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supported Channels",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Operating Hours",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "SLA Profile",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supervisor",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Backup Queue",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum workload",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Overflow threshold",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Escalation threshold",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "After-hours behavior",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Backup routing",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "VIP handling",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Emergency handling",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listServiceQueues",
       "notes": "Sends `?isActive=` to `listServiceQueues`.",
       "provenance": "contract marketing-crm.yaml GET /service-queues"
      },
      {
       "kind": "dataTable",
       "label": "Every service queue",
       "bindsTo": "ServiceQueue",
       "columns": [
        "ServiceQueue.id",
        "ServiceQueue.code",
        "ServiceQueue.name",
        "ServiceQueue.overflowWaitSeconds",
        "ServiceQueue.isActive",
        "ServiceQueue.scopePath"
       ],
       "operation": "listServiceQueues",
       "provenance": "contract marketing-crm.yaml GET /service-queues"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Payments",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Support configurable queues such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Support configurable queues such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Support configurable queues such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Group Sales Support",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Support configurable queues such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Access Control",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Support configurable queues such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Save service queue definition",
       "operation": "setServiceQueueDefinition",
       "permission": "CASE_MANAGE",
       "notes": "**An upsert keyed on `code`**, which is unique in the venue and never changes once created.",
       "provenance": "contract marketing-crm.yaml PUT /service-queues"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The queue configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the queue untouched.",
   "emptyFirstRun": "No queue configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQueues",
    "contract": "queue",
    "purpose": "List queues",
    "trigger": "onLoad"
   },
   {
    "operationId": "listServiceQueues",
    "contract": "marketing-crm",
    "purpose": "List customer-service queues",
    "trigger": "onLoad"
   },
   {
    "operationId": "setServiceQueueDefinition",
    "contract": "marketing-crm",
    "purpose": "Create or change a customer-service queue",
    "trigger": "onAction",
    "invalidates": [
     "listQueues",
     "listServiceQueues"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-020",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-020"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 25 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetServiceQueueDefinition",
    "component": "modal",
    "trigger": "Save service queue definition",
    "body": "**Collects what `setServiceQueueDefinition` sends before it is called.** Required: `id`, `code`, `name`, `isActive`. Optional: `overflowWaitSeconds`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ServiceQueue",
    "confirm": {
     "label": "Save service queue definition",
     "operation": "setServiceQueueDefinition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "isActive",
      "overflowWaitSeconds",
      "scopePath"
     ]
    },
    "provenance": "contract marketing-crm.yaml PUT /service-queues"
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
  "id": "SUP-021",
  "name": "Intelligent Routing, Skills & Assignment Engine",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.3",
   "page": 27
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/intelligent-routing-skills-assignment-engine-sup-021",
   "component": "apps/venue-support-web/src/routes/support/IntelligentRoutingSkillsAssignmentEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-019"
   ],
   "exitTo": [
    "SUP-019"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-019, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-019",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F135 step 4→5",
     "operation": "setIntelligentRoutingSkill"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Customer cases are routed to appropriately skilled and available agents using governed routing rules with transparent assignment logic.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine the best agent or team to handle each customer request.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Customer Service_Reference.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Customer Service_Reference.pdf, page 27"
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
       "label": "Save changes",
       "provenance": "contract operation setIntelligentRoutingSkill"
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
       "impliedBy": "setIntelligentRoutingSkill"
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
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listServiceQueues",
       "notes": "Sends `?isActive=` to `listServiceQueues`.",
       "provenance": "contract marketing-crm.yaml GET /service-queues"
      },
      {
       "kind": "dataTable",
       "label": "Every service queue",
       "bindsTo": "ServiceQueue",
       "columns": [
        "ServiceQueue.id",
        "ServiceQueue.code",
        "ServiceQueue.name",
        "ServiceQueue.overflowWaitSeconds",
        "ServiceQueue.isActive",
        "ServiceQueue.scopePath"
       ],
       "operation": "listServiceQueues",
       "provenance": "contract marketing-crm.yaml GET /service-queues"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The intelligent routing skills list.",
   "error": "Could not load. Names which read failed and leaves the intelligent routing skills untouched.",
   "emptyFirstRun": "No intelligent routing skills yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the intelligent routing skills are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setIntelligentRoutingSkill",
    "contract": "marketing-crm",
    "purpose": "Intelligent Routing, Skills & Assignment Engine",
    "trigger": "onAction"
   },
   {
    "operationId": "listCaseCategories",
    "contract": "marketing-crm",
    "purpose": "List case categories and subcategories",
    "trigger": "onLoad"
   },
   {
    "operationId": "listServiceQueues",
    "contract": "marketing-crm",
    "purpose": "List customer-service queues",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-021",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-021"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-022",
  "name": "SLA Policy & Service-Level Management",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.4",
   "page": 29
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/sla-policy-service-level-management-sup-022",
   "component": "apps/venue-support-web/src/routes/support/SlaPolicyServiceLevelManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-019"
   ],
   "exitTo": [
    "SUP-019"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-019, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-019",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F135 step 6→7",
     "operation": "listSlaPolicyService"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "cases likely to breach.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define and monitor service-level commitments for different customer-service scenarios.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Venue operating hours. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Customer Service_Reference.pdf, page 29 §Support"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "First Response SLA",
       "provenance": "pack Customer Service_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Next Response SLA",
       "provenance": "pack Customer Service_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Resolution SLA",
       "provenance": "pack Customer Service_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Internal Escalation SLA",
       "provenance": "pack Customer Service_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund Processing SLA",
       "provenance": "pack Customer Service_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Complaint Resolution SLA",
       "provenance": "pack Customer Service_Reference.pdf, page 29 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Venue operating hours",
       "provenance": "pack Customer Service_Reference.pdf, page 29 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sla policy service-level configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the sla policy service-level untouched.",
   "emptyFirstRun": "No sla policy service-level configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSlaPolicyService",
    "contract": "marketing-crm",
    "purpose": "SLA Policy & Service-Level Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "SlaPolicyServiceLevelManagementView.withinSla",
    "SlaPolicyServiceLevelManagementView.atRisk",
    "SlaPolicyServiceLevelManagementView.breached"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-022",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-022"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 13 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-023",
  "name": "Agent Workload, Availability & Workforce Control",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.5",
   "page": 31
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/agent-workload-availability-workforce-control-sup-023",
   "component": "apps/venue-support-web/src/routes/support/AgentWorkloadAvailabilityWorkforceControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-019"
   ],
   "exitTo": [
    "SUP-019"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-019, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-019",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F135 step 8→9",
     "operation": "listAgentWorkloadAvailability"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Supervisors can understand workload distribution and rebalance service resources before queue or SLA performance deteriorates.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Give supervisors visibility and control over active customer-service resources.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every agent workload availability",
       "columns": [
        "AgentWorkloadAvailabilityWorkforceControlView.agentName",
        "AgentWorkloadAvailabilityWorkforceControlView.team",
        "AgentWorkloadAvailabilityWorkforceControlView.skills",
        "AgentWorkloadAvailabilityWorkforceControlView.languages",
        "AgentWorkloadAvailabilityWorkforceControlView.status",
        "AgentWorkloadAvailabilityWorkforceControlView.activeCases",
        "AgentWorkloadAvailabilityWorkforceControlView.chats",
        "AgentWorkloadAvailabilityWorkforceControlView.calls",
        "AgentWorkloadAvailabilityWorkforceControlView.queues[].queueName",
        "AgentWorkloadAvailabilityWorkforceControlView.slaRiskCases",
        "AgentWorkloadAvailabilityWorkforceControlView.averageHandleSeconds",
        "AgentWorkloadAvailabilityWorkforceControlView.resolutionRate",
        "AgentWorkloadAvailabilityWorkforceControlView.utilization"
       ],
       "bindsTo": "AgentWorkloadAvailabilityWorkforceControlView",
       "operation": "listAgentWorkloadAvailability",
       "provenance": "pack Customer Service_Reference.pdf, page 31 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected agent workload availability",
       "bindsTo": "AgentWorkloadAvailabilityWorkforceControlView",
       "columns": [
        "AgentWorkloadAvailabilityWorkforceControlView.agentName",
        "AgentWorkloadAvailabilityWorkforceControlView.team",
        "AgentWorkloadAvailabilityWorkforceControlView.skills",
        "AgentWorkloadAvailabilityWorkforceControlView.languages",
        "AgentWorkloadAvailabilityWorkforceControlView.status",
        "AgentWorkloadAvailabilityWorkforceControlView.activeCases",
        "AgentWorkloadAvailabilityWorkforceControlView.chats",
        "AgentWorkloadAvailabilityWorkforceControlView.calls",
        "AgentWorkloadAvailabilityWorkforceControlView.queues[].queueName",
        "AgentWorkloadAvailabilityWorkforceControlView.slaRiskCases",
        "AgentWorkloadAvailabilityWorkforceControlView.averageHandleSeconds",
        "AgentWorkloadAvailabilityWorkforceControlView.resolutionRate",
        "AgentWorkloadAvailabilityWorkforceControlView.utilization"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Authorized supervisors can”, “Resource Management Integration”.",
       "provenance": "pack Customer Service_Reference.pdf, page 31 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The agent workload availability list.",
   "error": "Could not load. Names which read failed and leaves the agent workload availability untouched.",
   "emptyFirstRun": "No agent workload availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the agent workload availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAgentWorkloadAvailability",
    "contract": "marketing-crm",
    "purpose": "Agent Workload, Availability & Workforce Control",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AgentWorkloadAvailabilityWorkforceControlView.agentName",
    "AgentWorkloadAvailabilityWorkforceControlView.team",
    "AgentWorkloadAvailabilityWorkforceControlView.skills",
    "AgentWorkloadAvailabilityWorkforceControlView.languages",
    "AgentWorkloadAvailabilityWorkforceControlView.status",
    "AgentWorkloadAvailabilityWorkforceControlView.activeCases"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-023",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-023"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 31. 13 of 13 labels bound to a contract property; 13 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-024",
  "name": "Escalation & Critical Case Monitor",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.6",
   "page": 32
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/escalation-critical-case-monitor-sup-024",
   "component": "apps/venue-support-web/src/routes/support/EscalationCriticalCaseMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-019"
   ],
   "exitTo": [
    "SUP-019"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-019, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-019",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F135 step 10→11",
     "operation": "listEscalationCriticalCase"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Supervisors can identify, coordinate and resolve critical escalations and systemic service incidents from one central workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide supervisors with one workspace for cases requiring elevated attention.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every escalation critical case",
       "columns": [
        "EscalationCriticalCaseMonitorView.caseNumber",
        "EscalationCriticalCaseMonitorView.customerName",
        "EscalationCriticalCaseMonitorView.reason",
        "EscalationCriticalCaseMonitorView.priority",
        "EscalationCriticalCaseMonitorView.transactionValue",
        "EscalationCriticalCaseMonitorView.eventName",
        "EscalationCriticalCaseMonitorView.assignedToPrincipalId",
        "EscalationCriticalCaseMonitorView.escalatedToPrincipalId",
        "EscalationCriticalCaseMonitorView.escalatedAt",
        "EscalationCriticalCaseMonitorView.slaDueAt",
        "EscalationCriticalCaseMonitorView.isSlaBreached",
        "EscalationCriticalCaseMonitorView.status"
       ],
       "bindsTo": "EscalationCriticalCaseMonitorView",
       "operation": "listEscalationCriticalCase",
       "provenance": "pack Customer Service_Reference.pdf, page 32 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected escalation critical case",
       "bindsTo": "EscalationCriticalCaseMonitorView",
       "columns": [
        "EscalationCriticalCaseMonitorView.caseNumber",
        "EscalationCriticalCaseMonitorView.customerName",
        "EscalationCriticalCaseMonitorView.reason",
        "EscalationCriticalCaseMonitorView.priority",
        "EscalationCriticalCaseMonitorView.transactionValue",
        "EscalationCriticalCaseMonitorView.eventName",
        "EscalationCriticalCaseMonitorView.assignedToPrincipalId",
        "EscalationCriticalCaseMonitorView.escalatedToPrincipalId",
        "EscalationCriticalCaseMonitorView.escalatedAt",
        "EscalationCriticalCaseMonitorView.slaDueAt",
        "EscalationCriticalCaseMonitorView.isSlaBreached",
        "EscalationCriticalCaseMonitorView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Major Issue Detection”, “Potential Major Incident”.",
       "provenance": "pack Customer Service_Reference.pdf, page 32 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The escalation critical case list.",
   "error": "Could not load. Names which read failed and leaves the escalation critical case untouched.",
   "emptyFirstRun": "No escalation critical case yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the escalation critical case are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEscalationCriticalCase",
    "contract": "marketing-crm",
    "purpose": "Escalation & Critical Case Monitor",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-024",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-024"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 32. 19 of 19 labels bound to a contract property; 19 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-025",
  "name": "Quality Management & Agent Evaluation",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.7",
   "page": 34
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/quality-management-agent-evaluation-sup-025",
   "component": "apps/venue-support-web/src/routes/support/QualityManagementAgentEvaluation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-019"
   ],
   "exitTo": [
    "SUP-019"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-019, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-019",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F135 step 12→13",
     "operation": "listQualityAgentEvaluation"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "findings into measurable coaching actions.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure whether customer-service interactions meet TICVAI's defined service-quality standards.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Case. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Customer Service_Reference.pdf, page 34 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Customer Service_Reference.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Customer Service_Reference.pdf, page 34"
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
       "label": "Case",
       "provenance": "pack Customer Service_Reference.pdf, page 34 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listQualityAgentEvaluation",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The quality agent evaluation list.",
   "error": "Could not load. Names which read failed and leaves the quality agent evaluation untouched.",
   "emptyFirstRun": "No quality agent evaluation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the quality agent evaluation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQualityAgentEvaluation",
    "contract": "marketing-crm",
    "purpose": "Quality Management & Agent Evaluation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-025",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-025"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 1 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-026",
  "name": "Customer Satisfaction, Feedback & Voice of Customer",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.8",
   "page": 35
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/customer-satisfaction-feedback-voice-of-customer-sup-026",
   "component": "apps/venue-support-web/src/routes/support/CustomerSatisfactionFeedbackVoiceOfCustomer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-019"
   ],
   "exitTo": [
    "SUP-019"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-019, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-019",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F135 step 14→15",
     "operation": "listCustomerSatisfactionFeedback"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can understand what customers think about the service experience and trace negative trends back to their underlying operational causes.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Measure customer perception of TICVAI's support experience and identify recurring service problems.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Service Rating, NPS where used, Direct Customer Comment. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Customer Service_Reference.pdf, page 35 §Support"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "CSAT",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.csat"
      },
      {
       "kind": "metricTile",
       "label": "Survey Response Rate",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.surveyResponseRate"
      },
      {
       "kind": "metricTile",
       "label": "Positive %",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.positiveRate"
      },
      {
       "kind": "metricTile",
       "label": "Neutral %",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.neutralRate"
      },
      {
       "kind": "metricTile",
       "label": "Negative %",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.negativeRate"
      },
      {
       "kind": "metricTile",
       "label": "Complaints",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.complaints"
      },
      {
       "kind": "metricTile",
       "label": "Repeat Contact Rate",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.repeatContactRate"
      },
      {
       "kind": "metricTile",
       "label": "Customer Effort where measured",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.customerEffortScore"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Service Rating",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "NPS where used",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Direct Customer Comment",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer satisfaction feedback list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the customer satisfaction feedback untouched.",
   "emptyFirstRun": "No customer satisfaction feedback yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer satisfaction feedback are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerSatisfactionFeedback",
    "contract": "marketing-crm",
    "purpose": "Customer Satisfaction, Feedback & Voice of Customer",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.csat",
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.surveyResponseRate",
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.positiveRate",
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.neutralRate",
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.negativeRate",
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.complaints"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-026",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-026"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 35. 8 of 8 labels bound to a contract property; 11 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-027",
  "name": "Service Analytics & Root-Cause Intelligence",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.9",
   "page": 37
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/service-analytics-root-cause-intelligence-sup-027",
   "component": "apps/venue-support-web/src/routes/support/ServiceAnalyticsRootCauseIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-019"
   ],
   "exitTo": [
    "SUP-019"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-019, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "SUP-019",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F135 step 16→17",
     "operation": "listServiceRootCause"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can move beyond reporting case volumes and identify the actual product, process and technology issues generating customer demand.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Analyze; Compare) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide comprehensive analytics explaining why customers contact TICVAI and what is driving service demand.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Contact Volume",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.contactVolume"
      },
      {
       "kind": "metricTile",
       "label": "Cases",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.cases"
      },
      {
       "kind": "metricTile",
       "label": "First Response Time",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.averageFirstResponseSeconds"
      },
      {
       "kind": "metricTile",
       "label": "Resolution Time",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.averageResolutionSeconds"
      },
      {
       "kind": "metricTile",
       "label": "First Contact Resolution",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.firstContactResolutionRate"
      },
      {
       "kind": "metricTile",
       "label": "Reopen Rate",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.reopenRate"
      },
      {
       "kind": "metricTile",
       "label": "Escalation Rate",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.escalationRate"
      },
      {
       "kind": "metricTile",
       "label": "SLA Compliance",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.slaComplianceRate"
      },
      {
       "kind": "metricTile",
       "label": "Cost per Case where available",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.costPerCase"
      },
      {
       "kind": "metricTile",
       "label": "CSAT",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.csat"
      },
      {
       "kind": "metricTile",
       "label": "Refund Requests",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.refundRequests"
      },
      {
       "kind": "metricTile",
       "label": "Complaint Rate",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.complaintRate"
      },
      {
       "kind": "dataTable",
       "label": "Comparison",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.comparison.kpis[]",
       "columns": [
        "ServiceAnalyticsRootCauseIntelligenceView.comparison.kpis[].kpi",
        "ServiceAnalyticsRootCauseIntelligenceView.comparison.kpis[].current",
        "ServiceAnalyticsRootCauseIntelligenceView.comparison.kpis[].previous",
        "ServiceAnalyticsRootCauseIntelligenceView.comparison.kpis[].changeRate"
       ],
       "operation": "listServiceRootCause",
       "notes": "One comparison panel in place of the pack's six tiles (Today vs Yesterday, Week vs Week, Month vs Month, Event vs Event, Venue vs Venue, Product vs Product). The compare selector sends `?compare=` (previousDay, previousWeek, previousMonth, event, venue, product) and `?compareId=` to `listServiceRootCause`; the basis shown is `comparison.basis`.",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The service analytics root-cause list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the service analytics root-cause untouched.",
   "emptyFirstRun": "No service analytics root-cause yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the service analytics root-cause are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listServiceRootCause",
    "contract": "marketing-crm",
    "purpose": "Service Analytics & Root-Cause Intelligence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ServiceAnalyticsRootCauseIntelligenceView.contactVolume",
    "ServiceAnalyticsRootCauseIntelligenceView.cases",
    "ServiceAnalyticsRootCauseIntelligenceView.averageFirstResponseSeconds",
    "ServiceAnalyticsRootCauseIntelligenceView.averageResolutionSeconds",
    "ServiceAnalyticsRootCauseIntelligenceView.firstContactResolutionRate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-027",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-027"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 37. 17 of 17 labels bound to a contract property; 18 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "SUP-028",
  "name": "AI Contact Center Intelligence & Automation Studio",
  "module": "Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Customer Service_Reference.pdf",
   "board": "2",
   "number": "10.2.10",
   "page": 39
  },
  "implementation": {
   "app": "venue-support-web",
   "route": "/support/ai-contact-center-intelligence-automation-studio-sup-028",
   "component": "apps/venue-support-web/src/routes/support/AiContactCenterIntelligenceAutomationStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-019"
   ],
   "exitTo": [
    "SUP-019"
   ],
   "inferred": false,
   "notes": "**Reached from SUP-019, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "approved low-risk workflows without removing governance over customer-impacting decisions. Board 2 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast) and no metric row",
  "purpose": "Create the management-level AI intelligence layer for Customer Service. This is different from 10.1.10 AI Customer Service Copilot. Board 1 Copilot = helps one agent resolve one case. Board 2 AI Intelligence = improves the entire service operation.",
  "gaps": [
   {
    "operation": null,
    "why": "**AI Contact Center Intelligence & Automation Studio declares no operation that writes anything** — its only declared call is `listContactAutomation`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Every contact intelligence automation",
       "columns": [
        "AiContactCenterIntelligenceAutomationStudioView.forecast.contactVolume",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.queueDemand[]",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.requiredAgents",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.slaRiskCases",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.expectedComplaints",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.eventDaySupportDemand"
       ],
       "bindsTo": "AiContactCenterIntelligenceAutomationStudioView",
       "operation": "listContactAutomation",
       "provenance": "pack Customer Service_Reference.pdf, page 39 §Forecast"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected contact intelligence automation",
       "bindsTo": "AiContactCenterIntelligenceAutomationStudioView",
       "columns": [
        "AiContactCenterIntelligenceAutomationStudioView.forecast.contactVolume",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.queueDemand[]",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.requiredAgents",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.slaRiskCases",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.expectedComplaints",
        "AiContactCenterIntelligenceAutomationStudioView.forecast.eventDaySupportDemand"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Analyze governed information from”, “Workforce”, “Self-Service”, “Product Improvement”, “Operational Improvement”, “Incident Detection”.",
       "provenance": "pack Customer Service_Reference.pdf, page 39 §Forecast"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The contact intelligence automation list.",
   "error": "Could not load. Names which read failed and leaves the contact intelligence automation untouched.",
   "emptyFirstRun": "No contact intelligence automation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the contact intelligence automation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listContactAutomation",
    "contract": "marketing-crm",
    "purpose": "AI Contact Center Intelligence & Automation Studio",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiContactCenterIntelligenceAutomationStudioView.forecast.contactVolume",
    "AiContactCenterIntelligenceAutomationStudioView.forecast.queueDemand[]",
    "AiContactCenterIntelligenceAutomationStudioView.forecast.requiredAgents",
    "AiContactCenterIntelligenceAutomationStudioView.forecast.slaRiskCases",
    "AiContactCenterIntelligenceAutomationStudioView.forecast.expectedComplaints",
    "AiContactCenterIntelligenceAutomationStudioView.forecast.eventDaySupportDemand"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-028",
   "workshopBoard": "wireframes/WS43 Customer Service Board 2.dc.html#sup-028"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 39. 6 of 6 labels bound to a contract property; 6 of 95 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listAgentWorkloadAvailability": {
  "method": "GET",
  "path": "/agent-workload-availability",
  "contract": "marketing-crm",
  "summary": "Agent Workload, Availability & Workforce Control",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "queueId",
    "in": "query",
    "required": false
   },
   {
    "name": "team",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "skill",
    "in": "query",
    "required": false
   },
   {
    "name": "language",
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
 "listContact": {
  "method": "GET",
  "path": "/contact",
  "contract": "marketing-crm",
  "summary": "Contact Center Operations Command Center",
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
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "queueId",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ContactCenterOperationsCommandCenterView"
 },
 "listContactAutomation": {
  "method": "GET",
  "path": "/contact-automation",
  "contract": "marketing-crm",
  "summary": "AI Contact Center Intelligence & Automation Studio",
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
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "horizonHours",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "AiContactCenterIntelligenceAutomationStudioView"
 },
 "listCustomerSatisfactionFeedback": {
  "method": "GET",
  "path": "/customer-satisfaction-feedback",
  "contract": "marketing-crm",
  "summary": "Customer Satisfaction, Feedback & Voice of Customer",
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
    "name": "source",
    "in": "query",
    "required": false
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "agentPrincipalId",
    "in": "query",
    "required": false
   },
   {
    "name": "sentiment",
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
   }
  ],
  "requestBody": null,
  "responds": "CustomerSatisfactionFeedbackVoiceOfCustomerView"
 },
 "listEscalationCriticalCase": {
  "method": "GET",
  "path": "/escalation-critical-case",
  "contract": "marketing-crm",
  "summary": "Escalation & Critical Case Monitor",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "escalationType",
    "in": "query",
    "required": false
   },
   {
    "name": "priority",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "breachedOnly",
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
 "listQualityAgentEvaluation": {
  "method": "GET",
  "path": "/quality-agent-evaluation",
  "contract": "marketing-crm",
  "summary": "Quality Management & Agent Evaluation",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "agentPrincipalId",
    "in": "query",
    "required": false
   },
   {
    "name": "evaluatorPrincipalId",
    "in": "query",
    "required": false
   },
   {
    "name": "sourceType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "criticalFailureOnly",
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
 "listQueues": {
  "method": "GET",
  "path": "/queues",
  "contract": "queue",
  "summary": "List queues",
  "permission": "QUEUE_VIEW",
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
    "name": "openOnly",
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
 "listServiceQueues": {
  "method": "GET",
  "path": "/service-queues",
  "contract": "marketing-crm",
  "summary": "List customer-service queues",
  "permission": "CASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "listServiceRootCause": {
  "method": "GET",
  "path": "/service-root-cause",
  "contract": "marketing-crm",
  "summary": "Service Analytics & Root-Cause Intelligence",
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
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
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
    "name": "compare",
    "in": "query",
    "required": false
   },
   {
    "name": "compareId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ServiceAnalyticsRootCauseIntelligenceView"
 },
 "listSlaPolicyService": {
  "method": "GET",
  "path": "/sla-policy-service",
  "contract": "marketing-crm",
  "summary": "SLA Policy & Service-Level Management",
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
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "slaPolicyId",
    "in": "query",
    "required": false
   },
   {
    "name": "priority",
    "in": "query",
    "required": false
   },
   {
    "name": "kind",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "queueId",
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
   }
  ],
  "requestBody": null,
  "responds": "SlaPolicyServiceLevelManagementView"
 },
 "setIntelligentRoutingSkill": {
  "method": "PUT",
  "path": "/intelligent-routing-skill",
  "contract": "marketing-crm",
  "summary": "Create or change a case routing rule",
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
  "requestBody": "IntelligentRoutingSkillsAssignmentEngineInput",
  "responds": "IntelligentRoutingSkillsAssignmentEngineView"
 },
 "setServiceQueueDefinition": {
  "method": "PUT",
  "path": "/service-queues",
  "contract": "marketing-crm",
  "summary": "Create or change a customer-service queue",
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
  "requestBody": "ServiceQueue",
  "responds": "ServiceQueue"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AgentWorkloadAvailabilityWorkforceControlView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.agent_service_profile (new), marketing.agent_availability, marketing.case, marketing.conversation, marketing.service_queue (new) and workforce.shift",
  "description": "One agent's live status and workload. Rates are over the period since the agent's current shift started, or the venue's current day when no shift is rostered.",
  "required": [
   "principalId",
   "agentName",
   "status",
   "activeCases"
  ],
  "properties": {
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "agentName": {
    "type": "string",
    "description": "The agent's display name."
   },
   "team": {
    "type": "string",
    "nullable": true
   },
   "skills": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "busy",
     "onCall",
     "chatting",
     "afterCallWork",
     "break",
     "training",
     "offline"
    ]
   },
   "activeCases": {
    "type": "integer",
    "minimum": 0
   },
   "chats": {
    "type": "integer",
    "minimum": 0,
    "description": "Conversations the agent holds now."
   },
   "calls": {
    "type": "integer",
    "minimum": 0,
    "description": "Voice conversations in progress (0 or 1)."
   },
   "queues": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "queueId",
      "queueName"
     ],
     "properties": {
      "queueId": {
       "type": "string",
       "format": "uuid"
      },
      "queueName": {
       "type": "string"
      }
     }
    }
   },
   "slaRiskCases": {
    "type": "integer",
    "minimum": 0,
    "description": "The agent's open cases at risk or breached."
   },
   "averageHandleSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "resolutionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Cases resolved over cases handled."
   },
   "utilization": {
    "type": "number",
    "minimum": 0,
    "description": "Active cases and conversations over `maxConcurrentCases`; above 1 means overloaded."
   },
   "workloadBand": {
    "type": "string",
    "enum": [
     "available",
     "normal",
     "overloaded"
    ],
    "description": "`overloaded` at utilization 0.9 or above, `available` below 0.5."
   },
   "availabilityExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "AiContactCenterIntelligenceAutomationStudioView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.contact_automation (new), with the forecast and recommendations computed over marketing.case, marketing.conversation and marketing.agent_availability",
  "description": "The studio's forecast, recommendations and automations for the filters given.",
  "required": [
   "forecast",
   "recommendations",
   "automations"
  ],
  "properties": {
   "forecast": {
    "type": "object",
    "nullable": true,
    "description": "Expected over the next `horizonHours`.",
    "properties": {
     "contactVolume": {
      "type": "integer",
      "minimum": 0
     },
     "queueDemand": {
      "type": "array",
      "items": {
       "type": "object",
       "required": [
        "queueId",
        "expectedCases"
       ],
       "properties": {
        "queueId": {
         "type": "string",
         "format": "uuid"
        },
        "queueName": {
         "type": "string"
        },
        "expectedCases": {
         "type": "integer",
         "minimum": 0
        },
        "requiredAgents": {
         "type": "integer",
         "minimum": 0
        }
       }
      }
     },
     "requiredAgents": {
      "type": "integer",
      "minimum": 0
     },
     "slaRiskCases": {
      "type": "integer",
      "minimum": 0,
      "description": "Cases expected to breach."
     },
     "expectedComplaints": {
      "type": "integer",
      "minimum": 0
     },
     "eventDaySupportDemand": {
      "type": "integer",
      "minimum": 0,
      "description": "Expected cases tied to events on the day."
     },
     "generatedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   },
   "recommendations": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "type": "object",
     "required": [
      "category",
      "text"
     ],
     "properties": {
      "category": {
       "type": "string",
       "enum": [
        "workforce",
        "selfService",
        "productImprovement",
        "operationalImprovement",
        "incidentDetection"
       ]
      },
      "text": {
       "type": "string",
       "maxLength": 500
      },
      "evidence": {
       "type": "string",
       "maxLength": 500,
       "nullable": true
      },
      "confidence": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "automations": {
    "type": "array",
    "maxItems": 200,
    "items": {
     "$ref": "#/components/schemas/ContactAutomation"
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
 "ContactAutomation": {
  "type": "object",
  "x-ticvai-persistence": "marketing.contact_automation",
  "description": "One governed contact-centre automation (pack 10.2.10 AI Governance).",
  "required": [
   "code",
   "name",
   "level",
   "trigger",
   "allowedActions",
   "confidenceThreshold",
   "onException",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 60,
    "description": "The natural key, e.g. `autoResendValidTicket`."
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "level": {
    "type": "string",
    "enum": [
     "recommendOnly",
     "agentConfirmation",
     "supervisorGoverned",
     "fullyAutomated"
    ]
   },
   "trigger": {
    "type": "object",
    "required": [
     "event"
    ],
    "properties": {
     "event": {
      "type": "string",
      "enum": [
       "caseCreated",
       "caseUpdated",
       "conversationMessageReceived",
       "caseClusterDetected"
      ]
     },
     "conditions": {
      "type": "array",
      "maxItems": 20,
      "description": "All must hold.",
      "items": {
       "type": "object",
       "required": [
        "field",
        "operator"
       ],
       "properties": {
        "field": {
         "type": "string",
         "maxLength": 100,
         "description": "e.g. `case.kind`, `ticket.isValid`, `guest.identityVerified`, `cluster.caseCount`."
        },
        "operator": {
         "type": "string",
         "enum": [
          "eq",
          "neq",
          "in",
          "gt",
          "gte",
          "lt",
          "lte",
          "exists"
         ]
        },
        "value": {
         "description": "Any JSON value; omitted for `exists`."
        }
       }
      }
     },
     "windowMinutes": {
      "type": "integer",
      "minimum": 1,
      "nullable": true,
      "description": "For cluster triggers, e.g. 5 cases in 10 minutes."
     }
    }
   },
   "scope": {
    "type": "object",
    "description": "Where it applies; empty lists mean everywhere in the scope path.",
    "properties": {
     "venueIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "queueIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "channels": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/MessageChannel"
      }
     }
    }
   },
   "allowedActions": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "enum": [
      "resendTicket",
      "resolveCase",
      "createCase",
      "assignQueue",
      "setPriority",
      "sendMessage",
      "notifySupervisor",
      "flagPotentialIncident"
     ]
    }
   },
   "confidenceThreshold": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "onException": {
    "type": "string",
    "enum": [
     "leaveForAgent",
     "routeToQueue",
     "notifySupervisor"
    ]
   },
   "exceptionQueueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "killSwitch": {
    "type": "boolean",
    "default": false
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "approved",
     "active",
     "paused",
     "retired"
    ]
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "approvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "lastSimulation": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "properties": {
     "simulatedVersion": {
      "type": "integer",
      "minimum": 1
     },
     "periodStart": {
      "type": "string",
      "format": "date-time"
     },
     "periodEnd": {
      "type": "string",
      "format": "date-time"
     },
     "casesMatched": {
      "type": "integer",
      "minimum": 0
     },
     "casesResolvable": {
      "type": "integer",
      "minimum": 0
     },
     "agentHoursSaved": {
      "type": "number",
      "minimum": 0
     },
     "estimatedConfidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
     }
    }
   },
   "executionsLast30Days": {
    "type": "integer",
    "minimum": 0,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "ContactCenterOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case, marketing.conversation, marketing.agent_availability, marketing.sla_policy, marketing.form_submission (post-case CSAT surveys) and marketing.service_queue (new)",
  "description": "The contact centre's live figures for the filters given. Counts are of cases unless the name says otherwise; durations are averages over cases first responded to or resolved today.",
  "required": [
   "casesToday",
   "openCases",
   "unassignedCases",
   "customersWaiting",
   "criticalCases",
   "slaAtRisk",
   "slaBreached",
   "channels",
   "queues"
  ],
  "properties": {
   "casesToday": {
    "type": "integer",
    "minimum": 0,
    "description": "Cases created today."
   },
   "openCases": {
    "type": "integer",
    "minimum": 0,
    "description": "Cases not `resolved` or `closed`."
   },
   "unassignedCases": {
    "type": "integer",
    "minimum": 0
   },
   "customersWaiting": {
    "type": "integer",
    "minimum": 0,
    "description": "Unclaimed conversations waiting in a queue now."
   },
   "criticalCases": {
    "type": "integer",
    "minimum": 0,
    "description": "Open cases at priority `urgent`."
   },
   "slaAtRisk": {
    "type": "integer",
    "minimum": 0,
    "description": "Open cases that have used 75% or more of their SLA and have not breached."
   },
   "slaBreached": {
    "type": "integer",
    "minimum": 0,
    "description": "Open cases past their SLA (`Case.isSlaBreached`)."
   },
   "casesResolvedToday": {
    "type": "integer",
    "minimum": 0
   },
   "averageFirstResponseSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "averageResolutionSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "firstContactResolutionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Share of cases resolved today with no reopen and no transfer."
   },
   "csat": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Share of today's post-case CSAT responses that are satisfied (top two points of the scale). Null when there are none."
   },
   "activeAgents": {
    "type": "integer",
    "minimum": 0,
    "description": "Agents whose availability is not `offline`."
   },
   "agentUtilization": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Active cases and conversations held, over the active agents' combined capacity."
   },
   "channels": {
    "type": "array",
    "description": "Workload per contact channel, from `Case.channel` and `Conversation.channel`.",
    "items": {
     "type": "object",
     "required": [
      "channel",
      "openCases",
      "waiting"
     ],
     "properties": {
      "channel": {
       "type": "string",
       "enum": [
        "email",
        "phone",
        "liveChat",
        "whatsapp",
        "webForm",
        "mobileApp",
        "b2cPortal",
        "social",
        "frontDesk"
       ]
      },
      "openCases": {
       "type": "integer",
       "minimum": 0
      },
      "waiting": {
       "type": "integer",
       "minimum": 0
      },
      "slaAtRisk": {
       "type": "integer",
       "minimum": 0
      },
      "averageFirstResponseSeconds": {
       "type": "integer",
       "minimum": 0,
       "nullable": true
      }
     }
    }
   },
   "queues": {
    "type": "array",
    "description": "Queue health, worst first.",
    "items": {
     "type": "object",
     "required": [
      "queueId",
      "queueName",
      "openCases",
      "waiting",
      "health"
     ],
     "properties": {
      "queueId": {
       "type": "string",
       "format": "uuid"
      },
      "queueName": {
       "type": "string"
      },
      "openCases": {
       "type": "integer",
       "minimum": 0
      },
      "waiting": {
       "type": "integer",
       "minimum": 0
      },
      "slaAtRisk": {
       "type": "integer",
       "minimum": 0
      },
      "agentsOnline": {
       "type": "integer",
       "minimum": 0
      },
      "health": {
       "type": "string",
       "enum": [
        "healthy",
        "warning",
        "critical"
       ],
       "description": "`critical` when any case in the queue has breached or waiting exceeds the queue's overflow threshold; `warning` when any is at risk."
      }
     }
    }
   },
   "operationalFeed": {
    "type": "array",
    "maxItems": 50,
    "description": "Notable changes in the last hour, newest first (queue surges, cases nearing breach, a channel over its response target).",
    "items": {
     "type": "object",
     "required": [
      "occurredAt",
      "severity",
      "message"
     ],
     "properties": {
      "occurredAt": {
       "type": "string",
       "format": "date-time"
      },
      "severity": {
       "type": "string",
       "enum": [
        "info",
        "warning",
        "critical"
       ]
      },
      "message": {
       "type": "string",
       "maxLength": 300
      },
      "queueId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "channel": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "serviceRiskSummary": {
    "type": "object",
    "nullable": true,
    "description": "The AI operational summary; null when AI is disabled for the tenant. Advisory only, it changes nothing.",
    "required": [
     "riskLevel",
     "summary",
     "generatedAt"
    ],
    "properties": {
     "riskLevel": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high",
       "critical"
      ]
     },
     "summary": {
      "type": "string",
      "maxLength": 1000
     },
     "recommendations": {
      "type": "array",
      "maxItems": 5,
      "items": {
       "type": "string",
       "maxLength": 300
      }
     },
     "generatedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "CreateQueueRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "capacityPerCycle",
   "cycleMinutes"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "attractionProductId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "standby",
     "singleRider",
     "fastPass",
     "virtual",
     "accessible",
     "groupOnly",
     "staffOnly"
    ],
    "default": "standby",
    "description": "5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"
   },
   "operatingWindows": {
    "type": "array",
    "description": "**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n",
    "items": {
     "type": "object",
     "required": [
      "day",
      "from",
      "to"
     ],
     "properties": {
      "day": {
       "type": "string",
       "enum": [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun"
       ]
      },
      "from": {
       "type": "string",
       "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
       "description": "Venue local time, 24-hour `HH:MM`, when the queue starts running."
      },
      "to": {
       "type": "string",
       "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
       "description": "Venue local time, 24-hour `HH:MM`, when the queue stops running."
      },
      "lastEntryMinutesBefore": {
       "type": "integer",
       "default": 0,
       "description": "**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"
      }
     }
    }
   },
   "parentQueueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"
   },
   "loadBalanceWithQueueIds": {
    "type": "array",
    "description": "BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "inQueueOfferEnabled": {
    "type": "boolean",
    "default": false,
    "description": "**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"
   },
   "notifyBeforeCallMinutes": {
    "type": "integer",
    "default": 5,
    "description": "BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"
   },
   "capacityPerCycle": {
    "type": "integer",
    "minimum": 1
   },
   "cycleMinutes": {
    "type": "number",
    "minimum": 0
   },
   "maxPartySize": {
    "type": "integer",
    "default": 6
   },
   "returnWindowMinutes": {
    "type": "integer",
    "default": 15,
    "description": "How long a called party has to arrive before the entry expires."
   },
   "heightRequirementCm": {
    "type": "integer",
    "nullable": true
   },
   "fastPassAllocationPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "default": 0,
    "description": "Share of each cycle reserved for Fast Pass holders."
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "fastPass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/QueueFastPass"
     }
    ],
    "nullable": true,
    "description": "The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"
   }
  }
 },
 "CustomerSatisfactionFeedbackVoiceOfCustomerView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.form_submission and marketing.form_definition (survey forms), marketing.review, marketing.case and marketing.feedback_classification (new, the AI sentiment and topic per feedback item)",
  "description": "Voice-of-customer figures for the filters given. Rates are shares of feedback items in the period.",
  "required": [
   "responses",
   "breakdown",
   "comments"
  ],
  "properties": {
   "responses": {
    "type": "integer",
    "minimum": 0,
    "description": "Feedback items in the period."
   },
   "csat": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Share of CSAT answers in the top two points of the scale."
   },
   "nps": {
    "type": "integer",
    "minimum": -100,
    "maximum": 100,
    "nullable": true,
    "description": "Null where the tenant runs no NPS survey."
   },
   "surveyResponseRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Surveys answered over surveys sent."
   },
   "positiveRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "neutralRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "negativeRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "complaints": {
    "type": "integer",
    "minimum": 0
   },
   "repeatContactRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Customers with a second case within 7 days of the first, over customers with a case."
   },
   "customerEffortScore": {
    "type": "number",
    "minimum": 1,
    "maximum": 7,
    "nullable": true,
    "description": "Mean CES answer; null where effort is not measured."
   },
   "csatChangeRate": {
    "type": "number",
    "nullable": true,
    "description": "Relative change in `csat` against the previous period of equal length."
   },
   "aiSummary": {
    "type": "object",
    "nullable": true,
    "description": "AI-derived narrative of the feedback matching the filters (22.5.12; 29 September, build pass, group G2), labelled as AI on screen. Null when AI is off or fewer than 5 items match.",
    "required": [
     "text",
     "basedOnCount",
     "modelVersion"
    ],
    "properties": {
     "text": {
      "type": "string",
      "maxLength": 2000
     },
     "basedOnCount": {
      "type": "integer",
      "minimum": 0,
      "description": "The feedback items the summary was written from."
     },
     "modelVersion": {
      "type": "string",
      "maxLength": 60
     },
     "generatedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   },
   "breakdown": {
    "type": "array",
    "description": "One row per value of the `groupBy` dimension, most responses first.",
    "items": {
     "type": "object",
     "required": [
      "key",
      "label",
      "responses"
     ],
     "properties": {
      "key": {
       "type": "string",
       "description": "The id or enum value of the group."
      },
      "label": {
       "type": "string"
      },
      "responses": {
       "type": "integer",
       "minimum": 0
      },
      "csat": {
       "type": "number",
       "minimum": 0,
       "maximum": 1,
       "nullable": true
      },
      "negativeRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "themes": {
    "type": "array",
    "maxItems": 20,
    "description": "AI topic themes, largest share first. Empty when AI is disabled for the tenant.",
    "items": {
     "type": "object",
     "required": [
      "topic",
      "shareRate"
     ],
     "properties": {
      "topic": {
       "type": "string",
       "maxLength": 100
      },
      "shareRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "negativeRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "changeRate": {
       "type": "number",
       "nullable": true,
       "description": "Relative change in the theme's volume against the previous period."
      }
     }
    }
   },
   "trendAlerts": {
    "type": "array",
    "maxItems": 10,
    "items": {
     "type": "string",
     "maxLength": 300
    },
    "description": "AI-detected shifts, e.g. negative feedback on ticket delivery rising after a release."
   },
   "comments": {
    "type": "array",
    "maxItems": 50,
    "description": "The 50 latest comments with text, newest first.",
    "items": {
     "type": "object",
     "required": [
      "feedbackId",
      "source",
      "receivedAt"
     ],
     "properties": {
      "feedbackId": {
       "type": "string",
       "format": "uuid"
      },
      "source": {
       "type": "string",
       "enum": [
        "csatSurvey",
        "serviceRating",
        "nps",
        "postCaseSurvey",
        "complaint",
        "appFeedback",
        "webFeedback",
        "directComment"
       ]
      },
      "receivedAt": {
       "type": "string",
       "format": "date-time"
      },
      "comment": {
       "type": "string",
       "maxLength": 4000,
       "nullable": true
      },
      "rating": {
       "type": "number",
       "nullable": true,
       "description": "The answer on its survey's own scale."
      },
      "ratingScale": {
       "type": "string",
       "nullable": true,
       "enum": [
        "nps",
        "csat",
        "ces",
        "likert5",
        "likert7",
        "stars"
       ]
      },
      "sentiment": {
       "type": "string",
       "nullable": true,
       "enum": [
        "positive",
        "neutral",
        "negative"
       ]
      },
      "topic": {
       "type": "string",
       "nullable": true
      },
      "caseId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "agentPrincipalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "eventId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "followUpCaseId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "EscalationCriticalCaseMonitorView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case, marketing.case_escalation (new, one row per escalateCase call) and the related order in orders",
  "description": "One open escalated case, as of its latest escalation.",
  "required": [
   "caseId",
   "caseNumber",
   "reason",
   "escalationType",
   "priority",
   "escalatedAt",
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
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "customerName": {
    "type": "string",
    "nullable": true,
    "description": "Resolved from `pii.subject`; null unless the caller holds `GUEST_VIEW_PII`."
   },
   "reason": {
    "type": "string",
    "description": "The reason given to `escalateCase`, or `SLA breached` for an automatic escalation."
   },
   "reasonCategory": {
    "type": "string",
    "nullable": true,
    "enum": [
     "slaRisk",
     "customerComplaint",
     "repeatedContact",
     "highValue",
     "refundException",
     "operationalFailure",
     "systemFailure",
     "legalCompliance",
     "vipCustomer",
     "supervisorRequested",
     "other"
    ]
   },
   "escalationType": {
    "type": "string",
    "enum": [
     "vip",
     "financial",
     "eventDay",
     "management",
     "technical",
     "other"
    ],
    "description": "`vip` for a VIP-tier customer, `financial` for a refund or high-value order, `eventDay` when the case's event is today, `management` when escalated to a manager, `technical` for a technical category; the first that applies, in that order."
   },
   "priority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "transactionValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "The related order's total, when the case has one."
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "eventName": {
    "type": "string",
    "nullable": true
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "escalatedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "escalationCount": {
    "type": "integer",
    "minimum": 1
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isSlaBreached": {
    "type": "boolean"
   },
   "status": {
    "$ref": "#/components/schemas/CaseStatus"
   }
  }
 },
 "IntelligentRoutingSkillsAssignmentEngineInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.case_routing_rule",
  "description": "One case routing rule (pack 10.2.3). Empty match lists match everything; all non-empty lists must match.",
  "required": [
   "code",
   "name",
   "strategy",
   "rank",
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
    "maxLength": 60,
    "description": "The natural key, e.g. `eventDayArabic`."
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "rank": {
    "type": "integer",
    "minimum": 1,
    "description": "Lower is tried first."
   },
   "queueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The queue this rule routes into; null routes straight to an agent."
   },
   "match": {
    "type": "object",
    "properties": {
     "categoryIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      },
      "description": "Case categories and subcategories (`Case.categoryId`)."
     },
     "kinds": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CaseKind"
      }
     },
     "channels": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/MessageChannel"
      }
     },
     "customerLanguages": {
      "type": "array",
      "items": {
       "type": "string",
       "maxLength": 10
      },
      "description": "BCP-47 tags, e.g. `ar`, `en`."
     },
     "customerTypes": {
      "type": "array",
      "items": {
       "type": "string",
       "enum": [
        "individual",
        "member",
        "vip",
        "corporate",
        "group",
        "partner"
       ]
      }
     },
     "membershipTierIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "venueIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "eventIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "productIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "priorities": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CasePriority"
      }
     },
     "eventWithinHours": {
      "type": "integer",
      "minimum": 0,
      "nullable": true,
      "description": "Event proximity - matches only when the case's event starts within this many hours."
     }
    }
   },
   "strategy": {
    "type": "string",
    "enum": [
     "roundRobin",
     "leastBusy",
     "skillBased",
     "priorityBased",
     "languageBased",
     "customerTierBased",
     "aiRecommended"
    ]
   },
   "requiredSkills": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 60
    },
    "description": "Skills an agent must hold (`AgentServiceProfile.skills`), e.g. `ticketing`, `refunds`."
   },
   "requireLanguageMatch": {
    "type": "boolean",
    "default": true,
    "description": "Only agents who speak the customer's language are candidates."
   },
   "maxUtilizationRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Agents above this workload are skipped."
   },
   "respectSlaCapability": {
    "type": "boolean",
    "default": true,
    "description": "Skip agents whose current queue would push the case past its SLA."
   },
   "stickyOwnership": {
    "type": "boolean",
    "default": false,
    "description": "Prefer the agent who last handled the customer or the reopened case, if available."
   },
   "stickyWindowHours": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "fallbackQueueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the case goes when no candidate agent is available."
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "IntelligentRoutingSkillsAssignmentEngineView": {
  "description": "A routing rule as stored, with how often it has matched.",
  "x-ticvai-persistence": "none — the marketing.case_routing_rule (new) row plus a count over marketing.case",
  "allOf": [
   {
    "$ref": "#/components/schemas/IntelligentRoutingSkillsAssignmentEngineInput"
   },
   {
    "type": "object",
    "properties": {
     "matchedLast7Days": {
      "type": "integer",
      "minimum": 0,
      "readOnly": true
     },
     "lastMatchedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true
     }
    }
   }
  ]
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
 "QualityManagementAgentEvaluationView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.quality_evaluation",
  "description": "One quality evaluation of one interaction (pack 10.2.7). Resolution time and SLA outcome are read from the case, not entered.",
  "required": [
   "id",
   "agentPrincipalId",
   "sourceType",
   "evaluatedBy",
   "status",
   "criteria"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "agentPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "evaluatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The caller who scored it; null while only the AI has."
   },
   "sourceType": {
    "type": "string",
    "enum": [
     "call",
     "chat",
     "email",
     "whatsapp",
     "case",
     "complaint"
    ]
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "conversationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "evaluatedBy": {
    "type": "string",
    "enum": [
     "human",
     "ai"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "scored",
     "acknowledged"
    ]
   },
   "criteria": {
    "type": "array",
    "maxItems": 30,
    "items": {
     "type": "object",
     "required": [
      "criterion",
      "score",
      "maxScore"
     ],
     "properties": {
      "criterion": {
       "type": "string",
       "maxLength": 60,
       "description": "The tenant's criterion code; the pack's defaults are `greeting`, `customerVerification`, `understanding`, `accuracy`, `policyCompliance`, `communicationQuality`, `empathy`, `resolution`, `documentation`, `closing`."
      },
      "score": {
       "type": "integer",
       "minimum": 0
      },
      "maxScore": {
       "type": "integer",
       "minimum": 1
      },
      "comment": {
       "type": "string",
       "maxLength": 1000,
       "nullable": true
      }
     }
    }
   },
   "criticalFailures": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "incorrectRefund",
      "privacyViolation",
      "unauthorisedCompensation",
      "incorrectTicketInformation",
      "securityVerificationFailure",
      "other"
     ]
    }
   },
   "overallScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "readOnly": true,
    "description": "Criteria score as a percentage; 0 when any critical failure is recorded."
   },
   "aiFindings": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "required": [
      "area",
      "finding"
     ],
     "properties": {
      "area": {
       "type": "string",
       "enum": [
        "policyAdherence",
        "requiredStatements",
        "tone",
        "accuracy",
        "resolutionQuality",
        "missingCaseDocumentation"
       ]
      },
      "finding": {
       "type": "string",
       "maxLength": 500
      },
      "confidence": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "feedback": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true
   },
   "coachingActions": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "type"
     ],
     "properties": {
      "type": {
       "type": "string",
       "enum": [
        "productTraining",
        "policyTraining",
        "communicationCoaching",
        "systemTraining"
       ]
      },
      "note": {
       "type": "string",
       "maxLength": 500,
       "nullable": true
      },
      "dueAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "completedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "resolutionSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "readOnly": true
   },
   "slaMet": {
    "type": "boolean",
    "nullable": true,
    "readOnly": true
   },
   "agentComment": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "acknowledgedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "evaluatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "Queue": {
  "x-ticvai-persistence": "queue.queue + queue.queue_operating_window",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateQueueRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status",
     "waitingPartyCount"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "status": {
      "$ref": "#/components/schemas/QueueStatus"
     },
     "statusReason": {
      "type": "string",
      "nullable": true
     },
     "waitingPartyCount": {
      "type": "integer"
     },
     "waitingGuestCount": {
      "type": "integer"
     },
     "currentWaitMinutes": {
      "type": "integer",
      "nullable": true
     },
     "waitTimeSource": {
      "$ref": "#/components/schemas/WaitTimeSource"
     },
     "waitTimeAsOf": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"
     },
     "manualWaitExpiresAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"
     },
     "manualWaitNote": {
      "type": "string",
      "maxLength": 200,
      "nullable": true,
      "readOnly": true,
      "description": "The `note` given with the current manual figure. Cleared when it expires."
     },
     "expectedReopenAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
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
 "ServiceAnalyticsRootCauseIntelligenceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case, marketing.conversation, marketing.form_submission (CSAT) and the related orders and payments",
  "description": "Service analytics for the filters given, with the comparison asked for.",
  "required": [
   "contactVolume",
   "cases",
   "drivers",
   "comparison"
  ],
  "properties": {
   "contactVolume": {
    "type": "integer",
    "minimum": 0,
    "description": "Conversations and cases opened, a conversation that became a case counted once."
   },
   "cases": {
    "type": "integer",
    "minimum": 0
   },
   "averageFirstResponseSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "averageResolutionSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "firstContactResolutionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "reopenRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "escalationRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "slaComplianceRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "costPerCase": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "csat": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "refundRequests": {
    "type": "integer",
    "minimum": 0
   },
   "complaintRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "comparison": {
    "type": "object",
    "required": [
     "basis",
     "kpis"
    ],
    "properties": {
     "basis": {
      "type": "string",
      "enum": [
       "previousDay",
       "previousWeek",
       "previousMonth",
       "event",
       "venue",
       "product"
      ]
     },
     "compareId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "kpis": {
      "type": "array",
      "items": {
       "type": "object",
       "required": [
        "kpi"
       ],
       "properties": {
        "kpi": {
         "type": "string",
         "description": "The KPI's property name above, e.g. `contactVolume`."
        },
        "current": {
         "type": "number",
         "nullable": true
        },
        "previous": {
         "type": "number",
         "nullable": true
        },
        "changeRate": {
         "type": "number",
         "nullable": true
        }
       }
      }
     }
    }
   },
   "drivers": {
    "type": "array",
    "description": "Contact drivers, most cases first.",
    "items": {
     "type": "object",
     "required": [
      "driver",
      "cases",
      "shareRate"
     ],
     "properties": {
      "driver": {
       "type": "string",
       "enum": [
        "ticketDelivery",
        "refund",
        "reschedule",
        "paymentFailure",
        "membership",
        "accessIssue",
        "groupBooking",
        "generalInformation",
        "other"
       ]
      },
      "cases": {
       "type": "integer",
       "minimum": 0
      },
      "shareRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "changeRate": {
       "type": "number",
       "nullable": true
      }
     }
    }
   },
   "rootCauses": {
    "type": "array",
    "maxItems": 20,
    "description": "Case surges traced to one cause, largest first. Empty when AI is disabled for the tenant.",
    "items": {
     "type": "object",
     "required": [
      "summary",
      "cases"
     ],
     "properties": {
      "summary": {
       "type": "string",
       "maxLength": 500
      },
      "driver": {
       "type": "string",
       "nullable": true
      },
      "cases": {
       "type": "integer",
       "minimum": 0
      },
      "causeType": {
       "type": "string",
       "enum": [
        "paymentProvider",
        "event",
        "product",
        "release",
        "incident",
        "venueArea",
        "other"
       ]
      },
      "causeRef": {
       "type": "string",
       "nullable": true,
       "description": "The id of the provider, event, product or incident, where there is one."
      },
      "windowStart": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "windowEnd": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "avoidableContacts": {
    "type": "array",
    "description": "AI estimate of cases that could have been prevented, by remedy.",
    "items": {
     "type": "object",
     "required": [
      "preventableBy",
      "cases"
     ],
     "properties": {
      "preventableBy": {
       "type": "string",
       "enum": [
        "betterB2cInformation",
        "selfService",
        "productConfiguration",
        "improvedNotifications",
        "technicalFixes",
        "betterTicketDelivery"
       ]
      },
      "cases": {
       "type": "integer",
       "minimum": 0
      },
      "recommendation": {
       "type": "string",
       "maxLength": 500,
       "nullable": true
      }
     }
    }
   }
  }
 },
 "ServiceQueue": {
  "type": "object",
  "x-ticvai-persistence": "marketing.service_queue",
  "description": "**A customer-service queue** (e.g. `eventDaySupport`). Cases (`Case.queueId`), routing rules (`queueId`, `fallbackQueueId`) and agents (`AgentAvailability.queueIds`) name it; `listContact` and `listAgentWorkloadAvailability` report per queue. Maintained by `setServiceQueueDefinition`, read by `listServiceQueues` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n",
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
   "overflowWaitSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "The queue's overflow threshold; a case waiting longer marks the queue `critical`."
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
 "SlaPolicyServiceLevelManagementView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.case and marketing.sla_policy",
  "description": "SLA performance for the filters given. Counts are of open cases for the state counts and of cases in the period for the averages and the compliance rate.",
  "required": [
   "withinSla",
   "atRisk",
   "breached",
   "byPolicy"
  ],
  "properties": {
   "withinSla": {
    "type": "integer",
    "minimum": 0
   },
   "atRisk": {
    "type": "integer",
    "minimum": 0
   },
   "breached": {
    "type": "integer",
    "minimum": 0
   },
   "averageResponseSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Mean time to first response, less paused time."
   },
   "averageResolutionSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "slaComplianceRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Cases resolved in the period within target, over cases resolved in the period."
   },
   "byPolicy": {
    "type": "array",
    "description": "One row per SLA policy that timed a case in the period, worst compliance first.",
    "items": {
     "type": "object",
     "required": [
      "slaPolicyId",
      "code",
      "name",
      "withinSla",
      "atRisk",
      "breached"
     ],
     "properties": {
      "slaPolicyId": {
       "type": "string",
       "format": "uuid"
      },
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "firstResponseMinutes": {
       "type": "integer",
       "nullable": true
      },
      "resolutionMinutes": {
       "type": "integer",
       "nullable": true
      },
      "withinSla": {
       "type": "integer",
       "minimum": 0
      },
      "atRisk": {
       "type": "integer",
       "minimum": 0
      },
      "breached": {
       "type": "integer",
       "minimum": 0
      },
      "slaComplianceRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1,
       "nullable": true
      }
     }
    }
   },
   "forecastBreaches": {
    "type": "array",
    "maxItems": 50,
    "description": "AI forecast of open cases likely to breach before the static thresholds fire, soonest first. Advisory; empty when AI is disabled for the tenant.",
    "items": {
     "type": "object",
     "required": [
      "caseCount",
      "horizonMinutes"
     ],
     "properties": {
      "queueId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "queueName": {
       "type": "string",
       "nullable": true
      },
      "slaPolicyId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "caseCount": {
       "type": "integer",
       "minimum": 0
      },
      "horizonMinutes": {
       "type": "integer",
       "minimum": 1
      },
      "confidence": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
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
