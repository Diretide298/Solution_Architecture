# WS42 — Privacy  Consent   Preference Management board 2

**10 screens · 10 operations · 12 schemas · 2 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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
| `CMS-031` | Privacy Operations Command Center | listDetail | 1 | 0 | — |
| `CMS-032` | Customer Privacy, Consent & Preference 360° | listDetail | 1 | 0 | — |
| `CMS-033` | Consent Evidence, History & Withdrawal Management | listDetail | 1 | 0 | — |
| `CMS-034` | Data Subject / Customer Privacy Request Management | listDetail | 1 | 0 | — |
| `CMS-035` | Data Discovery, Access, Export & Correction Workspace | listDetail | 1 | 0 | — |
| `CMS-036` | Deletion, Anonymization & Restriction Operations | listDetail | 1 | 2 | — |
| `CMS-037` | Data Retention, Expiry & Legal Hold Operations | listDetail | 1 | 2 | — |
| `CMS-038` | Privacy Compliance, Exception & Investigation Workspace | listDetail | 1 | 0 | — |
| `CMS-039` | Privacy Audit, Evidence & Compliance Reporting | configEditor | 1 | 0 | — |
| `CMS-040` | Privacy Analytics & AI Compliance Intelligence | listDetail | 1 | 0 | — |

## Thin screens in this batch

