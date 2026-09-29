# WS135 — Marketing CRM Configuration Reference v1.0 board 1

**10 screens · 19 operations · 22 schemas · 8 permissions**

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
  `CASE_VIEW, GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, LEDGER_POST, MARKETING_MANAGE, MARKETING_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-734` | CRM Command Center | listDetail | 2 | 0 | — |
| `BO-735` | Guest Directory | listDetail | 7 | 3 | — |
| `BO-736` | Guest Master Configuration | listDetail | 3 | 0 | — |
| `BO-737` | Customer 360 Profile | listDetail | 2 | 0 | — |
| `BO-738` | Activity Timeline | listDetail | 3 | 0 | — |
| `BO-739` | Contact & Preferences | listDetail | 1 | 0 | — |
| `BO-740` | Family & Guardians | listDetail | 2 | 0 | — |
| `BO-741` | Corporate & Groups | listDetail | 2 | 0 | — |
| `BO-742` | Commerce & Documents | listDetail | 1 | 0 | — |
| `BO-743` | AI Guest Intelligence | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-734, BO-736, BO-737, BO-738, BO-739, BO-740, BO-741, BO-742, BO-743 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-734",
  "name": "CRM Command Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "01",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/crm-command-center-bo-734",
   "component": "apps/venue-management-web/src/routes/engagement-support/CrmCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-735",
    "BO-736",
    "BO-737",
    "BO-738",
    "BO-739",
    "BO-740",
    "BO-741",
    "BO-742",
    "BO-743"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-735",
     "trigger": "Guest Directory",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "subjectId"
     ]
    },
    {
     "to": "BO-736",
     "trigger": "Guest Master Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-737",
     "trigger": "Customer 360 Profile",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-738",
     "trigger": "Activity Timeline",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "subjectId"
     ]
    },
    {
     "to": "BO-739",
     "trigger": "Contact & Preferences",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-740",
     "trigger": "Family & Guardians",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "subjectId"
     ]
    },
    {
     "to": "BO-741",
     "trigger": "Corporate & Groups",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-742",
     "trigger": "Commerce & Documents",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-743",
     "trigger": "AI Guest Intelligence",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give authorized users an operational and analytical overview of the customer base. Display total, new, active, inactive, registered and guest-checkout customers with tenant, brand, venue, region and date filters. Show VIP, high-value, family, corporate, group, churn-risk, duplicate and incomplete-profile indicators. Present LTV, engagement, growth, consent health and source-synchronization trends with drill- down to the underlying guests. Surface explainable AI insights and prioritized actions without bypassing consent, eligibility or access policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 6"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "searchGuests",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run."
      },
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
   "loading": "The crm list.",
   "error": "Could not load. Names which read failed and leaves the crm untouched.",
   "emptyFirstRun": "No crm yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the crm are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchGuests",
    "contract": "marketing-crm",
    "purpose": "Find a guest",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSegments",
    "contract": "marketing-crm",
    "purpose": "Segment indicators",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-734",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-734"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-735",
  "name": "Guest Directory",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "02",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/guest-directory-bo-735",
   "component": "apps/venue-management-web/src/routes/engagement-support/GuestDirectory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-734"
   ],
   "exitTo": [
    "BO-734"
   ],
   "transitions": [
    {
     "to": "BO-734",
     "trigger": "Back to CRM Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a permission-controlled directory for locating and managing every guest record. Search by name, email, mobile, guest ID, external ID, ticket, booking, membership or loyalty identifier. Filter by profile status, segment, language, geography, membership, loyalty tier, wallet, LTV, engagement and churn risk. Support saved views, configurable columns, sorting, pagination, controlled export and auditable bulk actions. Open Customer 360 directly from a result while masking restricted personal or financial data by policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "notes": "**Guest record operations moved here from BO-036 Device Registry on 28 September (audit R254)** — `updateGuestProfile`, `mergeGuestProfiles`, `getGuestLoyalty`, `adjustLoyaltyPoints` and `getConsentHistory`, with their panels and forms. They had been attached to the device registry by module resemblance; managing a guest record is this screen's purpose.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 6"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "searchGuests",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getGuestProfile",
       "notes": "One record, read-only."
      },
      {
       "kind": "detailPanel",
       "label": "The loyalty position",
       "bindsTo": "LoyaltyPosition",
       "columns": [
        "LoyaltyPosition.leaderboardNickname",
        "LoyaltyPosition.subjectId",
        "LoyaltyPosition.programmeId",
        "LoyaltyPosition.pointsBalance",
        "LoyaltyPosition.lifetimePoints",
        "LoyaltyPosition.tierId",
        "LoyaltyPosition.tierCode",
        "LoyaltyPosition.tierName",
        "LoyaltyPosition.pointsToNextTier",
        "LoyaltyPosition.nextExpiryPoints",
        "LoyaltyPosition.nextExpiryAt"
       ],
       "operation": "getGuestLoyalty",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/loyalty"
      },
      {
       "kind": "detailPanel",
       "label": "The consent",
       "bindsTo": "ConsentRecord",
       "columns": [
        "ConsentRecord.purpose",
        "ConsentRecord.decision",
        "ConsentRecord.channels",
        "ConsentRecord.noticeVersion",
        "ConsentRecord.source",
        "ConsentRecord.recordedAt",
        "ConsentRecord.id",
        "ConsentRecord.subjectId",
        "ConsentRecord.recordedByPrincipalId",
        "ConsentRecord.supersededAt"
       ],
       "operation": "getConsentHistory",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/consents/history"
      },
      {
       "kind": "secondaryButton",
       "label": "Adjust loyalty points",
       "operation": "adjustLoyaltyPoints",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/loyalty/adjust"
      },
      {
       "kind": "destructiveButton",
       "label": "Merge guest profiles",
       "operation": "mergeGuestProfiles",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/merge"
      },
      {
       "kind": "secondaryButton",
       "label": "Save guest profile",
       "operation": "updateGuestProfile",
       "provenance": "contract marketing-crm.yaml PATCH /guests/{subjectId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest list.",
   "error": "Could not load. Names which read failed and leaves the guest untouched.",
   "emptyFirstRun": "No guest yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchGuests",
    "contract": "marketing-crm",
    "purpose": "The directory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Open one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "adjustLoyaltyPoints",
    "contract": "marketing-crm",
    "purpose": "Manually adjust points",
    "trigger": "onAction",
    "invalidates": [
     "searchGuests"
    ]
   },
   {
    "operationId": "getConsentHistory",
    "contract": "marketing-crm",
    "purpose": "Full consent history",
    "trigger": "onAction"
   },
   {
    "operationId": "getGuestLoyalty",
    "contract": "marketing-crm",
    "purpose": "A guest's loyalty position",
    "trigger": "onAction"
   },
   {
    "operationId": "mergeGuestProfiles",
    "contract": "marketing-crm",
    "purpose": "Merge a duplicate profile into this one",
    "trigger": "onAction",
    "invalidates": [
     "searchGuests"
    ]
   },
   {
    "operationId": "updateGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Amend a guest profile",
    "trigger": "onAction",
    "invalidates": [
     "searchGuests"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-735",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-735"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "navigation"
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmMergeGuestProfiles",
    "component": "confirmDialog",
    "trigger": "Merge guest profiles",
    "body": "**Names what `mergeGuestProfiles` changes and what it leaves alone**, in the consequence rather than the verb. A guest profile this affects should be identified in the dialog, not just counted. **Collects what `mergeGuestProfiles` sends before it is called.** Required: `duplicateSubjectId`, `reason`.",
    "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/merge"
   },
   {
    "id": "formAdjustLoyaltyPoints",
    "component": "modal",
    "trigger": "Adjust loyalty points",
    "body": "**Collects what `adjustLoyaltyPoints` sends before it is called.** Required: `programmeId`, `points`, `reason`. Optional: `reversedLoyaltyPointsId`, `notes`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AdjustLoyaltyPointsRequest",
    "confirm": {
     "label": "Adjust loyalty points",
     "operation": "adjustLoyaltyPoints"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "programmeId",
      "points",
      "reason",
      "reversedLoyaltyPointsId",
      "notes"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/loyalty/adjust"
   },
   {
    "id": "formUpdateGuestProfile",
    "component": "modal",
    "trigger": "Save guest profile",
    "body": "**Collects what `updateGuestProfile` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `preferredLanguage`, `preferredChannel`, `tags`, `notes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save guest profile",
     "operation": "updateGuestProfile"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "displayName",
      "preferredLanguage",
      "preferredChannel",
      "tags",
      "notes"
     ]
    },
    "provenance": "contract marketing-crm.yaml PATCH /guests/{subjectId}"
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
  "id": "BO-736",
  "name": "Guest Master Configuration",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "03",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/guest-master-configuration-bo-736",
   "component": "apps/venue-management-web/src/routes/engagement-support/GuestMasterConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-734"
   ],
   "exitTo": [
    "BO-734"
   ],
   "transitions": [
    {
     "to": "BO-734",
     "trigger": "Back to CRM Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the shared guest data model without software changes. Configuration Scope of Work | Version 1.0 6 Maintain standard and custom attributes, field groups, labels, data types, defaults, required flags and validation rules. Define primary and external identifiers, source-system priority, survivorship rules and profile- completeness scoring. Configure field visibility and editability by role, tenant, brand, venue, region and jurisdiction. Version and audit schema changes and expose approved attributes consistently through UI, API and events. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 6"
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
       "impliedBy": "setGuestAttributeModel",
       "label": "Save guest attribute model",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setGuestAttributeModel"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest master list.",
   "error": "Could not load. Names which read failed and leaves the guest master untouched.",
   "emptyFirstRun": "No guest master yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest master are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestAttributeModel",
    "contract": "marketing-crm",
    "purpose": "The shared data model",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setGuestAttributeModel",
    "contract": "marketing-crm",
    "purpose": "Change it, as a version",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGuestAttributeModel"
    ]
   },
   {
    "operationId": "setGuestExtraFields",
    "contract": "marketing-crm",
    "purpose": "Define the extra guest fields",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "getGuestAttributeModel"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-736",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-736"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-737",
  "name": "Customer 360 Profile",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "04",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/customer-360-profile-bo-737",
   "component": "apps/venue-management-web/src/routes/engagement-support/Customer360Profile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-734"
   ],
   "exitTo": [
    "BO-734"
   ],
   "transitions": [
    {
     "to": "BO-734",
     "trigger": "Back to CRM Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Present a consolidated, actionable view of one guest. Display identity, contacts, preferences, household, organization, membership, loyalty, wallet, tickets, bookings and visits. Show LTV, engagement, churn risk, communication eligibility, open cases, pending waivers and recent activity. Provide permission-controlled quick actions for communication, booking, case creation, campaign enrollment and profile maintenance. Allow role-based widget configuration while keeping the Customer Master Service as the system of record. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 7"
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
       "impliedBy": "listCustomerServiceProfile",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer 360 profile list.",
   "error": "Could not load. Names which read failed and leaves the customer 360 profile untouched.",
   "emptyFirstRun": "No customer 360 profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer 360 profile are still there. Names the active filter and offers to clear it.",
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
    "operationId": "listCustomerSegmentProfile",
    "contract": "catalogue",
    "purpose": "Customer Segment & Profile Pricing Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-737",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-737"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-738",
  "name": "Activity Timeline",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "05",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/activity-timeline-bo-738",
   "component": "apps/venue-management-web/src/routes/engagement-support/ActivityTimeline.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-734"
   ],
   "exitTo": [
    "BO-734"
   ],
   "transitions": [
    {
     "to": "BO-734",
     "trigger": "Back to CRM Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a chronological record of guest activity across the connected platform. Ingest purchases, ticket usage, reservations, visits, membership changes, loyalty, wallet, campaigns, messages, cases, surveys and waivers. Filter by date, channel, venue, event type, source system and outcome and open the related source transaction. Distinguish operational facts from user notes and AI-derived events and preserve event timestamps and source identifiers. Support reliable ordering, pagination and audit evidence without allowing historical events to be silently altered. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 7"
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
       "impliedBy": "getGuestProfile",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The activity timeline list.",
   "error": "Could not load. Names which read failed and leaves the activity timeline untouched.",
   "emptyFirstRun": "No activity timeline yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the activity timeline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "The consolidated record",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getGuestIntelligence",
    "contract": "marketing-crm",
    "purpose": "Value, engagement and risk",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getGuestRelationships",
    "contract": "marketing-crm",
    "purpose": "Household and organisation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-738",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-738"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "guestId",
     "from": "navigation"
    },
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
  "id": "BO-739",
  "name": "Contact & Preferences",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "06",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/contact-preferences-bo-739",
   "component": "apps/venue-management-web/src/routes/engagement-support/ContactPreferences.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-734"
   ],
   "exitTo": [
    "BO-734"
   ],
   "transitions": [
    {
     "to": "BO-734",
     "trigger": "Back to CRM Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain verified contact information and service preferences for each guest. Manage multiple email addresses, phone numbers, physical addresses, emergency contacts and social identifiers. Record preferred language, channel, contact time, frequency, interests, favorite attractions and visit preferences. Store accessibility and dietary requirements with suitable sensitivity and role restrictions. Configuration Scope of Work | Version 1.0 7 Show verification, suppression and consent status while delegating legal enforcement to the shared Consent Service. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 7"
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
       "impliedBy": "getGuestTimeline",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The contact preferences list.",
   "error": "Could not load. Names which read failed and leaves the contact preferences untouched.",
   "emptyFirstRun": "No contact preferences yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the contact preferences are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestTimeline",
    "contract": "marketing-crm",
    "purpose": "Everything they did, in order",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-739",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-739"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
  "id": "BO-740",
  "name": "Family & Guardians",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "07",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/family-guardians-bo-740",
   "component": "apps/venue-management-web/src/routes/engagement-support/FamilyGuardians.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-734"
   ],
   "exitTo": [
    "BO-734"
   ],
   "transitions": [
    {
     "to": "BO-734",
     "trigger": "Back to CRM Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Model households, dependants and guardians while preserving each person's individual identity. Create family groups and link parent, guardian, spouse and dependant relationships with effective dates. Configure purchasing, booking, profile-management and waiver-signing authority for minors and dependants. Support shared or separate benefits, memberships, bookings and communications without merging individual profiles. Record additions, removals, authority changes and exceptions in a complete relationship audit trail. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 8"
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
       "impliedBy": "updateGuestPreferences",
       "label": "Save guest preferences",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getGuestProfile",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateGuestPreferences"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The family guardians list.",
   "error": "Could not load. Names which read failed and leaves the family guardians untouched.",
   "emptyFirstRun": "No family guardians yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the family guardians are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateGuestPreferences",
    "contract": "marketing-crm",
    "purpose": "Contact and service preferences",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGuestConsents"
    ]
   },
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Verified contacts",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-740",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-740"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-741",
  "name": "Corporate & Groups",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "08",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/corporate-groups-bo-741",
   "component": "apps/venue-management-web/src/routes/engagement-support/CorporateGroups.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-734"
   ],
   "exitTo": [
    "BO-734"
   ],
   "transitions": [
    {
     "to": "BO-734",
     "trigger": "Back to CRM Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Link guests to corporate, school, travel and group structures. Support corporate accounts, schools, tour operators, travel agencies, resellers, clubs, teams and event groups. Define contacts, participant roles, billing relationships, booking authority and relationship validity periods. Display associated bookings, memberships, agreements and activity while respecting organizational access boundaries. Expose relationships to B2B, reservations, cases and reporting through secured services and APIs. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 8"
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
       "impliedBy": "getGuestRelationships",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setGuestRelationships",
       "label": "Save guest relationships",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setGuestRelationships"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The corporate groups list.",
   "error": "Could not load. Names which read failed and leaves the corporate groups untouched.",
   "emptyFirstRun": "No corporate groups yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the corporate groups are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestRelationships",
    "contract": "marketing-crm",
    "purpose": "Family and guardians",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setGuestRelationships",
    "contract": "marketing-crm",
    "purpose": "Link without merging",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGuestRelationships",
     "getGuestProfile"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-741",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-741"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
  "id": "BO-742",
  "name": "Commerce & Documents",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "09",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/commerce-documents-bo-742",
   "component": "apps/venue-management-web/src/routes/engagement-support/CommerceDocuments.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-734"
   ],
   "exitTo": [
    "BO-734"
   ],
   "transitions": [
    {
     "to": "BO-734",
     "trigger": "Back to CRM Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Consolidate the guest's commercial, service and document history. Provide tabs for tickets, reservations, memberships, loyalty, wallet, refunds, exchanges, transfers, upgrades and attendance. Display communications, cases, survey responses, ratings, reviews, waivers, identification documents and signed agreements. Link every item to its source transaction and show status, value, channel, venue, timestamps and authorized actions. Apply RBAC/PBAC, masking, retention, download and audit policies to financial, identity and legal records. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 8",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 8"
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
       "impliedBy": "setGuestRelationships",
       "label": "Save guest relationships",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setGuestRelationships"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commerce documents list.",
   "error": "Could not load. Names which read failed and leaves the commerce documents untouched.",
   "emptyFirstRun": "No commerce documents yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commerce documents are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGuestRelationships",
    "contract": "marketing-crm",
    "purpose": "Corporate, school and group links",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGuestRelationships",
     "getGuestProfile"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-742",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-742"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
  "id": "BO-743",
  "name": "AI Guest Intelligence",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "1",
   "number": "10",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/ai-guest-intelligence-bo-743",
   "component": "apps/venue-management-web/src/routes/engagement-support/AiGuestIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-734"
   ],
   "exitTo": [
    "BO-734"
   ],
   "transitions": [
    {
     "to": "BO-734",
     "trigger": "Back to CRM Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Turn the unified record into explainable customer insight and recommended actions. Calculate historical and predicted LTV, engagement, churn, inactivity, cancellation, affinity and upgrade propensity. Classify audiences and recommend the next campaign, offer, product, membership, reward, channel and next best action. Display contributing factors, confidence, model/version, expected impact and policy or data limitations. Require consent and eligibility checks, support accept/reject/feedback actions and audit all human and AI decisions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 9 Board 2 - Identity Resolution, Consent & Data Privacy Figure 2. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 10",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 9"
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
       "impliedBy": "getGuestTimeline",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "uploadGuestDocument",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "uploadGuestDocument"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest intelligence list.",
   "error": "Could not load. Names which read failed and leaves the guest intelligence untouched.",
   "emptyFirstRun": "No guest intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestTimeline",
    "contract": "marketing-crm",
    "purpose": "Commercial and document history",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "uploadGuestDocument",
    "contract": "marketing-crm",
    "purpose": "Attach a document",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-743",
   "workshopBoard": "wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-743"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "adjustLoyaltyPoints": {
  "method": "POST",
  "path": "/guests/{subjectId}/loyalty/adjust",
  "contract": "marketing-crm",
  "summary": "Manually adjust points",
  "permission": "LEDGER_POST",
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
  "requestBody": "AdjustLoyaltyPointsRequest",
  "responds": "LoyaltyAdjustmentResult"
 },
 "getConsentHistory": {
  "method": "GET",
  "path": "/guests/{subjectId}/consents/history",
  "contract": "marketing-crm",
  "summary": "Full consent history",
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
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "getGuestAttributeModel": {
  "method": "GET",
  "path": "/guest-attribute-model",
  "contract": "marketing-crm",
  "summary": "The shared guest data model",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestAttributeModel"
 },
 "getGuestIntelligence": {
  "method": "GET",
  "path": "/guests/{guestId}/intelligence",
  "contract": "marketing-crm",
  "summary": "Value, engagement, churn and propensity, with their reasons",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestIntelligence"
 },
 "getGuestLoyalty": {
  "method": "GET",
  "path": "/guests/{subjectId}/loyalty",
  "contract": "marketing-crm",
  "summary": "A guest's loyalty position",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "programmeId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "LoyaltyPosition"
 },
 "getGuestProfile": {
  "method": "GET",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Read a guest profile",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestProfileDetail"
 },
 "getGuestRelationships": {
  "method": "GET",
  "path": "/guests/{guestId}/relationships",
  "contract": "marketing-crm",
  "summary": "Household, guardians, corporate and group links",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestRelationship"
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
 "listCustomerSegmentProfile": {
  "method": "GET",
  "path": "/customer-segment-profile",
  "contract": "catalogue",
  "summary": "Customer Segment & Profile Pricing Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "dimension",
    "in": "query",
    "required": false
   },
   {
    "name": "segmentSource",
    "in": "query",
    "required": false
   },
   {
    "name": "customerId",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
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
 "mergeGuestProfiles": {
  "method": "POST",
  "path": "/guests/{subjectId}/merge",
  "contract": "marketing-crm",
  "summary": "Merge a duplicate profile into this one",
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
  "requestBody": null,
  "responds": "MergeResult"
 },
 "searchGuests": {
  "method": "GET",
  "path": "/guests",
  "contract": "marketing-crm",
  "summary": "Search guest profiles",
  "permission": "GUEST_VIEW",
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
    "name": "segmentId",
    "in": "query",
    "required": null
   },
   {
    "name": "hasConsentFor",
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
 "setGuestAttributeModel": {
  "method": "PUT",
  "path": "/guest-attribute-model",
  "contract": "marketing-crm",
  "summary": "Change the model, as a version",
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
  "requestBody": "GuestAttributeModel",
  "responds": "GuestAttributeModel"
 },
 "setGuestExtraFields": {
  "method": "PUT",
  "path": "/guest-extra-fields",
  "contract": "marketing-crm",
  "summary": "Define the extra guest fields",
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
  "requestBody": "GuestExtraFieldDefinition",
  "responds": "GuestExtraFieldDefinition"
 },
 "setGuestRelationships": {
  "method": "PUT",
  "path": "/guests/{guestId}/relationships",
  "contract": "marketing-crm",
  "summary": "Link people without merging them",
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
  "requestBody": null,
  "responds": "GuestRelationship"
 },
 "updateGuestPreferences": {
  "method": "PUT",
  "path": "/guests/{subjectId}/preferences",
  "contract": "marketing-crm",
  "summary": "The things a regular should not have to say twice",
  "permission": "GUEST_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GuestPreferences",
  "responds": "GuestPreferences"
 },
 "updateGuestProfile": {
  "method": "PATCH",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Amend a guest profile",
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
  "requestBody": null,
  "responds": "GuestProfileDetail"
 },
 "uploadGuestDocument": {
  "method": "POST",
  "path": "/guest-documents",
  "contract": "marketing-crm",
  "summary": "Store a guest photo, ID or signed document",
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
  "requestBody": "GuestDocument",
  "responds": "GuestDocument"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AdjustLoyaltyPointsRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — writes marketing.loyalty_points",
  "description": "**A correction is a new entry, never an edit.** Reversing an entry writes a row pointing at it through `reversedLoyaltyPointsId`; granting goodwill writes a row with no reversal target. Either way the movement has a reason and an author, and the history stays walkable.\n",
  "required": [
   "programmeId",
   "points",
   "reason"
  ],
  "properties": {
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "points": {
    "type": "integer",
    "description": "Signed. Negative removes points, and the balance may not go below zero."
   },
   "reason": {
    "type": "string",
    "description": "**Goodwill, correction or expiry reversal, and nothing else (decided 28 September, audit R149).** A service-recovery grant is `goodwill`, a fraud or migration fix is `correction`, and returning points that expired in error is `expiryReversal`. None of them moves the tier or `lifetimePoints`.\n",
    "enum": [
     "goodwill",
     "correction",
     "expiryReversal"
    ]
   },
   "reversedLoyaltyPointsId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The entry this reverses, when it is a reversal. **Set it and the sign is checked against the original** — a reversal that does not cancel what it names is a second grant wearing a correction's label.\n"
   },
   "notes": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   }
  }
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
 "GuestAttributeModel": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_attribute_model",
  "description": "Board 1.3. **Visibility by jurisdiction is what makes this a model and not a form.**",
  "properties": {
   "version": {
    "type": "integer"
   },
   "fieldGroups": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "displayOrder": {
       "type": "integer"
      }
     }
    }
   },
   "attributes": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "groupCode": {
       "type": "string"
      },
      "dataType": {
       "type": "string"
      },
      "standard": {
       "type": "boolean",
       "default": false
      },
      "mandatory": {
       "type": "boolean",
       "default": false
      },
      "defaultValue": {
       "nullable": true
      },
      "allowedValues": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "validationExpression": {
       "type": "string",
       "nullable": true
      },
      "sensitive": {
       "type": "boolean",
       "default": false
      },
      "visibleToRoles": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "editableByRoles": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "lawfulInJurisdictions": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "**Empty means everywhere.** A nationality field lawful in one jurisdiction and not another cannot be a column somebody ships.\n"
      },
      "countsTowardCompleteness": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "identifiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "primary": {
       "type": "boolean",
       "default": false
      },
      "sourceSystem": {
       "type": "string",
       "nullable": true
      },
      "sourcePriority": {
       "type": "integer"
      }
     }
    }
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "GuestDocument": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_document",
  "description": "BL-133. **No store for guest photos, avatars, IDs or signed documents anywhere.**\nDeliberately separate from `assets`, which holds a tenant's media library. **A guest's passport scan is not a marketing asset** — it has a different retention clock, a different access rule and a different reason to exist, and putting it in the same store means one careless query returns both.\n",
  "required": [
   "id",
   "subjectId",
   "kind",
   "storageRef",
   "retainUntil"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "avatar",
     "idDocument",
     "visa",
     "signedWaiver",
     "medicalNote",
     "accessibilityEvidence",
     "photo",
     "other"
    ]
   },
   "storageRef": {
    "type": "string",
    "description": "**The stored object's key in the guest-document store**, which is deliberately not `assets` (BL-133). No operation in this contract issues one yet: `assets` `createUpload` is staff-only and writes the media library, so the upload step for this store is still to be designed.\n"
   },
   "contentType": {
    "type": "string"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid"
   },
   "retainUntil": {
    "type": "string",
    "format": "date",
    "description": "**Required, not optional.** A guest document with no deletion date is a guest document kept forever, and the retention question is the one CF-64 is open on.\n**Kept until its purpose ends, then for the period client counsel sets (decided 28 September, audit R149).** The caller sets `retainUntil` to the end of the purpose (the visit, the waiver's validity, the visa's expiry) plus that period. **The period per `kind` is an open value**: until counsel names it, it is zero, so the document is deleted when the purpose ends.\n"
   },
   "uploadedAt": {
    "readOnly": true,
    "type": "string",
    "format": "date-time"
   },
   "uploadedByPrincipalId": {
    "readOnly": true,
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "GuestExtraFieldDefinition": {
  "type": "object",
  "x-ticvai-persistence": "none — composed from a field and its options",
  "description": "**A select with no options is not a field**, so the options come back with the definition rather than from a second call.\n",
  "required": [
   "field"
  ],
  "properties": {
   "field": {
    "$ref": "#/components/schemas/MarketingGuestExtraField"
   },
   "options": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MarketingGuestExtraOption"
    }
   }
  }
 },
 "GuestIntelligence": {
  "type": "object",
  "description": "Board 1.10. **Explainable, or an agent will ignore it or over-trust it.**",
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "scores": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "historicalLtv",
        "predictedLtv",
        "engagement",
        "churnRisk",
        "inactivityRisk",
        "cancellationRisk",
        "upgradePropensity",
        "nextPurchasePropensity"
       ]
      },
      "value": {
       "type": "number"
      },
      "band": {
       "type": "string",
       "nullable": true
      },
      "confidence": {
       "type": "number",
       "nullable": true
      },
      "modelId": {
       "type": "string",
       "nullable": true
      },
      "modelVersion": {
       "type": "string",
       "nullable": true
      },
      "computedAt": {
       "type": "string",
       "format": "date-time"
      },
      "factors": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "factor": {
          "type": "string"
         },
         "contribution": {
          "type": "number"
         }
        }
       }
      },
      "limitations": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "**Policy and data limitations travel with the score**, so the rule that prediction never overrides consent cannot be forgotten downstream.\n"
      }
     }
    }
   },
   "affinities": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "productCategoryId": {
       "type": "string",
       "format": "uuid"
      },
      "label": {
       "type": "string"
      },
      "strength": {
       "type": "number"
      }
     }
    }
   },
   "nextBestActions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "action": {
       "type": "string"
      },
      "expectedImpact": {
       "type": "string",
       "nullable": true
      },
      "confidence": {
       "type": "number",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "GuestPreferences": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_preference",
  "description": "**What the guest likes, kept apart from what they permit** (consent) and from who they are (the profile). One row per subject. `dietary` and `accessibility` are here rather than as tags because BL-134 gives them their own consent purpose and retention.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "seatingPreference": {
    "type": "string",
    "nullable": true,
    "maxLength": 200
   },
   "drinkPreferences": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "dietary": {
    "type": "array",
    "description": "Also written by `updateMyProfile`.",
    "items": {
     "type": "string"
    }
   },
   "accessibility": {
    "type": "array",
    "description": "Also written by `updateMyProfile`.",
    "items": {
     "type": "string"
    }
   },
   "preferredChannel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "x-ticvai-persisted": false,
    "description": "**Stored on the profile** (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest.\n"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "GuestProfile": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "type": "object",
  "required": [
   "subjectId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "nullable": true
   },
   "phone": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "preferredChannel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells. Marketing acts locally."
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "engagementScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"
   },
   "engagementTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "new",
     "active",
     "occasional",
     "lapsing",
     "lapsed",
     "dormant"
    ],
    "description": "5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"
   },
   "lifetimeValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "visitCount": {
    "type": "integer"
   },
   "lastVisitAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "mergedIntoSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"
   },
   "mergedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "GuestProfileDetail": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "allOf": [
   {
    "$ref": "#/components/schemas/GuestProfile"
   },
   {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
     },
     "consents": {
      "$ref": "#/components/schemas/ConsentState"
     },
     "loyalty": {
      "$ref": "#/components/schemas/LoyaltyPosition"
     },
     "openCaseCount": {
      "type": "integer"
     },
     "recentOrderIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "membershipIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "notes": {
      "type": "string",
      "nullable": true
     }
    }
   }
  ]
 },
 "GuestRelationship": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_relationship",
  "x-ticvai-retired-columns": [
   "related_guest_id"
  ],
  "description": "Boards 1.7 and 1.8. **Links people without merging them**, which is the whole design.\n",
  "required": [
   "relatedSubjectId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "relatedSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "parent",
     "guardian",
     "spouse",
     "dependant",
     "householdMember",
     "employee",
     "student",
     "groupLeader",
     "travelAgent",
     "reseller"
    ]
   },
   "authorities": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "purchaseFor",
      "bookFor",
      "manageProfile",
      "signWaiver",
      "viewHistory",
      "receiveCommunications"
     ]
    },
    "description": "**Four different permissions, not one relationship.** A guardianship granting all of them forever survives the child becoming an adult.\n"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "sharedBenefits": {
    "type": "boolean",
    "default": false
   },
   "verifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
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
 "LoyaltyAdjustmentResult": {
  "type": "object",
  "x-ticvai-persistence": "none — composed from the entry posted and the resulting position",
  "description": "**Both halves of an adjustment, because returning only the balance is the defect decision 8 named.** Until 20 September this operation moved `marketing.loyalty_position` and returned it, and posted nothing to `marketing.loyalty_points` — so a manual adjustment was the one movement in the system that could not be walked back to a reason.\n",
  "required": [
   "entry",
   "position"
  ],
  "properties": {
   "entry": {
    "$ref": "#/components/schemas/MarketingLoyaltyPoints"
   },
   "position": {
    "$ref": "#/components/schemas/LoyaltyPosition"
   }
  }
 },
 "LoyaltyPosition": {
  "x-ticvai-persistence": "marketing.loyalty_position",
  "type": "object",
  "required": [
   "subjectId",
   "programmeId",
   "pointsBalance",
   "tierCode"
  ],
  "properties": {
   "leaderboardNickname": {
    "type": "string",
    "nullable": true,
    "maxLength": 24,
    "description": "BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "lifetimePoints": {
    "type": "integer"
   },
   "tierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "pointsToNextTier": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryPoints": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MarketingGuestExtraField": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_extra_field",
  "description": "**Taken from the backend workbook, 20 September.** NEW TABLE. Defines an extra field that Admin wants to add to the customer form, such as Date of Birth, Emergency Contact, or Jersey Size.",
  "required": [
   "tenantId",
   "name",
   "type",
   "isRequired",
   "displayOrder",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "type": {
    "type": "string",
    "maxLength": 30
   },
   "isRequired": {
    "type": "boolean"
   },
   "displayOrder": {
    "type": "integer"
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MarketingGuestExtraOption": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_extra_option",
  "description": "**Taken from the backend workbook, 20 September.** NEW TABLE. Stores dropdown choices only when an extra field uses SELECT type, for example Language = English, Hindi, Marathi.",
  "required": [
   "fieldId",
   "name",
   "displayOrder",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "fieldId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "displayOrder": {
    "type": "integer"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "MarketingLoyaltyPoints": {
  "type": "object",
  "x-ticvai-persistence": "marketing.loyalty_points",
  "description": "**Taken from the backend workbook, 20 September.** Stores every loyalty point earn, redeem, expire, adjustment, or reversal transaction for a customer.",
  "required": [
   "programId",
   "customerId",
   "transactionType",
   "points",
   "balanceAfter",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "programId": {
    "type": "string",
    "format": "uuid"
   },
   "customerId": {
    "type": "string",
    "format": "uuid"
   },
   "transactionType": {
    "type": "string",
    "maxLength": 30
   },
   "points": {
    "type": "number"
   },
   "balanceAfter": {
    "type": "number"
   },
   "sourceType": {
    "type": "string",
    "maxLength": 50,
    "nullable": true
   },
   "sourceReferenceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "reversedLoyaltyPointsId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "notes": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "description": "For a manual movement, `AdjustLoyaltyPointsRequest.reason`. Null for an accrual, a redemption or an expiry, whose `transactionType` and source already say why. The three manual types are the only ones (audit R149).",
    "enum": [
     "goodwill",
     "correction",
     "expiryReversal"
    ]
   },
   "authorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who posted a manual movement. Null where the platform posted it."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
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
 }
}
```
