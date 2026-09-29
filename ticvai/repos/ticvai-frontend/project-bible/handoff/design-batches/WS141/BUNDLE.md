# WS141 — Marketing CRM Configuration Reference v1.0 board 7

**10 screens · 18 operations · 20 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_CONFIGURE, CASE_MANAGE, CASE_VIEW, GUEST_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-794` | Omnichannel Command Center | listDetail | 1 | 0 | — |
| `BO-795` | Unified Inbox | listDetail | 2 | 0 | — |
| `BO-796` | Guest Conversation 360 | listDetail | 2 | 0 | — |
| `BO-797` | AI Chatbot Configuration | listDetail | 1 | 0 | — |
| `BO-798` | Intent & Knowledge Management | listDetail | 1 | 0 | — |
| `BO-799` | Agent Workspace | listDetail | 4 | 0 | — |
| `BO-800` | Routing & Queue Management | listDetail | 5 | 1 | — |
| `BO-801` | Sales & Service Actions | listDetail | 1 | 0 | — |
| `BO-802` | Sentiment, Quality & Escalation | listDetail | 2 | 0 | — |
| `BO-803` | Chat Analytics & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-794, BO-795, BO-796, BO-797, BO-798, BO-799, BO-801, BO-802, BO-803 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-794",
  "name": "Omnichannel Command Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "01",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/omnichannel-command-center-bo-794",
   "component": "apps/venue-management-web/src/routes/engagement-support/OmnichannelCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-795",
    "BO-796",
    "BO-797",
    "BO-798",
    "BO-799",
    "BO-800",
    "BO-801",
    "BO-802",
    "BO-803"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-795",
     "trigger": "Unified Inbox",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "conversationId"
     ]
    },
    {
     "to": "BO-796",
     "trigger": "Guest Conversation 360",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "conversationId"
     ]
    },
    {
     "to": "BO-797",
     "trigger": "AI Chatbot Configuration",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-798",
     "trigger": "Intent & Knowledge Management",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-799",
     "trigger": "Agent Workspace",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "conversationId"
     ]
    },
    {
     "to": "BO-800",
     "trigger": "Routing & Queue Management",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-801",
     "trigger": "Sales & Service Actions",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-802",
     "trigger": "Sentiment, Quality & Escalation",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "caseId"
     ]
    },
    {
     "to": "BO-803",
     "trigger": "Chat Analytics & Audit",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor conversation demand, service level and commercial contribution. Show open, waiting, SLA-risk and escalated conversations, bot containment, agent handover, response and resolution time. Display CSAT, conversions, revenue and queue/channel/venue distribution with trend and capacity indicators. Surface outages, knowledge gaps, negative sentiment spikes and overloaded queues. Provide role-specific drill-down for supervisors, agents, sales, support and administrators. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 36"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 36"
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
       "impliedBy": "listConversations",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The omnichannel list.",
   "error": "Could not load. Names which read failed and leaves the omnichannel untouched.",
   "emptyFirstRun": "No omnichannel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the omnichannel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConversations",
    "contract": "marketing-crm",
    "purpose": "Conversations across channels",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-794",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-794"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 36. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-795",
  "name": "Unified Inbox",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "02",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/unified-inbox-bo-795",
   "component": "apps/venue-management-web/src/routes/engagement-support/UnifiedInbox.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-794"
   ],
   "exitTo": [
    "BO-794"
   ],
   "transitions": [
    {
     "to": "BO-794",
     "trigger": "Back to Omnichannel Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Consolidate all guest conversations into one manageable queue. Ingest email, SMS, WhatsApp, social, webchat, mobile-app chat and supported voice/messaging channels. Provide queue and channel filters, assignment, priority, unread state, SLA clock, search and saved views. Display the active conversation, rich messages, attachments, delivery/read status and internal notes. Prevent duplicate threads through identity and conversation correlation and retain the source channel. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 36"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 36"
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
       "impliedBy": "listConversations",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "claimConversation",
       "label": "Claim conversation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "claimConversation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The unified list.",
   "error": "Could not load. Names which read failed and leaves the unified untouched.",
   "emptyFirstRun": "No unified yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the unified are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConversations",
    "contract": "marketing-crm",
    "purpose": "The unified inbox",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "claimConversation",
    "contract": "marketing-crm",
    "purpose": "Take one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-795",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-795"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 36. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "conversationId",
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
 },
 {
  "id": "BO-796",
  "name": "Guest Conversation 360",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "03",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/guest-conversation-360-bo-796",
   "component": "apps/venue-management-web/src/routes/engagement-support/GuestConversation360.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-794"
   ],
   "exitTo": [
    "BO-794"
   ],
   "transitions": [
    {
     "to": "BO-794",
     "trigger": "Back to Omnichannel Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Combine conversation history with the identified guest's CRM context. Resolve the guest and display profile, value, tickets, reservations, membership, loyalty, wallet and open cases. Configuration Scope of Work | Version 1.0 36 Show all prior conversations across channels in chronological order with intent, outcome and agent/bot ownership. Allow authorized users to open linked records without losing the current conversation. Mask or restrict sensitive information and show confidence when identity is uncertain. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 36"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 36"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getConversation",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest conversation 360 list.",
   "error": "Could not load. Names which read failed and leaves the guest conversation 360 untouched.",
   "emptyFirstRun": "No guest conversation 360 yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest conversation 360 are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getConversation",
    "contract": "marketing-crm",
    "purpose": "The conversation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getGuestTimeline",
    "contract": "marketing-crm",
    "purpose": "What else they have done",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-796",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-796"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 36. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "conversationId",
     "from": "navigation"
    },
    {
     "name": "guestId",
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
 },
 {
  "id": "BO-797",
  "name": "AI Chatbot Configuration",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "04",
   "page": 37
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/ai-chatbot-configuration-bo-797",
   "component": "apps/venue-management-web/src/routes/engagement-support/AiChatbotConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-794"
   ],
   "exitTo": [
    "BO-794"
   ],
   "transitions": [
    {
     "to": "BO-794",
     "trigger": "Back to Omnichannel Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the AI assistant's identity, scope and operating controls. Set bot name, personality, tone, supported languages, channels, operating hours and brand/venue context. Configure confidence thresholds, fallback, authentication, guest-data access and maximum automated turns. Define permitted sales/service actions, prohibited topics, safe responses and human-handover conditions. Version, approve, test and audit configuration before deployment to any channel. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 37"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 37"
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
       "impliedBy": "setCustomerServiceCopilot",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
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
   "loading": "The chatbot list.",
   "error": "Could not load. Names which read failed and leaves the chatbot untouched.",
   "emptyFirstRun": "No chatbot yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the chatbot are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCustomerServiceCopilot",
    "contract": "marketing-crm",
    "purpose": "Chatbot configuration",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-797",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-797"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 37. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-798",
  "name": "Intent & Knowledge Management",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "05",
   "page": 37
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/intent-knowledge-management-bo-798",
   "component": "apps/venue-management-web/src/routes/engagement-support/IntentKnowledgeManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-794"
   ],
   "exitTo": [
    "BO-794"
   ],
   "transitions": [
    {
     "to": "BO-794",
     "trigger": "Back to Omnichannel Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage what the assistant understands and the information it may use. Maintain intents, example phrases, entities, synonyms, redirects, confidence and response variants. Connect approved FAQs, product data, policies, manuals and structured knowledge with freshness and ownership. Provide test console, expected result, source citation, ambiguity handling and low-confidence review queue. Track knowledge consumers, sync status, changes and answer-quality feedback. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 37"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 37"
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
       "impliedBy": "setCustomerServiceCopilot",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
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
   "loading": "The intent knowledge list.",
   "error": "Could not load. Names which read failed and leaves the intent knowledge untouched.",
   "emptyFirstRun": "No intent knowledge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the intent knowledge are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCustomerServiceCopilot",
    "contract": "marketing-crm",
    "purpose": "Intent and knowledge",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-798",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-798"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 37. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-799",
  "name": "Agent Workspace",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "06",
   "page": 37
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/agent-workspace-bo-799",
   "component": "apps/venue-management-web/src/routes/engagement-support/AgentWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-794"
   ],
   "exitTo": [
    "BO-794"
   ],
   "transitions": [
    {
     "to": "BO-794",
     "trigger": "Back to Omnichannel Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give live agents the context and tools required to resolve conversations efficiently. Provide active conversation, transcript, guest context, AI reply suggestion, canned responses and translation. Support rich messages, attachments, internal notes, tags, tasks, transfer and supervisor assistance. Expose authorized ticket, reservation, membership, loyalty, wallet and case actions without switching applications. Track agent presence, typing, ownership, response time, action outcomes and complete transcript history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 37",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 37"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 37"
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
       "impliedBy": "sendConversationMessage",
       "label": "Send conversation message",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "sendConversationMessage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The agent list.",
   "error": "Could not load. Names which read failed and leaves the agent untouched.",
   "emptyFirstRun": "No agent yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the agent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "sendConversationMessage",
    "contract": "marketing-crm",
    "purpose": "Reply",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "handoverToAgent",
    "contract": "marketing-crm",
    "purpose": "Take it from the bot",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setCallDisposition",
    "contract": "marketing-crm",
    "purpose": "Record why the conversation ended and any callback",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "startKioskAssist",
    "contract": "marketing-crm",
    "purpose": "Help a guest at a kiosk remotely",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-799",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-799"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 37. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "conversationId",
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
 },
 {
  "id": "BO-800",
  "name": "Routing & Queue Management",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "07",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/routing-queue-management-bo-800",
   "component": "apps/venue-management-web/src/routes/engagement-support/RoutingQueueManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-794"
   ],
   "exitTo": [
    "BO-794"
   ],
   "transitions": [
    {
     "to": "BO-794",
     "trigger": "Back to Omnichannel Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Route work to the correct team and balance workload. Create rules by intent, skill, department, venue, attraction, language, guest tier, priority and SLA risk. Configure queues, capacity, operating hours, overflow, assignment method, workload limits and fallback. Provide live queue counts, wait time, agent utilization, reassignment, pickup and supervisor override. Record the evaluated rule, routing reason, transfers and any manual intervention. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 38"
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
       "impliedBy": "setIntelligentRoutingSkill",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAgentWorkloadAvailability",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
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
   "loading": "The routing queue list.",
   "error": "Could not load. Names which read failed and leaves the routing queue untouched.",
   "emptyFirstRun": "No routing queue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the routing queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setIntelligentRoutingSkill",
    "contract": "marketing-crm",
    "purpose": "Routing and queues",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAgentWorkloadAvailability",
    "contract": "marketing-crm",
    "purpose": "Who is free",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
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
   },
   {
    "operationId": "setServiceQueueDefinition",
    "contract": "marketing-crm",
    "purpose": "Create or change a customer-service queue",
    "trigger": "onAction",
    "invalidates": [
     "listAgentWorkloadAvailability",
     "listCaseCategories",
     "listServiceQueues"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-800",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-800"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-801",
  "name": "Sales & Service Actions",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "08",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/sales-service-actions-bo-801",
   "component": "apps/venue-management-web/src/routes/engagement-support/SalesServiceActions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-794"
   ],
   "exitTo": [
    "BO-794"
   ],
   "transitions": [
    {
     "to": "BO-794",
     "trigger": "Back to Omnichannel Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow agents and AI to perform governed transactional actions. Create or modify tickets and reservations and view capacity, eligibility, price and policy before confirmation. Manage membership information, loyalty rewards and wallet top-ups within configured authority. Generate secure payment links, vouchers, QR tickets, forms and rich messages and confirm delivery. Create and escalate cases and require authentication, approval or live-agent control for sensitive actions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 38"
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
       "impliedBy": "setOrderBookingTicket",
       "label": "Save order booking ticket",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setOrderBookingTicket"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sales service actions list.",
   "error": "Could not load. Names which read failed and leaves the sales service actions untouched.",
   "emptyFirstRun": "No sales service actions yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sales service actions are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setOrderBookingTicket",
    "contract": "marketing-crm",
    "purpose": "Act on the order from the conversation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-801",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-801"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-802",
  "name": "Sentiment, Quality & Escalation",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "09",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/sentiment-quality-escalation-bo-802",
   "component": "apps/venue-management-web/src/routes/engagement-support/SentimentQualityEscalation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-794"
   ],
   "exitTo": [
    "BO-794"
   ],
   "transitions": [
    {
     "to": "BO-794",
     "trigger": "Back to Omnichannel Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Detect conversation risk and support consistent service quality. Analyze sentiment, emotion, urgency, intent confidence, compliance and quality score in near real time. Configure thresholds for supervisor alert, priority change, queue transfer, case creation or live- agent takeover. Provide transcript review, AI rationale, quality checklist, coaching notes and appeal/override controls. Monitor false positives, bias, model drift and outcomes and audit automated and human escalations. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 38"
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
       "impliedBy": "listQualityAgentEvaluation",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "escalateCase",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "escalateCase"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sentiment quality escalation list.",
   "error": "Could not load. Names which read failed and leaves the sentiment quality escalation untouched.",
   "emptyFirstRun": "No sentiment quality escalation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sentiment quality escalation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQualityAgentEvaluation",
    "contract": "marketing-crm",
    "purpose": "Sentiment, quality and escalation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "escalateCase",
    "contract": "marketing-crm",
    "purpose": "Escalate",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-802",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-802"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "caseId",
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
 },
 {
  "id": "BO-803",
  "name": "Chat Analytics & Audit",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "7",
   "number": "10",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/chat-analytics-audit-bo-803",
   "component": "apps/venue-management-web/src/routes/engagement-support/ChatAnalyticsAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-794"
   ],
   "exitTo": [
    "BO-794"
   ],
   "transitions": [
    {
     "to": "BO-794",
     "trigger": "Back to Omnichannel Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure channel, chatbot and agent performance and preserve conversation evidence. Report volume, response, resolution, abandonment, containment, handover, transfer, conversion, revenue and CSAT. Compare channel, queue, venue, intent, language, bot version, agent and time period. Configuration Scope of Work | Version 1.0 38 Provide conversation drill-down, action trace, AI/human ownership, case links and payment/sales outcome. Audit messages, transfers, AI actions, escalations, administrative changes and data access. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 39 Board 8 - Case Management, SLA & Service Recovery Figure 8. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 40",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 38"
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
       "impliedBy": "listUnifiedInteractionCommunication",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The chat analytics audit list.",
   "error": "Could not load. Names which read failed and leaves the chat analytics audit untouched.",
   "emptyFirstRun": "No chat analytics audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the chat analytics audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUnifiedInteractionCommunication",
    "contract": "marketing-crm",
    "purpose": "Chat analytics and audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-803",
   "workshopBoard": "wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-803"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getGuestTimeline": {
  "method": "GET",
  "path": "/guests/{guestId}/timeline",
  "contract": "marketing-crm",
  "summary": "Everything this guest did, in order, across the platform",
  "permission": "GUEST_VIEW",
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
    "name": "kinds",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestTimelineEvent"
 },
 "handoverToAgent": {
  "method": "POST",
  "path": "/conversations/{conversationId}/handover",
  "contract": "marketing-crm",
  "summary": "Pass an assistant conversation to a person",
  "permission": null,
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
 "setCallDisposition": {
  "method": "POST",
  "path": "/conversations/{conversationId}/disposition",
  "contract": "marketing-crm",
  "summary": "Why the conversation ended, and any callback",
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
  "requestBody": "CallDisposition",
  "responds": "CallDisposition"
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
 },
 "startKioskAssist": {
  "method": "POST",
  "path": "/kiosk-assists",
  "contract": "marketing-crm",
  "summary": "A staff member helps a guest at a kiosk, remotely",
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
  "responds": "KioskAssistSession"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "CallDisposition": {
  "type": "object",
  "description": "BL-082. **A conversation could be closed and nothing recorded why it ended** — information, no sale, sale successful. **That is the measure a contact centre runs on**, and its absence makes every conversation look identical in a report.\n",
  "required": [
   "outcome"
  ],
  "properties": {
   "outcome": {
    "type": "string",
    "enum": [
     "information",
     "resolved",
     "noSale",
     "saleCompleted",
     "callbackScheduled",
     "escalated",
     "wrongNumber",
     "abandoned",
     "unreachable"
    ]
   },
   "callbackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**An agent could not schedule a callback with the case attached**, so a promise to ring back lived in somebody's notebook.\n"
   },
   "callbackAssignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
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
 "GuestTimelineEvent": {
  "type": "object",
  "description": "Board 1.5. **Facts, notes and predictions distinguished on the row.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "kind": {
    "type": "string",
    "enum": [
     "purchase",
     "ticketUsed",
     "reservation",
     "visit",
     "membershipChange",
     "loyalty",
     "wallet",
     "campaign",
     "message",
     "case",
     "survey",
     "waiver",
     "note",
     "prediction"
    ]
   },
   "nature": {
    "type": "string",
    "enum": [
     "operationalFact",
     "userNote",
     "aiDerived"
    ],
    "description": "**A prediction and a gate scan are both useful and only one happened.**"
   },
   "summary": {
    "type": "string"
   },
   "channel": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceContract": {
    "type": "string",
    "nullable": true
   },
   "sourceReferenceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "value": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "outcome": {
    "type": "string",
    "nullable": true
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
 "KioskAssistSession": {
  "type": "object",
  "x-ticvai-persistence": "marketing.kiosk_assist_session",
  "description": "2.1.25. A staff member acting on a kiosk session remotely. **The guest can always see it and always end it** — remote assistance a guest cannot see or stop is surveillance.\n",
  "required": [
   "id",
   "deviceId",
   "staffPrincipalId",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "deviceId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "staffPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "staffDisplayName": {
    "type": "string",
    "description": "**Shown on the kiosk.** A guest being helped should know by whom.\n"
   },
   "cartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "enum": [
     "guestCalled",
     "healthAlert",
     "stuckSession",
     "paymentIssue",
     "proactive"
    ]
   },
   "endedBy": {
    "type": "string",
    "nullable": true,
    "enum": [
     "staff",
     "guest",
     "timeout"
    ]
   },
   "actionsTaken": {
    "type": "array",
    "description": "**Every action recorded as the staff member's**, not the kiosk's. A cashier completing a guest's checkout remotely is a staff action on a guest cart.\n",
    "items": {
     "type": "object",
     "properties": {
      "operationId": {
       "type": "string"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "endedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID; equals the `Idempotency-Key` header."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Required with `execute`; the action is recorded on this case."
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 }
}
```
