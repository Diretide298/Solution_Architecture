# WS04 — Access Control board 4

**10 screens · 15 operations · 16 schemas · 2 permissions**

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
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-174` | Media & Credential Command Center | listDetail | 3 | 0 | — |
| `BO-175` | Media Type & Technology Library | configEditor | 2 | 0 | — |
| `BO-176` | Virtual Credential & Media Association | listDetail | 1 | 0 | — |
| `BO-177` | Verification Method Selection & Locking | listDetail | 1 | 0 | — |
| `BO-178` | Media Issuance & Encoding Profile | listDetail | 2 | 0 | — |
| `BO-179` | Media Swap & Replacement | listDetail | 1 | 0 | — |
| `BO-180` | RFID & NFC Configuration | configEditor | 2 | 0 | — |
| `BO-181` | External & Partner Credential Mapping | configEditor | 1 | 0 | — |
| `BO-182` | Hotel, Wallet & External Media Integration | listDetail | 2 | 0 | — |
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
     "provenance": "derived — BO-100 declares entryState.params  and BO-174 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
  "purposeNote": "Administrator has one central view of all access credential and media technologies.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Central management page for every media and verification technology supported by Access Control.",
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
        "MediaCredentialCommandCenterViewSummary.ai"
       ],
       "notes": "The pack filters this screen by ai — which are present is a decision the pack already made.",
       "provenance": "pack Access Control Module_Reference.pdf, page 44 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Media Profiles",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.activeMediaProfiles",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "QR Credentials",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.qrCredentials",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "RFID Credentials",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.rfidCredentials",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "NFC Credentials",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.nfcCredentials",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Wallet Credentials",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.walletCredentials",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Biometric Credentials",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.biometricCredentials",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "External Credentials",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.externalCredentials",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Media Swaps Today",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.mediaSwapsToday",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Failed Media Reads",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.failedMediaReads",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Unknown Credentials",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.unknownCredentials",
       "operation": "listMediaCredential",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Verification Exceptions",
       "bindsTo": "MediaCredentialCommandCenterViewSummary.verificationExceptions",
       "operation": "listMediaCredential",
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
       "label": "Every media credential",
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
   },
   {
    "operationId": "listVirtualCredentialMedia",
    "contract": "access",
    "purpose": "Virtual Credential & Media Association",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMediaTypeCredential",
    "contract": "access",
    "purpose": "Media Type & Credential Technology Registry",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MediaCredentialCommandCenterViewSummary.activeMediaProfiles",
    "MediaCredentialCommandCenterViewSummary.qrCredentials",
    "MediaCredentialCommandCenterViewSummary.rfidCredentials",
    "MediaCredentialCommandCenterViewSummary.nfcCredentials",
    "MediaCredentialCommandCenterViewSummary.walletCredentials",
    "MediaCredentialCommandCenterViewSummary.biometricCredentials"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-174",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-174"
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
  "purposeNote": "New media technologies can be added through configuration/integration rather than changing ticketing business logic.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each profile defines) and no display directory — it is settings, not a population",
  "purpose": "Define reusable media technologies. The matrix expects support for linear barcode, two-dimensional codes, magnetic strips, contact/proximity RFID, NFC and biometric readers.",
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save media type",
       "operation": "setMediaTypeTechnology",
       "provenance": "contract access.yaml PUT /media-type-technology (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setMediaTypeTechnology",
    "contract": "access",
    "purpose": "Save media type",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-175",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-175"
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
  "purposeNote": "Different media representations resolve consistently to a single virtual credential and access state.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Associate one virtual ticket identity with its permitted media representations.",
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
    "VirtualCredentialMediaAssociationView.ticketId",
    "VirtualCredentialMediaAssociationView.guestId",
    "VirtualCredentialMediaAssociationView.entitlements"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-176",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-176"
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
  "purposeNote": "The selected verification method follows configurable locking and authorized-override policies.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control which verification method the guest chooses and when it becomes locked. The matrix specifies that although a ticket may technically support physical card, Dynamic QR, Face Pass and Face Tag, the customer should select one verification method. It may be changed before first successful verification, but after that the guest cannot change it; authorized venue operations may do so when necessary.",
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
    "VerificationMethodSelectionLockingView.availableMethods"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-177",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-177"
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
  "purposeNote": "Every issued medium receives a unique and traceable credential identifier using its configured encoding profile.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Configure how ticket identity is written or encoded onto each medium. The source requires ticket IDs to be generated as 2D barcode, QR or RFID and requires randomized, always- unique identifiers to reduce fraud.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save issuance and encoding profile",
       "operation": "setMediaIssuanceEncoding",
       "provenance": "contract access.yaml PUT /media-issuance-encoding (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setMediaIssuanceEncoding",
    "contract": "access",
    "purpose": "Save issuance and encoding profile",
    "trigger": "onAction"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-178",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-178"
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
  "purposeNote": "Media can be replaced without changing or duplicating the underlying ticket entitlement.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Transfer a ticket from one medium to another without changing the underlying virtual ticket. This directly covers the matrix requirement to swap RFID to barcode/QR or vice versa while transferring the attached information.",
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
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-179",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-179"
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
  "purposeNote": "RFID/NFC technologies can be configured according to operational range, reader capability and access journey.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Provide dedicated configuration for proximity credentials. The matrix requires RFID—including ISO 15693—and NFC, as well as multi-range RFID scanning at near, medium and far ranges.",
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
    "trigger": "onAction"
   },
   {
    "operationId": "setRfidNfcCard",
    "contract": "access",
    "purpose": "RFID, NFC, Card & Wristband Media Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-180",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-180"
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
  "purposeNote": "Approved external ticket formats can be recognized and normalized into TICVAI's standard access transaction model.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow TICVAI Access Control to understand credentials generated by other systems. The matrix explicitly requires reading reseller/external partner ticket formats and barcodes generated by other systems.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-181",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-181"
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
  "purposeNote": "Hotel cards, supported wallet credentials and specialized external media can participate in standard TICVAI access journeys.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure specialized external credential ecosystems. The source specifically requires hotel room-card integration at access points and an interface to the hotel's property-management system for room billing.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save integration",
       "operation": "setHotelWalletExternal",
       "provenance": "contract access.yaml PUT /hotel-wallet-external (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setHotelWalletExternal",
    "contract": "access",
    "purpose": "Save integration",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-182",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-182"
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
  "purposeNote": "Media profiles cannot be deployed to incompatible access devices without an explicit warning/authorized exception. Board 4 — Final 10 Screens # Backend Screen Main Responsibility 4.1 Media & Credential Command Center Overall media estate 4.2 Media Type & Technology Library Barcode, QR, RFID, NFC, wallet, biometric, etc. 4.3 Virtual Credential & Media Association Connect multiple media to one ticket identity 4.4 Verification Method Selection & Locking Guest method selection and first-use lock 4.5 Media Issuance & Encoding Profile Unique identifier and encoding configuration 4.6 Media Swap & Rep",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Ensure that every configured medium works with the intended access-control hardware before deployment. This is particularly important because the matrix says the solution should operate with hardware selected by the venue, while hardware limitations must be highlighted and recommended equipment exposed for procurement decisions.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-183",
   "workshopBoard": "wireframes/WS21 Access Control Board 4.dc.html#bo-183"
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
  "parameters": [
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
    "name": "media",
    "in": "query",
    "required": false
   },
   {
    "name": "credentialType",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "integration",
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
 "listMediaTypeCredential": {
  "method": "GET",
  "path": "/media-type-credential",
  "contract": "access",
  "summary": "Media Type & Credential Technology Registry",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaTypeCredentialTechnologyRegistryView"
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
 "publishMediaCompatibilityTesting": {
  "method": "PUT",
  "path": "/media-compatibility-testing",
  "contract": "access",
  "summary": "Media Compatibility, Testing & Publication",
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
  "requestBody": "MediaCompatibilityTestingPublicationInput",
  "responds": "MediaCompatibilityTestingPublicationView"
 },
 "setHotelWalletExternal": {
  "method": "PUT",
  "path": "/hotel-wallet-external",
  "contract": "access",
  "summary": "Save a hotel, wallet or external media integration",
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
  "requestBody": "HotelWalletExternalMediaIntegrationInput",
  "responds": "HotelWalletExternalMediaIntegrationView"
 },
 "setMediaIssuanceEncoding": {
  "method": "PUT",
  "path": "/media-issuance-encoding",
  "contract": "access",
  "summary": "Save a media issuance and encoding profile",
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
  "requestBody": "MediaIssuanceEncodingProfileInput",
  "responds": "MediaIssuanceEncodingProfileView"
 },
 "setMediaTypeTechnology": {
  "method": "PUT",
  "path": "/media-type-technology",
  "contract": "access",
  "summary": "Add, amend or retire a media type",
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
  "requestBody": "MediaTypeTechnologyLibraryInput",
  "responds": "MediaTypeTechnologyLibraryView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RfidNfcConfigurationInput",
  "responds": "RfidNfcConfigurationView"
 },
 "setRfidNfcCard": {
  "method": "PUT",
  "path": "/rfid-nfc-card",
  "contract": "access",
  "summary": "RFID, NFC, Card & Wristband Media Designer",
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
  "requestBody": "RfidNfcCardWristbandMediaDesignerInput",
  "responds": "RfidNfcCardWristbandMediaDesignerView"
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
   "validationMode": {
    "type": "string",
    "enum": [
     "localMapping",
     "apiValidation",
     "tokenValidation",
     "cachedValidation",
     "offlineMapping",
     "hybrid"
    ],
    "description": "How the partner credential is validated"
   },
   "mappingId": {
    "type": "string"
   },
   "partnerName": {
    "type": "string",
    "description": "e.g. Hotel Package Provider"
   },
   "credentialFormat": {
    "type": "string",
    "description": "Partner barcode/QR format"
   },
   "fieldMappings": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Partner field to TICVAI field pairs, e.g. ProductCode, VisitDate, GuestType, Entitlement"
   },
   "unrecognisedOutcome": {
    "type": "string",
    "enum": [
     "deny",
     "referToOperator"
    ],
    "description": "What happens when a partner credential cannot be resolved"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "active",
     "inactive"
    ]
   }
  }
 },
 "HotelWalletExternalMediaIntegrationInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Hotel, Wallet & External Media Integration submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "name",
   "integrationType",
   "externalSystem"
  ],
  "properties": {
   "integrationId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent creates an integration"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "integrationType": {
    "type": "string",
    "enum": [
     "hotelRoomCard",
     "hotelPms",
     "digitalWallet",
     "otherExternal"
    ]
   },
   "externalSystem": {
    "type": "string",
    "maxLength": 200,
    "description": "The external system, e.g. the hotel PMS product"
   },
   "connectionSecretRef": {
    "type": "string",
    "description": "Reference to the stored credentials of the external system. **Never the secret itself.** The client supplies the account and keys (vendor credential); the reference is set once they are stored"
   },
   "roomChargeEnabled": {
    "type": "boolean",
    "default": false
   },
   "mapsToVirtualCredential": {
    "type": "boolean",
    "default": true,
    "description": "The external card maps to a TICVAI Virtual Ticket rather than being validated by the external system"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "active",
     "inactive"
    ],
    "default": "draft"
   }
  }
 },
 "HotelWalletExternalMediaIntegrationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Hotel, Wallet & External Media Integration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "connectionSecretRef": {
    "type": "string",
    "description": "Reference to the stored credentials of the external system, never the secret itself (decided 29 September, VM close-out)"
   },
   "integrationId": {
    "type": "string"
   },
   "integrationType": {
    "type": "string",
    "enum": [
     "hotelRoomCard",
     "hotelPms",
     "digitalWallet",
     "otherExternal"
    ]
   },
   "name": {
    "type": "string"
   },
   "externalSystem": {
    "type": "string",
    "description": "External system name, e.g. the hotel PMS or wallet provider"
   },
   "roomChargeEnabled": {
    "type": "boolean",
    "description": "Attraction/service may be charged to the guest room via the PMS"
   },
   "mapsToVirtualCredential": {
    "type": "boolean",
    "description": "Credential resolves to a TICVAI virtual credential and follows the normal access decision"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "active",
     "inactive"
    ]
   }
  }
 },
 "MediaCompatibilityTestingPublicationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Media Compatibility, Testing & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "mediaProfileId": {
    "type": "string",
    "description": "Media profile being published"
   },
   "tenantId": {
    "type": "string",
    "description": "Tenant"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "parkId": {
    "type": "string",
    "description": "Park"
   },
   "gateId": {
    "type": "string",
    "description": "Gate"
   },
   "deviceGroupId": {
    "type": "string",
    "description": "Device group"
   },
   "stage": {
    "type": "string",
    "enum": [
     "draft",
     "compatibilityTest",
     "validate",
     "approval",
     "published"
    ]
   },
   "compatibilityWarnings": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Warnings from the compatibility test, e.g. a reader that cannot validate NFC offline"
   },
   "exceptionReason": {
    "type": "string",
    "description": "Required when publishing to a device with a compatibility warning"
   }
  },
  "required": [
   "mediaProfileId",
   "venueId"
  ]
 },
 "MediaCompatibilityTestingPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Compatibility, Testing & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "mediaProfileId": {
    "type": "string",
    "description": "Media profile being published"
   },
   "tenantId": {
    "type": "string",
    "description": "Tenant"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "parkId": {
    "type": "string",
    "description": "Park"
   },
   "gateId": {
    "type": "string",
    "description": "Gate"
   },
   "deviceGroupId": {
    "type": "string",
    "description": "Device group"
   },
   "stage": {
    "type": "string",
    "enum": [
     "draft",
     "compatibilityTest",
     "validate",
     "approval",
     "published"
    ]
   },
   "compatibilityWarnings": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Warnings from the compatibility test, e.g. a reader that cannot validate NFC offline"
   },
   "exceptionReason": {
    "type": "string",
    "description": "Required when publishing to a device with a compatibility warning"
   }
  },
  "required": [
   "mediaProfileId",
   "venueId"
  ]
 },
 "MediaIssuanceEncodingProfileInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Media Issuance & Encoding Profile submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back. The per-credential identifiers the View shows (credential identifier, randomised media identifier, ticket reference, secure token and reference) are generated at issue and are not writable.",
  "required": [
   "name",
   "mediaTypeId",
   "encodingFormat"
  ],
  "properties": {
   "encodingProfileId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent creates a profile"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "mediaTypeId": {
    "type": "string",
    "description": "The media type this profile encodes (`MediaTypeTechnologyLibraryView.mediaTypeId`)"
   },
   "encodingFormat": {
    "type": "string",
    "maxLength": 100
   },
   "offlinePayloadProfile": {
    "type": "string",
    "description": "Which entitlement data is embedded for offline validation"
   },
   "checksumSignatureWhereApplicable": {
    "type": "string",
    "description": "Checksum or signature scheme, where the media carries one"
   },
   "randomizationEnabled": {
    "type": "boolean",
    "default": true,
    "description": "Media identifiers are random rather than sequential"
   },
   "identifierCollisionCheckEnabled": {
    "type": "boolean",
    "default": true
   },
   "duplicatePreventionEnabled": {
    "type": "boolean",
    "default": true
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
    "type": "string",
    "description": "Offline payload profile reference"
   },
   "checksumSignatureWhereApplicable": {
    "type": "string",
    "description": "Reference to the signing profile managed by the secure platform layer; no key material"
   },
   "identifierCollisionCheckEnabled": {
    "type": "boolean",
    "description": "Identifier Collision Check — ENABLED"
   },
   "randomizationEnabled": {
    "type": "boolean",
    "description": "Randomization — ENABLED"
   },
   "encodingProfileId": {
    "type": "string",
    "description": "Encoding profile identifier"
   },
   "name": {
    "type": "string",
    "description": "Profile name, e.g. RFID Wristband, Adventure Park"
   },
   "mediaTypeId": {
    "type": "string",
    "description": "Media type this profile encodes"
   },
   "duplicatePreventionEnabled": {
    "type": "boolean",
    "description": "Duplicate prevention"
   }
  }
 },
 "MediaTypeCredentialTechnologyRegistryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Type & Credential Technology Registry displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "mediaTypeId": {
    "type": "string",
    "description": "Media Type ID"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "category": {
    "type": "string",
    "enum": [
     "digital",
     "physical",
     "biometric",
     "future"
    ],
    "description": "Media category"
   },
   "provider": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Provider integrations that implement this media type (media type is not the vendor)"
   },
   "technology": {
    "type": "string",
    "description": "Technology"
   },
   "tokenFormat": {
    "type": "string",
    "description": "Token format"
   },
   "generationMethod": {
    "type": "string",
    "description": "Generation method"
   },
   "validationMechanism": {
    "type": "string",
    "description": "Validation mechanism"
   },
   "supportsVisualDesign": {
    "type": "boolean",
    "description": "Supports visual design"
   },
   "supportsDynamicUpdate": {
    "type": "boolean",
    "description": "Supports dynamic update"
   },
   "supportsRevocation": {
    "type": "boolean",
    "description": "Supports revocation"
   },
   "supportsExpiration": {
    "type": "boolean",
    "description": "Supports expiration"
   },
   "supportsOfflineReference": {
    "type": "boolean",
    "description": "Supports offline reference"
   },
   "supportsReplacement": {
    "type": "boolean",
    "description": "Supports replacement"
   },
   "supportsEncryption": {
    "type": "boolean",
    "description": "Supports encryption"
   },
   "supportsSigning": {
    "type": "boolean",
    "description": "Supports signing"
   },
   "supportedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Supported channels"
   },
   "supportedDevices": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Supported devices"
   },
   "integrationAdapter": {
    "type": "string",
    "description": "Integration adapter"
   }
  },
  "required": [
   "mediaTypeId",
   "name",
   "category"
  ]
 },
 "MediaTypeTechnologyLibraryInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Media Type & Technology Library submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "name",
   "mediaType",
   "technology",
   "onlineOfflineCapability"
  ],
  "properties": {
   "mediaTypeId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent adds a media type"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "mediaType": {
    "type": "string",
    "enum": [
     "linearBarcode",
     "twoDimensionalBarcode",
     "qr",
     "rfidContact",
     "rfidProximity",
     "rfidIso15693",
     "rfidOtherStandard",
     "appCredential",
     "mobileWallet",
     "paperTicket",
     "wristband",
     "plasticCard",
     "hotelCard",
     "facePass",
     "faceTag",
     "partnerQr",
     "externalBarcode",
     "thirdPartyCredential"
    ]
   },
   "technology": {
    "type": "string",
    "enum": [
     "barcode",
     "rfid",
     "nfc",
     "magneticStripe",
     "mobile",
     "physical",
     "biometric",
     "external"
    ]
   },
   "encodingFormat": {
    "type": "string",
    "maxLength": 100
   },
   "supportedReaderTypes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "onlineOfflineCapability": {
    "type": "string",
    "enum": [
     "onlineOnly",
     "offlineOnly",
     "onlineAndOffline"
    ]
   },
   "writableReadOnly": {
    "type": "string",
    "enum": [
     "writable",
     "readOnly"
    ]
   },
   "securityClassification": {
    "type": "string",
    "maxLength": 100
   },
   "applicableVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Empty means every venue of the tenant"
   },
   "applicableProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Empty means every product"
   },
   "active": {
    "type": "boolean",
    "default": true,
    "description": "False retires the media type: no new credential is issued on it; credentials already issued stay valid until they expire"
   }
  }
 },
 "MediaTypeTechnologyLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Type & Technology Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "active": {
    "type": "boolean",
    "description": "False once retired through `setMediaTypeTechnology`; issued credentials stay valid (decided 29 September, VM close-out)"
   },
   "mediaType": {
    "type": "string",
    "enum": [
     "linearBarcode",
     "twoDimensionalBarcode",
     "qr",
     "rfidContact",
     "rfidProximity",
     "rfidIso15693",
     "rfidOtherStandard",
     "appCredential",
     "mobileWallet",
     "paperTicket",
     "wristband",
     "plasticCard",
     "hotelCard",
     "facePass",
     "faceTag",
     "partnerQr",
     "externalBarcode",
     "thirdPartyCredential"
    ],
    "description": "The kind of medium this profile defines"
   },
   "technology": {
    "type": "string",
    "enum": [
     "barcode",
     "rfid",
     "nfc",
     "magneticStripe",
     "mobile",
     "physical",
     "biometric",
     "external"
    ],
    "description": "Technology family"
   },
   "encodingFormat": {
    "type": "string",
    "description": "encoding format"
   },
   "supportedReaderTypes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "supported reader types"
   },
   "onlineOfflineCapability": {
    "type": "string",
    "enum": [
     "onlineOnly",
     "offlineOnly",
     "onlineAndOffline"
    ],
    "description": "online/offline capability"
   },
   "writableReadOnly": {
    "type": "string",
    "enum": [
     "writable",
     "readOnly"
    ],
    "description": "writable/read-only"
   },
   "securityClassification": {
    "type": "string",
    "description": "security classification"
   },
   "applicableVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Venue ids"
   },
   "applicableProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Product ids"
   },
   "mediaTypeId": {
    "type": "string",
    "description": "Media type profile identifier"
   },
   "name": {
    "type": "string",
    "description": "Profile name"
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
 },
 "RfidNfcCardWristbandMediaDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What RFID, NFC, Card & Wristband Media Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "rfidCard",
     "rfidWristband",
     "nfcCard",
     "nfcWristband",
     "membershipCard",
     "staffGuestCard",
     "customWearable"
    ],
    "description": "Physical medium"
   },
   "reusability": {
    "type": "string",
    "enum": [
     "disposable",
     "reusable"
    ],
    "description": "Disposable or reusable medium"
   },
   "printed": {
    "type": "boolean",
    "description": "Printed"
   },
   "encoded": {
    "type": "boolean",
    "description": "Encoded"
   },
   "colorCategory": {
    "type": "string",
    "description": "Color/category"
   },
   "sizeWhereApplicable": {
    "type": "string",
    "description": "Size where applicable"
   },
   "activationAtCollection": {
    "type": "boolean",
    "description": "Activation at collection"
   },
   "depositReferenceWhereApplicable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit/reference where applicable"
   },
   "mediaDimensions": {
    "type": "string",
    "description": "Media dimensions"
   },
   "front": {
    "type": "string",
    "description": "Front"
   },
   "back": {
    "type": "string",
    "description": "Back"
   },
   "printableArea": {
    "type": "string",
    "description": "Printable area"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "printedFields": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "customerName",
      "photo",
      "membershipTier",
      "expiry",
      "serialNumber",
      "qrBarcode"
     ]
    },
    "description": "Personal and reference fields printed on the medium"
   },
   "customArtwork": {
    "type": "string",
    "description": "Custom artwork"
   },
   "sponsorVenueBranding": {
    "type": "string",
    "description": "Sponsor/venue branding"
   },
   "rfidNfcTechnology": {
    "type": "string",
    "description": "RFID/NFC technology"
   },
   "chipProfile": {
    "type": "string",
    "description": "Chip/profile"
   },
   "uidReferenceHandling": {
    "type": "string",
    "description": "UID/reference handling"
   },
   "encodingProfile": {
    "type": "string",
    "description": "Encoding profile"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "readerCompatibility": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Reader compatibility"
   },
   "printerEncoderIntegration": {
    "type": "string",
    "description": "Printer/encoder integration"
   }
  },
  "required": [
   "templateId",
   "mediaKind"
  ]
 },
 "RfidNfcCardWristbandMediaDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What RFID, NFC, Card & Wristband Media Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Media template being designed"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "rfidCard",
     "rfidWristband",
     "nfcCard",
     "nfcWristband",
     "membershipCard",
     "staffGuestCard",
     "customWearable"
    ],
    "description": "Physical medium"
   },
   "reusability": {
    "type": "string",
    "enum": [
     "disposable",
     "reusable"
    ],
    "description": "Disposable or reusable medium"
   },
   "printed": {
    "type": "boolean",
    "description": "Printed"
   },
   "encoded": {
    "type": "boolean",
    "description": "Encoded"
   },
   "colorCategory": {
    "type": "string",
    "description": "Color/category"
   },
   "sizeWhereApplicable": {
    "type": "string",
    "description": "Size where applicable"
   },
   "activationAtCollection": {
    "type": "boolean",
    "description": "Activation at collection"
   },
   "depositReferenceWhereApplicable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit/reference where applicable"
   },
   "mediaDimensions": {
    "type": "string",
    "description": "Media dimensions"
   },
   "front": {
    "type": "string",
    "description": "Front"
   },
   "back": {
    "type": "string",
    "description": "Back"
   },
   "printableArea": {
    "type": "string",
    "description": "Printable area"
   },
   "logo": {
    "type": "string",
    "description": "Logo"
   },
   "printedFields": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "customerName",
      "photo",
      "membershipTier",
      "expiry",
      "serialNumber",
      "qrBarcode"
     ]
    },
    "description": "Personal and reference fields printed on the medium"
   },
   "customArtwork": {
    "type": "string",
    "description": "Custom artwork"
   },
   "sponsorVenueBranding": {
    "type": "string",
    "description": "Sponsor/venue branding"
   },
   "rfidNfcTechnology": {
    "type": "string",
    "description": "RFID/NFC technology"
   },
   "chipProfile": {
    "type": "string",
    "description": "Chip/profile"
   },
   "uidReferenceHandling": {
    "type": "string",
    "description": "UID/reference handling"
   },
   "encodingProfile": {
    "type": "string",
    "description": "Encoding profile"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "readerCompatibility": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Reader compatibility"
   },
   "printerEncoderIntegration": {
    "type": "string",
    "description": "Printer/encoder integration"
   }
  },
  "required": [
   "templateId",
   "mediaKind"
  ]
 },
 "RfidNfcConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What RFID & NFC Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "name": {
    "type": "string"
   },
   "rfidNfcProfileId": {
    "type": "string",
    "description": "RFID/NFC profile identifier"
   },
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
    "type": "array",
    "items": {
     "type": "string"
    },
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
   "nfcUses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "nfcTicket",
      "membership",
      "mobileDevice",
      "walletCredential"
     ]
    },
    "description": "NFC credential uses enabled by this profile"
   },
   "supportedReaders": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "supported readers"
   },
   "offlineCapability": {
    "type": "boolean",
    "description": "offline capability"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "zoneId": {
    "type": "string",
    "description": "Zone"
   },
   "gateId": {
    "type": "string",
    "description": "Gate"
   },
   "credentialType": {
    "type": "string",
    "description": "Credential"
   },
   "journey": {
    "type": "string",
    "description": "Journey"
   },
   "readRange": {
    "type": "string",
    "enum": [
     "near",
     "medium",
     "far"
    ],
    "description": "Read range associated with the venue, zone, gate, credential or journey"
   }
  },
  "required": [
   "rfidNfcProfileId",
   "venueId",
   "name"
  ]
 },
 "RfidNfcConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What RFID & NFC Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "name": {
    "type": "string"
   },
   "rfidNfcProfileId": {
    "type": "string",
    "description": "RFID/NFC profile identifier"
   },
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
    "type": "array",
    "items": {
     "type": "string"
    },
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
   "nfcUses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "nfcTicket",
      "membership",
      "mobileDevice",
      "walletCredential"
     ]
    },
    "description": "NFC credential uses enabled by this profile"
   },
   "supportedReaders": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "supported readers"
   },
   "offlineCapability": {
    "type": "boolean",
    "description": "offline capability"
   },
   "venueId": {
    "type": "string",
    "description": "Venue"
   },
   "zoneId": {
    "type": "string",
    "description": "Zone"
   },
   "gateId": {
    "type": "string",
    "description": "Gate"
   },
   "credentialType": {
    "type": "string",
    "description": "Credential"
   },
   "journey": {
    "type": "string",
    "description": "Journey"
   },
   "readRange": {
    "type": "string",
    "enum": [
     "near",
     "medium",
     "far"
    ],
    "description": "Read range associated with the venue, zone, gate, credential or journey"
   }
  },
  "required": [
   "rfidNfcProfileId",
   "venueId",
   "name"
  ]
 },
 "VerificationMethodSelectionLockingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Verification Method Selection & Locking displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "availableMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dynamicQr",
      "physicalCard",
      "rfid",
      "facePass",
      "faceTag"
     ]
    },
    "description": "Verification methods the guest may choose from"
   },
   "reason": {
    "type": "string",
    "enum": [
     "lostPhone",
     "damagedWristband",
     "accessibility",
     "deviceFailure",
     "guestService",
     "other"
    ],
    "description": "Reason code vocabulary for a method change; every change is audited"
   },
   "policyId": {
    "type": "string",
    "description": "Verification method policy identifier"
   },
   "productId": {
    "type": "string",
    "description": "Product the policy applies to"
   },
   "lockOnFirstSuccessfulAccess": {
    "type": "boolean",
    "description": "The chosen method locks at the first successful access"
   },
   "changeAfterLock": {
    "type": "string",
    "enum": [
     "notAllowed",
     "supervisorApproval"
    ],
    "description": "Who may change the method once locked; guests may not"
   }
  }
 }
}
```
