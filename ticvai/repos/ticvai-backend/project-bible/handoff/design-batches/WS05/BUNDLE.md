# WS05 — Access Control board 5

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
| `BO-184` | Biometric Access Command Center | listDetail | 1 | 0 | — |
| `BO-185` | Biometric Verification Profile Builder | configEditor | 1 | 0 | — |
| `BO-186` | Face Pass Enrollment Configuration | configEditor | 1 | 0 | — |
| `BO-187` | Biometric Consent & Guardian Management | configEditor | 1 | 0 | — |
| `BO-188` | Face Tag Temporary Enrollment | configEditor | 1 | 0 | — |
| `BO-189` | Face Matching & Verification Thresholds | configEditor | 1 | 0 | — |
| `BO-190` | Face Change, Re-enrollment & Identity Protection | listDetail | 1 | 0 | — |
| `BO-191` | Biometric Validation at Gate | listDetail | 1 | 0 | — |
| `BO-192` | Biometric Lifecycle, Retention & Deletion | configEditor | 1 | 0 | — |
| `BO-193` | Biometric Simulation, Audit & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-184, BO-188, BO-190, BO-191 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-184",
  "name": "Biometric Access Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.1",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/biometric-access-command-center-bo-184",
   "component": "apps/venue-management-web/src/routes/access-venue/BiometricAccessCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-185",
    "BO-186",
    "BO-187",
    "BO-188",
    "BO-189",
    "BO-190",
    "BO-191",
    "BO-192",
    "BO-193"
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
     "to": "BO-185",
     "trigger": "Works in Biometric Verification Profile Builder",
     "provenance": "flow F115 step 1→2",
     "operation": "listBiometricAccess"
    },
    {
     "to": "BO-186",
     "trigger": "Works in Face Pass Enrollment Configuration",
     "provenance": "flow F115 step 3→4",
     "operation": "listBiometricAccess"
    },
    {
     "to": "BO-187",
     "trigger": "Works in Biometric Consent & Guardian Management",
     "provenance": "flow F115 step 5→6",
     "operation": "listBiometricAccess"
    },
    {
     "to": "BO-188",
     "trigger": "Works in Face Tag Temporary Enrollment",
     "provenance": "flow F115 step 7→8",
     "operation": "listBiometricAccess"
    },
    {
     "to": "BO-189",
     "trigger": "Works in Face Matching & Verification Thresholds",
     "provenance": "flow F115 step 9→10",
     "operation": "listBiometricAccess"
    },
    {
     "to": "BO-190",
     "trigger": "Works in Face Change, Re-enrollment & Identity Protection",
     "provenance": "flow F115 step 11→12",
     "operation": "listBiometricAccess"
    },
    {
     "to": "BO-191",
     "trigger": "Works in Biometric Validation at Gate",
     "provenance": "flow F115 step 13→14",
     "operation": "listBiometricAccess"
    },
    {
     "to": "BO-192",
     "trigger": "Works in Biometric Lifecycle, Retention & Deletion",
     "provenance": "flow F115 step 15→16",
     "operation": "listBiometricAccess"
    },
    {
     "to": "BO-193",
     "trigger": "Works in Biometric Simulation, Audit & Publication",
     "provenance": "flow F115 step 17→18",
     "operation": "listBiometricAccess"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Central dashboard for biometric access configuration and operational health.",
  "purposeNote": "Authorized administrators can monitor and manage the biometric-access environment from one location.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every biometric access",
       "columns": [
        "BiometricAccessCommandCenterView.activeFacePassProfiles",
        "BiometricAccessCommandCenterView.activeFaceTags",
        "BiometricAccessCommandCenterView.enrollmentsToday",
        "BiometricAccessCommandCenterView.successfulFaceVerifications",
        "BiometricAccessCommandCenterView.failedVerifications",
        "BiometricAccessCommandCenterView.manualReviews",
        "BiometricAccessCommandCenterView.reEnrollmentRequests",
        "BiometricAccessCommandCenterView.blockedFaceChanges",
        "BiometricAccessCommandCenterView.profilesPendingDeletion",
        "BiometricAccessCommandCenterView.cameraReaderHealth",
        "BiometricAccessCommandCenterView.biometricSecurityAlerts"
       ],
       "bindsTo": "BiometricAccessCommandCenterView",
       "operation": "listBiometricAccess",
       "provenance": "pack Access Control Module_Reference.pdf, page 56 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected biometric access",
       "bindsTo": "BiometricAccessCommandCenterView",
       "columns": [
        "BiometricAccessCommandCenterView.activeFacePassProfiles",
        "BiometricAccessCommandCenterView.activeFaceTags",
        "BiometricAccessCommandCenterView.enrollmentsToday",
        "BiometricAccessCommandCenterView.successfulFaceVerifications",
        "BiometricAccessCommandCenterView.failedVerifications",
        "BiometricAccessCommandCenterView.manualReviews",
        "BiometricAccessCommandCenterView.reEnrollmentRequests",
        "BiometricAccessCommandCenterView.blockedFaceChanges",
        "BiometricAccessCommandCenterView.profilesPendingDeletion",
        "BiometricAccessCommandCenterView.cameraReaderHealth",
        "BiometricAccessCommandCenterView.biometricSecurityAlerts"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Profile Type Credential Venue Status”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 56 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The biometric access list.",
   "error": "Could not load. Names which read failed and leaves the biometric access untouched.",
   "emptyFirstRun": "No biometric access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the biometric access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBiometricAccess",
    "contract": "access",
    "purpose": "Biometric Access Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BiometricAccessCommandCenterView.activeFacePassProfiles",
    "BiometricAccessCommandCenterView.activeFaceTags",
    "BiometricAccessCommandCenterView.enrollmentsToday",
    "BiometricAccessCommandCenterView.successfulFaceVerifications",
    "BiometricAccessCommandCenterView.failedVerifications",
    "BiometricAccessCommandCenterView.manualReviews"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-184"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 56. 11 of 11 labels bound to a contract property; 11 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-185",
  "name": "Biometric Verification Profile Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.2",
   "page": 58
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/biometric-verification-profile-builder-bo-185",
   "component": "apps/venue-management-web/src/routes/access-venue/BiometricVerificationProfileBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-184"
   ],
   "exitTo": [
    "BO-184"
   ],
   "inferred": false,
   "notes": "**Reached from BO-184, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-184",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F115 step 2→3",
     "operation": "setBiometricVerificationProfile"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population",
  "purpose": "Configure which ticket/credential types can or must use biometric verification. The matrix specifically requires biometric checks to be configurable by ticket type, including memberships, annual passes, multi-day and multi-attraction products.",
  "purposeNote": "Biometric requirements can be activated or deactivated by product, credential and access location without development.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Ticket Product",
       "provenance": "pack Access Control Module_Reference.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Ticket Type",
       "provenance": "pack Access Control Module_Reference.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Access Control Module_Reference.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Annual Pass",
       "provenance": "pack Access Control Module_Reference.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Multi-Day Ticket",
       "provenance": "pack Access Control Module_Reference.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Multi-Attraction Ticket",
       "provenance": "pack Access Control Module_Reference.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "VIP Credential",
       "provenance": "pack Access Control Module_Reference.pdf, page 58 §Select"
      },
      {
       "kind": "selectField",
       "label": "Accreditation",
       "provenance": "pack Access Control Module_Reference.pdf, page 58 §Select"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setBiometricVerificationProfile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The biometric verification profile configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the biometric verification profile untouched.",
   "emptyFirstRun": "No biometric verification profile configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setBiometricVerificationProfile",
    "contract": "access",
    "purpose": "Biometric Verification Profile Builder",
    "trigger": "onAction",
    "invalidates": [
     "setBiometricVerificationProfile"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-185"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 58. 0 of 0 labels bound to a contract property; 8 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-186",
  "name": "Face Pass Enrollment Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.3",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/face-pass-enrollment-configuration-bo-186",
   "component": "apps/venue-management-web/src/routes/access-venue/FacePassEnrollmentConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-184"
   ],
   "exitTo": [
    "BO-184"
   ],
   "inferred": false,
   "notes": "**Reached from BO-184, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-184",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F115 step 4→5",
     "operation": "setFacePassEnrollment"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture Required Consent; Capture Face; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure persistent Face Pass registration. The source specifies that Face Pass may be registered through the App, ticket counters or Annual Pass counter.",
  "purposeNote": "Face Pass enrollment follows a controlled, configurable and fully auditable workflow.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "→",
       "provenance": "pack Access Control Module_Reference.pdf, page 59 §Capture Required Consent"
      },
      {
       "kind": "selectField",
       "label": "Account login required",
       "provenance": "pack Access Control Module_Reference.pdf, page 59 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Valid ticket/pass required",
       "provenance": "pack Access Control Module_Reference.pdf, page 59 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Identity check required",
       "provenance": "pack Access Control Module_Reference.pdf, page 59 §Configure"
      },
      {
       "kind": "textField",
       "label": "Number of capture attempts",
       "provenance": "pack Access Control Module_Reference.pdf, page 59 §Configure"
      },
      {
       "kind": "selectField",
       "label": "minimum image quality",
       "provenance": "pack Access Control Module_Reference.pdf, page 59 §Configure"
      },
      {
       "kind": "selectField",
       "label": "duplicate face detection",
       "provenance": "pack Access Control Module_Reference.pdf, page 59 §Configure"
      },
      {
       "kind": "selectField",
       "label": "operator verification",
       "provenance": "pack Access Control Module_Reference.pdf, page 59 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setFacePassEnrollment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The face pass enrollment configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the face pass enrollment untouched.",
   "emptyFirstRun": "No face pass enrollment configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setFacePassEnrollment",
    "contract": "access",
    "purpose": "Face Pass Enrollment Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setFacePassEnrollment"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-186"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 59. 0 of 0 labels bound to a contract property; 8 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-187",
  "name": "Biometric Consent & Guardian Management",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.4",
   "page": 60
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/biometric-consent-guardian-management-bo-187",
   "component": "apps/venue-management-web/src/routes/access-venue/BiometricConsentGuardianManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-184"
   ],
   "exitTo": [
    "BO-184"
   ],
   "inferred": false,
   "notes": "**Reached from BO-184, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-184",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F115 step 6→7",
     "operation": "listBiometricConsentGuardian"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population",
  "purpose": "Manage consent requirements associated with persistent biometric enrollment. The matrix requires App users to provide consent before Face Pass registration and requires guardian consent for minors. On-site enrollment also requires consent before facial data is captured.",
  "purposeNote": "Face Pass capture cannot proceed when the applicable configured consent requirement has not been satisfied.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Country/Jurisdiction",
       "provenance": "pack Access Control Module_Reference.pdf, page 60 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Access Control Module_Reference.pdf, page 60 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Access Control Module_Reference.pdf, page 60 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Credential",
       "provenance": "pack Access Control Module_Reference.pdf, page 60 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Enrollment Channel",
       "provenance": "pack Access Control Module_Reference.pdf, page 60 §Configure by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The biometric consent guardian configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the biometric consent guardian untouched.",
   "emptyFirstRun": "No biometric consent guardian configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBiometricConsentGuardian",
    "contract": "access",
    "purpose": "Biometric Consent & Guardian Management",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-187"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 60. 0 of 0 labels bound to a contract property; 5 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-188",
  "name": "Face Tag Temporary Enrollment",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.5",
   "page": 61
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/face-tag-temporary-enrollment-bo-188",
   "component": "apps/venue-management-web/src/routes/access-venue/FaceTagTemporaryEnrollment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-184"
   ],
   "exitTo": [
    "BO-184"
   ],
   "inferred": false,
   "notes": "**Reached from BO-184, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-184",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F115 step 8→9",
     "operation": "listFaceTagTemporary"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Face Captured) and no display directory — it is settings, not a population",
  "purpose": "Configure the temporary biometric model separately from Face Pass. The matrix describes Face Tag as temporarily stored facial data, enrollable at ticket counters or entry gates, with biometric data permanently deleted once the associated ticket is fully redeemed.",
  "purposeNote": "Temporary biometric identities are clearly separated from persistent biometric profiles and follow their configured automatic deletion lifecycle.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "→",
       "provenance": "pack Access Control Module_Reference.pdf, page 61 §Face Captured"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listFaceTagTemporary",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The face tag temporary configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the face tag temporary untouched.",
   "emptyFirstRun": "No face tag temporary configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFaceTagTemporary",
    "contract": "access",
    "purpose": "Face Tag Temporary Enrollment",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-188"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 61. 0 of 0 labels bound to a contract property; 1 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-189",
  "name": "Face Matching & Verification Thresholds",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.6",
   "page": 62
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/face-matching-verification-thresholds-bo-189",
   "component": "apps/venue-management-web/src/routes/access-venue/FaceMatchingVerificationThresholds.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-184"
   ],
   "exitTo": [
    "BO-184"
   ],
   "inferred": false,
   "notes": "**Reached from BO-184, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-184",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F115 step 10→11",
     "operation": "listFaceMatchingVerification"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure biometric verification behavior. The source requires a configurable Biometric Check Level determining the scoring of biometric comparison.",
  "purposeNote": "Biometric verification sensitivity can be configured by access context and provider capability.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Liveness check",
       "provenance": "pack Access Control Module_Reference.pdf, page 62 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Duplicate-face check",
       "provenance": "pack Access Control Module_Reference.pdf, page 62 §Configure"
      },
      {
       "kind": "selectField",
       "label": "image quality",
       "provenance": "pack Access Control Module_Reference.pdf, page 62 §Configure"
      },
      {
       "kind": "selectField",
       "label": "capture timeout",
       "provenance": "pack Access Control Module_Reference.pdf, page 62 §Configure"
      },
      {
       "kind": "selectField",
       "label": "retry quantity",
       "provenance": "pack Access Control Module_Reference.pdf, page 62 §Configure"
      },
      {
       "kind": "selectField",
       "label": "mask/obstruction handling",
       "provenance": "pack Access Control Module_Reference.pdf, page 62 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The face matching verification configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the face matching verification untouched.",
   "emptyFirstRun": "No face matching verification configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFaceMatchingVerification",
    "contract": "access",
    "purpose": "Face Matching & Verification Thresholds",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-189"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 62. 0 of 0 labels bound to a contract property; 6 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-190",
  "name": "Face Change, Re-enrollment & Identity Protection",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.7",
   "page": 63
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/face-change-re-enrollment-identity-protection-bo-190",
   "component": "apps/venue-management-web/src/routes/access-venue/FaceChangeReEnrollmentIdentityProtection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-184"
   ],
   "exitTo": [
    "BO-184"
   ],
   "inferred": false,
   "notes": "**Reached from BO-184, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-184",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F115 step 12→13",
     "operation": "listFaceChangeEnrollment"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Prevent guests from replacing a registered biometric identity with another person's face. The source explicitly states that customers may re-register Face Pass, but the system must compare the new facial data with the previous profile. If the difference exceeds an acceptable threshold, the update is blocked and venue assistance is required.",
  "purposeNote": "Biometric re-enrollment cannot silently replace the identity attached to a credential.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every face change re-enrollment",
       "columns": [
        "FaceChangeReEnrollmentIdentityProtectionView.existingProfileReference",
        "FaceChangeReEnrollmentIdentityProtectionView.newCaptureReference",
        "FaceChangeReEnrollmentIdentityProtectionView.matchResult",
        "FaceChangeReEnrollmentIdentityProtectionView.credential",
        "FaceChangeReEnrollmentIdentityProtectionView.guest",
        "FaceChangeReEnrollmentIdentityProtectionView.reasonForReEnrollment",
        "FaceChangeReEnrollmentIdentityProtectionView.previousChanges",
        "FaceChangeReEnrollmentIdentityProtectionView.operator"
       ],
       "bindsTo": "FaceChangeReEnrollmentIdentityProtectionView",
       "operation": "listFaceChangeEnrollment",
       "provenance": "pack Access Control Module_Reference.pdf, page 63 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected face change re-enrollment",
       "bindsTo": "FaceChangeReEnrollmentIdentityProtectionView",
       "columns": [
        "FaceChangeReEnrollmentIdentityProtectionView.existingProfileReference",
        "FaceChangeReEnrollmentIdentityProtectionView.newCaptureReference",
        "FaceChangeReEnrollmentIdentityProtectionView.matchResult",
        "FaceChangeReEnrollmentIdentityProtectionView.credential",
        "FaceChangeReEnrollmentIdentityProtectionView.guest",
        "FaceChangeReEnrollmentIdentityProtectionView.reasonForReEnrollment",
        "FaceChangeReEnrollmentIdentityProtectionView.previousChanges",
        "FaceChangeReEnrollmentIdentityProtectionView.operator"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Current Face”, “SIGNIFICANT IDENTITY DIFFERENCE”, “CHANGE BLOCKED”, “Change Reasons”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 63 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The face change re-enrollment list.",
   "error": "Could not load. Names which read failed and leaves the face change re-enrollment untouched.",
   "emptyFirstRun": "No face change re-enrollment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the face change re-enrollment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFaceChangeEnrollment",
    "contract": "access",
    "purpose": "Face Change, Re-enrollment & Identity Protection",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "FaceChangeReEnrollmentIdentityProtectionView.existingProfileReference",
    "FaceChangeReEnrollmentIdentityProtectionView.newCaptureReference",
    "FaceChangeReEnrollmentIdentityProtectionView.matchResult",
    "FaceChangeReEnrollmentIdentityProtectionView.credential",
    "FaceChangeReEnrollmentIdentityProtectionView.guest",
    "FaceChangeReEnrollmentIdentityProtectionView.reasonForReEnrollment"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-190"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 63. 8 of 8 labels bound to a contract property; 8 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-191",
  "name": "Biometric Validation at Gate",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.8",
   "page": 65
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/biometric-validation-at-gate-bo-191",
   "component": "apps/venue-management-web/src/routes/access-venue/BiometricValidationAtGate.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-184"
   ],
   "exitTo": [
    "BO-184"
   ],
   "inferred": false,
   "notes": "**Reached from BO-184, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-184",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F115 step 14→15",
     "operation": "listBiometricValidationGate"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how facial verification interacts with the physical access-control journey.",
  "purposeNote": "Biometric verification integrates transparently into the normal TICVAI admission and exit decision flow.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 65"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 65"
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
       "impliedBy": "listBiometricValidationGate",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The biometric validation gate list.",
   "error": "Could not load. Names which read failed and leaves the biometric validation gate untouched.",
   "emptyFirstRun": "No biometric validation gate yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the biometric validation gate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBiometricValidationGate",
    "contract": "access",
    "purpose": "Biometric Validation at Gate",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BiometricValidationAtGateView.decisionReturned",
    "BiometricValidationAtGateView.biometricMatchValidAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-191"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 65. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-192",
  "name": "Biometric Lifecycle, Retention & Deletion",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.9",
   "page": 66
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/biometric-lifecycle-retention-deletion-bo-192",
   "component": "apps/venue-management-web/src/routes/access-venue/BiometricLifecycleRetentionDeletion.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-184"
   ],
   "exitTo": [
    "BO-184"
   ],
   "inferred": false,
   "notes": "**Reached from BO-184, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-184",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F115 step 16→17",
     "operation": "listBiometricLifecycleRetention"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure separately for) and no display directory — it is settings, not a population",
  "purpose": "Manage biometric-data lifecycle and deletion rules.",
  "purposeNote": "Biometric information follows explicit, auditable lifecycle and deletion rules independently from ticket history.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Face Pass",
       "provenance": "pack Access Control Module_Reference.pdf, page 66 §Configure separately for"
      },
      {
       "kind": "selectField",
       "label": "Face Tag",
       "provenance": "pack Access Control Module_Reference.pdf, page 66 §Configure separately for"
      },
      {
       "kind": "selectField",
       "label": "Failed enrollment captures",
       "provenance": "pack Access Control Module_Reference.pdf, page 66 §Configure separately for"
      },
      {
       "kind": "selectField",
       "label": "abandoned registrations",
       "provenance": "pack Access Control Module_Reference.pdf, page 66 §Configure separately for"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The biometric lifecycle retention configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the biometric lifecycle retention untouched.",
   "emptyFirstRun": "No biometric lifecycle retention configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBiometricLifecycleRetention",
    "contract": "access",
    "purpose": "Biometric Lifecycle, Retention & Deletion",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-192"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 66. 0 of 0 labels bound to a contract property; 4 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-193",
  "name": "Biometric Simulation, Audit & Publication",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "5",
   "number": "5.10",
   "page": 67
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/biometric-simulation-audit-publication-bo-193",
   "component": "apps/venue-management-web/src/routes/access-venue/BiometricSimulationAuditPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-184"
   ],
   "exitTo": [
    "BO-184"
   ],
   "inferred": false,
   "notes": "**Reached from BO-184, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Test biometric configurations before live deployment.",
  "purposeNote": "No biometric access configuration enters production without testing, authorization, version control and auditability. Board 5 — Final 10-Screen Structure # Backend Screen Main Responsibility 5.1 Biometric Access Command Center Biometric estate and operational health",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Low-confidence match, Duplicate profile. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Access Control Module_Reference.pdf, page 67 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 67"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search biometric simulation audit",
       "provenance": "pack Access Control Module_Reference.pdf, page 67 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Guest",
        "Credential",
        "Face profile reference",
        "Gate",
        "Device",
        "Operator",
        "Date",
        "Result"
       ],
       "notes": "The pack filters this screen by guest, credential, face profile reference, gate, device, operator and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Access Control Module_Reference.pdf, page 67 §Search by"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Low-confidence match",
       "provenance": "pack Access Control Module_Reference.pdf, page 67 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate profile",
       "provenance": "pack Access Control Module_Reference.pdf, page 67 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The biometric simulation audit list.",
   "error": "Could not load. Names which read failed and leaves the biometric simulation audit untouched.",
   "emptyFirstRun": "No biometric simulation audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the biometric simulation audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBiometric",
    "contract": "access",
    "purpose": "Biometric Simulation, Audit & Publication",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-193"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 67. 0 of 8 labels bound to a contract property; 10 of 69 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listBiometric": {
  "method": "GET",
  "path": "/biometric",
  "contract": "access",
  "summary": "Biometric Simulation, Audit & Publication",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "guest",
    "in": "query",
    "required": false
   },
   {
    "name": "credential",
    "in": "query",
    "required": false
   },
   {
    "name": "faceProfileReference",
    "in": "query",
    "required": false
   },
   {
    "name": "gate",
    "in": "query",
    "required": false
   },
   {
    "name": "device",
    "in": "query",
    "required": false
   },
   {
    "name": "operator",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "result",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "BiometricSimulationAuditPublicationView"
 },
 "listBiometricAccess": {
  "method": "GET",
  "path": "/biometric-access",
  "contract": "access",
  "summary": "Biometric Access Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BiometricAccessCommandCenterView"
 },
 "listBiometricConsentGuardian": {
  "method": "GET",
  "path": "/biometric-consent-guardian",
  "contract": "access",
  "summary": "Biometric Consent & Guardian Management",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BiometricConsentGuardianManagementView"
 },
 "listBiometricLifecycleRetention": {
  "method": "GET",
  "path": "/biometric-lifecycle-retention",
  "contract": "access",
  "summary": "Biometric Lifecycle, Retention & Deletion",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BiometricLifecycleRetentionDeletionView"
 },
 "listBiometricValidationGate": {
  "method": "GET",
  "path": "/biometric-validation-gate",
  "contract": "access",
  "summary": "Biometric Validation at Gate",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BiometricValidationAtGateView"
 },
 "listFaceChangeEnrollment": {
  "method": "GET",
  "path": "/face-change-enrollment",
  "contract": "access",
  "summary": "Face Change, Re-enrollment & Identity Protection",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FaceChangeReEnrollmentIdentityProtectionView"
 },
 "listFaceMatchingVerification": {
  "method": "GET",
  "path": "/face-matching-verification",
  "contract": "access",
  "summary": "Face Matching & Verification Thresholds",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FaceMatchingVerificationThresholdsView"
 },
 "listFaceTagTemporary": {
  "method": "GET",
  "path": "/face-tag-temporary",
  "contract": "access",
  "summary": "Face Tag Temporary Enrollment",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FaceTagTemporaryEnrollmentView"
 },
 "setBiometricVerificationProfile": {
  "method": "PUT",
  "path": "/biometric-verification-profile",
  "contract": "access",
  "summary": "Biometric Verification Profile Builder",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "BiometricVerificationProfileBuilderInput",
  "responds": "BiometricVerificationProfileBuilderView"
 },
 "setFacePassEnrollment": {
  "method": "PUT",
  "path": "/face-pass-enrollment",
  "contract": "access",
  "summary": "Face Pass Enrollment Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "FacePassEnrollmentConfigurationInput",
  "responds": "FacePassEnrollmentConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BiometricAccessCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Access Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeFacePassProfiles": {
    "type": "integer",
    "description": "Active Face Pass Profiles"
   },
   "activeFaceTags": {
    "type": "integer",
    "description": "Active Face Tags"
   },
   "enrollmentsToday": {
    "type": "string",
    "description": "Enrollments Today"
   },
   "successfulFaceVerifications": {
    "type": "integer",
    "description": "Successful Face Verifications"
   },
   "failedVerifications": {
    "type": "integer",
    "description": "Failed Verifications"
   },
   "manualReviews": {
    "type": "integer",
    "description": "Manual Reviews"
   },
   "reEnrollmentRequests": {
    "type": "integer",
    "description": "Re-enrollment Requests"
   },
   "blockedFaceChanges": {
    "type": "integer",
    "description": "Blocked Face Changes"
   },
   "profilesPendingDeletion": {
    "type": "string",
    "description": "Profiles Pending Deletion"
   },
   "cameraReaderHealth": {
    "type": "string",
    "description": "Camera/Reader Health"
   },
   "biometricSecurityAlerts": {
    "type": "integer",
    "description": "Biometric Security Alerts"
   },
   "ai": {
    "type": "string",
    "description": "AI"
   }
  }
 },
 "BiometricConsentGuardianManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Consent & Guardian Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "countryJurisdiction": {
    "type": "string",
    "description": "Country/Jurisdiction"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "enrollmentChannel": {
    "type": "string",
    "description": "Enrollment Channel"
   },
   "guestCategory": {
    "type": "string",
    "description": "Guest Category"
   },
   "consentRecordId": {
    "type": "string",
    "description": "Consent record ID"
   },
   "policyVersion": {
    "type": "string",
    "description": "Policy/version"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "guardianReferenceWhereApplicable": {
    "type": "string",
    "description": "Guardian reference where applicable"
   },
   "operatorWhereApplicable": {
    "type": "string",
    "description": "Operator where applicable"
   },
   "withdrawalDeletionStatus": {
    "type": "string",
    "description": "withdrawal/deletion status"
   },
   "from": {
    "type": "string",
    "description": "from"
   },
   "consentRecordMayBeRetained": {
    "type": "string",
    "description": "consent record may be retained"
   }
  }
 },
 "BiometricLifecycleRetentionDeletionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Lifecycle, Retention & Deletion displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "verificationMethod": {
    "type": "string",
    "description": "verification method"
   },
   "activeCredential": {
    "type": "integer",
    "description": "Active Credential?"
   },
   "alreadyValidatedUsingFacePass": {
    "type": "string",
    "description": "Already validated using Face Pass?"
   },
   "reasonShown": {
    "type": "string",
    "description": "Reason shown"
   },
   "facePass": {
    "type": "string",
    "description": "Face Pass"
   },
   "faceTag": {
    "type": "string",
    "description": "Face Tag"
   },
   "failedEnrollmentCaptures": {
    "type": "integer",
    "description": "Failed enrollment captures"
   },
   "abandonedRegistrations": {
    "type": "string",
    "description": "abandoned registrations"
   },
   "temporaryCaptures": {
    "type": "string",
    "description": "temporary captures"
   }
  }
 },
 "BiometricSimulationAuditPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Simulation, Audit & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "validFacePass": {
    "type": "string",
    "description": "Valid Face Pass"
   },
   "faceMismatch": {
    "type": "string",
    "description": "Face mismatch"
   },
   "noBiometricProfile": {
    "type": "string",
    "description": "No biometric profile"
   },
   "lowConfidenceMatch": {
    "type": "string",
    "description": "Low-confidence match"
   },
   "livenessFailure": {
    "type": "string",
    "description": "Liveness failure"
   },
   "reEnrollmentAttempt": {
    "type": "string",
    "description": "Re-enrollment attempt"
   },
   "childAssignedAdult": {
    "type": "string",
    "description": "Child + assigned adult"
   },
   "faceTagExpired": {
    "type": "string",
    "description": "Face Tag expired"
   },
   "faceTagDeleted": {
    "type": "string",
    "description": "Face Tag deleted"
   },
   "offlineBiometricScenario": {
    "type": "integer",
    "description": "Offline biometric scenario"
   },
   "cameraUnavailable": {
    "type": "string",
    "description": "Camera unavailable"
   },
   "alternativeVerificationFallback": {
    "type": "string",
    "description": "alternative verification fallback"
   },
   "faceProfileActive": {
    "type": "integer",
    "description": "✓ Face profile active"
   },
   "verificationPolicySatisfied": {
    "type": "string",
    "description": "✓ Verification policy satisfied"
   },
   "matchPolicySatisfied": {
    "type": "string",
    "description": "✓ Match policy satisfied"
   },
   "credentialResolved": {
    "type": "string",
    "description": "✓ Credential resolved"
   },
   "ticketValid": {
    "type": "string",
    "description": "✓ Ticket valid"
   },
   "accessEntitlementValid": {
    "type": "string",
    "description": "✓ Access entitlement valid"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "credentialType": {
    "type": "string",
    "description": "Credential type"
   },
   "gateGroup": {
    "type": "string",
    "description": "Gate group"
   },
   "withAppropriateFallbackRules": {
    "type": "string",
    "description": "with appropriate fallback rules"
   },
   "required": {
    "type": "boolean",
    "description": "required"
   },
   "hardware": {
    "type": "string",
    "description": "hardware"
   }
  }
 },
 "BiometricValidationAtGateView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Validation at Gate displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "decisionReturned": {
    "type": "string",
    "description": "Decision returned"
   },
   "biometricMatchValidAccess": {
    "type": "string",
    "description": "Biometric Match + Valid Access"
   }
  }
 },
 "BiometricVerificationProfileBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Biometric Verification Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "selectType": {
    "type": "string",
    "enum": [
     "ticketProduct",
     "ticketType",
     "membership",
     "annualPass",
     "multiDayTicket",
     "multiAttractionTicket",
     "vipCredential",
     "accreditation",
     "selectedCustomerSegments"
    ],
    "description": "Vocabulary listed under Select."
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "mainEntryFaceRequired": {
    "type": "boolean",
    "description": "Main Entry → Face Required"
   },
   "attractionsCredentialOnly": {
    "type": "string",
    "description": "Attractions → Credential Only"
   },
   "vipLoungeFaceRequired": {
    "type": "boolean",
    "description": "VIP Lounge → Face Required"
   }
  }
 },
 "BiometricVerificationProfileBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Verification Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "facePass": {
    "type": "string",
    "description": "Face Pass"
   },
   "faceTag": {
    "type": "string",
    "description": "Face Tag"
   },
   "supportedFutureBiometricProvider": {
    "type": "string",
    "description": "Supported future biometric provider"
   },
   "selectType": {
    "type": "string",
    "enum": [
     "ticketProduct",
     "ticketType",
     "membership",
     "annualPass",
     "multiDayTicket",
     "multiAttractionTicket",
     "vipCredential",
     "accreditation",
     "selectedCustomerSegments"
    ],
    "description": "Vocabulary listed under Select."
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "mainEntryFaceRequired": {
    "type": "boolean",
    "description": "Main Entry → Face Required"
   },
   "attractionsCredentialOnly": {
    "type": "string",
    "description": "Attractions → Credential Only"
   },
   "vipLoungeFaceRequired": {
    "type": "boolean",
    "description": "VIP Lounge → Face Required"
   }
  }
 },
 "FaceChangeReEnrollmentIdentityProtectionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Face Change, Re-enrollment & Identity Protection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "existingProfileReference": {
    "type": "string",
    "description": "Existing profile reference"
   },
   "newCaptureReference": {
    "type": "integer",
    "description": "New capture reference"
   },
   "matchResult": {
    "type": "string",
    "description": "match result"
   },
   "credential": {
    "type": "string",
    "description": "credential"
   },
   "guest": {
    "type": "string",
    "description": "guest"
   },
   "reasonForReEnrollment": {
    "type": "string",
    "description": "reason for re-enrollment"
   },
   "previousChanges": {
    "type": "integer",
    "description": "previous changes"
   },
   "operator": {
    "type": "string",
    "description": "operator"
   },
   "auditHistory": {
    "type": "string",
    "description": "audit history"
   },
   "reasonsType": {
    "type": "string",
    "enum": [
     "appearanceChange",
     "poorOriginalCapture",
     "technicalIssue",
     "guestRequest",
     "recovery"
    ],
    "description": "Vocabulary listed under Change Reasons."
   }
  }
 },
 "FaceMatchingVerificationThresholdsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Face Matching & Verification Thresholds displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venuePolicy": {
    "type": "string",
    "description": "venue policy"
   },
   "livenessCheck": {
    "type": "string",
    "description": "Liveness check"
   },
   "duplicateFaceCheck": {
    "type": "string",
    "description": "Duplicate-face check"
   },
   "imageQuality": {
    "type": "string",
    "description": "image quality"
   },
   "captureTimeout": {
    "type": "string",
    "description": "capture timeout"
   },
   "maskObstructionHandling": {
    "type": "string",
    "description": "mask/obstruction handling"
   },
   "operatorFallback": {
    "type": "string",
    "description": "operator fallback"
   }
  }
 },
 "FacePassEnrollmentConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Face Pass Enrollment Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "ticvaiApp": {
    "type": "string",
    "description": "☑ TICVAI App"
   },
   "ticketCounter": {
    "type": "string",
    "description": "☑ Ticket Counter"
   },
   "annualPassCounter": {
    "type": "string",
    "description": "☑ Annual Pass Counter"
   },
   "selfServiceKiosk": {
    "type": "string",
    "description": "☐ Self-Service Kiosk"
   },
   "otherAuthorizedChannel": {
    "type": "string",
    "description": "☐ Other authorized channel"
   },
   "accountLoginRequired": {
    "type": "boolean",
    "description": "Account login required"
   },
   "validTicketPassRequired": {
    "type": "boolean",
    "description": "Valid ticket/pass required"
   },
   "identityCheckRequired": {
    "type": "boolean",
    "description": "Identity check required"
   },
   "numberOfCaptureAttempts": {
    "type": "integer",
    "description": "Number of capture attempts"
   },
   "minimumImageQuality": {
    "type": "string",
    "description": "minimum image quality"
   },
   "operatorVerification": {
    "type": "string",
    "description": "operator verification"
   },
   "enrollmentExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "enrollment expiry"
   },
   "alreadyAssociatedWith": {
    "type": "string",
    "description": "already associated with"
   }
  }
 },
 "FacePassEnrollmentConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Face Pass Enrollment Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticvaiApp": {
    "type": "string",
    "description": "☑ TICVAI App"
   },
   "ticketCounter": {
    "type": "string",
    "description": "☑ Ticket Counter"
   },
   "annualPassCounter": {
    "type": "string",
    "description": "☑ Annual Pass Counter"
   },
   "selfServiceKiosk": {
    "type": "string",
    "description": "☐ Self-Service Kiosk"
   },
   "otherAuthorizedChannel": {
    "type": "string",
    "description": "☐ Other authorized channel"
   },
   "accountLoginRequired": {
    "type": "boolean",
    "description": "Account login required"
   },
   "validTicketPassRequired": {
    "type": "boolean",
    "description": "Valid ticket/pass required"
   },
   "identityCheckRequired": {
    "type": "boolean",
    "description": "Identity check required"
   },
   "numberOfCaptureAttempts": {
    "type": "integer",
    "description": "Number of capture attempts"
   },
   "minimumImageQuality": {
    "type": "string",
    "description": "minimum image quality"
   },
   "operatorVerification": {
    "type": "string",
    "description": "operator verification"
   },
   "enrollmentExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "enrollment expiry"
   },
   "alreadyAssociatedWith": {
    "type": "string",
    "description": "already associated with"
   }
  }
 },
 "FaceTagTemporaryEnrollmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Face Tag Temporary Enrollment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketCounter": {
    "type": "string",
    "description": "Ticket Counter"
   },
   "entryGate": {
    "type": "string",
    "description": "Entry Gate"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "visit": {
    "type": "string",
    "description": "Visit"
   },
   "temporaryCredential": {
    "type": "string",
    "description": "Temporary Credential"
   },
   "alternativeConfigurableTriggersWherePermitted": {
    "type": "string",
    "description": "Alternative configurable triggers where permitted"
   },
   "endOfVisit": {
    "type": "string",
    "description": "End of visit"
   },
   "ticketExpiration": {
    "type": "string",
    "description": "Ticket expiration"
   },
   "credentialCancellation": {
    "type": "string",
    "description": "Credential cancellation"
   },
   "operationalRetentionThreshold": {
    "type": "integer",
    "description": "operational retention threshold"
   }
  }
 }
}
```