**CMS-032, CMS-033, CMS-035, CMS-036 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-031",
  "name": "Privacy Operations Command Center",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.1",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/privacy-operations-command-center-cms-031",
   "component": "apps/venue-management-web/src/routes/policy/PrivacyOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-032",
    "CMS-033",
    "CMS-034",
    "CMS-035",
    "CMS-036",
    "CMS-037",
    "CMS-038",
    "CMS-039",
    "CMS-040"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-032",
     "trigger": "Works in Customer Privacy, Consent & Preference 360°",
     "provenance": "flow F151 step 1→2",
     "operation": "listPrivacy"
    },
    {
     "to": "CMS-033",
     "trigger": "Works in Consent Evidence, History & Withdrawal Management",
     "provenance": "flow F151 step 3→4",
     "operation": "listPrivacy"
    },
    {
     "to": "CMS-034",
     "trigger": "Works in Data Subject / Customer Privacy Request Management",
     "provenance": "flow F151 step 5→6",
     "operation": "listPrivacy"
    },
    {
     "to": "CMS-035",
     "trigger": "Works in Data Discovery, Access, Export & Correction Workspace",
     "provenance": "flow F151 step 7→8",
     "operation": "listPrivacy"
    },
    {
     "to": "CMS-036",
     "trigger": "Works in Deletion, Anonymization & Restriction Operations",
     "provenance": "flow F151 step 9→10",
     "operation": "listPrivacy"
    },
    {
     "to": "CMS-037",
     "trigger": "Works in Data Retention, Expiry & Legal Hold Operations",
     "provenance": "flow F151 step 11→12",
     "operation": "listPrivacy"
    },
    {
     "to": "CMS-038",
     "trigger": "Works in Privacy Compliance, Exception & Investigation Workspace",
     "provenance": "flow F151 step 13→14",
     "operation": "listPrivacy"
    },
    {
     "to": "CMS-039",
     "trigger": "Works in Privacy Audit, Evidence & Compliance Reporting",
     "provenance": "flow F151 step 15→16",
     "operation": "listPrivacy"
    },
    {
     "to": "CMS-040",
     "trigger": "Works in Privacy Analytics & AI Compliance Intelligence",
     "provenance": "flow F151 step 17→18",
     "operation": "listPrivacy"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide Privacy, Compliance and authorized operational teams with a centralized real-time overview of privacy operations across TICVAI.",
  "purposeNote": "Authorized users can understand the current operational privacy position and identify actions requiring attention from one command center.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search privacy operations",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 21 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Brand",
        "Country",
        "Customer",
        "Request Type",
        "Consent Purpose",
        "Channel",
        "Status",
        "Risk",
        "Date",
        "Owner"
       ],
       "notes": "The pack filters this screen by tenant, brand, country, customer, request type, consent purpose and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 21 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every privacy operations",
       "columns": [
        "PrivacyOperationsCommandCenterView.totalCustomerPrivacyProfiles",
        "PrivacyOperationsCommandCenterView.activeConsentRecords",
        "PrivacyOperationsCommandCenterView.withdrawnConsents",
        "PrivacyOperationsCommandCenterView.marketingOptIns",
        "PrivacyOperationsCommandCenterView.marketingOptOuts",
        "PrivacyOperationsCommandCenterView.pendingDataRightsRequests",
        "PrivacyOperationsCommandCenterView.overdueRequests",
        "PrivacyOperationsCommandCenterView.pendingDeletionActions",
        "PrivacyOperationsCommandCenterView.pendingAnonymization",
        "PrivacyOperationsCommandCenterView.retentionActionsDue",
        "PrivacyOperationsCommandCenterView.consentEvidenceExceptions",
        "PrivacyOperationsCommandCenterView.privacyIncidentsExceptions",
        "PrivacyOperationsCommandCenterView.policyReAcceptancePending"
       ],
       "bindsTo": "PrivacyOperationsCommandCenterView",
       "operation": "listPrivacy",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 21 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected privacy operations",
       "bindsTo": "PrivacyOperationsCommandCenterView",
       "columns": [
        "PrivacyOperationsCommandCenterView.totalCustomerPrivacyProfiles",
        "PrivacyOperationsCommandCenterView.activeConsentRecords",
        "PrivacyOperationsCommandCenterView.withdrawnConsents",
        "PrivacyOperationsCommandCenterView.marketingOptIns",
        "PrivacyOperationsCommandCenterView.marketingOptOuts",
        "PrivacyOperationsCommandCenterView.pendingDataRightsRequests",
        "PrivacyOperationsCommandCenterView.overdueRequests",
        "PrivacyOperationsCommandCenterView.pendingDeletionActions",
        "PrivacyOperationsCommandCenterView.pendingAnonymization",
        "PrivacyOperationsCommandCenterView.retentionActionsDue",
        "PrivacyOperationsCommandCenterView.consentEvidenceExceptions",
        "PrivacyOperationsCommandCenterView.privacyIncidentsExceptions",
        "PrivacyOperationsCommandCenterView.policyReAcceptancePending"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Show breakdown by”, “Provide visibility into”.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 21 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Search Customer, Open Privacy Profile, Create Privacy Request, Review Withdrawal, Run Retention, Investigate Evidence, Export Compliance Report. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 21 §Authorized users may"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The privacy operations list.",
   "error": "Could not load. Names which read failed and leaves the privacy operations untouched.",
   "emptyFirstRun": "No privacy operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the privacy operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrivacy",
    "contract": "marketing-crm",
    "purpose": "Privacy Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PrivacyOperationsCommandCenterView.totalCustomerPrivacyProfiles",
    "PrivacyOperationsCommandCenterView.activeConsentRecords",
    "PrivacyOperationsCommandCenterView.withdrawnConsents",
    "PrivacyOperationsCommandCenterView.marketingOptIns",
    "PrivacyOperationsCommandCenterView.marketingOptOuts",
    "PrivacyOperationsCommandCenterView.pendingDataRightsRequests"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-031"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 21. 13 of 24 labels bound to a contract property; 31 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-032",
  "name": "Customer Privacy, Consent & Preference 360°",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.2",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/customer-privacy-consent-preference-360-cms-032",
   "component": "apps/venue-management-web/src/routes/policy/CustomerPrivacyConsentPreference360.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-031"
   ],
   "exitTo": [
    "CMS-031"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-031, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-031",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F151 step 2→3",
     "operation": "listCustomerPrivacyConsent"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide one authoritative privacy view for an individual customer or participant. This becomes the privacy equivalent of the customer 360° workspace. n ed el",
  "purposeNote": "An authorized user can reconstruct the customer's complete privacy relationship with TICVAI from one governed workspace.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every customer privacy consent",
       "columns": [
        "CustomerPrivacyConsentPreference360View.privacyPolicyVersion",
        "CustomerPrivacyConsentPreference360View.cookieNoticeVersion",
        "CustomerPrivacyConsentPreference360View.biometricNotice",
        "CustomerPrivacyConsentPreference360View.childrenSPrivacyNotice",
        "CustomerPrivacyConsentPreference360View.otherApplicablePrivacyDocuments"
       ],
       "bindsTo": "CustomerPrivacyConsentPreference360View",
       "operation": "listCustomerPrivacyConsent",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 22 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer privacy consent",
       "bindsTo": "CustomerPrivacyConsentPreference360View",
       "columns": [
        "CustomerPrivacyConsentPreference360View.privacyPolicyVersion",
        "CustomerPrivacyConsentPreference360View.cookieNoticeVersion",
        "CustomerPrivacyConsentPreference360View.biometricNotice",
        "CustomerPrivacyConsentPreference360View.childrenSPrivacyNotice",
        "CustomerPrivacyConsentPreference360View.otherApplicablePrivacyDocuments"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Display appropriate information such as”, “Email Consente”, “SMS Withdraw”, “Consente”, “Personalizatio”, “Show current”.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 22 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer privacy consent list.",
   "error": "Could not load. Names which read failed and leaves the customer privacy consent untouched.",
   "emptyFirstRun": "No customer privacy consent yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer privacy consent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerPrivacyConsent",
    "contract": "marketing-crm",
    "purpose": "Customer Privacy, Consent & Preference 360°",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CustomerPrivacyConsentPreference360View.privacyPolicyVersion",
    "CustomerPrivacyConsentPreference360View.cookieNoticeVersion",
    "CustomerPrivacyConsentPreference360View.biometricNotice",
    "CustomerPrivacyConsentPreference360View.childrenSPrivacyNotice",
    "CustomerPrivacyConsentPreference360View.otherApplicablePrivacyDocuments"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-032"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 22. 5 of 5 labels bound to a contract property; 5 of 50 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-033",
  "name": "Consent Evidence, History & Withdrawal Management",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.3",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/consent-evidence-history-withdrawal-management-cms-033",
   "component": "apps/venue-management-web/src/routes/policy/ConsentEvidenceHistoryWithdrawalManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-031"
   ],
   "exitTo": [
    "CMS-031"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-031, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-031",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F151 step 4→5",
     "operation": "listConsentEvidenceWithdrawal"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Maintain legally and operationally useful evidence of every consent event and manage subsequent withdrawals.",
  "purposeNote": "current privacy state and propagate to dependent systems.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every consent evidence history",
       "columns": [
        "ConsentEvidenceHistoryWithdrawalManagementView.requested",
        "ConsentEvidenceHistoryWithdrawalManagementView.processed",
        "ConsentEvidenceHistoryWithdrawalManagementView.propagated",
        "ConsentEvidenceHistoryWithdrawalManagementView.acknowledged",
        "ConsentEvidenceHistoryWithdrawalManagementView.failed",
        "Retry Required"
       ],
       "bindsTo": "ConsentEvidenceHistoryWithdrawalManagementView",
       "operation": "listConsentEvidenceWithdrawal",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 24 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected consent evidence history",
       "bindsTo": "ConsentEvidenceHistoryWithdrawalManagementView",
       "columns": [
        "ConsentEvidenceHistoryWithdrawalManagementView.requested",
        "ConsentEvidenceHistoryWithdrawalManagementView.processed",
        "ConsentEvidenceHistoryWithdrawalManagementView.propagated",
        "ConsentEvidenceHistoryWithdrawalManagementView.acknowledged",
        "ConsentEvidenceHistoryWithdrawalManagementView.failed",
        "Retry Required"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Consent Evidence Record”, “Evidence Principle”, “Withdrawal”, “Central Consent Engine”.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 24 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The consent evidence history list.",
   "error": "Could not load. Names which read failed and leaves the consent evidence history untouched.",
   "emptyFirstRun": "No consent evidence history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the consent evidence history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConsentEvidenceWithdrawal",
    "contract": "marketing-crm",
    "purpose": "Consent Evidence, History & Withdrawal Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ConsentEvidenceHistoryWithdrawalManagementView.requested",
    "ConsentEvidenceHistoryWithdrawalManagementView.processed",
    "ConsentEvidenceHistoryWithdrawalManagementView.propagated",
    "ConsentEvidenceHistoryWithdrawalManagementView.acknowledged",
    "ConsentEvidenceHistoryWithdrawalManagementView.failed",
    "Retry Required"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-033"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 24. 5 of 6 labels bound to a contract property; 6 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-034",
  "name": "Data Subject / Customer Privacy Request Management",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.4",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/data-subject-customer-privacy-request-management-cms-034",
   "component": "apps/venue-management-web/src/routes/policy/DataSubjectCustomerPrivacyRequestManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-031"
   ],
   "exitTo": [
    "CMS-031"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-031, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-031",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F151 step 6→7",
     "operation": "listDataSubjectCustomer"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide a governed case-management workflow for customer privacy requests.",
  "purposeNote": "Every customer privacy request can be received, verified, assigned, tracked and completed through a governed case workflow.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: ID Review where permitted. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Support"
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
       "label": "Every data subject customer",
       "columns": [
        "DataSubjectCustomerPrivacyRequestManagementView.daysRemaining",
        "DataSubjectCustomerPrivacyRequestManagementView.atRisk",
        "Overdue",
        "Escalated"
       ],
       "bindsTo": "DataSubjectCustomerPrivacyRequestManagementView",
       "operation": "listDataSubjectCustomer",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected data subject customer",
       "bindsTo": "DataSubjectCustomerPrivacyRequestManagementView",
       "columns": [
        "DataSubjectCustomerPrivacyRequestManagementView.daysRemaining",
        "DataSubjectCustomerPrivacyRequestManagementView.atRisk",
        "Overdue",
        "Escalated"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Configurable request types may include”, “Guardian / Representative”.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Customer Portal",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Service",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "ID Review where permitted",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Support configurable methods such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data subject customer list.",
   "error": "Could not load. Names which read failed and leaves the data subject customer untouched.",
   "emptyFirstRun": "No data subject customer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data subject customer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDataSubjectCustomer",
    "contract": "marketing-crm",
    "purpose": "Data Subject / Customer Privacy Request Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DataSubjectCustomerPrivacyRequestManagementView.daysRemaining",
    "DataSubjectCustomerPrivacyRequestManagementView.atRisk",
    "Overdue",
    "Escalated"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-034"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 26. 2 of 4 labels bound to a contract property; 20 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-035",
  "name": "Data Discovery, Access, Export & Correction Workspace",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.5",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/data-discovery-access-export-correction-workspace-cms-035",
   "component": "apps/venue-management-web/src/routes/policy/DataDiscoveryAccessExportCorrectionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-031"
   ],
   "exitTo": [
    "CMS-031"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-031, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-031",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F151 step 8→9",
     "operation": "setDataDiscoveryAccess"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow authorized privacy teams to locate customer data across TICVAI and connected systems when fulfilling access, export or correction requests.",
  "purposeNote": "Authorized teams can discover applicable customer data, prepare a controlled access/export response and route correction to the authoritative data owner.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every data discovery access",
       "columns": [
        "DataDiscoveryAccessExportCorrectionWorkspaceView.ticketing82Records",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.orders26Records",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.membership1Record",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.crm14Records",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.consent17Records"
       ],
       "bindsTo": "DataDiscoveryAccessExportCorrectionWorkspaceView",
       "operation": "setDataDiscoveryAccess",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 28 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected data discovery access",
       "bindsTo": "DataDiscoveryAccessExportCorrectionWorkspaceView",
       "columns": [
        "DataDiscoveryAccessExportCorrectionWorkspaceView.ticketing82Records",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.orders26Records",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.membership1Record",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.crm14Records",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.consent17Records"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Search using”, “Potential sources”, “Export Package”, “Correction”, “Before release”.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 28 §Show"
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
       "provenance": "contract operation setDataDiscoveryAccess"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data discovery access list.",
   "error": "Could not load. Names which read failed and leaves the data discovery access untouched.",
   "emptyFirstRun": "No data discovery access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data discovery access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDataDiscoveryAccess",
    "contract": "marketing-crm",
    "purpose": "Data Discovery, Access, Export & Correction Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setDataDiscoveryAccess"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "DataDiscoveryAccessExportCorrectionWorkspaceView.ticketing82Records",
    "DataDiscoveryAccessExportCorrectionWorkspaceView.orders26Records",
    "DataDiscoveryAccessExportCorrectionWorkspaceView.membership1Record",
    "DataDiscoveryAccessExportCorrectionWorkspaceView.crm14Records",
    "DataDiscoveryAccessExportCorrectionWorkspaceView.consent17Records"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-035"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 28. 5 of 5 labels bound to a contract property; 13 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-036",
  "name": "Deletion, Anonymization & Restriction Operations",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.6",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/deletion-anonymization-restriction-operations-cms-036",
   "component": "apps/venue-management-web/src/routes/policy/DeletionAnonymizationRestrictionOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-031"
   ],
   "exitTo": [
    "CMS-031"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-031, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-031",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F151 step 10→11",
     "operation": "listDeletionAnonymizationRestriction"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern privacy requests or policies requiring personal data to be deleted, anonymized or restricted. This screen requires strong controls because deletion may affect financial, ticketing, fraud, legal and operational records.",
  "purposeNote": "are legitimately configured for retention and provides evidence of the result.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Delete, Remove Biometric Reference. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 29 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 29"
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
       "kind": "destructiveButton",
       "label": "Delete",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove Biometric Reference",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 29 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDelete",
    "component": "confirmDialog",
    "trigger": "Delete",
    "body": "**Delete on a deletion anonymization restriction is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 29 §Support"
   },
   {
    "id": "confirmRemoveBiometricReference",
    "component": "confirmDialog",
    "trigger": "Remove Biometric Reference",
    "body": "**Remove Biometric Reference on a deletion anonymization restriction is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 29 §Support"
   }
  ],
  "states": {
   "loading": "The deletion anonymization restriction list.",
   "error": "Could not load. Names which read failed and leaves the deletion anonymization restriction untouched.",
   "emptyFirstRun": "No deletion anonymization restriction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deletion anonymization restriction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDeletionAnonymizationRestriction",
    "contract": "marketing-crm",
    "purpose": "Deletion, Anonymization & Restriction Operations",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DeletionAnonymizationRestrictionOperationsView.anonymize",
    "DeletionAnonymizationRestrictionOperationsView.pseudonymizeWhereConfigured",
    "DeletionAnonymizationRestrictionOperationsView.restrictProcessing",
    "DeletionAnonymizationRestrictionOperationsView.suppressMarketing",
    "DeletionAnonymizationRestrictionOperationsView.disconnectThirdPartyProfile"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-036"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 2 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-037",
  "name": "Data Retention, Expiry & Legal Hold Operations",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.7",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/data-retention-expiry-legal-hold-operations-cms-037",
   "component": "apps/venue-management-web/src/routes/policy/DataRetentionExpiryLegalHoldOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-031"
   ],
   "exitTo": [
    "CMS-031"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-031, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-031",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F151 step 12→13",
     "operation": "listDataRetentionExpiry"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Operationalize retention policies associated with Board 1 processing purposes and data categories.",
  "purposeNote": "preserving controlled holds, approvals and complete processing evidence.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Review, Delete, Archive, Place Hold, Release Hold. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Support"
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
       "label": "Every data retention expiry",
       "columns": [
        "DataRetentionExpiryLegalHoldOperationsView.recordsApproachingExpiry",
        "DataRetentionExpiryLegalHoldOperationsView.eligibleForDeletion",
        "DataRetentionExpiryLegalHoldOperationsView.eligibleForAnonymization",
        "DataRetentionExpiryLegalHoldOperationsView.underLegalHold",
        "DataRetentionExpiryLegalHoldOperationsView.processingFailures",
        "DataRetentionExpiryLegalHoldOperationsView.retentionExceptions"
       ],
       "bindsTo": "DataRetentionExpiryLegalHoldOperationsView",
       "operation": "listDataRetentionExpiry",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected data retention expiry",
       "bindsTo": "DataRetentionExpiryLegalHoldOperationsView",
       "columns": [
        "DataRetentionExpiryLegalHoldOperationsView.recordsApproachingExpiry",
        "DataRetentionExpiryLegalHoldOperationsView.eligibleForDeletion",
        "DataRetentionExpiryLegalHoldOperationsView.eligibleForAnonymization",
        "DataRetentionExpiryLegalHoldOperationsView.underLegalHold",
        "DataRetentionExpiryLegalHoldOperationsView.processingFailures",
        "DataRetentionExpiryLegalHoldOperationsView.retentionExceptions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Hold information includes”, “Retention jobs may run”, “Dry Run”.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Review",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Archive",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Place Hold",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Release Hold",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Support"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDelete",
    "component": "confirmDialog",
    "trigger": "Delete",
    "body": "**Delete on a data retention expiry is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Support"
   },
   {
    "id": "confirmArchive",
    "component": "confirmDialog",
    "trigger": "Archive",
    "body": "**Archive on a data retention expiry is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 30 §Support"
   }
  ],
  "states": {
   "loading": "The data retention expiry list.",
   "error": "Could not load. Names which read failed and leaves the data retention expiry untouched.",
   "emptyFirstRun": "No data retention expiry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data retention expiry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDataRetentionExpiry",
    "contract": "marketing-crm",
    "purpose": "Data Retention, Expiry & Legal Hold Operations",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DataRetentionExpiryLegalHoldOperationsView.recordsApproachingExpiry",
    "DataRetentionExpiryLegalHoldOperationsView.eligibleForDeletion",
    "DataRetentionExpiryLegalHoldOperationsView.eligibleForAnonymization",
    "DataRetentionExpiryLegalHoldOperationsView.underLegalHold",
    "DataRetentionExpiryLegalHoldOperationsView.processingFailures",
    "DataRetentionExpiryLegalHoldOperationsView.retentionExceptions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-037"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 30. 6 of 6 labels bound to a contract property; 14 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-038",
  "name": "Privacy Compliance, Exception & Investigation Workspace",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.8",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/privacy-compliance-exception-investigation-workspace-cms-038",
   "component": "apps/venue-management-web/src/routes/policy/PrivacyComplianceExceptionInvestigationWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-031"
   ],
   "exitTo": [
    "CMS-031"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-031, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-031",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F151 step 14→15",
     "operation": "setPrivacyComplianceException"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a centralized workspace for privacy configuration and operational exceptions requiring investigation.",
  "purposeNote": "Privacy-related exceptions can be centrally investigated, assigned, resolved and audited.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Security, Data Owner. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 32 §Allow escalation to appropriate"
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
       "label": "Every privacy compliance exception",
       "columns": [
        "PrivacyComplianceExceptionInvestigationWorkspaceView.severity",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.exception",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.customer",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.system",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.brand",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.country",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.detectedAt",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.owner",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.sla",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.status"
       ],
       "bindsTo": "PrivacyComplianceExceptionInvestigationWorkspaceView",
       "operation": "setPrivacyComplianceException",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 32 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected privacy compliance exception",
       "bindsTo": "PrivacyComplianceExceptionInvestigationWorkspaceView",
       "columns": [
        "PrivacyComplianceExceptionInvestigationWorkspaceView.severity",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.exception",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.customer",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.system",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.brand",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.country",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.detectedAt",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.owner",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.sla",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Provide”, “Workflow”, “Important Boundary”.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 32 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Security",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 32 §Allow escalation to appropriate"
      },
      {
       "kind": "secondaryButton",
       "label": "Data Owner",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 32 §Allow escalation to appropriate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The privacy compliance exception list.",
   "error": "Could not load. Names which read failed and leaves the privacy compliance exception untouched.",
   "emptyFirstRun": "No privacy compliance exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the privacy compliance exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPrivacyComplianceException",
    "contract": "marketing-crm",
    "purpose": "Privacy Compliance, Exception & Investigation Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setPrivacyComplianceException"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PrivacyComplianceExceptionInvestigationWorkspaceView.severity",
    "PrivacyComplianceExceptionInvestigationWorkspaceView.exception",
    "PrivacyComplianceExceptionInvestigationWorkspaceView.customer",
    "PrivacyComplianceExceptionInvestigationWorkspaceView.system",
    "PrivacyComplianceExceptionInvestigationWorkspaceView.brand",
    "PrivacyComplianceExceptionInvestigationWorkspaceView.country"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-038"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 32. 10 of 10 labels bound to a contract property; 12 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-039",
  "name": "Privacy Audit, Evidence & Compliance Reporting",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.9",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/privacy-audit-evidence-compliance-reporting-cms-039",
   "component": "apps/venue-management-web/src/routes/policy/PrivacyAuditEvidenceComplianceReporting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-031"
   ],
   "exitTo": [
    "CMS-031"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-031, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-031",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F151 step 16→17",
     "operation": "listPrivacyEvidenceCompliance"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture significant activities such as) and no display directory — it is settings, not a population",
  "purpose": "Provide immutable auditability and management/compliance reporting across privacy operations.",
  "purposeNote": "performed it, what rule/version applied and what evidence supports it.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Consent Granted",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Consent Withdrawn",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Preference Changed",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Policy Accepted",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Privacy Request Created",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Identity Verified",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Data Export Generated",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Correction Requested",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Deletion Approved",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Anonymization Executed",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Retention Action",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Legal Hold",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Administrative Override",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      },
      {
       "kind": "selectField",
       "label": "Configuration Change",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 33 §Capture significant activities such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The privacy audit evidence configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the privacy audit evidence untouched.",
   "emptyFirstRun": "No privacy audit evidence configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrivacyEvidenceCompliance",
    "contract": "marketing-crm",
    "purpose": "Privacy Audit, Evidence & Compliance Reporting",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-039"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 33. 0 of 0 labels bound to a contract property; 14 of 57 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-040",
  "name": "Privacy Analytics & AI Compliance Intelligence",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "2",
   "number": "17.2.10",
   "page": 35
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/privacy-analytics-ai-compliance-intelligence-cms-040",
   "component": "apps/venue-management-web/src/routes/policy/PrivacyAnalyticsAiComplianceIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-031"
   ],
   "exitTo": [
    "CMS-031"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-031, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Provide executives, Privacy Officers and Compliance teams with actionable privacy analytics and AI-assisted risk detection. This should be the intelligence layer across both Privacy Boards.",
  "purposeNote": "resolve compliance risks while keeping legally significant decisions under governed human control. Board 2 — Final Screen Register # Backend Screen Core Responsibility 17.2. Privacy Operations Command Center Overall privacy operations 1 17.2. Customer Privacy, Consent & Preference Complete customer privacy 2 360° view 17.2. Consent Evidence, History & Withdrawal Consent evidence and 3 Management withdrawal 17.2. Data Subject / Customer Privacy Request",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search privacy analytics compliance",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 35 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Brand",
        "Country",
        "Venue",
        "Channel",
        "Consent Purpose",
        "Customer Segment",
        "Product",
        "Policy Version",
        "Language",
        "Time Period"
       ],
       "notes": "The pack filters this screen by tenant, brand, country, venue, channel, consent purpose and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 35 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every privacy analytics compliance",
       "columns": [
        "PrivacyAnalyticsAiComplianceIntelligenceView.consentRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.withdrawalRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.marketingOptInRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.cookieAcceptanceByCategory",
        "PrivacyAnalyticsAiComplianceIntelligenceView.privacyRequests",
        "PrivacyAnalyticsAiComplianceIntelligenceView.averageResolutionTime",
        "PrivacyAnalyticsAiComplianceIntelligenceView.slaCompliance",
        "PrivacyAnalyticsAiComplianceIntelligenceView.deletionCompletionRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.retentionCompliance",
        "PrivacyAnalyticsAiComplianceIntelligenceView.policyAcceptance",
        "PrivacyAnalyticsAiComplianceIntelligenceView.guardianConsentCompletion",
        "PrivacyAnalyticsAiComplianceIntelligenceView.privacyExceptions",
        "PrivacyAnalyticsAiComplianceIntelligenceView.consentPropagationFailures"
       ],
       "bindsTo": "PrivacyAnalyticsAiComplianceIntelligenceView",
       "operation": "listPrivacyCompliance",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 35 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected privacy analytics compliance",
       "bindsTo": "PrivacyAnalyticsAiComplianceIntelligenceView",
       "columns": [
        "PrivacyAnalyticsAiComplianceIntelligenceView.consentRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.withdrawalRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.marketingOptInRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.cookieAcceptanceByCategory",
        "PrivacyAnalyticsAiComplianceIntelligenceView.privacyRequests",
        "PrivacyAnalyticsAiComplianceIntelligenceView.averageResolutionTime",
        "PrivacyAnalyticsAiComplianceIntelligenceView.slaCompliance",
        "PrivacyAnalyticsAiComplianceIntelligenceView.deletionCompletionRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.retentionCompliance",
        "PrivacyAnalyticsAiComplianceIntelligenceView.policyAcceptance",
        "PrivacyAnalyticsAiComplianceIntelligenceView.guardianConsentCompletion",
        "PrivacyAnalyticsAiComplianceIntelligenceView.privacyExceptions",
        "PrivacyAnalyticsAiComplianceIntelligenceView.consentPropagationFailures"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Privacy request cases”, “Locate/export/correct data”, “Final Area 17 Architecture”, “Compliance”.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 35 §Analyze"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** “Show overdue deletion requests.”, “Show minors with incomplete guardian privacy consent.”. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 35 §Authorized users may ask"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The privacy analytics compliance list.",
   "error": "Could not load. Names which read failed and leaves the privacy analytics compliance untouched.",
   "emptyFirstRun": "No privacy analytics compliance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the privacy analytics compliance are still there. The pack's own statuses are 7 Operations — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrivacyCompliance",
    "contract": "marketing-crm",
    "purpose": "Privacy Analytics & AI Compliance Intelligence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PrivacyAnalyticsAiComplianceIntelligenceView.consentRate",
    "PrivacyAnalyticsAiComplianceIntelligenceView.withdrawalRate",
    "PrivacyAnalyticsAiComplianceIntelligenceView.marketingOptInRate",
    "PrivacyAnalyticsAiComplianceIntelligenceView.cookieAcceptanceByCategory",
    "PrivacyAnalyticsAiComplianceIntelligenceView.privacyRequests",
    "PrivacyAnalyticsAiComplianceIntelligenceView.averageResolutionTime"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-040"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 35. 13 of 24 labels bound to a contract property; 31 of 107 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
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
 "listConsentEvidenceWithdrawal": {
  "method": "GET",
  "path": "/consent-evidence-withdrawal",
  "contract": "marketing-crm",
  "summary": "Consent Evidence, History & Withdrawal Management",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConsentEvidenceHistoryWithdrawalManagementView"
 },
 "listCustomerPrivacyConsent": {
  "method": "GET",
  "path": "/customer-privacy-consent",
  "contract": "marketing-crm",
  "summary": "Customer Privacy, Consent & Preference 360°",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CustomerPrivacyConsentPreference360View"
 },
 "listDataRetentionExpiry": {
  "method": "GET",
  "path": "/data-retention-expiry",
  "contract": "marketing-crm",
  "summary": "Data Retention, Expiry & Legal Hold Operations",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DataRetentionExpiryLegalHoldOperationsView"
 },
 "listDataSubjectCustomer": {
  "method": "GET",
  "path": "/data-subject-customer",
  "contract": "marketing-crm",
  "summary": "Data Subject / Customer Privacy Request Management",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DataSubjectCustomerPrivacyRequestManagementView"
 },
 "listDeletionAnonymizationRestriction": {
  "method": "GET",
  "path": "/deletion-anonymization-restriction",
  "contract": "marketing-crm",
  "summary": "Deletion, Anonymization & Restriction Operations",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DeletionAnonymizationRestrictionOperationsView"
 },
 "listPrivacy": {
  "method": "GET",
  "path": "/privacy",
  "contract": "marketing-crm",
  "summary": "Privacy Operations Command Center",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "tenant",
    "in": "query",
    "required": false
   },
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "customer",
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
    "name": "status",
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
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "tenant",
    "in": "query",
    "required": false
   },
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
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
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
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
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PrivacyAuditEvidenceComplianceReportingView"
 },
 "setDataDiscoveryAccess": {
  "method": "PUT",
  "path": "/data-discovery-access",
  "contract": "marketing-crm",
  "summary": "Data Discovery, Access, Export & Correction Workspace",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "DataDiscoveryAccessExportCorrectionWorkspaceInput",
  "responds": "DataDiscoveryAccessExportCorrectionWorkspaceView"
 },
 "setPrivacyComplianceException": {
  "method": "PUT",
  "path": "/privacy-compliance-exception",
  "contract": "marketing-crm",
  "summary": "Privacy Compliance, Exception & Investigation Workspace",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PrivacyComplianceExceptionInvestigationWorkspaceInput",
  "responds": "PrivacyComplianceExceptionInvestigationWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ConsentEvidenceHistoryWithdrawalManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Consent Evidence, History & Withdrawal Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "evidenceId": {
    "type": "string",
    "description": "Evidence ID"
   },
   "customerParticipant": {
    "type": "string",
    "description": "Customer / Participant"
   },
   "consentPurpose": {
    "type": "string",
    "description": "Consent Purpose"
   },
   "consentVersion": {
    "type": "string",
    "description": "Consent Version"
   },
   "exactApplicableWordingVersionReference": {
    "type": "string",
    "description": "Exact applicable wording/version reference"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "journeyCapturePoint": {
    "type": "string",
    "description": "Journey/Capture Point"
   },
   "userCustomerActor": {
    "type": "string",
    "description": "User/Customer Actor"
   },
   "sourceSystem": {
    "type": "string",
    "description": "Source System"
   },
   "deviceSessionReferenceWherePermitted": {
    "type": "string",
    "description": "Device/session reference where permitted"
   },
   "guardianReferenceWhereApplicable": {
    "type": "string",
    "description": "Guardian reference where applicable"
   },
   "yesterdaySHistoricalConsentEvidenceRemains": {
    "type": "string",
    "description": "Yesterday's historical consent evidence remains"
   },
   "customerPortal": {
    "type": "string",
    "description": "Customer Portal"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "preferenceCenter": {
    "type": "string",
    "description": "Preference Center"
   },
   "customerService": {
    "type": "string",
    "description": "Customer Service"
   },
   "authorizedStaff": {
    "type": "string",
    "description": "Authorized Staff"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "requested": {
    "type": "string",
    "description": "Requested"
   },
   "processed": {
    "type": "string",
    "description": "Processed"
   },
   "propagated": {
    "type": "string",
    "description": "Propagated"
   },
   "acknowledged": {
    "type": "string",
    "description": "Acknowledged"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   }
  }
 },
 "CustomerPrivacyConsentPreference360View": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Customer Privacy, Consent & Preference 360° displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "customerId": {
    "type": "string",
    "description": "Customer ID"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "account": {
    "type": "string",
    "description": "Account"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "preferredLanguage": {
    "type": "string",
    "description": "Preferred Language"
   },
   "ageCategory": {
    "type": "string",
    "description": "Age Category"
   },
   "guardianRelationshipWhereApplicable": {
    "type": "string",
    "description": "Guardian Relationship where applicable"
   },
   "accountStatus": {
    "type": "integer",
    "description": "Account Status"
   },
   "privacyRiskExceptionIndicator": {
    "type": "string",
    "description": "Privacy Risk/Exception indicator"
   },
   "v3212AugB2c": {
    "type": "string",
    "description": "v3.2 12 Aug B2C"
   },
   "v2820AugPortal": {
    "type": "string",
    "description": "v2.8 20 Aug Portal"
   },
   "whatsappV2112AugApp": {
    "type": "string",
    "description": "WhatsApp v2.1 12 Aug App"
   },
   "biometricsV4015AugApp": {
    "type": "string",
    "description": "Biometrics v4.0 15 Aug App"
   },
   "declinedV1412AugB2c": {
    "type": "string",
    "description": "Declined v1.4 12 Aug B2C"
   },
   "emailPreference": {
    "type": "string",
    "description": "Email preference"
   },
   "smsPreference": {
    "type": "string",
    "description": "SMS preference"
   },
   "whatsappPreference": {
    "type": "string",
    "description": "WhatsApp preference"
   },
   "pushPreference": {
    "type": "string",
    "description": "Push preference"
   },
   "brandPreferences": {
    "type": "integer",
    "description": "Brand preferences"
   },
   "marketingCategories": {
    "type": "integer",
    "description": "Marketing categories"
   },
   "personalizationPreferences": {
    "type": "integer",
    "description": "Personalization preferences"
   },
   "privacyPolicyVersion": {
    "type": "string",
    "description": "Privacy Policy Version"
   },
   "cookieNoticeVersion": {
    "type": "string",
    "description": "Cookie Notice Version"
   },
   "biometricNotice": {
    "type": "string",
    "description": "Biometric Notice"
   },
   "childrenSPrivacyNotice": {
    "type": "string",
    "description": "Children's Privacy Notice"
   },
   "otherApplicablePrivacyDocuments": {
    "type": "string",
    "description": "Other applicable privacy documents"
   },
   "choices": {
    "type": "string",
    "description": "choices"
   },
   "access": {
    "type": "string",
    "description": "Access"
   },
   "correction": {
    "type": "string",
    "description": "Correction"
   },
   "deletion": {
    "type": "string",
    "description": "Deletion"
   },
   "restriction": {
    "type": "string",
    "description": "Restriction"
   },
   "objection": {
    "type": "string",
    "description": "Objection"
   },
   "otherConfiguredRequests": {
    "type": "integer",
    "description": "Other configured requests"
   },
   "informationExists": {
    "type": "string",
    "description": "information exists"
   }
  }
 },
 "DataDiscoveryAccessExportCorrectionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is marketing.guest_profile at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Data Discovery, Access, Export & Correction Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "customerProfile": {
    "type": "string",
    "description": "Customer Profile"
   },
   "orders": {
    "type": "string",
    "description": "Orders"
   },
   "tickets": {
    "type": "string",
    "description": "Tickets"
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
   "crm": {
    "type": "string",
    "description": "CRM"
   },
   "marketing": {
    "type": "string",
    "description": "Marketing"
   },
   "paymentsReferences": {
    "type": "string",
    "description": "Payments references"
   },
   "waiverRecords": {
    "type": "string",
    "description": "Waiver records"
   },
   "resourceBookings": {
    "type": "string",
    "description": "Resource bookings"
   },
   "eventRegistrations": {
    "type": "string",
    "description": "Event registrations"
   },
   "consentRecords": {
    "type": "string",
    "description": "Consent records"
   },
   "credentialReferences": {
    "type": "string",
    "description": "Credential references"
   },
   "connectedApplications": {
    "type": "string",
    "description": "Connected applications"
   },
   "includedSystems": {
    "type": "string",
    "description": "Included systems"
   },
   "includedCategories": {
    "type": "string",
    "description": "Included categories"
   },
   "exclusions": {
    "type": "string",
    "description": "Exclusions"
   },
   "sensitiveFieldHandling": {
    "type": "string",
    "description": "Sensitive-field handling"
   },
   "format": {
    "type": "string",
    "description": "Format"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "encryptionSecurity": {
    "type": "string",
    "description": "Encryption/security"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   }
  }
 },
 "DataDiscoveryAccessExportCorrectionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Data Discovery, Access, Export & Correction Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "customerProfile": {
    "type": "string",
    "description": "Customer Profile"
   },
   "orders": {
    "type": "string",
    "description": "Orders"
   },
   "tickets": {
    "type": "string",
    "description": "Tickets"
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
   "crm": {
    "type": "string",
    "description": "CRM"
   },
   "marketing": {
    "type": "string",
    "description": "Marketing"
   },
   "paymentsReferences": {
    "type": "string",
    "description": "Payments references"
   },
   "waiverRecords": {
    "type": "string",
    "description": "Waiver records"
   },
   "resourceBookings": {
    "type": "string",
    "description": "Resource bookings"
   },
   "eventRegistrations": {
    "type": "string",
    "description": "Event registrations"
   },
   "consentRecords": {
    "type": "string",
    "description": "Consent records"
   },
   "credentialReferences": {
    "type": "string",
    "description": "Credential references"
   },
   "connectedApplications": {
    "type": "string",
    "description": "Connected applications"
   },
   "ticketing82Records": {
    "type": "string",
    "description": "Ticketing — 82 records"
   },
   "orders26Records": {
    "type": "string",
    "description": "Orders — 26 records"
   },
   "membership1Record": {
    "type": "string",
    "description": "Membership — 1 record"
   },
   "crm14Records": {
    "type": "string",
    "description": "CRM — 14 records"
   },
   "consent17Records": {
    "type": "string",
    "description": "Consent — 17 records"
   },
   "includedSystems": {
    "type": "string",
    "description": "Included systems"
   },
   "includedCategories": {
    "type": "string",
    "description": "Included categories"
   },
   "exclusions": {
    "type": "string",
    "description": "Exclusions"
   },
   "sensitiveFieldHandling": {
    "type": "string",
    "description": "Sensitive-field handling"
   },
   "format": {
    "type": "string",
    "description": "Format"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "encryptionSecurity": {
    "type": "string",
    "description": "Encryption/security"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   }
  }
 },
 "DataRetentionExpiryLegalHoldOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Data Retention, Expiry & Legal Hold Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "recordsApproachingExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "Records Approaching Expiry"
   },
   "eligibleForDeletion": {
    "type": "string",
    "description": "Eligible for Deletion"
   },
   "eligibleForAnonymization": {
    "type": "string",
    "description": "Eligible for Anonymization"
   },
   "underLegalHold": {
    "type": "string",
    "description": "Under Legal Hold"
   },
   "processingFailures": {
    "type": "integer",
    "description": "Processing Failures"
   },
   "retentionExceptions": {
    "type": "integer",
    "description": "Retention Exceptions"
   },
   "anonymize": {
    "type": "string",
    "description": "Anonymize"
   },
   "placeHold": {
    "type": "string",
    "description": "Place Hold"
   },
   "holdId": {
    "type": "string",
    "description": "Hold ID"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "scope": {
    "type": "string",
    "description": "Scope"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "start": {
    "type": "string",
    "description": "Start"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "daily": {
    "type": "string",
    "description": "Daily"
   },
   "weekly": {
    "type": "string",
    "description": "Weekly"
   },
   "monthly": {
    "type": "string",
    "description": "Monthly"
   },
   "onConfiguredSchedules": {
    "type": "string",
    "description": "On configured schedules"
   }
  }
 },
 "DataSubjectCustomerPrivacyRequestManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Data Subject / Customer Privacy Request Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "access": {
    "type": "string",
    "description": "Access"
   },
   "dataCopyExport": {
    "type": "string",
    "description": "Data Copy / Export"
   },
   "correction": {
    "type": "string",
    "description": "Correction"
   },
   "deletion": {
    "type": "string",
    "description": "Deletion"
   },
   "anonymization": {
    "type": "string",
    "description": "Anonymization"
   },
   "restriction": {
    "type": "string",
    "description": "Restriction"
   },
   "objection": {
    "type": "string",
    "description": "Objection"
   },
   "consentWithdrawal": {
    "type": "string",
    "description": "Consent Withdrawal"
   },
   "marketingOptOut": {
    "type": "string",
    "description": "Marketing Opt-out"
   },
   "otherOrganizationDefinedPrivacyRequests": {
    "type": "string",
    "description": "Other organization-defined privacy requests"
   },
   "customerPortal": {
    "type": "string",
    "description": "Customer Portal"
   },
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "emailManualEntry": {
    "type": "string",
    "description": "Email/manual entry"
   },
   "customerService": {
    "type": "string",
    "description": "Customer Service"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "guardian": {
    "type": "string",
    "description": "Guardian"
   },
   "authorizedRepresentative": {
    "type": "string",
    "description": "Authorized Representative"
   },
   "requestId": {
    "type": "string",
    "description": "Request ID"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "requestType": {
    "type": "string",
    "description": "Request Type"
   },
   "submittedAt": {
    "type": "string",
    "description": "Submitted At"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "jurisdiction": {
    "type": "string",
    "description": "Jurisdiction"
   },
   "dueDate": {
    "type": "string",
    "format": "date-time",
    "description": "Due Date"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "verificationStatus": {
    "type": "string",
    "description": "Verification Status"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "accountLogin": {
    "type": "string",
    "description": "Account Login"
   },
   "otp": {
    "type": "string",
    "description": "OTP"
   },
   "emailVerification": {
    "type": "string",
    "description": "Email Verification"
   },
   "mobileVerification": {
    "type": "string",
    "description": "Mobile Verification"
   },
   "idReviewWherePermitted": {
    "type": "string",
    "description": "ID Review where permitted"
   },
   "manualVerification": {
    "type": "string",
    "description": "Manual Verification"
   },
   "daysRemaining": {
    "type": "string",
    "description": "Days remaining"
   },
   "atRisk": {
    "type": "string",
    "description": "At risk"
   }
  }
 },
 "DeletionAnonymizationRestrictionOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Deletion, Anonymization & Restriction Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "anonymize": {
    "type": "string",
    "description": "Anonymize"
   },
   "pseudonymizeWhereConfigured": {
    "type": "string",
    "description": "Pseudonymize where configured"
   },
   "restrictProcessing": {
    "type": "string",
    "description": "Restrict Processing"
   },
   "suppressMarketing": {
    "type": "string",
    "description": "Suppress Marketing"
   },
   "disconnectThirdPartyProfile": {
    "type": "string",
    "description": "Disconnect Third-party Profile"
   },
   "otherConfiguredAction": {
    "type": "string",
    "description": "Other configured action"
   },
   "marketingProfileDelete": {
    "type": "string",
    "description": "Marketing Profile — Delete"
   },
   "biometricReferenceDelete": {
    "type": "string",
    "description": "Biometric Reference — Delete"
   },
   "fraudInvestigationHold": {
    "type": "string",
    "description": "Fraud Investigation — Hold"
   },
   "retentionRequirements": {
    "type": "string",
    "description": "Retention requirements"
   },
   "legalHolds": {
    "type": "string",
    "description": "Legal holds"
   },
   "financialRecords": {
    "type": "string",
    "description": "Financial records"
   },
   "activeTransactions": {
    "type": "integer",
    "description": "Active transactions"
   },
   "securityFraudRequirements": {
    "type": "string",
    "description": "Security/fraud requirements"
   },
   "contractualObligations": {
    "type": "string",
    "description": "Contractual obligations"
   },
   "configuredJurisdictionRules": {
    "type": "string",
    "description": "Configured jurisdiction rules"
   },
   "pending": {
    "type": "integer",
    "description": "Pending"
   },
   "processing": {
    "type": "string",
    "description": "Processing"
   },
   "completed": {
    "type": "string",
    "description": "Completed"
   },
   "retainedWithReason": {
    "type": "string",
    "description": "Retained with Reason"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "manualActionRequired": {
    "type": "boolean",
    "description": "Manual Action Required"
   }
  }
 },
 "PrivacyAnalyticsAiComplianceIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Privacy Analytics & AI Compliance Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "consentRate": {
    "type": "number",
    "description": "Consent Rate"
   },
   "withdrawalRate": {
    "type": "number",
    "description": "Withdrawal Rate"
   },
   "marketingOptInRate": {
    "type": "number",
    "description": "Marketing Opt-in Rate"
   },
   "cookieAcceptanceByCategory": {
    "type": "string",
    "description": "Cookie Acceptance by Category"
   },
   "privacyRequests": {
    "type": "string",
    "description": "Privacy Requests"
   },
   "averageResolutionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Resolution Time"
   },
   "slaCompliance": {
    "type": "string",
    "description": "SLA Compliance"
   },
   "deletionCompletionRate": {
    "type": "number",
    "description": "Deletion Completion Rate"
   },
   "retentionCompliance": {
    "type": "string",
    "description": "Retention Compliance"
   },
   "policyAcceptance": {
    "type": "string",
    "description": "Policy Acceptance"
   },
   "guardianConsentCompletion": {
    "type": "string",
    "description": "Guardian Consent Completion"
   },
   "privacyExceptions": {
    "type": "string",
    "description": "Privacy Exceptions"
   },
   "consentPropagationFailures": {
    "type": "string",
    "description": "Consent Propagation Failures"
   },
   "showOverdueDeletionRequests": {
    "type": "string",
    "description": "“Show overdue deletion requests.”"
   },
   "backendScreenCoreResponsibility": {
    "type": "string",
    "description": "# Backend Screen Core Responsibility"
   },
   "board1Configure": {
    "type": "string",
    "description": "Board 1 — CONFIGURE"
   },
   "board2Operate": {
    "type": "string",
    "description": "Board 2 — OPERATE"
   },
   "consentStates": {
    "type": "string",
    "description": "consent states"
   }
  }
 },
 "PrivacyAuditEvidenceComplianceReportingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Privacy Audit, Evidence & Compliance Reporting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "consentGranted": {
    "type": "string",
    "description": "Consent Granted"
   },
   "consentWithdrawn": {
    "type": "string",
    "description": "Consent Withdrawn"
   },
   "preferenceChanged": {
    "type": "string",
    "description": "Preference Changed"
   },
   "policyAccepted": {
    "type": "string",
    "description": "Policy Accepted"
   },
   "privacyRequestCreated": {
    "type": "string",
    "format": "date-time",
    "description": "Privacy Request Created"
   },
   "identityVerified": {
    "type": "string",
    "description": "Identity Verified"
   },
   "dataExportGenerated": {
    "type": "string",
    "description": "Data Export Generated"
   },
   "correctionRequested": {
    "type": "string",
    "description": "Correction Requested"
   },
   "deletionApproved": {
    "type": "string",
    "description": "Deletion Approved"
   },
   "anonymizationExecuted": {
    "type": "string",
    "description": "Anonymization Executed"
   },
   "retentionAction": {
    "type": "string",
    "description": "Retention Action"
   },
   "legalHold": {
    "type": "string",
    "description": "Legal Hold"
   },
   "administrativeOverride": {
    "type": "string",
    "description": "Administrative Override"
   },
   "configurationChange": {
    "type": "string",
    "description": "Configuration Change"
   },
   "eventId": {
    "type": "string",
    "description": "Event ID"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "actor": {
    "type": "string",
    "description": "Actor"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "before": {
    "type": "string",
    "description": "Before"
   },
   "after": {
    "type": "string",
    "description": "After"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "relatedCase": {
    "type": "string",
    "description": "Related Case"
   },
   "evidenceReference": {
    "type": "string",
    "description": "Evidence reference"
   },
   "consentStatusReport": {
    "type": "string",
    "description": "Consent Status Report"
   },
   "consentWithdrawalReport": {
    "type": "string",
    "description": "Consent Withdrawal Report"
   },
   "marketingPermissionReport": {
    "type": "string",
    "description": "Marketing Permission Report"
   },
   "privacyRequestSlaReport": {
    "type": "string",
    "description": "Privacy Request SLA Report"
   },
   "deletionAnonymizationReport": {
    "type": "string",
    "description": "Deletion/Anonymization Report"
   },
   "retentionReport": {
    "type": "string",
    "description": "Retention Report"
   },
   "policyAcceptanceReport": {
    "type": "string",
    "description": "Policy Acceptance Report"
   },
   "minorGuardianPrivacyReport": {
    "type": "string",
    "description": "Minor/Guardian Privacy Report"
   },
   "cookieTrackingComplianceReport": {
    "type": "string",
    "description": "Cookie/Tracking Compliance Report"
   },
   "biometricPrivacyReport": {
    "type": "string",
    "description": "Biometric Privacy Report"
   },
   "exceptionReport": {
    "type": "string",
    "description": "Exception Report"
   },
   "selected": {
    "type": "string",
    "description": "selected"
   }
  }
 },
 "PrivacyComplianceExceptionInvestigationWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Privacy Compliance, Exception & Investigation Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "exceptionSummary": {
    "type": "string",
    "description": "Exception summary"
   },
   "customerPrivacyProfile": {
    "type": "string",
    "description": "Customer privacy profile"
   },
   "relatedEvidence": {
    "type": "string",
    "description": "Related evidence"
   },
   "policyConfiguration": {
    "type": "string",
    "description": "Policy/configuration"
   },
   "systemEvents": {
    "type": "string",
    "description": "System events"
   },
   "timeline": {
    "type": "string",
    "description": "Timeline"
   },
   "rootCause": {
    "type": "string",
    "description": "Root cause"
   },
   "correctiveAction": {
    "type": "string",
    "description": "Corrective action"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "attachmentsReferenceEvidence": {
    "type": "string",
    "description": "Attachments/reference evidence"
   },
   "privacy": {
    "type": "string",
    "description": "Privacy"
   },
   "legal": {
    "type": "string",
    "description": "Legal"
   },
   "security": {
    "type": "string",
    "description": "Security"
   },
   "it": {
    "type": "string",
    "description": "IT"
   },
   "marketing": {
    "type": "string",
    "description": "Marketing"
   },
   "operations": {
    "type": "string",
    "description": "Operations"
   },
   "dataOwner": {
    "type": "string",
    "description": "Data Owner"
   },
   "fullEnterpriseCybersecurityIncidentManagementPlatform": {
    "type": "string",
    "description": "full enterprise cybersecurity incident-management platform"
   }
  }
 },
 "PrivacyComplianceExceptionInvestigationWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Privacy Compliance, Exception & Investigation Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "severity": {
    "type": "string",
    "description": "Severity"
   },
   "exception": {
    "type": "string",
    "description": "Exception"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "system": {
    "type": "string",
    "description": "System"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "detectedAt": {
    "type": "string",
    "description": "Detected At"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "exceptionSummary": {
    "type": "string",
    "description": "Exception summary"
   },
   "customerPrivacyProfile": {
    "type": "string",
    "description": "Customer privacy profile"
   },
   "relatedEvidence": {
    "type": "string",
    "description": "Related evidence"
   },
   "policyConfiguration": {
    "type": "string",
    "description": "Policy/configuration"
   },
   "systemEvents": {
    "type": "string",
    "description": "System events"
   },
   "timeline": {
    "type": "string",
    "description": "Timeline"
   },
   "rootCause": {
    "type": "string",
    "description": "Root cause"
   },
   "correctiveAction": {
    "type": "string",
    "description": "Corrective action"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "attachmentsReferenceEvidence": {
    "type": "string",
    "description": "Attachments/reference evidence"
   },
   "privacy": {
    "type": "string",
    "description": "Privacy"
   },
   "legal": {
    "type": "string",
    "description": "Legal"
   },
   "security": {
    "type": "string",
    "description": "Security"
   },
   "it": {
    "type": "string",
    "description": "IT"
   },
   "marketing": {
    "type": "string",
    "description": "Marketing"
   },
   "operations": {
    "type": "string",
    "description": "Operations"
   },
   "dataOwner": {
    "type": "string",
    "description": "Data Owner"
   },
   "fullEnterpriseCybersecurityIncidentManagementPlatform": {
    "type": "string",
    "description": "full enterprise cybersecurity incident-management platform"
   }
  }
 },
 "PrivacyOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Privacy Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalCustomerPrivacyProfiles": {
    "type": "integer",
    "description": "Total Customer Privacy Profiles"
   },
   "activeConsentRecords": {
    "type": "integer",
    "description": "Active Consent Records"
   },
   "withdrawnConsents": {
    "type": "integer",
    "description": "Withdrawn Consents"
   },
   "marketingOptIns": {
    "type": "integer",
    "description": "Marketing Opt-ins"
   },
   "marketingOptOuts": {
    "type": "integer",
    "description": "Marketing Opt-outs"
   },
   "pendingDataRightsRequests": {
    "type": "integer",
    "description": "Pending Data Rights Requests"
   },
   "overdueRequests": {
    "type": "integer",
    "description": "Overdue Requests"
   },
   "pendingDeletionActions": {
    "type": "integer",
    "description": "Pending Deletion Actions"
   },
   "pendingAnonymization": {
    "type": "integer",
    "description": "Pending Anonymization"
   },
   "retentionActionsDue": {
    "type": "string",
    "description": "Retention Actions Due"
   },
   "consentEvidenceExceptions": {
    "type": "integer",
    "description": "Consent Evidence Exceptions"
   },
   "privacyIncidentsExceptions": {
    "type": "string",
    "description": "Privacy Incidents / Exceptions"
   },
   "policyReAcceptancePending": {
    "type": "integer",
    "description": "Policy Re-Acceptance Pending"
   },
   "emailMarketing": {
    "type": "string",
    "description": "Email Marketing"
   },
   "smsMarketing": {
    "type": "string",
    "description": "SMS Marketing"
   },
   "whatsappMarketing": {
    "type": "string",
    "description": "WhatsApp Marketing"
   },
   "push": {
    "type": "string",
    "description": "Push"
   },
   "personalization": {
    "type": "string",
    "description": "Personalization"
   },
   "analytics": {
    "type": "integer",
    "description": "Analytics"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "biometrics": {
    "type": "integer",
    "description": "Biometrics"
   },
   "otherConfiguredPurposes": {
    "type": "integer",
    "description": "Other configured purposes"
   },
   "investigateEvidence": {
    "type": "string",
    "description": "Investigate Evidence"
   }
  }
 }
}
```
