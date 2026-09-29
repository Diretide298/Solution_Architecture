# WS108 — ACCREDITATION board 1

**10 screens · 7 operations · 6 schemas · 4 permissions**

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
  `ACCREDITATION_APPLY, ACCREDITATION_CONFIGURE, ACCREDITATION_VIEW, MARKETING_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-615` | Accreditation Command Center | listDetail | 2 | 0 | — |
| `BO-616` | Accreditation Application Directory | listDetail | 1 | 0 | — |
| `BO-617` | New Accreditation Application | listDetail | 1 | 0 | — |
| `BO-618` | Accreditation Form Builder | configEditor | 1 | 0 | — |
| `BO-619` | Accreditation Category Management | listDetail | 1 | 0 | — |
| `BO-620` | Accreditation Program Setup | listDetail | 1 | 0 | — |
| `BO-621` | Applicant Type Configuration | listDetail | 1 | 0 | — |
| `BO-622` | Application Requirements Matrix | listDetail | 1 | 0 | — |
| `BO-623` | Accreditation Intake Monitor | listDetail | 1 | 0 | — |
| `BO-624` | Registration Rules & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-615, BO-616, BO-617, BO-618, BO-619, BO-620, BO-621, BO-622, BO-623, BO-624 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-615",
  "name": "Accreditation Command Center",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "1",
   "page": 3
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-command-center-bo-615",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-616",
    "BO-617",
    "BO-618",
    "BO-619",
    "BO-620",
    "BO-621",
    "BO-622",
    "BO-623",
    "BO-624"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-616",
     "trigger": "Accreditation Application Directory",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-617",
     "trigger": "New Accreditation Application",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-618",
     "trigger": "Accreditation Form Builder",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-619",
     "trigger": "Accreditation Category Management",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-620",
     "trigger": "Accreditation Program Setup",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-621",
     "trigger": "Applicant Type Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-622",
     "trigger": "Application Requirements Matrix",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-623",
     "trigger": "Accreditation Intake Monitor",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-624",
     "trigger": "Registration Rules & Publication",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Executive and operational landing screen for the accreditation module.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 3"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 3"
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
       "impliedBy": "listAccreditationApplications",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation list.",
   "error": "Could not load. Names which read failed and leaves the accreditation untouched.",
   "emptyFirstRun": "No accreditation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationApplications",
    "contract": "accreditation",
    "purpose": "Applications in flight",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAccreditationHolders",
    "contract": "accreditation",
    "purpose": "Holders by status",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-615",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-615"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 3. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-616",
  "name": "Accreditation Application Directory",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "2",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-application-directory-bo-616",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationApplicationDirectory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-615"
   ],
   "exitTo": [
    "BO-615"
   ],
   "transitions": [
    {
     "to": "BO-615",
     "trigger": "Back to Accreditation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each application record shall display) and no metric row",
  "purpose": "Central repository of all accreditation applications.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack ACCREDITATION.pdf, page 4 §Each application record shall display"
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
       "label": "Every accreditation application",
       "columns": [
        "Application ID",
        "Applicant name",
        "Photograph",
        "Accreditation category",
        "Organization/company",
        "Event",
        "Venue",
        "Submission date",
        "Current status",
        "Assigned reviewer",
        "Credential status",
        "Expiry date"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack ACCREDITATION.pdf, page 4 §Each application record shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected accreditation application",
       "bindsTo": null,
       "columns": [
        "Application ID",
        "Applicant name",
        "Photograph",
        "Accreditation category",
        "Organization/company",
        "Event",
        "Venue",
        "Submission date",
        "Current status",
        "Assigned reviewer",
        "Credential status",
        "Expiry date"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Scope of Work”.",
       "provenance": "pack ACCREDITATION.pdf, page 4 §Each application record shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation application list.",
   "error": "Could not load. Names which read failed and leaves the accreditation application untouched.",
   "emptyFirstRun": "No accreditation application yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation application are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationApplications",
    "contract": "accreditation",
    "purpose": "The directory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Application ID",
    "Applicant name",
    "Photograph",
    "Accreditation category",
    "Organization/company",
    "Event"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-616",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-616"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 4. 0 of 12 labels bound to a contract property; 12 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-617",
  "name": "New Accreditation Application",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "3",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/new-accreditation-application-bo-617",
   "component": "apps/venue-management-web/src/routes/access-venue/NewAccreditationApplication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-615"
   ],
   "exitTo": [
    "BO-615"
   ],
   "transitions": [
    {
     "to": "BO-615",
     "trigger": "Back to Accreditation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized backend personnel to manually create accreditation applications.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 5"
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
       "impliedBy": "createAccreditationApplication",
       "label": "Create",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAccreditationApplication"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The new accreditation application list.",
   "error": "Could not load. Names which read failed and leaves the new accreditation application untouched.",
   "emptyFirstRun": "No new accreditation application yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the new accreditation application are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createAccreditationApplication",
    "contract": "accreditation",
    "purpose": "Start an application",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationApplications"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-617",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-617"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-618",
  "name": "Accreditation Form Builder",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "4",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-form-builder-bo-618",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationFormBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-615"
   ],
   "exitTo": [
    "BO-615"
   ],
   "transitions": [
    {
     "to": "BO-615",
     "trigger": "Back to Accreditation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Fields may be configured as) and no display directory — it is settings, not a population",
  "purpose": "Configure applicant-facing registration forms without software development.",
  "gaps": [
   {
    "operation": null,
    "why": "**Accreditation Form Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Mandatory / Optional / Conditional / Hidden",
       "provenance": "pack ACCREDITATION.pdf, page 5 §Fields may be configured as"
      },
      {
       "kind": "selectField",
       "label": "Key requirement: 12.1.2",
       "provenance": "pack ACCREDITATION.pdf, page 5 §Fields may be configured as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation form configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the accreditation form untouched.",
   "emptyFirstRun": "No accreditation form configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createForm",
    "contract": "marketing-crm",
    "purpose": "Build the application form",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-618",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-618"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 5. 0 of 0 labels bound to a contract property; 2 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-619",
  "name": "Accreditation Category Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "5",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-category-management-bo-619",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationCategoryManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-615"
   ],
   "exitTo": [
    "BO-615"
   ],
   "transitions": [
    {
     "to": "BO-615",
     "trigger": "Back to Accreditation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure reusable accreditation categories.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 6"
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
       "impliedBy": "listAccreditationProgrammes",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation category list.",
   "error": "Could not load. Names which read failed and leaves the accreditation category untouched.",
   "emptyFirstRun": "No accreditation category yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation category are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationProgrammes",
    "contract": "accreditation",
    "purpose": "Categories within a programme",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-619",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-619"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-620",
  "name": "Accreditation Program Setup",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "6",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-program-setup-bo-620",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationProgramSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-615"
   ],
   "exitTo": [
    "BO-615"
   ],
   "transitions": [
    {
     "to": "BO-615",
     "trigger": "Back to Accreditation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create the accreditation program governing a particular event, venue, season or organization.",
  "gaps": [
   {
    "operation": null,
    "why": "**Accreditation Program Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 7"
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
       "impliedBy": "createAccreditationProgramme",
       "label": "Create",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAccreditationProgramme"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation program list.",
   "error": "Could not load. Names which read failed and leaves the accreditation program untouched.",
   "emptyFirstRun": "No accreditation program yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation program are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createAccreditationProgramme",
    "contract": "accreditation",
    "purpose": "Set up a programme",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationProgrammes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-620",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-620"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-621",
  "name": "Applicant Type Configuration",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "7",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/applicant-type-configuration-bo-621",
   "component": "apps/venue-management-web/src/routes/access-venue/ApplicantTypeConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-615"
   ],
   "exitTo": [
    "BO-615"
   ],
   "transitions": [
    {
     "to": "BO-615",
     "trigger": "Back to Accreditation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure operational rules according to the type of person being accredited. Rather than building completely separate systems for staff, contractors, media, VIPs, etc., TICVAI should provide one accreditation engine with configurable applicant types. For each type, administrators shall define: Mandatory information Required documents Identity verification requirement Sponsor requirement Organization requirement Approval path Default validity Credential type Default access rules Renewal eligibility This architecture significantly reduces duplicated configuration.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 7"
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
       "impliedBy": "setAccreditationRequirements",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccreditationRequirements"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The applicant type list.",
   "error": "Could not load. Names which read failed and leaves the applicant type untouched.",
   "emptyFirstRun": "No applicant type yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the applicant type are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccreditationRequirements",
    "contract": "accreditation",
    "purpose": "Applicant types",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationProgrammes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-621",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-621"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-622",
  "name": "Application Requirements Matrix",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "8",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/application-requirements-matrix-bo-622",
   "component": "apps/venue-management-web/src/routes/access-venue/ApplicationRequirementsMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-615"
   ],
   "exitTo": [
    "BO-615"
   ],
   "transitions": [
    {
     "to": "BO-615",
     "trigger": "Back to Accreditation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure what an applicant must provide before an application can progress. The system shall allow administrators to configure requirements by: Program × Category × Applicant Type",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 8"
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
       "impliedBy": "setAccreditationRequirements",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccreditationRequirements"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The application requirements list.",
   "error": "Could not load. Names which read failed and leaves the application requirements untouched.",
   "emptyFirstRun": "No application requirements yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the application requirements are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccreditationRequirements",
    "contract": "accreditation",
    "purpose": "The requirements matrix",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationProgrammes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-622",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-622"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-623",
  "name": "Accreditation Intake Monitor",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "9",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-intake-monitor-bo-623",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationIntakeMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-615"
   ],
   "exitTo": [
    "BO-615"
   ],
   "transitions": [
    {
     "to": "BO-615",
     "trigger": "Back to Accreditation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§The screen shall show) and no metric row",
  "purpose": "Give operations teams visibility into incoming accreditation demand.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack ACCREDITATION.pdf, page 8 §The screen shall show"
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
       "label": "Every accreditation intake",
       "columns": [
        "Applications today",
        "Applications this week",
        "Application volumes by category",
        "Application volumes by organization",
        "Incomplete applications",
        "Applications awaiting documents",
        "Duplicate candidates",
        "Applications requiring review",
        "SLA ageing"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack ACCREDITATION.pdf, page 8 §The screen shall show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected accreditation intake",
       "bindsTo": null,
       "columns": [
        "Applications today",
        "Applications this week",
        "Application volumes by category",
        "Application volumes by organization",
        "Incomplete applications",
        "Applications awaiting documents",
        "Duplicate candidates",
        "Applications requiring review",
        "SLA ageing"
       ],
       "notes": null,
       "provenance": "pack ACCREDITATION.pdf, page 8 §The screen shall show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation intake list.",
   "error": "Could not load. Names which read failed and leaves the accreditation intake untouched.",
   "emptyFirstRun": "No accreditation intake yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation intake are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationApplications",
    "contract": "accreditation",
    "purpose": "Intake monitor",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Applications today",
    "Applications this week",
    "Application volumes by category",
    "Application volumes by organization",
    "Incomplete applications",
    "Applications awaiting documents"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-623",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-623"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 8. 0 of 9 labels bound to a contract property; 9 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-624",
  "name": "Registration Rules & Publication",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "1",
   "number": "10",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/registration-rules-publication-bo-624",
   "component": "apps/venue-management-web/src/routes/access-venue/RegistrationRulesPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-615"
   ],
   "exitTo": [
    "BO-615"
   ],
   "transitions": [
    {
     "to": "BO-615",
     "trigger": "Back to Accreditation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Final governance screen before opening an accreditation program for applications. The system shall provide a validation checklist covering: Registration form configured Categories configured Required documents configured Approval workflow assigned Credential template assigned Validity rules configured Access profile assigned Notification templates configured Application period configured Provide a complete operational workspace to create, review, verify, maintain and audit accreditation holder profiles before any credential is approved or issued. This board shall manage the individual’s identity, organization relationship, photographs, documents, verification status, duplicate detection, profile history and compliance readiness. The accreditation holder profile shall act as the single source of truth for the person across accreditation programs, events and venues.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 9"
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
       "impliedBy": "createAccreditationProgramme",
       "label": "Create",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAccreditationProgramme"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The registration rules publication list.",
   "error": "Could not load. Names which read failed and leaves the registration rules publication untouched.",
   "emptyFirstRun": "No registration rules publication yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the registration rules publication are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createAccreditationProgramme",
    "contract": "accreditation",
    "purpose": "Publish the rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationProgrammes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-624",
   "workshopBoard": "wireframes/WS01 ACCREDITATION Board 1.dc.html#bo-624"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createAccreditationApplication": {
  "method": "POST",
  "path": "/accreditation-applications",
  "contract": "accreditation",
  "summary": "Apply, or apply on behalf of somebody",
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
  "requestBody": "AccreditationApplication",
  "responds": "AccreditationApplication"
 },
 "createAccreditationProgramme": {
  "method": "POST",
  "path": "/accreditation-programmes",
  "contract": "accreditation",
  "summary": "Define a programme, its categories and its window",
  "permission": "ACCREDITATION_CONFIGURE",
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
  "requestBody": "AccreditationProgramme",
  "responds": "AccreditationProgramme"
 },
 "createForm": {
  "method": "POST",
  "path": "/forms",
  "contract": "marketing-crm",
  "summary": "Define a waiver, survey or capture form",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "FormDefinition",
  "responds": "FormDefinition"
 },
 "listAccreditationApplications": {
  "method": "GET",
  "path": "/accreditation-applications",
  "contract": "accreditation",
  "summary": "Applications, by state and programme",
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
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "applicantType",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationApplication"
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
 "listAccreditationProgrammes": {
  "method": "GET",
  "path": "/accreditation-programmes",
  "contract": "accreditation",
  "summary": "Programmes, their categories and their applicant types",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccreditationProgramme"
 },
 "setAccreditationRequirements": {
  "method": "PUT",
  "path": "/accreditation-requirements",
  "contract": "accreditation",
  "summary": "What each applicant type must supply and pass",
  "permission": "ACCREDITATION_CONFIGURE",
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
  "requestBody": "AccreditationRequirements",
  "responds": "AccreditationRequirements"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccreditationApplication": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.application",
  "description": "Board 1.3. **Usually submitted by an organisation on behalf of its people.**",
  "required": [
   "programmeId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "reference": {
    "type": "string"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "applicantType": {
    "type": "string"
   },
   "submittedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subject": {
    "type": "object",
    "additionalProperties": true,
    "description": "Name, date of birth, nationality, contact — shaped by the requirements matrix."
   },
   "requirementStatus": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "properties": {
      "requirementCode": {
       "type": "string"
      },
      "satisfied": {
       "type": "boolean"
      },
      "documentId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "submitted",
     "underReview",
     "informationRequested",
     "approved",
     "rejected",
     "withdrawn",
     "expired"
    ]
   },
   "decisionReason": {
    "type": "string",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "AccreditationProgramme": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.programme",
  "description": "Boards 1.5 and 1.6. **The thing an application is made against.**",
  "required": [
   "code",
   "name"
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
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "eventIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "categories": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "defaultAccessProfileId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "quota": {
       "type": "integer",
       "nullable": true,
       "description": "**A cap on how many may be accredited in this category.** Without one, a category is a promise nobody counted.\n"
      }
     }
    }
   },
   "applicantTypes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "applicationsOpenAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "applicationsCloseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "approvalWorkflowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "open",
     "closed",
     "archived"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationRequirements": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.requirements",
  "description": "Board 1.8. **Blocking submission and blocking approval are not the same.**",
  "properties": {
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "applicantType": {
       "type": "string"
      },
      "categoryCode": {
       "type": "string",
       "nullable": true
      },
      "requirementCode": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "kind": {
       "type": "string",
       "enum": [
        "document",
        "field",
        "photo",
        "backgroundCheck",
        "training",
        "declaration",
        "payment"
       ]
      },
      "blocksSubmission": {
       "type": "boolean",
       "default": false
      },
      "blocksApproval": {
       "type": "boolean",
       "default": true
      },
      "expiryMonths": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "FormDefinition": {
  "type": "object",
  "x-ticvai-persistence": "marketing.form_definition + marketing.form_definition_field",
  "description": "CF-129, CL-04. **A waiver, a survey and a data-capture form are one mechanism.**\nA waiver is this form with a signature. A survey is this form with a scale. A demographic capture is this form at the point of sale. They were raised as three separate gaps and share every part: field configuration, conditional display, versioning, an acceptance record and a stored artefact.\n**Three implementations would drift on the version rule first.** A waiver signed against version 3 must stay bound to version 3, and that is the same requirement a survey has when question wording changes mid-campaign — **an NPS score means nothing if you cannot say which question produced it.**\n",
  "required": [
   "id",
   "name",
   "kind",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "waiver",
     "survey",
     "dataCapture",
     "consentForm",
     "incidentReport",
     "registration"
    ]
   },
   "version": {
    "readOnly": true,
    "type": "integer",
    "description": "**Set by the server** — 1 on `createForm`, the next number on every change. **Immutable once anything is submitted against it.** A change creates a new version, and the old one stays readable forever — 2.15.13 requires the exact accepted version retained, which is legal evidence rather than a nicety.\n"
   },
   "fields": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FormField"
    }
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false,
    "description": "**What makes it a waiver.** And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it.\n"
   },
   "signatureKind": {
    "type": "string",
    "enum": [
     "drawn",
     "typed",
     "checkbox",
     "none"
    ],
    "default": "none"
   },
   "scoreScale": {
    "type": "string",
    "nullable": true,
    "enum": [
     "nps",
     "csat",
     "ces",
     "likert5",
     "likert7",
     "stars"
    ],
    "description": "**What makes it a survey.** Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's.\n"
   },
   "appliesToProductIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "validForMonths": {
    "type": "integer",
    "nullable": true,
    "description": "**How long an acceptance lasts.** A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to sign again — which only works if the expiry is stated.\n"
   },
   "minimumAge": {
    "type": "integer",
    "nullable": true
   },
   "requiresGuardianForMinors": {
    "type": "boolean",
    "default": true,
    "description": "**A minor cannot waive their own rights.** A guardian signs, and the record has to name them — an unsigned or self-signed minor waiver is worth nothing at the moment it matters.\n"
   },
   "status": {
    "readOnly": true,
    "type": "string",
    "enum": [
     "draft",
     "published",
     "superseded",
     "retired"
    ]
   },
   "legalReviewedBy": {
    "type": "string",
    "nullable": true
   },
   "legalReviewedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "FormField": {
  "type": "object",
  "description": "One field. **Conditional display is the shared requirement** — a survey branching on an answer and a waiver revealing a medical question on a yes are the same mechanism.\n",
  "required": [
   "key",
   "label",
   "type"
  ],
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "labelLocalised": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "type": {
    "type": "string",
    "enum": [
     "text",
     "longText",
     "number",
     "date",
     "select",
     "multiSelect",
     "boolean",
     "scale",
     "signature",
     "file",
     "phone",
     "email"
    ]
   },
   "options": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "isRequired": {
    "type": "boolean",
    "default": false
   },
   "isPersonalData": {
    "type": "boolean",
    "default": false,
    "description": "**Marked at the field, because retention is decided at the field.** A survey answer and a medical condition on the same form have different lifetimes, and a form-level flag makes the whole thing as sensitive as its most sensitive field.\n"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "showWhen": {
    "type": "object",
    "nullable": true,
    "properties": {
     "field": {
      "type": "string"
     },
     "equals": {
      "type": "string"
     }
    }
   }
  }
 }
}
```
