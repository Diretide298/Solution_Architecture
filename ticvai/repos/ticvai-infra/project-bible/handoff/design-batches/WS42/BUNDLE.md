# WS42 — Privacy  Consent   Preference Management board 2

**10 screens · 10 operations · 13 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AUDIT_VIEW, GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
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
| `CMS-040` | Privacy Analytics & AI Compliance Intelligence | listDetail | 2 | 0 | — |

## Thin screens in this batch

**CMS-032, CMS-033, CMS-035 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-031 holds none of them, so the edge carries nothing and CMS-001 opens cold"
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
  "purposeNote": "Authorized users can understand the current operational privacy position and identify actions requiring attention from one command center.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide Privacy, Compliance and authorized operational teams with a centralized real-time overview of privacy operations across TICVAI.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-031",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-031"
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
  "purposeNote": "An authorized user can reconstruct the customer's complete privacy relationship with TICVAI from one governed workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide one authoritative privacy view for an individual customer or participant. This becomes the privacy equivalent of the customer 360° workspace. n ed el",
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
        "CustomerPrivacyConsentPreference360View.policyAcceptance[].documentType",
        "CustomerPrivacyConsentPreference360View.policyAcceptance[].acceptedVersion",
        "CustomerPrivacyConsentPreference360View.policyAcceptance[].currentVersion",
        "CustomerPrivacyConsentPreference360View.policyAcceptance[].requiresReacceptance"
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
        "CustomerPrivacyConsentPreference360View.policyAcceptance[].documentType",
        "CustomerPrivacyConsentPreference360View.policyAcceptance[].acceptedVersion",
        "CustomerPrivacyConsentPreference360View.policyAcceptance[].currentVersion",
        "CustomerPrivacyConsentPreference360View.policyAcceptance[].requiresReacceptance"
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
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-032",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-032"
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
  "purposeNote": "current privacy state and propagate to dependent systems.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Maintain legally and operationally useful evidence of every consent event and manage subsequent withdrawals.",
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
        "ConsentEvidenceHistoryWithdrawalManagementView.propagation[].target",
        "ConsentEvidenceHistoryWithdrawalManagementView.propagation[].status"
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
        "ConsentEvidenceHistoryWithdrawalManagementView.propagation[].target",
        "ConsentEvidenceHistoryWithdrawalManagementView.propagation[].status"
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
    "Retry Required"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-033",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-033"
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
  "purposeNote": "Every customer privacy request can be received, verified, assigned, tracked and completed through a governed case workflow.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide a governed case-management workflow for customer privacy requests.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Email/manual entry, POS, API, Authorized Representative, ID Review where permitted. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Email/manual entry",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Service",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "POS",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "API",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Authorized Representative",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-034",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-034"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 26. 2 of 4 labels bound to a contract property; 24 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Authorized teams can discover applicable customer data, prepare a controlled access/export response and route correction to the authoritative data owner.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow authorized privacy teams to locate customer data across TICVAI and connected systems when fulfilling access, export or correction requests.",
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
        "DataDiscoveryAccessExportCorrectionWorkspaceView.results[].source",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.results[].recordCount"
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
        "DataDiscoveryAccessExportCorrectionWorkspaceView.results[].source",
        "DataDiscoveryAccessExportCorrectionWorkspaceView.results[].recordCount"
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
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-035",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-035"
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
  "purposeNote": "are legitimately configured for retention and provides evidence of the result.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern privacy requests or policies requiring personal data to be deleted, anonymized or restricted. This screen requires strong controls because deletion may affect financial, ticketing, fraud, legal and operational records.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Delete, Pseudonymize where configured, Remove Biometric Reference. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "kind": "secondaryButton",
       "label": "Pseudonymize where configured",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Restrict Processing",
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
    "DeletionAnonymizationRestrictionOperationsView.actionType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-036",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-036"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 4 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "preserving controlled holds, approvals and complete processing evidence.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Operationalize retention policies associated with Board 1 processing purposes and data categories.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Review, Extend where authorized, Delete, Archive, Place Hold, Release Hold. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "kind": "secondaryButton",
       "label": "Extend where authorized",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-037",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-037"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 30. 6 of 6 labels bound to a contract property; 15 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Privacy-related exceptions can be centrally investigated, assigned, resolved and audited.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a centralized workspace for privacy configuration and operational exceptions requiring investigation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Security, Operations, Data Owner. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
        "PrivacyComplianceExceptionInvestigationWorkspaceView.category",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.subjectId",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.system",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.brandId",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.country",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.detectedAt",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.ownerPrincipalId",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.slaDueAt",
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
        "PrivacyComplianceExceptionInvestigationWorkspaceView.category",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.subjectId",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.system",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.brandId",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.country",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.detectedAt",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.ownerPrincipalId",
        "PrivacyComplianceExceptionInvestigationWorkspaceView.slaDueAt",
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
       "label": "Operations",
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
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "PrivacyComplianceExceptionInvestigationWorkspaceView.severity",
    "PrivacyComplianceExceptionInvestigationWorkspaceView.system",
    "PrivacyComplianceExceptionInvestigationWorkspaceView.country"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-038",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-038"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 32. 10 of 10 labels bound to a contract property; 13 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "performed it, what rule/version applied and what evidence supports it.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture significant activities such as) and no display directory — it is settings, not a population",
  "purpose": "Provide immutable auditability and management/compliance reporting across privacy operations.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-039",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-039"
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
  "purposeNote": "resolve compliance risks while keeping legally significant decisions under governed human control. Board 2 — Final Screen Register # Backend Screen Core Responsibility 17.2. Privacy Operations Command Center Overall privacy operations 1 17.2. Customer Privacy, Consent & Preference Complete customer privacy 2 360° view 17.2. Consent Evidence, History & Withdrawal Consent evidence and 3 Management withdrawal 17.2. Data Subject / Customer Privacy Request",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Provide executives, Privacy Officers and Compliance teams with actionable privacy analytics and AI-assisted risk detection. This should be the intelligence layer across both Privacy Boards.",
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
        "PrivacyAnalyticsAiComplianceIntelligenceView.averageResolutionSeconds",
        "PrivacyAnalyticsAiComplianceIntelligenceView.slaComplianceRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.deletionCompletionRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.retentionComplianceRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.policyAcceptanceRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.guardianConsentCompletionRate",
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
        "PrivacyAnalyticsAiComplianceIntelligenceView.averageResolutionSeconds",
        "PrivacyAnalyticsAiComplianceIntelligenceView.slaComplianceRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.deletionCompletionRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.retentionComplianceRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.policyAcceptanceRate",
        "PrivacyAnalyticsAiComplianceIntelligenceView.guardianConsentCompletionRate",
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
   },
   {
    "operationId": "listPrivacyEvidenceCompliance",
    "contract": "marketing-crm",
    "purpose": "Privacy Audit, Evidence & Compliance Reporting",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PrivacyAnalyticsAiComplianceIntelligenceView.consentRate",
    "PrivacyAnalyticsAiComplianceIntelligenceView.withdrawalRate",
    "PrivacyAnalyticsAiComplianceIntelligenceView.marketingOptInRate",
    "PrivacyAnalyticsAiComplianceIntelligenceView.cookieAcceptanceByCategory",
    "PrivacyAnalyticsAiComplianceIntelligenceView.privacyRequests"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-040",
   "workshopBoard": "wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-040"
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
  "permission": "GUEST_VIEW",
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
    "name": "consentPurpose",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "source",
    "in": "query",
    "required": false
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
    "name": "propagationStatus",
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
 "listCustomerPrivacyConsent": {
  "method": "GET",
  "path": "/customer-privacy-consent",
  "contract": "marketing-crm",
  "summary": "Customer Privacy, Consent & Preference 360°",
  "permission": "GUEST_VIEW_PII",
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
  "responds": "CustomerPrivacyConsentPreference360View"
 },
 "listDataRetentionExpiry": {
  "method": "GET",
  "path": "/data-retention-expiry",
  "contract": "marketing-crm",
  "summary": "Data Retention, Expiry & Legal Hold Operations",
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
    "name": "dataCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "jurisdiction",
    "in": "query",
    "required": false
   },
   {
    "name": "holdStatus",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "DataRetentionExpiryLegalHoldOperationsView"
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
 "listDeletionAnonymizationRestriction": {
  "method": "GET",
  "path": "/deletion-anonymization-restriction",
  "contract": "marketing-crm",
  "summary": "Deletion, Anonymization & Restriction Operations",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "actionType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "setPrivacyComplianceException": {
  "method": "PUT",
  "path": "/privacy-compliance-exception",
  "contract": "marketing-crm",
  "summary": "Raise, investigate or close a privacy exception",
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
  "requestBody": "PrivacyComplianceExceptionInvestigationWorkspaceInput",
  "responds": "PrivacyComplianceExceptionInvestigationWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "ConsentSource": {
  "type": "string",
  "enum": [
   "guestApp",
   "website",
   "kiosk",
   "pos",
   "callCentre",
   "import",
   "agentRecorded"
  ]
 },
 "CustomerPrivacyConsentPreference360View": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.guest_profile, marketing.consent_record, marketing.consent_record_channel, marketing.consent_purpose, marketing.privacy_request (new), marketing.tracking_technology, pii.subject",
  "description": "One customer's privacy position (pack 17.2.2). Consent entries are current state; history is `listConsentEvidenceWithdrawal`.",
  "required": [
   "subjectId",
   "consents",
   "policyAcceptance"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "accountStatus": {
    "type": "string",
    "enum": [
     "active",
     "guest",
     "suspended",
     "archived",
     "erased"
    ],
    "description": "`archived` and `erased` are the ADR-0047 lifecycle stages."
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true,
    "description": "BCP 47 tag."
   },
   "ageCategory": {
    "type": "string",
    "enum": [
     "adult",
     "minor",
     "unknown"
    ]
   },
   "guardianSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guardianRelationship": {
    "type": "string",
    "nullable": true,
    "enum": [
     "parent",
     "legalGuardian",
     "other"
    ]
   },
   "openExceptionCount": {
    "type": "integer",
    "minimum": 0,
    "description": "The privacy risk/exception indicator; open exceptions naming this customer."
   },
   "consents": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "channel": {
       "allOf": [
        {
         "$ref": "#/components/schemas/MessageChannel"
        }
       ],
       "nullable": true
      },
      "decision": {
       "type": "string",
       "enum": [
        "granted",
        "declined",
        "withdrawn",
        "expired",
        "notAsked"
       ]
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "capturedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "source": {
       "allOf": [
        {
         "$ref": "#/components/schemas/ConsentSource"
        }
       ],
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean"
      }
     }
    }
   },
   "preferences": {
    "type": "object",
    "properties": {
     "channels": {
      "type": "array",
      "items": {
       "type": "object",
       "required": [
        "channel",
        "optedIn"
       ],
       "properties": {
        "channel": {
         "$ref": "#/components/schemas/MessageChannel"
        },
        "optedIn": {
         "type": "boolean"
        }
       }
      }
     },
     "brandIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "marketingCategories": {
      "type": "array",
      "items": {
       "type": "string",
       "maxLength": 80
      }
     },
     "personalisationEnabled": {
      "type": "boolean"
     }
    }
   },
   "policyAcceptance": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "documentType",
      "currentVersion"
     ],
     "properties": {
      "documentType": {
       "type": "string",
       "enum": [
        "privacyPolicy",
        "cookieNotice",
        "biometricNotice",
        "childrensPrivacyNotice",
        "other"
       ]
      },
      "documentName": {
       "type": "string",
       "nullable": true
      },
      "acceptedVersion": {
       "type": "string",
       "nullable": true
      },
      "acceptedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "currentVersion": {
       "type": "string"
      },
      "requiresReacceptance": {
       "type": "boolean"
      }
     }
    }
   },
   "trackingChoices": {
    "type": "array",
    "description": "Only where the preference is tied to this customer (a signed-in consent).",
    "items": {
     "type": "object",
     "required": [
      "category",
      "decision"
     ],
     "properties": {
      "category": {
       "type": "string",
       "enum": [
        "strictlyNecessary",
        "functional",
        "analytics",
        "personalisation",
        "marketing",
        "other"
       ]
      },
      "decision": {
       "type": "string",
       "enum": [
        "granted",
        "declined"
       ]
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "privacyRequests": {
    "type": "array",
    "description": "Open requests and the 20 most recent completed ones.",
    "items": {
     "type": "object",
     "required": [
      "requestId",
      "requestType",
      "status"
     ],
     "properties": {
      "requestId": {
       "type": "string",
       "format": "uuid"
      },
      "requestType": {
       "type": "string"
      },
      "status": {
       "type": "string",
       "enum": [
        "submitted",
        "inProgress",
        "completed"
       ]
      },
      "submittedAt": {
       "type": "string",
       "format": "date-time"
      },
      "dueAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "dataFootprint": {
    "type": "array",
    "description": "Where this customer's data exists, as counts; the records are reached through `setDataDiscoveryAccess`.",
    "items": {
     "type": "object",
     "required": [
      "system",
      "recordCount"
     ],
     "properties": {
      "system": {
       "type": "string",
       "enum": [
        "crm",
        "ticketing",
        "membership",
        "orders",
        "loyalty",
        "wallet",
        "marketing",
        "waiver",
        "biometricProviderReference",
        "connectedSystem"
       ]
      },
      "systemName": {
       "type": "string",
       "nullable": true,
       "description": "The connected system's name, when `system` is `connectedSystem`."
      },
      "recordCount": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "timeline": {
    "type": "array",
    "description": "The 50 most recent privacy events, newest first.",
    "items": {
     "type": "object",
     "required": [
      "occurredAt",
      "event"
     ],
     "properties": {
      "occurredAt": {
       "type": "string",
       "format": "date-time"
      },
      "event": {
       "type": "string",
       "enum": [
        "accountCreated",
        "policyAccepted",
        "consentGranted",
        "consentDeclined",
        "consentWithdrawn",
        "preferenceChanged",
        "privacyRequestCreated",
        "privacyRequestCompleted",
        "dataExportGenerated",
        "anonymised",
        "archived"
       ]
      },
      "summary": {
       "type": "string",
       "maxLength": 300
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
 "DataRetentionExpiryLegalHoldOperationsView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.retention_policy, marketing.legal_hold (new), marketing.privacy_action (new), marketing.guest_profile, pii.subject",
  "description": "The retention dashboard (pack 17.2.7) against ADR-0047's lifecycle.",
  "required": [
   "recordsApproachingExpiry",
   "policies",
   "holds"
  ],
  "properties": {
   "recordsApproachingExpiry": {
    "type": "integer",
    "minimum": 0,
    "description": "Inside the 90-day notice window before their retention action."
   },
   "eligibleForDeletion": {
    "type": "integer",
    "minimum": 0
   },
   "eligibleForAnonymization": {
    "type": "integer",
    "minimum": 0
   },
   "eligibleForArchive": {
    "type": "integer",
    "minimum": 0
   },
   "underLegalHold": {
    "type": "integer",
    "minimum": 0
   },
   "processingFailures": {
    "type": "integer",
    "minimum": 0
   },
   "retentionExceptions": {
    "type": "integer",
    "minimum": 0,
    "description": "Open `retentionFailure` / `deletionFailure` privacy exceptions."
   },
   "lifecycle": {
    "type": "object",
    "description": "Guest subjects by ADR-0047 stage.",
    "properties": {
     "active": {
      "type": "integer",
      "minimum": 0
     },
     "archived": {
      "type": "integer",
      "minimum": 0
     },
     "erased": {
      "type": "integer",
      "minimum": 0
     }
    }
   },
   "policies": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "policyId",
      "code",
      "action"
     ],
     "properties": {
      "policyId": {
       "type": "string",
       "format": "uuid"
      },
      "code": {
       "type": "string"
      },
      "dataCategory": {
       "type": "string"
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
      "retainMonths": {
       "type": "integer",
       "minimum": 0
      },
      "isSystemDefault": {
       "type": "boolean",
       "description": "True when inherited from the system default; false when the tenant or venue overrode it."
      },
      "floorMonths": {
       "type": "integer",
       "minimum": 0,
       "nullable": true
      },
      "ceilingMonths": {
       "type": "integer",
       "minimum": 0,
       "nullable": true
      },
      "anchor": {
       "type": "string",
       "enum": [
        "lastActivity",
        "creation",
        "eventEnd",
        "transactionDate"
       ]
      },
      "approachingExpiry": {
       "type": "integer",
       "minimum": 0
      },
      "eligibleNow": {
       "type": "integer",
       "minimum": 0
      },
      "heldBack": {
       "type": "integer",
       "minimum": 0
      },
      "schedule": {
       "type": "string",
       "enum": [
        "daily",
        "weekly",
        "monthly",
        "custom",
        "manual"
       ]
      },
      "nextRunAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "lastRun": {
       "type": "object",
       "nullable": true,
       "properties": {
        "runId": {
         "type": "string",
         "format": "uuid"
        },
        "completedAt": {
         "type": "string",
         "format": "date-time",
         "nullable": true
        },
        "recordsAffected": {
         "type": "integer",
         "minimum": 0
        },
        "failed": {
         "type": "integer",
         "minimum": 0
        }
       }
      }
     }
    }
   },
   "holds": {
    "type": "array",
    "description": "Holds in the requested states, by `reviewDate` ascending.",
    "items": {
     "$ref": "#/components/schemas/PrivacyLegalHold"
    }
   },
   "asOf": {
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
 "PrivacyComplianceExceptionInvestigationWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.privacy_exception",
  "description": "What a user may send to raise or progress a privacy exception (pack 17.2.8).",
  "required": [
   "category",
   "severity",
   "summary"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Absent to raise; present to update."
   },
   "category": {
    "type": "string",
    "enum": [
     "missingConsentEvidence",
     "consentPropagationFailure",
     "marketingAfterWithdrawal",
     "policyVersionMismatch",
     "missingGuardianConsent",
     "retentionFailure",
     "deletionFailure",
     "unknownTrackingTechnology",
     "unauthorisedDataAccess",
     "unmappedProcessingPurpose",
     "biometricPrivacyException",
     "dataExportFailure",
     "other"
    ]
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
   "summary": {
    "type": "string",
    "maxLength": 1000
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "system": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "detected",
     "triaged",
     "assigned",
     "investigated",
     "correctiveAction",
     "reviewed",
     "closed"
    ],
    "default": "detected"
   },
   "relatedEvidenceIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Consent evidence ids and audit event ids."
   },
   "policyReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "The configuration or policy version involved."
   },
   "rootCause": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true
   },
   "correctiveAction": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true
   },
   "notes": {
    "type": "string",
    "maxLength": 4000,
    "nullable": true
   },
   "attachmentAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "escalatedTo": {
    "type": "string",
    "nullable": true,
    "enum": [
     "privacy",
     "legal",
     "security",
     "it",
     "marketing",
     "operations",
     "dataOwner"
    ]
   },
   "privacyIncidentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `recordPrivacyIncident` record, when the exception is also a breach."
   }
  }
 },
 "PrivacyComplianceExceptionInvestigationWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.privacy_exception",
  "description": "One privacy exception as stored, with its investigation fields and timeline.",
  "allOf": [
   {
    "$ref": "#/components/schemas/PrivacyComplianceExceptionInvestigationWorkspaceInput"
   },
   {
    "type": "object",
    "required": [
     "id",
     "detectedAt"
    ],
    "properties": {
     "detectedAt": {
      "type": "string",
      "format": "date-time",
      "readOnly": true
     },
     "detectedBy": {
      "type": "string",
      "readOnly": true,
      "enum": [
       "platformCheck",
       "aiDetection",
       "user"
      ]
     },
     "slaDueAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "From the SLA policy for the severity (`setSlaPolicy`)."
     },
     "timeline": {
      "type": "array",
      "readOnly": true,
      "items": {
       "type": "object",
       "properties": {
        "at": {
         "type": "string",
         "format": "date-time"
        },
        "status": {
         "type": "string"
        },
        "principalId": {
         "type": "string",
         "format": "uuid",
         "nullable": true
        },
        "note": {
         "type": "string",
         "nullable": true
        }
       }
      }
     },
     "closedAt": {
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
   }
  ]
 },
 "PrivacyLegalHold": {
  "type": "object",
  "x-ticvai-persistence": "marketing.legal_hold",
  "description": "A legal or operational hold (pack 17.2.7 Hold information). Overrides scheduled deletion in its scope once approved.",
  "required": [
   "reason",
   "scope"
  ],
  "properties": {
   "holdId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "legal",
     "operational",
     "fraudInvestigation",
     "regulatorRequest"
    ],
    "default": "legal"
   },
   "reason": {
    "type": "string",
    "maxLength": 1000
   },
   "scope": {
    "type": "object",
    "description": "At least one selector.",
    "properties": {
     "subjectIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "dataCategories": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "retentionPolicyCodes": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "caseId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "startsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Defaults to approval time."
   },
   "reviewDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingApproval",
     "active",
     "released"
    ],
    "default": "pendingApproval",
    "description": "Set `active` to approve, `released` to release."
   },
   "placedByPrincipalId": {
    "type": "string",
    "format": "uuid",
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
   "releaseReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "releasedAt": {
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
 }
}
```
