# WS140 — Marketing CRM Configuration Reference v1.0 board 6

**10 screens · 13 operations · 12 schemas · 4 permissions**

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
  `GUEST_MANAGE, MARKETING_MANAGE, MARKETING_SEND, MARKETING_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-784` | Communications Center | listDetail | 1 | 0 | — |
| `BO-785` | Template Library | listDetail | 2 | 0 | — |
| `BO-786` | Newsletter Builder | listDetail | 1 | 0 | — |
| `BO-787` | Content Blocks & Product Feed | listDetail | 1 | 0 | — |
| `BO-788` | Subscriptions & Preferences | listDetail | 3 | 0 | — |
| `BO-789` | Transactional Notification Rules | listDetail | 2 | 0 | — |
| `BO-790` | Scheduling, Priority & Approval | listDetail | 1 | 0 | — |
| `BO-791` | Delivery, Retry & Failover | listDetail | 2 | 0 | — |
| `BO-792` | Deliverability & Analytics | listDetail | 1 | 0 | — |
| `BO-793` | AI Content, Translation & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-784, BO-785, BO-786, BO-787, BO-788, BO-789, BO-790, BO-791, BO-792, BO-793 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-784",
  "name": "Communications Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "01",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/communications-center-bo-784",
   "component": "apps/venue-management-web/src/routes/engagement-support/CommunicationsCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-785",
    "BO-786",
    "BO-787",
    "BO-788",
    "BO-789",
    "BO-790",
    "BO-791",
    "BO-792",
    "BO-793"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-785",
     "trigger": "Template Library",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-786",
     "trigger": "Newsletter Builder",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-787",
     "trigger": "Content Blocks & Product Feed",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-788",
     "trigger": "Subscriptions & Preferences",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-789",
     "trigger": "Transactional Notification Rules",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-790",
     "trigger": "Scheduling, Priority & Approval",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-791",
     "trigger": "Delivery, Retry & Failover",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-792",
     "trigger": "Deliverability & Analytics",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-793",
     "trigger": "AI Content, Translation & Audit",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor outbound communication volume, delivery and engagement. Show messages sent, delivered, failed, opened, clicked, converted and unsubscribed with attributed revenue. Compare email, SMS, WhatsApp, push, in-app, web and operational channels and providers. Display active alerts for provider outage, high bounce, consent error, queue delay or retry exhaustion. Filter and drill down by tenant, brand, venue, region, template, category, channel and date. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 31"
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
       "impliedBy": "listCommunicationService",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The communications list.",
   "error": "Could not load. Names which read failed and leaves the communications untouched.",
   "emptyFirstRun": "No communications yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the communications are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommunicationService",
    "contract": "marketing-crm",
    "purpose": "Channel health and volume",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-784",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-784"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-785",
  "name": "Template Library",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "02",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/template-library-bo-785",
   "component": "apps/venue-management-web/src/routes/engagement-support/TemplateLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-784"
   ],
   "exitTo": [
    "BO-784"
   ],
   "transitions": [
    {
     "to": "BO-784",
     "trigger": "Back to Communications Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Centrally manage reusable message templates. Organize marketing, ticketing, reservation, membership, loyalty, wallet and operational templates by channel and purpose. Maintain brand, venue, language, version, owner, approval, validity and active/inactive status. Preview test data, validate required tokens, links, attachments and channel-specific constraints. Clone, archive and compare templates while preserving lineage and complete change history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 31"
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
       "impliedBy": "listMessageTemplates",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createMessageTemplate",
       "label": "Create message template",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createMessageTemplate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The template list.",
   "error": "Could not load. Names which read failed and leaves the template untouched.",
   "emptyFirstRun": "No template yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the template are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMessageTemplates",
    "contract": "marketing-crm",
    "purpose": "The template library",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createMessageTemplate",
    "contract": "marketing-crm",
    "purpose": "Create one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-785",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-785"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-786",
  "name": "Newsletter Builder",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "03",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/newsletter-builder-bo-786",
   "component": "apps/venue-management-web/src/routes/engagement-support/NewsletterBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-784"
   ],
   "exitTo": [
    "BO-784"
   ],
   "transitions": [
    {
     "to": "BO-784",
     "trigger": "Back to Communications Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create responsive, branded newsletters without coding. Provide drag-and-drop header, text, image, event, ticket, membership, loyalty, CTA, divider and footer blocks. Configuration Scope of Work | Version 1.0 31 Support personalization, dynamic content, reusable templates, language variants and desktop/mobile preview. Validate accessibility, links, unsubscribe content, sender details and deliverability before test or approval. Support draft, test send, review, approve, schedule, clone and version-management workflows. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**Newsletter Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 31"
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
       "impliedBy": "createMessageTemplate",
       "label": "Create message template",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createMessageTemplate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The newsletter list.",
   "error": "Could not load. Names which read failed and leaves the newsletter untouched.",
   "emptyFirstRun": "No newsletter yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the newsletter are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createMessageTemplate",
    "contract": "marketing-crm",
    "purpose": "Build a newsletter",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-786",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-786"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-787",
  "name": "Content Blocks & Product Feed",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "04",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/content-blocks-product-feed-bo-787",
   "component": "apps/venue-management-web/src/routes/engagement-support/ContentBlocksProductFeed.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-784"
   ],
   "exitTo": [
    "BO-784"
   ],
   "transitions": [
    {
     "to": "BO-784",
     "trigger": "Back to Communications Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Connect communications to reusable content and live products. Maintain approved content blocks for banners, copy, events, tickets, memberships, loyalty, promotions, CTAs and footers. Configure live feeds from events, products, ticket inventory, capacity, pricing, promotions and recommendations. Define filters, sorting, fallback content, refresh interval, expiration and behavior when inventory is unavailable. Track which campaigns and templates use each block before editing or deactivation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 32"
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
       "impliedBy": "createMessageTemplate",
       "label": "Create message template",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createMessageTemplate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The content blocks product list.",
   "error": "Could not load. Names which read failed and leaves the content blocks product untouched.",
   "emptyFirstRun": "No content blocks product yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the content blocks product are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createMessageTemplate",
    "contract": "marketing-crm",
    "purpose": "Content blocks and product feed",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-787",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-787"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-788",
  "name": "Subscriptions & Preferences",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "05",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/subscriptions-preferences-bo-788",
   "component": "apps/venue-management-web/src/routes/engagement-support/SubscriptionsPreferences.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-784"
   ],
   "exitTo": [
    "BO-784"
   ],
   "transitions": [
    {
     "to": "BO-784",
     "trigger": "Back to Communications Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage newsletter subscriptions and messaging eligibility. Configure subscription categories, topics, channels, frequency, consent mapping, suppression and do-not-contact status. Search subscribers and view preferred channels, verification, consent source, status and last change. Support guest self-service and authorized administration while preventing forced marketing opt- in. Synchronize changes immediately to campaign, journey, newsletter and delivery services and audit them. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 32"
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
       "impliedBy": "setMarketingSubscription",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMarketingSubscription"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The subscriptions preferences list.",
   "error": "Could not load. Names which read failed and leaves the subscriptions preferences untouched.",
   "emptyFirstRun": "No subscriptions preferences yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscriptions preferences are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMarketingSubscription",
    "contract": "marketing-crm",
    "purpose": "Subscriptions and preferences",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getMarketingSubscription",
    "contract": "marketing-crm",
    "purpose": "What a guest is subscribed to",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "addSuppression",
    "contract": "marketing-crm",
    "purpose": "Suppress an address from all marketing",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "getMarketingSubscription"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-788",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-788"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-789",
  "name": "Transactional Notification Rules",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "06",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/transactional-notification-rules-bo-789",
   "component": "apps/venue-management-web/src/routes/engagement-support/TransactionalNotificationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-784"
   ],
   "exitTo": [
    "BO-784"
   ],
   "transitions": [
    {
     "to": "BO-784",
     "trigger": "Back to Communications Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Map operational events to the correct notification behavior. Configure rules for purchase, reservation, check-in, membership, loyalty, wallet, refund, cancellation, waitlist and operational events. Select template, channel, recipients, timing, priority, conditions, attachments and personalization mapping. Differentiate mandatory transactional notices from optional marketing and apply the correct consent policy. Test rules with sample events and prevent conflicting or duplicate notifications. Configuration Scope of Work | Version 1.0 32 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 32"
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
       "impliedBy": "listSystemTransactionalTemplate",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setMessageTrigger",
       "label": "Save message trigger",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMessageTrigger"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The transactional notification rules list.",
   "error": "Could not load. Names which read failed and leaves the transactional notification rules untouched.",
   "emptyFirstRun": "No transactional notification rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the transactional notification rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSystemTransactionalTemplate",
    "contract": "marketing-crm",
    "purpose": "Transactional templates",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setMessageTrigger",
    "contract": "marketing-crm",
    "purpose": "Notification rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-789",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-789"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-790",
  "name": "Scheduling, Priority & Approval",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "07",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/scheduling-priority-approval-bo-790",
   "component": "apps/venue-management-web/src/routes/engagement-support/SchedulingPriorityApproval.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-784"
   ],
   "exitTo": [
    "BO-784"
   ],
   "transitions": [
    {
     "to": "BO-784",
     "trigger": "Back to Communications Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control message timing, urgency and governance. Support immediate, scheduled, recurring and event-relative delivery with timezone, windows and blackout periods. Configure Critical, High, Medium and Low priority, queue treatment, escalation and delivery deadline. Route selected templates and schedules through reviewer and approver stages with delegation and comments. Provide a final audience, content, channel, cost and policy pre-flight before activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 33"
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
       "impliedBy": "listRoutingPriorityThrottling",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The scheduling priority approval list.",
   "error": "Could not load. Names which read failed and leaves the scheduling priority approval untouched.",
   "emptyFirstRun": "No scheduling priority approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the scheduling priority approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRoutingPriorityThrottling",
    "contract": "marketing-crm",
    "purpose": "Scheduling, priority and throttling",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-790",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-790"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-791",
  "name": "Delivery, Retry & Failover",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "08",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/delivery-retry-failover-bo-791",
   "component": "apps/venue-management-web/src/routes/engagement-support/DeliveryRetryFailover.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-784"
   ],
   "exitTo": [
    "BO-784"
   ],
   "transitions": [
    {
     "to": "BO-784",
     "trigger": "Back to Communications Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure reliable routing across communication providers and channels. Maintain primary, secondary and tertiary providers per channel, tenant, region and message category. Define retry count, delay, backoff, retryable errors, expiration and dead-letter handling. Configure channel failover order while rechecking consent, content compatibility and urgency. Provide message trace, provider response, failure reason, manual replay controls and audit history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 33"
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
       "impliedBy": "listDeliveryQueueFailure",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "retryMessageDispatch",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "retryMessageDispatch"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The delivery retry failover list.",
   "error": "Could not load. Names which read failed and leaves the delivery retry failover untouched.",
   "emptyFirstRun": "No delivery retry failover yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the delivery retry failover are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDeliveryQueueFailure",
    "contract": "marketing-crm",
    "purpose": "Failures and retries",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "retryMessageDispatch",
    "contract": "marketing-crm",
    "purpose": "Retry",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-791",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-791"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "dispatchId",
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
  "id": "BO-792",
  "name": "Deliverability & Analytics",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "09",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/deliverability-analytics-bo-792",
   "component": "apps/venue-management-web/src/routes/engagement-support/DeliverabilityAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-784"
   ],
   "exitTo": [
    "BO-784"
   ],
   "transitions": [
    {
     "to": "BO-784",
     "trigger": "Back to Communications Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor technical delivery quality and commercial outcomes. Report sender reputation, inbox placement, hard/soft bounce, complaints, blocks, opens, clicks and conversions. Compare providers, domains, channels, templates, languages, brands and regions over time. Trace individual messages from generation to provider response and guest engagement where authorized. Alert on thresholds and attribute revenue using the shared marketing attribution framework. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 33"
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
       "impliedBy": "listProviderHealthUsage",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The deliverability analytics list.",
   "error": "Could not load. Names which read failed and leaves the deliverability analytics untouched.",
   "emptyFirstRun": "No deliverability analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deliverability analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProviderHealthUsage",
    "contract": "marketing-crm",
    "purpose": "Deliverability and cost",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-792",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-792"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-793",
  "name": "AI Content, Translation & Audit",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "6",
   "number": "10",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/ai-content-translation-audit-bo-793",
   "component": "apps/venue-management-web/src/routes/engagement-support/AiContentTranslationAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-784"
   ],
   "exitTo": [
    "BO-784"
   ],
   "transitions": [
    {
     "to": "BO-784",
     "trigger": "Back to Communications Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use governed AI for communication creation and localization. Generate subject lines, titles, summaries and message variants by objective, tone, audience and channel. Translate content using approved languages, terminology glossary, brand rules and protected placeholders. Configuration Scope of Work | Version 1.0 33 Display confidence and changes, require manual review where configured and prevent unsupported claims. Retain prompt/context classification, model/version, output, edits, approver and publication audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 34 Board 7 - Omnichannel Inbox, AI Chatbot & Agent Workspace Figure 7. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 35",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 33"
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
       "impliedBy": "setLocalizationBrandingCustomer",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setLocalizationBrandingCustomer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The content translation audit list.",
   "error": "Could not load. Names which read failed and leaves the content translation audit untouched.",
   "emptyFirstRun": "No content translation audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the content translation audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setLocalizationBrandingCustomer",
    "contract": "marketing-crm",
    "purpose": "Content, translation and branding",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-793",
   "workshopBoard": "wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-793"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "addSuppression": {
  "method": "POST",
  "path": "/consent/suppression-list",
  "contract": "marketing-crm",
  "summary": "Suppress an address",
  "permission": "GUEST_MANAGE",
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
  "responds": "Suppression"
 },
 "createMessageTemplate": {
  "method": "POST",
  "path": "/message-templates",
  "contract": "marketing-crm",
  "summary": "Create a message template",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "MessageTemplate",
  "responds": "MessageTemplate"
 },
 "getMarketingSubscription": {
  "method": "GET",
  "path": "/marketing-subscriptions",
  "contract": "marketing-crm",
  "summary": "What this guest has opted into",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MarketingSubscription"
 },
 "listCommunicationService": {
  "method": "GET",
  "path": "/communication-service",
  "contract": "marketing-crm",
  "summary": "Communication Service Command Center",
  "permission": "MARKETING_VIEW",
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
  "responds": "CommunicationServiceCommandCenterView"
 },
 "listDeliveryQueueFailure": {
  "method": "GET",
  "path": "/delivery-queue-failure",
  "contract": "marketing-crm",
  "summary": "Delivery Queue, Failure & Retry Management",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "sourceModule",
    "in": "query",
    "required": false
   },
   {
    "name": "businessEvent",
    "in": "query",
    "required": false
   },
   {
    "name": "providerId",
    "in": "query",
    "required": false
   },
   {
    "name": "priority",
    "in": "query",
    "required": false
   },
   {
    "name": "failureCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
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
 "listMessageTemplates": {
  "method": "GET",
  "path": "/message-templates",
  "contract": "marketing-crm",
  "summary": "List message templates",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "listProviderHealthUsage": {
  "method": "GET",
  "path": "/provider-health-usage",
  "contract": "marketing-crm",
  "summary": "Provider Health, Usage & Cost Monitoring",
  "permission": "MARKETING_VIEW",
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
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "providerId",
    "in": "query",
    "required": false
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "module",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "messageClass",
    "in": "query",
    "required": false
   },
   {
    "name": "groupBy",
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
  "responds": "ProviderHealthUsageCostMonitoringView"
 },
 "listRoutingPriorityThrottling": {
  "method": "GET",
  "path": "/routing-priority-throttling",
  "contract": "marketing-crm",
  "summary": "Routing, Priority, Throttling & Fallback Rules",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "priorityClass",
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
 "listSystemTransactionalTemplate": {
  "method": "GET",
  "path": "/system-transactional-template",
  "contract": "marketing-crm",
  "summary": "System Transactional Template Registry",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ownership",
    "in": "query",
    "required": false
   },
   {
    "name": "sourceModule",
    "in": "query",
    "required": false
   },
   {
    "name": "businessEvent",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "language",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "retryMessageDispatch": {
  "method": "POST",
  "path": "/message-dispatches/{dispatchId}/retry",
  "contract": "marketing-crm",
  "summary": "Send it again, or by another channel",
  "permission": "MARKETING_SEND",
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
  "responds": "MessageDispatch"
 },
 "setLocalizationBrandingCustomer": {
  "method": "PUT",
  "path": "/localization-branding-customer",
  "contract": "marketing-crm",
  "summary": "Set a waiver version's languages, branding and channels",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "LocalizationBrandingCustomerExperienceConfigurationInput",
  "responds": "LocalizationBrandingCustomerExperienceConfigurationView"
 },
 "setMarketingSubscription": {
  "method": "PUT",
  "path": "/marketing-subscriptions",
  "contract": "marketing-crm",
  "summary": "Subscribe or unsubscribe",
  "permission": "MARKETING_VIEW",
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
  "requestBody": "MarketingSubscription",
  "responds": "MarketingSubscription"
 },
 "setMessageTrigger": {
  "method": "POST",
  "path": "/message-triggers",
  "contract": "marketing-crm",
  "summary": "Fire a message from a platform event",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "MessageTrigger",
  "responds": "MessageTrigger"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CommunicationServiceCommandCenterView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)",
  "description": "Platform KPIs and breakdowns for the communication service over the requested window. Counts are messages (one dispatch = one message on one channel), not recipients.\n",
  "required": [
   "windowFrom",
   "windowTo",
   "messagesProcessed",
   "byChannel",
   "byModule"
  ],
  "properties": {
   "windowFrom": {
    "type": "string",
    "format": "date-time"
   },
   "windowTo": {
    "type": "string",
    "format": "date-time"
   },
   "messagesProcessed": {
    "type": "integer",
    "minimum": 0,
    "description": "Messages accepted by the service in the window (the pack's \"Messages Processed Today\")."
   },
   "delivered": {
    "type": "integer",
    "minimum": 0
   },
   "failed": {
    "type": "integer",
    "minimum": 0
   },
   "pending": {
    "type": "integer",
    "minimum": 0
   },
   "retrying": {
    "type": "integer",
    "minimum": 0
   },
   "averageDeliverySeconds": {
    "type": "number",
    "minimum": 0,
    "description": "Mean time from acceptance to provider-confirmed delivery, in (fractional) seconds."
   },
   "providerAvailabilityRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Share of the window the active providers were reachable, weighted by volume."
   },
   "byChannel": {
    "type": "array",
    "description": "Sent volume and health per channel, one row per provider on it (the pack's channel tiles and Channel Health table).",
    "items": {
     "type": "object",
     "required": [
      "channel",
      "sent"
     ],
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "providerName": {
       "type": "string"
      },
      "sent": {
       "type": "integer",
       "minimum": 0
      },
      "successRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "averageLatencySeconds": {
       "type": "number",
       "minimum": 0
      },
      "health": {
       "type": "string",
       "enum": [
        "healthy",
        "warning",
        "critical"
       ]
      }
     }
    }
   },
   "byModule": {
    "type": "array",
    "description": "Volume originating from each TICVAI module.",
    "items": {
     "type": "object",
     "required": [
      "module",
      "volume"
     ],
     "properties": {
      "module": {
       "type": "string",
       "enum": [
        "crm",
        "ticketing",
        "membership",
        "waiver",
        "groupSales",
        "customerService",
        "finance",
        "wallet",
        "resourceManagement",
        "accessControl",
        "other"
       ]
      },
      "volume": {
       "type": "integer",
       "minimum": 0
      },
      "successRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "averageLatencySeconds": {
       "type": "number",
       "minimum": 0
      },
      "health": {
       "type": "string",
       "enum": [
        "healthy",
        "warning",
        "critical"
       ]
      }
     }
    }
   },
   "alerts": {
    "type": "array",
    "description": "Live operational alerts (failure-rate spikes, queued backlogs, providers near their rate limit).",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "severity",
      "message",
      "raisedAt"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "failureRateSpike",
        "queueBacklog",
        "rateLimitApproaching",
        "providerDegraded",
        "other"
       ]
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
       "type": "string"
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "raisedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "aiHealthSummary": {
    "type": "string",
    "description": "AI-written plain-language summary of platform health; absent when AI processing is off for the tenant."
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
 "LocalizationBrandingCustomerExperienceConfigurationInput": {
  "description": "The request body of `setLocalizationBrandingCustomer`, the record itself; read-only properties are ignored.",
  "allOf": [
   {
    "$ref": "#/components/schemas/LocalizationBrandingCustomerExperienceConfigurationView"
   }
  ]
 },
 "LocalizationBrandingCustomerExperienceConfigurationView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_localisation",
  "description": "Languages, branding and channels of one waiver version (pack 11.1.9), keyed on `formId` + `formVersion`.",
  "required": [
   "formId",
   "formVersion",
   "sourceLanguage",
   "languages"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "formVersion": {
    "type": "integer",
    "minimum": 1
   },
   "sourceLanguage": {
    "type": "string",
    "maxLength": 10,
    "description": "The language the legal text is written and reviewed in."
   },
   "languages": {
    "type": "array",
    "minItems": 1,
    "description": "Every language the version is offered in, the source language included. Arabic renders right to left.",
    "items": {
     "type": "object",
     "required": [
      "language",
      "required",
      "translationStatus",
      "approvalStatus"
     ],
     "properties": {
      "language": {
       "type": "string",
       "maxLength": 10
      },
      "required": {
       "type": "boolean",
       "description": "Publication waits for this language's approval."
      },
      "translationStatus": {
       "type": "string",
       "enum": [
        "notStarted",
        "aiDrafted",
        "inTranslation",
        "inReview",
        "complete"
       ]
      },
      "translatorUserId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "reviewerUserId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "approvalStatus": {
       "type": "string",
       "enum": [
        "pending",
        "approved",
        "rejected"
       ]
      },
      "lastUpdated": {
       "type": "string",
       "format": "date-time",
       "readOnly": true
      }
     }
    }
   },
   "branding": {
    "type": "object",
    "properties": {
     "brandLogoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "venueLogoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "themeId": {
      "type": "string",
      "nullable": true,
      "description": "The white-label theme it takes colours and typography from."
     },
     "header": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "footer": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "customerInstructions": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "confirmationMessage": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "supportEmail": {
      "type": "string",
      "format": "email",
      "nullable": true
     },
     "supportPhone": {
      "type": "string",
      "maxLength": 30,
      "nullable": true
     }
    }
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2cWeb",
      "mobileApp",
      "emailLink",
      "qrLink",
      "kiosk",
      "posFrontDesk",
      "groupPortal"
     ]
    },
    "description": "Where the waiver is offered; every channel renders the same version and rules."
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
 "MarketingSubscription": {
  "type": "object",
  "x-ticvai-persistence": "marketing.subscription",
  "x-ticvai-retired-columns": [
   "guest_id",
   "subscribed"
  ],
  "description": "**Drafted 4 September.** What a guest asked to receive. **Deliberately separate from `marketing.consent`** - consent is what the law allows, a subscription is what the person wants, and a system that stores one and reports the other is the reason unsubscribe links stop working.",
  "required": [
   "id",
   "subjectId",
   "channel",
   "listName",
   "isSubscribed"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The guest — from the guest session, or from `unsubscribeToken` when there is no session."
   },
   "channel": {
    "type": "string",
    "enum": [
     "email",
     "sms",
     "push"
    ]
   },
   "listName": {
    "type": "string"
   },
   "isSubscribed": {
    "type": "boolean"
   },
   "source": {
    "type": "string",
    "description": "Where the opt-in happened, because a regulator asks."
   },
   "unsubscribeToken": {
    "writeOnly": true,
    "type": "string",
    "description": "**Unsubscribe must work without a login.** The link in a message carries the token and `setMarketingSubscription` accepts it in place of a session. **Write-only: never returned**, so a `MARKETING_VIEW` holder reading subscriptions cannot act as the guest."
   },
   "updatedAt": {
    "readOnly": true,
    "type": "string",
    "format": "date-time"
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
 "MessageDispatch": {
  "x-ticvai-persistence": "marketing.message_dispatch",
  "type": "object",
  "required": [
   "id",
   "subjectId",
   "channel",
   "status",
   "queuedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "campaignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "messageTriggerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `MessageTrigger` that fired it, and through its `event` the `BusinessEvent` and source module; null for a campaign or a direct send. Attempts are in `MessageDispatchAttempt`. (decided 29 September, data model for the agreed operations)"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "sent",
     "delivered",
     "opened",
     "clicked",
     "bounced",
     "failed",
     "suppressed"
    ]
   },
   "failureReason": {
    "type": "string",
    "nullable": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true
   },
   "queuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "deliveredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isTest": {
    "type": "boolean",
    "default": false,
    "description": "A `testSendCampaign` message. Excluded from `CampaignPerformance` and `Campaign.sentCount`."
   },
   "openedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "From the provider's engagement events. `CampaignPerformance.opened` counts these."
   },
   "clickedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "complainedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "unsubscribedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MessageTemplate": {
  "x-ticvai-persistence": "marketing.message_template",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "channel",
   "bodies"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "subjects": {
    "type": "object",
    "description": "Per language. Email only.",
    "additionalProperties": {
     "type": "string"
    }
   },
   "bodies": {
    "type": "object",
    "description": "Per language, keyed by ISO 639-1 code.",
    "additionalProperties": {
     "type": "string"
    }
   },
   "mergeFields": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "missingLanguages": {
    "type": "array",
    "readOnly": true,
    "description": "Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect.\n",
    "items": {
     "type": "string"
    }
   },
   "providerTemplateId": {
    "type": "string",
    "nullable": true,
    "description": "Required for WhatsApp, where templates are pre-approved by the provider."
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The brand whose identity the template carries; null for the tenant default."
   },
   "ownership": {
    "type": "string",
    "enum": [
     "platform",
     "crm"
    ],
    "default": "crm",
    "description": "`platform` = a transactional template owned by the communication service; `crm` = a marketing template owned by CRM (`listSystemTransactionalTemplate`). Content by language and version is in `MessageTemplateVersion`. (decided 29 September, data model for the agreed operations)"
   }
  }
 },
 "MessageTrigger": {
  "type": "object",
  "x-ticvai-persistence": "marketing.message_trigger",
  "description": "**What fires a message.** Before, during and after a visit are one mechanism with a different sign on the offset.\n",
  "required": [
   "id",
   "event",
   "templateId",
   "isActive"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "event": {
    "type": "string",
    "description": "The platform event that fires it — `order.completed`, `access.validated`, `queue.turnApproaching`. **Named from the event catalogue** (`BusinessEvent.eventType`), so a trigger cannot bind to something nothing publishes. Its conditions are `MessageTriggerCondition` rows.\n"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "offsetMinutes": {
    "type": "integer",
    "default": 0,
    "description": "Negative fires before the anchor, positive after. **A reminder the day before a visit is -1440 against the performance**, not a separate concept.\n"
   },
   "anchor": {
    "type": "string",
    "enum": [
     "eventTime",
     "performanceStart",
     "visitEnd"
    ],
    "default": "eventTime"
   },
   "priority": {
    "type": "string",
    "enum": [
     "operational",
     "transactional",
     "marketing"
    ],
    "default": "transactional",
    "description": "**A queue-turn alert and a monthly newsletter are not the same urgency and were the same dispatch.** `operational` bypasses batching and quiet hours; `marketing` never does.\n"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
 "ProviderHealthUsageCostMonitoringView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)",
  "description": "Provider reliability, usage and cost for the window and filters.",
  "required": [
   "windowFrom",
   "windowTo",
   "volume",
   "providers"
  ],
  "properties": {
   "windowFrom": {
    "type": "string",
    "format": "date-time"
   },
   "windowTo": {
    "type": "string",
    "format": "date-time"
   },
   "volume": {
    "type": "integer",
    "minimum": 0
   },
   "successRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "failureRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "averageDeliverySeconds": {
    "type": "number",
    "minimum": 0
   },
   "averageApiLatencySeconds": {
    "type": "number",
    "minimum": 0
   },
   "availabilityRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "retries": {
    "type": "integer",
    "minimum": 0
   },
   "fallbackCount": {
    "type": "integer",
    "minimum": 0,
    "description": "Messages delivered through a fallback provider or channel."
   },
   "cost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "costPerMessage": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providers": {
    "type": "array",
    "description": "Provider comparison.",
    "items": {
     "type": "object",
     "required": [
      "providerId",
      "channel",
      "volume"
     ],
     "properties": {
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "providerName": {
       "type": "string"
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "volume": {
       "type": "integer",
       "minimum": 0
      },
      "successRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "averageDeliverySeconds": {
       "type": "number",
       "minimum": 0
      },
      "costPerThousand": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "health": {
       "type": "string",
       "enum": [
        "healthy",
        "warning",
        "critical"
       ]
      }
     }
    }
   },
   "breakdown": {
    "type": "array",
    "description": "Usage and cost per value of the groupBy dimension.",
    "items": {
     "type": "object",
     "required": [
      "key",
      "volume"
     ],
     "properties": {
      "key": {
       "type": "string",
       "description": "The dimension value's id or code."
      },
      "label": {
       "type": "string"
      },
      "volume": {
       "type": "integer",
       "minimum": 0
      },
      "cost": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "alerts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "message",
      "raisedAt"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "budgetThreshold",
        "successRateBelowTarget",
        "latencyAboveTarget",
        "slaBreach"
       ]
      },
      "message": {
       "type": "string"
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "raisedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "slaTargets": {
    "type": "array",
    "description": "Contractual provider targets, only where configured.",
    "items": {
     "type": "object",
     "required": [
      "providerId",
      "metric",
      "target"
     ],
     "properties": {
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "metric": {
       "type": "string",
       "enum": [
        "successRate",
        "availabilityRate",
        "averageDeliverySeconds"
       ]
      },
      "target": {
       "type": "number"
      },
      "observed": {
       "type": "number"
      },
      "met": {
       "type": "boolean"
      }
     }
    }
   },
   "aiRecommendations": {
    "type": "array",
    "description": "Advisory provider changes on cost/performance trade-offs.",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "Suppression": {
  "x-ticvai-persistence": "marketing.suppression",
  "type": "object",
  "required": [
   "channel",
   "address",
   "reason",
   "suppressedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "address": {
    "type": "string"
   },
   "reason": {
    "type": "string"
   },
   "suppressedAt": {
    "type": "string",
    "format": "date-time"
   },
   "suppressedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 }
}
```
