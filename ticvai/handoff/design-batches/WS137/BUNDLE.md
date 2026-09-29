# WS137 — Marketing CRM Configuration Reference v1.0 board 3

**10 screens · 11 operations · 13 schemas · 4 permissions**

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
  `AI_USE, MARKETING_MANAGE, MARKETING_VIEW, PRICE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-754` | Audience Intelligence | listDetail | 2 | 0 | — |
| `BO-755` | Dynamic Segment Builder | listDetail | 2 | 0 | — |
| `BO-756` | Static Lists & Imports | listDetail | 2 | 0 | — |
| `BO-757` | Behavioral Segmentation | listDetail | 1 | 0 | — |
| `BO-758` | Membership & Loyalty Segments | listDetail | 1 | 0 | — |
| `BO-759` | Demographic & Geographic | listDetail | 1 | 0 | — |
| `BO-760` | Revenue & Engagement Segments | listDetail | 1 | 0 | — |
| `BO-761` | AI Audience Discovery | listDetail | 2 | 0 | — |
| `BO-762` | Predictive Audiences | listDetail | 4 | 0 | — |
| `BO-763` | Activation & Governance | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-754, BO-755, BO-756, BO-757, BO-758, BO-759, BO-760, BO-761, BO-762 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-754",
  "name": "Audience Intelligence",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "01",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/audience-intelligence-bo-754",
   "component": "apps/venue-management-web/src/routes/engagement-support/AudienceIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-755",
    "BO-756",
    "BO-757",
    "BO-758",
    "BO-759",
    "BO-760",
    "BO-761",
    "BO-762",
    "BO-763"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-755",
     "trigger": "Dynamic Segment Builder",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "segmentId"
     ]
    },
    {
     "to": "BO-756",
     "trigger": "Static Lists & Imports",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-757",
     "trigger": "Behavioral Segmentation",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-758",
     "trigger": "Membership & Loyalty Segments",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-759",
     "trigger": "Demographic & Geographic",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-760",
     "trigger": "Revenue & Engagement Segments",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-761",
     "trigger": "AI Audience Discovery",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-762",
     "trigger": "Predictive Audiences",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "segmentId"
     ]
    },
    {
     "to": "BO-763",
     "trigger": "Activation & Governance",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give marketers and CRM teams an overview of addressable audience health. Show total guests, reachable guests, active segments, consent-eligible audience, high-value and churn-risk populations. Visualize growth, overlap, duplication, suppression and reachability by channel, brand, venue and region. Identify stale, shrinking, high-performing or conflicting audiences and link to the responsible definitions. Provide explainable AI observations without modifying or activating segments automatically. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 16"
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
       "impliedBy": "listSegments",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audience intelligence list.",
   "error": "Could not load. Names which read failed and leaves the audience intelligence untouched.",
   "emptyFirstRun": "No audience intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the audience intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAudienceOverlap",
    "contract": "marketing-crm",
    "purpose": "Reachability and overlap",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSegments",
    "contract": "marketing-crm",
    "purpose": "Active segments",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-754",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-754"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-755",
  "name": "Dynamic Segment Builder",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "02",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/dynamic-segment-builder-bo-755",
   "component": "apps/venue-management-web/src/routes/engagement-support/DynamicSegmentBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-754"
   ],
   "exitTo": [
    "BO-754"
   ],
   "transitions": [
    {
     "to": "BO-754",
     "trigger": "Back to Audience Intelligence",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized users to create automatically refreshed rule-based audiences. Provide nested AND/OR/NOT logic across profile, behavior, transaction, membership, loyalty, wallet and custom attributes. Show live audience count, reachable count, exclusions, consent impact and representative sample guests while rules are edited. Support effective dates, refresh frequency, ownership, tags, descriptions, approvals and reusable rule groups. Validate incompatible conditions, excessive complexity and restricted attributes before save or activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**Dynamic Segment Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 16"
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
       "impliedBy": "createSegment",
       "label": "Create segment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSegment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic segment list.",
   "error": "Could not load. Names which read failed and leaves the dynamic segment untouched.",
   "emptyFirstRun": "No dynamic segment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic segment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createSegment",
    "contract": "marketing-crm",
    "purpose": "Build a rule-based audience",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSegments",
     "getAudienceOverlap"
    ]
   },
   {
    "operationId": "previewSegment",
    "contract": "marketing-crm",
    "purpose": "Live count while editing",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-755",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-755"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "segmentId",
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
  "id": "BO-756",
  "name": "Static Lists & Imports",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "03",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/static-lists-imports-bo-756",
   "component": "apps/venue-management-web/src/routes/engagement-support/StaticListsImports.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-754"
   ],
   "exitTo": [
    "BO-754"
   ],
   "transitions": [
    {
     "to": "BO-754",
     "trigger": "Back to Audience Intelligence",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage governed fixed audiences and externally supplied lists. Create lists manually or through secure file import with field mapping, validation, deduplication and error handling. Configuration Scope of Work | Version 1.0 16 Match imported members to the Customer Master and control whether unmatched records may create leads or remain quarantined. Record source, owner, purpose, consent basis, expiry, refresh history and file provenance. Support additions, removals, suppression and export under RBAC/PBAC and audit controls. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 16"
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
       "impliedBy": "importAudienceList",
       "label": "Import audience list",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAudienceLists",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "importAudienceList"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The static lists imports list.",
   "error": "Could not load. Names which read failed and leaves the static lists imports untouched.",
   "emptyFirstRun": "No static lists imports yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the static lists imports are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "importAudienceList",
    "contract": "marketing-crm",
    "purpose": "Import a supplied list",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAudienceLists",
     "listSegments"
    ]
   },
   {
    "operationId": "listAudienceLists",
    "contract": "marketing-crm",
    "purpose": "Lists held",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-756",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-756"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-757",
  "name": "Behavioral Segmentation",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "04",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/behavioral-segmentation-bo-757",
   "component": "apps/venue-management-web/src/routes/engagement-support/BehavioralSegmentation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-754"
   ],
   "exitTo": [
    "BO-754"
   ],
   "transitions": [
    {
     "to": "BO-754",
     "trigger": "Back to Audience Intelligence",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Build audiences from observable guest activity. Use purchase, visit, ticket scan, reservation, cart, app, web, campaign, chatbot, survey and review events. Support recency, frequency, count, value, sequence, absence-of-event and time-window conditions. Preview top behaviors, sources and data freshness and exclude bot, employee, test or fraudulent activity. Refresh segments through event streams and expose rule/version provenance for each inclusion. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 17"
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
       "impliedBy": "createSegment",
       "label": "Create segment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSegment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The behavioral segmentation list.",
   "error": "Could not load. Names which read failed and leaves the behavioral segmentation untouched.",
   "emptyFirstRun": "No behavioral segmentation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the behavioral segmentation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createSegment",
    "contract": "marketing-crm",
    "purpose": "Behavioural conditions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSegments",
     "getAudienceOverlap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-757",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-757"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 17. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-758",
  "name": "Membership & Loyalty Segments",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "05",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/membership-loyalty-segments-bo-758",
   "component": "apps/venue-management-web/src/routes/engagement-support/MembershipLoyaltySegments.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-754"
   ],
   "exitTo": [
    "BO-754"
   ],
   "transitions": [
    {
     "to": "BO-754",
     "trigger": "Back to Audience Intelligence",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create audiences using membership, loyalty and wallet state. Filter by membership type, status, start, expiry, renewal, freeze, benefit use and upgrade eligibility. Filter by loyalty tier, points, earn/redemption history, reward use, milestone and tier movement. Use wallet balance, top-up, spend, low-balance and dormancy conditions while protecting financial data. Combine these signals with profile and behavior rules and show reachable audience before activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 17"
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
       "impliedBy": "createSegment",
       "label": "Create segment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSegment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership loyalty segments list.",
   "error": "Could not load. Names which read failed and leaves the membership loyalty segments untouched.",
   "emptyFirstRun": "No membership loyalty segments yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership loyalty segments are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createSegment",
    "contract": "marketing-crm",
    "purpose": "Membership, loyalty and wallet conditions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSegments",
     "getAudienceOverlap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-758",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-758"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 17. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-759",
  "name": "Demographic & Geographic",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "06",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/demographic-geographic-bo-759",
   "component": "apps/venue-management-web/src/routes/engagement-support/DemographicGeographic.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-754"
   ],
   "exitTo": [
    "BO-754"
   ],
   "transitions": [
    {
     "to": "BO-754",
     "trigger": "Back to Audience Intelligence",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure demographic and location-based audiences responsibly. Use age band, household, language, country, city, postcode, visitor type, nationality where lawful and custom demographics. Support location radius, venue proximity, travel market, timezone and resident/tourist classification. Display consent, fairness, minimum-audience and restricted-attribute warnings before use. Allow jurisdiction-specific field availability and prevent prohibited sensitive targeting. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 17"
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
       "impliedBy": "createSegment",
       "label": "Create segment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSegment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The demographic geographic list.",
   "error": "Could not load. Names which read failed and leaves the demographic geographic untouched.",
   "emptyFirstRun": "No demographic geographic yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the demographic geographic are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createSegment",
    "contract": "marketing-crm",
    "purpose": "Demographic and geographic conditions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSegments",
     "getAudienceOverlap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-759",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-759"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 17. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-760",
  "name": "Revenue & Engagement Segments",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "07",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/revenue-engagement-segments-bo-760",
   "component": "apps/venue-management-web/src/routes/engagement-support/RevenueEngagementSegments.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-754"
   ],
   "exitTo": [
    "BO-754"
   ],
   "transitions": [
    {
     "to": "BO-754",
     "trigger": "Back to Audience Intelligence",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create value- and engagement-based audiences. Configuration Scope of Work | Version 1.0 17 Use total revenue, LTV, average order value, purchase frequency, category spend, refund behavior and propensity. Use engagement score, campaign interaction, app activity, visit frequency, inactivity and product affinity. Define bands, percentiles, scoring periods and calculation sources and preview distribution before publishing. Protect against circular attribution and record the data snapshot and scoring version used. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 17"
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
       "impliedBy": "createSegment",
       "label": "Create segment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSegment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue engagement segments list.",
   "error": "Could not load. Names which read failed and leaves the revenue engagement segments untouched.",
   "emptyFirstRun": "No revenue engagement segments yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue engagement segments are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createSegment",
    "contract": "marketing-crm",
    "purpose": "Value and engagement bands",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSegments",
     "getAudienceOverlap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-760",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-760"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 17. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-761",
  "name": "AI Audience Discovery",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "08",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/ai-audience-discovery-bo-761",
   "component": "apps/venue-management-web/src/routes/engagement-support/AiAudienceDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-754"
   ],
   "exitTo": [
    "BO-754"
   ],
   "transitions": [
    {
     "to": "BO-754",
     "trigger": "Back to Audience Intelligence",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Discover meaningful customer clusters using explainable AI. Present suggested clusters with dominant traits, size, reachability, value, engagement and observed opportunity. Show contributing variables, confidence, stability, bias/fairness checks and excluded sensitive attributes. Allow users to inspect sample profiles and convert a recommendation into an editable governed segment. Require human approval and retain feedback, model/version and final segment definition. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 18"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 18"
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
       "impliedBy": "listAudienceDiscoveryTargeting",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "proposeLookalikeSegment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "proposeLookalikeSegment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audience discovery list.",
   "error": "Could not load. Names which read failed and leaves the audience discovery untouched.",
   "emptyFirstRun": "No audience discovery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the audience discovery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAudienceDiscoveryTargeting",
    "contract": "promotions",
    "purpose": "AI Audience Discovery & Targeting Optimization",
    "trigger": "onLoad"
   },
   {
    "operationId": "proposeLookalikeSegment",
    "contract": "ai",
    "purpose": "Propose a lookalike segment from a seed segment or list, as rules to save",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-761",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-761"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-762",
  "name": "Predictive Audiences",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "09",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/predictive-audiences-bo-762",
   "component": "apps/venue-management-web/src/routes/engagement-support/PredictiveAudiences.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-754"
   ],
   "exitTo": [
    "BO-754"
   ],
   "transitions": [
    {
     "to": "BO-754",
     "trigger": "Back to Audience Intelligence",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create model-based audiences for future behavior and opportunity. Support lookalike, churn, reactivation, membership upgrade, next purchase and high-value propensity audiences. Display prediction window, threshold, audience size, confidence, lift and primary model factors. Allow threshold simulation and exclusions and monitor drift, performance and fairness after activation. Never use predictive status to override consent, eligibility, pricing, capacity or service policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 18"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 18"
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
       "impliedBy": "createSegment",
       "label": "Create segment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSegment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The predictive audiences list.",
   "error": "Could not load. Names which read failed and leaves the predictive audiences untouched.",
   "emptyFirstRun": "No predictive audiences yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the predictive audiences are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createSegment",
    "contract": "marketing-crm",
    "purpose": "Convert a predictive audience into a segment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSegments",
     "getAudienceOverlap"
    ]
   },
   {
    "operationId": "previewSegment",
    "contract": "marketing-crm",
    "purpose": "Threshold simulation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "decideProposedAction",
    "contract": "ai",
    "purpose": "Record which AI draft or proposal was used, or why it was refused",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "proposeLookalikeSegment",
    "contract": "ai",
    "purpose": "Propose a lookalike segment from a seed segment or list, as rules to save",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-762",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-762"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "segmentId",
     "from": "navigation"
    },
    {
     "name": "actionId",
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
  "id": "BO-763",
  "name": "Activation & Governance",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "3",
   "number": "10",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/activation-governance-bo-763",
   "component": "apps/venue-management-web/src/routes/engagement-support/ActivationGovernance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-754"
   ],
   "exitTo": [
    "BO-754"
   ],
   "transitions": [
    {
     "to": "BO-754",
     "trigger": "Back to Audience Intelligence",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control where audiences are used and how they remain compliant. Activate to campaigns, journeys, website, mobile app and approved external platforms through secured connectors. Configure suppression, consent enforcement, frequency limits, destination mapping, refresh schedule and expiry. Require approval for sensitive, high-volume or external activation and provide a pre-flight impact summary. Configuration Scope of Work | Version 1.0 18 Track synchronization, failures, member counts, destination use, versions and the complete activation audit trail. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 19 Board 4 - Campaign Management & Attribution Figure 4. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 20",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 18"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 18"
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
       "impliedBy": "activateAudience",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAudienceActivations",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "activateAudience"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The activation governance list.",
   "error": "Could not load. Names which read failed and leaves the activation governance untouched.",
   "emptyFirstRun": "No activation governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the activation governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "activateAudience",
    "contract": "marketing-crm",
    "purpose": "Push it somewhere, with consent enforced",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAudienceActivations"
    ]
   },
   {
    "operationId": "listAudienceActivations",
    "contract": "marketing-crm",
    "purpose": "Where audiences are in use",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-763",
   "workshopBoard": "wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-763"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "activateAudience": {
  "method": "POST",
  "path": "/audience-activations",
  "contract": "marketing-crm",
  "summary": "Push an audience to a campaign, journey or external platform",
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
  "requestBody": "AudienceActivation",
  "responds": null
 },
 "createSegment": {
  "method": "POST",
  "path": "/segments",
  "contract": "marketing-crm",
  "summary": "Create a segment",
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
  "requestBody": "CreateSegmentRequest",
  "responds": "Segment"
 },
 "decideProposedAction": {
  "method": "POST",
  "path": "/proposed-actions/{actionId}/decide",
  "contract": "ai",
  "summary": "Approve or reject a proposal",
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
  "responds": "ProposedAction"
 },
 "getAudienceOverlap": {
  "method": "GET",
  "path": "/audience-overlap",
  "contract": "marketing-crm",
  "summary": "How much audiences overlap, and how many are reachable",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "segmentIds",
    "in": "query",
    "required": true
   },
   {
    "name": "channel",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AudienceOverlap"
 },
 "importAudienceList": {
  "method": "POST",
  "path": "/audience-lists",
  "contract": "marketing-crm",
  "summary": "Load a supplied list, matched against the guest master",
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
  "requestBody": "AudienceList",
  "responds": "AudienceList"
 },
 "listAudienceActivations": {
  "method": "GET",
  "path": "/audience-activations",
  "contract": "marketing-crm",
  "summary": "Where audiences are being used, and whether they are still in sync",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "listAudienceDiscoveryTargeting": {
  "method": "GET",
  "path": "/audience-discovery-targeting",
  "contract": "promotions",
  "summary": "AI Audience Discovery & Targeting Optimization",
  "permission": "PRICE_VIEW",
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
  "responds": "AiAudienceDiscoveryTargetingOptimizationView"
 },
 "listAudienceLists": {
  "method": "GET",
  "path": "/audience-lists",
  "contract": "marketing-crm",
  "summary": "Static and imported audiences",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "listSegments": {
  "method": "GET",
  "path": "/segments",
  "contract": "marketing-crm",
  "summary": "List segments",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "search",
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
 "previewSegment": {
  "method": "POST",
  "path": "/segments/{segmentId}/preview",
  "contract": "marketing-crm",
  "summary": "Estimate segment size and reachability",
  "permission": "MARKETING_VIEW",
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
  "responds": "SegmentPreview"
 },
 "proposeLookalikeSegment": {
  "method": "POST",
  "path": "/ai/segment-suggestions",
  "contract": "ai",
  "summary": "Propose a lookalike segment from a seed, for a person to save",
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
  "responds": "AiLookalikeSegmentProposal"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiAudienceDiscoveryTargetingOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What AI Audience Discovery & Targeting Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "narrowAudience": {
    "type": "string",
    "description": "Narrow audience"
   },
   "expandAudience": {
    "type": "string",
    "description": "Expand audience"
   },
   "excludeLowValueSegment": {
    "type": "string",
    "description": "Exclude low-value segment"
   },
   "changeEligibility": {
    "type": "string",
    "description": "Change eligibility"
   },
   "changeChannel": {
    "type": "string",
    "description": "Change channel"
   },
   "changeTiming": {
    "type": "string",
    "description": "Change timing"
   },
   "changePromotion": {
    "type": "string",
    "description": "Change promotion"
   },
   "reduceFrequency": {
    "type": "string",
    "description": "Reduce frequency"
   },
   "membershipTierEligibility": {
    "type": "string",
    "description": "Membership/tier eligibility"
   },
   "membershipAndLoyaltyEligibility": {
    "type": "string",
    "description": "Membership and loyalty eligibility"
   },
   "audienceName": {
    "type": "string",
    "description": "Discovered audience"
   },
   "audienceSize": {
    "type": "integer",
    "description": "Audience size"
   },
   "suggestedOffer": {
    "type": "string",
    "description": "Suggested offer"
   },
   "predictedConversion": {
    "type": "number",
    "description": "Predicted conversion, percent"
   },
   "estimatedIncrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated incremental revenue"
   },
   "rationale": {
    "type": "string",
    "description": "Why this audience (explainable factors)"
   }
  }
 },
 "AiLookalikeSegmentProposal": {
  "type": "object",
  "x-ticvai-persistence": "none — the draft is an ai.proposed_action row (kind audience); the evidence is its decision record",
  "description": "A lookalike segment as rules a person can read, edit and save (22.14.12). The criteria are shaped as `marketing-crm` `SegmentCriterion` (attribute, operator, value) and restated here because a satellite cannot reference another satellite.",
  "required": [
   "proposedActionId",
   "criteria",
   "estimatedReach"
  ],
  "properties": {
   "proposedActionId": {
    "type": "string",
    "format": "uuid",
    "description": "The `ai.proposed_action` row whose payload is the `marketing-crm.createSegment` body."
   },
   "name": {
    "type": "string",
    "nullable": true
   },
   "criteria": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "attribute",
      "operator"
     ],
     "properties": {
      "attribute": {
       "type": "string"
      },
      "operator": {
       "type": "string"
      },
      "value": {
       "description": "As `SegmentCriterion.value` in marketing-crm (any type)."
      },
      "weight": {
       "type": "number",
       "nullable": true,
       "description": "How much this attribute separated the seed from everyone else."
      }
     }
    }
   },
   "similarityBasis": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "attribute": {
       "type": "string"
      },
      "seedShare": {
       "type": "number",
       "description": "Share of the seed holding the value."
      },
      "populationShare": {
       "type": "number",
       "description": "Share of the tenant's consented guests holding it."
      }
     }
    }
   },
   "estimatedReach": {
    "type": "integer",
    "description": "Consented guests the criteria select, excluding the seed where `excludeSeed`."
   },
   "seedSize": {
    "type": "integer"
   },
   "overlapWithSeed": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Share of the seed the criteria would also select; a check that the rules describe the seed."
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "AudienceActivation": {
  "type": "object",
  "x-ticvai-persistence": "marketing.audience_activation",
  "description": "Board 3.10. **Consent is enforced at activation, not at definition.**",
  "required": [
   "segmentId",
   "destination"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "segmentId": {
    "type": "string",
    "format": "uuid"
   },
   "destination": {
    "type": "string",
    "enum": [
     "campaign",
     "journey",
     "website",
     "mobileApp",
     "externalAdPlatform",
     "partnerFeed"
    ]
   },
   "destinationReference": {
    "type": "string",
    "nullable": true
   },
   "external": {
    "type": "boolean",
    "default": false
   },
   "suppressionListIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "enforceConsent": {
    "type": "boolean",
    "default": true
   },
   "frequencyCapPerWeek": {
    "type": "integer",
    "nullable": true
   },
   "refreshSchedule": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "preFlight": {
    "type": "object",
    "readOnly": true,
    "properties": {
     "members": {
      "type": "integer"
     },
     "reachable": {
      "type": "integer"
     },
     "suppressed": {
      "type": "integer"
     },
     "consentBlocked": {
      "type": "integer"
     },
     "frequencyBlocked": {
      "type": "integer"
     }
    }
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "failed",
     "expired"
    ]
   },
   "lastSyncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastSyncErrors": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AudienceList": {
  "type": "object",
  "x-ticvai-persistence": "marketing.audience_list",
  "description": "Board 3.3. **Consent basis is required on the import, not optional metadata.**",
  "required": [
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "manual",
     "imported",
     "suppression"
    ]
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "fieldMapping": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "rowsRead": {
    "type": "integer",
    "readOnly": true
   },
   "matched": {
    "type": "integer",
    "readOnly": true
   },
   "unmatched": {
    "type": "integer",
    "readOnly": true
   },
   "duplicatesRemoved": {
    "type": "integer",
    "readOnly": true
   },
   "rejected": {
    "type": "integer",
    "readOnly": true
   },
   "unmatchedHandling": {
    "type": "string",
    "enum": [
     "createLead",
     "quarantine"
    ],
    "default": "quarantine",
    "description": "**The two honest answers.** Silently dropping them tells a marketer their list of ten thousand reached ten thousand.\n"
   },
   "source": {
    "type": "string"
   },
   "owner": {
    "type": "string",
    "format": "uuid"
   },
   "purpose": {
    "type": "string"
   },
   "consentBasis": {
    "type": "string"
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AudienceOverlap": {
  "type": "object",
  "description": "Board 3.1. **Reachable is always smaller, and it is the number that matters.**",
  "properties": {
   "segments": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "segmentId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "members": {
       "type": "integer"
      },
      "reachable": {
       "type": "integer"
      },
      "suppressed": {
       "type": "integer"
      },
      "consentBlocked": {
       "type": "integer"
      },
      "duplicates": {
       "type": "integer"
      }
     }
    }
   },
   "pairwiseOverlap": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "segmentIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "shared": {
       "type": "integer"
      },
      "sharedPercent": {
       "type": "number"
      }
     }
    }
   },
   "totalUnique": {
    "type": "integer"
   },
   "totalReachable": {
    "type": "integer"
   }
  }
 },
 "CreateSegmentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "criteria"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "match": {
    "type": "string",
    "enum": [
     "all",
     "any"
    ],
    "default": "all"
   },
   "criteria": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/SegmentCriterion"
    }
   },
   "excludeSegmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
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
 },
 "ProposedAction": {
  "type": "object",
  "x-ticvai-persistence": "ai.proposed_action",
  "required": [
   "id",
   "kind",
   "targetContract",
   "targetOperation",
   "payload",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "interactionId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "pricing",
     "promotion",
     "operational",
     "financial",
     "configuration",
     "content",
     "audience"
    ],
    "description": "`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."
   },
   "targetContract": {
    "type": "string",
    "description": "Which contract would perform it. The assistant never performs it itself."
   },
   "targetOperation": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "description": "**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n",
    "enum": [
     "proposed",
     "approved",
     "rejected",
     "applied",
     "expired"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."
   },
   "approvalLevel": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decisionReason": {
    "type": "string",
    "nullable": true,
    "description": "Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"
   },
   "proposedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan",
    "description": "The plan this action presents for a decision (AI design 2.2 D, 3.8)."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."
   },
   "changeSetHash": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."
   }
  }
 },
 "Segment": {
  "x-ticvai-persistence": "marketing.segment + marketing.segment_criterion",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateSegmentRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "lastEvaluatedSize": {
      "type": "integer",
      "nullable": true
     },
     "lastEvaluatedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "SegmentCriterion": {
  "x-ticvai-persistence": "marketing.segment_criterion",
  "type": "object",
  "required": [
   "attribute",
   "operator"
  ],
  "properties": {
   "attribute": {
    "type": "string",
    "description": "Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language.\n**Free-form rather than an enum, which is why 22.14.8, 5.3.19 and 5.5.17b were readable as gaps and are not.** `walletBalance`, `engagementTier` and `portfolioScope` are expressible today; what was missing was anybody saying so.\n**Three that need saying, because the naive reading is wrong:**\n`walletBalance` should segment on **`cash` credit only**. A guest with 200 dirhams of promotional credit expiring Friday is a different campaign from one with 200 of their own money, and treating them alike sends a spend-it-now message to somebody who was given it.\n`walletBalance.expiringWithinDays` is the segment that earns the attribute — **credit about to expire unspent is a guest about to be disappointed and a venue about to book breakage**, and only one of those is worth a message.\n`portfolioScope` aggregates across a `DelegatedAccess` delegation (CF-132) and **must not message every member about a household total** — that is how a venue tells a teenager what their parent spends.\n`entitlementExpiringWithinDays` (29 September, build pass, group G2; 5.5.30): the guest holds a ticket or pass in `issued` or `partiallyConsumed` whose `validTo` is within that many days, kept current from `entitlement.expiringSoon` and the entitlement read model. **Unused passes about to lapse** are this attribute with `entitlementRemainingUses` greater than zero.\n"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "in",
     "notIn",
     "exists",
     "notExists",
     "withinDays"
    ]
   },
   "value": {},
   "values": {
    "type": "array",
    "items": {}
   }
  }
 },
 "SegmentPreview": {
  "x-ticvai-persistence": "none — evaluated live",
  "type": "object",
  "required": [
   "segmentId",
   "matchingCount",
   "reachable"
  ],
  "properties": {
   "segmentId": {
    "type": "string",
    "format": "uuid"
   },
   "matchingCount": {
    "type": "integer"
   },
   "reachable": {
    "type": "array",
    "description": "Per channel, after consent and suppression. A segment of 50,000 with 3,000 email consents is a 3,000-person campaign.\n",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "reachableCount": {
       "type": "integer"
      },
      "excludedNoConsent": {
       "type": "integer"
      },
      "excludedSuppressed": {
       "type": "integer"
      },
      "excludedNoAddress": {
       "type": "integer"
      }
     }
    }
   },
   "evaluatedAt": {
    "type": "string",
    "format": "date-time"
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
 }
}
```
