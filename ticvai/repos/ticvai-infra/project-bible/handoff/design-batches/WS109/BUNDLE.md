# WS109 — ACCREDITATION board 2

**10 screens · 8 operations · 4 schemas · 4 permissions**

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
  `ACCREDITATION_APPLY, ACCREDITATION_APPROVE, ACCREDITATION_MANAGE, ACCREDITATION_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-625` | Accreditation Holder Directory | listDetail | 1 | 0 | — |
| `BO-626` | Accreditation Holder Profile | listDetail | 1 | 0 | — |
| `BO-627` | Identity Details & Verification | listDetail | 1 | 0 | — |
| `BO-628` | Photo Management | listDetail | 1 | 0 | — |
| `BO-629` | Document Repository | listDetail | 1 | 0 | — |
| `BO-630` | Document Verification Queue | listDetail | 1 | 0 | — |
| `BO-631` | Duplicate & Identity Conflict Detection | listDetail | 2 | 1 | — |
| `BO-632` | Organization & Affiliation Management | listDetail | 1 | 0 | — |
| `BO-633` | Profile Completeness & Compliance Monitor | listDetail | 1 | 0 | — |
| `BO-634` | Profile History & Audit Timeline | configEditor | 1 | 0 | — |

## Thin screens in this batch

**BO-625, BO-626, BO-627, BO-628, BO-629, BO-630, BO-631, BO-632, BO-633 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-625",
  "name": "Accreditation Holder Directory",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "1",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-holder-directory-bo-625",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationHolderDirectory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-626",
    "BO-627",
    "BO-628",
    "BO-629",
    "BO-630",
    "BO-631",
    "BO-632",
    "BO-633",
    "BO-634"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-626",
     "trigger": "Accreditation Holder Profile",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-627",
     "trigger": "Identity Details & Verification",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-628",
     "trigger": "Photo Management",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-629",
     "trigger": "Document Repository",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-630",
     "trigger": "Document Verification Queue",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-631",
     "trigger": "Duplicate & Identity Conflict Detection",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-632",
     "trigger": "Organization & Affiliation Management",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-633",
     "trigger": "Profile Completeness & Compliance Monitor",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-634",
     "trigger": "Profile History & Audit Timeline",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each holder record shall display) and no metric row",
  "purpose": "Central searchable directory of all accreditation holders.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack ACCREDITATION.pdf, page 10 §Each holder record shall display"
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
       "label": "Every accreditation holder",
       "columns": [
        "Holder ID",
        "Profile photograph",
        "Full name",
        "Accreditation category",
        "Applicant type",
        "Organization/company",
        "Current accreditation status",
        "Identity verification status",
        "Active credentials",
        "Linked event/venue",
        "Expiry status",
        "Last updated date",
        "Name",
        "Email",
        "Mobile",
        "Passport/ID number where permitted",
        "Organization",
        "Accreditation ID",
        "Credential ID",
        "Category",
        "Event",
        "Venue",
        "Verification status",
        "Accreditation status",
        "Credential status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack ACCREDITATION.pdf, page 10 §Each holder record shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected accreditation holder",
       "bindsTo": null,
       "columns": [
        "Holder ID",
        "Profile photograph",
        "Full name",
        "Accreditation category",
        "Applicant type",
        "Organization/company",
        "Current accreditation status",
        "Identity verification status",
        "Active credentials",
        "Linked event/venue",
        "Expiry status",
        "Last updated date",
        "Name",
        "Email",
        "Mobile",
        "Passport/ID number where permitted",
        "Organization",
        "Accreditation ID",
        "Credential ID",
        "Category",
        "Event",
        "Venue",
        "Verification status",
        "Accreditation status",
        "Credential status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Scope of Work”.",
       "provenance": "pack ACCREDITATION.pdf, page 10 §Each holder record shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation holder list.",
   "error": "Could not load. Names which read failed and leaves the accreditation holder untouched.",
   "emptyFirstRun": "No accreditation holder yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation holder are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationHolders",
    "contract": "accreditation",
    "purpose": "The holder directory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Holder ID",
    "Profile photograph",
    "Full name",
    "Accreditation category",
    "Applicant type",
    "Organization/company"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-625",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-625"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 10. 0 of 25 labels bound to a contract property; 25 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-626",
  "name": "Accreditation Holder Profile",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "2",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-holder-profile-bo-626",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationHolderProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-625"
   ],
   "exitTo": [
    "BO-625"
   ],
   "transitions": [
    {
     "to": "BO-625",
     "trigger": "Back to Accreditation Holder Directory",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Master profile screen for an accredited person.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 11"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getAccreditationHolder",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation holder profile list.",
   "error": "Could not load. Names which read failed and leaves the accreditation holder profile untouched.",
   "emptyFirstRun": "No accreditation holder profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation holder profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAccreditationHolder",
    "contract": "accreditation",
    "purpose": "One holder",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-626",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-626"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "holderId",
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
  "id": "BO-627",
  "name": "Identity Details & Verification",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "3",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/identity-details-verification-bo-627",
   "component": "apps/venue-management-web/src/routes/access-venue/IdentityDetailsVerification.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-625"
   ],
   "exitTo": [
    "BO-625"
   ],
   "transitions": [
    {
     "to": "BO-625",
     "trigger": "Back to Accreditation Holder Directory",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Capture identity data and verify the holder before approval.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 12"
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
       "impliedBy": "updateAccreditationHolder",
       "label": "Save accreditation holder",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateAccreditationHolder"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The identity details verification list.",
   "error": "Could not load. Names which read failed and leaves the identity details verification untouched.",
   "emptyFirstRun": "No identity details verification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the identity details verification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateAccreditationHolder",
    "contract": "accreditation",
    "purpose": "Identity and verification",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccreditationHolder",
     "listAccreditationHolders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-627",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-627"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "holderId",
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
  "id": "BO-628",
  "name": "Photo Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "4",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/photo-management-bo-628",
   "component": "apps/venue-management-web/src/routes/access-venue/PhotoManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-625"
   ],
   "exitTo": [
    "BO-625"
   ],
   "transitions": [
    {
     "to": "BO-625",
     "trigger": "Back to Accreditation Holder Directory",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage accreditation holder photographs.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 13"
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
       "impliedBy": "updateAccreditationHolder",
       "label": "Save accreditation holder",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateAccreditationHolder"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The photo list.",
   "error": "Could not load. Names which read failed and leaves the photo untouched.",
   "emptyFirstRun": "No photo yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the photo are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateAccreditationHolder",
    "contract": "accreditation",
    "purpose": "Photo management",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccreditationHolder",
     "listAccreditationHolders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-628",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-628"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "holderId",
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
  "id": "BO-629",
  "name": "Document Repository",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "5",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/document-repository-bo-629",
   "component": "apps/venue-management-web/src/routes/access-venue/DocumentRepository.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-625"
   ],
   "exitTo": [
    "BO-625"
   ],
   "transitions": [
    {
     "to": "BO-625",
     "trigger": "Back to Accreditation Holder Directory",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Store and manage accreditation-related supporting documents.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 14"
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
       "impliedBy": "submitAccreditationDocument",
       "label": "Submit",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "submitAccreditationDocument"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The document repository list.",
   "error": "Could not load. Names which read failed and leaves the document repository untouched.",
   "emptyFirstRun": "No document repository yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the document repository are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "submitAccreditationDocument",
    "contract": "accreditation",
    "purpose": "The document repository",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccreditationHolder"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-629",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-629"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-630",
  "name": "Document Verification Queue",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "6",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/document-verification-queue-bo-630",
   "component": "apps/venue-management-web/src/routes/access-venue/DocumentVerificationQueue.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-625"
   ],
   "exitTo": [
    "BO-625"
   ],
   "transitions": [
    {
     "to": "BO-625",
     "trigger": "Back to Accreditation Holder Directory",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Operational review queue for uploaded accreditation documentation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 15"
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
       "impliedBy": "verifyAccreditationDocument",
       "label": "Verify",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "verifyAccreditationDocument"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The document verification queue list.",
   "error": "Could not load. Names which read failed and leaves the document verification queue untouched.",
   "emptyFirstRun": "No document verification queue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the document verification queue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "verifyAccreditationDocument",
    "contract": "accreditation",
    "purpose": "Verify a document",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccreditationHolder"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-630",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-630"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "documentId",
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
  "id": "BO-631",
  "name": "Duplicate & Identity Conflict Detection",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "7",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/duplicate-identity-conflict-detection-bo-631",
   "component": "apps/venue-management-web/src/routes/access-venue/DuplicateIdentityConflictDetection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-625"
   ],
   "exitTo": [
    "BO-625"
   ],
   "transitions": [
    {
     "to": "BO-625",
     "trigger": "Back to Accreditation Holder Directory",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Prevent duplicate holder records and potential identity conflicts.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 15"
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
       "impliedBy": "listAccreditationIdentityConflicts",
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
       "label": "Resolve identity conflict",
       "operation": "resolveIdentityConflict",
       "permission": "ACCREDITATION_MANAGE",
       "notes": "**Takes a suspected pair out of `pending`** (decided 29 September, writers pass).",
       "provenance": "contract accreditation.yaml POST /accreditation-identity-conflicts/{conflictId}/resolve"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The duplicate identity conflict list.",
   "error": "Could not load. Names which read failed and leaves the duplicate identity conflict untouched.",
   "emptyFirstRun": "No duplicate identity conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the duplicate identity conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationIdentityConflicts",
    "contract": "accreditation",
    "purpose": "Possible duplicates",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "resolveIdentityConflict",
    "contract": "accreditation",
    "purpose": "Decide whether two accreditation records are the same person",
    "trigger": "onAction",
    "invalidates": [
     "listAccreditationIdentityConflicts"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-631",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-631"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formResolveIdentityConflict",
    "component": "modal",
    "trigger": "Resolve identity conflict",
    "body": "**Collects what `resolveIdentityConflict` sends before it is called.** Required: `outcome`, `reason`. Optional: `survivingHolderId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resolve identity conflict",
     "operation": "resolveIdentityConflict"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outcome",
      "reason",
      "survivingHolderId"
     ]
    },
    "provenance": "contract accreditation.yaml POST /accreditation-identity-conflicts/{conflictId}/resolve"
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
  "id": "BO-632",
  "name": "Organization & Affiliation Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "8",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/organization-affiliation-management-bo-632",
   "component": "apps/venue-management-web/src/routes/access-venue/OrganizationAffiliationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-625"
   ],
   "exitTo": [
    "BO-625"
   ],
   "transitions": [
    {
     "to": "BO-625",
     "trigger": "Back to Accreditation Holder Directory",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Link holders to their employer, contractor, media organization, government authority or sponsor.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 16"
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
       "impliedBy": "updateAccreditationHolder",
       "label": "Save accreditation holder",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateAccreditationHolder"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The organization affiliation list.",
   "error": "Could not load. Names which read failed and leaves the organization affiliation untouched.",
   "emptyFirstRun": "No organization affiliation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the organization affiliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateAccreditationHolder",
    "contract": "accreditation",
    "purpose": "Organisation and affiliation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccreditationHolder",
     "listAccreditationHolders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-632",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-632"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "holderId",
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
  "id": "BO-633",
  "name": "Profile Completeness & Compliance Monitor",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "9",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/profile-completeness-compliance-monitor-bo-633",
   "component": "apps/venue-management-web/src/routes/access-venue/ProfileCompletenessComplianceMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-625"
   ],
   "exitTo": [
    "BO-625"
   ],
   "transitions": [
    {
     "to": "BO-625",
     "trigger": "Back to Accreditation Holder Directory",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show whether a holder profile is ready to proceed to accreditation approval.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 17"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getAccreditationHolder",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The profile completeness compliance list.",
   "error": "Could not load. Names which read failed and leaves the profile completeness compliance untouched.",
   "emptyFirstRun": "No profile completeness compliance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the profile completeness compliance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAccreditationHolder",
    "contract": "accreditation",
    "purpose": "Completeness and compliance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-633",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-633"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 17. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "holderId",
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
  "id": "BO-634",
  "name": "Profile History & Audit Timeline",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "2",
   "number": "10",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/profile-history-audit-timeline-bo-634",
   "component": "apps/venue-management-web/src/routes/access-venue/ProfileHistoryAuditTimeline.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-625"
   ],
   "exitTo": [
    "BO-625"
   ],
   "transitions": [
    {
     "to": "BO-625",
     "trigger": "Back to Accreditation Holder Directory",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each audit event shall capture) and no display directory — it is settings, not a population",
  "purpose": "Provide a complete historical record of holder profile changes.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack ACCREDITATION.pdf, page 17 §Each audit event shall capture"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack ACCREDITATION.pdf, page 17 §Each audit event shall capture"
      },
      {
       "kind": "selectField",
       "label": "Action",
       "provenance": "pack ACCREDITATION.pdf, page 17 §Each audit event shall capture"
      },
      {
       "kind": "selectField",
       "label": "Previous value",
       "provenance": "pack ACCREDITATION.pdf, page 17 §Each audit event shall capture"
      },
      {
       "kind": "selectField",
       "label": "New value",
       "provenance": "pack ACCREDITATION.pdf, page 17 §Each audit event shall capture"
      },
      {
       "kind": "selectField",
       "label": "Source/channel",
       "provenance": "pack ACCREDITATION.pdf, page 17 §Each audit event shall capture"
      },
      {
       "kind": "textField",
       "label": "Related accreditation or event",
       "provenance": "pack ACCREDITATION.pdf, page 17 §Each audit event shall capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The profile history audit configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the profile history audit untouched.",
   "emptyFirstRun": "No profile history audit configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listAccreditationAudit",
    "contract": "accreditation",
    "purpose": "Profile history",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-634",
   "workshopBoard": "wireframes/WS02 ACCREDITATION Board 2.dc.html#bo-634"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 17. 0 of 0 labels bound to a contract property; 7 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getAccreditationHolder": {
  "method": "GET",
  "path": "/accreditation-holders/{holderId}",
  "contract": "accreditation",
  "summary": "One holder — identity, documents, access and history",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccreditationHolder"
 },
 "listAccreditationAudit": {
  "method": "GET",
  "path": "/accreditation-audit",
  "contract": "accreditation",
  "summary": "The immutable record of who granted what to whom",
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
    "name": "from",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationAuditRecord"
 },
 "listAccreditationHolders": {
  "method": "GET",
  "path": "/accreditation-holders",
  "contract": "accreditation",
  "summary": "Everybody accredited, and what state they are in",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "programmeId",
    "in": "query",
    "required": null
   },
   {
    "name": "organisationId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "expiringWithinDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationHolder"
 },
 "listAccreditationIdentityConflicts": {
  "method": "GET",
  "path": "/accreditation-identity-conflicts",
  "contract": "accreditation",
  "summary": "People who may already be accredited under another record",
  "permission": "ACCREDITATION_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccreditationIdentityConflict"
 },
 "resolveIdentityConflict": {
  "method": "POST",
  "path": "/accreditation-identity-conflicts/{conflictId}/resolve",
  "contract": "accreditation",
  "summary": "Decide whether two accreditation records are the same person",
  "permission": "ACCREDITATION_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationIdentityConflict"
 },
 "submitAccreditationDocument": {
  "method": "POST",
  "path": "/accreditation-documents",
  "contract": "accreditation",
  "summary": "Supply a document against a requirement",
  "permission": "ACCREDITATION_APPLY",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AccreditationDocument",
  "responds": "AccreditationDocument"
 },
 "updateAccreditationHolder": {
  "method": "PUT",
  "path": "/accreditation-holders/{holderId}",
  "contract": "accreditation",
  "summary": "Amend identity, affiliation or contact details",
  "permission": "ACCREDITATION_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AccreditationHolder",
  "responds": "AccreditationHolder"
 },
 "verifyAccreditationDocument": {
  "method": "POST",
  "path": "/accreditation-documents/{documentId}/verify",
  "contract": "accreditation",
  "summary": "Accept or refuse a submitted document",
  "permission": "ACCREDITATION_APPROVE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationDocument"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccreditationAuditRecord": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.audit",
  "description": "Board 8.7. **Who gave this person access to that place, when, and on whose authority.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "holderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "action": {
    "type": "string"
   },
   "actorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "previousValue": {
    "nullable": true
   },
   "newValue": {
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "previousRecordHash": {
    "type": "string",
    "nullable": true
   },
   "recordHash": {
    "type": "string"
   },
   "integrity": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "intact",
     "broken",
     "unverifiable"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationDocument": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.document",
  "description": "Board 2.5. **Submitted against a named requirement, not into a folder.**",
  "required": [
   "requirementCode",
   "assetId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "holderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "applicationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "requirementCode": {
    "type": "string"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "submitted",
     "verified",
     "rejected",
     "expired"
    ]
   },
   "verifiedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "verifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "rejectionReason": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "**An insurance certificate valid until March accredits somebody until March**, whatever the programme says.\n"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationHolder": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.holder",
  "description": "**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n",
  "required": [
   "id",
   "fullName"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accreditationNumber": {
    "type": "string"
   },
   "fullName": {
    "type": "string"
   },
   "photoAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "nationality": {
    "type": "string",
    "nullable": true
   },
   "identityDocumentVerified": {
    "type": "boolean",
    "default": false
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "affiliationRole": {
    "type": "string",
    "nullable": true
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked",
     "expired",
     "archived"
    ]
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "completenessPercent": {
    "type": "integer",
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationIdentityConflict": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.identity_conflict",
  "description": "Board 2.7. **One badge revoked and the other still opening doors.**\n\n**Stored, not recomputed on each read** (data model for the agreed operations, 29 September): a suspected pair is raised by `createAccreditationApplication` and `importAccreditationHolders` using `marketing-crm`'s identity resolution, and keeps its id and status while somebody decides it, so a pair rejected as two different people is not raised again on the next import. Resolved by `resolveIdentityConflict` (`pending` to `merged` or `rejected`, decided 29 September, writers pass); lifecycle in `states/accreditation-identity-conflict.yaml`.",
  "required": [
   "id",
   "holderIds",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "holderIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "score": {
    "type": "number"
   },
   "matchedOn": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "differingAccess": {
    "type": "boolean"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "merged",
     "rejected"
    ]
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "survivingHolderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The holder kept when the conflict was merged"
   },
   "resolutionReason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "readOnly": true
   },
   "resolvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
