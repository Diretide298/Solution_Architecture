# WS04 — Access Control board 4

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
| `BO-174` | Media & Credential Command Center | listDetail | 1 | 0 | — |
| `BO-175` | Media Type & Technology Library | configEditor | 1 | 0 | — |
| `BO-176` | Virtual Credential & Media Association | listDetail | 1 | 0 | — |
| `BO-177` | Verification Method Selection & Locking | listDetail | 1 | 0 | — |
| `BO-178` | Media Issuance & Encoding Profile | listDetail | 1 | 0 | — |
| `BO-179` | Media Swap & Replacement | listDetail | 1 | 0 | — |
| `BO-180` | RFID & NFC Configuration | configEditor | 1 | 0 | — |
| `BO-181` | External & Partner Credential Mapping | configEditor | 1 | 0 | — |
| `BO-182` | Hotel, Wallet & External Media Integration | listDetail | 1 | 0 | — |
| `BO-183` | Media Compatibility, Testing & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-176, BO-177, BO-178, BO-179, BO-182, BO-183 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-174",
  "name": "Media & Credential Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.1",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-credential-command-center-bo-174",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaCredentialCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-175",
    "BO-176",
    "BO-177",
    "BO-178",
    "BO-179",
    "BO-180",
    "BO-181",
    "BO-182",
    "BO-183"
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
     "to": "BO-175",
     "trigger": "Works in Media Type & Technology Library",
     "provenance": "flow F114 step 1→2",
     "operation": "listMediaCredential"
    },
    {
     "to": "BO-176",
     "trigger": "Works in Virtual Credential & Media Association",
     "provenance": "flow F114 step 3→4",
     "operation": "listMediaCredential"
    },
    {
     "to": "BO-177",
     "trigger": "Works in Verification Method Selection & Locking",
     "provenance": "flow F114 step 5→6",
     "operation": "listMediaCredential"
    },
    {
     "to": "BO-178",
     "trigger": "Works in Media Issuance & Encoding Profile",
     "provenance": "flow F114 step 7→8",
     "operation": "listMediaCredential"
    },
    {
     "to": "BO-179",
     "trigger": "Works in Media Swap & Replacement",
     "provenance": "flow F114 step 9→10",
     "operation": "listMediaCredential"
    },
    {
     "to": "BO-180",
     "trigger": "Works in RFID & NFC Configuration",
     "provenance": "flow F114 step 11→12",
     "operation": "listMediaCredential"
    },
    {
     "to": "BO-181",
     "trigger": "Works in External & Partner Credential Mapping",
     "provenance": "flow F114 step 13→14",
     "operation": "listMediaCredential"
    },
    {
     "to": "BO-182",
     "trigger": "Works in Hotel, Wallet & External Media Integration",
     "provenance": "flow F114 step 15→16",
     "operation": "listMediaCredential"
    },
    {
     "to": "BO-183",
     "trigger": "Works in Media Compatibility, Testing & Publication",
     "provenance": "flow F114 step 17→18",
     "operation": "listMediaCredential"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Central management page for every media and verification technology supported by Access Control.",
  "purposeNote": "Administrator has one central view of all access credential and media technologies.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search media credential",
       "provenance": "pack Access Control Module_Reference.pdf, page 44 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "MediaCredentialCommandCenterView.ai"
       ],
       "notes": "The pack filters this screen by ai — which are present is a decision the pack already made.",
       "provenance": "pack Access Control Module_Reference.pdf, page 44 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every media credential",
       "columns": [
        "MediaCredentialCommandCenterView.activeMediaProfiles",
        "MediaCredentialCommandCenterView.qrCredentials",
        "MediaCredentialCommandCenterView.rfidCredentials",
        "MediaCredentialCommandCenterView.nfcCredentials",
        "MediaCredentialCommandCenterView.walletCredentials",
        "MediaCredentialCommandCenterView.biometricCredentials",
        "MediaCredentialCommandCenterView.externalCredentials",
        "MediaCredentialCommandCenterView.mediaSwapsToday",
        "MediaCredentialCommandCenterView.failedMediaReads",
        "MediaCredentialCommandCenterView.unknownCredentials",
        "MediaCredentialCommandCenterView.verificationExceptions"
       ],
       "bindsTo": "MediaCredentialCommandCenterView",
       "operation": "listMediaCredential",
       "provenance": "pack Access Control Module_Reference.pdf, page 44 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected media credential",
       "bindsTo": "MediaCredentialCommandCenterView",
       "columns": [
        "MediaCredentialCommandCenterView.activeMediaProfiles",
        "MediaCredentialCommandCenterView.qrCredentials",
        "MediaCredentialCommandCenterView.rfidCredentials",
        "MediaCredentialCommandCenterView.nfcCredentials",
        "MediaCredentialCommandCenterView.walletCredentials",
        "MediaCredentialCommandCenterView.biometricCredentials",
        "MediaCredentialCommandCenterView.externalCredentials",
        "MediaCredentialCommandCenterView.mediaSwapsToday",
        "MediaCredentialCommandCenterView.failedMediaReads",
        "MediaCredentialCommandCenterView.unknownCredentials",
        "MediaCredentialCommandCenterView.verificationExceptions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Media Directory”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 44 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The media credential list.",
   "error": "Could not load. Names which read failed and leaves the media credential untouched.",
   "emptyFirstRun": "No media credential yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the media credential are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaCredential",
    "contract": "access",
    "purpose": "Media & Credential Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MediaCredentialCommandCenterView.activeMediaProfiles",
    "MediaCredentialCommandCenterView.qrCredentials",
    "MediaCredentialCommandCenterView.rfidCredentials",
    "MediaCredentialCommandCenterView.nfcCredentials",
    "MediaCredentialCommandCenterView.walletCredentials",
    "MediaCredentialCommandCenterView.biometricCredentials"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-174"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 44. 12 of 12 labels bound to a contract property; 12 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-175",
  "name": "Media Type & Technology Library",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.2",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-type-technology-library-bo-175",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaTypeTechnologyLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-174"
   ],
   "exitTo": [
    "BO-174"
   ],
   "inferred": false,
   "notes": "**Reached from BO-174, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-174",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F114 step 2→3",
     "operation": "listMediaTypeTechnology"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each profile defines) and no display directory — it is settings, not a population",
  "purpose": "Define reusable media technologies. The matrix expects support for linear barcode, two-dimensional codes, magnetic strips, contact/proximity RFID, NFC and biometric readers.",
  "purposeNote": "New media technologies can be added through configuration/integration rather than changing ticketing business logic.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "technology",
       "provenance": "pack Access Control Module_Reference.pdf, page 45 §Each profile defines"
      },
      {
       "kind": "selectField",
       "label": "encoding format",
       "provenance": "pack Access Control Module_Reference.pdf, page 45 §Each profile defines"
      },
      {
       "kind": "selectField",
       "label": "supported reader types",
       "provenance": "pack Access Control Module_Reference.pdf, page 45 §Each profile defines"
      },
      {
       "kind": "selectField",
       "label": "online/offline capability",
       "provenance": "pack Access Control Module_Reference.pdf, page 45 §Each profile defines"
      },
      {
       "kind": "selectField",
       "label": "writable/read-only",
       "provenance": "pack Access Control Module_Reference.pdf, page 45 §Each profile defines"
      },
      {
       "kind": "selectField",
       "label": "security classification",
       "provenance": "pack Access Control Module_Reference.pdf, page 45 §Each profile defines"
      },
      {
       "kind": "selectField",
       "label": "applicable venues",
       "provenance": "pack Access Control Module_Reference.pdf, page 45 §Each profile defines"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The media type technology configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the media type technology untouched.",
   "emptyFirstRun": "No media type technology configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaTypeTechnology",
    "contract": "access",
    "purpose": "Media Type & Technology Library",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-175"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 45. 0 of 0 labels bound to a contract property; 7 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-176",
  "name": "Virtual Credential & Media Association",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.3",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/virtual-credential-media-association-bo-176",
   "component": "apps/venue-management-web/src/routes/access-venue/VirtualCredentialMediaAssociation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-174"
   ],
   "exitTo": [
    "BO-174"
   ],
   "inferred": false,
   "notes": "**Reached from BO-174, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-174",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F114 step 4→5",
     "operation": "listVirtualCredentialMedia"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Associate one virtual ticket identity with its permitted media representations.",
  "purposeNote": "Different media representations resolve consistently to a single virtual credential and access state.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 46"
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
       "impliedBy": "listVirtualCredentialMedia",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The virtual credential media list.",
   "error": "Could not load. Names which read failed and leaves the virtual credential media untouched.",
   "emptyFirstRun": "No virtual credential media yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the virtual credential media are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVirtualCredentialMedia",
    "contract": "access",
    "purpose": "Virtual Credential & Media Association",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "VirtualCredentialMediaAssociationView.andThereforeToTheSame",
    "VirtualCredentialMediaAssociationView.ticket",
    "VirtualCredentialMediaAssociationView.guest",
    "VirtualCredentialMediaAssociationView.entitlements",
    "VirtualCredentialMediaAssociationView.accessHistory"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-176"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-177",
  "name": "Verification Method Selection & Locking",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.4",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/verification-method-selection-locking-bo-177",
   "component": "apps/venue-management-web/src/routes/access-venue/VerificationMethodSelectionLocking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-174"
   ],
   "exitTo": [
    "BO-174"
   ],
   "inferred": false,
   "notes": "**Reached from BO-174, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-174",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F114 step 6→7",
     "operation": "listVerificationMethodSelection"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control which verification method the guest chooses and when it becomes locked. The matrix specifies that although a ticket may technically support physical card, Dynamic QR, Face Pass and Face Tag, the customer should select one verification method. It may be changed before first successful verification, but after that the guest cannot change it; authorized venue operations may do so when necessary.",
  "purposeNote": "The selected verification method follows configurable locking and authorized-override policies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 47"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 47"
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
       "impliedBy": "listVerificationMethodSelection",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The verification method selection list.",
   "error": "Could not load. Names which read failed and leaves the verification method selection untouched.",
   "emptyFirstRun": "No verification method selection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the verification method selection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVerificationMethodSelection",
    "contract": "access",
    "purpose": "Verification Method Selection & Locking",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "VerificationMethodSelectionLockingView.dynamicQr",
    "VerificationMethodSelectionLockingView.physicalCard",
    "VerificationMethodSelectionLockingView.rfid",
    "VerificationMethodSelectionLockingView.facePass",
    "VerificationMethodSelectionLockingView.faceTag"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-177"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 47. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-178",
  "name": "Media Issuance & Encoding Profile",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.5",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-issuance-encoding-profile-bo-178",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaIssuanceEncodingProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-174"
   ],
   "exitTo": [
    "BO-174"
   ],
   "inferred": false,
   "notes": "**Reached from BO-174, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-174",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F114 step 8→9",
     "operation": "listMediaIssuanceEncoding"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Configure how ticket identity is written or encoded onto each medium. The source requires ticket IDs to be generated as 2D barcode, QR or RFID and requires randomized, always- unique identifiers to reduce fraud.",
  "purposeNote": "Every issued medium receives a unique and traceable credential identifier using its configured encoding profile.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every media issuance encoding",
       "columns": [
        "MediaIssuanceEncodingProfileView.identifierCollisionCheckEnabled",
        "MediaIssuanceEncodingProfileView.randomizationEnabled",
        "Duplicate Prevention — ENABLED"
       ],
       "bindsTo": "MediaIssuanceEncodingProfileView",
       "operation": "listMediaIssuanceEncoding",
       "provenance": "pack Access Control Module_Reference.pdf, page 48 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected media issuance encoding",
       "bindsTo": "MediaIssuanceEncodingProfileView",
       "columns": [
        "MediaIssuanceEncodingProfileView.identifierCollisionCheckEnabled",
        "MediaIssuanceEncodingProfileView.randomizationEnabled",
        "Duplicate Prevention — ENABLED"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Security”, “Security / Signing Profile”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 48 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The media issuance encoding list.",
   "error": "Could not load. Names which read failed and leaves the media issuance encoding untouched.",
   "emptyFirstRun": "No media issuance encoding yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the media issuance encoding are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaIssuanceEncoding",
    "contract": "access",
    "purpose": "Media Issuance & Encoding Profile",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MediaIssuanceEncodingProfileView.identifierCollisionCheckEnabled",
    "MediaIssuanceEncodingProfileView.randomizationEnabled",
    "Duplicate Prevention — ENABLED"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-178"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 48. 2 of 3 labels bound to a contract property; 9 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-179",
  "name": "Media Swap & Replacement",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.6",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-swap-replacement-bo-179",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaSwapReplacement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-174"
   ],
   "exitTo": [
    "BO-174"
   ],
   "inferred": false,
   "notes": "**Reached from BO-174, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-174",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F114 step 10→11",
     "operation": "listMediaSwapReplacement"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Transfer a ticket from one medium to another without changing the underlying virtual ticket. This directly covers the matrix requirement to swap RFID to barcode/QR or vice versa while transferring the attached information.",
  "purposeNote": "Media can be replaced without changing or duplicating the underlying ticket entitlement.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 49"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 49"
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
       "impliedBy": "listMediaSwapReplacement",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The media swap replacement list.",
   "error": "Could not load. Names which read failed and leaves the media swap replacement untouched.",
   "emptyFirstRun": "No media swap replacement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the media swap replacement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaSwapReplacement",
    "contract": "access",
    "purpose": "Media Swap & Replacement",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MediaSwapReplacementView.to",
    "MediaSwapReplacementView.ticket",
    "MediaSwapReplacementView.guest",
    "MediaSwapReplacementView.remainingEntitlements",
    "MediaSwapReplacementView.entryHistory"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-179"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-180",
  "name": "RFID & NFC Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.7",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/rfid-nfc-configuration-bo-180",
   "component": "apps/venue-management-web/src/routes/access-venue/RfidNfcConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-174"
   ],
   "exitTo": [
    "BO-174"
   ],
   "inferred": false,
   "notes": "**Reached from BO-174, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-174",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F114 step 12→13",
     "operation": "setRfidNfc"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Provide dedicated configuration for proximity credentials. The matrix requires RFID—including ISO 15693—and NFC, as well as multi-range RFID scanning at near, medium and far ranges.",
  "purposeNote": "RFID/NFC technologies can be configured according to operational range, reader capability and access journey.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "RFID standard",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "tag/card type",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "frequency/interface profile",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "reader compatibility",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "read/write behavior",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "encoding profile",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "NFC ticket",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "membership",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "mobile device",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "wallet credential",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
      },
      {
       "kind": "selectField",
       "label": "supported readers",
       "provenance": "pack Access Control Module_Reference.pdf, page 50 §Configure"
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
       "provenance": "contract operation setRfidNfc"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rfid nfc configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the rfid nfc untouched.",
   "emptyFirstRun": "No rfid nfc configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRfidNfc",
    "contract": "access",
    "purpose": "RFID & NFC Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setRfidNfc"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-180"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 50. 0 of 0 labels bound to a contract property; 11 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-181",
  "name": "External & Partner Credential Mapping",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.8",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/external-partner-credential-mapping-bo-181",
   "component": "apps/venue-management-web/src/routes/access-venue/ExternalPartnerCredentialMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-174"
   ],
   "exitTo": [
    "BO-174"
   ],
   "inferred": false,
   "notes": "**Reached from BO-174, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-174",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F114 step 14→15",
     "operation": "listExternalPartnerCredential"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow TICVAI Access Control to understand credentials generated by other systems. The matrix explicitly requires reading reseller/external partner ticket formats and barcodes generated by other systems.",
  "purposeNote": "Approved external ticket formats can be recognized and normalized into TICVAI's standard access transaction model.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Local Mapping",
       "provenance": "pack Access Control Module_Reference.pdf, page 51 §Configure"
      },
      {
       "kind": "selectField",
       "label": "API Validation",
       "provenance": "pack Access Control Module_Reference.pdf, page 51 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Token Validation",
       "provenance": "pack Access Control Module_Reference.pdf, page 51 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cached Validation",
       "provenance": "pack Access Control Module_Reference.pdf, page 51 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Offline Mapping",
       "provenance": "pack Access Control Module_Reference.pdf, page 51 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The external partner credential configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the external partner credential untouched.",
   "emptyFirstRun": "No external partner credential configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listExternalPartnerCredential",
    "contract": "access",
    "purpose": "External & Partner Credential Mapping",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-181"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 51. 0 of 0 labels bound to a contract property; 5 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-182",
  "name": "Hotel, Wallet & External Media Integration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.9",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hotel-wallet-external-media-integration-bo-182",
   "component": "apps/venue-management-web/src/routes/access-venue/HotelWalletExternalMediaIntegration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-174"
   ],
   "exitTo": [
    "BO-174"
   ],
   "inferred": false,
   "notes": "**Reached from BO-174, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-174",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F114 step 16→17",
     "operation": "listHotelWalletExternal"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure specialized external credential ecosystems. The source specifically requires hotel room-card integration at access points and an interface to the hotel's property-management system for room billing.",
  "purposeNote": "Hotel cards, supported wallet credentials and specialized external media can participate in standard TICVAI access journeys.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 53"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 53"
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
       "impliedBy": "listHotelWalletExternal",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hotel wallet external list.",
   "error": "Could not load. Names which read failed and leaves the hotel wallet external untouched.",
   "emptyFirstRun": "No hotel wallet external yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hotel wallet external are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listHotelWalletExternal",
    "contract": "access",
    "purpose": "Hotel, Wallet & External Media Integration",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "HotelWalletExternalMediaIntegrationView.accessDecisionProceedsNormally"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-182"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 53. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-183",
  "name": "Media Compatibility, Testing & Publication",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "4",
   "number": "4.10",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-compatibility-testing-publication-bo-183",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaCompatibilityTestingPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-174"
   ],
   "exitTo": [
    "BO-174"
   ],
   "inferred": false,
   "notes": "**Reached from BO-174, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Ensure that every configured medium works with the intended access-control hardware before deployment. This is particularly important because the matrix says the solution should operate with hardware selected by the venue, while hardware limitations must be highlighted and recommended equipment exposed for procurement decisions.",
  "purposeNote": "Media profiles cannot be deployed to incompatible access devices without an explicit warning/authorized exception. Board 4 — Final 10 Screens # Backend Screen Main Responsibility 4.1 Media & Credential Command Center Overall media estate 4.2 Media Type & Technology Library Barcode, QR, RFID, NFC, wallet, biometric, etc. 4.3 Virtual Credential & Media Association Connect multiple media to one ticket identity 4.4 Verification Method Selection & Locking Guest method selection and first-use lock 4.5 Media Issuance & Encoding Profile Unique identifier and encoding configuration 4.6 Media Swap & Rep",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 54"
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
       "label": "Publish",
       "provenance": "contract operation publishMediaCompatibilityTesting"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens for publishMediaCompatibilityTesting"
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
   "loading": "The media compatibility testing list.",
   "error": "Could not load. Names which read failed and leaves the media compatibility testing untouched.",
   "emptyFirstRun": "No media compatibility testing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the media compatibility testing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishMediaCompatibilityTesting",
    "contract": "access",
    "purpose": "Media Compatibility, Testing & Publication",
    "trigger": "onAction",
    "invalidates": [
     "publishMediaCompatibilityTesting"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-183"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 62 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listExternalPartnerCredential": {
  "method": "GET",
  "path": "/external-partner-credential",
  "contract": "access",
  "summary": "External & Partner Credential Mapping",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ExternalPartnerCredentialMappingView"
 },
 "listHotelWalletExternal": {
  "method": "GET",
  "path": "/hotel-wallet-external",
  "contract": "access",
  "summary": "Hotel, Wallet & External Media Integration",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "HotelWalletExternalMediaIntegrationView"
 },
 "listMediaCredential": {
  "method": "GET",
  "path": "/media-credential",
  "contract": "access",
  "summary": "Media & Credential Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaCredentialCommandCenterView"
 },
 "listMediaIssuanceEncoding": {
  "method": "GET",
  "path": "/media-issuance-encoding",
  "contract": "access",
  "summary": "Media Issuance & Encoding Profile",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaIssuanceEncodingProfileView"
 },
 "listMediaSwapReplacement": {
  "method": "GET",
  "path": "/media-swap-replacement",
  "contract": "access",
  "summary": "Media Swap & Replacement",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaSwapReplacementView"
 },
 "listMediaTypeTechnology": {
  "method": "GET",
  "path": "/media-type-technology",
  "contract": "access",
  "summary": "Media Type & Technology Library",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaTypeTechnologyLibraryView"
 },
 "listVerificationMethodSelection": {
  "method": "GET",
  "path": "/verification-method-selection",
  "contract": "access",
  "summary": "Verification Method Selection & Locking",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VerificationMethodSelectionLockingView"
 },
 "listVirtualCredentialMedia": {
  "method": "GET",
  "path": "/virtual-credential-media",
  "contract": "access",
  "summary": "Virtual Credential & Media Association",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VirtualCredentialMediaAssociationView"
 },
 "publishMediaCompatibilityTesting": {
  "method": "PUT",
  "path": "/media-compatibility-testing",
  "contract": "access",
  "summary": "Media Compatibility, Testing & Publication",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "MediaCompatibilityTestingPublicationInput",
  "responds": "MediaCompatibilityTestingPublicationView"
 },
 "setRfidNfc": {
  "method": "PUT",
  "path": "/rfid-nfc",
  "contract": "access",
  "summary": "RFID & NFC Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "RfidNfcConfigurationInput",
  "responds": "RfidNfcConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ExternalPartnerCredentialMappingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What External & Partner Credential Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "localMapping": {
    "type": "string",
    "description": "Local Mapping"
   },
   "apiValidation": {
    "type": "string",
    "description": "API Validation"
   },
   "tokenValidation": {
    "type": "string",
    "description": "Token Validation"
   },
   "cachedValidation": {
    "type": "string",
    "description": "Cached Validation"
   },
   "offlineMapping": {
    "type": "integer",
    "description": "Offline Mapping"
   },
   "hybrid": {
    "type": "string",
    "description": "Hybrid"
   },
   "dependingOnPolicy": {
    "type": "string",
    "description": "depending on policy"
   }
  }
 },
 "HotelWalletExternalMediaIntegrationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Hotel, Wallet & External Media Integration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "accessDecisionProceedsNormally": {
    "type": "string",
    "description": "Access decision proceeds normally"
   }
  }
 },
 "MediaCompatibilityTestingPublicationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Media Compatibility, Testing & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "rfid": {
    "type": "string",
    "description": "RFID ✓ ✓ ✓ ✓"
   },
   "nfc": {
    "type": "string",
    "description": "NFC ✓ ✓ ✓ ✓"
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
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "deviceGroup": {
    "type": "string",
    "description": "Device group"
   },
   "communicate": {
    "type": "string",
    "description": "communicate"
   },
   "theTicketIsFullyRedeemed": {
    "type": "string",
    "description": "the ticket is fully redeemed"
   },
   "retentionDeletionAudit": {
    "type": "string",
    "description": "Retention/Deletion → Audit"
   }
  }
 },
 "MediaCompatibilityTestingPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Compatibility, Testing & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "rfid": {
    "type": "string",
    "description": "RFID ✓ ✓ ✓ ✓"
   },
   "nfc": {
    "type": "string",
    "description": "NFC ✓ ✓ ✓ ✓"
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
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "deviceGroup": {
    "type": "string",
    "description": "Device group"
   },
   "communicate": {
    "type": "string",
    "description": "communicate"
   },
   "theTicketIsFullyRedeemed": {
    "type": "string",
    "description": "the ticket is fully redeemed"
   },
   "retentionDeletionAudit": {
    "type": "string",
    "description": "Retention/Deletion → Audit"
   }
  }
 },
 "MediaCredentialCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media & Credential Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeMediaProfiles": {
    "type": "integer",
    "description": "Active Media Profiles"
   },
   "qrCredentials": {
    "type": "integer",
    "description": "QR Credentials"
   },
   "rfidCredentials": {
    "type": "integer",
    "description": "RFID Credentials"
   },
   "nfcCredentials": {
    "type": "integer",
    "description": "NFC Credentials"
   },
   "walletCredentials": {
    "type": "integer",
    "description": "Wallet Credentials"
   },
   "biometricCredentials": {
    "type": "integer",
    "description": "Biometric Credentials"
   },
   "externalCredentials": {
    "type": "integer",
    "description": "External Credentials"
   },
   "mediaSwapsToday": {
    "type": "string",
    "description": "Media Swaps Today"
   },
   "failedMediaReads": {
    "type": "integer",
    "description": "Failed Media Reads"
   },
   "unknownCredentials": {
    "type": "integer",
    "description": "Unknown Credentials"
   },
   "verificationExceptions": {
    "type": "integer",
    "description": "Verification Exceptions"
   },
   "ai": {
    "type": "string",
    "description": "AI"
   }
  }
 },
 "MediaIssuanceEncodingProfileView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Issuance & Encoding Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "credentialIdentifier": {
    "type": "string",
    "description": "Credential identifier"
   },
   "randomizedMediaIdentifier": {
    "type": "string",
    "description": "Randomized media identifier"
   },
   "ticketIdReference": {
    "type": "string",
    "description": "Ticket ID reference"
   },
   "secureToken": {
    "type": "string",
    "description": "Secure token"
   },
   "secureReference": {
    "type": "string",
    "description": "Secure reference"
   },
   "encodingFormat": {
    "type": "string",
    "description": "Encoding format"
   },
   "offlinePayloadProfile": {
    "type": "integer",
    "description": "offline payload profile"
   },
   "checksumSignatureWhereApplicable": {
    "type": "string",
    "description": "checksum/signature where applicable"
   },
   "identifierCollisionCheckEnabled": {
    "type": "boolean",
    "description": "Identifier Collision Check — ENABLED"
   },
   "randomizationEnabled": {
    "type": "boolean",
    "description": "Randomization — ENABLED"
   },
   "insteadAdministratorsSelectAControlled": {
    "type": "string",
    "description": "Instead administrators select a controlled"
   }
  }
 },
 "MediaSwapReplacementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Swap & Replacement displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "to": {
    "type": "string",
    "description": "To"
   },
   "ticket": {
    "type": "string",
    "description": "✓ Ticket"
   },
   "guest": {
    "type": "string",
    "description": "✓ Guest"
   },
   "remainingEntitlements": {
    "type": "string",
    "description": "✓ Remaining entitlements"
   },
   "entryHistory": {
    "type": "string",
    "description": "✓ Entry history"
   },
   "reEntryStatus": {
    "type": "string",
    "description": "✓ Re-entry status"
   },
   "fastPassBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "✓ Fast Pass balance"
   },
   "reservations": {
    "type": "string",
    "description": "✓ Reservations"
   },
   "membershipAssociation": {
    "type": "string",
    "description": "✓ Membership association"
   },
   "reasonsType": {
    "type": "string",
    "enum": [
     "lost",
     "damaged",
     "deviceChange",
     "upgrade",
     "guestRequest",
     "operationalReplacement",
     "fraudSecurity",
     "accessibility"
    ],
    "description": "Vocabulary listed under Swap Reasons."
   }
  }
 },
 "MediaTypeTechnologyLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Type & Technology Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "qr": {
    "type": "string",
    "description": "QR"
   },
   "contact": {
    "type": "string",
    "description": "Contact"
   },
   "proximity": {
    "type": "string",
    "description": "Proximity"
   },
   "iso15693": {
    "type": "string",
    "description": "ISO 15693"
   },
   "otherSupportedStandards": {
    "type": "string",
    "description": "Other supported standards"
   },
   "appCredential": {
    "type": "string",
    "description": "App Credential"
   },
   "mobileWallet": {
    "type": "string",
    "description": "Mobile Wallet"
   },
   "paperTicket": {
    "type": "string",
    "description": "Paper Ticket"
   },
   "wristband": {
    "type": "string",
    "description": "Wristband"
   },
   "plasticCard": {
    "type": "string",
    "description": "Plastic Card"
   },
   "hotelCard": {
    "type": "string",
    "description": "Hotel Card"
   },
   "facePass": {
    "type": "string",
    "description": "Face Pass"
   },
   "faceTag": {
    "type": "string",
    "description": "Face Tag"
   },
   "partnerQr": {
    "type": "string",
    "description": "Partner QR"
   },
   "externalBarcode": {
    "type": "string",
    "description": "External Barcode"
   },
   "thirdPartyCredential": {
    "type": "string",
    "description": "Third-party Credential"
   },
   "technology": {
    "type": "string",
    "description": "technology"
   },
   "encodingFormat": {
    "type": "string",
    "description": "encoding format"
   },
   "supportedReaderTypes": {
    "type": "string",
    "description": "supported reader types"
   },
   "onlineOfflineCapability": {
    "type": "integer",
    "description": "online/offline capability"
   },
   "writableReadOnly": {
    "type": "string",
    "description": "writable/read-only"
   },
   "securityClassification": {
    "type": "string",
    "description": "security classification"
   },
   "applicableVenues": {
    "type": "string",
    "description": "applicable venues"
   },
   "applicableProducts": {
    "type": "string",
    "description": "applicable products"
   }
  }
 },
 "RfidNfcConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What RFID & NFC Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "rfidStandard": {
    "type": "string",
    "description": "RFID standard"
   },
   "tagCardType": {
    "type": "string",
    "description": "tag/card type"
   },
   "frequencyInterfaceProfile": {
    "type": "string",
    "description": "frequency/interface profile"
   },
   "readerCompatibility": {
    "type": "string",
    "description": "reader compatibility"
   },
   "readWriteBehavior": {
    "type": "string",
    "description": "read/write behavior"
   },
   "encodingProfile": {
    "type": "string",
    "description": "encoding profile"
   },
   "securityProfile": {
    "type": "string",
    "description": "security profile"
   },
   "nfcTicket": {
    "type": "string",
    "description": "NFC ticket"
   },
   "membership": {
    "type": "string",
    "description": "membership"
   },
   "mobileDevice": {
    "type": "string",
    "description": "mobile device"
   },
   "walletCredential": {
    "type": "string",
    "description": "wallet credential"
   },
   "supportedReaders": {
    "type": "string",
    "description": "supported readers"
   },
   "offlineCapability": {
    "type": "integer",
    "description": "offline capability"
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
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "journey": {
    "type": "string",
    "description": "Journey"
   }
  }
 },
 "RfidNfcConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What RFID & NFC Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "rfidStandard": {
    "type": "string",
    "description": "RFID standard"
   },
   "tagCardType": {
    "type": "string",
    "description": "tag/card type"
   },
   "frequencyInterfaceProfile": {
    "type": "string",
    "description": "frequency/interface profile"
   },
   "readerCompatibility": {
    "type": "string",
    "description": "reader compatibility"
   },
   "readWriteBehavior": {
    "type": "string",
    "description": "read/write behavior"
   },
   "encodingProfile": {
    "type": "string",
    "description": "encoding profile"
   },
   "securityProfile": {
    "type": "string",
    "description": "security profile"
   },
   "nfcTicket": {
    "type": "string",
    "description": "NFC ticket"
   },
   "membership": {
    "type": "string",
    "description": "membership"
   },
   "mobileDevice": {
    "type": "string",
    "description": "mobile device"
   },
   "walletCredential": {
    "type": "string",
    "description": "wallet credential"
   },
   "supportedReaders": {
    "type": "string",
    "description": "supported readers"
   },
   "offlineCapability": {
    "type": "integer",
    "description": "offline capability"
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
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "journey": {
    "type": "string",
    "description": "Journey"
   }
  }
 },
 "VerificationMethodSelectionLockingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Verification Method Selection & Locking displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dynamicQr": {
    "type": "string",
    "description": "☑ Dynamic QR"
   },
   "physicalCard": {
    "type": "string",
    "description": "☑ Physical Card"
   },
   "rfid": {
    "type": "string",
    "description": "☑ RFID"
   },
   "facePass": {
    "type": "string",
    "description": "☑ Face Pass"
   },
   "faceTag": {
    "type": "string",
    "description": "☑ Face Tag"
   },
   "guestNotAllowed": {
    "type": "boolean",
    "description": "Guest — Not Allowed"
   },
   "operationsSupervisorApproval": {
    "type": "string",
    "description": "Operations — Supervisor Approval"
   },
   "verificationMethodLocked": {
    "type": "string",
    "description": "🔒 VERIFICATION METHOD LOCKED"
   },
   "reason": {
    "type": "string",
    "enum": [
     "lostPhone",
     "damagedWristband",
     "accessibility",
     "deviceFailure",
     "guestService",
     "everyChangeIsAudited"
    ],
    "description": "Vocabulary listed under Reason."
   }
  }
 },
 "VirtualCredentialMediaAssociationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Credential & Media Association displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "andThereforeToTheSame": {
    "type": "string",
    "description": "and therefore to the same"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "guest": {
    "type": "string",
    "description": "Guest"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "accessHistory": {
    "type": "string",
    "description": "Access history"
   },
   "consumptionState": {
    "type": "string",
    "description": "Consumption state"
   },
   "simultaneously": {
    "type": "string",
    "description": "simultaneously"
   },
   "qr8x72": {
    "type": "string",
    "description": "QR 8X72"
   },
   "rfid298173": {
    "type": "string",
    "description": "RFID 298173"
   },
   "walletCredential827": {
    "type": "string",
    "description": "Wallet Credential 827"
   },
   "resolvesTo": {
    "type": "string",
    "description": "resolves to"
   }
  }
 }
}
```
