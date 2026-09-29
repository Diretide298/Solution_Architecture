# WS157 — Resource Management Configuration board 3

**10 screens · 30 operations · 30 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW, USER_MANAGE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-873` | Staff Resource Directory | listDetail | 1 | 0 | — |
| `BO-874` | Staff Resource Profile | configEditor | 4 | 0 | — |
| `BO-875` | Skills & Competency Management | listDetail | 1 | 0 | — |
| `BO-876` | Certification & Expiry Management | configEditor | 2 | 0 | — |
| `BO-877` | Qualification & Assignment Rule Engine | listDetail | 3 | 0 | — |
| `BO-878` | Staff Availability & Working Pattern | configEditor | 4 | 0 | — |
| `BO-879` | Shift Template & Assignment Configuration | configEditor | 4 | 0 | — |
| `BO-880` | Break, Leave & Absence Configuration | configEditor | 6 | 0 | — |
| `BO-881` | Overtime & Working-Hour Rules | configEditor | 1 | 0 | — |
| `BO-882` | Workforce Integration & Synchronization Center | listDetail | 9 | 0 | — |

## Thin screens in this batch

**BO-873, BO-875, BO-877 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-873",
  "name": "Staff Resource Directory",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "01",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/staff-resource-directory-bo-873",
   "component": "apps/venue-management-web/src/routes/rentals/StaffResourceDirectory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-874",
    "BO-875",
    "BO-876",
    "BO-877",
    "BO-878",
    "BO-879",
    "BO-880",
    "BO-881",
    "BO-882"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-874",
     "trigger": "Staff Resource Profile",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-875",
     "trigger": "Skills & Competency Management",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-876",
     "trigger": "Certification & Expiry Management",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-877",
     "trigger": "Qualification & Assignment Rule Engine",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-878",
     "trigger": "Staff Availability & Working Pattern",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-879",
     "trigger": "Shift Template & Assignment Configuration",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-880",
     "trigger": "Break, Leave & Absence Configuration",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-881",
     "trigger": "Overtime & Working-Hour Rules",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-882",
     "trigger": "Workforce Integration & Synchronization Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the centralized master directory for all personnel who may be assigned as operational resources within TICVAI.",
  "purposeNote": "Authorized users can locate and manage staff resources from one centralized directory using structured filters or conversational AI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 33"
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
       "label": "Search staff resource",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 33 §Users shall filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Department",
        "Role",
        "Staff type",
        "Skill",
        "Certification",
        "Qualification",
        "Availability",
        "Employment type",
        "Status"
       ],
       "notes": "The pack filters this screen by venue, department, role, staff type, skill, certification and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 33 §Users shall filter by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staff resource list.",
   "error": "Could not load. Names which read failed and leaves the staff resource untouched.",
   "emptyFirstRun": "No staff resource yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the staff resource are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrincipals",
    "contract": "identity",
    "purpose": "The staff directory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-873",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-873"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 33. 0 of 10 labels bound to a contract property; 10 of 58 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-874",
  "name": "Staff Resource Profile",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "02",
   "page": 35
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/staff-resource-profile-bo-874",
   "component": "apps/venue-management-web/src/routes/rentals/StaffResourceProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-873"
   ],
   "exitTo": [
    "BO-873"
   ],
   "transitions": [
    {
     "to": "BO-873",
     "trigger": "Back to Staff Resource Directory",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Maintain the operational resource profile for an individual employee or contractor. This profile shall complement the organization's HR employee record rather than unnecessarily duplicate an HR system.",
  "purposeNote": "Each staff resource has a complete operational profile that can be safely referenced by scheduling, resource allocation, event management, mobile operations, and AI services.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Resource priority",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer selectable yes/no",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "textField",
       "label": "Individual selection allowed yes/no",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Bookable yes/no",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Scheduling enabled yes/no",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum concurrent assignment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default assignment duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Preferred operating area",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Languages",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tags",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Employment Classification",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "External agency",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "External employee ID",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Source system",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Synchronization status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Last synchronization",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 35 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staff resource profile configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the staff resource profile untouched.",
   "emptyFirstRun": "No staff resource profile configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getPrincipal",
    "contract": "identity",
    "purpose": "One person",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listResources",
    "contract": "resources",
    "purpose": "Them as a bookable resource",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getEmployee",
    "contract": "workforce",
    "purpose": "Show the HR record behind the staff resource (agency, external id, externally mastered fields)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) External agency, External employee ID; Source system, Synchronization status, Last synchronization"
   },
   {
    "operationId": "listIntegrationSources",
    "contract": "workforce",
    "purpose": "Show the source system, its sync status and last sync",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) External agency, External employee ID; Source system, Synchronization status, Last synchronization"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-874",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-874"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 35. 0 of 0 labels bound to a contract property; 16 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** External agency, External employee ID: `getEmployee`; Source system, Synchronization status, Last synchronization: `listIntegrationSources`.",
  "entryState": {
   "params": [
    {
     "name": "principalId",
     "from": "session"
    },
    {
     "name": "employeeId",
     "from": "BO-873"
    }
   ],
   "coldEntry": "Opened from BO-873 with the employee picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the employee no longer exists."
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
  "id": "BO-875",
  "name": "Skills & Competency Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "03",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/skills-competency-management-bo-875",
   "component": "apps/venue-management-web/src/routes/rentals/SkillsCompetencyManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-873"
   ],
   "exitTo": [
    "BO-873"
   ],
   "transitions": [
    {
     "to": "BO-873",
     "trigger": "Back to Staff Resource Directory",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define what each staff resource is capable of performing.",
  "purposeNote": "Administrators can maintain reusable staff competencies and proficiency levels that are available to the assignment and AI recommendation engines.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 36"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 36"
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
       "impliedBy": "setResourceQualifications",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setResourceQualifications"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The skills competency list.",
   "error": "Could not load. Names which read failed and leaves the skills competency untouched.",
   "emptyFirstRun": "No skills competency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the skills competency are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setResourceQualifications",
    "contract": "resources",
    "purpose": "Skills and competencies",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-875",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-875"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 36. 0 of 0 labels bound to a contract property; 0 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
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
  "id": "BO-876",
  "name": "Certification & Expiry Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "04",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/certification-expiry-management-bo-876",
   "component": "apps/venue-management-web/src/routes/rentals/CertificationExpiryManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-873"
   ],
   "exitTo": [
    "BO-873"
   ],
   "transitions": [
    {
     "to": "BO-873",
     "trigger": "Back to Staff Resource Directory",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Manage certifications, licenses and credentials required for staff assignments.",
  "purposeNote": "unqualified staff from being assigned where mandatory certification rules apply.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Certification code",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Certification name",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Issuing authority",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable roles",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable resource types",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable venues",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Validity period",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Renewal requirements",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Mandatory/optional",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Warning period",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 38 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The certification expiry configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the certification expiry untouched.",
   "emptyFirstRun": "No certification expiry configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setResourceQualifications",
    "contract": "resources",
    "purpose": "Certification and expiry",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "validateWorkforceCompliance",
    "contract": "workforce",
    "purpose": "What has lapsed",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-876",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-876"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 38. 0 of 0 labels bound to a contract property; 10 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
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
  "id": "BO-877",
  "name": "Qualification & Assignment Rule Engine",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "05",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/qualification-assignment-rule-engine-bo-877",
   "component": "apps/venue-management-web/src/routes/rentals/QualificationAssignmentRuleEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-873"
   ],
   "exitTo": [
    "BO-873"
   ],
   "transitions": [
    {
     "to": "BO-873",
     "trigger": "Back to Staff Resource Directory",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert skills, certifications and operational policies into machine-enforceable assignment rules.",
  "purposeNote": "Staff assignment requirements are machine-readable, testable and automatically enforced before assignment confirmation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 39"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 39"
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
       "label": "Minimum requirement",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 39 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Preferred requirement",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 39 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Mandatory requirement",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 39 §Support"
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
   "loading": "The qualification rule list.",
   "error": "Could not load. Names which read failed and leaves the qualification rule untouched.",
   "emptyFirstRun": "No qualification rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the qualification rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setResourceQualifications",
    "contract": "resources",
    "purpose": "Qualification rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "suggestResources",
    "contract": "resources",
    "purpose": "Who qualifies",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setExperienceResourceRequirements",
    "contract": "resources",
    "purpose": "Save qualification requirements as mandatory or preferred with a minimum quantity",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Minimum requirement, Preferred requirement, Mandatory requirement",
    "invalidates": [
     "suggestResources"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-877",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-877"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 39. 0 of 0 labels bound to a contract property; 3 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Minimum requirement, Preferred requirement, Mandatory requirement: `setExperienceResourceRequirements`.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
     "from": "navigation"
    },
    {
     "name": "experienceId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opened from BO-873 with the experience picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the experience no longer exists."
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
  "id": "BO-878",
  "name": "Staff Availability & Working Pattern",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "06",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/staff-availability-working-pattern-bo-878",
   "component": "apps/venue-management-web/src/routes/rentals/StaffAvailabilityWorkingPattern.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-873"
   ],
   "exitTo": [
    "BO-873"
   ],
   "transitions": [
    {
     "to": "BO-873",
     "trigger": "Back to Staff Resource Directory",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Users shall configure) and no display directory — it is settings, not a population",
  "purpose": "Define when an individual staff resource is normally available to work.",
  "purposeNote": "Each staff resource has a reliable working-availability pattern that feeds the centralized Resource Calendar and assignment engine.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Working days",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Start time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "End time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Time zone",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective period",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Weekly hours",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Availability type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Seasonal pattern",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Availability Types",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Additional availability",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Temporary unavailability",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Special working day",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Venue reassignment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Restricted hours",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Calendar Preview",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Available",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Working",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Unavailable",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Leave",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Break",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      },
      {
       "kind": "selectField",
       "label": "Existing assignment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Users shall configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "External schedule",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 40 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staff availability working configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the staff availability working untouched.",
   "emptyFirstRun": "No staff availability working configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getResourceSchedule",
    "contract": "resources",
    "purpose": "Availability and working pattern",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setResourceSchedule",
    "contract": "resources",
    "purpose": "Set it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setFieldOwnership",
    "contract": "workforce",
    "purpose": "Declare the working pattern mastered by an external workforce system",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) External schedule"
   },
   {
    "operationId": "listIntegrationSources",
    "contract": "workforce",
    "purpose": "The integration sources whose field ownership is set",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-878",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-878"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 40. 0 of 0 labels bound to a contract property; 22 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** External schedule: `setFieldOwnership`.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
     "from": "navigation"
    },
    {
     "name": "sourceId",
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
  "id": "BO-879",
  "name": "Shift Template & Assignment Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "07",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/shift-template-assignment-configuration-bo-879",
   "component": "apps/venue-management-web/src/routes/rentals/ShiftTemplateAssignmentConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-873"
   ],
   "exitTo": [
    "BO-873"
   ],
   "transitions": [
    {
     "to": "BO-873",
     "trigger": "Back to Staff Resource Directory",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall define) and no display directory — it is settings, not a population",
  "purpose": "Configure reusable workforce shift structures that can later be used by the operational roster engine.",
  "purposeNote": "Administrators can create reusable governed shift structures that can subsequently be consumed by rostering and workforce scheduling.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Maximum shifts per day",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 41 §Administrators shall define"
      },
      {
       "kind": "selectField",
       "label": "Maximum consecutive days",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 41 §Administrators shall define"
      },
      {
       "kind": "textField",
       "label": "Minimum rest between shifts",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 41 §Administrators shall define"
      },
      {
       "kind": "selectField",
       "label": "Allowed roles",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 41 §Administrators shall define"
      },
      {
       "kind": "selectField",
       "label": "Venue restrictions",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 41 §Administrators shall define"
      },
      {
       "kind": "selectField",
       "label": "Skill requirements",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 41 §Administrators shall define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The shift template configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the shift template untouched.",
   "emptyFirstRun": "No shift template configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listShiftTemplates",
    "contract": "workforce",
    "purpose": "Shift templates",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setShiftTemplate",
    "contract": "workforce",
    "purpose": "Define one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listShiftTemplates"
    ]
   },
   {
    "operationId": "listShiftPatterns",
    "contract": "workforce",
    "purpose": "Shift patterns",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setShiftPattern",
    "contract": "workforce",
    "purpose": "Define a shift pattern and its break",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listShiftTemplates",
     "listShiftPatterns"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-879",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-879"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 41. 0 of 0 labels bound to a contract property; 6 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-880",
  "name": "Break, Leave & Absence Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "08",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/break-leave-absence-configuration-bo-880",
   "component": "apps/venue-management-web/src/routes/rentals/BreakLeaveAbsenceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-873"
   ],
   "exitTo": [
    "BO-873"
   ],
   "transitions": [
    {
     "to": "BO-873",
     "trigger": "Back to Staff Resource Directory",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Ensure employee availability reflects breaks, approved leave, absences and other workforce exceptions.",
  "purposeNote": "Breaks, leave and absences are automatically reflected in staff availability and cannot be ignored by downstream scheduling without authorized override.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Break type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum shift duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Break duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Paid/unpaid",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mandatory/optional",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Earliest break",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Latest break",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number of breaks",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Leave Types",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Administrative block",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 42 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The break leave absence configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the break leave absence untouched.",
   "emptyFirstRun": "No break leave absence configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listLeaveRequests",
    "contract": "workforce",
    "purpose": "Leave and absence",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "requestLeave",
    "contract": "workforce",
    "purpose": "Request time off",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listLeaveRequests",
     "getStaffingCoverage"
    ]
   },
   {
    "operationId": "listLeaveTypes",
    "contract": "workforce",
    "purpose": "Leave types",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setLeaveType",
    "contract": "workforce",
    "purpose": "Define a leave type",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listLeaveRequests",
     "listLeaveTypes"
    ]
   },
   {
    "operationId": "listLeaveBalances",
    "contract": "workforce",
    "purpose": "Leave balances",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "createResourceBlock",
    "contract": "resources",
    "purpose": "Block the staff resource's time for an administrative reason",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Administrative block"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-880",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-880"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 42. 0 of 0 labels bound to a contract property; 10 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Administrative block: `createResourceBlock`.",
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
  "id": "BO-881",
  "name": "Overtime & Working-Hour Rules",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "09",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/overtime-working-hour-rules-bo-881",
   "component": "apps/venue-management-web/src/routes/rentals/OvertimeWorkingHourRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-873"
   ],
   "exitTo": [
    "BO-873"
   ],
   "transitions": [
    {
     "to": "BO-873",
     "trigger": "Back to Staff Resource Directory",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Configure workforce rules controlling employee working hours and overtime eligibility before operational rostering occurs.",
  "purposeNote": "Working-hour and overtime rules are configurable and automatically considered before staff assignments are confirmed.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Standard daily hours",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 44 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Standard weekly hours",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 44 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum daily hours",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 44 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum weekly hours",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 44 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum rest period",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 44 §Administrators shall configure"
      },
      {
       "kind": "textField",
       "label": "Maximum consecutive working days",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 44 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Overtime threshold",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 44 §Administrators shall configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approval required",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 44 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The overtime working-hour rules configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the overtime working-hour rules untouched.",
   "emptyFirstRun": "No overtime working-hour rules configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setStaffingRules",
    "contract": "workforce",
    "purpose": "Overtime and working-hour rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getStaffingCoverage",
     "validateWorkforceCompliance"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-881",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-881"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 44. 0 of 0 labels bound to a contract property; 8 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Approval required are choices sent by `setStaffingRules` (overtime.requiresApproval).",
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
  "id": "BO-882",
  "name": "Workforce Integration & Synchronization Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "3",
   "number": "10",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/workforce-integration-synchronization-center-bo-882",
   "component": "apps/venue-management-web/src/routes/rentals/WorkforceIntegrationSynchronizationCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-873"
   ],
   "exitTo": [
    "BO-873"
   ],
   "transitions": [
    {
     "to": "BO-873",
     "trigger": "Back to Staff Resource Directory",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Connect TICVAI Resource Management with external HR, workforce management, payroll, identity, and employee systems where applicable. Provide TICVAI with a centralized, intelligent Workforce Operations & Rostering Engine that converts staff profiles, availability, skills, certifications, working-hour rules, and demand forecasts into executable operational rosters. Board 4 shall enable managers to: Build operational rosters Assign employees to attractions, venues, events, and activities Define minimum staffing requirements Validate role and skill coverage Identify staffing shortages Manage shift swaps, transfers, pickups, and releases Monitor planned versus actual attendance Capture check-in/check-out and attendance exceptions Validate workforce compliance before assignments Calculate and forecast labor costs Use AI to optimize staffing",
  "purposeNote": "clear field ownership, traceability and operational consistency.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 45 §Display"
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
       "label": "Every workforce integration synchronization",
       "columns": [
        "Connected systems",
        "Last synchronization",
        "Successful records",
        "Failed records",
        "Warnings",
        "Mapping errors",
        "Authentication status",
        "Conflict Handling"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 45 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected workforce integration synchronization",
       "bindsTo": null,
       "columns": [
        "Connected systems",
        "Last synchronization",
        "Successful records",
        "Failed records",
        "Warnings",
        "Mapping errors",
        "Authentication status",
        "Conflict Handling"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Integration Sources”, “External System Master”, “For example”, “Board 3 Shared Governance”, “Board 3 End-to-End Outcome”, “The platform understands”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 45 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "API",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Webhooks/event-driven integration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Scheduled synchronization",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Manual synchronization",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "File import where required",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Integration Monitoring",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 45 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workforce integration synchronization list.",
   "error": "Could not load. Names which read failed and leaves the workforce integration synchronization untouched.",
   "emptyFirstRun": "No workforce integration synchronization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workforce integration synchronization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRotaAssignments",
    "contract": "workforce",
    "purpose": "Rota synchronisation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listIntegrationSources",
    "contract": "workforce",
    "purpose": "Connected workforce systems",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setIntegrationSource",
    "contract": "workforce",
    "purpose": "Connect or reconfigure an external workforce system",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listRotaAssignments",
     "listIntegrationSources"
    ]
   },
   {
    "operationId": "getFieldOwnership",
    "contract": "workforce",
    "purpose": "Which system masters each field",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setFieldOwnership",
    "contract": "workforce",
    "purpose": "Declare who masters each field",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listRotaAssignments",
     "listIntegrationSources",
     "getFieldOwnership"
    ]
   },
   {
    "operationId": "listSyncRuns",
    "contract": "workforce",
    "purpose": "Synchronisation runs",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "startSync",
    "contract": "workforce",
    "purpose": "Run a synchronisation now",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listRotaAssignments",
     "listIntegrationSources",
     "getFieldOwnership",
     "listSyncRuns"
    ]
   },
   {
    "operationId": "listSyncConflicts",
    "contract": "workforce",
    "purpose": "Disagreements between systems",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "resolveSyncConflict",
    "contract": "workforce",
    "purpose": "Settle a disagreement",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listRotaAssignments",
     "listIntegrationSources",
     "getFieldOwnership",
     "listSyncRuns"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Connected systems",
    "Last synchronization",
    "Successful records",
    "Failed records",
    "Warnings",
    "Mapping errors"
   ],
   "params": [
    {
     "name": "sourceId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-882",
   "workshopBoard": "wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-882"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 45. 0 of 8 labels bound to a contract property; 14 of 111 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** API, Webhooks/event-driven integration, Scheduled synchronization, File import where required: `setIntegrationSource`; Manual synchronization: `startSync`; Integration Monitoring: `listSyncRuns`.",
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
 "createResourceBlock": {
  "method": "POST",
  "path": "/resource-blocks",
  "contract": "resources",
  "summary": "Take a resource out of service for a window, with a reason",
  "permission": "RESOURCE_MANAGE",
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
  "requestBody": "ResourceBlock",
  "responds": "ResourceBlock"
 },
 "getEmployee": {
  "method": "GET",
  "path": "/employees/{employeeId}",
  "contract": "workforce",
  "summary": "One person, with their employment, postings and leave balances",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "employeeId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "WorkforceEmployeeProfile"
 },
 "getFieldOwnership": {
  "method": "GET",
  "path": "/integration-sources/{sourceId}/field-ownership",
  "contract": "workforce",
  "summary": "Which fields this source masters",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "sourceId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "WorkforceFieldOwnership"
 },
 "getPrincipal": {
  "method": "GET",
  "path": "/principals/{principalId}",
  "contract": "identity",
  "summary": "Read a principal",
  "permission": "USER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Principal"
 },
 "getResourceSchedule": {
  "method": "GET",
  "path": "/resources/{resourceId}/schedule",
  "contract": "resources",
  "summary": "The pattern of when it is normally available",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceSchedule"
 },
 "listIntegrationSources": {
  "method": "GET",
  "path": "/integration-sources",
  "contract": "workforce",
  "summary": "External systems that master workforce data, and their health",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "WorkforceIntegrationSource"
 },
 "listLeaveBalances": {
  "method": "GET",
  "path": "/leave-balances",
  "contract": "workforce",
  "summary": "What each person has left, by leave type",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "employeeId",
    "in": "query",
    "required": null
   },
   {
    "name": "leaveTypeId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkforceLeaveBalance"
 },
 "listLeaveRequests": {
  "method": "GET",
  "path": "/leave-requests",
  "contract": "workforce",
  "summary": "Leave, absence and their effect on cover",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "LeaveRequest"
 },
 "listLeaveTypes": {
  "method": "GET",
  "path": "/leave-types",
  "contract": "workforce",
  "summary": "Leave types and how each accrues",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WorkforceLeaveType"
 },
 "listPrincipals": {
  "method": "GET",
  "path": "/principals",
  "contract": "identity",
  "summary": "List principals",
  "permission": "USER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "isActive",
    "in": "query",
    "required": null
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
 "listResources": {
  "method": "GET",
  "path": "/resources",
  "contract": "resources",
  "summary": "Resources at this venue",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "availableFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "availableTo",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Resource"
 },
 "listRotaAssignments": {
  "method": "GET",
  "path": "/rota-assignments",
  "contract": "workforce",
  "summary": "The rota",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "departmentId",
    "in": "query",
    "required": null
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
 "listShiftPatterns": {
  "method": "GET",
  "path": "/shift-patterns",
  "contract": "workforce",
  "summary": "Named shift patterns",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WorkforceShift"
 },
 "listShiftTemplates": {
  "method": "GET",
  "path": "/shift-templates",
  "contract": "workforce",
  "summary": "Named shift patterns a rota is built from",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ShiftTemplate"
 },
 "listSyncConflicts": {
  "method": "GET",
  "path": "/sync-conflicts",
  "contract": "workforce",
  "summary": "Disagreements a person has to settle",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "sourceId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
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
 "listSyncRuns": {
  "method": "GET",
  "path": "/sync-runs",
  "contract": "workforce",
  "summary": "Synchronisation history, with counts",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "sourceId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
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
 "requestLeave": {
  "method": "POST",
  "path": "/leave-requests",
  "contract": "workforce",
  "summary": "Ask for time off, against the cover it would cost",
  "permission": "WORKFORCE_VIEW",
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
  "requestBody": "LeaveRequest",
  "responds": "LeaveRequest"
 },
 "resolveSyncConflict": {
  "method": "POST",
  "path": "/sync-conflicts",
  "contract": "workforce",
  "summary": "Settle a disagreement",
  "permission": "WORKFORCE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ResolveSyncConflictRequest",
  "responds": "WorkforceSyncConflict"
 },
 "setExperienceResourceRequirements": {
  "method": "PUT",
  "path": "/experiences/{experienceId}/resource-requirements",
  "contract": "resources",
  "summary": "Bind resource requirements to an experience",
  "permission": "RESOURCE_CONFIGURE",
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
  "responds": "ResourceRequirement"
 },
 "setFieldOwnership": {
  "method": "PUT",
  "path": "/integration-sources/{sourceId}/field-ownership",
  "contract": "workforce",
  "summary": "Declare who masters each field",
  "permission": "WORKFORCE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "sourceId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "WorkforceFieldOwnership",
  "responds": "WorkforceFieldOwnership"
 },
 "setIntegrationSource": {
  "method": "PUT",
  "path": "/integration-sources",
  "contract": "workforce",
  "summary": "Connect or reconfigure an external workforce system",
  "permission": "WORKFORCE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "WorkforceIntegrationSource",
  "responds": "WorkforceIntegrationSource"
 },
 "setLeaveType": {
  "method": "PUT",
  "path": "/leave-types",
  "contract": "workforce",
  "summary": "Define a leave type",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "WorkforceLeaveType",
  "responds": "WorkforceLeaveType"
 },
 "setResourceQualifications": {
  "method": "PUT",
  "path": "/resources/{resourceId}/qualifications",
  "contract": "resources",
  "summary": "What a person resource is certified to do, and until when",
  "permission": "RESOURCE_MANAGE",
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
  "responds": "Qualification"
 },
 "setResourceSchedule": {
  "method": "PUT",
  "path": "/resources/{resourceId}/schedule",
  "contract": "resources",
  "summary": "Operating hours, working pattern and bookable slots",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourceSchedule",
  "responds": "ResourceSchedule"
 },
 "setShiftPattern": {
  "method": "PUT",
  "path": "/shift-patterns",
  "contract": "workforce",
  "summary": "Define a shift pattern and its break",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "WorkforceShift",
  "responds": "WorkforceShift"
 },
 "setShiftTemplate": {
  "method": "PUT",
  "path": "/shift-templates",
  "contract": "workforce",
  "summary": "Define a shift pattern, its breaks and its qualifications",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "ShiftTemplate",
  "responds": "ShiftTemplate"
 },
 "setStaffingRules": {
  "method": "PUT",
  "path": "/staffing-rules",
  "contract": "workforce",
  "summary": "Minimum cover, working-hour limits and overtime",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "StaffingRules",
  "responds": "StaffingRules"
 },
 "startSync": {
  "method": "POST",
  "path": "/sync-runs",
  "contract": "workforce",
  "summary": "Run a synchronisation now",
  "permission": "WORKFORCE_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "suggestResources": {
  "method": "GET",
  "path": "/resource-suggestions",
  "contract": "resources",
  "summary": "Resources matching a requirement, by attribute",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "resourceTypeId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   },
   {
    "name": "attributes",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Resource"
 },
 "validateWorkforceCompliance": {
  "method": "GET",
  "path": "/workforce-compliance",
  "contract": "workforce",
  "summary": "Where the rota breaks a rule",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WorkforceComplianceFinding"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "LeaveRequest": {
  "type": "object",
  "x-ticvai-persistence": "workforce.leave_request",
  "description": "Resource board 3.8. **Approving leave without seeing the gap is how four supervisors book the same week.**\n",
  "required": [
   "principalId",
   "from",
   "to",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "annual",
     "sick",
     "unpaid",
     "parental",
     "compassionate",
     "training",
     "timeOffInLieu"
    ]
   },
   "from": {
    "type": "string",
    "format": "date"
   },
   "to": {
    "type": "string",
    "format": "date"
   },
   "halfDay": {
    "type": "boolean",
    "default": false
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "requested",
     "approved",
     "rejected",
     "cancelled",
     "taken"
    ]
   },
   "coverageImpact": {
    "type": "array",
    "readOnly": true,
    "items": {
     "$ref": "#/components/schemas/StaffingCoverage"
    }
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
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
 "Principal": {
  "x-ticvai-persistence": "identity.principal",
  "type": "object",
  "required": [
   "id",
   "username",
   "displayName",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "username": {
    "type": "string"
   },
   "displayName": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Past this, resolution returns DENY regardless of grants."
   },
   "primaryRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Determines the landing screen when the principal holds several roles and picks one at login.\n"
   },
   "roles": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RoleSummary"
    }
   },
   "lastLoginAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "Qualification": {
  "type": "object",
  "x-ticvai-persistence": "resources.qualification",
  "description": "1.2.36. **A role is not a skill**, and the check happens before assignment rather than after.\n",
  "required": [
   "code",
   "name"
  ],
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**The resource that holds this qualification.** Set from the path of `setResourceQualifications`; without it a stored qualification belongs to nobody and the check before assignment has nothing to check against. One row per resource and `code`.\n"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "issuedAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "**The field that makes this worth having.** A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one.\n"
   },
   "issuer": {
    "type": "string",
    "nullable": true
   },
   "documentAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ResolveSyncConflictRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — writes sync_conflict",
  "required": [
   "conflictId",
   "resolution"
  ],
  "properties": {
   "conflictId": {
    "type": "string",
    "format": "uuid"
   },
   "resolution": {
    "type": "string",
    "enum": [
     "acceptExternal",
     "keepTicvai",
     "retry",
     "ignore",
     "escalate"
    ]
   },
   "note": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "releaseAffectedAssignments": {
    "type": "boolean",
    "default": false,
    "description": "**For a termination conflict, what happens to the shifts already rostered.** Board 3 requires the downstream consequence to be acted on rather than reported: releasing them puts the shifts back on the marketplace, and leaving them means a manager has decided to cover them another way.\n"
   }
  }
 },
 "Resource": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource",
  "description": "**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId"
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
   "kind": {
    "$ref": "#/components/schemas/ResourceKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "parentResourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true,
    "description": "Configurable per kind — capacity, size, shade, power, poolside."
   },
   "setupMinutes": {
    "type": "integer",
    "default": 0,
    "description": "**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"
   },
   "teardownMinutes": {
    "type": "integer",
    "default": 0,
    "description": "After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"
   },
   "cleaningPolicy": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ResourceCleaningPolicy"
     }
    ],
    "nullable": true,
    "description": "How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."
   },
   "requiresQualification": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Qualification codes a person must hold to be assigned to this."
   },
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "booked",
     "checkedOut",
     "maintenance",
     "retired"
    ]
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ResourceBlock": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_block",
  "description": "Board 2.07. **A block is not a booking**, and the reason travels with it so an operator knows whether to wait or to look elsewhere.\n",
  "required": [
   "resourceId",
   "from",
   "to",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
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
    "type": "string",
    "enum": [
     "setup",
     "teardown",
     "maintenance",
     "blackout",
     "closed",
     "operational",
     "training"
    ]
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "createdBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceCleaningPolicy": {
  "x-ticvai-persistence": "none — columns on resources.resource",
  "type": "object",
  "description": "**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n",
  "required": [
   "mode",
   "bufferMinutes"
  ],
  "properties": {
   "mode": {
    "type": "string",
    "enum": [
     "afterEveryBooking",
     "timesPerDay"
    ]
   },
   "bufferMinutes": {
    "type": "integer",
    "minimum": 5,
    "maximum": 240,
    "description": "Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."
   },
   "cleaningsPerDay": {
    "type": "integer",
    "minimum": 1,
    "maximum": 24,
    "nullable": true,
    "description": "Required for `timesPerDay`; ignored for `afterEveryBooking`."
   },
   "windowStart": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true,
    "description": "Venue-local time the cleaning window opens. Null means the resource's opening time."
   },
   "windowEnd": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true,
    "description": "Venue-local time the cleaning window closes. Null means the resource's closing time."
   }
  }
 },
 "ResourceKind": {
  "type": "string",
  "description": "BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n",
  "enum": [
   "cabana",
   "lounger",
   "locker",
   "wheelchair",
   "stroller",
   "equipment",
   "room",
   "auditorium",
   "vehicle",
   "instructor",
   "staff",
   "table",
   "pitch",
   "studio",
   "other"
  ],
  "x-ticvai-refuses": {
   "mealPlan": "**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."
  }
 },
 "ResourceRequirement": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_requirement",
  "description": "**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n",
  "required": [
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceTypeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"
   },
   "quantity": {
    "type": "integer",
    "default": 1
   },
   "mandatory": {
    "type": "boolean",
    "default": true
   },
   "requiredQualifications": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "requiredAttributes": {
    "type": "object",
    "additionalProperties": true
   },
   "substituteResourceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceSchedule": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_schedule",
  "description": "Boards 2.03 and 2.04. **A recurring pattern with exceptions, not a list of dates.** A schedule written as concrete dates silently expires.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "availabilityMode": {
    "type": "string",
    "enum": [
     "alwaysAvailable",
     "scheduled",
     "onRequest"
    ]
   },
   "windows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "from": {
       "type": "string",
       "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
       "description": "Local time of day, HH:MM."
      },
      "to": {
       "type": "string",
       "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
       "description": "Local time of day, HH:MM."
      },
      "effectiveFrom": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "effectiveTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "slotMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "**How finely this resource's time can be cut**, which is a property of the resource and not of the product sold against it.\n"
   },
   "minimumBookingMinutes": {
    "type": "integer",
    "nullable": true
   },
   "maximumBookingMinutes": {
    "type": "integer",
    "nullable": true
   },
   "advanceBookingDays": {
    "type": "integer",
    "nullable": true
   },
   "exceptions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "date": {
       "type": "string",
       "format": "date"
      },
      "closed": {
       "type": "boolean"
      },
      "from": {
       "type": "string",
       "nullable": true,
       "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
       "description": "Local time of day, HH:MM."
      },
      "to": {
       "type": "string",
       "nullable": true,
       "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
       "description": "Local time of day, HH:MM."
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RoleSummary": {
  "x-ticvai-persistence": "none — projection over role",
  "type": "object",
  "required": [
   "id",
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
   "isPrimary": {
    "type": "boolean"
   }
  }
 },
 "RotaAssignment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.rota_assignment",
  "required": [
   "principalId",
   "venueId",
   "startsAt",
   "endsAt",
   "position"
  ],
  "properties": {
   "overtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"
   },
   "restPeriodBefore": {
    "type": "integer",
    "nullable": true,
    "description": "Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"
   },
   "breachesWorkingHourLimit": {
    "type": "boolean",
    "default": false,
    "readOnly": true,
    "description": "**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"
   },
   "labourCost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "position": {
    "type": "string",
    "description": "What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"
   },
   "requiredRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "$ref": "#/components/schemas/RotaStatus"
   },
   "breakMinutes": {
    "type": "integer",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "RotaStatus": {
  "type": "string",
  "enum": [
   "planned",
   "published",
   "confirmed",
   "swapPending",
   "cancelled",
   "completed",
   "noShow"
  ]
 },
 "ShiftTemplate": {
  "type": "object",
  "x-ticvai-persistence": "workforce.shift_template",
  "description": "Resource board 3.7. **The unit a manager actually thinks in.**",
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
   "kind": {
    "type": "string",
    "enum": [
     "early",
     "late",
     "middle",
     "split",
     "double",
     "night",
     "onCall",
     "overtime"
    ]
   },
   "startsAt": {
    "type": "string"
   },
   "endsAt": {
    "type": "string"
   },
   "breaks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "afterMinutes": {
       "type": "integer"
      },
      "minutes": {
       "type": "integer"
      },
      "paid": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "requiredQualifications": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "roleCode": {
    "type": "string",
    "nullable": true
   },
   "costCentre": {
    "type": "string",
    "nullable": true
   },
   "hourlyRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "StaffingCoverage": {
  "type": "object",
  "description": "Resource board 4.4. **The gap is the product.**",
  "properties": {
   "date": {
    "type": "string",
    "format": "date"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "positionCode": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "from": {
    "type": "string"
   },
   "to": {
    "type": "string"
   },
   "required": {
    "type": "integer"
   },
   "rostered": {
    "type": "integer"
   },
   "qualified": {
    "type": "integer",
    "description": "**A position filled by somebody not qualified for it is still a gap.**"
   },
   "gap": {
    "type": "integer"
   },
   "severity": {
    "type": "string",
    "enum": [
     "covered",
     "tight",
     "short",
     "blocking"
    ]
   },
   "openShiftIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "basisApplied": {
    "type": "string",
    "enum": [
     "minimum",
     "forecastRequirement"
    ],
    "description": "Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the period, `minimum`."
   },
   "minimumRequired": {
    "type": "integer",
    "nullable": true,
    "description": "The configured minimum for the position and window."
   },
   "forecastRequired": {
    "type": "number",
    "nullable": true,
    "description": "The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. Null where none was handed over."
   },
   "forecastRequiredP90": {
    "type": "number",
    "nullable": true,
    "description": "The busy-case requirement, for planning to the busy case."
   },
   "forecastVersionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it."
   }
  }
 },
 "StaffingRules": {
  "type": "object",
  "x-ticvai-persistence": "workforce.staffing_rules + workforce.position_requirement",
  "description": "Resource board 4.3. **A safety rule before it is a cost rule.**",
  "properties": {
   "minimumCover": {
    "type": "array",
    "description": "**Minimum staffing per position, venue and time window, with the qualifications it requires**: the rows of `workforce.position_requirement` (data model for the agreed operations, 29 September). `getStaffingCoverage` measures the rota against them; before this they were an array with no table, so no minimum was stored.",
    "items": {
     "type": "object",
     "required": [
      "id",
      "positionCode",
      "minimumHeadcount"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "positionCode": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "venueId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "attractionId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "minimumHeadcount": {
       "type": "integer",
       "minimum": 0
      },
      "daysOfWeek": {
       "type": "array",
       "nullable": true,
       "description": "Days the minimum applies; absent means every day the venue is open",
       "items": {
        "type": "string",
        "enum": [
         "monday",
         "tuesday",
         "wednesday",
         "thursday",
         "friday",
         "saturday",
         "sunday"
        ]
       }
      },
      "startsAt": {
       "type": "string",
       "nullable": true,
       "description": "Start of the time window, local time (HH:MM) as `ShiftTemplate.startsAt`; absent means opening"
      },
      "endsAt": {
       "type": "string",
       "nullable": true,
       "description": "End of the time window, local time (HH:MM); absent means closing"
      },
      "requiredQualifications": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "appliesWhenOpen": {
       "type": "boolean",
       "default": true
      },
      "blocksOperation": {
       "type": "boolean",
       "default": true,
       "description": "**A ride requiring two operators cannot run with one.** Where this is true the attraction closes rather than running short.\n"
      }
     }
    }
   },
   "maximumHoursPerDay": {
    "type": "integer",
    "nullable": true
   },
   "maximumHoursPerWeek": {
    "type": "integer",
    "nullable": true
   },
   "minimumRestHours": {
    "type": "integer",
    "nullable": true
   },
   "maximumConsecutiveDays": {
    "type": "integer",
    "nullable": true
   },
   "overtime": {
    "type": "object",
    "properties": {
     "allowed": {
      "type": "boolean",
      "default": true
     },
     "afterHoursPerWeek": {
      "type": "integer",
      "nullable": true
     },
     "rateMultiplier": {
      "type": "number",
      "nullable": true
     },
     "requiresApproval": {
      "type": "boolean",
      "default": true
     }
    }
   },
   "minimumAgeForNightShift": {
    "type": "integer",
    "nullable": true
   },
   "defaultIncentiveRateMultiplier": {
    "type": "number",
    "nullable": true,
    "minimum": 1,
    "description": "**What an open shift pays above base when it is released.** Added 22 September: `workforce.open_shift.incentive_rate_multiplier` was set per shift with nothing behind it, so two identical shifts could price differently and record no reason. The shift still carries its own value — **as the snapshot**, the rule-and-record split `payments.fee_rule` and `orders.order_fee` use — and this is where it comes from.\n**Top-level rather than beside `overtime`** so the value is its own column. Nested in an object it would be a key inside a JSON blob, which nothing can index, constrain or pair to the shift that uses it.\n"
   },
   "maximumIncentiveRateMultiplier": {
    "type": "number",
    "nullable": true,
    "minimum": 1,
    "description": "**The ceiling on an incentive.** A shift nobody claims is the moment somebody raises the multiplier in a hurry — the same reason `maximumDailyCharge` bounds a late fee."
   },
   "incentiveApprovalAbove": {
    "type": "number",
    "nullable": true,
    "minimum": 1,
    "description": "**Above this multiplier a second person approves the release.** Routed as an approval, not a boolean — `overtime.requiresApproval` beside it is one of 26 approval flags across the contracts that no approval kind, matrix row or SLA reaches."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WorkforceComplianceFinding": {
  "type": "object",
  "description": "Resource board 4.8. **Checked before the rota is published, not in an inspection.**",
  "properties": {
   "code": {
    "type": "string",
    "enum": [
     "expiredQualification",
     "missingQualification",
     "exceededDailyHours",
     "exceededWeeklyHours",
     "insufficientRest",
     "missedBreak",
     "consecutiveDaysExceeded",
     "underAgeNightShift",
     "belowMinimumCover"
    ]
   },
   "severity": {
    "type": "string",
    "enum": [
     "breach",
     "warning"
    ]
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "principalName": {
    "type": "string",
    "nullable": true
   },
   "date": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "detail": {
    "type": "string"
   },
   "rotaAssignmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "WorkforceEmployee": {
  "type": "object",
  "x-ticvai-persistence": "workforce.employee",
  "description": "**Taken from the backend workbook, 20 September.** Stores the main employee/staff master record.",
  "required": [
   "tenantId",
   "code",
   "firstName",
   "lastName",
   "dateOfJoining",
   "employmentType",
   "employmentStatus",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "code": {
    "type": "string",
    "maxLength": 50
   },
   "firstName": {
    "type": "string",
    "maxLength": 100
   },
   "lastName": {
    "type": "string",
    "maxLength": 100
   },
   "email": {
    "type": "string",
    "maxLength": 254,
    "nullable": true
   },
   "mobile": {
    "type": "string",
    "maxLength": 30,
    "nullable": true
   },
   "dateOfJoining": {
    "type": "string",
    "format": "date"
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "**What the under-age check needs** (data model for the agreed operations, 29 September): `validateWorkforceCompliance` reports `underAgeNightShift` against `StaffingRules.minimumAgeForNightShift`, and that rule has nothing to compare with unless the employee's age is on file. **An employee with no date of birth is reported as a warning**, not assumed to be of age."
   },
   "employmentType": {
    "type": "string",
    "maxLength": 30
   },
   "employmentStatus": {
    "type": "string",
    "maxLength": 30
   },
   "managerEmployeeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkforceEmployeeProfile": {
  "type": "object",
  "x-ticvai-persistence": "none — composed from employee and four related tables",
  "description": "**One person and everything a profile screen asks about them.** The employment record, the postings and the leave balances are separate tables and one question, so fanning out across four endpoints is four round trips and four chances to render a half-loaded person.\n",
  "required": [
   "employee"
  ],
  "properties": {
   "employee": {
    "$ref": "#/components/schemas/WorkforceEmployee"
   },
   "employments": {
    "type": "array",
    "description": "Most recent first. **More than one is normal** — a seasonal worker rehired each summer has several, and collapsing them to the current one loses the service history that leave accrual is calculated from.\n",
    "items": {
     "$ref": "#/components/schemas/WorkforceEmployment"
    }
   },
   "assignments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/WorkforceWorkAssignment"
    }
   },
   "leaveBalances": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/WorkforceLeaveBalance"
    }
   },
   "jobTitles": {
    "type": "array",
    "description": "The titles the postings name, so a client does not have to resolve them one by one.\n",
    "items": {
     "$ref": "#/components/schemas/WorkforceJobTitle"
    }
   },
   "externallyMasteredFields": {
    "type": "array",
    "description": "**Which fields on this record the venue may not edit**, resolved from `field_ownership` for whichever source masters this employee. A screen that shows an editable input over a field the HRMS owns has promised something it cannot keep.\n",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "WorkforceEmployment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.employment",
  "description": "**Taken from the backend workbook, 20 September.** Stores employment terms and contract validity.",
  "required": [
   "employeeId",
   "contractType",
   "startDate",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "employeeId": {
    "type": "string",
    "format": "uuid"
   },
   "contractType": {
    "type": "string",
    "maxLength": 30
   },
   "startDate": {
    "type": "string",
    "format": "date"
   },
   "endDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "standardHoursPerWeek": {
    "type": "number",
    "nullable": true
   },
   "probationEndDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "status": {
    "type": "string",
    "maxLength": 30
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WorkforceFieldOwnership": {
  "type": "object",
  "x-ticvai-persistence": "workforce.field_ownership",
  "description": "**Which system owns a field, which is what prevents conflicting updates.** Board 3: *\"For every field, administrators shall determine ... External System Master.\"* Without this, an employee record mastered in HRMS and edited here disagrees with its source and nothing can say which answer is right.\nOne row per table and column. Absent means ours, so nothing has to be enumerated before it is decided.\n",
  "required": [
   "tableName",
   "columnName",
   "master"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tableName": {
    "type": "string",
    "maxLength": 120
   },
   "columnName": {
    "type": "string",
    "maxLength": 120
   },
   "master": {
    "type": "string",
    "enum": [
     "ticvai",
     "external"
    ]
   },
   "sourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The integration source that masters it, when `master` is `external`."
   },
   "onConflict": {
    "type": "string",
    "enum": [
     "externalWins",
     "ticvaiWins",
     "flagForReview"
    ]
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "WorkforceIntegrationSource": {
  "type": "object",
  "x-ticvai-persistence": "workforce.integration_source",
  "description": "**An external system that masters some of our workforce data.** Board 3 names HRMS, Workforce Management, Payroll, Time & Attendance, Identity Management and external staffing agencies. The six-state display Board 10 asks for lives on this row: what is connected, when it last synchronised, and whether its credentials still work.\n",
  "required": [
   "code",
   "name",
   "kind",
   "transport",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 60
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "kind": {
    "type": "string",
    "enum": [
     "hrms",
     "workforceManagement",
     "payroll",
     "timeAndAttendance",
     "identity",
     "staffingAgency"
    ]
   },
   "transport": {
    "type": "string",
    "enum": [
     "api",
     "webhook",
     "scheduled",
     "manual",
     "fileImport"
    ],
    "description": "Board 3, Support. **`manual` and `fileImport` are in the list on purpose** — a staffing agency that sends a spreadsheet is still a system of record, and modelling only the API cases would leave the messiest source unmanaged.\n"
   },
   "authenticationStatus": {
    "type": "string",
    "enum": [
     "healthy",
     "expiring",
     "expired",
     "failed",
     "notConfigured"
    ]
   },
   "lastSynchronisedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "degraded",
     "suspended"
    ]
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "WorkforceJobTitle": {
  "type": "object",
  "x-ticvai-persistence": "workforce.job_title",
  "description": "**Taken from the backend workbook, 20 September.** Stores job/designation definitions such as Cashier, Manager, Chef or Technician.",
  "required": [
   "tenantId",
   "code",
   "name",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 50
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "description": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkforceLeaveBalance": {
  "type": "object",
  "x-ticvai-persistence": "workforce.leave_balance",
  "description": "**Taken from the backend workbook, 20 September.** Stores leave entitlement, used amount and remaining balance per employee/period.",
  "required": [
   "employeeId",
   "typeId",
   "periodYear",
   "entitledDays",
   "usedDays",
   "pendingDays",
   "availableDays",
   "updatedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "employeeId": {
    "type": "string",
    "format": "uuid"
   },
   "typeId": {
    "type": "string",
    "format": "uuid"
   },
   "periodYear": {
    "type": "integer"
   },
   "entitledDays": {
    "type": "number"
   },
   "usedDays": {
    "type": "number"
   },
   "pendingDays": {
    "type": "number"
   },
   "availableDays": {
    "type": "number"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WorkforceLeaveType": {
  "type": "object",
  "x-ticvai-persistence": "workforce.leave_type",
  "description": "**Taken from the backend workbook, 20 September.** Defines leave categories and basic leave behavior.",
  "required": [
   "tenantId",
   "code",
   "name",
   "isPaid",
   "requiresApproval",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 50
   },
   "name": {
    "type": "string",
    "maxLength": 100
   },
   "isPaid": {
    "type": "boolean"
   },
   "requiresApproval": {
    "type": "boolean"
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WorkforceShift": {
  "type": "object",
  "x-ticvai-persistence": "workforce.shift",
  "description": "**Taken from the backend workbook, 20 September.** Defines reusable shifts such as Morning, Evening or Night.",
  "required": [
   "tenantId",
   "code",
   "name",
   "startTime",
   "endTime",
   "breakMinutes",
   "crossesMidnight",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 50
   },
   "name": {
    "type": "string",
    "maxLength": 100
   },
   "startTime": {
    "type": "string",
    "maxLength": 0
   },
   "endTime": {
    "type": "string",
    "maxLength": 0
   },
   "breakMinutes": {
    "type": "integer"
   },
   "crossesMidnight": {
    "type": "boolean"
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WorkforceSyncConflict": {
  "type": "object",
  "x-ticvai-persistence": "workforce.sync_conflict",
  "description": "**A disagreement a person has to settle, and the assignments it puts at risk.** Board 3 lists the cases by name: an employee in HR and not here, a venue changed externally, a certification expired, and *\"employee terminated externally but has future TICVAI assignments\"* — where *\"the system shall flag affected downstream assignments\"*.\n`affectedAssignmentIds` is deliberately an array and deliberately an exception: it is a snapshot of what was at risk when the conflict was raised, not a live relationship, and it must not change when a roster does.\n",
  "required": [
   "sourceId",
   "kind",
   "status",
   "raisedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "sourceId": {
    "type": "string",
    "format": "uuid"
   },
   "syncRunId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "missingInTicvai",
     "missingExternally",
     "venueChangedExternally",
     "certificationExpired",
     "terminatedExternally",
     "fieldDisagreement"
    ]
   },
   "employeeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "externalReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "detail": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "affectedAssignmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "retried",
     "reprocessed",
     "escalated",
     "resolved",
     "ignored"
    ]
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "resolvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "WorkforceSyncRun": {
  "type": "object",
  "x-ticvai-persistence": "workforce.sync_run",
  "description": "**One synchronisation, and what it did.** Board 10 asks the page to show successful records, failed records, warnings and mapping errors rather than *\"integration failed\"* — and to say the operational consequence: *\"12 employee availability updates could not be synchronised. Four employees have assignments within the next 24 hours.\"* That sentence needs counts on a row, not a log line.\n",
  "required": [
   "sourceId",
   "startedAt",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "sourceId": {
    "type": "string",
    "format": "uuid"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "finishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "running",
     "succeeded",
     "partial",
     "failed"
    ]
   },
   "recordsRead": {
    "type": "integer"
   },
   "recordsApplied": {
    "type": "integer"
   },
   "recordsFailed": {
    "type": "integer"
   },
   "warningCount": {
    "type": "integer"
   },
   "mappingErrorCount": {
    "type": "integer"
   },
   "trigger": {
    "type": "string",
    "enum": [
     "scheduled",
     "manual",
     "webhook",
     "fileImport"
    ]
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "WorkforceWorkAssignment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.work_assignment",
  "description": "**Taken from the backend workbook, 20 September.** Assigns an employee to a job and operational location/scope for an effective period.",
  "required": [
   "employeeId",
   "jobTitleId",
   "effectiveFrom",
   "isPrimary",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "employeeId": {
    "type": "string",
    "format": "uuid"
   },
   "jobTitleId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "isPrimary": {
    "type": "boolean"
   },
   "status": {
    "type": "string",
    "maxLength": 30
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 }
}
```
