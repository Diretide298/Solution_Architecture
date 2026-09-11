# WS11 — Access Control board 11

**10 screens · 10 operations · 12 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ACCESS_POINT_CONFIGURE, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-244` | Access Security & Fraud Command Center | listDetail | 1 | 0 | — |
| `BO-245` | Fraud Detection Rule & Signal Library | listDetail | 1 | 0 | — |
| `BO-246` | Credential Sharing & Concurrent Usage Detection | listDetail | 1 | 0 | — |
| `BO-247` | Unified Identity & Credential Lock Manager | listDetail | 1 | 0 | — |
| `BO-248` | Biometric & Identity Integrity Monitoring | listDetail | 1 | 0 | — |
| `BO-249` | Relationship & Companion Fraud Monitoring | configEditor | 1 | 0 | — |
| `BO-250` | Access Risk Scoring & Decision Engine | listDetail | 1 | 0 | — |
| `BO-251` | Real-Time Security Response & Playbook Builder | listDetail | 1 | 0 | — |
| `BO-252` | Security Investigation & Evidence Workspace | listDetail | 1 | 0 | — |
| `BO-253` | Security Analytics, AI Detection & Governance | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-244, BO-245, BO-246, BO-247, BO-248, BO-250, BO-252 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-244",
  "name": "Access Security & Fraud Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.1",
   "page": 151
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-security-fraud-command-center-bo-244",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessSecurityFraudCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-245",
    "BO-246",
    "BO-247",
    "BO-248",
    "BO-249",
    "BO-250",
    "BO-251",
    "BO-252",
    "BO-253"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-245",
     "trigger": "Works in Fraud Detection Rule & Signal Library",
     "provenance": "flow F121 step 1→2",
     "operation": "listAccessSecurityFraud"
    },
    {
     "to": "BO-246",
     "trigger": "Works in Credential Sharing & Concurrent Usage Detection",
     "provenance": "flow F121 step 3→4",
     "operation": "listAccessSecurityFraud"
    },
    {
     "to": "BO-247",
     "trigger": "Works in Unified Identity & Credential Lock Manager",
     "provenance": "flow F121 step 5→6",
     "operation": "listAccessSecurityFraud"
    },
    {
     "to": "BO-248",
     "trigger": "Works in Biometric & Identity Integrity Monitoring",
     "provenance": "flow F121 step 7→8",
     "operation": "listAccessSecurityFraud"
    },
    {
     "to": "BO-249",
     "trigger": "Works in Relationship & Companion Fraud Monitoring",
     "provenance": "flow F121 step 9→10",
     "operation": "listAccessSecurityFraud"
    },
    {
     "to": "BO-250",
     "trigger": "Works in Access Risk Scoring & Decision Engine",
     "provenance": "flow F121 step 11→12",
     "operation": "listAccessSecurityFraud"
    },
    {
     "to": "BO-251",
     "trigger": "Works in Real-Time Security Response & Playbook Builder",
     "provenance": "flow F121 step 13→14",
     "operation": "listAccessSecurityFraud"
    },
    {
     "to": "BO-252",
     "trigger": "Works in Security Investigation & Evidence Workspace",
     "provenance": "flow F121 step 15→16",
     "operation": "listAccessSecurityFraud"
    },
    {
     "to": "BO-253",
     "trigger": "Works in Security Analytics, AI Detection & Governance",
     "provenance": "flow F121 step 17→18",
     "operation": "listAccessSecurityFraud"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide security teams with a real-time command center for access-related fraud and suspicious activity across all venues.",
  "purposeNote": "Security teams can understand the overall fraud and access-security posture from one screen.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every access security fraud",
       "columns": [
        "AccessSecurityFraudCommandCenterView.activeSecurityAlerts",
        "AccessSecurityFraudCommandCenterView.highRiskCredentials",
        "AccessSecurityFraudCommandCenterView.credentialsLockedToday",
        "AccessSecurityFraudCommandCenterView.suspiciousQrActivity",
        "AccessSecurityFraudCommandCenterView.deviceSharingAlerts",
        "AccessSecurityFraudCommandCenterView.biometricAlerts",
        "Duplicate Access Attempts",
        "AccessSecurityFraudCommandCenterView.blacklistedCredentials",
        "AccessSecurityFraudCommandCenterView.activeInvestigations",
        "AccessSecurityFraudCommandCenterView.fraudPrevented",
        "AccessSecurityFraudCommandCenterView.lowRisk",
        "AccessSecurityFraudCommandCenterView.mediumRisk",
        "AccessSecurityFraudCommandCenterView.highRisk",
        "AccessSecurityFraudCommandCenterView.critical"
       ],
       "bindsTo": "AccessSecurityFraudCommandCenterView",
       "operation": "listAccessSecurityFraud",
       "provenance": "pack Access Control Module_Reference.pdf, page 151 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access security fraud",
       "bindsTo": "AccessSecurityFraudCommandCenterView",
       "columns": [
        "AccessSecurityFraudCommandCenterView.activeSecurityAlerts",
        "AccessSecurityFraudCommandCenterView.highRiskCredentials",
        "AccessSecurityFraudCommandCenterView.credentialsLockedToday",
        "AccessSecurityFraudCommandCenterView.suspiciousQrActivity",
        "AccessSecurityFraudCommandCenterView.deviceSharingAlerts",
        "AccessSecurityFraudCommandCenterView.biometricAlerts",
        "Duplicate Access Attempts",
        "AccessSecurityFraudCommandCenterView.blacklistedCredentials",
        "AccessSecurityFraudCommandCenterView.activeInvestigations",
        "AccessSecurityFraudCommandCenterView.fraudPrevented",
        "AccessSecurityFraudCommandCenterView.lowRisk",
        "AccessSecurityFraudCommandCenterView.mediumRisk",
        "AccessSecurityFraudCommandCenterView.highRisk",
        "AccessSecurityFraudCommandCenterView.critical"
       ],
       "notes": "The pack groups this record's detail under its own headings: “CRITICAL”, “HIGH”, “MEDIUM”, “Display incidents geographically across”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 151 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access security fraud list.",
   "error": "Could not load. Names which read failed and leaves the access security fraud untouched.",
   "emptyFirstRun": "No access security fraud yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access security fraud are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessSecurityFraud",
    "contract": "access",
    "purpose": "Access Security & Fraud Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AccessSecurityFraudCommandCenterView.activeSecurityAlerts",
    "AccessSecurityFraudCommandCenterView.highRiskCredentials",
    "AccessSecurityFraudCommandCenterView.credentialsLockedToday",
    "AccessSecurityFraudCommandCenterView.suspiciousQrActivity",
    "AccessSecurityFraudCommandCenterView.deviceSharingAlerts",
    "AccessSecurityFraudCommandCenterView.biometricAlerts"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-244"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 151. 13 of 14 labels bound to a contract property; 14 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-245",
  "name": "Fraud Detection Rule & Signal Library",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.2",
   "page": 152
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/fraud-detection-rule-signal-library-bo-245",
   "component": "apps/venue-management-web/src/routes/access-venue/FraudDetectionRuleSignalLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-244"
   ],
   "exitTo": [
    "BO-244"
   ],
   "inferred": false,
   "notes": "**Reached from BO-244, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-244",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F121 step 2→3",
     "operation": "listFraudDetectionRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the signals TICVAI uses to identify suspicious access behavior.",
  "purposeNote": "Fraud detection logic is configurable rather than hard-coded.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 152"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 152"
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
       "impliedBy": "listFraudDetectionRule",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fraud detection rule list.",
   "error": "Could not load. Names which read failed and leaves the fraud detection rule untouched.",
   "emptyFirstRun": "No fraud detection rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the fraud detection rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFraudDetectionRule",
    "contract": "access",
    "purpose": "Fraud Detection Rule & Signal Library",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "FraudDetectionRuleSignalLibraryView.excessiveQrActivations",
    "FraudDetectionRuleSignalLibraryView.multipleActiveSessions",
    "FraudDetectionRuleSignalLibraryView.credentialCopied",
    "FraudDetectionRuleSignalLibraryView.excessiveRefreshAttempts",
    "FraudDetectionRuleSignalLibraryView.invalidSignature"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-245"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 152. 0 of 0 labels bound to a contract property; 0 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-246",
  "name": "Credential Sharing & Concurrent Usage Detection",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.3",
   "page": 154
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-sharing-concurrent-usage-detection-bo-246",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialSharingConcurrentUsageDetection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-244"
   ],
   "exitTo": [
    "BO-244"
   ],
   "inferred": false,
   "notes": "**Reached from BO-244, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-244",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F121 step 4→5",
     "operation": "listCredentialSharingConcurrent"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Detect one of the most important access-control fraud scenarios: One valid ticket being shared by multiple people or devices.",
  "purposeNote": "validation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 154"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 154"
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
       "impliedBy": "listCredentialSharingConcurrent",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential sharing concurrent list.",
   "error": "Could not load. Names which read failed and leaves the credential sharing concurrent untouched.",
   "emptyFirstRun": "No credential sharing concurrent yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential sharing concurrent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialSharingConcurrent",
    "contract": "access",
    "purpose": "Credential Sharing & Concurrent Usage Detection",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialSharingConcurrentUsageDetectionView.iphoneDeviceA",
    "CredentialSharingConcurrentUsageDetectionView.additionalDevices",
    "CredentialSharingConcurrentUsageDetectionView.maximumActiveDevices",
    "CredentialSharingConcurrentUsageDetectionView.increaseRisk",
    "CredentialSharingConcurrentUsageDetectionView.requireId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-246"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 154. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-247",
  "name": "Unified Identity & Credential Lock Manager",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.4",
   "page": 155
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/unified-identity-credential-lock-manager-bo-247",
   "component": "apps/venue-management-web/src/routes/access-venue/UnifiedIdentityCredentialLockManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-244"
   ],
   "exitTo": [
    "BO-244"
   ],
   "inferred": false,
   "notes": "**Reached from BO-244, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-244",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F121 step 6→7",
     "operation": "listUnifiedIdentityCredential"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide the single security lock required by the matrix so suspicious activity can immediately stop all access associated with an identity.",
  "purposeNote": "One security action can immediately restrict all configured access representations associated with a suspicious identity.",
  "gaps": [
   {
    "operation": null,
    "why": "**Unified Identity & Credential Lock Manager declares no operation that writes anything** — its only declared call is `listUnifiedIdentityCredential`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Every unified identity credential",
       "columns": [
        "UnifiedIdentityCredentialLockManagerView.centralPlatform",
        "UnifiedIdentityCredentialLockManagerView.venueEdge",
        "UnifiedIdentityCredentialLockManagerView.onlineGates",
        "UnifiedIdentityCredentialLockManagerView.offlineRevocationPackage",
        "UnifiedIdentityCredentialLockManagerView.mobileDevices"
       ],
       "bindsTo": "UnifiedIdentityCredentialLockManagerView",
       "operation": "listUnifiedIdentityCredential",
       "provenance": "pack Access Control Module_Reference.pdf, page 155 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected unified identity credential",
       "bindsTo": "UnifiedIdentityCredentialLockManagerView",
       "columns": [
        "UnifiedIdentityCredentialLockManagerView.centralPlatform",
        "UnifiedIdentityCredentialLockManagerView.venueEdge",
        "UnifiedIdentityCredentialLockManagerView.onlineGates",
        "UnifiedIdentityCredentialLockManagerView.offlineRevocationPackage",
        "UnifiedIdentityCredentialLockManagerView.mobileDevices"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Identity”, “Associated Credentials”, “Lock Duration”, “Unlock”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 155 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The unified identity credential list.",
   "error": "Could not load. Names which read failed and leaves the unified identity credential untouched.",
   "emptyFirstRun": "No unified identity credential yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the unified identity credential are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUnifiedIdentityCredential",
    "contract": "access",
    "purpose": "Unified Identity & Credential Lock Manager",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "UnifiedIdentityCredentialLockManagerView.centralPlatform",
    "UnifiedIdentityCredentialLockManagerView.venueEdge",
    "UnifiedIdentityCredentialLockManagerView.onlineGates",
    "UnifiedIdentityCredentialLockManagerView.offlineRevocationPackage",
    "UnifiedIdentityCredentialLockManagerView.mobileDevices"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-247"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 155. 5 of 5 labels bound to a contract property; 9 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-248",
  "name": "Biometric & Identity Integrity Monitoring",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.5",
   "page": 156
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/biometric-identity-integrity-monitoring-bo-248",
   "component": "apps/venue-management-web/src/routes/access-venue/BiometricIdentityIntegrityMonitoring.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-244"
   ],
   "exitTo": [
    "BO-244"
   ],
   "inferred": false,
   "notes": "**Reached from BO-244, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-244",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F121 step 8→9",
     "operation": "listBiometricIdentityIntegrity"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor) and no metric row",
  "purpose": "Detect suspicious biometric and identity-related changes without duplicating Board 5's biometric configuration. Board 5 configures biometrics. Board 11 monitors biometric security risk.",
  "purposeNote": "Identity changes and unusual biometric behavior automatically feed TICVAI's access-risk process.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every biometric identity integrity",
       "columns": [
        "BiometricIdentityIntegrityMonitoringView.faceChanged",
        "BiometricIdentityIntegrityMonitoringView.reEnrollment",
        "BiometricIdentityIntegrityMonitoringView.repeatedFaceMismatch",
        "multiple faces associated with one credential",
        "one face associated with multiple credentials",
        "BiometricIdentityIntegrityMonitoringView.suspiciousEnrollmentFrequency"
       ],
       "bindsTo": "BiometricIdentityIntegrityMonitoringView",
       "operation": "listBiometricIdentityIntegrity",
       "provenance": "pack Access Control Module_Reference.pdf, page 156 §Monitor"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected biometric identity integrity",
       "bindsTo": "BiometricIdentityIntegrityMonitoringView",
       "columns": [
        "BiometricIdentityIntegrityMonitoringView.faceChanged",
        "BiometricIdentityIntegrityMonitoringView.reEnrollment",
        "BiometricIdentityIntegrityMonitoringView.repeatedFaceMismatch",
        "multiple faces associated with one credential",
        "one face associated with multiple credentials",
        "BiometricIdentityIntegrityMonitoringView.suspiciousEnrollmentFrequency"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Original Face Enrollment”, “Successful Visits”, “Face Changed”, “Reason”, “Enrollment 1”, “Enrollment 2”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 156 §Monitor"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The biometric identity integrity list.",
   "error": "Could not load. Names which read failed and leaves the biometric identity integrity untouched.",
   "emptyFirstRun": "No biometric identity integrity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the biometric identity integrity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBiometricIdentityIntegrity",
    "contract": "access",
    "purpose": "Biometric & Identity Integrity Monitoring",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BiometricIdentityIntegrityMonitoringView.faceChanged",
    "BiometricIdentityIntegrityMonitoringView.reEnrollment",
    "BiometricIdentityIntegrityMonitoringView.repeatedFaceMismatch",
    "multiple faces associated with one credential",
    "one face associated with multiple credentials",
    "BiometricIdentityIntegrityMonitoringView.suspiciousEnrollmentFrequency"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-248"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 156. 4 of 6 labels bound to a contract property; 6 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-249",
  "name": "Relationship & Companion Fraud Monitoring",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.6",
   "page": 158
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/relationship-companion-fraud-monitoring-bo-249",
   "component": "apps/venue-management-web/src/routes/access-venue/RelationshipCompanionFraudMonitoring.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-244"
   ],
   "exitTo": [
    "BO-244"
   ],
   "inferred": false,
   "notes": "**Reached from BO-244, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-244",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F121 step 10→11",
     "operation": "listRelationshipCompanionFraud"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Detect abuse involving linked guests such as: Child + Adult POD + Companion Guest + Nanny Group Leader + Group Membership dependents.",
  "purposeNote": "Linked-person relationships are continuously monitored rather than checked only at initial credential creation.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Companion changed during visit",
       "provenance": "pack Access Control Module_Reference.pdf, page 158 §Configure"
      },
      {
       "kind": "textField",
       "label": "Nanny credential used without primary guest",
       "provenance": "pack Access Control Module_Reference.pdf, page 158 §Configure"
      },
      {
       "kind": "textField",
       "label": "Child enters/exits with unauthorized adult",
       "provenance": "pack Access Control Module_Reference.pdf, page 158 §Configure"
      },
      {
       "kind": "selectField",
       "label": "excessive relationship changes",
       "provenance": "pack Access Control Module_Reference.pdf, page 158 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The relationship companion fraud configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the relationship companion fraud untouched.",
   "emptyFirstRun": "No relationship companion fraud configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRelationshipCompanionFraud",
    "contract": "access",
    "purpose": "Relationship & Companion Fraud Monitoring",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-249"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 158. 0 of 0 labels bound to a contract property; 4 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-250",
  "name": "Access Risk Scoring & Decision Engine",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.7",
   "page": 159
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-risk-scoring-decision-engine-bo-250",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessRiskScoringDecisionEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-244"
   ],
   "exitTo": [
    "BO-244"
   ],
   "inferred": false,
   "notes": "**Reached from BO-244, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-244",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F121 step 12→13",
     "operation": "listAccessRiskScoring"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert multiple security signals into a unified access risk score.",
  "purposeNote": "Multiple fraud indicators produce a consistent, explainable security risk assessment.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 159"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 159"
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
       "impliedBy": "listAccessRiskScoring",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access risk scoring list.",
   "error": "Could not load. Names which read failed and leaves the access risk scoring untouched.",
   "emptyFirstRun": "No access risk scoring yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access risk scoring are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessRiskScoring",
    "contract": "access",
    "purpose": "Access Risk Scoring & Decision Engine",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AccessRiskScoringDecisionEngineView.newDevice10",
    "AccessRiskScoringDecisionEngineView.multipleSessions20",
    "AccessRiskScoringDecisionEngineView.impossibleTravel25",
    "AccessRiskScoringDecisionEngineView.previousFailedAttempts12",
    "AccessRiskScoringDecisionEngineView.faceMismatch15"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-250"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 159. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-251",
  "name": "Real-Time Security Response & Playbook Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.8",
   "page": 161
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/real-time-security-response-playbook-builder-bo-251",
   "component": "apps/venue-management-web/src/routes/access-venue/RealTimeSecurityResponsePlaybookBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-244"
   ],
   "exitTo": [
    "BO-244"
   ],
   "inferred": false,
   "notes": "**Reached from BO-244, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-244",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F121 step 14→15",
     "operation": "setRealTimeSecurity"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure what TICVAI automatically does when security conditions are detected.",
  "purposeNote": "Security responses are standardized, automated where appropriate and consistently executed across venues.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 10 actions on this screen and the screen declares 1 operation.** Unserved: Alert Only, Increase Risk Score, Require Additional Verification, Require Supervisor, Temporarily Lock, Full Identity Lock, Blacklist, Notify Security …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Access Control Module_Reference.pdf, page 161 §Available Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 161"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 161"
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
       "label": "Alert Only",
       "provenance": "pack Access Control Module_Reference.pdf, page 161 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Increase Risk Score",
       "provenance": "pack Access Control Module_Reference.pdf, page 161 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Require Additional Verification",
       "provenance": "pack Access Control Module_Reference.pdf, page 161 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Require Supervisor",
       "provenance": "pack Access Control Module_Reference.pdf, page 161 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Temporarily Lock",
       "provenance": "pack Access Control Module_Reference.pdf, page 161 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Full Identity Lock",
       "provenance": "pack Access Control Module_Reference.pdf, page 161 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Blacklist",
       "provenance": "pack Access Control Module_Reference.pdf, page 161 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify Security",
       "provenance": "pack Access Control Module_Reference.pdf, page 161 §Available Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The real-time security response list.",
   "error": "Could not load. Names which read failed and leaves the real-time security response untouched.",
   "emptyFirstRun": "No real-time security response yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the real-time security response are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRealTimeSecurity",
    "contract": "access",
    "purpose": "Real-Time Security Response & Playbook Builder",
    "trigger": "onAction",
    "invalidates": [
     "setRealTimeSecurity"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-251"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 161. 0 of 0 labels bound to a contract property; 10 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-252",
  "name": "Security Investigation & Evidence Workspace",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.9",
   "page": 162
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/security-investigation-evidence-workspace-bo-252",
   "component": "apps/venue-management-web/src/routes/access-venue/SecurityInvestigationEvidenceWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-244"
   ],
   "exitTo": [
    "BO-244"
   ],
   "inferred": false,
   "notes": "**Reached from BO-244, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-244",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F121 step 16→17",
     "operation": "setSecurityInvestigationEvidence"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide security specialists with a deeper investigation environment than Board 9's operational incident workspace.",
  "purposeNote": "Security teams can reconstruct and investigate suspicious access behavior using a unified evidence trail.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 162"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 162"
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
       "provenance": "contract operation setSecurityInvestigationEvidence"
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
       "impliedBy": "setSecurityInvestigationEvidence"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The security investigation evidence list.",
   "error": "Could not load. Names which read failed and leaves the security investigation evidence untouched.",
   "emptyFirstRun": "No security investigation evidence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the security investigation evidence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSecurityInvestigationEvidence",
    "contract": "access",
    "purpose": "Security Investigation & Evidence Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setSecurityInvestigationEvidence"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-252"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 162. 0 of 0 labels bound to a contract property; 0 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-253",
  "name": "Security Analytics, AI Detection & Governance",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "11",
   "number": "11.10",
   "page": 164
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/security-analytics-ai-detection-governance-bo-253",
   "component": "apps/venue-management-web/src/routes/access-venue/SecurityAnalyticsAiDetectionGovernance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-244"
   ],
   "exitTo": [
    "BO-244"
   ],
   "inferred": false,
   "notes": "**Reached from BO-244, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show; Measure) and no metric row",
  "purpose": "Provide long-term intelligence on fraud patterns, security controls and effectiveness.",
  "purposeNote": "Board 11 — Final 10-Screen Structure # Backend Screen Main Responsibility 11.1 Access Security & Fraud Command Center Real-time security posture 11.2 Fraud Detection Rule & Signal Library Configure fraud indicators 11.3 Credential Sharing & Concurrent Usage Detection Detect credential/device sharing 11.4 Unified Identity & Credential Lock Manager Immediately restrict compromised identities 11.5 Biometric & Identity Integrity Monitoring Detect biometric/identity anomalies 11.6 Relationship & Companion Fraud Monitoring Protect child/POD/nanny/group relationships 11.7 Access Risk Scoring & Decisi",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search security analytics detection",
       "provenance": "pack Access Control Module_Reference.pdf, page 164 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Park",
        "Event",
        "Product",
        "Channel",
        "Reseller",
        "Credential Type",
        "Media",
        "Device",
        "Gate"
       ],
       "notes": "The pack filters this screen by venue, park, event, product, channel, reseller and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Access Control Module_Reference.pdf, page 164 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every security analytics detection",
       "columns": [
        "SecurityAnalyticsAiDetectionGovernanceView.fraudAttempts",
        "SecurityAnalyticsAiDetectionGovernanceView.preventedFraud",
        "SecurityAnalyticsAiDetectionGovernanceView.credentialSharing",
        "Duplicate Usage",
        "SecurityAnalyticsAiDetectionGovernanceView.biometricAlerts",
        "SecurityAnalyticsAiDetectionGovernanceView.deviceBindingViolations",
        "SecurityAnalyticsAiDetectionGovernanceView.companionViolations",
        "SecurityAnalyticsAiDetectionGovernanceView.blacklistHits",
        "SecurityAnalyticsAiDetectionGovernanceView.identityLocks",
        "SecurityAnalyticsAiDetectionGovernanceView.detectionRate",
        "SecurityAnalyticsAiDetectionGovernanceView.falsePositiveIndicator",
        "SecurityAnalyticsAiDetectionGovernanceView.operatorOverrideRate",
        "SecurityAnalyticsAiDetectionGovernanceView.averageInvestigationTime",
        "SecurityAnalyticsAiDetectionGovernanceView.averageResponseTime",
        "SecurityAnalyticsAiDetectionGovernanceView.recurringFraudRate",
        "SecurityAnalyticsAiDetectionGovernanceView.financialExposure"
       ],
       "bindsTo": "SecurityAnalyticsAiDetectionGovernanceView",
       "operation": "listSecurityDetectionGovernance",
       "provenance": "pack Access Control Module_Reference.pdf, page 164 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected security analytics detection",
       "bindsTo": "SecurityAnalyticsAiDetectionGovernanceView",
       "columns": [
        "SecurityAnalyticsAiDetectionGovernanceView.fraudAttempts",
        "SecurityAnalyticsAiDetectionGovernanceView.preventedFraud",
        "SecurityAnalyticsAiDetectionGovernanceView.credentialSharing",
        "Duplicate Usage",
        "SecurityAnalyticsAiDetectionGovernanceView.biometricAlerts",
        "SecurityAnalyticsAiDetectionGovernanceView.deviceBindingViolations",
        "SecurityAnalyticsAiDetectionGovernanceView.companionViolations",
        "SecurityAnalyticsAiDetectionGovernanceView.blacklistHits",
        "SecurityAnalyticsAiDetectionGovernanceView.identityLocks",
        "SecurityAnalyticsAiDetectionGovernanceView.detectionRate",
        "SecurityAnalyticsAiDetectionGovernanceView.falsePositiveIndicator",
        "SecurityAnalyticsAiDetectionGovernanceView.operatorOverrideRate",
        "SecurityAnalyticsAiDetectionGovernanceView.averageInvestigationTime",
        "SecurityAnalyticsAiDetectionGovernanceView.averageResponseTime",
        "SecurityAnalyticsAiDetectionGovernanceView.recurringFraudRate",
        "SecurityAnalyticsAiDetectionGovernanceView.financialExposure"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Fraud Attempts by Sales Channel”, “Emerging Pattern Detected”, “Record changes to”, “Board 11 Key Workflow”, “A key distinction”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 164 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The security analytics detection list.",
   "error": "Could not load. Names which read failed and leaves the security analytics detection untouched.",
   "emptyFirstRun": "No security analytics detection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the security analytics detection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSecurityDetectionGovernance",
    "contract": "access",
    "purpose": "Security Analytics, AI Detection & Governance",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "SecurityAnalyticsAiDetectionGovernanceView.fraudAttempts",
    "SecurityAnalyticsAiDetectionGovernanceView.preventedFraud",
    "SecurityAnalyticsAiDetectionGovernanceView.credentialSharing",
    "Duplicate Usage",
    "SecurityAnalyticsAiDetectionGovernanceView.biometricAlerts",
    "SecurityAnalyticsAiDetectionGovernanceView.deviceBindingViolations"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-253"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 164. 15 of 26 labels bound to a contract property; 26 of 93 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listAccessRiskScoring": {
  "method": "GET",
  "path": "/access-risk-scoring",
  "contract": "access",
  "summary": "Access Risk Scoring & Decision Engine",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessRiskScoringDecisionEngineView"
 },
 "listAccessSecurityFraud": {
  "method": "GET",
  "path": "/access-security-fraud",
  "contract": "access",
  "summary": "Access Security & Fraud Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessSecurityFraudCommandCenterView"
 },
 "listBiometricIdentityIntegrity": {
  "method": "GET",
  "path": "/biometric-identity-integrity",
  "contract": "access",
  "summary": "Biometric & Identity Integrity Monitoring",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BiometricIdentityIntegrityMonitoringView"
 },
 "listCredentialSharingConcurrent": {
  "method": "GET",
  "path": "/credential-sharing-concurrent",
  "contract": "access",
  "summary": "Credential Sharing & Concurrent Usage Detection",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialSharingConcurrentUsageDetectionView"
 },
 "listFraudDetectionRule": {
  "method": "GET",
  "path": "/fraud-detection-rule",
  "contract": "access",
  "summary": "Fraud Detection Rule & Signal Library",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FraudDetectionRuleSignalLibraryView"
 },
 "listRelationshipCompanionFraud": {
  "method": "GET",
  "path": "/relationship-companion-fraud",
  "contract": "access",
  "summary": "Relationship & Companion Fraud Monitoring",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RelationshipCompanionFraudMonitoringView"
 },
 "listSecurityDetectionGovernance": {
  "method": "GET",
  "path": "/security-detection-governance",
  "contract": "access",
  "summary": "Security Analytics, AI Detection & Governance",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "park",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "reseller",
    "in": "query",
    "required": false
   },
   {
    "name": "credentialType",
    "in": "query",
    "required": false
   },
   {
    "name": "media",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "SecurityAnalyticsAiDetectionGovernanceView"
 },
 "listUnifiedIdentityCredential": {
  "method": "GET",
  "path": "/unified-identity-credential",
  "contract": "access",
  "summary": "Unified Identity & Credential Lock Manager",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "UnifiedIdentityCredentialLockManagerView"
 },
 "setRealTimeSecurity": {
  "method": "PUT",
  "path": "/real-time-security",
  "contract": "access",
  "summary": "Real-Time Security Response & Playbook Builder",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "RealTimeSecurityResponsePlaybookBuilderInput",
  "responds": "RealTimeSecurityResponsePlaybookBuilderView"
 },
 "setSecurityInvestigationEvidence": {
  "method": "PUT",
  "path": "/security-investigation-evidence",
  "contract": "access",
  "summary": "Security Investigation & Evidence Workspace",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "SecurityInvestigationEvidenceWorkspaceInput",
  "responds": "SecurityInvestigationEvidenceWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessRiskScoringDecisionEngineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Risk Scoring & Decision Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "newDevice10": {
    "type": "integer",
    "description": "New Device +10"
   },
   "multipleSessions20": {
    "type": "string",
    "description": "Multiple Sessions +20"
   },
   "impossibleTravel25": {
    "type": "string",
    "description": "Impossible Travel +25"
   },
   "previousFailedAttempts12": {
    "type": "integer",
    "description": "Previous Failed Attempts +12"
   },
   "faceMismatch15": {
    "type": "string",
    "description": "Face Mismatch +15"
   },
   "criticalLockSecurityReview": {
    "type": "string",
    "description": "Critical Lock + Security Review"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketValue": {
    "type": "string",
    "description": "Ticket Value"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "accessZone": {
    "type": "string",
    "description": "Access Zone"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "credentialType": {
    "type": "string",
    "description": "Credential type"
   },
   "historicalBehavior": {
    "type": "string",
    "description": "historical behavior"
   }
  }
 },
 "AccessSecurityFraudCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Security & Fraud Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeSecurityAlerts": {
    "type": "integer",
    "description": "Active Security Alerts"
   },
   "highRiskCredentials": {
    "type": "integer",
    "description": "High-Risk Credentials"
   },
   "credentialsLockedToday": {
    "type": "string",
    "description": "Credentials Locked Today"
   },
   "suspiciousQrActivity": {
    "type": "string",
    "description": "Suspicious QR Activity"
   },
   "deviceSharingAlerts": {
    "type": "integer",
    "description": "Device-Sharing Alerts"
   },
   "biometricAlerts": {
    "type": "integer",
    "description": "Biometric Alerts"
   },
   "blacklistedCredentials": {
    "type": "integer",
    "description": "Blacklisted Credentials"
   },
   "activeInvestigations": {
    "type": "integer",
    "description": "Active Investigations"
   },
   "fraudPrevented": {
    "type": "string",
    "description": "Fraud Prevented"
   },
   "lowRisk": {
    "type": "string",
    "description": "🟢 Low Risk"
   },
   "mediumRisk": {
    "type": "string",
    "description": "🟡 Medium Risk"
   },
   "highRisk": {
    "type": "string",
    "description": "🟠 High Risk"
   },
   "critical": {
    "type": "string",
    "description": "🔴 Critical"
   },
   "unusuallyHighReEntryAttemptsDetected": {
    "type": "integer",
    "description": "Unusually high re-entry attempts detected"
   }
  }
 },
 "BiometricIdentityIntegrityMonitoringView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric & Identity Integrity Monitoring displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "faceChanged": {
    "type": "string",
    "description": "Face changed"
   },
   "reEnrollment": {
    "type": "string",
    "description": "Re-enrollment"
   },
   "repeatedFaceMismatch": {
    "type": "string",
    "description": "repeated face mismatch"
   },
   "suspiciousEnrollmentFrequency": {
    "type": "string",
    "description": "suspicious enrollment frequency"
   },
   "unusualVerificationFailures": {
    "type": "integer",
    "description": "unusual verification failures"
   },
   "successfulVisits": {
    "type": "integer",
    "description": "Successful Visits (the pack shows 28)"
   },
   "currentVerification": {
    "type": "string",
    "description": "Current verification"
   },
   "oldBiometricReference": {
    "type": "string",
    "description": "Old biometric reference"
   },
   "newBiometricReference": {
    "type": "integer",
    "description": "New biometric reference"
   },
   "changeDate": {
    "type": "string",
    "format": "date-time",
    "description": "change date"
   },
   "location": {
    "type": "string",
    "description": "location"
   },
   "operator": {
    "type": "string",
    "description": "operator"
   },
   "verificationProcess": {
    "type": "string",
    "description": "verification process"
   },
   "reason": {
    "type": "string",
    "description": "reason"
   },
   "approval": {
    "type": "string",
    "description": "approval"
   }
  }
 },
 "CredentialSharingConcurrentUsageDetectionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Sharing & Concurrent Usage Detection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "iphoneDeviceA": {
    "type": "string",
    "description": "iPhone — Device A"
   },
   "additionalDevices": {
    "type": "integer",
    "description": "Additional Devices (the pack shows 3)"
   },
   "maximumActiveDevices": {
    "type": "integer",
    "description": "Maximum Active Devices (the pack shows 1)"
   },
   "increaseRisk": {
    "type": "string",
    "description": "Increase Risk"
   },
   "requireId": {
    "type": "string",
    "description": "Require ID"
   },
   "requireBiometric": {
    "type": "boolean",
    "description": "Require Biometric"
   },
   "requireOperator": {
    "type": "boolean",
    "description": "Require Operator"
   },
   "securityAlert": {
    "type": "string",
    "description": "Security alert"
   }
  }
 },
 "FraudDetectionRuleSignalLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Fraud Detection Rule & Signal Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "excessiveQrActivations": {
    "type": "string",
    "description": "Excessive QR activations"
   },
   "multipleActiveSessions": {
    "type": "string",
    "description": "Multiple active sessions"
   },
   "credentialCopied": {
    "type": "string",
    "description": "Credential copied"
   },
   "excessiveRefreshAttempts": {
    "type": "integer",
    "description": "Excessive refresh attempts"
   },
   "invalidSignature": {
    "type": "string",
    "description": "Invalid signature"
   },
   "expiredCredential": {
    "type": "integer",
    "description": "Expired credential"
   },
   "revokedCredential": {
    "type": "string",
    "description": "Revoked credential"
   },
   "screenshotReplayAttempt": {
    "type": "string",
    "description": "Screenshot/replay attempt"
   },
   "abnormalTransferFrequency": {
    "type": "string",
    "description": "Abnormal transfer frequency"
   },
   "repeatedFailedValidation": {
    "type": "string",
    "description": "Repeated failed validation"
   },
   "newDevice": {
    "type": "integer",
    "description": "New device"
   },
   "multipleDevices": {
    "type": "string",
    "description": "Multiple devices"
   },
   "deviceBindingMismatch": {
    "type": "string",
    "description": "Device-binding mismatch"
   },
   "rootedCompromisedDeviceWhereDetectable": {
    "type": "string",
    "description": "Rooted/compromised device where detectable"
   },
   "abnormalDeviceChanges": {
    "type": "string",
    "description": "abnormal device changes"
   },
   "impossibleDeviceMovement": {
    "type": "string",
    "description": "impossible device movement"
   },
   "suspiciousScannerDeviceActivity": {
    "type": "string",
    "description": "suspicious scanner/device activity"
   },
   "simultaneousUse": {
    "type": "string",
    "description": "simultaneous use"
   },
   "antiPassbackViolations": {
    "type": "string",
    "description": "anti-passback violations"
   },
   "unusualReEntry": {
    "type": "string",
    "description": "unusual re-entry"
   },
   "unusualCrossover": {
    "type": "string",
    "description": "unusual crossover"
   },
   "excessiveAttractionUse": {
    "type": "string",
    "description": "excessive attraction use"
   },
   "repeatedWrongGateAttempts": {
    "type": "integer",
    "description": "repeated wrong-gate attempts"
   },
   "abnormalFastPassConsumption": {
    "type": "string",
    "description": "abnormal Fast Pass consumption"
   },
   "faceMismatch": {
    "type": "string",
    "description": "Face mismatch"
   },
   "unusualFaceChange": {
    "type": "string",
    "description": "unusual face change"
   },
   "multipleIdentitiesLinked": {
    "type": "string",
    "description": "multiple identities linked"
   },
   "suspiciousCompanionChanges": {
    "type": "string",
    "description": "suspicious companion changes"
   },
   "podNannyRelationshipAnomalies": {
    "type": "string",
    "description": "POD/nanny relationship anomalies"
   },
   "gateA1002": {
    "type": "string",
    "description": "Gate A — 10:02"
   },
   "gateB1003": {
    "type": "string",
    "description": "Gate B — 10:03"
   },
   "severity": {
    "type": "string",
    "description": "Severity"
   },
   "weight": {
    "type": "string",
    "description": "Weight"
   },
   "threshold": {
    "type": "integer",
    "description": "Threshold"
   },
   "scope": {
    "type": "string",
    "description": "Scope"
   },
   "applicableCredentialTypes": {
    "type": "string",
    "description": "Applicable credential types"
   },
   "applicableVenues": {
    "type": "string",
    "description": "Applicable venues"
   },
   "timeWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Time window"
   },
   "offlineAvailability": {
    "type": "integer",
    "description": "Offline availability"
   },
   "response": {
    "type": "string",
    "description": "Response"
   }
  }
 },
 "RealTimeSecurityResponsePlaybookBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Real-Time Security Response & Playbook Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "alertOnly": {
    "type": "string",
    "description": "Alert Only"
   },
   "increaseRiskScore": {
    "type": "number",
    "description": "Increase Risk Score"
   },
   "requireAdditionalVerification": {
    "type": "boolean",
    "description": "Require Additional Verification"
   },
   "requireSupervisor": {
    "type": "boolean",
    "description": "Require Supervisor"
   },
   "temporarilyLock": {
    "type": "string",
    "description": "Temporarily Lock"
   },
   "fullIdentityLock": {
    "type": "string",
    "description": "Full Identity Lock"
   },
   "blacklist": {
    "type": "string",
    "description": "Blacklist"
   },
   "after": {
    "type": "string",
    "description": "after"
   }
  }
 },
 "RealTimeSecurityResponsePlaybookBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Real-Time Security Response & Playbook Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "alertOnly": {
    "type": "string",
    "description": "Alert Only"
   },
   "increaseRiskScore": {
    "type": "number",
    "description": "Increase Risk Score"
   },
   "requireAdditionalVerification": {
    "type": "boolean",
    "description": "Require Additional Verification"
   },
   "requireSupervisor": {
    "type": "boolean",
    "description": "Require Supervisor"
   },
   "temporarilyLock": {
    "type": "string",
    "description": "Temporarily Lock"
   },
   "fullIdentityLock": {
    "type": "string",
    "description": "Full Identity Lock"
   },
   "blacklist": {
    "type": "string",
    "description": "Blacklist"
   },
   "after": {
    "type": "string",
    "description": "after"
   }
  }
 },
 "RelationshipCompanionFraudMonitoringView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Relationship & Companion Fraud Monitoring displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "differentCompanionBAttemptedEntry": {
    "type": "string",
    "description": "Different Companion B attempted entry"
   },
   "companionChangedDuringVisit": {
    "type": "string",
    "description": "Companion changed during visit"
   },
   "childEntersExitsWithUnauthorizedAdult": {
    "type": "string",
    "description": "Child enters/exits with unauthorized adult"
   },
   "excessiveRelationshipChanges": {
    "type": "string",
    "description": "excessive relationship changes"
   },
   "relationshipChangeAttempt": {
    "type": "string",
    "description": "Relationship Change Attempt"
   },
   "yellowIntervention": {
    "type": "string",
    "description": "Yellow intervention"
   },
   "supervisorVerification": {
    "type": "string",
    "description": "Supervisor verification"
   },
   "idVerification": {
    "type": "string",
    "description": "ID verification"
   },
   "biometricVerification": {
    "type": "string",
    "description": "Biometric verification"
   },
   "securityEscalation": {
    "type": "string",
    "description": "Security escalation"
   },
   "accessDenial": {
    "type": "string",
    "description": "Access denial"
   }
  }
 },
 "SecurityAnalyticsAiDetectionGovernanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Security Analytics, AI Detection & Governance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fraudAttempts": {
    "type": "integer",
    "description": "Fraud Attempts"
   },
   "preventedFraud": {
    "type": "string",
    "description": "Prevented Fraud"
   },
   "credentialSharing": {
    "type": "string",
    "description": "Credential Sharing"
   },
   "biometricAlerts": {
    "type": "integer",
    "description": "Biometric Alerts"
   },
   "deviceBindingViolations": {
    "type": "integer",
    "description": "Device-Binding Violations"
   },
   "companionViolations": {
    "type": "integer",
    "description": "Companion Violations"
   },
   "blacklistHits": {
    "type": "integer",
    "description": "Blacklist Hits"
   },
   "identityLocks": {
    "type": "integer",
    "description": "Identity Locks"
   },
   "securityOverrides": {
    "type": "integer",
    "description": "Security Overrides"
   },
   "web8": {
    "type": "number",
    "description": "Web: 8%"
   },
   "pos3": {
    "type": "number",
    "description": "POS: 3%"
   },
   "b2b12": {
    "type": "number",
    "description": "B2B: 12%"
   },
   "resellerX41": {
    "type": "number",
    "description": "Reseller X: 41%"
   },
   "resellerY7": {
    "type": "number",
    "description": "Reseller Y: 7%"
   },
   "detectionRate": {
    "type": "number",
    "description": "Detection Rate"
   },
   "falsePositiveIndicator": {
    "type": "string",
    "description": "False Positive Indicator"
   },
   "operatorOverrideRate": {
    "type": "number",
    "description": "Operator Override Rate"
   },
   "averageInvestigationTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Investigation Time"
   },
   "averageResponseTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Response Time"
   },
   "recurringFraudRate": {
    "type": "number",
    "description": "Recurring Fraud Rate"
   },
   "financialExposure": {
    "type": "string",
    "description": "Financial Exposure"
   },
   "estimatedFraudPrevented": {
    "type": "string",
    "description": "Estimated Fraud Prevented"
   },
   "fraudRules": {
    "type": "string",
    "description": "fraud rules"
   },
   "thresholds": {
    "type": "string",
    "description": "thresholds"
   },
   "riskModels": {
    "type": "string",
    "description": "risk models"
   },
   "responsePlaybooks": {
    "type": "string",
    "description": "response playbooks"
   },
   "blacklistPolicies": {
    "type": "string",
    "description": "blacklist policies"
   },
   "aiRecommendations": {
    "type": "string",
    "description": "AI recommendations"
   },
   "patternImproveControls": {
    "type": "string",
    "description": "Pattern → Improve Controls"
   },
   "board3CredentialSecurity": {
    "type": "string",
    "description": "Board 3 — Credential Security"
   },
   "board5BiometricAccess": {
    "type": "string",
    "description": "Board 5 — Biometric Access"
   },
   "board9LiveOperations": {
    "type": "string",
    "description": "Board 9 — Live Operations"
   },
   "board10DynamicPolicy": {
    "type": "string",
    "description": "Board 10 — Dynamic Policy"
   },
   "contextualConditions": {
    "type": "string",
    "description": "contextual conditions"
   },
   "abusiveCompromisedOrFraudulent": {
    "type": "string",
    "description": "abusive, compromised or fraudulent"
   }
  }
 },
 "SecurityInvestigationEvidenceWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Security Investigation & Evidence Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "critical91": {
    "type": "string",
    "description": "CRITICAL — 91"
   },
   "operatorIntervention": {
    "type": "string",
    "description": "Operator Intervention"
   },
   "credentialHistory": {
    "type": "string",
    "description": "Credential history"
   },
   "scanRecords": {
    "type": "string",
    "description": "Scan records"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "deviceIds": {
    "type": "string",
    "description": "device IDs"
   },
   "qrActivations": {
    "type": "string",
    "description": "QR activations"
   },
   "mediaChanges": {
    "type": "string",
    "description": "media changes"
   },
   "biometricEvents": {
    "type": "string",
    "description": "biometric events"
   },
   "companionRelationships": {
    "type": "string",
    "description": "companion relationships"
   },
   "posTicketTransactionReference": {
    "type": "string",
    "description": "POS/ticket transaction reference"
   },
   "overrides": {
    "type": "string",
    "description": "overrides"
   },
   "blacklistEvents": {
    "type": "string",
    "description": "blacklist events"
   },
   "securityPolicies": {
    "type": "string",
    "description": "security policies"
   },
   "blacklist": {
    "type": "string",
    "description": "Blacklist"
   },
   "clearRisk": {
    "type": "string",
    "description": "Clear Risk"
   }
  }
 },
 "SecurityInvestigationEvidenceWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Security Investigation & Evidence Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "critical91": {
    "type": "string",
    "description": "CRITICAL — 91"
   },
   "operatorIntervention": {
    "type": "string",
    "description": "Operator Intervention"
   },
   "credentialHistory": {
    "type": "string",
    "description": "Credential history"
   },
   "scanRecords": {
    "type": "string",
    "description": "Scan records"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "deviceIds": {
    "type": "string",
    "description": "device IDs"
   },
   "qrActivations": {
    "type": "string",
    "description": "QR activations"
   },
   "mediaChanges": {
    "type": "string",
    "description": "media changes"
   },
   "biometricEvents": {
    "type": "string",
    "description": "biometric events"
   },
   "companionRelationships": {
    "type": "string",
    "description": "companion relationships"
   },
   "posTicketTransactionReference": {
    "type": "string",
    "description": "POS/ticket transaction reference"
   },
   "overrides": {
    "type": "string",
    "description": "overrides"
   },
   "blacklistEvents": {
    "type": "string",
    "description": "blacklist events"
   },
   "securityPolicies": {
    "type": "string",
    "description": "security policies"
   },
   "blacklist": {
    "type": "string",
    "description": "Blacklist"
   },
   "clearRisk": {
    "type": "string",
    "description": "Clear Risk"
   }
  }
 },
 "UnifiedIdentityCredentialLockManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Unified Identity & Credential Lock Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestJohnSmith": {
    "type": "string",
    "description": "Guest: John Smith"
   },
   "ticketVc18274": {
    "type": "string",
    "description": "Ticket VC-18274"
   },
   "rfidWristbandRf8291": {
    "type": "string",
    "description": "RFID Wristband RF-8291"
   },
   "dynamicQr": {
    "type": "string",
    "description": "Dynamic QR"
   },
   "walletCredential": {
    "type": "string",
    "description": "Wallet Credential"
   },
   "facePass": {
    "type": "string",
    "description": "Face Pass"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "fastPass": {
    "type": "string",
    "description": "Fast Pass"
   },
   "selectType": {
    "type": "string",
    "enum": [
     "credentialOnly",
     "mediaOnly",
     "entitlement",
     "venue",
     "allVenueAccess",
     "fullIdentity"
    ],
    "description": "Vocabulary listed under Select."
   },
   "untilManuallyReleased": {
    "type": "string",
    "format": "date-time",
    "description": "Until manually released"
   },
   "endOfDay": {
    "type": "string",
    "description": "End of day"
   },
   "nHours": {
    "type": "string",
    "description": "N hours"
   },
   "untilInvestigationComplete": {
    "type": "string",
    "format": "date-time",
    "description": "Until investigation complete"
   },
   "permanent": {
    "type": "string",
    "description": "Permanent"
   },
   "centralPlatform": {
    "type": "string",
    "description": "Central Platform ✓"
   },
   "venueEdge": {
    "type": "string",
    "description": "Venue Edge ✓"
   },
   "onlineGates": {
    "type": "integer",
    "description": "Online Gates ✓"
   },
   "offlineRevocationPackage": {
    "type": "integer",
    "description": "Offline Revocation Package ✓"
   },
   "mobileDevices": {
    "type": "string",
    "description": "Mobile Devices ✓"
   }
  }
 }
}
```
