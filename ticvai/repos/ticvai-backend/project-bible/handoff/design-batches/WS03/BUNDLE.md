# WS03 — Access Control board 3

**10 screens · 17 operations · 18 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, GUEST_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-164` | Digital Credential Security Command Center | commandCentre | 4 | 1 | — |
| `BO-165` | Dynamic QR Security Profile Builder | configEditor | 1 | 0 | — |
| `BO-166` | Credential Activation & Display Rules | listDetail | 2 | 0 | — |
| `BO-167` | Device Binding & Session Security | listDetail | 3 | 2 | — |
| `BO-168` | BLE Beacon & Geofence Configuration | configEditor | 1 | 0 | — |
| `BO-169` | Credential Transfer & Rebinding | configEditor | 2 | 1 | — |
| `BO-170` | Credential Revocation & Lifecycle Events | listDetail | 2 | 1 | — |
| `BO-171` | Offline Cryptographic Validation Profile | listDetail | 3 | 1 | — |
| `BO-172` | Embedded Entitlement Payload Designer | listDetail | 1 | 0 | — |
| `BO-173` | Credential Security Simulation, Audit & Publication | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-166, BO-170, BO-171, BO-172, BO-173 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — BO-100 declares entryState.params  and BO-164 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
       "bindsTo": "DigitalCredentialSecurityCommandCenterViewSummary.activeDigitalCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Dynamic QR Enabled",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterViewSummary.dynamicQrEnabled"
      },
      {
       "kind": "metricTile",
       "label": "Device-Bound Credentials",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterViewSummary.deviceBoundCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Location-Protected Credentials",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterViewSummary.locationProtectedCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Offline-Ready Credentials",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterViewSummary.offlineReadyCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Credentials Revoked Today",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterViewSummary.credentialsRevokedToday"
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
       "bindsTo": "DigitalCredentialSecurityCommandCenterViewSummary.securityAlerts"
      },
      {
       "kind": "metricTile",
       "label": "Suspicious Sessions",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §KPI Cards",
       "bindsTo": "DigitalCredentialSecurityCommandCenterViewSummary.suspiciousSessions"
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
        "DigitalCredentialSecurityCommandCenterView.credentialType"
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
        "DigitalCredentialSecurityCommandCenterView.credentialType"
       ],
       "notes": "The pack groups this record's detail under its own headings: “For each credential profile”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 29 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save device binding policy",
       "operation": "setDeviceBindingPolicy",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind Device Binding & Session Security** (BO-167): how many devices a mobile credential may be active on, how many concurrent sessions, and what a device change needs.",
       "provenance": "contract access.yaml PUT /device-binding-policy"
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
   },
   {
    "operationId": "listCredentialSecurity",
    "contract": "access",
    "purpose": "Credential Security Simulation, Audit & Publication",
    "trigger": "onLoad"
   },
   {
    "operationId": "setDynamicSecurityProfile",
    "contract": "access",
    "purpose": "Create or change a dynamic QR security profile from the command centre",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listDigitalCredentialSecurity",
     "listCredentialSecurity"
    ]
   },
   {
    "operationId": "setDeviceBindingPolicy",
    "contract": "access",
    "purpose": "Set the device binding policy of a venue",
    "trigger": "onAction",
    "invalidates": [
     "listDigitalCredentialSecurity",
     "listCredentialSecurity"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "DigitalCredentialSecurityCommandCenterView.credentialType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-164",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-164"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 29. 15 of 15 labels bound to a contract property; 16 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetDeviceBindingPolicy",
    "component": "modal",
    "trigger": "Save device binding policy",
    "body": "**Collects what `setDeviceBindingPolicy` sends before it is called.** Required: `venueId`. Optional: `maximumActiveDevices`, `concurrentSessions`, `deviceChangePolicy`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "DeviceBindingPolicyInput",
    "confirm": {
     "label": "Save device binding policy",
     "operation": "setDeviceBindingPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "maximumActiveDevices",
      "concurrentSessions",
      "deviceChangePolicy"
     ]
    },
    "provenance": "contract access.yaml PUT /device-binding-policy"
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
  "purposeNote": "Administrators can create reusable dynamic-QR security profiles without configuring individual tickets manually.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Options; Configuration may include) and no display directory — it is settings, not a population",
  "purpose": "Configure how a dynamic QR is generated and protected. The matrix requires a unique QR per issued ticket/pass and periodic QR refresh to reduce screenshot and duplication fraud.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-165",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-165"
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
  "purposeNote": "The credential is only displayed in a usable form when its configured activation conditions are satisfied.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure when the guest is permitted to see/use the credential. The matrix specifies that after registration, a ticket may appear as a blurred QR and only become clear and usable near the park entrance.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save activation and display rule",
       "operation": "setCredentialActivationDisplay",
       "provenance": "contract access.yaml PUT /credential-activation-display (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setCredentialActivationDisplay",
    "contract": "access",
    "purpose": "Save activation and display rule",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialActivationDisplayRulesView.beforeActivationDisplay"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-166",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-166"
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
  "purposeNote": "A credential cannot be duplicated across unauthorized devices when device binding is enabled.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Prevent one credential from being shared across unauthorized devices. The source explicitly requires tickets to be linked to a specific device/user and suspicious patterns such as device sharing and multiple simultaneous sessions to be detected.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save device binding policy",
       "operation": "setDeviceBindingPolicy",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind Device Binding & Session Security** (BO-167): how many devices a mobile credential may be active on, how many concurrent sessions, and what a device change needs.",
       "provenance": "contract access.yaml PUT /device-binding-policy"
      },
      {
       "kind": "secondaryButton",
       "label": "Release credential device",
       "operation": "releaseCredentialDevice",
       "permission": "GUEST_MANAGE",
       "notes": "**A service agent frees a credential from a device** (a lost phone, a device change that needs an operator or supervisor under the policy): sets `deactivatedAt` on the binding, so the guest can bind the credential on another device.",
       "provenance": "contract access.yaml POST /device-bindings/{bindingId}/release"
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
   },
   {
    "operationId": "setDeviceBindingPolicy",
    "contract": "access",
    "purpose": "Set the device binding policy of a venue",
    "trigger": "onAction",
    "invalidates": [
     "listDeviceBindingSession"
    ]
   },
   {
    "operationId": "releaseCredentialDevice",
    "contract": "access",
    "purpose": "Release a credential from a device",
    "trigger": "onAction",
    "invalidates": [
     "listDeviceBindingSession"
    ]
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
   ],
   "params": [
    {
     "name": "bindingId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-167",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-167"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 33. 7 of 8 labels bound to a contract property; 8 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetDeviceBindingPolicy",
    "component": "modal",
    "trigger": "Save device binding policy",
    "body": "**Collects what `setDeviceBindingPolicy` sends before it is called.** Required: `venueId`. Optional: `maximumActiveDevices`, `concurrentSessions`, `deviceChangePolicy`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "DeviceBindingPolicyInput",
    "confirm": {
     "label": "Save device binding policy",
     "operation": "setDeviceBindingPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "maximumActiveDevices",
      "concurrentSessions",
      "deviceChangePolicy"
     ]
    },
    "provenance": "contract access.yaml PUT /device-binding-policy"
   },
   {
    "id": "formReleaseCredentialDevice",
    "component": "modal",
    "trigger": "Release credential device",
    "body": "**Collects what `releaseCredentialDevice` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Release credential device",
     "operation": "releaseCredentialDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract access.yaml POST /device-bindings/{bindingId}/release"
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
  "purposeNote": "Digital credentials can automatically activate/deactivate according to configured physical-location context.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Map-Based Configuration; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure location-aware credential activation. This is a major requirement under 3.1.9. The matrix requires BLE beacon proximity and geofence boundaries to activate/deactivate credentials at venue, attraction, zone and gate level.",
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
       "label": "Venue",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Attraction",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Zone",
       "provenance": "pack Access Control Module_Reference.pdf, page 34 §Support"
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-168",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-168"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 34. 0 of 0 labels bound to a contract property; 11 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Venue, Attraction, Zone are choices sent by `setBleBeaconGeofence`.",
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
  "purposeNote": "Transferred tickets cannot remain simultaneously usable by both sender and recipient.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Securely manage digital-ticket transfers. The matrix requires tickets to be transferable through email/app, with the recipient required to authenticate before accessing and activating the transferred QR.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Release credential device",
       "operation": "releaseCredentialDevice",
       "permission": "GUEST_MANAGE",
       "notes": "**A service agent frees a credential from a device** (a lost phone, a device change that needs an operator or supervisor under the policy): sets `deactivatedAt` on the binding, so the guest can bind the credential on another device.",
       "provenance": "contract access.yaml POST /device-bindings/{bindingId}/release"
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
   },
   {
    "operationId": "releaseCredentialDevice",
    "contract": "access",
    "purpose": "Release a credential from a device",
    "trigger": "onAction",
    "invalidates": [
     "listCredentialTransferRebinding"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-169",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-169"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 35. 0 of 0 labels bound to a contract property; 9 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formReleaseCredentialDevice",
    "component": "modal",
    "trigger": "Release credential device",
    "body": "**Collects what `releaseCredentialDevice` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Release credential device",
     "operation": "releaseCredentialDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract access.yaml POST /device-bindings/{bindingId}/release"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bindingId",
     "from": "navigation",
     "optional": true
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
  "purposeNote": "A revoked or replaced credential cannot remain valid within the access ecosystem beyond the configured synchronization/offline security policy.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Immediately invalidate credentials when the underlying ticket changes. Requirement 3.1.4 specifically requires dynamic QR invalidation after refunds, cancellations, transfers, exchanges, upgrades or reissues.",
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
        "CredentialRevocationLifecycleEventsView.propagationTargets"
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
        "CredentialRevocationLifecycleEventsView.propagationTargets"
       ],
       "notes": null,
       "provenance": "pack Access Control Module_Reference.pdf, page 36 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save credential event propagation rule",
       "operation": "setCredentialEventPropagationRule",
       "permission": "ACCESS_POINT_CONFIGURE",
       "provenance": "contract access.yaml PUT /credential-event-propagation-rules"
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
   },
   {
    "operationId": "setCredentialEventPropagationRule",
    "contract": "access",
    "purpose": "Set how a ticket lifecycle event propagates to the credential",
    "trigger": "onAction",
    "invalidates": [
     "listCredentialRevocationLifecycle"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialRevocationLifecycleEventsView.propagationTargets"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-170",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-170"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 36. 5 of 5 labels bound to a contract property; 14 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetCredentialEventPropagationRule",
    "component": "modal",
    "trigger": "Save credential event propagation rule",
    "body": "**Collects what `setCredentialEventPropagationRule` sends before it is called.** Required: `id`, `triggerEvent`, `scopePath`. Optional: `revocationAction`, `propagationTargets`, `monitoredConditions`, `propagation`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessCredentialEventPropagationRule",
    "confirm": {
     "label": "Save credential event propagation rule",
     "operation": "setCredentialEventPropagationRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "triggerEvent",
      "scopePath",
      "revocationAction",
      "propagationTargets",
      "monitoredConditions",
      "propagation"
     ]
    },
    "provenance": "contract access.yaml PUT /credential-event-propagation-rules"
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
  "purposeNote": "Supported credentials can be securely validated offline without exposing private signing secrets to gate devices.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow access devices to validate secure credentials without continuous backend connectivity. The matrix explicitly requires offline cryptographic validation and embedded entitlement validation without real-time backend connectivity.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save offline policy",
       "operation": "setOfflinePolicy",
       "permission": "TENANT_CONFIGURE",
       "notes": "Board 5 of the client's POS set, and **one of only two things in 36 board screens the package could not do.** ADR-0013 makes the POS local-first and nothing configured the policy.",
       "provenance": "contract tenancy.yaml PUT /offline-policy"
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
    "operationId": "setGateOfflinePolicy",
    "purpose": "Save the gate offline validation, revocation cache and degraded-mode policy (writers pass, 29 September)",
    "contract": "access"
   },
   {
    "operationId": "listOfflineCryptographicValidation",
    "contract": "access",
    "purpose": "Offline Cryptographic Validation Profile",
    "trigger": "onLoad"
   },
   {
    "operationId": "setOfflinePolicy",
    "contract": "tenancy",
    "purpose": "What a workstation may do with no network, and for how long",
    "trigger": "onAction",
    "invalidates": [
     "listOfflineCryptographicValidation"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "OfflineCryptographicValidationProfileView.offlineChecks"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-171",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-171"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetOfflinePolicy",
    "component": "modal",
    "trigger": "Save offline policy",
    "body": "**Collects what `setOfflinePolicy` sends before it is called.** Required: `scopePath`. Optional: `id`, `maxOfflineHours`, `allowedOffline`, `offlineValueCeiling`, `offlineTransactionCeiling`, `onCeilingBreach`, `requiresManagerToExtend`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "OfflinePolicy",
    "confirm": {
     "label": "Save offline policy",
     "operation": "setOfflinePolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "scopePath",
      "id",
      "maxOfflineHours",
      "allowedOffline",
      "offlineValueCeiling",
      "offlineTransactionCeiling",
      "onCeilingBreach",
      "requiresManagerToExtend"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /offline-policy"
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
  "purposeNote": "Administrators can determine the minimum secure information required for reliable offline admission.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine what operational information can be securely carried by the credential for offline decisions. The matrix permits embedded information including ticket type, seat assignment, event ID, venue access rights, timeslot, reservations, locker assignments, membership entitlements, guest category and validity.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-172",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-172"
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
  "purposeNote": "Credential-security configurations can be tested, approved, deployed, audited and rolled back before affecting live access. Board 3 — Final 10-Screen Structure # Backend Screen Responsibility Digital Credential Security Command Overall credential-security configuration and 3.1",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Test the complete secure credential lifecycle before production deployment.",
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
   },
   {
    "operationId": "listCredentialSecurityOperational",
    "contract": "access",
    "purpose": "Credential Security, Audit & Operational Evidence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-173",
   "workshopBoard": "wireframes/WS20 Access Control Board 3.dc.html#bo-173"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CredentialRevocationLifecycleEventsView"
 },
 "listCredentialSecurity": {
  "method": "GET",
  "path": "/credential-security",
  "contract": "access",
  "summary": "Credential Security Simulation, Audit & Publication",
  "permission": "AUDIT_VIEW",
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
 "listCredentialSecurityOperational": {
  "method": "GET",
  "path": "/credential-security-operational",
  "contract": "access",
  "summary": "Credential Security, Audit & Operational Evidence",
  "permission": "AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "virtualTicket",
    "in": "query",
    "required": false
   },
   {
    "name": "action",
    "in": "query",
    "required": false
   },
   {
    "name": "actor",
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
 "listCredentialTransferRebinding": {
  "method": "GET",
  "path": "/credential-transfer-rebinding",
  "contract": "access",
  "summary": "Credential Transfer & Rebinding",
  "permission": "SCOPE_VIEW",
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
 "listDigitalCredentialSecurity": {
  "method": "GET",
  "path": "/digital-credential-security",
  "contract": "access",
  "summary": "Digital Credential Security Command Center",
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
 "listOfflineCryptographicValidation": {
  "method": "GET",
  "path": "/offline-cryptographic-validation",
  "contract": "access",
  "summary": "Offline Cryptographic Validation Profile",
  "permission": "SCOPE_VIEW",
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
  "responds": "OfflineCryptographicValidationProfileView"
 },
 "releaseCredentialDevice": {
  "method": "POST",
  "path": "/device-bindings/{bindingId}/release",
  "contract": "access",
  "summary": "Release a credential from a device",
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
  "responds": "AccessDeviceBinding"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "BleBeaconGeofenceConfigurationInput",
  "responds": "BleBeaconGeofenceConfigurationView"
 },
 "setCredentialActivationDisplay": {
  "method": "PUT",
  "path": "/credential-activation-display",
  "contract": "access",
  "summary": "Save a credential activation and display rule",
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
  "requestBody": "CredentialActivationDisplayRulesInput",
  "responds": "CredentialActivationDisplayRulesView"
 },
 "setCredentialEventPropagationRule": {
  "method": "PUT",
  "path": "/credential-event-propagation-rules",
  "contract": "access",
  "summary": "Set how a ticket lifecycle event propagates to the credential",
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
  "requestBody": "AccessCredentialEventPropagationRule",
  "responds": "AccessCredentialEventPropagationRule"
 },
 "setDeviceBindingPolicy": {
  "method": "PUT",
  "path": "/device-binding-policy",
  "contract": "access",
  "summary": "Set the device binding policy of a venue",
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
  "requestBody": "DeviceBindingPolicyInput",
  "responds": "AccessCredentialPolicy"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "EmbeddedEntitlementPayloadDesignerInput",
  "responds": "EmbeddedEntitlementPayloadDesignerView"
 },
 "setGateOfflinePolicy": {
  "method": "PUT",
  "path": "/offline-policies",
  "contract": "access",
  "summary": "Set the offline policy of a venue",
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
  "requestBody": "AccessOfflinePolicy",
  "responds": "AccessOfflinePolicy"
 },
 "setOfflinePolicy": {
  "method": "PUT",
  "path": "/offline-policy",
  "contract": "tenancy",
  "summary": "What a workstation may do with no network, and for how long",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "OfflinePolicy",
  "responds": "OfflinePolicy"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessCredentialEventPropagationRule": {
  "type": "object",
  "x-ticvai-persistence": "access.credential_event_propagation_rule",
  "description": "For one ticket lifecycle event, the revocation action on the credential and how the change propagates to every bound medium, with the conditions monitored (declared 29 September, data-model close-out DM1).",
  "required": [
   "id",
   "triggerEvent",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "triggerEvent": {
    "type": "string",
    "enum": [
     "entry",
     "exit",
     "redemption",
     "partialConsumption",
     "cancellation",
     "refund",
     "suspension",
     "reactivation",
     "transfer",
     "exchange",
     "upgrade",
     "reissue",
     "expiry",
     "replacement",
     "manualInvalidation",
     "fraudLock",
     "accountSuspension"
    ],
    "description": "Unique per scope; one vocabulary for both screens that read it (decided 29 September, writers pass)"
   },
   "revocationAction": {
    "type": "string",
    "nullable": true,
    "enum": [
     "invalidate",
     "suspend",
     "replace"
    ],
    "description": "What happens to the credential; refund, exchange and reissue always revoke"
   },
   "propagationTargets": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "centralPlatform",
      "mobileApp",
      "gateNetwork",
      "offlineRevocationPackage",
      "walletCredentialService"
     ]
    }
   },
   "monitoredConditions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "delayedUpdates",
      "conflictingStates",
      "offlineTransactionsPendingSynchronization",
      "providerUpdateFailures",
      "staleWalletCredentials"
     ]
    }
   },
   "propagation": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "How the Virtual Ticket state change reaches every bound medium"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AccessCredentialPolicy": {
  "type": "object",
  "x-ticvai-persistence": "access.credential_policy",
  "description": "One credential policy of one kind for a venue - activation and display rule, transfer policy, Virtual Ticket identity configuration or device binding policy; merges the proposed credential_display_rule, transfer_policy and virtual_ticket_config (declared 29 September, data-model close-out DM1). The deviceBinding row is written by setDeviceBindingPolicy (decided 29 September, writers pass).",
  "required": [
   "id",
   "kind",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The ruleId (display rule) or policyId (transfer policy) of the operations"
   },
   "kind": {
    "type": "string",
    "enum": [
     "activationDisplay",
     "transfer",
     "virtualTicketIdentity",
     "deviceBinding"
    ],
    "description": "Which policy this row is; the columns of the other kinds stay null"
   },
   "name": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for activationDisplay and virtualTicketIdentity (one virtualTicketIdentity row per venue)"
   },
   "beforeActivationDisplay": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "hideQr",
      "blurQr",
      "showCountdown",
      "showAvailableAtVenue",
      "showVenueDirections"
     ]
    },
    "description": "activationDisplay - what the guest sees before the credential activates"
   },
   "activeDisplay": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dynamicQr",
      "activationTimer",
      "credentialStatus",
      "remainingEntitlements"
     ]
    },
    "description": "activationDisplay - what the guest sees once it is active"
   },
   "activationTriggers": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "activationDisplay - what activates the credential, e.g. beacon proximity, geofence entry, time before admission"
   },
   "transferAllowed": {
    "type": "boolean",
    "nullable": true,
    "description": "transfer"
   },
   "numberOfTransfers": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "transfer"
   },
   "beforeFirstValidationOnly": {
    "type": "boolean",
    "nullable": true,
    "description": "transfer"
   },
   "requireRecipientAccount": {
    "type": "boolean",
    "nullable": true,
    "description": "transfer"
   },
   "requireOtp": {
    "type": "boolean",
    "nullable": true,
    "description": "transfer"
   },
   "requireAcceptance": {
    "type": "boolean",
    "nullable": true,
    "description": "transfer"
   },
   "returnToSender": {
    "type": "boolean",
    "nullable": true,
    "description": "transfer"
   },
   "transferDeadlineHours": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "transfer - hours before the visit after which transfer closes"
   },
   "cancelPendingAllowed": {
    "type": "boolean",
    "nullable": true,
    "description": "transfer"
   },
   "transferAuditRequired": {
    "type": "boolean",
    "nullable": true,
    "description": "transfer"
   },
   "idGenerationPattern": {
    "type": "string",
    "nullable": true,
    "description": "virtualTicketIdentity - Virtual Ticket ID format: prefix, suffix and length"
   },
   "ticketClassification": {
    "type": "string",
    "nullable": true,
    "description": "virtualTicketIdentity"
   },
   "ticketOwnershipModel": {
    "type": "string",
    "nullable": true,
    "description": "virtualTicketIdentity"
   },
   "holderAssignmentRequirements": {
    "type": "string",
    "nullable": true,
    "description": "virtualTicketIdentity"
   },
   "transferabilityReference": {
    "type": "string",
    "nullable": true,
    "description": "virtualTicketIdentity"
   },
   "validityModel": {
    "type": "string",
    "nullable": true,
    "description": "virtualTicketIdentity"
   },
   "consumptionModel": {
    "type": "string",
    "nullable": true,
    "description": "virtualTicketIdentity"
   },
   "entitlementModel": {
    "type": "string",
    "nullable": true,
    "description": "virtualTicketIdentity"
   },
   "mediaRequirements": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "virtualTicketIdentity - media types a ticket of this configuration must carry"
   },
   "maximumActiveDevices": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "deviceBinding"
   },
   "concurrentSessions": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "deviceBinding"
   },
   "deviceChangePolicy": {
    "type": "string",
    "nullable": true,
    "enum": [
     "notAllowed",
     "allowedBeforeFirstUse",
     "otpVerificationRequired",
     "operatorApprovalRequired",
     "supervisorApprovalRequired"
    ],
    "description": "deviceBinding"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AccessDeviceBinding": {
  "type": "object",
  "x-ticvai-persistence": "access.device_binding",
  "description": "One guest device bound to a credential, with its registration, last activation and security status; the binding policy in force is a deviceBinding row of access.credential_policy (declared 29 September, data-model close-out DM1). Written by bindCredentialDevice (the guest app) and releaseCredentialDevice; securityStatus is set by the sharing detection job (decided 29 September, writers pass).",
  "required": [
   "id",
   "entitlementId",
   "deviceId",
   "registeredAt",
   "securityStatus",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest (pii.subject)"
   },
   "entitlementId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "credentialBindingId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "deviceId": {
    "type": "string",
    "maxLength": 200
   },
   "deviceReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "appInstallationId": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "os": {
    "type": "string",
    "maxLength": 50,
    "nullable": true
   },
   "registeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastActivatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastKnownVenueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "securityStatus": {
    "type": "string",
    "enum": [
     "normal",
     "suspicious",
     "blocked"
    ],
    "default": "normal"
   },
   "deactivatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Set when the binding is removed (deactivation, or a transfer of the credential)"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AccessOfflinePolicy": {
  "type": "object",
  "x-ticvai-persistence": "access.offline_policy",
  "description": "The offline policy of one venue: what gates validate locally and for how long, how old the revocation cache may get, and how devices step down through degraded modes. Merges access.offline_validation_profile, access.revocation_cache_policy and access.degraded_mode_policy (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "venueId",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "maxOfflineDurationHours": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Hours a gate may validate offline"
   },
   "offlineChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "credentialAuthenticity",
      "digitalSignature",
      "ticketId",
      "venue",
      "park",
      "zone",
      "visitDate",
      "timeWindow",
      "credentialStatusSnapshot",
      "ticketType",
      "guestCategory",
      "seat",
      "timeslot",
      "reservation",
      "entitlements",
      "reEntryPermissions",
      "validityPeriod"
     ]
    },
    "description": "What a gate may validate locally"
   },
   "afterThresholdBehavior": {
    "type": "string",
    "enum": [
     "continueRestrictedValidation",
     "operatorWarning",
     "supervisorMode",
     "failClosed",
     "fallback"
    ],
    "nullable": true
   },
   "revocationTriggerEvents": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "fraudLock",
      "refund",
      "cancellation",
      "lostCredential",
      "transfer",
      "reissue",
      "manualInvalidation"
     ]
    },
    "description": "Events that push an invalidation into the offline cache"
   },
   "revocationMaxAllowedAgeMinutes": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Maximum allowed revocation cache age"
   },
   "revocationStalenessAction": {
    "type": "string",
    "enum": [
     "continue",
     "continueWithWarning",
     "restrictedProductsOnly",
     "supervisorMode",
     "denySelectedCredentialClasses",
     "failClosed"
    ],
    "nullable": true,
    "description": "What devices do when the cache is older than the maximum allowed age"
   },
   "operatingModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "online",
      "degraded",
      "edgeMode",
      "localOffline",
      "unsafeExpired"
     ]
    },
    "description": "Operating modes a device moves through as connectivity fails"
   },
   "centralUnavailableAfterSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Seconds without central services before switching to edge mode"
   },
   "edgeUnavailableAfterSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Seconds without the venue edge before switching to local offline"
   },
   "automaticSwitch": {
    "type": "boolean",
    "default": true,
    "description": "Switch modes automatically without stopping guest flow"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "BleBeaconGeofenceConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What BLE Beacon & Geofence Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
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
    "description": "Metres"
   },
   "activeInactive": {
    "type": "string",
    "enum": [
     "active",
     "inactive"
    ],
    "description": "Active/Inactive"
   },
   "health": {
    "type": "string",
    "enum": [
     "healthy",
     "degraded",
     "offline"
    ],
    "description": "Read-only, reported by the beacon"
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
   },
   "geofenceRadiusMeters": {
    "type": "integer",
    "description": "Radius of a circular activation zone"
   },
   "geofenceBoundary": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Polygon points as lat,lng when the zone is drawn"
   }
  },
  "required": [
   "beaconId",
   "venue"
  ]
 },
 "BleBeaconGeofenceConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What BLE Beacon & Geofence Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "description": "Metres"
   },
   "activeInactive": {
    "type": "string",
    "enum": [
     "active",
     "inactive"
    ],
    "description": "Active/Inactive"
   },
   "health": {
    "type": "string",
    "enum": [
     "healthy",
     "degraded",
     "offline"
    ],
    "description": "Read-only, reported by the beacon"
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
   },
   "geofenceRadiusMeters": {
    "type": "integer",
    "description": "Radius of a circular activation zone"
   },
   "geofenceBoundary": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Polygon points as lat,lng when the zone is drawn"
   }
  },
  "required": [
   "beaconId",
   "venue"
  ]
 },
 "CredentialActivationDisplayRulesInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Credential Activation & Display Rules submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "venueId",
   "name",
   "beforeActivationDisplay",
   "activeDisplay",
   "activationTriggers"
  ],
  "properties": {
   "ruleId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent creates a rule"
   },
   "venueId": {
    "type": "string",
    "description": "Venue the rule applies to"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "beforeActivationDisplay": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "hideQr",
      "blurQr",
      "showCountdown",
      "showAvailableAtVenue",
      "showVenueDirections"
     ]
    },
    "description": "What the guest sees before the credential activates"
   },
   "activeDisplay": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dynamicQr",
      "activationTimer",
      "credentialStatus",
      "remainingEntitlements"
     ]
    },
    "description": "What the guest sees once it is active"
   },
   "activationTriggers": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "minItems": 1,
    "description": "What activates the credential, e.g. beacon proximity, geofence entry, time before admission"
   }
  }
 },
 "CredentialActivationDisplayRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Activation & Display Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "beforeActivationDisplay": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "hideQr",
      "blurQr",
      "showCountdown",
      "showAvailableAtVenue",
      "showVenueDirections"
     ]
    }
   },
   "activeDisplay": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dynamicQr",
      "activationTimer",
      "credentialStatus",
      "remainingEntitlements"
     ]
    }
   },
   "name": {
    "type": "string"
   },
   "activationTriggers": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Conditions that make the credential eligible, e.g. beaconProximity, geofence, timeWindow"
   }
  },
  "required": [
   "ruleId"
  ]
 },
 "CredentialRevocationLifecycleEventsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Revocation & Lifecycle Events displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "revocationAction": {
    "type": "string",
    "enum": [
     "invalidate",
     "suspend",
     "replace"
    ],
    "description": "What happens to the credential on the event"
   },
   "triggerEvent": {
    "type": "string",
    "enum": [
     "refund",
     "cancellation",
     "transfer",
     "exchange",
     "upgrade",
     "reissue",
     "expiry",
     "manualInvalidation",
     "fraudLock",
     "accountSuspension"
    ],
    "description": "Ticket event, in the access.credential_event_propagation_rule vocabulary (ticketExpiration is expiry) (decided 29 September, writers pass)"
   },
   "propagationTargets": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "centralPlatform",
      "mobileApp",
      "gateNetwork",
      "offlineRevocationPackage",
      "walletCredentialService"
     ]
    }
   }
  },
  "required": [
   "triggerEvent",
   "revocationAction"
  ]
 },
 "CredentialTransferRebindingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Transfer & Rebinding displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "transferAllowed": {
    "type": "boolean"
   },
   "policyId": {
    "type": "string"
   },
   "numberOfTransfers": {
    "type": "integer",
    "description": "Number of transfers"
   },
   "beforeFirstValidationOnly": {
    "type": "boolean",
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
    "type": "boolean",
    "description": "Return to sender"
   },
   "name": {
    "type": "string"
   },
   "transferDeadlineHours": {
    "type": "integer",
    "description": "Hours before the visit after which transfer closes"
   },
   "cancelPendingAllowed": {
    "type": "boolean"
   },
   "transferAuditRequired": {
    "type": "boolean"
   }
  },
  "required": [
   "policyId",
   "transferAllowed"
  ]
 },
 "DeviceBindingPolicyInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; written as the deviceBinding row of access.credential_policy (declared 29 September, writers pass)",
  "required": [
   "venueId"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "maximumActiveDevices": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "Devices the credential may be active on at once"
   },
   "concurrentSessions": {
    "type": "integer",
    "minimum": 1,
    "default": 1
   },
   "deviceChangePolicy": {
    "type": "string",
    "enum": [
     "notAllowed",
     "allowedBeforeFirstUse",
     "otpVerificationRequired",
     "operatorApprovalRequired",
     "supervisorApprovalRequired"
    ],
    "default": "otpVerificationRequired"
   }
  }
 },
 "DynamicQrSecurityProfileBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is access.scan_event at 7%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Dynamic QR Security Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "name": {
    "type": "string"
   },
   "profileId": {
    "type": "string",
    "maxLength": 64,
    "description": "The credential security profile's code (access.credential_security_profile.code) (decided 29 September, writers pass)"
   },
   "qrMode": {
    "type": "string",
    "enum": [
     "static",
     "dynamic",
     "dynamicDeviceBound",
     "dynamicLocationBound",
     "dynamicDeviceLocationBound"
    ]
   },
   "payloadComponents": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "credentialId",
      "ticketId",
      "timestamp",
      "nonceOtp",
      "deviceBindingReference",
      "venueContext",
      "entitlementPayload",
      "signatureKeyReference"
     ]
    },
    "description": "What the QR payload carries"
   },
   "venueId": {
    "type": "string"
   },
   "refreshIntervalSeconds": {
    "type": "integer",
    "description": "QR rotation interval, e.g. 15, 30, 45, 60 or custom"
   }
  },
  "required": [
   "profileId",
   "name",
   "qrMode"
  ]
 },
 "DynamicQrSecurityProfileBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Dynamic QR Security Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "name": {
    "type": "string"
   },
   "profileId": {
    "type": "string"
   },
   "qrMode": {
    "type": "string",
    "enum": [
     "static",
     "dynamic",
     "dynamicDeviceBound",
     "dynamicLocationBound",
     "dynamicDeviceLocationBound"
    ]
   },
   "payloadComponents": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "credentialId",
      "ticketId",
      "timestamp",
      "nonceOtp",
      "deviceBindingReference",
      "venueContext",
      "entitlementPayload",
      "signatureKeyReference"
     ]
    },
    "description": "What the QR payload carries"
   },
   "venueId": {
    "type": "string"
   },
   "refreshIntervalSeconds": {
    "type": "integer",
    "description": "QR rotation interval, e.g. 15, 30, 45, 60 or custom"
   }
  },
  "required": [
   "profileId",
   "name",
   "qrMode"
  ]
 },
 "EmbeddedEntitlementPayloadDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Embedded Entitlement Payload Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "profileId": {
    "type": "string",
    "description": "The credential security profile's code (access.credential_security_profile.code) (decided 29 September, writers pass)",
    "maxLength": 64
   },
   "embeddedClaims": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "credentialId",
      "ticketType",
      "guestCategory",
      "venue",
      "park",
      "zone",
      "attractionPermissions",
      "date",
      "time",
      "timeslot",
      "expiry",
      "admission",
      "fastPass",
      "membership",
      "reservation",
      "locker",
      "seat",
      "otherOperationalClaims"
     ]
    },
    "description": "Claims carried in the credential for offline decisions"
   },
   "name": {
    "type": "string"
   }
  },
  "required": [
   "profileId",
   "embeddedClaims"
  ]
 },
 "EmbeddedEntitlementPayloadDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Embedded Entitlement Payload Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "profileId": {
    "type": "string",
    "description": "Credential security profile the payload belongs to"
   },
   "embeddedClaims": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "credentialId",
      "ticketType",
      "guestCategory",
      "venue",
      "park",
      "zone",
      "attractionPermissions",
      "date",
      "time",
      "timeslot",
      "expiry",
      "admission",
      "fastPass",
      "membership",
      "reservation",
      "locker",
      "seat",
      "otherOperationalClaims"
     ]
    },
    "description": "Claims carried in the credential for offline decisions"
   },
   "name": {
    "type": "string"
   }
  },
  "required": [
   "profileId",
   "embeddedClaims"
  ]
 },
 "OfflineCryptographicValidationProfileView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Offline Cryptographic Validation Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maxOfflineDurationHours": {
    "type": "integer",
    "description": "e.g. 8"
   },
   "offlineChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "credentialAuthenticity",
      "digitalSignature",
      "ticketId",
      "venue",
      "park",
      "zone",
      "visitDate",
      "timeWindow",
      "credentialStatusSnapshot",
      "ticketType",
      "guestCategory",
      "seat",
      "timeslot",
      "reservation",
      "entitlements",
      "reEntryPermissions",
      "validityPeriod"
     ]
    },
    "description": "What a gate may validate locally"
   },
   "afterThresholdBehavior": {
    "type": "string",
    "enum": [
     "continueRestrictedValidation",
     "operatorWarning",
     "supervisorMode",
     "failClosed",
     "fallback"
    ]
   }
  },
  "required": [
   "offlineChecks",
   "maxOfflineDurationHours",
   "afterThresholdBehavior"
  ]
 },
 "OfflinePolicy": {
  "type": "object",
  "x-ticvai-persistence": "platform.offline_policy",
  "description": "Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n**One per scope node, keyed on `scopePath`** (pull audit R162). `id` is server-owned and absent where `getOfflinePolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them is refused `400`, `errors[]` naming the field.\n",
  "required": [
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$",
    "description": "**The node this policy is for, and the key `setOfflinePolicy` upserts on.** The body names its target here, because the path does not.\n"
   },
   "maxOfflineHours": {
    "type": "integer",
    "default": 24,
    "minimum": 1,
    "maximum": 72,
    "description": "**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect. Bounds 1 to 72 hours: proposed, client to correct (audit R129).\n"
   },
   "allowedOffline": {
    "type": "array",
    "description": "**What may happen with no network**, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified.\n",
    "items": {
     "type": "string",
     "enum": [
      "sale",
      "refund",
      "exchange",
      "entitlementIssue",
      "entitlementValidate",
      "loyaltyAccrual",
      "loyaltyRedemption",
      "walletSpend",
      "priceOverride",
      "discount",
      "voidLine",
      "noSale"
     ]
    }
   },
   "offlineValueCeiling": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129).\n"
   },
   "offlineTransactionCeiling": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 5000,
    "description": "**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. Bounds 1 to 5,000: proposed, client to correct (audit R129).\n"
   },
   "onCeilingBreach": {
    "type": "string",
    "enum": [
     "warn",
     "blockNewSales",
     "blockAll"
    ],
    "default": "blockNewSales"
   },
   "requiresManagerToExtend": {
    "type": "boolean",
    "default": true
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
