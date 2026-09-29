# WS146 — Marketing CRM Configuration Reference v1.0 board 12

**10 screens · 11 operations · 9 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-844` | Waiver Command Center | listDetail | 1 | 0 | — |
| `BO-845` | Waiver Template Builder | listDetail | 1 | 0 | — |
| `BO-846` | Assignment Rules | listDetail | 2 | 0 | — |
| `BO-847` | Version, Expiry & Renewal | listDetail | 1 | 0 | — |
| `BO-848` | Signature Experience Setup | listDetail | 1 | 0 | — |
| `BO-849` | Guardian & Group Signing | listDetail | 1 | 0 | — |
| `BO-850` | Pre-Arrival Completion | listDetail | 1 | 0 | — |
| `BO-851` | Verification & Access Control | listDetail | 1 | 0 | — |
| `BO-852` | Documents, Search & Retention | listDetail | 2 | 0 | — |
| `BO-853` | Legal Evidence & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-844, BO-845, BO-846, BO-847, BO-848, BO-849, BO-850, BO-851, BO-852, BO-853 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-844",
  "name": "Waiver Command Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "01",
   "page": 58
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/waiver-command-center-bo-844",
   "component": "apps/venue-management-web/src/routes/engagement-support/WaiverCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-845",
    "BO-846",
    "BO-847",
    "BO-848",
    "BO-849",
    "BO-850",
    "BO-851",
    "BO-852",
    "BO-853"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-845",
     "trigger": "Waiver Template Builder",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-846",
     "trigger": "Assignment Rules",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-847",
     "trigger": "Version, Expiry & Renewal",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-848",
     "trigger": "Signature Experience Setup",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-849",
     "trigger": "Guardian & Group Signing",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-850",
     "trigger": "Pre-Arrival Completion",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-851",
     "trigger": "Verification & Access Control",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-852",
     "trigger": "Documents, Search & Retention",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-853",
     "trigger": "Legal Evidence & Audit",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor waiver completion, expiry and operational access risk. Show required, completed, pending, expired and expiring waivers, blocked entries and guardian signatures. Analyze completion by venue, activity, event, product, channel, guest type and arrival date. Surface missing signatures, failed verification, version changes requiring re-sign and access-control exceptions. Provide operational drill-down and alerts without exposing document content to unauthorized roles. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 58"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 58"
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
       "impliedBy": "listWaiver",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver list.",
   "error": "Could not load. Names which read failed and leaves the waiver untouched.",
   "emptyFirstRun": "No waiver yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the waiver are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiver",
    "contract": "marketing-crm",
    "purpose": "Waiver Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-844",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-844"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 58. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-845",
  "name": "Waiver Template Builder",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "02",
   "page": 58
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/waiver-template-builder-bo-845",
   "component": "apps/venue-management-web/src/routes/engagement-support/WaiverTemplateBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-844"
   ],
   "exitTo": [
    "BO-844"
   ],
   "transitions": [
    {
     "to": "BO-844",
     "trigger": "Back to Waiver Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create legal waiver and declaration templates without development. Support liability release, general consent, parental consent, medical declaration, risk acknowledgement and activity agreement types. Provide sections, clauses, variables, conditional content, initials, attachments and signature blocks. Manage multilingual content, legal owner, jurisdiction, risk category, approval and preview. Version every legal change and prohibit publishing until required legal and business approvals complete. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**Waiver Template Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 58"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 58"
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
       "impliedBy": "listWaiver",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver template list.",
   "error": "Could not load. Names which read failed and leaves the waiver template untouched.",
   "emptyFirstRun": "No waiver template yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the waiver template are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiver",
    "contract": "marketing-crm",
    "purpose": "Waivers and their state",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-845",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-845"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 58. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-846",
  "name": "Assignment Rules",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "03",
   "page": 58
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/assignment-rules-bo-846",
   "component": "apps/venue-management-web/src/routes/engagement-support/AssignmentRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-844"
   ],
   "exitTo": [
    "BO-844"
   ],
   "transitions": [
    {
     "to": "BO-844",
     "trigger": "Back to Waiver Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine which waiver or form each guest must complete. Build rules using product, attraction, event, activity, venue, age, membership, risk category and jurisdiction. Configuration Scope of Work | Version 1.0 58 Assign one or multiple required documents with priority, effective dates and exception handling. Detect conflicting, missing or circular rules and simulate results for sample guests/bookings. Version, approve and audit rules and retain the rule/version used for each assignment. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 58"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 58"
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
       "impliedBy": "listWaiverTemplateMaster",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setDigitalWaiverForm",
       "label": "Save digital waiver form",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setDigitalWaiverForm"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rules list.",
   "error": "Could not load. Names which read failed and leaves the rules untouched.",
   "emptyFirstRun": "No rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiverTemplateMaster",
    "contract": "marketing-crm",
    "purpose": "Templates",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setDigitalWaiverForm",
    "contract": "marketing-crm",
    "purpose": "Build one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-846",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-846"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 58. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-847",
  "name": "Version, Expiry & Renewal",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "04",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/version-expiry-renewal-bo-847",
   "component": "apps/venue-management-web/src/routes/engagement-support/VersionExpiryRenewal.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-844"
   ],
   "exitTo": [
    "BO-844"
   ],
   "transitions": [
    {
     "to": "BO-844",
     "trigger": "Back to Waiver Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control legal-document lifecycle and re-sign requirements. Maintain version history, effective dates, changed clauses, approver, status and expiry period. Configure whether a change or elapsed period requires all, selected or future guests to sign again. Define renewal reminders, grace period, replacement behavior and treatment of active bookings. Preserve every signed version and prevent current templates from altering historical evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 59"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 59"
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
       "impliedBy": "listWaiverTriggerEligibility",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The version expiry renewal list.",
   "error": "Could not load. Names which read failed and leaves the version expiry renewal untouched.",
   "emptyFirstRun": "No version expiry renewal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the version expiry renewal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiverTriggerEligibility",
    "contract": "marketing-crm",
    "purpose": "Assignment rules",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-847",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-847"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 59. 0 of 0 labels bound to a contract property; 0 of 7 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-848",
  "name": "Signature Experience Setup",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "05",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/signature-experience-setup-bo-848",
   "component": "apps/venue-management-web/src/routes/engagement-support/SignatureExperienceSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-844"
   ],
   "exitTo": [
    "BO-844"
   ],
   "transitions": [
    {
     "to": "BO-844",
     "trigger": "Back to Waiver Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure secure signing across supported guest touchpoints. Support website, mobile app, kiosk, tablet, POS and dedicated waiver-station channels. Configure identity verification, signature, initials, witness, review-before-submit and completion receipt. Define accessible, multilingual flow, timeout, session recovery, device controls and offline behavior. Test the end-to-end experience and map every captured element to the evidence record. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**Signature Experience Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 59"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 59"
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
       "impliedBy": "listVersioningEffectiveDate",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The signature experience list.",
   "error": "Could not load. Names which read failed and leaves the signature experience untouched.",
   "emptyFirstRun": "No signature experience yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the signature experience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVersioningEffectiveDate",
    "contract": "marketing-crm",
    "purpose": "Version, expiry and renewal",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-848",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-848"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 59. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-849",
  "name": "Guardian & Group Signing",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "06",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/guardian-group-signing-bo-849",
   "component": "apps/venue-management-web/src/routes/engagement-support/GuardianGroupSigning.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-844"
   ],
   "exitTo": [
    "BO-844"
   ],
   "transitions": [
    {
     "to": "BO-844",
     "trigger": "Back to Waiver Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage authority and multi-participant signing for minors and groups. Use Customer Master family/guardian relationships and record the authority basis for each dependant. Support one authorized signer for multiple family members, students or group participants where permitted. Configure minimum self-sign age, one/both guardian requirement, partial group signing and exceptions. Show roster status and require individual signatures for documents or participants that cannot be delegated. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 59"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 59"
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
       "impliedBy": "setSignatorySignatureGuardian",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSignatorySignatureGuardian"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guardian group signing list.",
   "error": "Could not load. Names which read failed and leaves the guardian group signing untouched.",
   "emptyFirstRun": "No guardian group signing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guardian group signing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSignatorySignatureGuardian",
    "contract": "marketing-crm",
    "purpose": "Signature experience",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-849",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-849"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 59. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-850",
  "name": "Pre-Arrival Completion",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "07",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/pre-arrival-completion-bo-850",
   "component": "apps/venue-management-web/src/routes/engagement-support/PreArrivalCompletion.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-844"
   ],
   "exitTo": [
    "BO-844"
   ],
   "transitions": [
    {
     "to": "BO-844",
     "trigger": "Back to Waiver Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Collect required waivers before the guest reaches the venue. Link the request to booking, ticket, event, activity, participants and scheduled arrival. Configuration Scope of Work | Version 1.0 59 Send secure email, SMS or WhatsApp link/QR in the guest's language with a completion deadline. Configure reminder schedule, resend, authentication, expiry and status synchronization. Show completed, pending and not-started participants and stop reminders immediately after valid completion. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 59"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 59"
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
       "impliedBy": "listMinorGuardianGroup",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pre-arrival completion list.",
   "error": "Could not load. Names which read failed and leaves the pre-arrival completion untouched.",
   "emptyFirstRun": "No pre-arrival completion yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pre-arrival completion are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMinorGuardianGroup",
    "contract": "marketing-crm",
    "purpose": "Guardian and group signing",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-850",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-850"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 59. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-851",
  "name": "Verification & Access Control",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "08",
   "page": 60
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/verification-access-control-bo-851",
   "component": "apps/venue-management-web/src/routes/engagement-support/VerificationAccessControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-844"
   ],
   "exitTo": [
    "BO-844"
   ],
   "transitions": [
    {
     "to": "BO-844",
     "trigger": "Back to Waiver Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Enforce waiver requirements during check-in and access validation. Return real-time valid, missing, expired or wrong-version status during ticket scan or check-in. Show required documents and participant while minimizing sensitive content at the gate. Configure admit/block outcomes, supervisor override, reason, approval and offline cache/freshness. Record scan, decision, waiver evidence reference, device, operator, override and final access outcome. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 60"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 60"
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
       "impliedBy": "listParticipantWaiverStatus",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The verification access list.",
   "error": "Could not load. Names which read failed and leaves the verification access untouched.",
   "emptyFirstRun": "No verification access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the verification access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listParticipantWaiverStatus",
    "contract": "marketing-crm",
    "purpose": "Pre-arrival completion",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-851",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-851"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 60. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-852",
  "name": "Documents, Search & Retention",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "09",
   "page": 60
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/documents-search-retention-bo-852",
   "component": "apps/venue-management-web/src/routes/engagement-support/DocumentsSearchRetention.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-844"
   ],
   "exitTo": [
    "BO-844"
   ],
   "transitions": [
    {
     "to": "BO-844",
     "trigger": "Back to Waiver Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Securely store and retrieve signed waiver evidence. Search by guest, guardian, participant, booking, ticket, activity, event, date, version and status. Store signed PDF/evidence package, metadata, relationships, status and authorized view/download actions. Apply encryption, RBAC/PBAC, retention, legal hold, archive and deletion/anonymization policies. Track every access, download, policy action and downstream reference and prevent silent alteration. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 60"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 60"
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
       "impliedBy": "setWaiverVerificationValidation",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getWaiverStatus",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setWaiverVerificationValidation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The documents search retention list.",
   "error": "Could not load. Names which read failed and leaves the documents search retention untouched.",
   "emptyFirstRun": "No documents search retention yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the documents search retention are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWaiverVerificationValidation",
    "contract": "marketing-crm",
    "purpose": "Verification and access control",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getWaiverStatus",
    "contract": "marketing-crm",
    "purpose": "Whether this guest may enter",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-852",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-852"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 60. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "subjectId",
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
  "id": "BO-853",
  "name": "Legal Evidence & Audit",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "12",
   "number": "10",
   "page": 60
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/legal-evidence-audit-bo-853",
   "component": "apps/venue-management-web/src/routes/engagement-support/LegalEvidenceAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-844"
   ],
   "exitTo": [
    "BO-844"
   ],
   "transitions": [
    {
     "to": "BO-844",
     "trigger": "Back to Waiver Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a defensible record of signing and subsequent operational use. Record signer and participant identity, authority, timestamp, timezone, IP/device, channel and verification method. Store consent/template version, content hash, signature/initials, witness, attachments and completion receipt. Include access-control decisions, overrides, renewals, revocations and related communications in the timeline. Export a controlled evidence bundle with integrity validation and full audit history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 60",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 60"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 60"
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
       "impliedBy": "listComplianceEvidenceWaiver",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The legal evidence audit list.",
   "error": "Could not load. Names which read failed and leaves the legal evidence audit untouched.",
   "emptyFirstRun": "No legal evidence audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the legal evidence audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listComplianceEvidenceWaiver",
    "contract": "marketing-crm",
    "purpose": "Documents, search and retention",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-853",
   "workshopBoard": "wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-853"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 60. 0 of 0 labels bound to a contract property; 0 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getWaiverStatus": {
  "method": "GET",
  "path": "/guests/{subjectId}/waiver-status",
  "contract": "marketing-crm",
  "summary": "Whether this guest may be issued a ticket that requires a waiver",
  "permission": "GUEST_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "listComplianceEvidenceWaiver": {
  "method": "GET",
  "path": "/compliance-evidence-waiver",
  "contract": "marketing-crm",
  "summary": "Compliance Evidence, Audit & Waiver Repository",
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "participantSubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "signatorySubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": false
   },
   {
    "name": "orderId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "formVersion",
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
 "listMinorGuardianGroup": {
  "method": "GET",
  "path": "/minor-guardian-group",
  "contract": "marketing-crm",
  "summary": "Minor, Guardian & Group Consent Management",
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "groupBookingId",
    "in": "query",
    "required": false
   },
   {
    "name": "guardianSubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "orderId",
    "in": "query",
    "required": false
   },
   {
    "name": "performanceId",
    "in": "query",
    "required": false
   },
   {
    "name": "consentStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "visitFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "visitTo",
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
 "listParticipantWaiverStatus": {
  "method": "GET",
  "path": "/participant-waiver-statu",
  "contract": "marketing-crm",
  "summary": "Participant Waiver Status & Tracking",
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "q",
    "in": "query",
    "required": false
   },
   {
    "name": "participantSubjectId",
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
    "name": "groupBookingId",
    "in": "query",
    "required": false
   },
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "performanceId",
    "in": "query",
    "required": false
   },
   {
    "name": "visitFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "visitTo",
    "in": "query",
    "required": false
   },
   {
    "name": "completionStatus",
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
 "listVersioningEffectiveDate": {
  "method": "GET",
  "path": "/versioning-effective-date",
  "contract": "marketing-crm",
  "summary": "Versioning, Effective Dates & Legal Change Control",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "compareWith",
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
 "listWaiver": {
  "method": "GET",
  "path": "/waiver",
  "contract": "marketing-crm",
  "summary": "Waiver Operations Command Center",
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
    "name": "formId",
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
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "participantType",
    "in": "query",
    "required": false
   },
   {
    "name": "bookingChannel",
    "in": "query",
    "required": false
   },
   {
    "name": "breakdownBy",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WaiverOperationsCommandCenterView"
 },
 "listWaiverTemplateMaster": {
  "method": "GET",
  "path": "/waiver-template-master",
  "contract": "marketing-crm",
  "summary": "Waiver Template Library & Master Setup",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "waiverType",
    "in": "query",
    "required": false
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "isMasterTemplate",
    "in": "query",
    "required": false
   },
   {
    "name": "q",
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
 "listWaiverTriggerEligibility": {
  "method": "GET",
  "path": "/waiver-trigger-eligibility",
  "contract": "marketing-crm",
  "summary": "Waiver Trigger, Eligibility & Completion Rules",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "triggerPoint",
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
 "setDigitalWaiverForm": {
  "method": "PUT",
  "path": "/digital-waiver-form",
  "contract": "marketing-crm",
  "summary": "Save the layout of a draft waiver version",
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
  "requestBody": "DigitalWaiverFormBuilderInput",
  "responds": "DigitalWaiverFormBuilderView"
 },
 "setSignatorySignatureGuardian": {
  "method": "PUT",
  "path": "/signatory-signature-guardian",
  "contract": "marketing-crm",
  "summary": "Set who must sign a draft waiver version, and how",
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
  "requestBody": "SignatorySignatureGuardianRuleConfigurationInput",
  "responds": "SignatorySignatureGuardianRuleConfigurationView"
 },
 "setWaiverVerificationValidation": {
  "method": "PUT",
  "path": "/waiver-verification-validation",
  "contract": "marketing-crm",
  "summary": "Record a reviewer's verification decision on a waiver submission",
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
  "requestBody": "WaiverVerificationValidationWorkspaceInput",
  "responds": "WaiverVerificationValidationWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "DigitalWaiverFormBuilderInput": {
  "description": "The request body of `setDigitalWaiverForm`, the layout record itself; read-only properties are ignored.",
  "allOf": [
   {
    "$ref": "#/components/schemas/DigitalWaiverFormBuilderView"
   }
  ]
 },
 "DigitalWaiverFormBuilderView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_form_layout",
  "description": "The layout of one waiver version (pack 11.1.3), keyed on `formId` + `formVersion`. Immutable once the version is published, like the version itself.",
  "required": [
   "formId",
   "formVersion",
   "sections"
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
   "sections": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "sectionKey",
      "kind",
      "blocks"
     ],
     "properties": {
      "sectionKey": {
       "type": "string",
       "maxLength": 60
      },
      "kind": {
       "type": "string",
       "enum": [
        "header",
        "participantInformation",
        "waiverTerms",
        "safetyAcknowledgements",
        "questions",
        "consent",
        "signature",
        "custom"
       ]
      },
      "title": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "numbered": {
       "type": "boolean",
       "default": false
      },
      "mandatoryReading": {
       "type": "boolean",
       "default": false,
       "description": "The signatory must tick \"I have read and understood this section\" before continuing."
      },
      "acknowledgementText": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "showWhen": {
       "type": "object",
       "nullable": true,
       "description": "Shown only when the condition holds, e.g. `isMinor` equals `true` shows the guardian section.",
       "required": [
        "subject",
        "operator"
       ],
       "properties": {
        "subject": {
         "type": "string",
         "maxLength": 60,
         "description": "A field key of this version, or `isMinor` (resolved from the waiver's guardian threshold)."
        },
        "operator": {
         "type": "string",
         "enum": [
          "equals",
          "notEquals",
          "in",
          "lessThan",
          "greaterThan",
          "isAnswered"
         ]
        },
        "value": {
         "type": "string",
         "maxLength": 200,
         "nullable": true
        }
       }
      },
      "blocks": {
       "type": "array",
       "items": {
        "type": "object",
        "required": [
         "blockKey",
         "kind"
        ],
        "properties": {
         "blockKey": {
          "type": "string",
          "maxLength": 60
         },
         "kind": {
          "type": "string",
          "enum": [
           "heading",
           "paragraph",
           "legalText",
           "instructions",
           "imageLogo",
           "divider",
           "informationBox",
           "checkbox",
           "acknowledgement",
           "question",
           "signature",
           "initials",
           "date",
           "customerDetails",
           "guardianDetails"
          ]
         },
         "content": {
          "$ref": "#/components/schemas/LocalisedText"
         },
         "assetId": {
          "type": "string",
          "format": "uuid",
          "nullable": true,
          "description": "The image for an `imageLogo` block."
         },
         "fieldKey": {
          "type": "string",
          "maxLength": 60,
          "nullable": true,
          "description": "The `FormField.key` an input block collects; required for input kinds."
         },
         "mandatoryNotice": {
          "type": "boolean",
          "default": false,
          "description": "Rendered as a notice that cannot be collapsed."
         }
        }
       }
      }
     }
    }
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "draft",
     "published",
     "superseded",
     "retired"
    ],
    "description": "`FormDefinition.status` of this version."
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
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
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
 "SignatorySignatureGuardianRuleConfigurationInput": {
  "description": "The request body of `setSignatorySignatureGuardian`, the rule record itself; read-only properties are ignored.",
  "allOf": [
   {
    "$ref": "#/components/schemas/SignatorySignatureGuardianRuleConfigurationView"
   }
  ]
 },
 "SignatorySignatureGuardianRuleConfigurationView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_signatory_rule",
  "description": "The signatory rules of one waiver version (pack 11.1.5), keyed on `formId` + `formVersion`; immutable once the version is published.",
  "required": [
   "formId",
   "formVersion",
   "primarySignatory",
   "acceptanceMethod",
   "requiresGuardianForMinors"
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
   "primarySignatory": {
    "type": "string",
    "enum": [
     "ticketHolder",
     "purchaser",
     "participant",
     "parent",
     "legalGuardian",
     "groupLeader",
     "corporateRepresentative",
     "member",
     "rentalCustomer",
     "otherAuthorizedSignatory"
    ]
   },
   "allowedSignatories": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "ticketHolder",
      "purchaser",
      "participant",
      "parent",
      "legalGuardian",
      "groupLeader",
      "corporateRepresentative",
      "member",
      "rentalCustomer",
      "otherAuthorizedSignatory"
     ]
    },
    "description": "Who else may sign in the primary signatory's place."
   },
   "coSignature": {
    "type": "string",
    "nullable": true,
    "enum": [
     "participantAndGuardian",
     "customerAndAuthorizedRepresentative"
    ],
    "description": "Set when two people must both sign."
   },
   "signatureRequired": {
    "type": "boolean",
    "default": true
   },
   "initialsRequired": {
    "type": "boolean",
    "default": false
   },
   "acceptanceMethod": {
    "type": "string",
    "enum": [
     "drawnSignature",
     "typedName",
     "checkbox"
    ],
    "description": "Kept equal to `FormDefinition.signatureKind` (drawn, typed, checkbox)."
   },
   "captureRelationship": {
    "type": "boolean",
    "default": true,
    "description": "Whoever signs for someone else states their relationship."
   },
   "identityVerification": {
    "type": "string",
    "enum": [
     "none",
     "signedInAccount",
     "oneTimeCode",
     "idDocumentCheck"
    ],
    "default": "none"
   },
   "requiresGuardianForMinors": {
    "type": "boolean",
    "description": "Written to `FormDefinition.requiresGuardianForMinors`."
   },
   "guardianThresholdAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 25,
    "nullable": true,
    "description": "A participant under this age needs a guardian. Written to `FormDefinition.minimumAge`. No default."
   },
   "guardianThresholdByCountry": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "country",
      "age"
     ],
     "properties": {
      "country": {
       "type": "string",
       "pattern": "^[A-Z]{2}$"
      },
      "age": {
       "type": "integer",
       "minimum": 1,
       "maximum": 25
      }
     }
    },
    "description": "Per-country thresholds that override `guardianThresholdAge`."
   },
   "guardianSignsForEachMinor": {
    "type": "boolean",
    "default": true,
    "description": "One guardian signature per minor, never one for the family."
   },
   "groupSigningModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "eachParticipantIndividually",
      "guardianForEachMinor",
      "groupLeaderForGroup",
      "organisationRepresentativeDeclaration"
     ]
    },
    "description": "The modes a group booking may use. Empty means each participant signs individually."
   },
   "recordedEvidence": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "string",
     "enum": [
      "timestamp",
      "waiverVersion",
      "signatory",
      "authenticationMethod",
      "transactionReference",
      "customerReference",
      "documentHash",
      "deviceInfo",
      "consentEvidence"
     ]
    },
    "description": "Always all of them; listed so the reviewer sees what is kept."
   },
   "legalApprovedBy": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "`FormDefinition.legalReviewedBy`, set at the legal/compliance step of `approveWaiverTesting`."
   },
   "legalApprovedAt": {
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
 "WaiverOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.waiver_requirement (new), marketing.form_definition, marketing.form_submission, marketing.waiver_signature, marketing.waiver_verification (new), marketing.waiver_exception (new), orders.order_line, orders.group_booking and catalogue.performance",
  "description": "Waiver readiness for the filters given. Counts are of participant waiver requirements for activities in the window unless the name says otherwise.",
  "required": [
   "waiversRequired",
   "completed",
   "pending",
   "completionRate",
   "byPeriod",
   "breakdown",
   "upcomingActivities"
  ],
  "properties": {
   "waiversRequired": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements assigned, excluding `superseded`."
   },
   "completed": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements `completed` or `verified`."
   },
   "pending": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements `assigned`, `sent` or `opened`, not yet started."
   },
   "partiallyCompleted": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements `inProgress`, and participants with some but not all waivers complete."
   },
   "expiring": {
    "type": "integer",
    "minimum": 0,
    "description": "Completed requirements whose acceptance (`FormSubmission.expiresAt`) ends before the activity starts."
   },
   "invalid": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements `expired`, or completed against a superseded version."
   },
   "rejected": {
    "type": "integer",
    "minimum": 0
   },
   "guardianConsentPending": {
    "type": "integer",
    "minimum": 0,
    "description": "Minor participants whose guardian has not yet signed."
   },
   "upcomingParticipantsMissingWaiver": {
    "type": "integer",
    "minimum": 0,
    "description": "Participants with at least one mandatory requirement not complete."
   },
   "accessBlocked": {
    "type": "integer",
    "minimum": 0,
    "description": "Participants whose ticket download, activation, check-in or access is currently blocked by a waiver."
   },
   "manualExceptions": {
    "type": "integer",
    "minimum": 0,
    "description": "Approved exceptions (`setWaiverException`) in force."
   },
   "completionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "`completed` / `waiversRequired`."
   },
   "byPeriod": {
    "type": "array",
    "description": "Today, tomorrow and this week, in that order, whatever the window.",
    "items": {
     "type": "object",
     "required": [
      "period",
      "waiversRequired",
      "completed",
      "missing"
     ],
     "properties": {
      "period": {
       "type": "string",
       "enum": [
        "today",
        "tomorrow",
        "thisWeek"
       ]
      },
      "waiversRequired": {
       "type": "integer",
       "minimum": 0
      },
      "completed": {
       "type": "integer",
       "minimum": 0
      },
      "missing": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "breakdown": {
    "type": "array",
    "maxItems": 100,
    "description": "One entry per value of `breakdownBy`, lowest completion first.",
    "items": {
     "type": "object",
     "required": [
      "key",
      "label",
      "waiversRequired",
      "completed",
      "completionRate"
     ],
     "properties": {
      "key": {
       "type": "string",
       "description": "The id of the venue, event, product, performance, group booking, booking or waiver form."
      },
      "label": {
       "type": "string"
      },
      "waiversRequired": {
       "type": "integer",
       "minimum": 0
      },
      "completed": {
       "type": "integer",
       "minimum": 0
      },
      "missing": {
       "type": "integer",
       "minimum": 0
      },
      "completionRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "upcomingActivities": {
    "type": "array",
    "maxItems": 100,
    "description": "Performances in the window, most at risk first, then by `dateTime`.",
    "items": {
     "type": "object",
     "required": [
      "performanceId",
      "eventActivity",
      "dateTime",
      "participants",
      "waiversRequired",
      "completed",
      "missing",
      "completion",
      "operationalRisk"
     ],
     "properties": {
      "performanceId": {
       "type": "string",
       "format": "uuid"
      },
      "eventId": {
       "type": "string",
       "format": "uuid"
      },
      "eventActivity": {
       "type": "string",
       "description": "The event or activity name."
      },
      "venueId": {
       "type": "string",
       "format": "uuid"
      },
      "venue": {
       "type": "string",
       "description": "The venue name."
      },
      "dateTime": {
       "type": "string",
       "format": "date-time",
       "description": "When the performance starts."
      },
      "participants": {
       "type": "integer",
       "minimum": 0
      },
      "waiversRequired": {
       "type": "integer",
       "minimum": 0
      },
      "completed": {
       "type": "integer",
       "minimum": 0
      },
      "missing": {
       "type": "integer",
       "minimum": 0
      },
      "completion": {
       "type": "number",
       "minimum": 0,
       "maximum": 1,
       "description": "The performance's waiver readiness (the pack's Readiness Score)."
      },
      "guardianPending": {
       "type": "integer",
       "minimum": 0
      },
      "exceptions": {
       "type": "integer",
       "minimum": 0
      },
      "admissionAtRisk": {
       "type": "boolean",
       "description": "At least one missing requirement is configured to block check-in or access."
      },
      "operationalRisk": {
       "type": "string",
       "enum": [
        "ready",
        "attention",
        "critical"
       ],
       "description": "`critical` when a missing requirement would block admission; `attention` when anything is missing; otherwise `ready`."
      }
     }
    }
   },
   "insights": {
    "type": "array",
    "maxItems": 20,
    "description": "Advisory predictions, e.g. participants unlikely to complete before arrival without another reminder. Never change a status.",
    "items": {
     "type": "object",
     "required": [
      "message"
     ],
     "properties": {
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "predictedIncomplete": {
       "type": "integer",
       "minimum": 0,
       "nullable": true
      },
      "message": {
       "type": "string",
       "maxLength": 500
      }
     }
    }
   }
  }
 },
 "WaiverVerificationValidationWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_verification",
  "description": "A reviewer's decision on one waiver submission. The automatic checks are the server's and are not sent; the reviewer records the checks only a person can make.",
  "required": [
   "submissionId",
   "result"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "submissionId": {
    "type": "string",
    "format": "uuid",
    "description": "The `FormSubmission` reviewed; the natural key."
   },
   "result": {
    "type": "string",
    "enum": [
     "verified",
     "rejected",
     "correctionRequired",
     "escalated"
    ]
   },
   "participantMatch": {
    "type": "boolean",
    "nullable": true,
    "description": "The reviewer confirmed the signed participant is the booked participant."
   },
   "bookingMatch": {
    "type": "boolean",
    "nullable": true
   },
   "guardianRelationshipPresent": {
    "type": "boolean",
    "nullable": true,
    "description": "The reviewer confirmed the signatory's guardianship under the configured policy."
   },
   "requiredEvidencePresent": {
    "type": "boolean",
    "nullable": true,
    "description": "Any supporting document the form requires was seen."
   },
   "reasonCode": {
    "type": "string",
    "nullable": true,
    "enum": [
     "signatoryNotAuthorised",
     "participantMismatch",
     "wrongVersion",
     "incompleteAnswers",
     "evidenceMissing",
     "suspectedFraud",
     "other"
    ]
   },
   "note": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true,
    "description": "Required for `rejected`, `correctionRequired`, `escalated`, and for changing an earlier decision."
   },
   "escalatedTo": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The staff member the review is escalated to; required for `escalated`."
   },
   "reviewedBy": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "reviewedAt": {
    "type": "string",
    "format": "date-time",
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
 "WaiverVerificationValidationWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.form_submission, marketing.waiver_signature, marketing.form_definition, marketing.waiver_verification (new) and marketing.waiver_requirement (new); names from pii.subject",
  "description": "One waiver submission in the verification queue, with its automatic checks, the reviewer's findings and any anomalies flagged.",
  "required": [
   "submissionId",
   "participant",
   "waiver",
   "version",
   "submitted",
   "status",
   "checks"
  ],
  "properties": {
   "submissionId": {
    "type": "string",
    "format": "uuid"
   },
   "requirementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "participant": {
    "type": "object",
    "properties": {
     "subjectId": {
      "type": "string",
      "format": "uuid"
     },
     "name": {
      "type": "string"
     },
     "age": {
      "type": "integer",
      "minimum": 0,
      "nullable": true
     }
    }
   },
   "waiver": {
    "type": "object",
    "properties": {
     "formId": {
      "type": "string",
      "format": "uuid"
     },
     "name": {
      "type": "string"
     }
    }
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "description": "The form version signed."
   },
   "booking": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "signatory": {
    "type": "object",
    "properties": {
     "subjectId": {
      "type": "string",
      "format": "uuid"
     },
     "name": {
      "type": "string"
     },
     "signatoryType": {
      "type": "string",
      "enum": [
       "participant",
       "guardian",
       "organisationRepresentative"
      ]
     }
    }
   },
   "submitted": {
    "type": "string",
    "format": "date-time",
    "description": "`FormSubmission.submittedAt`, the device time of signing."
   },
   "verificationReason": {
    "type": "string",
    "enum": [
     "configuredManualReview",
     "automaticCheckFailed",
     "minorSignedAsAdult",
     "guardianDiscrepancy",
     "participantMismatch",
     "evidenceRequired",
     "aiAnomaly",
     "sampleReview"
    ]
   },
   "risk": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "automaticallyValidated",
     "pendingManualVerification",
     "verified",
     "correctionRequired",
     "rejected",
     "escalated"
    ]
   },
   "checks": {
    "type": "object",
    "description": "Each check the form's configuration applies; null when it does not apply. The first seven are evaluated by the server, the last three recorded by the reviewer.",
    "properties": {
     "requiredFieldsComplete": {
      "type": "boolean",
      "nullable": true
     },
     "requiredQuestionsAnswered": {
      "type": "boolean",
      "nullable": true
     },
     "requiredAcknowledgementsAccepted": {
      "type": "boolean",
      "nullable": true
     },
     "signaturePresent": {
      "type": "boolean",
      "nullable": true
     },
     "correctWaiverVersion": {
      "type": "boolean",
      "nullable": true
     },
     "effectiveDateValid": {
      "type": "boolean",
      "nullable": true,
      "description": "The version signed was in effect at signing and the acceptance covers the visit."
     },
     "guardianRelationshipPresent": {
      "type": "boolean",
      "nullable": true,
      "description": "Evaluated from `GuestRelationship` where recorded, otherwise the reviewer's."
     },
     "participantMatch": {
      "type": "boolean",
      "nullable": true
     },
     "bookingMatch": {
      "type": "boolean",
      "nullable": true
     },
     "requiredEvidencePresent": {
      "type": "boolean",
      "nullable": true
     }
    }
   },
   "anomalies": {
    "type": "array",
    "description": "Advisory flags for the reviewer; never a decision.",
    "items": {
     "type": "object",
     "required": [
      "code",
      "message"
     ],
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "minorSignedAsAdult",
        "guardianSurnameDiffers",
        "signatoryIsMinor",
        "signedAfterActivity",
        "duplicateSubmission",
        "other"
       ]
      },
      "message": {
       "type": "string",
       "maxLength": 500
      },
      "source": {
       "type": "string",
       "enum": [
        "rule",
        "ai"
       ]
      }
     }
    }
   },
   "reviewedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reviewedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 }
}
```
