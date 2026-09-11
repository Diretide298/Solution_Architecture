# WS26 — Customer Service board 2

**10 screens · 10 operations · 11 schemas · 3 permissions**

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
  `MARKETING_MANAGE, MARKETING_VIEW, QUEUE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: listQueues
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SUP-019` | Contact Center Operations Command Center | commandCentre | 1 | 0 | — |
| `SUP-020` | Queue Configuration & Management | configEditor | 1 | 0 | — |
| `SUP-021` | Intelligent Routing, Skills & Assignment Engine | listDetail | 1 | 0 | — |
| `SUP-022` | SLA Policy & Service-Level Management | configEditor | 1 | 0 | — |
| `SUP-023` | Agent Workload, Availability & Workforce Control | listDetail | 1 | 0 | — |
| `SUP-024` | Escalation & Critical Case Monitor | listDetail | 1 | 0 | — |
| `SUP-025` | Quality Management & Agent Evaluation | listDetail | 1 | 0 | — |
| `SUP-026` | Customer Satisfaction, Feedback & Voice of Customer | commandCentre | 1 | 0 | — |
| `SUP-027` | Service Analytics & Root-Cause Intelligence | commandCentre | 1 | 0 | — |
| `SUP-028` | AI Contact Center Intelligence & Automation Studio | listDetail | 1 | 0 | — |

## Thin screens in this batch

