# WS03 — Access Control board 3

**10 screens · 10 operations · 13 schemas · 2 permissions**

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
| `BO-164` | Digital Credential Security Command Center | commandCentre | 1 | 0 | — |
| `BO-165` | Dynamic QR Security Profile Builder | configEditor | 1 | 0 | — |
| `BO-166` | Credential Activation & Display Rules | listDetail | 1 | 0 | — |
| `BO-167` | Device Binding & Session Security | listDetail | 1 | 0 | — |
| `BO-168` | BLE Beacon & Geofence Configuration | configEditor | 1 | 0 | — |
| `BO-169` | Credential Transfer & Rebinding | configEditor | 1 | 0 | — |
| `BO-170` | Credential Revocation & Lifecycle Events | listDetail | 1 | 0 | — |
| `BO-171` | Offline Cryptographic Validation Profile | listDetail | 1 | 0 | — |
| `BO-172` | Embedded Entitlement Payload Designer | listDetail | 1 | 0 | — |
| `BO-173` | Credential Security Simulation, Audit & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-166, BO-167, BO-170, BO-171, BO-172, BO-173 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-164",
  "name": "Digital Credential Security Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.1",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/digital-credential-security-command-center-bo-164",
   "component": "apps/venue-management-web/src/routes/access-venue/DigitalCredentialSecurityCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-165",
    "BO-166",
    "BO-167",
    "BO-168",
    "BO-169",
    "BO-170",
    "BO-171",
    "BO-172",
    "BO-173"
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
     "to": "BO-165",
     "trigger": "Works in Dynamic QR Security Profile Builder",
     "provenance": "flow F113 step 1→2",
     "operation": "listDigitalCredentialSecurity"
    },
    {
     "to": "BO-166",
     "trigger": "Works in Credential Activation & Display Rules",
     "provenance": "flow F113 step 3→4",
     "operation": "listDigitalCredentialSecurity"
    },
    {
     "to": "BO-167",
     "trigger": "Works in Device Binding & Session Security",
     "provenance": "flow F113 step 5→6",
     "operation": "listDigitalCredentialSecurity"
    },
    {
     "to": "BO-168",
     "trigger": "Works in BLE Beacon & Geofence Configuration",
     "provenance": "flow F113 step 7→8",
     "operation": "listDigitalCredentialSecurity"
    },
    {
     "to": "BO-169",
     "trigger": "Works in Credential Transfer & Rebinding",
     "provenance": "flow F113 step 9→10",
     "operation": "listDigitalCredentialSecurity"
    },
    {
     "to": "BO-170",
     "trigger": "Works in Credential Revocation & Lifecycle Events",
     "provenance": "flow F113 step 11→12",
     "operation": "listDigitalCredentialSecurity"
    },
    {
     "to": "BO-171",
     "trigger": "Works in Offline Cryptographic Validation Profile",
     "provenance": "flow F113 step 13→14",
     "operation": "listDigitalCredentialSecurity"
    },
    {
     "to": "BO-172",
     "trigger": "Works in Embedded Entitlement Payload Designer",
     "provenance": "flow F113 step 15→16",
     "operation": "listDigitalCredentialSecurity"
    },
    {
     "to": "BO-173",
     "trigger": "Works in Credential Security Simulation, Audit & Publication",
     "provenance": "flow F113 step 17→18",
     "operation": "listDigitalCredentialSecurity"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can centrally understand the security posture and configuration of all digital access credentials.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Central configuration and monitoring page for all secure digital credentials.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Digital Credentials",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterView.activeDigitalCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Dynamic QR Enabled",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterView.dynamicQrEnabled"
      },
      {
       "kind": "metricTile",
       "label": "Device-Bound Credentials",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterView.deviceBoundCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Location-Protected Credentials",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterView.locationProtectedCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Offline-Ready Credentials",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterView.offlineReadyCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Credentials Revoked Today",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterView.credentialsRevokedToday"
      },
      {
       "kind": "metricTile",
       "label": "Transfer Events",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Security Alerts",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterView.securityAlerts"
      },
      {
       "kind": "metricTile",
       "label": "Suspicious Sessions",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterView.suspiciousSessions"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every digital credential security",
       "columns": [
        "DigitalCredentialSecurityCommandCenterView.dynamicQrTickets",
        "DigitalCredentialSecurityCommandCenterView.membershipCredentials",
        "DigitalCredentialSecurityCommandCenterView.annualPasses",
        "DigitalCredentialSecurityCommandCenterView.mobileWalletCredentials",
        "DigitalCredentialSecurityCommandCenterView.loyaltyCredentials",
        "DigitalCredentialSecurityCommandCenterView.digitalPasses",
        "DigitalCredentialSecurityCommandCenterView.eventCredentials"
       ],
       "bindsTo": "DigitalCredentialSecurityCommandCenterView",
       "operation": "listDigitalCredentialSecurity",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected digital credential security",
       "bindsTo": "DigitalCredentialSecurityCommandCenterView",
       "columns": [
        "DigitalCredentialSecurityCommandCenterView.dynamicQrTickets",
        "DigitalCredentialSecurityCommandCenterView.membershipCredentials",
        "DigitalCredentialSecurityCommandCenterView.annualPasses",
        "DigitalCredentialSecurityCommandCenterView.mobileWalletCredentials",
        "DigitalCredentialSecurityCommandCenterView.loyaltyCredentials",
        "DigitalCredentialSecurityCommandCenterView.digitalPasses",
        "DigitalCredentialSecurityCommandCenterView.eventCredentials"
       ],
       "notes": "The pack groups this record's detail under its own headings: “For each credential profile”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital credential security list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the digital credential security untouched.",
   "emptyFirstRun": "No digital credential security yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital credential security are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDigitalCredentialSecurity",
    "contract": "access",
    "purpose": "Digital Credential Security Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DigitalCredentialSecurityCommandCenterView.dynamicQrTickets",
    "DigitalCredentialSecurityCommandCenterView.membershipCredentials",
    "DigitalCredentialSecurityCommandCenterView.annualPasses",
    "DigitalCredentialSecurityCommandCenterView.mobileWalletCredentials",
    "DigitalCredentialSecurityCommandCenterView.loyaltyCredentials",
    "DigitalCredentialSecurityCommandCenterView.digitalPasses"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-164"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 29. 15 of 15 labels bound to a contract property; 16 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-165",
  "name": "Dynamic QR Security Profile Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.2",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/dynamic-qr-security-profile-builder-bo-165",
   "component": "apps/venue-management-web/src/routes/access-venue/DynamicQrSecurityProfileBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-164"
   ],
   "exitTo": [
    "BO-164"
   ],
   "inferred": false,
   "notes": "**Reached from BO-164, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-164",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F113 step 2→3",
     "operation": "setDynamicSecurityProfile"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Options; Configuration may include) and no display directory — it is settings, not a population",
  "purpose": "Configure how a dynamic QR is generated and protected. The matrix requires a unique QR per issued ticket/pass and periodic QR refresh to reduce screenshot and duplication fraud.",
  "purposeNote": "Administrators can create reusable dynamic-QR security profiles without configuring individual tickets manually.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Refresh Every: 30 seconds",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "15 sec",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Options"
      },
      {
       "kind": "selectField",
       "label": "30 sec",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Options"
      },
      {
       "kind": "selectField",
       "label": "45 sec",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Options"
      },
      {
       "kind": "selectField",
       "label": "60 sec",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Options"
      },
      {
       "kind": "selectField",
       "label": "Custom",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Options"
      },
      {
       "kind": "selectField",
       "label": "Credential ID",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Configuration may include"
      },
      {
       "kind": "selectField",
       "label": "Ticket ID",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Configuration may include"
      },
      {
       "kind": "selectField",
       "label": "Timestamp",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Configuration may include"
      },
      {
       "kind": "selectField",
       "label": "Nonce / OTP",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Configuration may include"
      },
      {
       "kind": "selectField",
       "label": "Device binding reference",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Configuration may include"
      },
      {
       "kind": "selectField",
       "label": "Venue context",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Configuration may include"
      },
      {
       "kind": "selectField",
       "label": "Entitlement payload",
       "provenance": "pack Access Control Module_Reference.pdf, page 30 §Configuration may include"
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
       "provenance": "contract operation setDynamicSecurityProfile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic security profile configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the dynamic security profile untouched.",
   "emptyFirstRun": "No dynamic security profile configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDynamicSecurityProfile",
    "contract": "access",
    "purpose": "Dynamic QR Security Profile Builder",
    "trigger": "onAction",
    "invalidates": [
     "setDynamicSecurityProfile"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-165"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 13 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-166",
  "name": "Credential Activation & Display Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.3",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-activation-display-rules-bo-166",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialActivationDisplayRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-164"
   ],
   "exitTo": [
    "BO-164"
   ],
   "inferred": false,
   "notes": "**Reached from BO-164, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-164",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F113 step 4→5",
     "operation": "listCredentialActivationDisplay"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure when the guest is permitted to see/use the credential. The matrix specifies that after registration, a ticket may appear as a blurred QR and only become clear and usable near the park entrance.",
  "purposeNote": "The credential is only displayed in a usable form when its configured activation conditions are satisfied.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 32"
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
       "impliedBy": "listCredentialActivationDisplay",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential activation display list.",
   "error": "Could not load. Names which read failed and leaves the credential activation display untouched.",
   "emptyFirstRun": "No credential activation display yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential activation display are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialActivationDisplay",
    "contract": "access",
    "purpose": "Credential Activation & Display Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialActivationDisplayRulesView.hideQr",
    "CredentialActivationDisplayRulesView.blurQr",
    "CredentialActivationDisplayRulesView.showCountdown",
    "CredentialActivationDisplayRulesView.showAvailableAtVenue",
    "CredentialActivationDisplayRulesView.showVenueDirections"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-166"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-167",
  "name": "Device Binding & Session Security",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.4",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/device-binding-session-security-bo-167",
   "component": "apps/venue-management-web/src/routes/access-venue/DeviceBindingSessionSecurity.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-164"
   ],
   "exitTo": [
    "BO-164"
   ],
   "inferred": false,
   "notes": "**Reached from BO-164, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-164",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F113 step 6→7",
     "operation": "listDeviceBindingSession"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Prevent one credential from being shared across unauthorized devices. The source explicitly requires tickets to be linked to a specific device/user and suspicious patterns such as device sharing and multiple simultaneous sessions to be detected.",
  "purposeNote": "A credential cannot be duplicated across unauthorized devices when device binding is enabled.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every device binding session",
       "columns": [
        "DeviceBindingSessionSecurityView.user",
        "DeviceBindingSessionSecurityView.credential",
        "Device ID/reference",
        "DeviceBindingSessionSecurityView.appInstallation",
        "DeviceBindingSessionSecurityView.os",
        "DeviceBindingSessionSecurityView.registrationDate",
        "DeviceBindingSessionSecurityView.lastActivation",
        "DeviceBindingSessionSecurityView.lastKnownVenue"
       ],
       "bindsTo": "DeviceBindingSessionSecurityView",
       "operation": "listDeviceBindingSession",
       "provenance": "pack Access Control Module_Reference.pdf, page 33 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected device binding session",
       "bindsTo": "DeviceBindingSessionSecurityView",
       "columns": [
        "DeviceBindingSessionSecurityView.user",
        "DeviceBindingSessionSecurityView.credential",
        "Device ID/reference",
        "DeviceBindingSessionSecurityView.appInstallation",
        "DeviceBindingSessionSecurityView.os",
        "DeviceBindingSessionSecurityView.registrationDate",
        "DeviceBindingSessionSecurityView.lastActivation",
        "DeviceBindingSessionSecurityView.lastKnownVenue"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Maximum Active Devices”, “Concurrent Sessions”, “Device Change”, “Credential active on Device A”, “Response”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 33 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The device binding session list.",
   "error": "Could not load. Names which read failed and leaves the device binding session untouched.",
   "emptyFirstRun": "No device binding session yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the device binding session are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDeviceBindingSession",
    "contract": "access",
    "purpose": "Device Binding & Session Security",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DeviceBindingSessionSecurityView.user",
    "DeviceBindingSessionSecurityView.credential",
    "Device ID/reference",
    "DeviceBindingSessionSecurityView.appInstallation",
    "DeviceBindingSessionSecurityView.os",
    "DeviceBindingSessionSecurityView.registrationDate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-167"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 33. 7 of 8 labels bound to a contract property; 8 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-168",
  "name": "BLE Beacon & Geofence Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.5",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ble-beacon-geofence-configuration-bo-168",
   "component": "apps/venue-management-web/src/routes/access-venue/BleBeaconGeofenceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-164"
   ],
   "exitTo": [
    "BO-164"
   ],
   "inferred": false,
   "notes": "**Reached from BO-164, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-164",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F113 step 8→9",
     "operation": "setBleBeaconGeofence"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Map-Based Configuration; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure location-aware credential activation. This is a major requirement under 3.1.9. The matrix requires BLE beacon proximity and geofence boundaries to activate/deactivate credentials at venue, attraction, zone and gate level.",
  "purposeNote": "Digital credentials can automatically activate/deactivate according to configured physical-location context.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Beacon Name",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Beacon ID",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Zone",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gate",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Proximity threshold",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Active/Inactive",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Health",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Configure"
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
       "provenance": "contract operation setBleBeaconGeofence"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ble beacon geofence configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the ble beacon geofence untouched.",
   "emptyFirstRun": "No ble beacon geofence configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setBleBeaconGeofence",
    "contract": "access",
    "purpose": "BLE Beacon & Geofence Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setBleBeaconGeofence"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-168"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 8 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-169",
  "name": "Credential Transfer & Rebinding",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.6",
   "page": 35
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-transfer-rebinding-bo-169",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialTransferRebinding.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-164"
   ],
   "exitTo": [
    "BO-164"
   ],
   "inferred": false,
   "notes": "**Reached from BO-164, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-164",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F113 step 10→11",
     "operation": "listCredentialTransferRebinding"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Securely manage digital-ticket transfers. The matrix requires tickets to be transferable through email/app, with the recipient required to authenticate before accessing and activating the transferred QR.",
  "purposeNote": "Transferred tickets cannot remain simultaneously usable by both sender and recipient.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Transfer allowed",
       "provenance": "pack Access Control Module_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number of transfers",
       "provenance": "pack Access Control Module_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer deadline",
       "provenance": "pack Access Control Module_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "textField",
       "label": "Before first validation only",
       "provenance": "pack Access Control Module_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require recipient account",
       "provenance": "pack Access Control Module_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require OTP",
       "provenance": "pack Access Control Module_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require acceptance",
       "provenance": "pack Access Control Module_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cancel pending transfer",
       "provenance": "pack Access Control Module_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Return to sender",
       "provenance": "pack Access Control Module_Reference.pdf, page 35 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential transfer rebinding configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credential transfer rebinding untouched.",
   "emptyFirstRun": "No credential transfer rebinding configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialTransferRebinding",
    "contract": "access",
    "purpose": "Credential Transfer & Rebinding",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-169"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 35. 0 of 0 labels bound to a contract property; 9 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-170",
  "name": "Credential Revocation & Lifecycle Events",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.7",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-revocation-lifecycle-events-bo-170",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialRevocationLifecycleEvents.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-164"
   ],
   "exitTo": [
    "BO-164"
   ],
   "inferred": false,
   "notes": "**Reached from BO-164, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-164",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F113 step 12→13",
     "operation": "listCredentialRevocationLifecycle"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Immediately invalidate credentials when the underlying ticket changes. Requirement 3.1.4 specifically requires dynamic QR invalidation after refunds, cancellations, transfers, exchanges, upgrades or reissues.",
  "purposeNote": "A revoked or replaced credential cannot remain valid within the access ecosystem beyond the configured synchronization/offline security policy.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every credential revocation lifecycle",
       "columns": [
        "CredentialRevocationLifecycleEventsView.centralPlatform",
        "CredentialRevocationLifecycleEventsView.mobileApp",
        "CredentialRevocationLifecycleEventsView.gateNetwork",
        "CredentialRevocationLifecycleEventsView.offlineRevocationPackage",
        "CredentialRevocationLifecycleEventsView.walletCredentialService"
       ],
       "bindsTo": "CredentialRevocationLifecycleEventsView",
       "operation": "listCredentialRevocationLifecycle",
       "provenance": "pack Access Control Module_Reference.pdf, page 36 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential revocation lifecycle",
       "bindsTo": "CredentialRevocationLifecycleEventsView",
       "columns": [
        "CredentialRevocationLifecycleEventsView.centralPlatform",
        "CredentialRevocationLifecycleEventsView.mobileApp",
        "CredentialRevocationLifecycleEventsView.gateNetwork",
        "CredentialRevocationLifecycleEventsView.offlineRevocationPackage",
        "CredentialRevocationLifecycleEventsView.walletCredentialService"
       ],
       "notes": null,
       "provenance": "pack Access Control Module_Reference.pdf, page 36 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential revocation lifecycle list.",
   "error": "Could not load. Names which read failed and leaves the credential revocation lifecycle untouched.",
   "emptyFirstRun": "No credential revocation lifecycle yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential revocation lifecycle are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialRevocationLifecycle",
    "contract": "access",
    "purpose": "Credential Revocation & Lifecycle Events",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialRevocationLifecycleEventsView.centralPlatform",
    "CredentialRevocationLifecycleEventsView.mobileApp",
    "CredentialRevocationLifecycleEventsView.gateNetwork",
    "CredentialRevocationLifecycleEventsView.offlineRevocationPackage",
    "CredentialRevocationLifecycleEventsView.walletCredentialService"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-170"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 36. 5 of 5 labels bound to a contract property; 14 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-171",
  "name": "Offline Cryptographic Validation Profile",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.8",
   "page": 37
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/offline-cryptographic-validation-profile-bo-171",
   "component": "apps/venue-management-web/src/routes/access-venue/OfflineCryptographicValidationProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-164"
   ],
   "exitTo": [
    "BO-164"
   ],
   "inferred": false,
   "notes": "**Reached from BO-164, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-164",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F113 step 14→15",
     "operation": "listOfflineCryptographicValidation"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow access devices to validate secure credentials without continuous backend connectivity. The matrix explicitly requires offline cryptographic validation and embedded entitlement validation without real-time backend connectivity.",
  "purposeNote": "Supported credentials can be securely validated offline without exposing private signing secrets to gate devices.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 37"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 37"
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
       "impliedBy": "listOfflineCryptographicValidation",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline cryptographic validation list.",
   "error": "Could not load. Names which read failed and leaves the offline cryptographic validation untouched.",
   "emptyFirstRun": "No offline cryptographic validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline cryptographic validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOfflineCryptographicValidation",
    "contract": "access",
    "purpose": "Offline Cryptographic Validation Profile",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OfflineCryptographicValidationProfileView.credentialAuthenticity",
    "OfflineCryptographicValidationProfileView.digitalSignature",
    "OfflineCryptographicValidationProfileView.ticketId",
    "OfflineCryptographicValidationProfileView.venue",
    "OfflineCryptographicValidationProfileView.park"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-171"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-172",
  "name": "Embedded Entitlement Payload Designer",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.9",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/embedded-entitlement-payload-designer-bo-172",
   "component": "apps/venue-management-web/src/routes/access-venue/EmbeddedEntitlementPayloadDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-164"
   ],
   "exitTo": [
    "BO-164"
   ],
   "inferred": false,
   "notes": "**Reached from BO-164, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-164",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F113 step 16→17",
     "operation": "setEmbeddedEntitlementPayload"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine what operational information can be securely carried by the credential for offline decisions. The matrix permits embedded information including ticket type, seat assignment, event ID, venue access rights, timeslot, reservations, locker assignments, membership entitlements, guest category and validity.",
  "purposeNote": "Administrators can determine the minimum secure information required for reliable offline admission.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 38"
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
       "provenance": "contract operation setEmbeddedEntitlementPayload"
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
       "impliedBy": "setEmbeddedEntitlementPayload"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The embedded entitlement payload list.",
   "error": "Could not load. Names which read failed and leaves the embedded entitlement payload untouched.",
   "emptyFirstRun": "No embedded entitlement payload yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the embedded entitlement payload are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEmbeddedEntitlementPayload",
    "contract": "access",
    "purpose": "Embedded Entitlement Payload Designer",
    "trigger": "onAction",
    "invalidates": [
     "setEmbeddedEntitlementPayload"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-172"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-173",
  "name": "Credential Security Simulation, Audit & Publication",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "3",
   "number": "3.10",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-security-simulation-audit-publication-bo-173",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialSecuritySimulationAuditPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-164"
   ],
   "exitTo": [
    "BO-164"
   ],
   "inferred": false,
   "notes": "**Reached from BO-164, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Test the complete secure credential lifecycle before production deployment.",
  "purposeNote": "Credential-security configurations can be tested, approved, deployed, audited and rolled back before affecting live access. Board 3 — Final 10-Screen Structure # Backend Screen Responsibility Digital Credential Security Command Overall credential-security configuration and 3.1",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every credential security simulation",
       "columns": [
        "CredentialSecuritySimulationAuditPublicationView.signatureValid",
        "CredentialSecuritySimulationAuditPublicationView.deviceValid",
        "CredentialSecuritySimulationAuditPublicationView.venueValid",
        "CredentialSecuritySimulationAuditPublicationView.entitlementValid",
        "CredentialSecuritySimulationAuditPublicationView.qrFreshnessFailed"
       ],
       "bindsTo": "CredentialSecuritySimulationAuditPublicationView",
       "operation": "listCredentialSecurity",
       "provenance": "pack Access Control Module_Reference.pdf, page 39 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential security simulation",
       "bindsTo": "CredentialSecuritySimulationAuditPublicationView",
       "columns": [
        "CredentialSecuritySimulationAuditPublicationView.signatureValid",
        "CredentialSecuritySimulationAuditPublicationView.deviceValid",
        "CredentialSecuritySimulationAuditPublicationView.venueValid",
        "CredentialSecuritySimulationAuditPublicationView.entitlementValid",
        "CredentialSecuritySimulationAuditPublicationView.qrFreshnessFailed"
       ],
       "notes": "The pack groups this record's detail under its own headings: “QR age”, “Every important event records”, “Center health”, “Board 3 workflow”, “There is a deliberate distinction”, “Media, Credential & Verification Methods”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 39 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential security simulation list.",
   "error": "Could not load. Names which read failed and leaves the credential security simulation untouched.",
   "emptyFirstRun": "No credential security simulation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential security simulation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialSecurity",
    "contract": "access",
    "purpose": "Credential Security Simulation, Audit & Publication",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialSecuritySimulationAuditPublicationView.signatureValid",
    "CredentialSecuritySimulationAuditPublicationView.deviceValid",
    "CredentialSecuritySimulationAuditPublicationView.venueValid",
    "CredentialSecuritySimulationAuditPublicationView.entitlementValid",
    "CredentialSecuritySimulationAuditPublicationView.qrFreshnessFailed"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-173"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 39. 5 of 5 labels bound to a contract property; 6 of 72 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listCredentialActivationDisplay": {
  "method": "GET",
  "path": "/credential-activation-display",
  "contract": "access",
  "summary": "Credential Activation & Display Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialActivationDisplayRulesView"
 },
 "listCredentialRevocationLifecycle": {
  "method": "GET",
  "path": "/credential-revocation-lifecycle",
  "contract": "access",
  "summary": "Credential Revocation & Lifecycle Events",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialRevocationLifecycleEventsView"
 },
 "listCredentialSecurity": {
  "method": "GET",
  "path": "/credential-security",
  "contract": "access",
  "summary": "Credential Security Simulation, Audit & Publication",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialSecuritySimulationAuditPublicationView"
 },
 "listCredentialTransferRebinding": {
  "method": "GET",
  "path": "/credential-transfer-rebinding",
  "contract": "access",
  "summary": "Credential Transfer & Rebinding",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialTransferRebindingView"
 },
 "listDeviceBindingSession": {
  "method": "GET",
  "path": "/device-binding-session",
  "contract": "access",
  "summary": "Device Binding & Session Security",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DeviceBindingSessionSecurityView"
 },
 "listDigitalCredentialSecurity": {
  "method": "GET",
  "path": "/digital-credential-security",
  "contract": "access",
  "summary": "Digital Credential Security Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DigitalCredentialSecurityCommandCenterView"
 },
 "listOfflineCryptographicValidation": {
  "method": "GET",
  "path": "/offline-cryptographic-validation",
  "contract": "access",
  "summary": "Offline Cryptographic Validation Profile",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OfflineCryptographicValidationProfileView"
 },
 "setBleBeaconGeofence": {
  "method": "PUT",
  "path": "/ble-beacon-geofence",
  "contract": "access",
  "summary": "BLE Beacon & Geofence Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "BleBeaconGeofenceConfigurationInput",
  "responds": "BleBeaconGeofenceConfigurationView"
 },
 "setDynamicSecurityProfile": {
  "method": "PUT",
  "path": "/dynamic-security-profile",
  "contract": "access",
  "summary": "Dynamic QR Security Profile Builder",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "DynamicQrSecurityProfileBuilderInput",
  "responds": "DynamicQrSecurityProfileBuilderView"
 },
 "setEmbeddedEntitlementPayload": {
  "method": "PUT",
  "path": "/embedded-entitlement-payload",
  "contract": "access",
  "summary": "Embedded Entitlement Payload Designer",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "EmbeddedEntitlementPayloadDesignerInput",
  "responds": "EmbeddedEntitlementPayloadDesignerView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BleBeaconGeofenceConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What BLE Beacon & Geofence Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "andDraws": {
    "type": "string",
    "description": "and draws"
   },
   "beaconName": {
    "type": "string",
    "description": "Beacon Name"
   },
   "beaconId": {
    "type": "string",
    "description": "Beacon ID"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "proximityThreshold": {
    "type": "integer",
    "description": "Proximity threshold"
   },
   "activeInactive": {
    "type": "integer",
    "description": "Active/Inactive"
   },
   "health": {
    "type": "string",
    "description": "Health"
   },
   "lastDetected": {
    "type": "string",
    "format": "date-time",
    "description": "Last detected"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   }
  }
 },
 "BleBeaconGeofenceConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What BLE Beacon & Geofence Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "andDraws": {
    "type": "string",
    "description": "and draws"
   },
   "beaconName": {
    "type": "string",
    "description": "Beacon Name"
   },
   "beaconId": {
    "type": "string",
    "description": "Beacon ID"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "proximityThreshold": {
    "type": "integer",
    "description": "Proximity threshold"
   },
   "activeInactive": {
    "type": "integer",
    "description": "Active/Inactive"
   },
   "health": {
    "type": "string",
    "description": "Health"
   },
   "lastDetected": {
    "type": "string",
    "format": "date-time",
    "description": "Last detected"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   }
  }
 },
 "CredentialActivationDisplayRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Activation & Display Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "hideQr": {
    "type": "string",
    "description": "Hide QR"
   },
   "blurQr": {
    "type": "string",
    "description": "Blur QR"
   },
   "showCountdown": {
    "type": "string",
    "description": "Show countdown"
   },
   "showAvailableAtVenue": {
    "type": "string",
    "description": "Show \"Available at Venue\""
   },
   "showVenueDirections": {
    "type": "string",
    "description": "Show venue directions"
   },
   "displayDynamicQr": {
    "type": "string",
    "description": "Display dynamic QR"
   },
   "displayActivationTimer": {
    "type": "string",
    "description": "Display activation timer"
   },
   "displayCredentialStatus": {
    "type": "string",
    "description": "Display credential status"
   },
   "displayRemainingEntitlements": {
    "type": "string",
    "description": "Display remaining entitlements"
   }
  }
 },
 "CredentialRevocationLifecycleEventsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Revocation & Lifecycle Events displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "exchange": {
    "type": "string",
    "description": "Exchange"
   },
   "ticketExpiration": {
    "type": "string",
    "description": "Ticket expiration"
   },
   "manualInvalidation": {
    "type": "string",
    "description": "Manual invalidation"
   },
   "fraudLock": {
    "type": "string",
    "description": "Fraud lock"
   },
   "accountSuspension": {
    "type": "string",
    "description": "Account suspension"
   },
   "centralPlatform": {
    "type": "string",
    "description": "Central Platform ✓"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App ✓"
   },
   "gateNetwork": {
    "type": "string",
    "description": "Gate Network ✓"
   },
   "offlineRevocationPackage": {
    "type": "integer",
    "description": "Offline Revocation Package ✓"
   },
   "walletCredentialService": {
    "type": "string",
    "description": "Wallet/Credential Service ✓"
   }
  }
 },
 "CredentialSecuritySimulationAuditPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Security Simulation, Audit & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "signatureValid": {
    "type": "string",
    "description": "✓ Signature valid"
   },
   "deviceValid": {
    "type": "string",
    "description": "✓ Device valid"
   },
   "venueValid": {
    "type": "string",
    "description": "✓ Venue valid"
   },
   "entitlementValid": {
    "type": "string",
    "description": "✓ Entitlement valid"
   },
   "qrFreshnessFailed": {
    "type": "integer",
    "description": "✕ QR freshness failed"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "guestAccountReference": {
    "type": "string",
    "description": "Guest/account reference"
   },
   "device": {
    "type": "string",
    "description": "Device"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "operator": {
    "type": "string",
    "description": "Operator"
   },
   "activation": {
    "type": "string",
    "description": "Activation"
   },
   "refresh": {
    "type": "string",
    "description": "Refresh"
   },
   "validation": {
    "type": "string",
    "description": "Validation"
   },
   "revocation": {
    "type": "string",
    "description": "revocation"
   },
   "resultReasonCode": {
    "type": "string",
    "description": "result/reason code"
   },
   "securityApprovePublish": {
    "type": "string",
    "description": "Security → Approve & Publish"
   },
   "dynamicDigitalCredentials": {
    "type": "string",
    "description": "dynamic digital credentials"
   }
  }
 },
 "CredentialTransferRebindingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Transfer & Rebinding displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "numberOfTransfers": {
    "type": "integer",
    "description": "Number of transfers"
   },
   "beforeFirstValidationOnly": {
    "type": "string",
    "description": "Before first validation only"
   },
   "requireRecipientAccount": {
    "type": "boolean",
    "description": "Require recipient account"
   },
   "requireOtp": {
    "type": "boolean",
    "description": "Require OTP"
   },
   "requireAcceptance": {
    "type": "boolean",
    "description": "Require acceptance"
   },
   "returnToSender": {
    "type": "string",
    "description": "Return to sender"
   },
   "oldCredentialInvalid": {
    "type": "string",
    "description": "Old Credential → INVALID"
   },
   "oldDeviceBindingRemoved": {
    "type": "string",
    "description": "Old Device Binding → REMOVED"
   },
   "recipientCredentialActiveEligible": {
    "type": "string",
    "description": "Recipient Credential → ACTIVE/ELIGIBLE"
   }
  }
 },
 "DeviceBindingSessionSecurityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Device Binding & Session Security displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumActiveDevices": {
    "type": "integer",
    "description": "Maximum Active Devices (the pack shows 1)"
   },
   "concurrentSessions": {
    "type": "integer",
    "description": "Concurrent Sessions (the pack shows 1)"
   },
   "notAllowed": {
    "type": "boolean",
    "description": "Not allowed"
   },
   "allowedBeforeFirstUse": {
    "type": "string",
    "description": "Allowed before first use"
   },
   "otpVerificationRequired": {
    "type": "boolean",
    "description": "OTP verification required"
   },
   "operatorApprovalRequired": {
    "type": "boolean",
    "description": "Operator approval required"
   },
   "supervisorApprovalRequired": {
    "type": "boolean",
    "description": "Supervisor approval required"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "deviceId": {
    "type": "string",
    "description": "Device ID"
   },
   "deviceReference": {
    "type": "string",
    "description": "Device reference"
   },
   "appInstallation": {
    "type": "string",
    "description": "App installation"
   },
   "os": {
    "type": "integer",
    "description": "OS"
   },
   "registrationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Registration date"
   },
   "lastActivation": {
    "type": "string",
    "format": "date-time",
    "description": "Last activation"
   },
   "lastKnownVenue": {
    "type": "string",
    "format": "date-time",
    "description": "Last known venue"
   },
   "securityStatus": {
    "type": "integer",
    "description": "Security status"
   },
   "andSimultaneously": {
    "type": "string",
    "description": "and simultaneously"
   }
  }
 },
 "DigitalCredentialSecurityCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Digital Credential Security Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dynamicQrTickets": {
    "type": "integer",
    "description": "Dynamic QR Tickets"
   },
   "membershipCredentials": {
    "type": "integer",
    "description": "Membership Credentials"
   },
   "annualPasses": {
    "type": "integer",
    "description": "Annual Passes"
   },
   "mobileWalletCredentials": {
    "type": "integer",
    "description": "Mobile Wallet Credentials"
   },
   "loyaltyCredentials": {
    "type": "integer",
    "description": "Loyalty Credentials"
   },
   "digitalPasses": {
    "type": "integer",
    "description": "Digital Passes"
   },
   "eventCredentials": {
    "type": "integer",
    "description": "Event Credentials"
   },
   "activeDigitalCredentials": {
    "type": "integer",
    "description": "Active Digital Credentials"
   },
   "dynamicQrEnabled": {
    "type": "boolean",
    "description": "Dynamic QR Enabled"
   },
   "deviceBoundCredentials": {
    "type": "integer",
    "description": "Device-Bound Credentials"
   },
   "locationProtectedCredentials": {
    "type": "integer",
    "description": "Location-Protected Credentials"
   },
   "offlineReadyCredentials": {
    "type": "integer",
    "description": "Offline-Ready Credentials"
   },
   "credentialsRevokedToday": {
    "type": "string",
    "description": "Credentials Revoked Today"
   },
   "securityAlerts": {
    "type": "integer",
    "description": "Security Alerts"
   },
   "suspiciousSessions": {
    "type": "integer",
    "description": "Suspicious Sessions"
   }
  }
 },
 "DynamicQrSecurityProfileBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is access.scan_event at 7%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Dynamic QR Security Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "static": {
    "type": "string",
    "description": "Static"
   },
   "dynamic": {
    "type": "string",
    "description": "Dynamic"
   },
   "dynamicDeviceBound": {
    "type": "string",
    "description": "Dynamic + Device Bound"
   },
   "dynamicLocationBound": {
    "type": "string",
    "description": "Dynamic + Location Bound"
   },
   "refreshEvery30Seconds": {
    "type": "string",
    "description": "Refresh Every: 30 seconds"
   },
   "custom": {
    "type": "string",
    "description": "Custom"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential ID"
   },
   "ticketId": {
    "type": "string",
    "description": "Ticket ID"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "nonceOtp": {
    "type": "string",
    "description": "Nonce / OTP"
   },
   "deviceBindingReference": {
    "type": "string",
    "description": "Device binding reference"
   },
   "venueContext": {
    "type": "string",
    "description": "Venue context"
   },
   "entitlementPayload": {
    "type": "string",
    "description": "Entitlement payload"
   },
   "cryptographicSignatureKeyReference": {
    "type": "string",
    "description": "cryptographic signature/key reference"
   },
   "screens": {
    "type": "string",
    "description": "screens"
   }
  }
 },
 "DynamicQrSecurityProfileBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Dynamic QR Security Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "static": {
    "type": "string",
    "description": "Static"
   },
   "dynamic": {
    "type": "string",
    "description": "Dynamic"
   },
   "dynamicDeviceBound": {
    "type": "string",
    "description": "Dynamic + Device Bound"
   },
   "dynamicLocationBound": {
    "type": "string",
    "description": "Dynamic + Location Bound"
   },
   "refreshEvery30Seconds": {
    "type": "string",
    "description": "Refresh Every: 30 seconds"
   },
   "custom": {
    "type": "string",
    "description": "Custom"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential ID"
   },
   "ticketId": {
    "type": "string",
    "description": "Ticket ID"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "nonceOtp": {
    "type": "string",
    "description": "Nonce / OTP"
   },
   "deviceBindingReference": {
    "type": "string",
    "description": "Device binding reference"
   },
   "venueContext": {
    "type": "string",
    "description": "Venue context"
   },
   "entitlementPayload": {
    "type": "string",
    "description": "Entitlement payload"
   },
   "cryptographicSignatureKeyReference": {
    "type": "string",
    "description": "cryptographic signature/key reference"
   },
   "screens": {
    "type": "string",
    "description": "screens"
   }
  }
 },
 "EmbeddedEntitlementPayloadDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Embedded Entitlement Payload Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "credentialId": {
    "type": "string",
    "description": "Credential ID"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "guestCategory": {
    "type": "string",
    "description": "Guest category"
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
   "attractionPermissions": {
    "type": "string",
    "description": "Attraction permissions"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "expiry"
   },
   "admission": {
    "type": "string",
    "description": "Admission"
   },
   "fastPass": {
    "type": "string",
    "description": "Fast Pass"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "reservation": {
    "type": "string",
    "description": "Reservation"
   },
   "locker": {
    "type": "string",
    "description": "Locker"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "otherPermittedOperationalClaims": {
    "type": "string",
    "description": "other permitted operational claims"
   },
   "ai": {
    "type": "string",
    "description": "AI"
   }
  }
 },
 "EmbeddedEntitlementPayloadDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Embedded Entitlement Payload Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "credentialId": {
    "type": "string",
    "description": "Credential ID"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "guestCategory": {
    "type": "string",
    "description": "Guest category"
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
   "attractionPermissions": {
    "type": "string",
    "description": "Attraction permissions"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "expiry"
   },
   "admission": {
    "type": "string",
    "description": "Admission"
   },
   "fastPass": {
    "type": "string",
    "description": "Fast Pass"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "reservation": {
    "type": "string",
    "description": "Reservation"
   },
   "locker": {
    "type": "string",
    "description": "Locker"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "otherPermittedOperationalClaims": {
    "type": "string",
    "description": "other permitted operational claims"
   },
   "ai": {
    "type": "string",
    "description": "AI"
   }
  }
 },
 "OfflineCryptographicValidationProfileView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline Cryptographic Validation Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "credentialAuthenticity": {
    "type": "string",
    "description": "Credential authenticity"
   },
   "digitalSignature": {
    "type": "string",
    "description": "Digital signature"
   },
   "ticketId": {
    "type": "string",
    "description": "Ticket ID"
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
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit date"
   },
   "timeWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Time window"
   },
   "credentialStatusSnapshot": {
    "type": "string",
    "description": "Credential status snapshot"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "guestCategory": {
    "type": "string",
    "description": "Guest category"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "reservation": {
    "type": "string",
    "description": "Reservation"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "reEntryPermissions": {
    "type": "string",
    "description": "Re-entry permissions"
   },
   "validityPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "validity period"
   },
   "continueRestrictedValidation": {
    "type": "string",
    "description": "Continue restricted validation"
   },
   "operatorWarning": {
    "type": "string",
    "description": "Operator warning"
   },
   "supervisorMode": {
    "type": "string",
    "description": "Supervisor mode"
   },
   "failClosed": {
    "type": "integer",
    "description": "Fail closed"
   },
   "configurableFallback": {
    "type": "string",
    "description": "configurable fallback"
   }
  }
 }
}
```
