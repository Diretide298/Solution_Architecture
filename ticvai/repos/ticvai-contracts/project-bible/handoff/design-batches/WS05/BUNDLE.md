# WS05 — Access Control board 5

**10 screens · 14 operations · 14 schemas · 3 permissions**

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
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-184` | Biometric Access Command Center | listDetail | 3 | 0 | — |
| `BO-185` | Biometric Verification Profile Builder | configEditor | 1 | 0 | — |
| `BO-186` | Face Pass Enrollment Configuration | configEditor | 1 | 0 | — |
| `BO-187` | Biometric Consent & Guardian Management | configEditor | 1 | 0 | — |
| `BO-188` | Face Tag Temporary Enrollment | configEditor | 2 | 0 | — |
| `BO-189` | Face Matching & Verification Thresholds | configEditor | 2 | 0 | — |
| `BO-190` | Face Change, Re-enrollment & Identity Protection | listDetail | 1 | 0 | — |
| `BO-191` | Biometric Validation at Gate | listDetail | 2 | 0 | — |
| `BO-192` | Biometric Lifecycle, Retention & Deletion | configEditor | 2 | 0 | — |
| `BO-193` | Biometric Simulation, Audit & Publication | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-188, BO-190, BO-191 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — BO-100 declares entryState.params  and BO-184 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
  "purposeNote": "Authorized administrators can monitor and manage the biometric-access environment from one location.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Central dashboard for biometric access configuration and operational health.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Face Pass Profiles",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.activeFacePassProfiles",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Active Face Tags",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.activeFaceTags",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Enrollments Today",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.enrollmentsToday",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Successful Face Verifications",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.successfulFaceVerifications",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Failed Verifications",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.failedVerifications",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Manual Reviews",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.manualReviews",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Re-enrollment Requests",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.reEnrollmentRequests",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Blocked Face Changes",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.blockedFaceChanges",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Profiles Pending Deletion",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.profilesPendingDeletion",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Camera/Reader Health",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.cameraReaderHealth",
       "operation": "listBiometricAccess",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Biometric Security Alerts",
       "bindsTo": "BiometricAccessCommandCenterViewSummary.biometricSecurityAlerts",
       "operation": "listBiometricAccess",
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
       "label": "Every biometric access",
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
   },
   {
    "operationId": "setBiometricVerificationProfile",
    "contract": "access",
    "purpose": "Create or change a biometric verification profile",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listBiometricAccess"
    ]
   },
   {
    "operationId": "setFacePassEnrollment",
    "contract": "access",
    "purpose": "Change Face Pass enrolment settings",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listBiometricAccess"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "BiometricAccessCommandCenterViewSummary.activeFacePassProfiles",
    "BiometricAccessCommandCenterViewSummary.activeFaceTags",
    "BiometricAccessCommandCenterViewSummary.enrollmentsToday",
    "BiometricAccessCommandCenterViewSummary.successfulFaceVerifications",
    "BiometricAccessCommandCenterViewSummary.failedVerifications",
    "BiometricAccessCommandCenterViewSummary.manualReviews"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-184",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-184"
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
  "purposeNote": "Biometric requirements can be activated or deactivated by product, credential and access location without development.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population",
  "purpose": "Configure which ticket/credential types can or must use biometric verification. The matrix specifically requires biometric checks to be configurable by ticket type, including memberships, annual passes, multi-day and multi-attraction products.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-185",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-185"
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
  "purposeNote": "Face Pass enrollment follows a controlled, configurable and fully auditable workflow.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture Required Consent; Capture Face; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure persistent Face Pass registration. The source specifies that Face Pass may be registered through the App, ticket counters or Annual Pass counter.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-186",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-186"
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
  "purposeNote": "Face Pass capture cannot proceed when the applicable configured consent requirement has not been satisfied.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population",
  "purpose": "Manage consent requirements associated with persistent biometric enrollment. The matrix requires App users to provide consent before Face Pass registration and requires guardian consent for minors. On-site enrollment also requires consent before facial data is captured.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-187",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-187"
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
  "purposeNote": "Temporary biometric identities are clearly separated from persistent biometric profiles and follow their configured automatic deletion lifecycle.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Face Captured) and no display directory — it is settings, not a population",
  "purpose": "Configure the temporary biometric model separately from Face Pass. The matrix describes Face Tag as temporarily stored facial data, enrollable at ticket counters or entry gates, with biometric data permanently deleted once the associated ticket is fully redeemed.",
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save Face Tag profile",
       "operation": "setFaceTagTemporaryEnrollment",
       "provenance": "contract access.yaml PUT /face-tag-temporary (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setFaceTagTemporaryEnrollment",
    "contract": "access",
    "purpose": "Save Face Tag profile",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-188",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-188"
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
  "purposeNote": "Biometric verification sensitivity can be configured by access context and provider capability.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure biometric verification behavior. The source requires a configurable Biometric Check Level determining the scoring of biometric comparison.",
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save thresholds",
       "operation": "setFaceMatchingVerification",
       "provenance": "contract access.yaml PUT /face-matching-verification (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setFaceMatchingVerification",
    "contract": "access",
    "purpose": "Save thresholds",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-189",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-189"
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
  "purposeNote": "Biometric re-enrollment cannot silently replace the identity attached to a credential.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Prevent guests from replacing a registered biometric identity with another person's face. The source explicitly states that customers may re-register Face Pass, but the system must compare the new facial data with the previous profile. If the difference exceeds an acceptable threshold, the update is blocked and venue assistance is required.",
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
        "FaceChangeReEnrollmentIdentityProtectionView.credentialId",
        "FaceChangeReEnrollmentIdentityProtectionView.guestId",
        "FaceChangeReEnrollmentIdentityProtectionView.reasonForReEnrollment",
        "FaceChangeReEnrollmentIdentityProtectionView.previousChanges",
        "FaceChangeReEnrollmentIdentityProtectionView.operatorId"
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
        "FaceChangeReEnrollmentIdentityProtectionView.credentialId",
        "FaceChangeReEnrollmentIdentityProtectionView.guestId",
        "FaceChangeReEnrollmentIdentityProtectionView.reasonForReEnrollment",
        "FaceChangeReEnrollmentIdentityProtectionView.previousChanges",
        "FaceChangeReEnrollmentIdentityProtectionView.operatorId"
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
    "FaceChangeReEnrollmentIdentityProtectionView.credentialId",
    "FaceChangeReEnrollmentIdentityProtectionView.guestId",
    "FaceChangeReEnrollmentIdentityProtectionView.reasonForReEnrollment"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-190",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-190"
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
  "purposeNote": "Biometric verification integrates transparently into the normal TICVAI admission and exit decision flow.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how facial verification interacts with the physical access-control journey.",
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setBiometricVerificationProfile",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setBiometricVerificationProfile"
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
   },
   {
    "operationId": "setBiometricVerificationProfile",
    "contract": "access",
    "purpose": "Choose which gates, zones and attractions require a face match",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listBiometricValidationGate"
    ]
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-191",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-191"
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
  "purposeNote": "Biometric information follows explicit, auditable lifecycle and deletion rules independently from ticket history.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure separately for) and no display directory — it is settings, not a population",
  "purpose": "Manage biometric-data lifecycle and deletion rules.",
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save retention rule",
       "operation": "setBiometricLifecycleRetention",
       "notes": "Step-up (mfa) on save. The retention period is still provisional: how long Face Pass, Face Tag and failed capture data may be kept per region is the client's make-or-break question (K1).",
       "provenance": "contract access.yaml PUT /biometric-lifecycle-retention (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setBiometricLifecycleRetention",
    "contract": "access",
    "purpose": "Save retention rule",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-192",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-192"
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
  "purposeNote": "No biometric access configuration enters production without testing, authorization, version control and auditability. Board 5 — Final 10-Screen Structure # Backend Screen Main Responsibility 5.1 Biometric Access Command Center Biometric estate and operational health",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Test biometric configurations before live deployment.",
  "gaps": [
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
      },
      {
       "kind": "primaryButton",
       "label": "Run simulation",
       "operation": "simulateBiometricConfiguration",
       "provenance": "contract access.yaml POST /biometric/simulate (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "simulateBiometricConfiguration",
    "contract": "access",
    "purpose": "Run simulation",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-193",
   "workshopBoard": "wireframes/WS22 Access Control Board 5.dc.html#bo-193"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 67. 0 of 8 labels bound to a contract property; 10 of 69 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `simulateBiometricConfiguration`.",
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
  "permission": "AUDIT_VIEW",
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
   },
   {
    "name": "reasonCode",
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
 "listBiometricAccess": {
  "method": "GET",
  "path": "/biometric-access",
  "contract": "access",
  "summary": "Biometric Access Command Center",
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
 "listBiometricConsentGuardian": {
  "method": "GET",
  "path": "/biometric-consent-guardian",
  "contract": "access",
  "summary": "Biometric Consent & Guardian Management",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "countryJurisdiction",
    "in": "query",
    "required": false
   },
   {
    "name": "tenantId",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "credentialType",
    "in": "query",
    "required": false
   },
   {
    "name": "enrollmentChannel",
    "in": "query",
    "required": false
   },
   {
    "name": "guestCategory",
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
 "setBiometricLifecycleRetention": {
  "method": "PUT",
  "path": "/biometric-lifecycle-retention",
  "contract": "access",
  "summary": "Save a biometric retention rule",
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
  "requestBody": "BiometricLifecycleRetentionDeletionInput",
  "responds": "BiometricLifecycleRetentionDeletionView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "BiometricVerificationProfileBuilderInput",
  "responds": "BiometricVerificationProfileBuilderView"
 },
 "setFaceMatchingVerification": {
  "method": "PUT",
  "path": "/face-matching-verification",
  "contract": "access",
  "summary": "Save face matching and verification thresholds",
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
  "requestBody": "FaceMatchingVerificationThresholdsInput",
  "responds": "FaceMatchingVerificationThresholdsView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "FacePassEnrollmentConfigurationInput",
  "responds": "FacePassEnrollmentConfigurationView"
 },
 "setFaceTagTemporaryEnrollment": {
  "method": "PUT",
  "path": "/face-tag-temporary",
  "contract": "access",
  "summary": "Save a Face Tag profile",
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
  "requestBody": "FaceTagTemporaryEnrollmentInput",
  "responds": "FaceTagTemporaryEnrollmentView"
 },
 "simulateBiometricConfiguration": {
  "method": "POST",
  "path": "/biometric/simulate",
  "contract": "access",
  "summary": "Run a biometric scenario before publishing",
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
  "requestBody": "BiometricSimulationInput",
  "responds": "BiometricSimulationAuditPublicationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BiometricLifecycleRetentionDeletionInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Biometric Lifecycle, Retention & Deletion submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "venueId",
   "dataCategory",
   "retentionDays",
   "deletionTrigger"
  ],
  "properties": {
   "policyId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent creates a retention rule"
   },
   "venueId": {
    "type": "string"
   },
   "dataCategory": {
    "type": "string",
    "enum": [
     "facePass",
     "faceTag",
     "failedEnrollmentCaptures",
     "abandonedRegistrations",
     "temporaryCaptures"
    ],
    "description": "Biometric data category this rule governs"
   },
   "retentionDays": {
    "type": "integer",
    "minimum": 0,
    "description": "Maximum retention in days. **No default and no maximum here on purpose**: the lawful period per region is the client counsel's value (make-or-break (a), see the operation)"
   },
   "deletionTrigger": {
    "type": "string",
    "enum": [
     "deletionRequest",
     "ticketFullyRedeemed",
     "endOfVisit",
     "ticketExpiration",
     "membershipEnded",
     "captureFailed",
     "registrationAbandoned"
    ],
    "description": "Event that starts the retention clock"
   }
  }
 },
 "BiometricLifecycleRetentionDeletionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Lifecycle, Retention & Deletion displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dataCategory": {
    "type": "string",
    "enum": [
     "facePass",
     "faceTag",
     "failedEnrollmentCaptures",
     "abandonedRegistrations",
     "temporaryCaptures"
    ],
    "description": "Biometric data category this retention rule governs"
   },
   "policyId": {
    "type": "string"
   },
   "venueId": {
    "type": "string"
   },
   "retentionDays": {
    "type": "integer",
    "description": "Maximum retention in days; value set per region once confirmed. No default (make-or-break (a), see `setBiometricLifecycleRetention`)"
   },
   "deletionTrigger": {
    "type": "string",
    "enum": [
     "deletionRequest",
     "ticketFullyRedeemed",
     "endOfVisit",
     "ticketExpiration",
     "membershipEnded",
     "captureFailed",
     "registrationAbandoned"
    ],
    "description": "Event that starts the retention clock (decided 29 September, VM close-out)"
   }
  }
 },
 "BiometricSimulationAuditPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Simulation, Audit & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "scenario": {
    "type": "string",
    "enum": [
     "validFacePass",
     "faceMismatch",
     "noBiometricProfile",
     "lowConfidenceMatch",
     "livenessFailure",
     "duplicateProfile",
     "reEnrollmentAttempt",
     "childAssignedAdult",
     "faceTagExpired",
     "faceTagDeleted",
     "offlineBiometric",
     "cameraUnavailable",
     "alternativeVerificationFallback"
    ],
    "description": "Simulated scenario (simulation rows only)"
   },
   "eventId": {
    "type": "string"
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "isSimulation": {
    "type": "boolean"
   },
   "guestId": {
    "type": "string"
   },
   "credentialId": {
    "type": "string"
   },
   "faceProfileReference": {
    "type": "string"
   },
   "gateId": {
    "type": "string"
   },
   "deviceId": {
    "type": "string"
   },
   "operatorId": {
    "type": "string"
   },
   "result": {
    "type": "string",
    "enum": [
     "allowed",
     "review",
     "denied"
    ]
   },
   "reasonCode": {
    "type": "string"
   },
   "decisionTrace": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Checks passed or failed, e.g. face profile active, match policy satisfied, ticket valid"
   }
  }
 },
 "BiometricSimulationInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only (decided 29 September, VM close-out)",
  "description": "One simulated biometric validation, run before a biometric profile is published (decided 29 September, VM close-out).",
  "required": [
   "scenario",
   "venueId"
  ],
  "properties": {
   "scenario": {
    "type": "string",
    "enum": [
     "validFacePass",
     "faceMismatch",
     "noBiometricProfile",
     "lowConfidenceMatch",
     "livenessFailure",
     "duplicateProfile",
     "reEnrollmentAttempt",
     "childAssignedAdult",
     "faceTagExpired",
     "faceTagDeleted",
     "offlineBiometric",
     "cameraUnavailable",
     "alternativeVerificationFallback"
    ]
   },
   "venueId": {
    "type": "string"
   },
   "gateGroupId": {
    "type": "string",
    "description": "Empty simulates at every gate group of the venue"
   },
   "credentialType": {
    "type": "string"
   },
   "profileId": {
    "type": "string",
    "description": "The draft biometric verification profile to test; empty tests the published one"
   }
  }
 },
 "BiometricValidationAtGateView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Validation at Gate displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "accessPointId": {
    "type": "string"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "green",
     "yellow",
     "red"
    ]
   },
   "conditions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Conditions that give this outcome, e.g. uncertain match, face mismatch, revoked profile"
   },
   "outcomeProfileId": {
    "type": "string",
    "description": "Gate response profile from the validation outcome designer"
   },
   "exitCaptureEnabled": {
    "type": "boolean",
    "description": "Face capture at exit records exit time"
   }
  }
 },
 "BiometricVerificationProfileBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Biometric Verification Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "faceRequirement": {
    "type": "string",
    "enum": [
     "notUsed",
     "optional",
     "required"
    ],
    "description": "Whether face verification is not used, allowed, or required at this location (e.g. main entry required, attractions credential only)"
   },
   "biometricType": {
    "type": "string",
    "enum": [
     "facePass",
     "faceTag",
     "otherProvider"
    ],
    "description": "Biometric model this profile uses"
   },
   "profileId": {
    "type": "string",
    "description": "Biometric verification profile identifier"
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
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "parkId": {
    "type": "string",
    "description": "Park"
   },
   "zoneId": {
    "type": "string",
    "description": "Zone"
   },
   "attractionId": {
    "type": "string",
    "description": "Attraction"
   },
   "gateId": {
    "type": "string",
    "description": "Gate"
   },
   "name": {
    "type": "string"
   }
  },
  "required": [
   "profileId",
   "venueId",
   "selectType",
   "biometricType",
   "faceRequirement"
  ]
 },
 "BiometricVerificationProfileBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Biometric Verification Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "faceRequirement": {
    "type": "string",
    "enum": [
     "notUsed",
     "optional",
     "required"
    ],
    "description": "Whether face verification is not used, allowed, or required at this location (e.g. main entry required, attractions credential only)"
   },
   "biometricType": {
    "type": "string",
    "enum": [
     "facePass",
     "faceTag",
     "otherProvider"
    ],
    "description": "Biometric model this profile uses"
   },
   "profileId": {
    "type": "string",
    "description": "Biometric verification profile identifier"
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
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "parkId": {
    "type": "string",
    "description": "Park"
   },
   "zoneId": {
    "type": "string",
    "description": "Zone"
   },
   "attractionId": {
    "type": "string",
    "description": "Attraction"
   },
   "gateId": {
    "type": "string",
    "description": "Gate"
   },
   "name": {
    "type": "string"
   }
  },
  "required": [
   "profileId",
   "venueId",
   "selectType",
   "biometricType",
   "faceRequirement"
  ]
 },
 "FaceMatchingVerificationThresholdsInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Face Matching & Verification Thresholds submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back. Proposed defaults are ours (our build plan); the scores are a 0-1 scale whatever the face vendor reports, normalised by the adapter (R077).",
  "required": [
   "venueId",
   "accessContext",
   "highConfidenceMin",
   "reviewRangeMin"
  ],
  "properties": {
   "profileId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent creates a threshold profile"
   },
   "venueId": {
    "type": "string"
   },
   "accessContext": {
    "type": "string",
    "maxLength": 100,
    "description": "Where the thresholds apply, e.g. main entry, child protection"
   },
   "highConfidenceMin": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Score at or above which the match is high confidence (allow if every other rule passes)"
   },
   "reviewRangeMin": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Score at or above which the match goes to operator review; below it is denied. Must be below highConfidenceMin"
   },
   "retryQuantity": {
    "type": "integer",
    "minimum": 0,
    "maximum": 5,
    "default": 2
   },
   "livenessCheck": {
    "type": "boolean",
    "default": true
   },
   "duplicateFaceCheck": {
    "type": "boolean",
    "default": true
   },
   "imageQuality": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high"
    ],
    "default": "medium",
    "description": "Minimum image quality accepted"
   },
   "captureTimeout": {
    "type": "integer",
    "minimum": 1,
    "maximum": 60,
    "default": 10,
    "description": "Seconds"
   },
   "maskObstructionHandling": {
    "type": "string",
    "enum": [
     "deny",
     "operatorReview",
     "fallbackMethod"
    ],
    "default": "operatorReview"
   },
   "operatorFallback": {
    "type": "boolean",
    "default": true,
    "description": "Review-range results go to operator verification"
   }
  }
 },
 "FaceMatchingVerificationThresholdsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Face Matching & Verification Thresholds displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "livenessCheck": {
    "type": "boolean",
    "description": "Liveness check"
   },
   "duplicateFaceCheck": {
    "type": "boolean",
    "description": "Duplicate-face check"
   },
   "imageQuality": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high"
    ],
    "description": "Minimum image quality accepted (decided 29 September, VM close-out)"
   },
   "captureTimeout": {
    "type": "integer",
    "description": "Seconds"
   },
   "maskObstructionHandling": {
    "type": "string",
    "enum": [
     "deny",
     "operatorReview",
     "fallbackMethod"
    ],
    "description": "What a masked or obstructed face leads to (decided 29 September, VM close-out)"
   },
   "operatorFallback": {
    "type": "boolean",
    "description": "Review-range results go to operator verification"
   },
   "profileId": {
    "type": "string"
   },
   "venueId": {
    "type": "string"
   },
   "accessContext": {
    "type": "string",
    "description": "Where the thresholds apply, e.g. main entry, child protection"
   },
   "highConfidenceMin": {
    "type": "number",
    "description": "Score at or above which the match is high confidence (allow if all other rules pass)"
   },
   "reviewRangeMin": {
    "type": "number",
    "description": "Score at or above which the match goes to operator review; below it is denied"
   },
   "retryQuantity": {
    "type": "integer"
   }
  }
 },
 "FacePassEnrollmentConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Face Pass Enrollment Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue this enrolment configuration applies to"
   },
   "enrollmentChannels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "ticvaiApp",
      "ticketCounter",
      "annualPassCounter",
      "selfServiceKiosk",
      "otherAuthorizedChannel"
     ]
    },
    "description": "Channels where Face Pass enrolment is enabled"
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
    "type": "boolean",
    "description": "An operator must verify the capture"
   },
   "enrollmentExpiry": {
    "type": "integer",
    "description": "Days an enrolment stays valid before re-enrolment is needed"
   },
   "duplicateFaceDetection": {
    "type": "boolean",
    "description": "Block a face already associated with another annual pass"
   }
  },
  "required": [
   "venueId"
  ]
 },
 "FacePassEnrollmentConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Face Pass Enrollment Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue this enrolment configuration applies to"
   },
   "enrollmentChannels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "ticvaiApp",
      "ticketCounter",
      "annualPassCounter",
      "selfServiceKiosk",
      "otherAuthorizedChannel"
     ]
    },
    "description": "Channels where Face Pass enrolment is enabled"
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
    "type": "boolean",
    "description": "An operator must verify the capture"
   },
   "enrollmentExpiry": {
    "type": "integer",
    "description": "Days an enrolment stays valid before re-enrolment is needed"
   },
   "duplicateFaceDetection": {
    "type": "boolean",
    "description": "Block a face already associated with another annual pass"
   }
  },
  "required": [
   "venueId"
  ]
 },
 "FaceTagTemporaryEnrollmentInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Face Tag Temporary Enrollment submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "venueId",
   "name",
   "enrollmentChannels",
   "bindTo",
   "deletionTrigger"
  ],
  "properties": {
   "profileId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent creates a Face Tag profile"
   },
   "venueId": {
    "type": "string"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "enrollmentChannels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "ticketCounter",
      "entryGate"
     ]
    },
    "minItems": 1,
    "description": "Where a Face Tag may be captured"
   },
   "bindTo": {
    "type": "string",
    "enum": [
     "ticket",
     "visit",
     "temporaryCredential"
    ],
    "default": "ticket",
    "description": "What the Face Tag is bound to"
   },
   "deletionTrigger": {
    "type": "string",
    "enum": [
     "ticketFullyRedeemed",
     "endOfVisit",
     "ticketExpiration",
     "credentialCancellation",
     "operationalRetentionThreshold"
    ],
    "default": "ticketFullyRedeemed",
    "description": "When the Face Tag is deleted automatically. The matrix: deleted once the ticket is fully redeemed"
   },
   "retentionThresholdHours": {
    "type": "integer",
    "minimum": 1,
    "description": "Used only when deletionTrigger is operationalRetentionThreshold, and then required. **No default and no maximum here on purpose**: the longest lawful period is the client counsel's value (make-or-break (a), see the operation)"
   }
  }
 },
 "FaceTagTemporaryEnrollmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Face Tag Temporary Enrollment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "enrollmentChannels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "ticketCounter",
      "entryGate"
     ]
    },
    "description": "Where a Face Tag may be captured"
   },
   "bindTo": {
    "type": "string",
    "enum": [
     "ticket",
     "visit",
     "temporaryCredential"
    ],
    "description": "What the Face Tag is bound to"
   },
   "deletionTrigger": {
    "type": "string",
    "enum": [
     "ticketFullyRedeemed",
     "endOfVisit",
     "ticketExpiration",
     "credentialCancellation",
     "operationalRetentionThreshold"
    ],
    "description": "When the Face Tag is automatically deleted; default ticketFullyRedeemed"
   },
   "profileId": {
    "type": "string"
   },
   "venueId": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "retentionThresholdHours": {
    "type": "integer",
    "description": "Used when deletionTrigger is operationalRetentionThreshold. No default (make-or-break (a), see `setFaceTagTemporaryEnrollment`)"
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
 }
}
```
