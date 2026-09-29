# WS113 — ACCREDITATION board 6

**10 screens · 5 operations · 4 schemas · 3 permissions**

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
  `ACCREDITATION_CONFIGURE, ACCREDITATION_MANAGE, ACCREDITATION_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-664` | Accreditation Lifecycle Command Center | listDetail | 1 | 0 | — |
| `BO-665` | Accreditation Status Workflow | configEditor | 1 | 0 | — |
| `BO-666` | Validity Period Configuration | listDetail | 1 | 0 | — |
| `BO-667` | Event & Venue Accreditation Assignment | listDetail | 1 | 0 | — |
| `BO-668` | Multi-Venue Accreditation Management | listDetail | 1 | 0 | — |
| `BO-669` | Temporary & Seasonal Accreditation | configEditor | 1 | 0 | — |
| `BO-670` | Suspension & Reactivation Management | configEditor | 1 | 0 | — |
| `BO-671` | Accreditation Revocation Management | listDetail | 1 | 0 | — |
| `BO-672` | Expiry Monitor & Expiration Rules | listDetail | 1 | 0 | — |
| `BO-673` | Accreditation Renewal Workspace | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-664, BO-666, BO-667, BO-668, BO-671, BO-672, BO-673 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-664",
  "name": "Accreditation Lifecycle Command Center",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "1",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-lifecycle-command-center-bo-664",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationLifecycleCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-665",
    "BO-666",
    "BO-667",
    "BO-668",
    "BO-669",
    "BO-670",
    "BO-671",
    "BO-672",
    "BO-673"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-665",
     "trigger": "Accreditation Status Workflow",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-666",
     "trigger": "Validity Period Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-667",
     "trigger": "Event & Venue Accreditation Assignment",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-668",
     "trigger": "Multi-Venue Accreditation Management",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-669",
     "trigger": "Temporary & Seasonal Accreditation",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-670",
     "trigger": "Suspension & Reactivation Management",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-671",
     "trigger": "Accreditation Revocation Management",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-672",
     "trigger": "Expiry Monitor & Expiration Rules",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-673",
     "trigger": "Accreditation Renewal Workspace",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Central operational dashboard for accreditation lifecycle status.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 46"
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
       "impliedBy": "listAccreditationHolders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation lifecycle list.",
   "error": "Could not load. Names which read failed and leaves the accreditation lifecycle untouched.",
   "emptyFirstRun": "No accreditation lifecycle yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation lifecycle are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationHolders",
    "contract": "accreditation",
    "purpose": "Lifecycle at a glance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-664",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-664"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-665",
  "name": "Accreditation Status Workflow",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "2",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-status-workflow-bo-665",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationStatusWorkflow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-664"
   ],
   "exitTo": [
    "BO-664"
   ],
   "transitions": [
    {
     "to": "BO-664",
     "trigger": "Back to Accreditation Lifecycle Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each transition may define) and no display directory — it is settings, not a population",
  "purpose": "Configure and manage the accreditation lifecycle statuses.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Required permission",
       "provenance": "pack ACCREDITATION.pdf, page 47 §Each transition may define"
      },
      {
       "kind": "selectField",
       "label": "Approval requirement",
       "provenance": "pack ACCREDITATION.pdf, page 47 §Each transition may define"
      },
      {
       "kind": "selectField",
       "label": "Reason requirement",
       "provenance": "pack ACCREDITATION.pdf, page 47 §Each transition may define"
      },
      {
       "kind": "selectField",
       "label": "Notification",
       "provenance": "pack ACCREDITATION.pdf, page 47 §Each transition may define"
      },
      {
       "kind": "selectField",
       "label": "Credential action",
       "provenance": "pack ACCREDITATION.pdf, page 47 §Each transition may define"
      },
      {
       "kind": "selectField",
       "label": "Access-right action",
       "provenance": "pack ACCREDITATION.pdf, page 47 §Each transition may define"
      },
      {
       "kind": "selectField",
       "label": "Key requirement: 12.1.32",
       "provenance": "pack ACCREDITATION.pdf, page 47 §Each transition may define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation status workflow configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the accreditation status workflow untouched.",
   "emptyFirstRun": "No accreditation status workflow configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setAccreditationStatus",
    "contract": "accreditation",
    "purpose": "Move through the workflow",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationHolders",
     "listAccreditationAudit"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-665",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-665"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 47. 0 of 0 labels bound to a contract property; 7 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-666",
  "name": "Validity Period Configuration",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "3",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/validity-period-configuration-bo-666",
   "component": "apps/venue-management-web/src/routes/access-venue/ValidityPeriodConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-664"
   ],
   "exitTo": [
    "BO-664"
   ],
   "transitions": [
    {
     "to": "BO-664",
     "trigger": "Back to Accreditation Lifecycle Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how long an accreditation remains valid.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 48"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 48"
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
       "impliedBy": "setAccreditationValidity",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccreditationValidity"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The validity period list.",
   "error": "Could not load. Names which read failed and leaves the validity period untouched.",
   "emptyFirstRun": "No validity period yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the validity period are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccreditationValidity",
    "contract": "accreditation",
    "purpose": "Validity periods",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationHolders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-666",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-666"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 48. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-667",
  "name": "Event & Venue Accreditation Assignment",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "4",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/event-venue-accreditation-assignment-bo-667",
   "component": "apps/venue-management-web/src/routes/access-venue/EventVenueAccreditationAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-664"
   ],
   "exitTo": [
    "BO-664"
   ],
   "transitions": [
    {
     "to": "BO-664",
     "trigger": "Back to Accreditation Lifecycle Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine the event and venue scope of an accreditation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 49"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 49"
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
   "loading": "The event venue accreditation list.",
   "error": "Could not load. Names which read failed and leaves the event venue accreditation untouched.",
   "emptyFirstRun": "No event venue accreditation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event venue accreditation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createAccreditationProgramme",
    "contract": "accreditation",
    "purpose": "Event and venue assignment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationProgrammes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-667",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-667"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-668",
  "name": "Multi-Venue Accreditation Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "5",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/multi-venue-accreditation-management-bo-668",
   "component": "apps/venue-management-web/src/routes/access-venue/MultiVenueAccreditationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-664"
   ],
   "exitTo": [
    "BO-664"
   ],
   "transitions": [
    {
     "to": "BO-664",
     "trigger": "Back to Accreditation Lifecycle Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow one accreditation to operate across multiple approved venues.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 49"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 49"
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
       "impliedBy": "setAccessProfile",
       "label": "Save access profile",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccessProfile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-venue accreditation list.",
   "error": "Could not load. Names which read failed and leaves the multi-venue accreditation untouched.",
   "emptyFirstRun": "No multi-venue accreditation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-venue accreditation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccessProfile",
    "contract": "accreditation",
    "purpose": "Multi-venue accreditation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccessProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-668",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-668"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-669",
  "name": "Temporary & Seasonal Accreditation",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "6",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/temporary-seasonal-accreditation-bo-669",
   "component": "apps/venue-management-web/src/routes/access-venue/TemporarySeasonalAccreditation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-664"
   ],
   "exitTo": [
    "BO-664"
   ],
   "transitions": [
    {
     "to": "BO-664",
     "trigger": "Back to Accreditation Lifecycle Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Manage short-duration and recurring accreditation programs.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Accreditation type",
       "provenance": "pack ACCREDITATION.pdf, page 50 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Start/end date",
       "provenance": "pack ACCREDITATION.pdf, page 50 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Events",
       "provenance": "pack ACCREDITATION.pdf, page 50 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Venues",
       "provenance": "pack ACCREDITATION.pdf, page 50 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Access profile",
       "provenance": "pack ACCREDITATION.pdf, page 50 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic expiry",
       "provenance": "pack ACCREDITATION.pdf, page 50 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Renewal eligibility",
       "provenance": "pack ACCREDITATION.pdf, page 50 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The temporary seasonal accreditation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the temporary seasonal accreditation untouched.",
   "emptyFirstRun": "No temporary seasonal accreditation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setAccreditationValidity",
    "contract": "accreditation",
    "purpose": "Temporary and seasonal",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationHolders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-669",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-669"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 50. 0 of 0 labels bound to a contract property; 7 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-670",
  "name": "Suspension & Reactivation Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "7",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/suspension-reactivation-management-bo-670",
   "component": "apps/venue-management-web/src/routes/access-venue/SuspensionReactivationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-664"
   ],
   "exitTo": [
    "BO-664"
   ],
   "transitions": [
    {
     "to": "BO-664",
     "trigger": "Back to Accreditation Lifecycle Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§The operator shall specify) and no display directory — it is settings, not a population",
  "purpose": "Temporarily disable accreditation without permanently terminating it.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Suspension reason",
       "provenance": "pack ACCREDITATION.pdf, page 51 §The operator shall specify"
      },
      {
       "kind": "selectField",
       "label": "Effective date/time",
       "provenance": "pack ACCREDITATION.pdf, page 51 §The operator shall specify"
      },
      {
       "kind": "textField",
       "label": "Expected end date where applicable",
       "provenance": "pack ACCREDITATION.pdf, page 51 §The operator shall specify"
      },
      {
       "kind": "selectField",
       "label": "Notes",
       "provenance": "pack ACCREDITATION.pdf, page 51 §The operator shall specify"
      },
      {
       "kind": "selectField",
       "label": "Supporting evidence",
       "provenance": "pack ACCREDITATION.pdf, page 51 §The operator shall specify"
      },
      {
       "kind": "selectField",
       "label": "Approver where required",
       "provenance": "pack ACCREDITATION.pdf, page 51 §The operator shall specify"
      },
      {
       "kind": "selectField",
       "label": "Credential → Suspended",
       "provenance": "pack ACCREDITATION.pdf, page 51 §The operator shall specify"
      },
      {
       "kind": "textField",
       "label": "Access Rights → Disabled",
       "provenance": "pack ACCREDITATION.pdf, page 51 §The operator shall specify"
      },
      {
       "kind": "selectField",
       "label": "Key requirement: 12.1.34",
       "provenance": "pack ACCREDITATION.pdf, page 51 §The operator shall specify"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The suspension reactivation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the suspension reactivation untouched.",
   "emptyFirstRun": "No suspension reactivation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setAccreditationStatus",
    "contract": "accreditation",
    "purpose": "Suspend and reactivate",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationHolders",
     "listAccreditationAudit"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-670",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-670"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 51. 0 of 0 labels bound to a contract property; 9 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-671",
  "name": "Accreditation Revocation Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "8",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-revocation-management-bo-671",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationRevocationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-664"
   ],
   "exitTo": [
    "BO-664"
   ],
   "transitions": [
    {
     "to": "BO-664",
     "trigger": "Back to Accreditation Lifecycle Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Permanently terminate an accreditation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 51"
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
       "impliedBy": "setAccreditationStatus",
       "label": "Save accreditation status",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccreditationStatus"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation revocation list.",
   "error": "Could not load. Names which read failed and leaves the accreditation revocation untouched.",
   "emptyFirstRun": "No accreditation revocation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation revocation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccreditationStatus",
    "contract": "accreditation",
    "purpose": "Revoke",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationHolders",
     "listAccreditationAudit"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-671",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-671"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 51. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-672",
  "name": "Expiry Monitor & Expiration Rules",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "9",
   "page": 52
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/expiry-monitor-expiration-rules-bo-672",
   "component": "apps/venue-management-web/src/routes/access-venue/ExpiryMonitorExpirationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-664"
   ],
   "exitTo": [
    "BO-664"
   ],
   "transitions": [
    {
     "to": "BO-664",
     "trigger": "Back to Accreditation Lifecycle Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Proactively manage accreditations approaching expiry.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 52"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 52"
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
       "impliedBy": "listAccreditationHolders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The expiry expiration rules list.",
   "error": "Could not load. Names which read failed and leaves the expiry expiration rules untouched.",
   "emptyFirstRun": "No expiry expiration rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the expiry expiration rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccreditationHolders",
    "contract": "accreditation",
    "purpose": "Expiring soon",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-672",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-672"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 52. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-673",
  "name": "Accreditation Renewal Workspace",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "6",
   "number": "10",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-renewal-workspace-bo-673",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationRenewalWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-664"
   ],
   "exitTo": [
    "BO-664"
   ],
   "transitions": [
    {
     "to": "BO-664",
     "trigger": "Back to Accreditation Lifecycle Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage accreditation renewal without unnecessarily recreating the holder or application.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 53"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 53"
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
       "impliedBy": "setAccreditationValidity",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccreditationValidity"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation renewal list.",
   "error": "Could not load. Names which read failed and leaves the accreditation renewal untouched.",
   "emptyFirstRun": "No accreditation renewal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation renewal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccreditationValidity",
    "contract": "accreditation",
    "purpose": "Expiry and renewal rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccreditationHolders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-673",
   "workshopBoard": "wireframes/WS06 ACCREDITATION Board 6.dc.html#bo-673"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 53. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "setAccessProfile": {
  "method": "PUT",
  "path": "/accreditation-access-profiles",
  "contract": "accreditation",
  "summary": "Define which zones, on which dates, at which times",
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
  "requestBody": "AccessProfile",
  "responds": "AccessProfile"
 },
 "setAccreditationStatus": {
  "method": "POST",
  "path": "/accreditation-holders/{holderId}/status",
  "contract": "accreditation",
  "summary": "Suspend, reactivate, revoke or expire an accreditation",
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
  "responds": "AccreditationHolder"
 },
 "setAccreditationValidity": {
  "method": "PUT",
  "path": "/accreditation-validity",
  "contract": "accreditation",
  "summary": "Validity periods, renewal windows and expiry behaviour",
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
  "requestBody": "AccreditationValidity",
  "responds": "AccreditationValidity"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessProfile": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.access_profile",
  "description": "Board 5.2. **How an estate stays governable.**",
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
   "zoneIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "operationalAreas": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "schedule": {
    "type": "array",
    "description": "**Zone, date and time are three dimensions and all three are needed.**",
    "items": {
     "type": "object",
     "properties": {
      "zoneId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "dateFrom": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "dateTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "from": {
       "type": "string",
       "nullable": true
      },
      "to": {
       "type": "string",
       "nullable": true
      },
      "eventPhase": {
       "type": "string",
       "nullable": true,
       "enum": [
        "build",
        "rehearsal",
        "doorsOpen",
        "liveShow",
        "breakdown"
       ]
      }
     }
    }
   },
   "escortRequired": {
    "type": "boolean",
    "default": false
   },
   "holderCount": {
    "type": "integer",
    "readOnly": true
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
 "AccreditationValidity": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.validity",
  "description": "Board 6.3. **The control most often configured as never.**",
  "properties": {
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "validityKind": {
    "type": "string",
    "enum": [
     "eventDuration",
     "fixedPeriod",
     "seasonal",
     "rolling",
     "permanent"
    ]
   },
   "validityMonths": {
    "type": "integer",
    "nullable": true
   },
   "renewalWindowDays": {
    "type": "integer",
    "nullable": true
   },
   "renewalRequiresReverification": {
    "type": "boolean",
    "default": true,
    "description": "**The point of an expiry is that somebody looks again.**"
   },
   "onExpiry": {
    "type": "string",
    "enum": [
     "revokeAccess",
     "gracePeriod",
     "autoRenew"
    ],
    "default": "revokeAccess"
   },
   "gracePeriodDays": {
    "type": "integer",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
