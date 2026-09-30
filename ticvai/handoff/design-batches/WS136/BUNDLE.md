# WS136 — Marketing CRM Configuration Reference v1.0 board 2

**10 screens · 23 operations · 26 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `AUDIT_VIEW, GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, MARKETING_MANAGE, MARKETING_VIEW, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-744` | Data Governance Center | listDetail | 2 | 0 | — |
| `BO-745` | Identity Resolution Rules | listDetail | 2 | 0 | — |
| `BO-746` | Duplicate Review & Merge | listDetail | 5 | 0 | — |
| `BO-747` | Consent Policy Configuration | listDetail | 2 | 0 | — |
| `BO-748` | Consent Capture & Versions | listDetail | 2 | 0 | — |
| `BO-749` | Guest Preference Center | listDetail | 2 | 0 | — |
| `BO-750` | Data Subject Requests | listDetail | 2 | 0 | — |
| `BO-751` | Retention & Anonymization | listDetail | 4 | 0 | — |
| `BO-752` | Privacy & AI Governance | listDetail | 2 | 0 | — |
| `BO-753` | Compliance Audit Dashboard | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-744, BO-745, BO-746, BO-747, BO-748, BO-749, BO-750, BO-751, BO-752, BO-753 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-744",
  "name": "Data Governance Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "01",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/data-governance-center-bo-744",
   "component": "apps/venue-management-web/src/routes/engagement-support/DataGovernanceCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-745",
    "BO-746",
    "BO-747",
    "BO-748",
    "BO-749",
    "BO-750",
    "BO-751",
    "BO-752",
    "BO-753"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-745",
     "trigger": "Identity Resolution Rules",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-746",
     "trigger": "Duplicate Review & Merge",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-747",
     "trigger": "Consent Policy Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-748",
     "trigger": "Consent Capture & Versions",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-749",
     "trigger": "Guest Preference Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-750",
     "trigger": "Data Subject Requests",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-751",
     "trigger": "Retention & Anonymization",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-752",
     "trigger": "Privacy & AI Governance",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-753",
     "trigger": "Compliance Audit Dashboard",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a consolidated view of customer-data quality, consent and privacy operations. Show duplicate profiles, pending merges, consent coverage, expiring consent, data-subject requests, retention actions and incidents. Filter by tenant, brand, venue, region, jurisdiction, data category, severity and owner. Surface overdue work, legal deadlines and high-risk exceptions with drill-down to the governing record. Provide trend analysis and controlled exports for privacy, legal, security and audit teams. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 11"
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
       "impliedBy": "listPrivacyCompliance",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data governance list.",
   "error": "Could not load. Names which read failed and leaves the data governance untouched.",
   "emptyFirstRun": "No data governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrivacyCompliance",
    "contract": "marketing-crm",
    "purpose": "Data quality and consent coverage",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listDuplicateCandidates",
    "contract": "marketing-crm",
    "purpose": "Pending merges",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-744",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-744"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-745",
  "name": "Identity Resolution Rules",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "02",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/identity-resolution-rules-bo-745",
   "component": "apps/venue-management-web/src/routes/engagement-support/IdentityResolutionRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-744"
   ],
   "exitTo": [
    "BO-744"
   ],
   "transitions": [
    {
     "to": "BO-744",
     "trigger": "Back to Data Governance Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how potential duplicates are detected and a master identity is selected. Build weighted exact, normalized and fuzzy matching rules for email, phone, name, date of birth, membership, loyalty, passport and external IDs. Define match, possible-match and no-match thresholds, source priority, survivorship and field- level confidence. Support jurisdictional restrictions, excluded sources, false-positive handling and rule simulation before activation. Version, approve and audit rules and record the rule/version used for every automated decision. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 11"
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
       "impliedBy": "setIdentityResolutionRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setIdentityResolutionRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The identity resolution rules list.",
   "error": "Could not load. Names which read failed and leaves the identity resolution rules untouched.",
   "emptyFirstRun": "No identity resolution rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the identity resolution rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getIdentityResolutionRules",
    "contract": "marketing-crm",
    "purpose": "Matching rules",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setIdentityResolutionRules",
    "contract": "marketing-crm",
    "purpose": "Weights, thresholds, survivorship",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getIdentityResolutionRules",
     "listDuplicateCandidates"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-745",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-745"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-746",
  "name": "Duplicate Review & Merge",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "03",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/duplicate-review-merge-bo-746",
   "component": "apps/venue-management-web/src/routes/engagement-support/DuplicateReviewMerge.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-744"
   ],
   "exitTo": [
    "BO-744"
   ],
   "transitions": [
    {
     "to": "BO-744",
     "trigger": "Back to Data Governance Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow trained users to review, merge, split or reject suspected duplicate profiles. Compare records side by side, highlight conflicts and display recommended master values with confidence and source provenance. Configuration Scope of Work | Version 1.0 11 Preview linked tickets, bookings, memberships, loyalty, wallet, cases, consents and documents before committing. Preserve all transaction history, identifiers, relationships and audit evidence and prevent unsafe automatic merges. Require reason codes and approval for high-risk merges and support controlled split/recovery where permitted. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 11"
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
       "impliedBy": "listDuplicateCandidates",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows. **Only unverified matches arrive here** (decided 28 September, audit R120 (b)): a verified contact match attaches the order to the guest automatically at checkout, so this queue holds the matches no guest has proved."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "decideDuplicateCandidate",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "decideDuplicateCandidate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The duplicate review merge list.",
   "error": "Could not load. Names which read failed and leaves the duplicate review merge untouched.",
   "emptyFirstRun": "No duplicate review merge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the duplicate review merge are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestMatchPolicy",
    "contract": "marketing-crm",
    "purpose": "How returning guests are recognised",
    "trigger": "onLoad"
   },
   {
    "operationId": "setGuestMatchPolicy",
    "contract": "marketing-crm",
    "purpose": "Match returning guests by email, mobile or either",
    "trigger": "onAction"
   },
   {
    "operationId": "listDuplicateCandidates",
    "contract": "marketing-crm",
    "purpose": "Side by side",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "decideDuplicateCandidate",
    "contract": "marketing-crm",
    "purpose": "Merge, reject or split",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listDuplicateCandidates"
    ]
   },
   {
    "operationId": "mergeGuests",
    "contract": "marketing-crm",
    "purpose": "Perform the merge",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listDuplicateCandidates",
     "searchGuests",
     "getGuestProfile"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-746",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-746"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "candidateId",
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
  "id": "BO-747",
  "name": "Consent Policy Configuration",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "04",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/consent-policy-configuration-bo-747",
   "component": "apps/venue-management-web/src/routes/engagement-support/ConsentPolicyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-744"
   ],
   "exitTo": [
    "BO-744"
   ],
   "transitions": [
    {
     "to": "BO-744",
     "trigger": "Back to Data Governance Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the legal and operational rules governing consent. Configure consent purposes, marketing categories, processing purposes and channel-specific permission for email, SMS, WhatsApp, push and direct mail. Define jurisdiction, lawful basis, age and guardian requirements, capture channels, expiry, renewal and hard/soft enforcement. Map policies to brands, venues, products, audiences and processing activities with precedence and conflict handling. Require legal review, effective dates, version control and immutable policy-change history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 12"
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
       "impliedBy": "listConsentPurposes",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setConsentPurposes",
       "label": "Save consent purposes",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setConsentPurposes"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The consent policy list.",
   "error": "Could not load. Names which read failed and leaves the consent policy untouched.",
   "emptyFirstRun": "No consent policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the consent policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConsentPurposes",
    "contract": "marketing-crm",
    "purpose": "Purposes and lawful bases",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setConsentPurposes",
    "contract": "marketing-crm",
    "purpose": "Configure them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-747",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-747"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-748",
  "name": "Consent Capture & Versions",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "05",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/consent-capture-versions-bo-748",
   "component": "apps/venue-management-web/src/routes/engagement-support/ConsentCaptureVersions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-744"
   ],
   "exitTo": [
    "BO-744"
   ],
   "transitions": [
    {
     "to": "BO-744",
     "trigger": "Back to Data Governance Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage the content and lifecycle of guest consent statements. Create multilingual consent versions with acknowledgement text, links, effective dates and supported channels. Capture who consented, what they saw, when, where, by which channel and under which policy version. Support withdrawal, expiry, re-consent and guardian authorization without overwriting prior evidence. Publish only approved versions and make the active statement available consistently to all touchpoints. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 12"
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "recordConsent",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordConsent"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The consent capture versions list.",
   "error": "Could not load. Names which read failed and leaves the consent capture versions untouched.",
   "emptyFirstRun": "No consent capture versions yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the consent capture versions are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVersioningEffectiveDate",
    "contract": "marketing-crm",
    "purpose": "Consent versions",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "recordConsent",
    "contract": "marketing-crm",
    "purpose": "Capture a decision",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGuestConsents",
     "getAudienceOverlap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-748",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-748"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-749",
  "name": "Guest Preference Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "06",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/guest-preference-center-bo-749",
   "component": "apps/venue-management-web/src/routes/engagement-support/GuestPreferenceCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-744"
   ],
   "exitTo": [
    "BO-744"
   ],
   "transitions": [
    {
     "to": "BO-744",
     "trigger": "Back to Data Governance Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the guest-facing center for communication choices and privacy preferences. Expose subscription categories, topics, preferred channels, contact frequency, quiet hours and global or brand-level opt-outs. Apply identity verification and clearly distinguish transactional messages from optional marketing. Synchronize changes in real time to campaigns, journeys, chatbot, newsletters and notification delivery. Store an auditable receipt for every preference change and provide accessible, multilingual presentation. Configuration Scope of Work | Version 1.0 12 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 12"
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
       "impliedBy": "setCommunicationPreferenceMarketing",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getGuestConsents",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setCommunicationPreferenceMarketing"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest preference list.",
   "error": "Could not load. Names which read failed and leaves the guest preference untouched.",
   "emptyFirstRun": "No guest preference yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest preference are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCommunicationPreferenceMarketing",
    "contract": "marketing-crm",
    "purpose": "The preference centre",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getGuestConsents",
    "contract": "marketing-crm",
    "purpose": "What a guest has chosen",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-749",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-749"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-750",
  "name": "Data Subject Requests",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "07",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/data-subject-requests-bo-750",
   "component": "apps/venue-management-web/src/routes/engagement-support/DataSubjectRequests.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-744"
   ],
   "exitTo": [
    "BO-744"
   ],
   "transitions": [
    {
     "to": "BO-744",
     "trigger": "Back to Data Governance Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage privacy requests from intake through verified completion. Support access, rectification, portability, erasure, restriction and objection request types. Verify requester identity, calculate statutory deadlines, assign owners, gather approvals and track dependencies. Search connected systems, assemble export packages and document exclusions, legal holds or denied actions. Record communications, evidence, completion status and SLA performance in an immutable case history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 13"
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
       "impliedBy": "listDataSubjectCustomer",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setDataDiscoveryAccess",
       "label": "Save data discovery access",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setDataDiscoveryAccess"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data subject requests list.",
   "error": "Could not load. Names which read failed and leaves the data subject requests untouched.",
   "emptyFirstRun": "No data subject requests yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data subject requests are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDataSubjectCustomer",
    "contract": "marketing-crm",
    "purpose": "Privacy requests",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setDataDiscoveryAccess",
    "contract": "marketing-crm",
    "purpose": "Assemble and respond",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-750",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-750"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-751",
  "name": "Retention & Anonymization",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "08",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/retention-anonymization-bo-751",
   "component": "apps/venue-management-web/src/routes/engagement-support/RetentionAnonymization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-744"
   ],
   "exitTo": [
    "BO-744"
   ],
   "transitions": [
    {
     "to": "BO-744",
     "trigger": "Back to Data Governance Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how long customer data is retained and what happens at expiry. Define policies by data category, jurisdiction, purpose, guest status, transaction type and source system. Support archive, anonymize, pseudonymize and delete actions, legal holds, fraud exceptions and scheduled execution. Preview affected records, dependencies and downstream consequences before high-impact actions. Produce completion evidence and reconcile results across analytics, search, documents, backups and integrations. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 13"
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
       "impliedBy": "setDataRetentionPolicy",
       "label": "Save data retention policy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setDataRetentionPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The retention anonymization list.",
   "error": "Could not load. Names which read failed and leaves the retention anonymization untouched.",
   "emptyFirstRun": "No retention anonymization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the retention anonymization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDataRetentionPolicy",
    "contract": "marketing-crm",
    "purpose": "Retention by category and jurisdiction",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listDataRetentionExpiry"
    ]
   },
   {
    "operationId": "runDataRetention",
    "contract": "marketing-crm",
    "purpose": "Preview or execute",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listDataRetentionExpiry",
     "searchGuests"
    ]
   },
   {
    "operationId": "listDataRetentionSettings",
    "contract": "tenancy",
    "purpose": "Retention period per data class",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setDataRetentionSetting",
    "contract": "tenancy",
    "purpose": "Set a class's period",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-751",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-751"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "dataClass",
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
  "id": "BO-752",
  "name": "Privacy & AI Governance",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "09",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/privacy-ai-governance-bo-752",
   "component": "apps/venue-management-web/src/routes/engagement-support/PrivacyAiGovernance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-744"
   ],
   "exitTo": [
    "BO-744"
   ],
   "transitions": [
    {
     "to": "BO-744",
     "trigger": "Back to Data Governance Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control privacy incidents and approved uses of customer data by AI. Track incident type, severity, affected data, containment, owner, notification obligations, mitigation and closure. Maintain approved models/use cases, prohibited data, risk level, purpose limitation and human- review requirements. Configure prompt/output retention, masking, vendor/model access and escalation for sensitive or high-impact decisions. Link controls to AI recommendations across CRM and preserve model, policy, reviewer and outcome evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 13"
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
       "impliedBy": "recordPrivacyIncident",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPrivacy",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordPrivacyIncident"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The privacy governance list.",
   "error": "Could not load. Names which read failed and leaves the privacy governance untouched.",
   "emptyFirstRun": "No privacy governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the privacy governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordPrivacyIncident",
    "contract": "marketing-crm",
    "purpose": "Record an incident",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listPrivacy",
    "contract": "marketing-crm",
    "purpose": "Approved AI uses and limits",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-752",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-752"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-753",
  "name": "Compliance Audit Dashboard",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "2",
   "number": "10",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/compliance-audit-dashboard-bo-753",
   "component": "apps/venue-management-web/src/routes/engagement-support/ComplianceAuditDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-744"
   ],
   "exitTo": [
    "BO-744"
   ],
   "transitions": [
    {
     "to": "BO-744",
     "trigger": "Back to Data Governance Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Demonstrate consent and privacy compliance through measurable evidence. Configuration Scope of Work | Version 1.0 13 Report consent coverage and expiry, request volumes and SLA, retention completion, anonymization, deletion and incident trends. Drill down by jurisdiction, business unit, channel, policy, owner and data category. Provide controlled evidence packages, exception logs and audit exports with source references and timestamps. Restrict compliance information appropriately and record every view, export and administrative action. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 14 Board 3 - Audience Segmentation & Personalization Figure 3. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 15",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 13"
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
       "impliedBy": "listPrivacyEvidenceCompliance",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The compliance audit list.",
   "error": "Could not load. Names which read failed and leaves the compliance audit untouched.",
   "emptyFirstRun": "No compliance audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the compliance audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrivacyEvidenceCompliance",
    "contract": "marketing-crm",
    "purpose": "Evidence for an audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-753",
   "workshopBoard": "wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-753"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "decideDuplicateCandidate": {
  "method": "POST",
  "path": "/duplicate-candidates/{candidateId}/decide",
  "contract": "marketing-crm",
  "summary": "Merge, reject or split",
  "permission": "GUEST_MANAGE",
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
  "responds": "DuplicateCandidate"
 },
 "getGuestConsents": {
  "method": "GET",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Read a guest's consent state",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConsentState"
 },
 "getGuestMatchPolicy": {
  "method": "GET",
  "path": "/guest-match-policy",
  "contract": "marketing-crm",
  "summary": "How returning guests are recognised at checkout",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestMatchPolicy"
 },
 "getIdentityResolutionRules": {
  "method": "GET",
  "path": "/identity-resolution-rules",
  "contract": "marketing-crm",
  "summary": "How duplicates are detected and a master is chosen",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "IdentityResolutionRules"
 },
 "listConsentPurposes": {
  "method": "GET",
  "path": "/consent-purposes",
  "contract": "marketing-crm",
  "summary": "Configured consent purposes",
  "permission": "GUEST_VIEW",
  "offlineCapable": true,
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
 "listDataRetentionSettings": {
  "method": "GET",
  "path": "/data-retention-settings",
  "contract": "tenancy",
  "summary": "How long the tenant keeps each class of data",
  "permission": "TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "dataClass",
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
 "listDataSubjectCustomer": {
  "method": "GET",
  "path": "/data-subject-customer",
  "contract": "marketing-crm",
  "summary": "Data Subject / Customer Privacy Request Management",
  "permission": "GUEST_VIEW",
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
    "name": "requestType",
    "in": "query",
    "required": false
   },
   {
    "name": "subjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "jurisdiction",
    "in": "query",
    "required": false
   },
   {
    "name": "slaState",
    "in": "query",
    "required": false
   },
   {
    "name": "ownerPrincipalId",
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
 "listDuplicateCandidates": {
  "method": "GET",
  "path": "/duplicate-candidates",
  "contract": "marketing-crm",
  "summary": "Suspected duplicates awaiting a decision",
  "permission": "GUEST_MANAGE",
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
   },
   {
    "name": "band",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listPrivacy": {
  "method": "GET",
  "path": "/privacy",
  "contract": "marketing-crm",
  "summary": "Privacy Operations Command Center",
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
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "requestType",
    "in": "query",
    "required": false
   },
   {
    "name": "consentPurpose",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "ownerPrincipalId",
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
  "responds": "PrivacyOperationsCommandCenterView"
 },
 "listPrivacyCompliance": {
  "method": "GET",
  "path": "/privacy-compliance",
  "contract": "marketing-crm",
  "summary": "Privacy Analytics & AI Compliance Intelligence",
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
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "consentPurpose",
    "in": "query",
    "required": false
   },
   {
    "name": "segmentId",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "policyVersion",
    "in": "query",
    "required": false
   },
   {
    "name": "language",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "PrivacyAnalyticsAiComplianceIntelligenceView"
 },
 "listPrivacyEvidenceCompliance": {
  "method": "GET",
  "path": "/privacy-evidence-compliance",
  "contract": "marketing-crm",
  "summary": "Privacy Audit, Evidence & Compliance Reporting",
  "permission": "AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "action",
    "in": "query",
    "required": false
   },
   {
    "name": "report",
    "in": "query",
    "required": false
   },
   {
    "name": "subjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "requestId",
    "in": "query",
    "required": false
   },
   {
    "name": "actorPrincipalId",
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
 "mergeGuests": {
  "method": "POST",
  "path": "/guests/merge",
  "contract": "marketing-crm",
  "summary": "Two records, one person",
  "permission": "GUEST_MANAGE",
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
  "responds": "MergeResult"
 },
 "recordConsent": {
  "method": "POST",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Record a consent decision",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RecordConsentRequest",
  "responds": "ConsentState"
 },
 "recordPrivacyIncident": {
  "method": "POST",
  "path": "/privacy-incidents",
  "contract": "marketing-crm",
  "summary": "Log a personal-data breach and start the clock",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "PrivacyIncident",
  "responds": "PrivacyIncident"
 },
 "runDataRetention": {
  "method": "POST",
  "path": "/retention-runs",
  "contract": "marketing-crm",
  "summary": "Preview or execute a retention pass",
  "permission": "GUEST_MANAGE",
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
  "responds": "RetentionRunResult"
 },
 "setCommunicationPreferenceMarketing": {
  "method": "PUT",
  "path": "/communication-preference-marketing",
  "contract": "marketing-crm",
  "summary": "Communication Preference & Marketing Permission Configuration",
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
  "requestBody": "CommunicationPreferenceMarketingPermissionConfiguratInput",
  "responds": "CommunicationPreferenceMarketingPermissionConfiguratView"
 },
 "setConsentPurposes": {
  "method": "PUT",
  "path": "/consent-purposes",
  "contract": "marketing-crm",
  "summary": "Configure consent purposes",
  "permission": "GUEST_MANAGE",
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
  "responds": "ConsentPurposeConfig"
 },
 "setDataDiscoveryAccess": {
  "method": "PUT",
  "path": "/data-discovery-access",
  "contract": "marketing-crm",
  "summary": "Data Discovery, Access, Export & Correction Workspace",
  "permission": "GUEST_VIEW_PII",
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
  "requestBody": "DataDiscoveryAccessExportCorrectionWorkspaceInput",
  "responds": "DataDiscoveryAccessExportCorrectionWorkspaceView"
 },
 "setDataRetentionPolicy": {
  "method": "PUT",
  "path": "/retention-policies",
  "contract": "marketing-crm",
  "summary": "How long guest data is kept, and what happens at expiry",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "DataRetentionPolicy",
  "responds": "DataRetentionPolicy"
 },
 "setDataRetentionSetting": {
  "method": "PUT",
  "path": "/data-retention-settings/{dataClass}",
  "contract": "tenancy",
  "summary": "Set how long the tenant keeps one class of data",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "TenantDataRetentionSetting",
  "responds": "TenantDataRetentionSetting"
 },
 "setGuestMatchPolicy": {
  "method": "PUT",
  "path": "/guest-match-policy",
  "contract": "marketing-crm",
  "summary": "Set how returning guests are recognised",
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
  "requestBody": "GuestMatchPolicy",
  "responds": "GuestMatchPolicy"
 },
 "setIdentityResolutionRules": {
  "method": "PUT",
  "path": "/identity-resolution-rules",
  "contract": "marketing-crm",
  "summary": "Matching weights, thresholds and survivorship",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "IdentityResolutionRules",
  "responds": "IdentityResolutionRules"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CommunicationPreferenceMarketingPermissionConfiguratInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "One communication preference category, as the privacy administrator defines it (pack 17.1.4 Configuration).",
  "required": [
   "categoryCode",
   "name",
   "classification",
   "availableChannels",
   "defaultBehavior",
   "customerEditable"
  ],
  "properties": {
   "categoryCode": {
    "type": "string",
    "maxLength": 60,
    "description": "The natural key, e.g. `orderConfirmation`, `promotions`, `birthdayCampaigns`."
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "description": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "classification": {
    "type": "string",
    "enum": [
     "transactional",
     "marketing"
    ],
    "description": "The pack's critical principle. Decides whether consent is needed at all."
   },
   "communicationType": {
    "type": "string",
    "enum": [
     "orderConfirmation",
     "ticketDelivery",
     "paymentInformation",
     "eventChanges",
     "securityMessages",
     "promotions",
     "newEvents",
     "membershipOffers",
     "loyaltyOffers",
     "birthdayCampaigns",
     "partnerOffers",
     "surveys",
     "other"
    ]
   },
   "consentPurpose": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ConsentPurpose"
     }
    ],
    "nullable": true,
    "description": "Required for `marketing`. The purpose whose consent a send checks first."
   },
   "availableChannels": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "applicableBrandIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Empty means every brand of the tenant."
   },
   "applicableCountries": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{2}$"
    },
    "description": "Empty means every country."
   },
   "customerEditable": {
    "type": "boolean",
    "description": "Whether the guest may change it in the preference centre."
   },
   "defaultBehavior": {
    "type": "string",
    "enum": [
     "on",
     "off"
    ],
    "description": "`off` for every `marketing` category (opt-in)."
   },
   "reconfirmAfterMonths": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Ask the guest again after this long; null never."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "retired"
    ],
    "default": "active"
   }
  }
 },
 "CommunicationPreferenceMarketingPermissionConfiguratView": {
  "x-ticvai-persistence": "marketing.communication_preference_type",
  "description": "A stored communication preference category.",
  "allOf": [
   {
    "$ref": "#/components/schemas/CommunicationPreferenceMarketingPermissionConfiguratInput"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true
     },
     "version": {
      "type": "integer",
      "minimum": 1,
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
   }
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
 "ConsentPurpose": {
  "type": "string",
  "enum": [
   "marketing",
   "personalisation",
   "profiling",
   "thirdPartySharing",
   "aiProcessing",
   "transactional"
  ]
 },
 "ConsentPurposeConfig": {
  "x-ticvai-persistence": "marketing.consent_purpose + marketing.consent_purpose_channel",
  "type": "object",
  "required": [
   "purpose",
   "channels",
   "noticeVersion",
   "isRequiredForService"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "displayName": {
    "type": "string"
   },
   "description": {
    "type": "string"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string",
    "description": "Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"
   },
   "isRequiredForService": {
    "type": "boolean",
    "description": "True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"
   },
   "expiresAfterMonths": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "ConsentSource": {
  "type": "string",
  "enum": [
   "guestApp",
   "website",
   "kiosk",
   "pos",
   "callCentre",
   "import",
   "agentRecorded",
   "cookieBanner",
   "checkout"
  ],
  "description": "`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."
 },
 "ConsentState": {
  "x-ticvai-persistence": "none — projection over consent_record",
  "type": "object",
  "required": [
   "subjectId",
   "purposes"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision",
      "requiresRenewal"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "decision": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "channels": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean",
       "description": "True where the notice has been superseded since consent was given."
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "DataDiscoveryAccessExportCorrectionWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.privacy_export_package",
  "description": "What a privacy user sends for one request (pack 17.2.5 Data Discovery, Export Package, Correction, Review).",
  "required": [
   "requestId"
  ],
  "properties": {
   "requestId": {
    "type": "string",
    "format": "uuid",
    "description": "The privacy request (`setPrivacyRequest`); the natural key."
   },
   "identifiers": {
    "type": "array",
    "description": "Extra identifiers to search by; the request's subject is always included.",
    "items": {
     "type": "object",
     "required": [
      "type",
      "value"
     ],
     "properties": {
      "type": {
       "type": "string",
       "enum": [
        "customerId",
        "email",
        "mobile",
        "membershipId",
        "orderId",
        "participantId",
        "other"
       ]
      },
      "value": {
       "type": "string",
       "maxLength": 200
      }
     }
    }
   },
   "sources": {
    "type": "array",
    "description": "Sources to search; empty means all.",
    "items": {
     "type": "string",
     "enum": [
      "customerProfile",
      "orders",
      "tickets",
      "membership",
      "loyalty",
      "wallet",
      "crm",
      "marketing",
      "paymentReferences",
      "waiverRecords",
      "resourceBookings",
      "eventRegistrations",
      "consentRecords",
      "credentialReferences",
      "connectedApplications"
     ]
    }
   },
   "exportPackage": {
    "type": "object",
    "nullable": true,
    "description": "Present to generate or progress the export package.",
    "properties": {
     "includedSources": {
      "type": "array",
      "items": {
       "type": "string",
       "description": "A value of `sources`."
      }
     },
     "includedCategories": {
      "type": "array",
      "items": {
       "type": "string",
       "maxLength": 80
      }
     },
     "exclusions": {
      "type": "array",
      "items": {
       "type": "string",
       "maxLength": 200
      },
      "description": "Records withheld, each with a reason (e.g. another person's data, a legal hold)."
     },
     "sensitiveFieldHandling": {
      "type": "string",
      "enum": [
       "include",
       "mask",
       "exclude"
      ],
      "default": "mask"
     },
     "format": {
      "type": "string",
      "enum": [
       "json",
       "csv",
       "pdf"
      ],
      "default": "json"
     },
     "language": {
      "type": "string",
      "description": "BCP 47 tag for the cover letter and field labels."
     },
     "passwordProtected": {
      "type": "boolean",
      "default": true
     },
     "expiresAt": {
      "type": "string",
      "format": "date-time"
     },
     "reviewAction": {
      "type": "string",
      "nullable": true,
      "enum": [
       "submitForReview",
       "approve",
       "reject",
       "deliver"
      ],
      "description": "Moves the package through generated -> privacyReview -> approved -> delivered."
     }
    }
   },
   "corrections": {
    "type": "array",
    "description": "Correction requests to route to the system of record.",
    "items": {
     "type": "object",
     "required": [
      "field",
      "proposedValue"
     ],
     "properties": {
      "field": {
       "type": "string",
       "maxLength": 100,
       "description": "e.g. `email`, `dateOfBirth`."
      },
      "proposedValue": {
       "type": "string",
       "maxLength": 500
      },
      "note": {
       "type": "string",
       "maxLength": 500,
       "nullable": true
      }
     }
    }
   }
  }
 },
 "DataDiscoveryAccessExportCorrectionWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.privacy_export_package",
  "description": "One request's discovery results, export package and routed corrections.",
  "required": [
   "requestId",
   "results"
  ],
  "properties": {
   "requestId": {
    "type": "string",
    "format": "uuid"
   },
   "discoveredAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "results": {
    "type": "array",
    "description": "Record counts per source; the records themselves go only into the export package.",
    "items": {
     "type": "object",
     "required": [
      "source",
      "recordCount"
     ],
     "properties": {
      "source": {
       "type": "string",
       "description": "A value of the input's `sources`."
      },
      "systemName": {
       "type": "string",
       "nullable": true
      },
      "recordCount": {
       "type": "integer",
       "minimum": 0
      },
      "searchFailed": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "exportPackage": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "properties": {
     "status": {
      "type": "string",
      "enum": [
       "generating",
       "generated",
       "privacyReview",
       "approved",
       "rejected",
       "delivered",
       "expired"
      ]
     },
     "format": {
      "type": "string",
      "enum": [
       "json",
       "csv",
       "pdf"
      ]
     },
     "generatedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "approvedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "deliveredAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "expiresAt": {
      "type": "string",
      "format": "date-time"
     },
     "assetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The encrypted package in the asset store."
     },
     "dsarRequestId": {
      "type": "string",
      "nullable": true,
      "description": "The cross-region fan-out that assembled it."
     }
    }
   },
   "corrections": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "required": [
      "field",
      "systemOfRecord",
      "status"
     ],
     "properties": {
      "field": {
       "type": "string"
      },
      "systemOfRecord": {
       "type": "string",
       "description": "The owning contract/table, e.g. `pii.subject_contact`."
      },
      "operation": {
       "type": "string",
       "nullable": true,
       "description": "The operation that performs it, e.g. `updateGuestProfile`."
      },
      "status": {
       "type": "string",
       "enum": [
        "routed",
        "applied",
        "rejected",
        "manualActionRequired"
       ]
      },
      "updatedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
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
 "DataRetentionPolicy": {
  "type": "object",
  "x-ticvai-persistence": "marketing.retention_policy",
  "description": "Board 2.8. **The only routine operation that destroys data irrecoverably at scale.**",
  "required": [
   "code"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "dataCategory": {
    "type": "string"
   },
   "jurisdictions": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "guestStatus": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "retainMonths": {
    "type": "integer",
    "description": "At most the tenant's effective `guestProfile` period (tenancy `setDataRetentionSetting`, decided 29 September); a rule may only shorten it."
   },
   "action": {
    "type": "string",
    "enum": [
     "archive",
     "anonymise",
     "pseudonymise",
     "delete"
    ]
   },
   "legalHoldsRespected": {
    "type": "boolean",
    "default": true
   },
   "fraudExceptionMonths": {
    "type": "integer",
    "nullable": true
   },
   "approvalRequired": {
    "type": "boolean",
    "default": true
   },
   "schedule": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "DataSubjectCustomerPrivacyRequestManagementView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.privacy_request",
  "description": "One customer privacy request (pack 17.2.4 Case Information). The case layer over the cross-region `platform.dsar_request` fan-out, which it references when it raises one.",
  "required": [
   "subjectId",
   "requestType",
   "source",
   "requesterRole",
   "jurisdiction"
  ],
  "properties": {
   "requestId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "The person the request is about."
   },
   "requestType": {
    "type": "string",
    "maxLength": 60,
    "description": "A configured request type code (`setPrivacyRequestTypes`), e.g. `access`, `dataExport`, `correction`, `deletion`, `anonymisation`, `restriction`, `objection`, `consentWithdrawal`, `marketingOptOut`."
   },
   "source": {
    "type": "string",
    "enum": [
     "customerPortal",
     "b2c",
     "mobileApp",
     "emailManual",
     "customerService",
     "pos",
     "api"
    ]
   },
   "requesterRole": {
    "type": "string",
    "enum": [
     "self",
     "guardian",
     "authorisedRepresentative"
    ]
   },
   "requesterSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guardian or representative, when not `self`; verified like the subject."
   },
   "jurisdiction": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "description": "Selects the response period configured for this request type."
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "`submittedAt` plus the jurisdiction's configured response period; null when none is configured."
   },
   "deadlineConfigured": {
    "type": "boolean",
    "readOnly": true
   },
   "daysRemaining": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "Negative once overdue; null without a deadline."
   },
   "atRisk": {
    "type": "boolean",
    "readOnly": true,
    "description": "Inside the request type's configured warning window before `dueAt`."
   },
   "slaState": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "onTrack",
     "atRisk",
     "overdue",
     "escalated",
     "noDeadline"
    ]
   },
   "priority": {
    "type": "string",
    "enum": [
     "P1",
     "P2",
     "P3",
     "P4"
    ],
    "default": "P3"
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "verificationMethod": {
    "type": "string",
    "nullable": true,
    "enum": [
     "accountLogin",
     "otp",
     "emailVerification",
     "mobileVerification",
     "idReview",
     "manualVerification"
    ],
    "description": "One of the methods the request type allows."
   },
   "verificationStatus": {
    "type": "string",
    "enum": [
     "notStarted",
     "pending",
     "verified",
     "failed"
    ],
    "default": "notStarted"
   },
   "status": {
    "type": "string",
    "enum": [
     "submitted",
     "inProgress",
     "completed"
    ],
    "default": "submitted",
    "description": "MoM 20 Aug lifecycle."
   },
   "stage": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "description": "The configured workflow step within `inProgress` (a stage code of the request type)."
   },
   "outcome": {
    "type": "string",
    "nullable": true,
    "enum": [
     "fulfilled",
     "partiallyFulfilled",
     "refused",
     "withdrawnByRequester"
    ],
    "description": "Required to complete. `refused` and `partiallyFulfilled` need `outcomeReason`."
   },
   "outcomeReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "escalated": {
    "type": "boolean",
    "default": false
   },
   "dsarRequestId": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The cross-region `DsarRequest.requestId`, when fulfilment fanned out."
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The customer-service case it came in through, if any."
   },
   "notes": {
    "type": "string",
    "maxLength": 4000,
    "nullable": true
   },
   "completedAt": {
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
 "DuplicateCandidate": {
  "type": "object",
  "x-ticvai-persistence": "marketing.duplicate_candidate",
  "x-ticvai-retired-columns": [
   "guest_ids"
  ],
  "description": "Board 2.3. **Rejection is as valuable as merging**, or the same pair returns weekly.",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectIds": {
    "type": "array",
    "description": "The profiles proposed as one person.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "score": {
    "type": "number"
   },
   "band": {
    "type": "string",
    "enum": [
     "match",
     "possibleMatch"
    ]
   },
   "matchedOn": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "field": {
       "type": "string"
      },
      "values": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "recommended": {
       "type": "string",
       "nullable": true
      },
      "confidence": {
       "type": "number",
       "nullable": true
      },
      "provenance": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "linkedRecordCounts": {
    "type": "object",
    "additionalProperties": {
     "type": "integer"
    },
    "description": "Tickets, bookings, memberships, loyalty, wallet, cases, consents, documents — **previewed before anything is committed**, because merging is not reversible in practice.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "merged",
     "rejected",
     "split"
    ]
   },
   "decidedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "GuestMatchPolicy": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_match_policy",
  "description": "How a guest checking out without an account is recognised. One per venue. **The rev 3 Config controls map here unchanged** (decided 29 September, rev 3 DG-1, no change): *Match returning guests by* is `matchBy`; *Guest checkout (code proof)* is the white-label FeatureToggle `guestCheckout`, off by default, with the code proved through `identity` and the match offered by `checkGuestCheckoutMatch` and `decideGuestCheckoutMatch`.\n",
  "required": [
   "matchBy"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "matchBy": {
    "type": "string",
    "enum": [
     "email",
     "mobile",
     "emailOrMobile"
    ],
    "default": "email",
    "description": "The key a returning guest is matched on. Design control: *Match returning guests by*."
   },
   "offerAtCheckout": {
    "type": "boolean",
    "default": true,
    "description": "Whether a verified contact is matched at the payment step. On, a verified match attaches the order automatically (audit R120 (b)). Off means staff merge later only, and `checkGuestCheckoutMatch` skips the lookup entirely (audit R149)."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   }
  }
 },
 "IdentityResolutionRules": {
  "type": "object",
  "x-ticvai-persistence": "marketing.identity_rules",
  "description": "Board 2.2. **Three thresholds, and the middle band is the point.**",
  "properties": {
   "matchers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "field": {
       "type": "string",
       "enum": [
        "email",
        "phone",
        "name",
        "dateOfBirth",
        "membershipNumber",
        "loyaltyNumber",
        "passportNumber",
        "externalId",
        "address"
       ]
      },
      "comparison": {
       "type": "string",
       "enum": [
        "exact",
        "normalised",
        "fuzzy",
        "phonetic"
       ]
      },
      "weight": {
       "type": "number"
      },
      "required": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "matchThreshold": {
    "type": "number"
   },
   "possibleMatchThreshold": {
    "type": "number"
   },
   "survivorship": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "field": {
       "type": "string"
      },
      "rule": {
       "type": "string",
       "enum": [
        "mostRecent",
        "oldest",
        "highestSourcePriority",
        "mostComplete",
        "verifiedFirst",
        "manual"
       ]
      }
     }
    },
    "description": "**Per field, not per record.** The newer record has the better phone number and the older one has the loyalty history.\n"
   },
   "excludedSources": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "jurisdictionRestrictions": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "autoMergeAllowed": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "MergeResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "survivingSubjectId",
   "absorbedSubjectId",
   "transferred"
  ],
  "properties": {
   "survivingSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "absorbedSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "transferred": {
    "type": "object",
    "properties": {
     "orders": {
      "type": "integer"
     },
     "cases": {
      "type": "integer"
     },
     "loyaltyPoints": {
      "type": "integer",
      "description": "The total points moved across every programme. The per-programme outcome is `loyaltyProgrammes`."
     }
    }
   },
   "loyaltyProgrammes": {
    "type": "array",
    "description": "**One entry per loyalty programme either record belonged to (decided 28 September, audit R149).** Points are added and the higher tier is kept, per programme — a single points number cannot say which programme it belongs to.\n",
    "items": {
     "type": "object",
     "required": [
      "programmeId",
      "pointsAdded",
      "resultingPoints"
     ],
     "properties": {
      "programmeId": {
       "type": "string",
       "format": "uuid"
      },
      "pointsAdded": {
       "type": "integer",
       "description": "The absorbed record's balance in this programme, added to the survivor's."
      },
      "resultingPoints": {
       "type": "integer"
      },
      "tierKept": {
       "type": "string",
       "nullable": true,
       "description": "The higher of the two records' tiers in this programme."
      }
     }
    }
   },
   "consentOutcome": {
    "type": "array",
    "description": "Per purpose, the resulting position. Where the two profiles disagreed, the more restrictive position won.\n",
    "items": {
     "type": "object",
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "result": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "wasRestricted": {
       "type": "boolean"
      }
     }
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
 "PrivacyAnalyticsAiComplianceIntelligenceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.consent_record, marketing.privacy_request (new), marketing.privacy_action (new), marketing.retention_policy, marketing.privacy_exception (new), marketing.consent_propagation (new), marketing.tracking_technology",
  "description": "Privacy KPIs for a period (pack 17.2.10). Rates are 0-1 over the period's denominators.",
  "required": [
   "consentRate",
   "withdrawalRate",
   "marketingOptInRate"
  ],
  "properties": {
   "consentRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Granted over presented."
   },
   "withdrawalRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "marketingOptInRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "cookieAcceptanceByCategory": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "category",
      "acceptanceRate"
     ],
     "properties": {
      "category": {
       "type": "string",
       "enum": [
        "functional",
        "analytics",
        "personalisation",
        "marketing",
        "other"
       ]
      },
      "acceptanceRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "privacyRequests": {
    "type": "integer",
    "minimum": 0,
    "description": "Requests submitted in the period."
   },
   "privacyRequestsByType": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "requestType": {
       "type": "string"
      },
      "count": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
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
    "description": "Completed within `dueAt`, over completed requests that had one."
   },
   "deletionCompletionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "retentionComplianceRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true,
    "description": "Records actioned by their due date, over records due."
   },
   "policyAcceptanceRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "guardianConsentCompletionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "privacyExceptions": {
    "type": "integer",
    "minimum": 0
   },
   "consentPropagationFailures": {
    "type": "integer",
    "minimum": 0
   },
   "consentFunnel": {
    "type": "array",
    "description": "In order, each step's count and rate over the first step.",
    "items": {
     "type": "object",
     "required": [
      "step",
      "count"
     ],
     "properties": {
      "step": {
       "type": "string",
       "maxLength": 80,
       "description": "e.g. privacyNoticeDisplayed, marketingConsentPresented, emailOptIn."
      },
      "count": {
       "type": "integer",
       "minimum": 0
      },
      "rate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "riskFindings": {
    "type": "array",
    "description": "AI findings for human investigation; none is acted on automatically.",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "summary"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "trendAnomaly",
        "abandonmentByLanguage",
        "supersededPolicyInUse",
        "configurationMismatch",
        "other"
       ]
      },
      "summary": {
       "type": "string",
       "maxLength": 500
      },
      "severity": {
       "type": "string",
       "enum": [
        "low",
        "medium",
        "high"
       ]
      },
      "detectedAt": {
       "type": "string",
       "format": "date-time"
      },
      "exceptionId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "Set once someone raised an exception from it."
      }
     }
    }
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "PrivacyAuditEvidenceComplianceReportingView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.privacy_audit_event",
  "description": "One privacy audit event (pack 17.2.9 Audit Fields). Append-only; written by the operation that performed the event, never through an API.",
  "required": [
   "eventId",
   "action",
   "occurredAt"
  ],
  "properties": {
   "eventId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "action": {
    "type": "string",
    "enum": [
     "consentGranted",
     "consentWithdrawn",
     "preferenceChanged",
     "policyAccepted",
     "privacyRequestCreated",
     "identityVerified",
     "dataExportGenerated",
     "correctionRequested",
     "deletionApproved",
     "anonymisationExecuted",
     "retentionAction",
     "legalHold",
     "administrativeOverride",
     "configurationChange"
    ]
   },
   "actorType": {
    "type": "string",
    "enum": [
     "customer",
     "guardian",
     "staff",
     "system",
     "ai"
    ]
   },
   "actorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "actorRole": {
    "type": "string",
    "nullable": true,
    "description": "The role the actor held at the time."
   },
   "source": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
   },
   "channel": {
    "type": "string",
    "nullable": true,
    "description": "A `ConsentSource` value or the staff surface it came through."
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "before": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "The changed fields before, masked where the field is sensitive."
   },
   "after": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true
   },
   "reason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "approvalReference": {
    "type": "string",
    "nullable": true,
    "description": "The approval that authorised it (privacy action approval, hold approval, package approval)."
   },
   "relatedRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "relatedCaseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "evidenceReference": {
    "type": "string",
    "nullable": true,
    "description": "e.g. the consent evidence id, the policy version, the export asset id."
   }
  }
 },
 "PrivacyIncident": {
  "type": "object",
  "x-ticvai-persistence": "marketing.privacy_incident",
  "description": "BL-176. **A personal-data breach has a regulator clock**, and UAE PDPL gives 72 hours from discovery. Nothing in the package recorded one.\n**Modelled on the maintenance incident pattern**, because the shape is the same — discovery, assessment, containment, notification, closure — and **the field that matters is the one that starts the clock.**\n",
  "required": [
   "id",
   "discoveredAt",
   "severity",
   "status"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "discoveredAt": {
    "type": "string",
    "format": "date-time",
    "description": "**The clock starts here, not at occurrence.** 72 hours runs from discovery, which is why this is separate from `occurredAt` and why a discovery nobody recorded is a deadline nobody is counting.\n"
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "severity": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "affectedSubjectCount": {
    "type": "integer",
    "nullable": true
   },
   "dataCategories": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "contact",
      "identity",
      "financial",
      "biometric",
      "health",
      "location",
      "behavioural",
      "credentials"
     ]
    }
   },
   "containedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "regulatorNotifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Or a recorded reason for not notifying.** Deciding a breach is not notifiable is a legitimate decision and an undocumented one is indistinguishable from having missed it.\n"
   },
   "subjectsNotifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "notNotifiedRationale": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "assessing",
     "contained",
     "notified",
     "closed"
    ]
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "PrivacyOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.guest_profile, marketing.consent_record, marketing.privacy_request (new), marketing.privacy_action (new), marketing.retention_policy, marketing.privacy_exception (new), marketing.privacy_incident",
  "description": "The privacy operations position for the caller's scope and filters (pack 17.2.1).",
  "required": [
   "totalCustomerPrivacyProfiles",
   "consentHealth",
   "requestQueue"
  ],
  "properties": {
   "totalCustomerPrivacyProfiles": {
    "type": "integer",
    "minimum": 0
   },
   "activeConsentRecords": {
    "type": "integer",
    "minimum": 0
   },
   "withdrawnConsents": {
    "type": "integer",
    "minimum": 0
   },
   "marketingOptIns": {
    "type": "integer",
    "minimum": 0
   },
   "marketingOptOuts": {
    "type": "integer",
    "minimum": 0
   },
   "pendingDataRightsRequests": {
    "type": "integer",
    "minimum": 0,
    "description": "Requests not yet `completed`."
   },
   "overdueRequests": {
    "type": "integer",
    "minimum": 0
   },
   "requestsWithoutDeadline": {
    "type": "integer",
    "minimum": 0,
    "description": "Open requests whose jurisdiction has no configured response period."
   },
   "pendingDeletionActions": {
    "type": "integer",
    "minimum": 0
   },
   "pendingAnonymization": {
    "type": "integer",
    "minimum": 0
   },
   "retentionActionsDue": {
    "type": "integer",
    "minimum": 0,
    "description": "Records inside the 90-day notice window before their retention action (ADR-0047 §6)."
   },
   "consentEvidenceExceptions": {
    "type": "integer",
    "minimum": 0
   },
   "privacyIncidentsExceptions": {
    "type": "integer",
    "minimum": 0,
    "description": "Open privacy exceptions plus open privacy incidents."
   },
   "policyReAcceptancePending": {
    "type": "integer",
    "minimum": 0,
    "description": "Customers whose accepted notice version has been superseded."
   },
   "consentHealth": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "category",
      "granted",
      "withdrawn",
      "declined"
     ],
     "properties": {
      "category": {
       "type": "string",
       "enum": [
        "emailMarketing",
        "smsMarketing",
        "whatsappMarketing",
        "pushMarketing",
        "personalisation",
        "analytics",
        "location",
        "biometrics",
        "other"
       ]
      },
      "otherLabel": {
       "type": "string",
       "nullable": true,
       "description": "The configured purpose name, when `category` is `other`."
      },
      "granted": {
       "type": "integer",
       "minimum": 0
      },
      "withdrawn": {
       "type": "integer",
       "minimum": 0
      },
      "declined": {
       "type": "integer",
       "minimum": 0
      },
      "requiresRenewal": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "requestQueue": {
    "type": "array",
    "description": "Open and recently completed requests by status and configured stage.",
    "items": {
     "type": "object",
     "required": [
      "status",
      "count"
     ],
     "properties": {
      "status": {
       "type": "string",
       "enum": [
        "submitted",
        "inProgress",
        "completed"
       ]
      },
      "stage": {
       "type": "string",
       "nullable": true
      },
      "count": {
       "type": "integer",
       "minimum": 0
      },
      "atRisk": {
       "type": "integer",
       "minimum": 0
      },
      "overdue": {
       "type": "integer",
       "minimum": 0
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
      "count"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "requestsApproachingDeadline",
        "requestsOverdue",
        "requestsWithoutDeadline",
        "supersededNoticeAccepted",
        "withdrawnConsentInMarketingExport",
        "consentPropagationFailed",
        "retentionActionFailed"
       ]
      },
      "count": {
       "type": "integer",
       "minimum": 0
      },
      "detail": {
       "type": "string",
       "maxLength": 300,
       "nullable": true
      }
     }
    }
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "RecordConsentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "purpose",
   "decision",
   "noticeVersion",
   "source",
   "recordedAt"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "decision": {
    "$ref": "#/components/schemas/ConsentDecision"
   },
   "channels": {
    "type": "array",
    "description": "Omit to apply to every channel the purpose covers.",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string"
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "RetentionRunResult": {
  "type": "object",
  "x-ticvai-persistence": "marketing.retention_run",
  "description": "Board 2.8. **Completion evidence is the half that gets forgotten until an audit.**",
  "properties": {
   "runId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-column": "id",
    "description": "The run, stored as `marketing.retention_run`; `PrivacyAction.retentionRunId` points here. Preview runs are stored too, so an executed pass can be compared with what it previewed."
   },
   "policyId": {
    "type": "string",
    "format": "uuid"
   },
   "mode": {
    "type": "string",
    "enum": [
     "preview",
     "execute"
    ]
   },
   "recordsAffected": {
    "type": "integer"
   },
   "byAction": {
    "type": "object",
    "additionalProperties": {
     "type": "integer"
    }
   },
   "heldBack": {
    "type": "integer"
   },
   "heldBackReasons": {
    "type": "object",
    "additionalProperties": {
     "type": "integer"
    }
   },
   "dependencies": {
    "type": "array",
    "x-ticvai-persisted": false,
    "description": "Computed for the response; the executed run's detail is in the evidence asset.",
    "items": {
     "type": "object",
     "properties": {
      "surface": {
       "type": "string"
      },
      "count": {
       "type": "integer"
      },
      "consequence": {
       "type": "string"
      }
     }
    }
   },
   "evidenceAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "TenantDataRetentionClass": {
  "type": "string",
  "description": "**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n",
  "enum": [
   "guestProfile",
   "paymentRecord",
   "financialRecord",
   "auditRecord",
   "approvalRecord",
   "complianceInspection",
   "faceTagBiometric",
   "facePassBiometric",
   "aiPrompts",
   "aiConversations",
   "aiDecisionRecords",
   "aiMetadataIndex"
  ]
 },
 "TenantDataRetentionSetting": {
  "type": "object",
  "x-ticvai-persistence": "tenancy.data_retention_setting",
  "description": "**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n",
  "required": [
   "dataClass"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "dataClass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TenantDataRetentionClass"
     }
    ],
    "x-ticvai-unique": "tenant",
    "description": "One row per class per tenant. On a write it comes from the path; a body value is ignored."
   },
   "retainAmount": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "description": "The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"
   },
   "retainUnit": {
    "type": "string",
    "nullable": true,
    "enum": [
     "days",
     "months",
     "years"
    ],
    "description": "Required with `retainAmount`."
   },
   "followsDataClass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TenantDataRetentionClass"
     }
    ],
    "nullable": true,
    "description": "Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"
   },
   "onExpiry": {
    "type": "string",
    "enum": [
     "archive",
     "anonymise",
     "delete"
    ],
    "default": "archive",
    "description": "ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"
   },
   "anchor": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "createdAt",
     "lastActivity",
     "decidedAt",
     "ticketExpiry"
    ],
    "description": "What the period is counted from. Fixed per class by the platform."
   },
   "effectiveAmount": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The period actually applied, after follows and defaults are resolved."
   },
   "effectiveUnit": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "days",
     "months",
     "years"
    ]
   },
   "isDefault": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "True when the tenant has not set this class and the platform default applies."
   },
   "defaultAmount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false
   },
   "defaultUnit": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "days",
     "months",
     "years"
    ]
   },
   "legalMinimumAmount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "A floor the law sets. A shorter period is refused (`422`)."
   },
   "legalMaximumAmount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."
   },
   "legalLimitUnit": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "days",
     "months",
     "years"
    ]
   },
   "legalBasis": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The law or requirement the limit comes from, e.g. `4.3.4`."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The tenant. Retention is set at tenant scope only."
   }
  }
 },
 "VersioningEffectiveDatesLegalChangeControlView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.form_definition, marketing.waiver_version_control (new), marketing.form_submission and marketing.waiver_signature",
  "description": "One version of one waiver and its change control (pack 11.1.8).",
  "required": [
   "formId",
   "versionNumber",
   "status",
   "createdAt"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "waiverName": {
    "type": "string"
   },
   "versionNumber": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "superseded",
     "retired"
    ],
    "description": "`FormDefinition.status` (states/form-definition.yaml)."
   },
   "lifecycleStatus": {
    "type": "string",
    "enum": [
     "draft",
     "review",
     "pendingApproval",
     "approved",
     "scheduled",
     "published",
     "suspended",
     "expired",
     "archived"
    ]
   },
   "createdByUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "changeReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "legalReviewer": {
    "type": "string",
    "nullable": true,
    "description": "`FormDefinition.legalReviewedBy`."
   },
   "legalReviewedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "approvedByUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedAt": {
    "type": "string",
    "format": "date-time",
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
   "resignRule": {
    "type": "string",
    "enum": [
     "noResign",
     "resignAtNextBooking",
     "resignBeforeNextVisit"
    ],
    "description": "Whether people who signed an earlier version must sign this one."
   },
   "suspended": {
    "type": "boolean",
    "default": false
   },
   "suspensionReason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "signatureCount": {
    "type": "integer",
    "minimum": 0,
    "description": "Signatures taken against this exact version."
   },
   "comparison": {
    "type": "object",
    "nullable": true,
    "description": "Present when `compareWith` is given.",
    "properties": {
     "comparedWithVersion": {
      "type": "integer",
      "minimum": 1
     },
     "addedText": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "blockKey": {
         "type": "string"
        },
        "language": {
         "type": "string"
        },
        "text": {
         "type": "string"
        }
       }
      }
     },
     "removedText": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "blockKey": {
         "type": "string"
        },
        "language": {
         "type": "string"
        },
        "text": {
         "type": "string"
        }
       }
      }
     },
     "changedQuestions": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Field keys added, removed or changed."
     },
     "changedSignatoryRules": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Names of the signatory-rule properties that differ."
     },
     "changedAssociations": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      },
      "description": "Associations added, removed or changed between the two versions' publication."
     }
    }
   }
  }
 }
}
```
