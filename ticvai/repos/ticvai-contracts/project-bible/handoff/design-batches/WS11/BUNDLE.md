# WS11 — Access Control board 11

**10 screens · 11 operations · 10 schemas · 3 permissions**

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
  `ACCESS_POINT_CONFIGURE, REPORT_VIEW_VENUE, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-244` | Access Security & Fraud Command Center | listDetail | 1 | 0 | — |
| `BO-245` | Fraud Detection Rule & Signal Library | listDetail | 2 | 0 | — |
| `BO-246` | Credential Sharing & Concurrent Usage Detection | listDetail | 1 | 0 | — |
| `BO-247` | Unified Identity & Credential Lock Manager | listDetail | 1 | 0 | — |
| `BO-248` | Biometric & Identity Integrity Monitoring | listDetail | 2 | 0 | — |
| `BO-249` | Relationship & Companion Fraud Monitoring | configEditor | 1 | 0 | — |
| `BO-250` | Access Risk Scoring & Decision Engine | listDetail | 1 | 0 | — |
| `BO-251` | Real-Time Security Response & Playbook Builder | listDetail | 1 | 0 | — |
| `BO-252` | Security Investigation & Evidence Workspace | listDetail | 1 | 0 | — |
| `BO-253` | Security Analytics, AI Detection & Governance | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-245, BO-246, BO-247, BO-248, BO-250, BO-252 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — BO-100 declares entryState.params  and BO-244 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
  "purposeNote": "Security teams can understand the overall fraud and access-security posture from one screen.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide security teams with a real-time command center for access-related fraud and suspicious activity across all venues.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Security Alerts",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.activeSecurityAlerts",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "High-Risk Credentials",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.highRiskCredentials",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Credentials Locked Today",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.credentialsLockedToday",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Suspicious QR Activity",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.suspiciousQrActivity",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Device-Sharing Alerts",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.deviceSharingAlerts",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Biometric Alerts",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.biometricAlerts",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Blacklisted Credentials",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.blacklistedCredentials",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Active Investigations",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.activeInvestigations",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Fraud attempts prevented today",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.fraudPrevented",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Share of today's validations at low risk, percent",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.lowRisk",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Share at medium risk, percent",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.mediumRisk",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Share at high risk, percent",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.highRisk",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Share at critical risk, percent",
       "bindsTo": "AccessSecurityFraudCommandCenterViewSummary.critical",
       "operation": "listAccessSecurityFraud",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every access security fraud",
       "columns": [
        "Duplicate Access Attempts"
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
        "Duplicate Access Attempts"
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
    "AccessSecurityFraudCommandCenterViewSummary.activeSecurityAlerts",
    "AccessSecurityFraudCommandCenterViewSummary.highRiskCredentials",
    "AccessSecurityFraudCommandCenterViewSummary.credentialsLockedToday",
    "AccessSecurityFraudCommandCenterViewSummary.suspiciousQrActivity",
    "AccessSecurityFraudCommandCenterViewSummary.deviceSharingAlerts",
    "AccessSecurityFraudCommandCenterViewSummary.biometricAlerts"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-244",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-244"
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
  "purposeNote": "Fraud detection logic is configurable rather than hard-coded.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the signals TICVAI uses to identify suspicious access behavior.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save fraud rule",
       "operation": "setFraudDetectionRule",
       "provenance": "contract access.yaml PUT /fraud-detection-rule (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setFraudDetectionRule",
    "contract": "access",
    "purpose": "Save fraud rule",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "FraudDetectionRuleSignalLibraryView.signal"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-245",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-245"
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
  "purposeNote": "validation.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Detect one of the most important access-control fraud scenarios: One valid ticket being shared by multiple people or devices.",
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
    "CredentialSharingConcurrentUsageDetectionView.additionalDevices",
    "CredentialSharingConcurrentUsageDetectionView.maximumActiveDevices",
    "CredentialSharingConcurrentUsageDetectionView.responseActions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-246",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-246"
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
  "purposeNote": "One security action can immediately restrict all configured access representations associated with a suspicious identity.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide the single security lock required by the matrix so suspicious activity can immediately stop all access associated with an identity.",
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
        "UnifiedIdentityCredentialLockManagerView.propagatedTo"
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
        "UnifiedIdentityCredentialLockManagerView.propagatedTo"
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
    "UnifiedIdentityCredentialLockManagerView.propagatedTo"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-247",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-247"
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
  "purposeNote": "Identity changes and unusual biometric behavior automatically feed TICVAI's access-risk process.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor) and no metric row",
  "purpose": "Detect suspicious biometric and identity-related changes without duplicating Board 5's biometric configuration. Board 5 configures biometrics. Board 11 monitors biometric security risk.",
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
        "BiometricIdentityIntegrityMonitoringView.anomalyType",
        "multiple faces associated with one credential",
        "one face associated with multiple credentials"
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
        "BiometricIdentityIntegrityMonitoringView.anomalyType",
        "multiple faces associated with one credential",
        "one face associated with multiple credentials"
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
   },
   {
    "operationId": "setSecurityInvestigationEvidence",
    "contract": "access",
    "purpose": "Open an investigation on a flagged face change or mismatch",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listBiometricIdentityIntegrity"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "BiometricIdentityIntegrityMonitoringView.anomalyType",
    "multiple faces associated with one credential",
    "one face associated with multiple credentials"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-248",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-248"
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
  "purposeNote": "Linked-person relationships are continuously monitored rather than checked only at initial credential creation.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Detect abuse involving linked guests such as: Child + Adult POD + Companion Guest + Nanny Group Leader + Group Membership dependents.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-249",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-249"
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
  "purposeNote": "Multiple fraud indicators produce a consistent, explainable security risk assessment.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert multiple security signals into a unified access risk score.",
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
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-250",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-250"
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
  "purposeNote": "Security responses are standardized, automated where appropriate and consistently executed across venues.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure what TICVAI automatically does when security conditions are detected.",
  "gaps": [
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-251",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-251"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 161. 0 of 0 labels bound to a contract property; 10 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Alert Only, Increase Risk Score, Require Additional Verification, Require Supervisor, Temporarily Lock, Full Identity Lock, Blacklist, Notify Security … are choices sent by `setRealTimeSecurity`.",
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
  "purposeNote": "Security teams can reconstruct and investigate suspicious access behavior using a unified evidence trail.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide security specialists with a deeper investigation environment than Board 9's operational incident workspace.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-252",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-252"
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
  "purposeNote": "Board 11 — Final 10-Screen Structure # Backend Screen Main Responsibility 11.1 Access Security & Fraud Command Center Real-time security posture 11.2 Fraud Detection Rule & Signal Library Configure fraud indicators 11.3 Credential Sharing & Concurrent Usage Detection Detect credential/device sharing 11.4 Unified Identity & Credential Lock Manager Immediately restrict compromised identities 11.5 Biometric & Identity Integrity Monitoring Detect biometric/identity anomalies 11.6 Relationship & Companion Fraud Monitoring Protect child/POD/nanny/group relationships 11.7 Access Risk Scoring & Decisi",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show; Measure) and no metric row",
  "purpose": "Provide long-term intelligence on fraud patterns, security controls and effectiveness.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-253",
   "workshopBoard": "wireframes/WS28 Access Control Board 11.dc.html#bo-253"
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
    "name": "zone",
    "in": "query",
    "required": false
   },
   {
    "name": "gate",
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
 "listBiometricIdentityIntegrity": {
  "method": "GET",
  "path": "/biometric-identity-integrity",
  "contract": "access",
  "summary": "Biometric & Identity Integrity Monitoring",
  "permission": "SCOPE_VIEW",
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
 "listCredentialSharingConcurrent": {
  "method": "GET",
  "path": "/credential-sharing-concurrent",
  "contract": "access",
  "summary": "Credential Sharing & Concurrent Usage Detection",
  "permission": "SCOPE_VIEW",
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
  "permission": "REPORT_VIEW_VENUE",
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
   },
   {
    "name": "device",
    "in": "query",
    "required": false
   },
   {
    "name": "gate",
    "in": "query",
    "required": false
   },
   {
    "name": "timeDay",
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
 "setFraudDetectionRule": {
  "method": "PUT",
  "path": "/fraud-detection-rule",
  "contract": "access",
  "summary": "Save an access fraud detection rule",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "FraudDetectionRuleSignalLibraryInput",
  "responds": "FraudDetectionRuleSignalLibraryView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
   "riskFactors": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "venue",
      "product",
      "ticketValue",
      "event",
      "accessZone",
      "time",
      "credentialType",
      "historicalBehavior"
     ]
    },
    "description": "Context the score may depend on"
   },
   "mediumThreshold": {
    "type": "integer",
    "description": "Score from which risk is medium (pack: 30)"
   },
   "highThreshold": {
    "type": "integer",
    "description": "Score from which risk is high (pack: 60)"
   },
   "criticalThreshold": {
    "type": "integer",
    "description": "Score from which risk is critical (pack: 80)"
   }
  }
 },
 "FraudDetectionRuleSignalLibraryInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Fraud Detection Rule & Signal Library submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "signal",
   "severity",
   "threshold",
   "timeWindow",
   "response"
  ],
  "properties": {
   "ruleId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent creates a rule"
   },
   "signal": {
    "type": "string",
    "enum": [
     "excessiveQrActivations",
     "multipleActiveSessions",
     "credentialCopied",
     "excessiveRefreshAttempts",
     "invalidSignature",
     "expiredCredential",
     "revokedCredential",
     "screenshotReplayAttempt",
     "abnormalTransferFrequency",
     "repeatedFailedValidation",
     "newDevice",
     "multipleDevices",
     "deviceBindingMismatch",
     "rootedCompromisedDevice",
     "abnormalDeviceChanges",
     "impossibleDeviceMovement",
     "suspiciousScannerDeviceActivity",
     "duplicateEntry",
     "simultaneousUse",
     "antiPassbackViolations",
     "unusualReEntry",
     "unusualCrossover",
     "excessiveAttractionUse",
     "repeatedWrongGateAttempts",
     "abnormalFastPassConsumption",
     "faceMismatch",
     "unusualFaceChange",
     "multipleIdentitiesLinked",
     "suspiciousCompanionChanges",
     "podNannyRelationshipAnomalies"
    ]
   },
   "signalCategory": {
    "type": "string",
    "enum": [
     "credential",
     "device",
     "access",
     "identity"
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
   "weight": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "description": "Contribution to the access risk score"
   },
   "threshold": {
    "type": "integer",
    "minimum": 1,
    "description": "Occurrences within timeWindow that fire the rule"
   },
   "timeWindow": {
    "type": "integer",
    "minimum": 1,
    "description": "Minutes"
   },
   "scope": {
    "type": "string",
    "description": "Scope path the rule applies to; empty is the whole tenant"
   },
   "applicableCredentialTypes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "applicableVenues": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "offlineAvailability": {
    "type": "boolean",
    "default": false,
    "description": "Evaluated on the gate when offline"
   },
   "response": {
    "type": "string",
    "enum": [
     "alertOnly",
     "increaseRiskScore",
     "requireAdditionalVerification",
     "requireSupervisor",
     "temporarilyLock",
     "fullIdentityLock",
     "blacklist"
    ],
    "default": "alertOnly"
   },
   "enabled": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "FraudDetectionRuleSignalLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Fraud Detection Rule & Signal Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "signal": {
    "type": "string",
    "enum": [
     "excessiveQrActivations",
     "multipleActiveSessions",
     "credentialCopied",
     "excessiveRefreshAttempts",
     "invalidSignature",
     "expiredCredential",
     "revokedCredential",
     "screenshotReplayAttempt",
     "abnormalTransferFrequency",
     "repeatedFailedValidation",
     "newDevice",
     "multipleDevices",
     "deviceBindingMismatch",
     "rootedCompromisedDevice",
     "abnormalDeviceChanges",
     "impossibleDeviceMovement",
     "suspiciousScannerDeviceActivity",
     "duplicateEntry",
     "simultaneousUse",
     "antiPassbackViolations",
     "unusualReEntry",
     "unusualCrossover",
     "excessiveAttractionUse",
     "repeatedWrongGateAttempts",
     "abnormalFastPassConsumption",
     "faceMismatch",
     "unusualFaceChange",
     "multipleIdentitiesLinked",
     "suspiciousCompanionChanges",
     "podNannyRelationshipAnomalies"
    ],
    "description": "The fraud signal this rule configures"
   },
   "severity": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Severity"
   },
   "weight": {
    "type": "integer",
    "description": "Points the signal adds to the access risk score"
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
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Applicable credential types"
   },
   "applicableVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Applicable venues"
   },
   "timeWindow": {
    "type": "integer",
    "description": "Window the threshold is counted over, in minutes"
   },
   "offlineAvailability": {
    "type": "boolean",
    "description": "Whether the signal is evaluated offline at the edge"
   },
   "response": {
    "type": "string",
    "enum": [
     "alertOnly",
     "increaseRiskScore",
     "requireAdditionalVerification",
     "requireSupervisor",
     "temporarilyLock",
     "fullIdentityLock",
     "blacklist"
    ],
    "description": "Response"
   },
   "signalCategory": {
    "type": "string",
    "enum": [
     "credential",
     "device",
     "access",
     "identity"
    ]
   },
   "enabled": {
    "type": "boolean"
   }
  },
  "required": [
   "ruleId",
   "signal"
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
 "RealTimeSecurityResponsePlaybookBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Real-Time Security Response & Playbook Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "triggerCondition": {
    "type": "string",
    "description": "e.g. Risk Score > 75 AND signal = simultaneousUse"
   },
   "name": {
    "type": "string"
   },
   "playbookId": {
    "type": "string"
   },
   "responseActions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "alertOnly",
      "increaseRiskScore",
      "requireAdditionalVerification",
      "requireSupervisor",
      "temporarilyLock",
      "fullIdentityLock",
      "blacklist",
      "notifySecurity",
      "createIncident",
      "notifyGuestServices",
      "triggerEdgeDistribution"
     ]
    },
    "description": "Actions the playbook runs when triggered"
   },
   "acknowledgeWithinMinutes": {
    "type": "integer"
   },
   "escalateToRole": {
    "type": "string",
    "description": "e.g. Security Supervisor"
   },
   "escalateAfterMinutes": {
    "type": "integer"
   },
   "enabled": {
    "type": "boolean"
   }
  },
  "required": [
   "playbookId",
   "name",
   "triggerCondition",
   "responseActions"
  ]
 },
 "RealTimeSecurityResponsePlaybookBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Real-Time Security Response & Playbook Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "triggerCondition": {
    "type": "string",
    "description": "e.g. Risk Score > 75 AND signal = simultaneousUse"
   },
   "name": {
    "type": "string"
   },
   "playbookId": {
    "type": "string"
   },
   "responseActions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "alertOnly",
      "increaseRiskScore",
      "requireAdditionalVerification",
      "requireSupervisor",
      "temporarilyLock",
      "fullIdentityLock",
      "blacklist",
      "notifySecurity",
      "createIncident",
      "notifyGuestServices",
      "triggerEdgeDistribution"
     ]
    },
    "description": "Actions the playbook runs when triggered"
   },
   "acknowledgeWithinMinutes": {
    "type": "integer"
   },
   "escalateToRole": {
    "type": "string",
    "description": "e.g. Security Supervisor"
   },
   "escalateAfterMinutes": {
    "type": "integer"
   },
   "enabled": {
    "type": "boolean"
   }
  },
  "required": [
   "playbookId",
   "name",
   "triggerCondition",
   "responseActions"
  ]
 },
 "RelationshipCompanionFraudMonitoringView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Relationship & Companion Fraud Monitoring displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "ruleType": {
    "type": "string",
    "enum": [
     "companionChangedDuringVisit",
     "nannyCredentialWithoutPrimaryGuest",
     "childWithUnauthorizedAdult",
     "companionLinkedToMultiplePrimaries",
     "excessiveRelationshipChanges",
     "groupLeaderAcrossUnrelatedGroups"
    ]
   },
   "responses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "yellowIntervention",
      "supervisorVerification",
      "idVerification",
      "biometricVerification",
      "securityEscalation",
      "accessDenial"
     ]
    }
   },
   "relationshipType": {
    "type": "string",
    "enum": [
     "childAdult",
     "podCompanion",
     "guestNanny",
     "groupLeaderGroup",
     "membershipDependent"
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
   "enabled": {
    "type": "boolean"
   }
  },
  "required": [
   "ruleId",
   "ruleType"
  ]
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
    "type": "integer",
    "description": "Prevented Fraud"
   },
   "credentialSharing": {
    "type": "integer",
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
   "detectionRate": {
    "type": "number",
    "description": "Detection Rate"
   },
   "falsePositiveIndicator": {
    "type": "number",
    "description": "False Positive Indicator"
   },
   "operatorOverrideRate": {
    "type": "number",
    "description": "Operator Override Rate"
   },
   "averageInvestigationTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "averageResponseTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "recurringFraudRate": {
    "type": "number",
    "description": "Recurring Fraud Rate"
   },
   "financialExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Financial Exposure"
   },
   "estimatedFraudPrevented": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated Fraud Prevented"
   },
   "duplicateUsage": {
    "type": "integer"
   }
  }
 },
 "SecurityInvestigationEvidenceWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Security Investigation & Evidence Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "investigationId": {
    "type": "string"
   },
   "evidenceSources": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "credentialHistory",
      "scanRecords",
      "gate",
      "deviceIds",
      "qrActivations",
      "mediaChanges",
      "transferHistory",
      "biometricEvents",
      "companionRelationships",
      "posTicketTransactionReference",
      "overrides",
      "blacklistEvents",
      "securityPolicies"
     ]
    },
    "description": "Sources correlated into this investigation"
   },
   "subjectCredentialId": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "actionTaken",
     "resolved",
     "closed"
    ]
   },
   "riskScore": {
    "type": "integer"
   },
   "riskLevel": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "notes": {
    "type": "string"
   },
   "linkedIncidentId": {
    "type": "string"
   }
  },
  "required": [
   "investigationId"
  ]
 },
 "SecurityInvestigationEvidenceWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Security Investigation & Evidence Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "investigationId": {
    "type": "string"
   },
   "evidenceSources": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "credentialHistory",
      "scanRecords",
      "gate",
      "deviceIds",
      "qrActivations",
      "mediaChanges",
      "transferHistory",
      "biometricEvents",
      "companionRelationships",
      "posTicketTransactionReference",
      "overrides",
      "blacklistEvents",
      "securityPolicies"
     ]
    },
    "description": "Sources correlated into this investigation"
   },
   "subjectCredentialId": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "actionTaken",
     "resolved",
     "closed"
    ]
   },
   "riskScore": {
    "type": "integer"
   },
   "riskLevel": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "notes": {
    "type": "string"
   },
   "linkedIncidentId": {
    "type": "string"
   }
  },
  "required": [
   "investigationId"
  ]
 }
}
```
