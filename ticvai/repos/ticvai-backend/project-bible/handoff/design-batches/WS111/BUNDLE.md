# WS111 — ACCREDITATION board 4

**9 screens · 9 operations · 8 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `ACCREDITATION_CONFIGURE, ACCREDITATION_ISSUE, ACCREDITATION_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-644` | Credential Issuance Command Center | listDetail | 1 | 0 | — |
| `BO-645` | Credential Generation Workspace | listDetail | 1 | 0 | — |
| `BO-646` | Credential Media Configuration | listDetail | 1 | 0 | — |
| `BO-647` | Badge Template Designer | listDetail | 1 | 0 | — |
| `BO-648` | Badge Printing & Print Queue | listDetail | 2 | 0 | — |
| `BO-649` | Digital & Mobile Credential Management | listDetail | 3 | 0 | — |
| `BO-650` | NFC & RFID Credential Encoding | listDetail | 1 | 0 | — |
| `BO-651` | Credential Activation & Delivery | listDetail | 2 | 0 | — |
| `BO-653` | Credential Registry & Credential History | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-644, BO-645, BO-646, BO-647, BO-648, BO-649, BO-650, BO-651, BO-653 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-644",
  "name": "Credential Issuance Command Center",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "4",
   "number": "1",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-issuance-command-center-bo-644",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialIssuanceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-645",
    "BO-646",
    "BO-647",
    "BO-648",
    "BO-649",
    "BO-650",
    "BO-651",
    "BO-027",
    "BO-653"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-645",
     "trigger": "Credential Generation Workspace",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-646",
     "trigger": "Credential Media Configuration",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-647",
     "trigger": "Badge Template Designer",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-648",
     "trigger": "Badge Printing & Print Queue",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-649",
     "trigger": "Digital & Mobile Credential Management",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-650",
     "trigger": "NFC & RFID Credential Encoding",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-651",
     "trigger": "Credential Activation & Delivery",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-027",
     "trigger": "Credential Replacement & Reissue (BO-027, absorbed BO-652, audit R276)",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-653",
     "trigger": "Credential Registry & Credential History",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Central operational dashboard for accreditation credential issuance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 28"
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
       "impliedBy": "listCredentialGenerationIssuance",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential issuance list.",
   "error": "Could not load. Names which read failed and leaves the credential issuance untouched.",
   "emptyFirstRun": "No credential issuance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential issuance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialGenerationIssuance",
    "contract": "access",
    "purpose": "Credential Generation & Issuance Monitor",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-644",
   "workshopBoard": "wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-644"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-645",
  "name": "Credential Generation Workspace",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "4",
   "number": "2",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-generation-workspace-bo-645",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialGenerationWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-644"
   ],
   "exitTo": [
    "BO-644"
   ],
   "transitions": [
    {
     "to": "BO-644",
     "trigger": "Back to Credential Issuance Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert an approved accreditation into an operational credential.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 29"
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
       "label": "Key requirement: 12.1.4",
       "provenance": "pack ACCREDITATION.pdf, page 29 §Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAccreditationCredentials",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential generation list.",
   "error": "Could not load. Names which read failed and leaves the credential generation untouched.",
   "emptyFirstRun": "No credential generation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential generation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationCredentials",
    "contract": "accreditation",
    "purpose": "Credentials issued",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-645",
   "workshopBoard": "wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-645"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 29. 0 of 0 labels bound to a contract property; 1 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Key requirement: 12.1.4 are choices sent by `listAccreditationCredentials` (requirement reference shown on the workspace).",
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
  "id": "BO-646",
  "name": "Credential Media Configuration",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "4",
   "number": "3",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-media-configuration-bo-646",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialMediaConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-644"
   ],
   "exitTo": [
    "BO-644"
   ],
   "transitions": [
    {
     "to": "BO-644",
     "trigger": "Back to Credential Issuance Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the credential technologies available for each accreditation program.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 30"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "issueAccreditationCredential",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "issueAccreditationCredential"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential media list.",
   "error": "Could not load. Names which read failed and leaves the credential media untouched.",
   "emptyFirstRun": "No credential media yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential media are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "issueAccreditationCredential",
    "contract": "accreditation",
    "purpose": "Generate a credential",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationCredentials"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-646",
   "workshopBoard": "wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-646"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-647",
  "name": "Badge Template Designer",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "4",
   "number": "4",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/badge-template-designer-bo-647",
   "component": "apps/venue-management-web/src/routes/access-venue/BadgeTemplateDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-644"
   ],
   "exitTo": [
    "BO-644"
   ],
   "transitions": [
    {
     "to": "BO-644",
     "trigger": "Back to Credential Issuance Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Design physical accreditation badges.",
  "gaps": [
   {
    "operation": null,
    "why": "**Badge Template Designer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 30"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setBadgeTemplate",
       "label": "Save badge template",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setBadgeTemplate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The badge template designer list.",
   "error": "Could not load. Names which read failed and leaves the badge template designer untouched.",
   "emptyFirstRun": "No badge template designer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the badge template designer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setBadgeTemplate",
    "contract": "accreditation",
    "purpose": "Credential media",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listBadgeTemplates"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-647",
   "workshopBoard": "wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-647"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-648",
  "name": "Badge Printing & Print Queue",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "4",
   "number": "5",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/badge-printing-print-queue-bo-648",
   "component": "apps/venue-management-web/src/routes/access-venue/BadgePrintingPrintQueue.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-644"
   ],
   "exitTo": [
    "BO-644"
   ],
   "transitions": [
    {
     "to": "BO-644",
     "trigger": "Back to Credential Issuance Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage physical accreditation badge production.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 31"
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
       "impliedBy": "listBadgeTemplates",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setBadgeTemplate",
       "label": "Save badge template",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setBadgeTemplate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The badge printing print list.",
   "error": "Could not load. Names which read failed and leaves the badge printing print untouched.",
   "emptyFirstRun": "No badge printing print yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the badge printing print are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBadgeTemplates",
    "contract": "accreditation",
    "purpose": "Badge designs",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setBadgeTemplate",
    "contract": "accreditation",
    "purpose": "Design one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listBadgeTemplates"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-648",
   "workshopBoard": "wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-648"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-649",
  "name": "Digital & Mobile Credential Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "4",
   "number": "6",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/digital-mobile-credential-management-bo-649",
   "component": "apps/venue-management-web/src/routes/access-venue/DigitalMobileCredentialManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-644"
   ],
   "exitTo": [
    "BO-644"
   ],
   "transitions": [
    {
     "to": "BO-644",
     "trigger": "Back to Credential Issuance Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage credentials delivered electronically to accreditation holders.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 32"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createBadgePrintJob",
       "label": "Create badge print job",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listBadgePrintJobs",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createBadgePrintJob"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital mobile credential list.",
   "error": "Could not load. Names which read failed and leaves the digital mobile credential untouched.",
   "emptyFirstRun": "No digital mobile credential yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital mobile credential are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createBadgePrintJob",
    "contract": "accreditation",
    "purpose": "Queue for printing",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listBadgePrintJobs"
    ]
   },
   {
    "operationId": "listBadgePrintJobs",
    "contract": "accreditation",
    "purpose": "The print queue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "deliverAccreditationCredential",
    "contract": "accreditation",
    "purpose": "Send a mobile credential to its holder",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-649",
   "workshopBoard": "wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-649"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "credentialId",
     "from": "navigation"
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
  "id": "BO-650",
  "name": "NFC & RFID Credential Encoding",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "4",
   "number": "7",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/nfc-rfid-credential-encoding-bo-650",
   "component": "apps/venue-management-web/src/routes/access-venue/NfcRfidCredentialEncoding.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-644"
   ],
   "exitTo": [
    "BO-644"
   ],
   "transitions": [
    {
     "to": "BO-644",
     "trigger": "Back to Credential Issuance Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Associate physical NFC/RFID media with an accreditation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 33"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "issueAccreditationCredential",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "issueAccreditationCredential"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The nfc rfid credential list.",
   "error": "Could not load. Names which read failed and leaves the nfc rfid credential untouched.",
   "emptyFirstRun": "No nfc rfid credential yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the nfc rfid credential are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "issueAccreditationCredential",
    "contract": "accreditation",
    "purpose": "Digital and mobile credentials",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationCredentials"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-650",
   "workshopBoard": "wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-650"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-651",
  "name": "Credential Activation & Delivery",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "4",
   "number": "8",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-activation-delivery-bo-651",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialActivationDelivery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-644"
   ],
   "exitTo": [
    "BO-644"
   ],
   "transitions": [
    {
     "to": "BO-644",
     "trigger": "Back to Credential Issuance Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control when an issued credential becomes operational.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 33"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "issueAccreditationCredential",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "issueAccreditationCredential"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential activation delivery list.",
   "error": "Could not load. Names which read failed and leaves the credential activation delivery untouched.",
   "emptyFirstRun": "No credential activation delivery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential activation delivery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "issueAccreditationCredential",
    "contract": "accreditation",
    "purpose": "NFC and RFID encoding",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationCredentials"
    ]
   },
   {
    "operationId": "deliverAccreditationCredential",
    "contract": "accreditation",
    "purpose": "Deliver, and optionally activate on open",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-651",
   "workshopBoard": "wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-651"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "credentialId",
     "from": "navigation"
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
  "id": "BO-653",
  "name": "Credential Registry & Credential History",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "4",
   "number": "10",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-registry-credential-history-bo-653",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialRegistryCredentialHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-644"
   ],
   "exitTo": [
    "BO-644"
   ],
   "transitions": [
    {
     "to": "BO-644",
     "trigger": "Back to Credential Issuance Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain the authoritative record of every credential issued by TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 34"
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
       "impliedBy": "listCredential",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential registry credential list.",
   "error": "Could not load. Names which read failed and leaves the credential registry credential untouched.",
   "emptyFirstRun": "No credential registry credential yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential registry credential are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredential",
    "contract": "access",
    "purpose": "Credential Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-653",
   "workshopBoard": "wireframes/WS04 ACCREDITATION Board 4.dc.html#bo-653"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createBadgePrintJob": {
  "method": "POST",
  "path": "/badge-print-jobs",
  "contract": "accreditation",
  "summary": "Queue badges for printing",
  "permission": "ACCREDITATION_ISSUE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "BadgePrintJob",
  "responds": "BadgePrintJob"
 },
 "deliverAccreditationCredential": {
  "method": "POST",
  "path": "/accreditation-credentials/{credentialId}/deliver",
  "contract": "accreditation",
  "summary": "Send a mobile credential to its holder",
  "permission": "ACCREDITATION_ISSUE",
  "offlineCapable": null,
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
  "responds": "AccreditationCredentialDelivery"
 },
 "issueAccreditationCredential": {
  "method": "POST",
  "path": "/accreditation-credentials",
  "contract": "accreditation",
  "summary": "Produce a badge, a mobile credential, or both",
  "permission": "ACCREDITATION_ISSUE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AccreditationCredential",
  "responds": "AccreditationCredential"
 },
 "listAccreditationCredentials": {
  "method": "GET",
  "path": "/accreditation-credentials",
  "contract": "accreditation",
  "summary": "Badges and digital credentials issued",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "holderId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationCredential"
 },
 "listBadgePrintJobs": {
  "method": "GET",
  "path": "/badge-print-jobs",
  "contract": "accreditation",
  "summary": "The print queue, and what failed",
  "permission": "ACCREDITATION_ISSUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BadgePrintJob"
 },
 "listBadgeTemplates": {
  "method": "GET",
  "path": "/badge-templates",
  "contract": "accreditation",
  "summary": "Badge designs, and what prints on each",
  "permission": "ACCREDITATION_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BadgeTemplate"
 },
 "listCredential": {
  "method": "GET",
  "path": "/credential",
  "contract": "access",
  "summary": "Credential Operations Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "media",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "customer",
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
    "name": "provider",
    "in": "query",
    "required": false
   },
   {
    "name": "exception",
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
 "listCredentialGenerationIssuance": {
  "method": "GET",
  "path": "/credential-generation-issuance",
  "contract": "access",
  "summary": "Credential Generation & Issuance Monitor",
  "permission": "SCOPE_VIEW",
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
    "name": "trigger",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
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
 "setBadgeTemplate": {
  "method": "PUT",
  "path": "/badge-templates",
  "contract": "accreditation",
  "summary": "Design a badge",
  "permission": "ACCREDITATION_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "BadgeTemplate",
  "responds": "BadgeTemplate"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccreditationCredential": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.credential",
  "description": "Board 4. **Not the accreditation** — reissuing one re-vets nobody.",
  "required": [
   "holderId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "holderId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "printedBadge",
     "mobileCredential",
     "qr",
     "nfcCard",
     "rfidCard",
     "wristband"
    ]
   },
   "symbology": {
    "type": "string",
    "nullable": true,
    "description": "12.1.22. **How `encodedIdentifier` is carried**, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a `mobileCredential`, a barcode where a printed badge carries one, `nfcNdef` or `rfidEpc` for an encoded card, `none` where nothing is encoded.\n",
    "enum": [
     "qr",
     "dataMatrix",
     "pdf417",
     "aztec",
     "code128",
     "nfcNdef",
     "rfidEpc",
     "none"
    ]
   },
   "serialNumber": {
    "type": "string",
    "nullable": true
   },
   "encodedIdentifier": {
    "type": "string",
    "nullable": true
   },
   "badgeTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "issuedBy": {
    "type": "string",
    "format": "uuid"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingPrint",
     "issued",
     "active",
     "lost",
     "replaced",
     "revoked",
     "expired"
    ]
   },
   "replacesCredentialId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "replacementCount": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationCredentialDelivery": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.mobile_credential_delivery",
  "description": "12.1.21. **Issuing a mobile credential and getting it onto a phone are two acts**, and the second is recorded so *\"I never got it\"* has an answer. Written by `deliverAccreditationCredential` (the accreditation team sends it) and `issueMyAccreditationWalletPass` (the holder adds it to a wallet).\n",
  "required": [
   "credentialId",
   "channel"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "credentialId": {
    "type": "string",
    "format": "uuid"
   },
   "holderId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "channel": {
    "type": "string",
    "enum": [
     "email",
     "sms",
     "holderApp",
     "appleWallet",
     "googleWallet"
    ]
   },
   "destinationMasked": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The address or number used, masked (`j***@agency.com`). Always the holder's own"
   },
   "walletPassSerial": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "walletPassUrl": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Signed and expiring; adds the pass to the wallet"
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "queued",
     "sent",
     "delivered",
     "opened",
     "failed",
     "superseded"
    ]
   },
   "failureReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "deliveredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "BadgePrintJob": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.print_job",
  "description": "Board 4.5. **Printing fails mid-batch and the operator needs to know which landed.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "credentialIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "printerDeviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "printing",
     "completed",
     "partiallyFailed",
     "failed"
    ]
   },
   "printed": {
    "type": "integer",
    "readOnly": true
   },
   "failed": {
    "type": "integer",
    "readOnly": true
   },
   "failures": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "credentialId": {
       "type": "string",
       "format": "uuid"
      },
      "reason": {
       "type": "string"
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "BadgeTemplate": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.badge_template",
  "description": "Board 4.4. **A security artefact as much as a printed card.**",
  "required": [
   "code"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "size": {
    "type": "string",
    "nullable": true
   },
   "showPhoto": {
    "type": "boolean",
    "default": true
   },
   "showZones": {
    "type": "boolean",
    "default": true
   },
   "colourStripe": {
    "type": "string",
    "nullable": true,
    "description": "**What a security officer checks at a glance.** The stripe is the control that works at ten metres in the dark.\n"
   },
   "showOrganisation": {
    "type": "boolean",
    "default": true
   },
   "showValidity": {
    "type": "boolean",
    "default": true
   },
   "backgroundAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "securityFeatures": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "CredentialGenerationIssuanceMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Generation & Issuance Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "trigger": {
    "type": "string",
    "enum": [
     "orderConfirmation",
     "ticketIssuance",
     "membershipActivation",
     "customerRequest",
     "staffAction",
     "rfidCollection",
     "walletRequest",
     "faceEnrollment",
     "api",
     "bulkOperation",
     "scheduledProcess"
    ],
    "description": "What triggered generation"
   },
   "requestId": {
    "type": "string",
    "description": "Request ID"
   },
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "template": {
    "type": "string",
    "description": "Template"
   },
   "templateVersion": {
    "type": "string",
    "description": "Template Version"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Requested At"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Generated At"
   },
   "status": {
    "type": "string",
    "enum": [
     "requested",
     "queued",
     "templateResolved",
     "dataMapped",
     "credentialGenerated",
     "bound",
     "ready",
     "delivered",
     "failed"
    ],
    "description": "Generation stage"
   },
   "error": {
    "type": "string",
    "description": "Error"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "customerContext": {
    "type": "string",
    "description": "Customer context"
   },
   "failureReason": {
    "type": "string",
    "enum": [
     "templateMissing",
     "requiredDataMissing",
     "providerUnavailable",
     "invalidPayload",
     "tokenGenerationFailure",
     "walletGenerationFailure",
     "encoderUnavailable"
    ],
    "description": "Failure category when status is failed"
   }
  }
 },
 "CredentialOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket ID"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential ID"
   },
   "mediaType": {
    "type": "string",
    "description": "Media Type"
   },
   "customerParticipant": {
    "type": "string",
    "description": "Customer / Participant"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "credentialStatus": {
    "type": "string",
    "enum": [
     "pendingGeneration",
     "generated",
     "pendingActivation",
     "active",
     "suspended",
     "revoked",
     "expired",
     "failed"
    ],
    "description": "Credential status"
   },
   "deliveryStatus": {
    "type": "string",
    "enum": [
     "notRequired",
     "pending",
     "sent",
     "delivered",
     "openedDownloaded",
     "completed",
     "failed",
     "bounced",
     "expired",
     "cancelled"
    ],
    "description": "Delivery status (15.3.4)"
   },
   "activationStatus": {
    "type": "string",
    "enum": [
     "pending",
     "scheduled",
     "active",
     "notRequired"
    ],
    "description": "Activation status"
   },
   "bindingStatus": {
    "type": "string",
    "enum": [
     "pending",
     "bound",
     "unbound",
     "failed"
    ],
    "description": "Binding status"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "lastActivity": {
    "type": "string",
    "format": "date-time",
    "description": "Last Activity"
   },
   "exception": {
    "type": "string",
    "description": "Exception"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   }
  }
 },
 "CredentialOperationsCommandCenterViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "virtualTicketsIssued": {
    "type": "integer",
    "description": "Virtual Tickets Issued"
   },
   "credentialsGenerated": {
    "type": "integer",
    "description": "Credentials Generated"
   },
   "activeCredentials": {
    "type": "integer",
    "description": "Active Credentials"
   },
   "pendingGeneration": {
    "type": "integer",
    "description": "Pending Generation"
   },
   "pendingDelivery": {
    "type": "integer",
    "description": "Pending Delivery"
   },
   "pendingBinding": {
    "type": "integer",
    "description": "Pending Binding"
   },
   "pendingActivation": {
    "type": "integer",
    "description": "Pending Activation"
   },
   "suspended": {
    "type": "integer",
    "description": "Suspended"
   },
   "revoked": {
    "type": "integer",
    "description": "Revoked"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "failedGeneration": {
    "type": "integer",
    "description": "Failed Generation"
   },
   "failedDelivery": {
    "type": "integer",
    "description": "Failed Delivery"
   },
   "synchronizationExceptions": {
    "type": "integer",
    "description": "Synchronization Exceptions"
   },
   "multiMediaVirtualTickets": {
    "type": "integer",
    "description": "Multi-Media Virtual Tickets"
   },
   "virtualTicketsWithoutActiveMedia": {
    "type": "integer",
    "description": "Virtual Tickets Without Active Media"
   },
   "dynamicQr": {
    "type": "integer",
    "description": "Credentials of this media type"
   },
   "barcode": {
    "type": "integer",
    "description": "Credentials of this media type"
   },
   "pdf": {
    "type": "integer",
    "description": "Credentials of this media type"
   },
   "appleWallet": {
    "type": "integer",
    "description": "Credentials of this media type"
   },
   "googleWallet": {
    "type": "integer",
    "description": "Credentials of this media type"
   },
   "rfid": {
    "type": "integer",
    "description": "Credentials of this media type"
   },
   "nfc": {
    "type": "integer",
    "description": "Credentials of this media type"
   },
   "faceRecognitionReference": {
    "type": "integer",
    "description": "Credentials of this media type"
   },
   "card": {
    "type": "integer",
    "description": "Credentials of this media type"
   },
   "wristband": {
    "type": "integer",
    "description": "Credentials of this media type"
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
