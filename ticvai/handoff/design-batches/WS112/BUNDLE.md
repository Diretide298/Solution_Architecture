# WS112 — ACCREDITATION board 5

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
| `BO-654` | Accreditation Access Command Center | commandCentre | 1 | 0 | — |
| `BO-655` | Access Profile Management | configEditor | 2 | 0 | — |
| `BO-656` | Venue & Zone Access Matrix | listDetail | 1 | 0 | — |
| `BO-657` | Operational Area Permission Management | listDetail | 1 | 0 | — |
| `BO-658` | Date & Time Access Rules | listDetail | 1 | 0 | — |
| `BO-659` | Access Schedule Management | listDetail | 1 | 0 | — |
| `BO-660` | Holder Access Assignment | listDetail | 1 | 0 | — |
| `BO-661` | Temporary Access & Exception Management | listDetail | 1 | 0 | — |
| `BO-662` | Access Revocation & Suspension | listDetail | 1 | 0 | — |
| `BO-663` | Access Rights Preview, Impact & Synchronization | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-656, BO-657, BO-658, BO-659, BO-660, BO-661, BO-662, BO-663 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-654",
  "name": "Accreditation Access Command Center",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "1",
   "page": 37
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accreditation-access-command-center-bo-654",
   "component": "apps/venue-management-web/src/routes/access-venue/AccreditationAccessCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-655",
    "BO-656",
    "BO-657",
    "BO-658",
    "BO-659",
    "BO-660",
    "BO-661",
    "BO-662",
    "BO-663"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-655",
     "trigger": "Access Profile Management",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-656",
     "trigger": "Venue & Zone Access Matrix",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-657",
     "trigger": "Operational Area Permission Management",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-658",
     "trigger": "Date & Time Access Rules",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-659",
     "trigger": "Access Schedule Management",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-660",
     "trigger": "Holder Access Assignment",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-661",
     "trigger": "Temporary Access & Exception Management",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-662",
     "trigger": "Access Revocation & Suspension",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-663",
     "trigger": "Access Rights Preview, Impact & Synchronization",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Dashboard KPIs shall include) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Central operational dashboard for accreditation access permissions.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active access profiles",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Accredited holders with access",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Credentials with assigned access",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Restricted-access holders",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Temporary access grants",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Expiring permissions",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Suspended access",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Revoked access",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Access exceptions",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Unassigned approved credentials",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Event",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Venue",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Accreditation program",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Category",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Organization",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Zone",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Access profile",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      },
      {
       "kind": "metricTile",
       "label": "Credential status",
       "provenance": "pack ACCREDITATION.pdf, page 37 §Dashboard KPIs shall include"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accreditation access list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the accreditation access untouched.",
   "emptyFirstRun": "No accreditation access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accreditation access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessProfiles",
    "contract": "accreditation",
    "purpose": "Access at a glance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-654",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-654"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 37. 0 of 0 labels bound to a contract property; 18 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-655",
  "name": "Access Profile Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "2",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-profile-management-bo-655",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessProfileManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-654"
   ],
   "exitTo": [
    "BO-654"
   ],
   "transitions": [
    {
     "to": "BO-654",
     "trigger": "Back to Accreditation Access Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each profile shall define) and no display directory — it is settings, not a population",
  "purpose": "Create reusable accreditation access profiles.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack ACCREDITATION.pdf, page 38 §Each profile shall define"
      },
      {
       "kind": "selectField",
       "label": "Permitted zones",
       "provenance": "pack ACCREDITATION.pdf, page 38 §Each profile shall define"
      },
      {
       "kind": "selectField",
       "label": "Permitted operational areas",
       "provenance": "pack ACCREDITATION.pdf, page 38 §Each profile shall define"
      },
      {
       "kind": "selectField",
       "label": "Date validity",
       "provenance": "pack ACCREDITATION.pdf, page 38 §Each profile shall define"
      },
      {
       "kind": "selectField",
       "label": "Time validity",
       "provenance": "pack ACCREDITATION.pdf, page 38 §Each profile shall define"
      },
      {
       "kind": "selectField",
       "label": "Access schedule",
       "provenance": "pack ACCREDITATION.pdf, page 38 §Each profile shall define"
      },
      {
       "kind": "selectField",
       "label": "Accreditation categories allowed",
       "provenance": "pack ACCREDITATION.pdf, page 38 §Each profile shall define"
      },
      {
       "kind": "selectField",
       "label": "Applicable events",
       "provenance": "pack ACCREDITATION.pdf, page 38 §Each profile shall define"
      },
      {
       "kind": "selectField",
       "label": "Default credential behavior",
       "provenance": "pack ACCREDITATION.pdf, page 38 §Each profile shall define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access profile configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the access profile untouched.",
   "emptyFirstRun": "No access profile configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listAccessProfiles",
    "contract": "accreditation",
    "purpose": "Profiles",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setAccessProfile",
    "contract": "accreditation",
    "purpose": "Define one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccessProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-655",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-655"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 38. 0 of 0 labels bound to a contract property; 9 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-656",
  "name": "Venue & Zone Access Matrix",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "3",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/venue-zone-access-matrix-bo-656",
   "component": "apps/venue-management-web/src/routes/access-venue/VenueZoneAccessMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-654"
   ],
   "exitTo": [
    "BO-654"
   ],
   "transitions": [
    {
     "to": "BO-654",
     "trigger": "Back to Accreditation Access Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Visually configure which accreditation profiles can access each venue zone.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 39"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 39"
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
   "loading": "The venue zone access list.",
   "error": "Could not load. Names which read failed and leaves the venue zone access untouched.",
   "emptyFirstRun": "No venue zone access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue zone access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccessProfile",
    "contract": "accreditation",
    "purpose": "Venue and zone matrix",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccessProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-656",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-656"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 39. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-657",
  "name": "Operational Area Permission Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "4",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/operational-area-permission-management-bo-657",
   "component": "apps/venue-management-web/src/routes/access-venue/OperationalAreaPermissionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-654"
   ],
   "exitTo": [
    "BO-654"
   ],
   "transitions": [
    {
     "to": "BO-654",
     "trigger": "Back to Accreditation Access Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure access to operational areas below the broader zone level.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 40"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 40"
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
   "loading": "The operational area permission list.",
   "error": "Could not load. Names which read failed and leaves the operational area permission untouched.",
   "emptyFirstRun": "No operational area permission yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational area permission are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccessProfile",
    "contract": "accreditation",
    "purpose": "Operational area permissions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccessProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-657",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-657"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 40. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-658",
  "name": "Date & Time Access Rules",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "5",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/date-time-access-rules-bo-658",
   "component": "apps/venue-management-web/src/routes/access-venue/DateTimeAccessRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-654"
   ],
   "exitTo": [
    "BO-654"
   ],
   "transitions": [
    {
     "to": "BO-654",
     "trigger": "Back to Accreditation Access Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control when accreditation access is valid.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 40"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 40"
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
   "loading": "The date time access list.",
   "error": "Could not load. Names which read failed and leaves the date time access untouched.",
   "emptyFirstRun": "No date time access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the date time access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccessProfile",
    "contract": "accreditation",
    "purpose": "Date and time rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccessProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-658",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-658"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 40. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-659",
  "name": "Access Schedule Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "6",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-schedule-management-bo-659",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessScheduleManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-654"
   ],
   "exitTo": [
    "BO-654"
   ],
   "transitions": [
    {
     "to": "BO-654",
     "trigger": "Back to Accreditation Access Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create reusable schedules for accreditation permissions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 41"
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
   "loading": "The access schedule list.",
   "error": "Could not load. Names which read failed and leaves the access schedule untouched.",
   "emptyFirstRun": "No access schedule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access schedule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccessProfile",
    "contract": "accreditation",
    "purpose": "Schedule by event phase",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listAccessProfiles"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-659",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-659"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 41. 0 of 0 labels bound to a contract property; 0 of 6 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-660",
  "name": "Holder Access Assignment",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "7",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/holder-access-assignment-bo-660",
   "component": "apps/venue-management-web/src/routes/access-venue/HolderAccessAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-654"
   ],
   "exitTo": [
    "BO-654"
   ],
   "transitions": [
    {
     "to": "BO-654",
     "trigger": "Back to Accreditation Access Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§The screen shall display) and no metric row",
  "purpose": "Assign access permissions to an individual accreditation holder.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack ACCREDITATION.pdf, page 42 §The screen shall display"
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
       "label": "Every holder access",
       "columns": [
        "Holder",
        "Photograph",
        "Accreditation",
        "Category",
        "Credential",
        "Event",
        "Venue",
        "Current access profile"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack ACCREDITATION.pdf, page 42 §The screen shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected holder access",
       "bindsTo": null,
       "columns": [
        "Holder",
        "Photograph",
        "Accreditation",
        "Category",
        "Credential",
        "Event",
        "Venue",
        "Current access profile"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Administrators shall be able to”, “Inherited Access”, “Individual Override”.",
       "provenance": "pack ACCREDITATION.pdf, page 42 §The screen shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The holder access list.",
   "error": "Could not load. Names which read failed and leaves the holder access untouched.",
   "emptyFirstRun": "No holder access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the holder access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setHolderAccess",
    "contract": "accreditation",
    "purpose": "Assign profiles to a holder",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccreditationHolder"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Holder",
    "Photograph",
    "Accreditation",
    "Category",
    "Credential",
    "Event"
   ],
   "params": [
    {
     "name": "holderId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-660",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-660"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 42. 0 of 8 labels bound to a contract property; 8 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-661",
  "name": "Temporary Access & Exception Management",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "8",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/temporary-access-exception-management-bo-661",
   "component": "apps/venue-management-web/src/routes/access-venue/TemporaryAccessExceptionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-654"
   ],
   "exitTo": [
    "BO-654"
   ],
   "transitions": [
    {
     "to": "BO-654",
     "trigger": "Back to Accreditation Access Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide controlled short-term access outside normal accreditation permissions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 42"
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
       "impliedBy": "setHolderAccess",
       "label": "Save holder access",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setHolderAccess"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The temporary access exception list.",
   "error": "Could not load. Names which read failed and leaves the temporary access exception untouched.",
   "emptyFirstRun": "No temporary access exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the temporary access exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setHolderAccess",
    "contract": "accreditation",
    "purpose": "Temporary access and exceptions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccreditationHolder"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-661",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-661"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-662",
  "name": "Access Revocation & Suspension",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "9",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-revocation-suspension-bo-662",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessRevocationSuspension.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-654"
   ],
   "exitTo": [
    "BO-654"
   ],
   "transitions": [
    {
     "to": "BO-654",
     "trigger": "Back to Accreditation Access Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Immediately remove or temporarily disable accreditation access.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 43"
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
   "loading": "The access revocation suspension list.",
   "error": "Could not load. Names which read failed and leaves the access revocation suspension untouched.",
   "emptyFirstRun": "No access revocation suspension yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access revocation suspension are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccreditationStatus",
    "contract": "accreditation",
    "purpose": "Revoke or suspend",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-662",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-662"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-663",
  "name": "Access Rights Preview, Impact & Synchronization",
  "module": "Access & Venue",
  "requiresModule": "accreditation",
  "wave": 3,
  "source": {
   "pack": "ACCREDITATION.pdf",
   "board": "5",
   "number": "10",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-rights-preview-impact-synchronization-bo-663",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessRightsPreviewImpactSynchronization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-654"
   ],
   "exitTo": [
    "BO-654"
   ],
   "transitions": [
    {
     "to": "BO-654",
     "trigger": "Back to Accreditation Access Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Validate accreditation access before publishing it to Access Control.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 44"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack ACCREDITATION.pdf, page 44"
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
       "impliedBy": "previewAccessImpact",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "previewAccessImpact"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access rights preview list.",
   "error": "Could not load. Names which read failed and leaves the access rights preview untouched.",
   "emptyFirstRun": "No access rights preview yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access rights preview are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "previewAccessImpact",
    "contract": "accreditation",
    "purpose": "Who this change would affect",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-663",
   "workshopBoard": "wireframes/WS05 ACCREDITATION Board 5.dc.html#bo-663"
  },
  "apisNote": "Regenerated 9 September 2026 from ACCREDITATION.pdf page 44. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listAccessProfiles": {
  "method": "GET",
  "path": "/accreditation-access-profiles",
  "contract": "accreditation",
  "summary": "Named bundles of zones, dates and times",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessProfile"
 },
 "previewAccessImpact": {
  "method": "POST",
  "path": "/accreditation-access-profiles/preview",
  "contract": "accreditation",
  "summary": "Who this change would affect, and how",
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
  "requestBody": "AccessProfile",
  "responds": "AccessImpact"
 },
 "setAccessProfile": {
  "method": "PUT",
  "path": "/accreditation-access-profiles",
  "contract": "accreditation",
  "summary": "Define which zones, on which dates, at which times",
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
  "responds": "AccreditationHolder"
 },
 "setHolderAccess": {
  "method": "PUT",
  "path": "/accreditation-holders/{holderId}/access",
  "contract": "accreditation",
  "summary": "Assign profiles, and any exception on top",
  "permission": "ACCREDITATION_MANAGE",
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
  "requestBody": "HolderAccess",
  "responds": "HolderAccess"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessImpact": {
  "type": "object",
  "description": "Board 5.10. **There is no undo fast enough once a shift has started.**",
  "properties": {
   "holdersAffected": {
    "type": "integer"
   },
   "gainingAccess": {
    "type": "integer"
   },
   "losingAccess": {
    "type": "integer"
   },
   "leftWithNoAccess": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "holderId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      }
     }
    }
   },
   "zonesAdded": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "zonesRemoved": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
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
   "email": {
    "type": "string",
    "format": "email",
    "nullable": true,
    "description": "12.1.16. The holder's own address — where a mobile credential and renewal notices go"
   },
   "phone": {
    "type": "string",
    "nullable": true,
    "description": "12.1.16. E.164"
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
 "HolderAccess": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.holder_access",
  "description": "Boards 5.7 and 5.8. **An exception with no end is a profile change nobody reviewed.**\n",
  "properties": {
   "holderId": {
    "type": "string",
    "format": "uuid"
   },
   "accessProfileIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "exceptions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "zoneId": {
       "type": "string",
       "format": "uuid"
      },
      "grant": {
       "type": "boolean"
      },
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "approvedBy": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "effectiveZones": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