**SUP-021, SUP-023, SUP-024, SUP-025, SUP-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — SUP-001 declares entryState.params sessionId, so an edge into it must carry them"
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide supervisors and management with a real-time view of customer-service operations across",
  "purposeNote": "Supervisors can understand the real-time operational state of Customer Service and identify the queues, channels and issues requiring immediate intervention.",
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
       "bindsTo": "ContactCenterOperationsCommandCenterView.firstResponseTime"
      },
      {
       "kind": "metricTile",
       "label": "Average Resolution Time",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.averageResolutionTime"
      },
      {
       "kind": "metricTile",
       "label": "First Contact Resolution",
       "provenance": "pack Customer Service_Reference.pdf, page 24 §Display",
       "bindsTo": "ContactCenterOperationsCommandCenterView.firstContactResolution"
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-019"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure and operate the queues through which customer-service cases are organized.",
  "purposeNote": "Administrators can configure specialized service queues and supervisors can operationally adjust them without changing application code.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Membership, Group Sales Support. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Membership",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Support configurable queues such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Group Sales Support",
       "provenance": "pack Customer Service_Reference.pdf, page 25 §Support configurable queues such as"
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-020"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 22 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine the best agent or team to handle each customer request.",
  "purposeNote": "Customer cases are routed to appropriately skilled and available agents using governed routing rules with transparent assignment logic.",
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
    "trigger": "onAction",
    "invalidates": [
     "setIntelligentRoutingSkill"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-021"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define and monitor service-level commitments for different customer-service scenarios.",
  "purposeNote": "cases likely to breach.",
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
    "SlaPolicyServiceLevelManagementView.breached",
    "SlaPolicyServiceLevelManagementView.averageResponse",
    "SlaPolicyServiceLevelManagementView.averageResolution",
    "SlaPolicyServiceLevelManagementView.slaCompliance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-022"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 12 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Give supervisors visibility and control over active customer-service resources.",
  "purposeNote": "Supervisors can understand workload distribution and rebalance service resources before queue or SLA performance deteriorates.",
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
        "AgentWorkloadAvailabilityWorkforceControlView.agent",
        "AgentWorkloadAvailabilityWorkforceControlView.team",
        "AgentWorkloadAvailabilityWorkforceControlView.skills",
        "AgentWorkloadAvailabilityWorkforceControlView.languages",
        "AgentWorkloadAvailabilityWorkforceControlView.status",
        "AgentWorkloadAvailabilityWorkforceControlView.activeCases",
        "AgentWorkloadAvailabilityWorkforceControlView.chats",
        "AgentWorkloadAvailabilityWorkforceControlView.calls",
        "AgentWorkloadAvailabilityWorkforceControlView.queue",
        "AgentWorkloadAvailabilityWorkforceControlView.slaRiskCases",
        "AgentWorkloadAvailabilityWorkforceControlView.averageHandleTime",
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
        "AgentWorkloadAvailabilityWorkforceControlView.agent",
        "AgentWorkloadAvailabilityWorkforceControlView.team",
        "AgentWorkloadAvailabilityWorkforceControlView.skills",
        "AgentWorkloadAvailabilityWorkforceControlView.languages",
        "AgentWorkloadAvailabilityWorkforceControlView.status",
        "AgentWorkloadAvailabilityWorkforceControlView.activeCases",
        "AgentWorkloadAvailabilityWorkforceControlView.chats",
        "AgentWorkloadAvailabilityWorkforceControlView.calls",
        "AgentWorkloadAvailabilityWorkforceControlView.queue",
        "AgentWorkloadAvailabilityWorkforceControlView.slaRiskCases",
        "AgentWorkloadAvailabilityWorkforceControlView.averageHandleTime",
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
    "AgentWorkloadAvailabilityWorkforceControlView.agent",
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
   "board": "wireframes/P12 Venue Support.dc.html#sup-023"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide supervisors with one workspace for cases requiring elevated attention.",
  "purposeNote": "Supervisors can identify, coordinate and resolve critical escalations and systemic service incidents from one central workspace.",
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
        "EscalationCriticalCaseMonitorView.escalatedCases",
        "EscalationCriticalCaseMonitorView.criticalCases",
        "EscalationCriticalCaseMonitorView.slaBreaches",
        "EscalationCriticalCaseMonitorView.vipEscalations",
        "EscalationCriticalCaseMonitorView.financialEscalations",
        "EscalationCriticalCaseMonitorView.eventDayEscalations",
        "EscalationCriticalCaseMonitorView.managementEscalations",
        "EscalationCriticalCaseMonitorView.technicalEscalations",
        "EscalationCriticalCaseMonitorView.case",
        "EscalationCriticalCaseMonitorView.customer",
        "EscalationCriticalCaseMonitorView.reason",
        "EscalationCriticalCaseMonitorView.priority",
        "EscalationCriticalCaseMonitorView.transactionValue",
        "EscalationCriticalCaseMonitorView.event",
        "EscalationCriticalCaseMonitorView.assignedAgent",
        "EscalationCriticalCaseMonitorView.escalatedTo",
        "EscalationCriticalCaseMonitorView.escalationTime",
        "EscalationCriticalCaseMonitorView.sla",
        "EscalationCriticalCaseMonitorView.currentStatus"
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
        "EscalationCriticalCaseMonitorView.escalatedCases",
        "EscalationCriticalCaseMonitorView.criticalCases",
        "EscalationCriticalCaseMonitorView.slaBreaches",
        "EscalationCriticalCaseMonitorView.vipEscalations",
        "EscalationCriticalCaseMonitorView.financialEscalations",
        "EscalationCriticalCaseMonitorView.eventDayEscalations",
        "EscalationCriticalCaseMonitorView.managementEscalations",
        "EscalationCriticalCaseMonitorView.technicalEscalations",
        "EscalationCriticalCaseMonitorView.case",
        "EscalationCriticalCaseMonitorView.customer",
        "EscalationCriticalCaseMonitorView.reason",
        "EscalationCriticalCaseMonitorView.priority",
        "EscalationCriticalCaseMonitorView.transactionValue",
        "EscalationCriticalCaseMonitorView.event",
        "EscalationCriticalCaseMonitorView.assignedAgent",
        "EscalationCriticalCaseMonitorView.escalatedTo",
        "EscalationCriticalCaseMonitorView.escalationTime",
        "EscalationCriticalCaseMonitorView.sla",
        "EscalationCriticalCaseMonitorView.currentStatus"
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
   "preloaded": [
    "EscalationCriticalCaseMonitorView.escalatedCases",
    "EscalationCriticalCaseMonitorView.criticalCases",
    "EscalationCriticalCaseMonitorView.slaBreaches",
    "EscalationCriticalCaseMonitorView.vipEscalations",
    "EscalationCriticalCaseMonitorView.financialEscalations",
    "EscalationCriticalCaseMonitorView.eventDayEscalations"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-024"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure whether customer-service interactions meet TICVAI's defined service-quality standards.",
  "purposeNote": "findings into measurable coaching actions.",
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
   "preloaded": [
    "QualityManagementAgentEvaluationView.greeting",
    "QualityManagementAgentEvaluationView.customerVerification",
    "QualityManagementAgentEvaluationView.understanding",
    "QualityManagementAgentEvaluationView.accuracy",
    "QualityManagementAgentEvaluationView.policyCompliance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-025"
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Measure customer perception of TICVAI's support experience and identify recurring service problems.",
  "purposeNote": "Management can understand what customers think about the service experience and trace negative trends back to their underlying operational causes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Direct Customer Comment. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.positive"
      },
      {
       "kind": "metricTile",
       "label": "Neutral %",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.neutral"
      },
      {
       "kind": "metricTile",
       "label": "Negative %",
       "provenance": "pack Customer Service_Reference.pdf, page 35 §Display",
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.negative"
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
       "bindsTo": "CustomerSatisfactionFeedbackVoiceOfCustomerView.customerEffortWhereMeasured"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
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
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.positive",
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.neutral",
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.negative",
    "CustomerSatisfactionFeedbackVoiceOfCustomerView.complaints"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-026"
  },
  "apisNote": "Regenerated 9 September 2026 from Customer Service_Reference.pdf page 35. 8 of 8 labels bound to a contract property; 9 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Analyze; Compare) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide comprehensive analytics explaining why customers contact TICVAI and what is driving service demand.",
  "purposeNote": "Management can move beyond reporting case volumes and identify the actual product, process and technology issues generating customer demand.",
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
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.firstResponseTime"
      },
      {
       "kind": "metricTile",
       "label": "Resolution Time",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.resolutionTime"
      },
      {
       "kind": "metricTile",
       "label": "First Contact Resolution",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.firstContactResolution"
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
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.slaCompliance"
      },
      {
       "kind": "metricTile",
       "label": "Cost per Case where available",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.costPerCaseWhereAvailable"
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
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze"
      },
      {
       "kind": "metricTile",
       "label": "Complaint Rate",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Analyze",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.complaintRate"
      },
      {
       "kind": "metricTile",
       "label": "Today vs Yesterday",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Compare",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.todayVsYesterday"
      },
      {
       "kind": "metricTile",
       "label": "Week vs Week",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Compare",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.weekVsWeek"
      },
      {
       "kind": "metricTile",
       "label": "Month vs Month",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Compare",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.monthVsMonth"
      },
      {
       "kind": "metricTile",
       "label": "Event vs Event",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Compare",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.eventVsEvent"
      },
      {
       "kind": "metricTile",
       "label": "Venue vs Venue",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Compare",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.venueVsVenue"
      },
      {
       "kind": "metricTile",
       "label": "Product vs Product",
       "provenance": "pack Customer Service_Reference.pdf, page 37 §Compare",
       "bindsTo": "ServiceAnalyticsRootCauseIntelligenceView.productVsProduct"
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
    "ServiceAnalyticsRootCauseIntelligenceView.firstResponseTime",
    "ServiceAnalyticsRootCauseIntelligenceView.resolutionTime",
    "ServiceAnalyticsRootCauseIntelligenceView.firstContactResolution"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-027"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast) and no metric row",
  "purpose": "Create the management-level AI intelligence layer for Customer Service. This is different from 10.1.10 AI Customer Service Copilot. Board 1 Copilot = helps one agent resolve one case. Board 2 AI Intelligence = improves the entire service operation.",
  "purposeNote": "approved low-risk workflows without removing governance over customer-impacting decisions. Board 2 — Final Screen Register",
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
        "AiContactCenterIntelligenceAutomationStudioView.contactVolume",
        "AiContactCenterIntelligenceAutomationStudioView.queueDemand",
        "AiContactCenterIntelligenceAutomationStudioView.requiredAgents",
        "AiContactCenterIntelligenceAutomationStudioView.slaRisk",
        "AiContactCenterIntelligenceAutomationStudioView.expectedComplaints",
        "AiContactCenterIntelligenceAutomationStudioView.eventDaySupportDemand"
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
        "AiContactCenterIntelligenceAutomationStudioView.contactVolume",
        "AiContactCenterIntelligenceAutomationStudioView.queueDemand",
        "AiContactCenterIntelligenceAutomationStudioView.requiredAgents",
        "AiContactCenterIntelligenceAutomationStudioView.slaRisk",
        "AiContactCenterIntelligenceAutomationStudioView.expectedComplaints",
        "AiContactCenterIntelligenceAutomationStudioView.eventDaySupportDemand"
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
    "AiContactCenterIntelligenceAutomationStudioView.contactVolume",
    "AiContactCenterIntelligenceAutomationStudioView.queueDemand",
    "AiContactCenterIntelligenceAutomationStudioView.requiredAgents",
    "AiContactCenterIntelligenceAutomationStudioView.slaRisk",
    "AiContactCenterIntelligenceAutomationStudioView.expectedComplaints",
    "AiContactCenterIntelligenceAutomationStudioView.eventDaySupportDemand"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-028"
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
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AgentWorkloadAvailabilityWorkforceControlView"
 },
 "listContact": {
  "method": "GET",
  "path": "/contact",
  "contract": "marketing-crm",
  "summary": "Contact Center Operations Command Center",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ContactCenterOperationsCommandCenterView"
 },
 "listContactAutomation": {
  "method": "GET",
  "path": "/contact-automation",
  "contract": "marketing-crm",
  "summary": "AI Contact Center Intelligence & Automation Studio",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiContactCenterIntelligenceAutomationStudioView"
 },
 "listCustomerSatisfactionFeedback": {
  "method": "GET",
  "path": "/customer-satisfaction-feedback",
  "contract": "marketing-crm",
  "summary": "Customer Satisfaction, Feedback & Voice of Customer",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CustomerSatisfactionFeedbackVoiceOfCustomerView"
 },
 "listEscalationCriticalCase": {
  "method": "GET",
  "path": "/escalation-critical-case",
  "contract": "marketing-crm",
  "summary": "Escalation & Critical Case Monitor",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EscalationCriticalCaseMonitorView"
 },
 "listQualityAgentEvaluation": {
  "method": "GET",
  "path": "/quality-agent-evaluation",
  "contract": "marketing-crm",
  "summary": "Quality Management & Agent Evaluation",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "QualityManagementAgentEvaluationView"
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
 "listServiceRootCause": {
  "method": "GET",
  "path": "/service-root-cause",
  "contract": "marketing-crm",
  "summary": "Service Analytics & Root-Cause Intelligence",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ServiceAnalyticsRootCauseIntelligenceView"
 },
 "listSlaPolicyService": {
  "method": "GET",
  "path": "/sla-policy-service",
  "contract": "marketing-crm",
  "summary": "SLA Policy & Service-Level Management",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SlaPolicyServiceLevelManagementView"
 },
 "setIntelligentRoutingSkill": {
  "method": "PUT",
  "path": "/intelligent-routing-skill",
  "contract": "marketing-crm",
  "summary": "Intelligent Routing, Skills & Assignment Engine",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "IntelligentRoutingSkillsAssignmentEngineInput",
  "responds": "IntelligentRoutingSkillsAssignmentEngineView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AgentWorkloadAvailabilityWorkforceControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Agent Workload, Availability & Workforce Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "available": {
    "type": "string",
    "description": "Available"
   },
   "busy": {
    "type": "string",
    "description": "Busy"
   },
   "onCall": {
    "type": "string",
    "description": "On Call"
   },
   "chatting": {
    "type": "string",
    "description": "Chatting"
   },
   "afterCallWork": {
    "type": "string",
    "description": "After Call Work"
   },
   "break": {
    "type": "string",
    "description": "Break"
   },
   "training": {
    "type": "string",
    "description": "Training"
   },
   "offline": {
    "type": "integer",
    "description": "Offline"
   },
   "agent": {
    "type": "string",
    "description": "Agent"
   },
   "team": {
    "type": "string",
    "description": "Team"
   },
   "skills": {
    "type": "integer",
    "description": "Skills"
   },
   "languages": {
    "type": "integer",
    "description": "Languages"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "activeCases": {
    "type": "integer",
    "description": "Active Cases"
   },
   "chats": {
    "type": "integer",
    "description": "Chats"
   },
   "calls": {
    "type": "integer",
    "description": "Calls"
   },
   "queue": {
    "type": "string",
    "description": "Queue"
   },
   "slaRiskCases": {
    "type": "integer",
    "description": "SLA Risk Cases"
   },
   "averageHandleTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Handle Time"
   },
   "resolutionRate": {
    "type": "number",
    "description": "Resolution Rate"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization"
   },
   "reassignCases": {
    "type": "string",
    "description": "Reassign Cases"
   },
   "changeAvailability": {
    "type": "string",
    "description": "Change Availability"
   },
   "requestAssistance": {
    "type": "string",
    "description": "Request Assistance"
   },
   "managementWhereApplicable": {
    "type": "string",
    "description": "Management where applicable"
   }
  }
 },
 "AiContactCenterIntelligenceAutomationStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What AI Contact Center Intelligence & Automation Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "cases": {
    "type": "string",
    "description": "Cases"
   },
   "interactions": {
    "type": "string",
    "description": "Interactions"
   },
   "queues": {
    "type": "string",
    "description": "Queues"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "agentPerformance": {
    "type": "string",
    "description": "Agent Performance"
   },
   "qa": {
    "type": "string",
    "description": "QA"
   },
   "customerFeedback": {
    "type": "string",
    "description": "Customer Feedback"
   },
   "orders": {
    "type": "string",
    "description": "Orders"
   },
   "tickets": {
    "type": "string",
    "description": "Tickets"
   },
   "payments": {
    "type": "string",
    "description": "Payments"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "events": {
    "type": "string",
    "description": "Events"
   },
   "systemIncidents": {
    "type": "string",
    "description": "System Incidents"
   },
   "contactVolume": {
    "type": "integer",
    "description": "Contact Volume"
   },
   "queueDemand": {
    "type": "string",
    "description": "Queue Demand"
   },
   "requiredAgents": {
    "type": "string",
    "description": "Required Agents"
   },
   "slaRisk": {
    "type": "string",
    "description": "SLA Risk"
   },
   "expectedComplaints": {
    "type": "string",
    "description": "Expected Complaints"
   },
   "eventDaySupportDemand": {
    "type": "string",
    "description": "Event-Day Support Demand"
   },
   "level1RecommendOnly": {
    "type": "string",
    "description": "Level 1 — Recommend Only"
   },
   "aiSuggestsAction": {
    "type": "string",
    "description": "AI suggests action"
   },
   "level2AgentConfirmation": {
    "type": "string",
    "description": "Level 2 — Agent Confirmation"
   },
   "aiPreparesActionAgentApproves": {
    "type": "string",
    "description": "AI prepares action; agent approves"
   },
   "level3SupervisorGovernedAutomation": {
    "type": "string",
    "description": "Level 3 — Supervisor-Governed Automation"
   },
   "approvedLowRiskWorkflowsExecuteAutomatically": {
    "type": "integer",
    "description": "Approved low-risk workflows execute automatically"
   },
   "onlySpecificallyApprovedScenarios": {
    "type": "string",
    "description": "Only specifically approved scenarios"
   },
   "estimatedAutomationConfidence964": {
    "type": "number",
    "description": "Estimated automation confidence: 96.4%"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "scope": {
    "type": "string",
    "description": "Scope"
   },
   "allowedActions": {
    "type": "string",
    "description": "Allowed Actions"
   },
   "confidenceThreshold": {
    "type": "integer",
    "description": "Confidence Threshold"
   },
   "exceptionHandling": {
    "type": "string",
    "description": "Exception Handling"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "auditTrail": {
    "type": "string",
    "description": "Audit Trail"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective Dates"
   },
   "killSwitch": {
    "type": "string",
    "description": "Kill Switch"
   },
   "management": {
    "type": "string",
    "description": "management"
   }
  }
 },
 "ContactCenterOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Contact Center Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "casesToday": {
    "type": "string",
    "description": "Cases Today"
   },
   "unassignedCases": {
    "type": "integer",
    "description": "Unassigned Cases"
   },
   "customersWaiting": {
    "type": "string",
    "description": "Customers Waiting"
   },
   "criticalCases": {
    "type": "integer",
    "description": "Critical Cases"
   },
   "slaAtRisk": {
    "type": "string",
    "description": "SLA At Risk"
   },
   "slaBreached": {
    "type": "string",
    "description": "SLA Breached"
   },
   "casesResolvedToday": {
    "type": "string",
    "description": "Cases Resolved Today"
   },
   "firstResponseTime": {
    "type": "string",
    "format": "date-time",
    "description": "First Response Time"
   },
   "averageResolutionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Resolution Time"
   },
   "firstContactResolution": {
    "type": "string",
    "description": "First Contact Resolution"
   },
   "csat": {
    "type": "string",
    "description": "CSAT"
   },
   "activeAgents": {
    "type": "integer",
    "description": "Active Agents"
   },
   "agentUtilization": {
    "type": "number",
    "description": "Agent Utilization"
   },
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
   "whatsapp": {
    "type": "string",
    "description": "WhatsApp"
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
   "socialChannelsWhereIntegrated": {
    "type": "string",
    "description": "Social channels where integrated"
   },
   "frontDesk": {
    "type": "string",
    "description": "Front Desk"
   },
   "frontPos": {
    "type": "integer",
    "description": "Front POS"
   },
   "nNgRiskTs": {
    "type": "string",
    "description": "n ng Risk ts"
   },
   "ng": {
    "type": "string",
    "description": "ng"
   }
  }
 },
 "CustomerSatisfactionFeedbackVoiceOfCustomerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Customer Satisfaction, Feedback & Voice of Customer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "csat": {
    "type": "string",
    "description": "CSAT"
   },
   "serviceRating": {
    "type": "string",
    "description": "Service Rating"
   },
   "npsWhereUsed": {
    "type": "string",
    "description": "NPS where used"
   },
   "postCaseSurvey": {
    "type": "string",
    "description": "Post-Case Survey"
   },
   "complaint": {
    "type": "string",
    "description": "Complaint"
   },
   "appFeedback": {
    "type": "string",
    "description": "App Feedback"
   },
   "webFeedback": {
    "type": "string",
    "description": "Web Feedback"
   },
   "directCustomerComment": {
    "type": "string",
    "description": "Direct Customer Comment"
   },
   "surveyResponseRate": {
    "type": "number",
    "description": "Survey Response Rate"
   },
   "positive": {
    "type": "number",
    "description": "Positive %"
   },
   "neutral": {
    "type": "number",
    "description": "Neutral %"
   },
   "negative": {
    "type": "number",
    "description": "Negative %"
   },
   "complaints": {
    "type": "integer",
    "description": "Complaints"
   },
   "repeatContactRate": {
    "type": "number",
    "description": "Repeat Contact Rate"
   },
   "customerEffortWhereMeasured": {
    "type": "string",
    "description": "Customer Effort where measured"
   },
   "agent": {
    "type": "string",
    "description": "Agent"
   },
   "team": {
    "type": "string",
    "description": "Team"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "caseType": {
    "type": "string",
    "description": "Case Type"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "sentiment": {
    "type": "string",
    "description": "Sentiment"
   },
   "topic": {
    "type": "string",
    "description": "Topic"
   },
   "case": {
    "type": "string",
    "description": "Case"
   },
   "productEvent": {
    "type": "string",
    "description": "Product/Event"
   },
   "rating": {
    "type": "string",
    "description": "Rating"
   },
   "followUpCase": {
    "type": "string",
    "description": "Follow-up Case"
   },
   "supervisorTask": {
    "type": "string",
    "description": "Supervisor Task"
   },
   "complaintReview": {
    "type": "string",
    "description": "Complaint Review"
   }
  }
 },
 "EscalationCriticalCaseMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Escalation & Critical Case Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "escalatedCases": {
    "type": "integer",
    "description": "Escalated Cases"
   },
   "criticalCases": {
    "type": "integer",
    "description": "Critical Cases"
   },
   "slaBreaches": {
    "type": "integer",
    "description": "SLA Breaches"
   },
   "vipEscalations": {
    "type": "integer",
    "description": "VIP Escalations"
   },
   "financialEscalations": {
    "type": "integer",
    "description": "Financial Escalations"
   },
   "eventDayEscalations": {
    "type": "integer",
    "description": "Event-Day Escalations"
   },
   "managementEscalations": {
    "type": "integer",
    "description": "Management Escalations"
   },
   "technicalEscalations": {
    "type": "integer",
    "description": "Technical Escalations"
   },
   "case": {
    "type": "string",
    "description": "Case"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "transactionValue": {
    "type": "string",
    "description": "Transaction Value"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "assignedAgent": {
    "type": "string",
    "description": "Assigned Agent"
   },
   "escalatedTo": {
    "type": "string",
    "description": "Escalated To"
   },
   "escalationTime": {
    "type": "string",
    "format": "date-time",
    "description": "Escalation Time"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "currentStatus": {
    "type": "integer",
    "description": "Current Status"
   }
  }
 },
 "IntelligentRoutingSkillsAssignmentEngineInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is marketing.message_trigger at 11%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Intelligent Routing, Skills & Assignment Engine submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "caseCategory": {
    "type": "string",
    "description": "Case Category"
   },
   "subcategory": {
    "type": "string",
    "description": "Subcategory"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerLanguage": {
    "type": "string",
    "description": "Customer Language"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "membershipTier": {
    "type": "string",
    "description": "Membership Tier"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "agentSkill": {
    "type": "string",
    "description": "Agent Skill"
   },
   "agentAvailability": {
    "type": "string",
    "description": "Agent Availability"
   },
   "currentWorkload": {
    "type": "string",
    "description": "Current Workload"
   },
   "eventProximity": {
    "type": "string",
    "description": "Event Proximity"
   },
   "caseTicketReschedule": {
    "type": "string",
    "description": "Case: Ticket reschedule"
   },
   "languageArabic": {
    "type": "string",
    "description": "Language: Arabic"
   },
   "priorityHigh": {
    "type": "string",
    "description": "Priority: High"
   },
   "type": {
    "type": "string",
    "enum": [
     "arabicSkill",
     "ticketingSkill",
     "currentWorkload62",
     "slaCapability"
    ],
    "description": "Vocabulary listed under Reason."
   }
  }
 },
 "IntelligentRoutingSkillsAssignmentEngineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Intelligent Routing, Skills & Assignment Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "caseCategory": {
    "type": "string",
    "description": "Case Category"
   },
   "subcategory": {
    "type": "string",
    "description": "Subcategory"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerLanguage": {
    "type": "string",
    "description": "Customer Language"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "membershipTier": {
    "type": "string",
    "description": "Membership Tier"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "agentSkill": {
    "type": "string",
    "description": "Agent Skill"
   },
   "agentAvailability": {
    "type": "string",
    "description": "Agent Availability"
   },
   "currentWorkload": {
    "type": "string",
    "description": "Current Workload"
   },
   "eventProximity": {
    "type": "string",
    "description": "Event Proximity"
   },
   "caseTicketReschedule": {
    "type": "string",
    "description": "Case: Ticket reschedule"
   },
   "languageArabic": {
    "type": "string",
    "description": "Language: Arabic"
   },
   "priorityHigh": {
    "type": "string",
    "description": "Priority: High"
   },
   "type": {
    "type": "string",
    "enum": [
     "arabicSkill",
     "ticketingSkill",
     "currentWorkload62",
     "slaCapability"
    ],
    "description": "Vocabulary listed under Reason."
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
 "QualityManagementAgentEvaluationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Quality Management & Agent Evaluation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "greeting": {
    "type": "string",
    "description": "Greeting"
   },
   "customerVerification": {
    "type": "string",
    "description": "Customer Verification"
   },
   "understanding": {
    "type": "string",
    "description": "Understanding"
   },
   "accuracy": {
    "type": "string",
    "description": "Accuracy"
   },
   "policyCompliance": {
    "type": "string",
    "description": "Policy Compliance"
   },
   "communicationQuality": {
    "type": "string",
    "description": "Communication Quality"
   },
   "empathy": {
    "type": "string",
    "description": "Empathy"
   },
   "resolution": {
    "type": "string",
    "description": "Resolution"
   },
   "documentation": {
    "type": "string",
    "description": "Documentation"
   },
   "closing": {
    "type": "string",
    "description": "Closing"
   },
   "call": {
    "type": "string",
    "description": "Call"
   },
   "chat": {
    "type": "string",
    "description": "Chat"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "whatsapp": {
    "type": "string",
    "description": "WhatsApp"
   },
   "case": {
    "type": "string",
    "description": "Case"
   },
   "complaint": {
    "type": "string",
    "description": "Complaint"
   },
   "policyAdherence": {
    "type": "string",
    "description": "Policy adherence"
   },
   "requiredStatements": {
    "type": "string",
    "description": "Required statements"
   },
   "tone": {
    "type": "string",
    "description": "Tone"
   },
   "resolutionQuality": {
    "type": "string",
    "description": "Resolution quality"
   },
   "missingCaseDocumentation": {
    "type": "string",
    "description": "Missing case documentation"
   },
   "productTraining": {
    "type": "string",
    "description": "Product Training"
   },
   "policyTraining": {
    "type": "string",
    "description": "Policy Training"
   },
   "communicationCoaching": {
    "type": "string",
    "description": "Communication Coaching"
   },
   "systemTraining": {
    "type": "string",
    "description": "System Training"
   }
  }
 },
 "ServiceAnalyticsRootCauseIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Service Analytics & Root-Cause Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "contactVolume": {
    "type": "integer",
    "description": "Contact Volume"
   },
   "cases": {
    "type": "string",
    "description": "Cases"
   },
   "firstResponseTime": {
    "type": "string",
    "format": "date-time",
    "description": "First Response Time"
   },
   "resolutionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Resolution Time"
   },
   "firstContactResolution": {
    "type": "string",
    "description": "First Contact Resolution"
   },
   "reopenRate": {
    "type": "number",
    "description": "Reopen Rate"
   },
   "escalationRate": {
    "type": "number",
    "description": "Escalation Rate"
   },
   "slaCompliance": {
    "type": "string",
    "description": "SLA Compliance"
   },
   "costPerCaseWhereAvailable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost per Case where available"
   },
   "csat": {
    "type": "string",
    "description": "CSAT"
   },
   "complaintRate": {
    "type": "number",
    "description": "Complaint Rate"
   },
   "todayVsYesterday": {
    "type": "string",
    "description": "Today vs Yesterday"
   },
   "weekVsWeek": {
    "type": "string",
    "description": "Week vs Week"
   },
   "monthVsMonth": {
    "type": "string",
    "description": "Month vs Month"
   },
   "eventVsEvent": {
    "type": "string",
    "description": "Event vs Event"
   },
   "venueVsVenue": {
    "type": "string",
    "description": "Venue vs Venue"
   },
   "productVsProduct": {
    "type": "string",
    "description": "Product vs Product"
   },
   "betterB2cInformation": {
    "type": "string",
    "description": "Better B2C information"
   },
   "selfService": {
    "type": "string",
    "description": "Self-service"
   },
   "productConfiguration": {
    "type": "string",
    "description": "Product configuration"
   },
   "improvedNotifications": {
    "type": "string",
    "description": "Improved notifications"
   },
   "technicalFixes": {
    "type": "string",
    "description": "Technical fixes"
   },
   "betterTicketDelivery": {
    "type": "string",
    "description": "Better ticket delivery"
   }
  }
 },
 "SlaPolicyServiceLevelManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What SLA Policy & Service-Level Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "firstResponseSla": {
    "type": "string",
    "description": "First Response SLA"
   },
   "nextResponseSla": {
    "type": "string",
    "format": "date-time",
    "description": "Next Response SLA"
   },
   "resolutionSla": {
    "type": "string",
    "description": "Resolution SLA"
   },
   "internalEscalationSla": {
    "type": "string",
    "description": "Internal Escalation SLA"
   },
   "complaintResolutionSla": {
    "type": "string",
    "description": "Complaint Resolution SLA"
   },
   "caseType": {
    "type": "string",
    "description": "Case Type"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerTier": {
    "type": "string",
    "description": "Customer Tier"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "groupCustomer": {
    "type": "string",
    "description": "Group Customer"
   },
   "firstResponse5Minutes": {
    "type": "string",
    "description": "First Response: 5 minutes"
   },
   "resolutionTarget30Minutes": {
    "type": "string",
    "description": "Resolution Target: 30 minutes"
   },
   "firstResponse4Hours": {
    "type": "string",
    "description": "First Response: 4 hours"
   },
   "resolutionTarget24Hours": {
    "type": "string",
    "description": "Resolution Target: 24 hours"
   },
   "calendarTime": {
    "type": "string",
    "format": "date-time",
    "description": "Calendar time"
   },
   "businessHours": {
    "type": "string",
    "description": "Business hours"
   },
   "venueOperatingHours": {
    "type": "string",
    "description": "Venue operating hours"
   },
   "pausedStates": {
    "type": "string",
    "description": "Paused states"
   },
   "holidayCalendars": {
    "type": "string",
    "description": "Holiday calendars"
   },
   "withinSla": {
    "type": "string",
    "description": "Within SLA"
   },
   "atRisk": {
    "type": "string",
    "description": "At Risk"
   },
   "breached": {
    "type": "string",
    "description": "Breached"
   },
   "averageResponse": {
    "type": "number",
    "description": "Average Response"
   },
   "averageResolution": {
    "type": "number",
    "description": "Average Resolution"
   },
   "slaCompliance": {
    "type": "number",
    "description": "SLA Compliance %"
   }
  }
 }
}
```
