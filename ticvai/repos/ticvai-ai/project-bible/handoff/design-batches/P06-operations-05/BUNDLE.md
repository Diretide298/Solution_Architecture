# P06-operations-05 — P06 · Operations (5 of 5)

**6 screens · 15 operations · 26 schemas · 9 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `ACCESS_VALIDATE, ANNOUNCEMENT_PUBLISH, INCIDENT_MANAGE, INCIDENT_VIEW, INSPECTION_MANAGE, INSPECTION_SUBMIT, INSPECTION_VIEW, REPORT_VIEW_VENUE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **5 of these operations work offline**: acknowledgeAnnouncement, listAnnouncements, listInspectionTemplates, logout, submitInspection
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-048` | Opening checklist | listDetail | 4 | 2 | — |
| `EMP-047` | Emergency mode | listDetail | 4 | 1 | — |
| `EMP-050` | Post-incident restore | listDetail | 4 | 2 | — |
| `EMP-045` | Arabic / RTL | listDetail | 0 | 0 | — |
| `EMP-046` | Sign out | configEditor | 1 | 0 | — |
| `EMP-049` | Hand over the journal | listDetail | 2 | 1 | — |

## Thin screens in this batch

**EMP-045, EMP-046 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-048",
  "name": "Opening checklist",
  "module": "Operations",
  "requiresModule": "maintenance",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/opening-checklist",
   "component": "apps/venue-staff-app/src/routes/operations/OpeningChecklistDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Sees the home screen on duty",
     "provenance": "flow F08 step 3→4, F64 step 3→4"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-048 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-048 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listInspectionTemplates` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Confirm a gate is fit to open before the first guest reaches it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every inspection template",
       "bindsTo": "InspectionTemplate",
       "columns": [
        "InspectionTemplate.id",
        "InspectionTemplate.code",
        "InspectionTemplate.name",
        "InspectionTemplate.venueId",
        "InspectionTemplate.appliesToAssetCategoryId",
        "InspectionTemplate.frequency",
        "InspectionTemplate.items",
        "InspectionTemplate.retentionYears",
        "InspectionTemplate.isActive"
       ],
       "operation": "listInspectionTemplates",
       "provenance": "contract maintenance.yaml GET /inspection-templates"
      },
      {
       "kind": "dataTable",
       "label": "Every inspection",
       "bindsTo": "Inspection",
       "columns": [
        "Inspection.id",
        "Inspection.templateId",
        "Inspection.templateName",
        "Inspection.venueId",
        "Inspection.assetId",
        "Inspection.outcome",
        "Inspection.failedItemCount",
        "Inspection.failedSafetyCriticalCount",
        "Inspection.performedByPrincipalId",
        "Inspection.performedAt",
        "Inspection.recordedAt",
        "Inspection.syncedAt"
       ],
       "operation": "listInspections",
       "provenance": "contract maintenance.yaml GET /inspections"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected inspection template",
       "bindsTo": "InspectionTemplate",
       "columns": [
        "InspectionTemplate.id",
        "InspectionTemplate.code",
        "InspectionTemplate.name",
        "InspectionTemplate.venueId",
        "InspectionTemplate.appliesToAssetCategoryId",
        "InspectionTemplate.frequency",
        "InspectionTemplate.items",
        "InspectionTemplate.retentionYears",
        "InspectionTemplate.isActive"
       ],
       "operation": "listInspectionTemplates",
       "provenance": "contract maintenance.yaml GET /inspection-templates"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Submit inspection",
       "operation": "submitInspection",
       "provenance": "contract maintenance.yaml POST /inspections"
      },
      {
       "kind": "secondaryButton",
       "label": "Create inspection template",
       "operation": "createInspectionTemplate",
       "provenance": "contract maintenance.yaml POST /inspection-templates"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The opening checklist list.",
   "error": "Could not load. Names which read failed and leaves the opening checklist untouched.",
   "emptyFirstRun": "No opening checklist yet. Offers Submit inspection (`submitInspection`).",
   "emptyNoResults": "Never shown: `listInspectionTemplates` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `INSPECTION_VIEW`, which `listInspectionTemplates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Works from the cached template. Completions queue"
  },
  "apis": [
   {
    "operationId": "listInspectionTemplates",
    "contract": "maintenance",
    "purpose": "List inspection templates",
    "trigger": "onLoad"
   },
   {
    "operationId": "submitInspection",
    "contract": "maintenance",
    "purpose": "Submit a completed inspection",
    "trigger": "onAction",
    "invalidates": [
     "listInspectionTemplates"
    ]
   },
   {
    "operationId": "createInspectionTemplate",
    "contract": "maintenance",
    "purpose": "Create an inspection template",
    "trigger": "onAction",
    "invalidates": [
     "listInspectionTemplates"
    ]
   },
   {
    "operationId": "listInspections",
    "contract": "maintenance",
    "purpose": "List completed inspections",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "InspectionTemplate.id",
    "InspectionTemplate.code",
    "InspectionTemplate.name",
    "InspectionTemplate.venueId",
    "InspectionTemplate.appliesToAssetCategoryId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-048"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSubmitInspection",
    "component": "modal",
    "trigger": "Submit inspection",
    "body": "**Collects what `submitInspection` sends before it is called.** Required: `id`, `templateId`, `venueId`, `responses`, `recordedAt`. Optional: `assetId`, `signatureRef`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SubmitInspectionRequest",
    "confirm": {
     "label": "Submit inspection",
     "operation": "submitInspection"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "templateId",
      "venueId",
      "responses",
      "recordedAt",
      "assetId",
      "signatureRef"
     ]
    },
    "provenance": "contract maintenance.yaml POST /inspections"
   },
   {
    "id": "formCreateInspectionTemplate",
    "component": "modal",
    "trigger": "Create inspection template",
    "body": "**Collects what `createInspectionTemplate` sends before it is called.** Required: `id`, `code`, `name`, `items`. Optional: `instructions`, `venueId`, `appliesToAssetCategoryId`, `frequency`, `retentionYears`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "InspectionTemplate",
    "confirm": {
     "label": "Create inspection template",
     "operation": "createInspectionTemplate"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "items",
      "instructions",
      "venueId",
      "appliesToAssetCategoryId",
      "frequency",
      "retentionYears",
      "isActive"
     ]
    },
    "provenance": "contract maintenance.yaml POST /inspection-templates"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-047",
  "name": "Emergency mode",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/emergency-mode",
   "component": "apps/venue-staff-app/src/routes/operations/EmergencyModeDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-050"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003",
    "EMP-050"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-047 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-047 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-047 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    },
    {
     "to": "EMP-050",
     "trigger": "Post-incident restore",
     "provenance": "derived — EMP-050 declares entryState.params incidentId and EMP-047 holds none of them, so the edge carries nothing and EMP-050 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act",
  "purpose": "Evacuate, and stop pretending to be a ticketing app.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "toggle",
       "label": "Unacknowledged only",
       "operation": "listAnnouncements",
       "notes": "Sends `?unacknowledgedOnly=` to `listAnnouncements`.",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "dataTable",
       "label": "Every announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishAnnouncement",
       "notes": "Declares `publishAnnouncement`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "detailPanel",
       "label": "The announcement reach",
       "bindsTo": "AnnouncementReach",
       "columns": [
        "AnnouncementReach.announcementId",
        "AnnouncementReach.targeted",
        "AnnouncementReach.delivered",
        "AnnouncementReach.acknowledged",
        "AnnouncementReach.outstanding"
       ],
       "operation": "getAnnouncementReach",
       "provenance": "contract workforce.yaml GET /announcements/{announcementId}/reach"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Acknowledge announcement",
       "operation": "acknowledgeAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements/{announcementId}/acknowledge"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish announcement",
       "operation": "publishAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements",
       "notes": "Kind `emergency` needs ANNOUNCEMENT_EMERGENCY, not ANNOUNCEMENT_PUBLISH; without it the emergency kind is not offered and a publish is refused 403 `emergency-permission-required` (decided 28 September, audit R091 (1))."
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The emergency mode list.",
   "error": "Could not load. Names which read failed and leaves the emergency mode untouched.",
   "emptyFirstRun": "No emergency mode yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on unacknowledgedOnly and the emergency mode are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Fully offline by design"
  },
  "apis": [
   {
    "operationId": "listAnnouncements",
    "contract": "workforce",
    "purpose": "What staff have been told",
    "trigger": "onLoad"
   },
   {
    "operationId": "acknowledgeAnnouncement",
    "contract": "workforce",
    "purpose": "Confirm you have read it",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   },
   {
    "operationId": "getAnnouncementReach",
    "contract": "workforce",
    "purpose": "Who has acknowledged, and who has not",
    "trigger": "onAction"
   },
   {
    "operationId": "publishAnnouncement",
    "contract": "workforce",
    "purpose": "Tell staff something",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "announcementId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `announcementId`.",
   "preloaded": [
    "Announcement.id",
    "Announcement.title",
    "Announcement.body",
    "Announcement.kind",
    "Announcement.venueIds"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-047"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPublishAnnouncement",
    "component": "modal",
    "trigger": "Publish announcement",
    "body": "**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. **An `emergency` kind requires ANNOUNCEMENT_EMERGENCY** (audit R091 (1)). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Announcement",
    "confirm": {
     "label": "Publish announcement",
     "operation": "publishAnnouncement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "body",
      "kind",
      "publishedAt",
      "id",
      "venueIds",
      "departmentIds",
      "roleIds",
      "requiresAcknowledgement",
      "expiresAt",
      "publishedByPrincipalId",
      "locale"
     ]
    },
    "provenance": "contract workforce.yaml POST /announcements"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-050",
  "name": "Post-incident restore",
  "module": "Operations",
  "requiresModule": "maintenance",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/post-incident-restore",
   "component": "apps/venue-staff-app/src/routes/operations/PostIncidentRestoreDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-047"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-027",
    "EMP-047"
   ],
   "notes": "**Reached from EMP-047** — recovery is reached from the emergency it follows. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-047",
     "trigger": "If it is a venue-wide event, an announcement goes out",
     "provenance": "flow F69 step 3→4"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-050 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-050 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "carries": [
      "incidentId"
     ],
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-050 holds incidentId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: reportIncident. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listIncidents` reads the population and `getIncident` reads one of them — list, select, act",
  "purpose": "Put the venue back to how it was.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Severity",
       "operation": "listIncidents",
       "notes": "Sends `?severity=` to `listIncidents`.",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listIncidents",
       "notes": "Sends `?status=` to `listIncidents`.",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "toggle",
       "label": "Is reportable",
       "operation": "listIncidents",
       "notes": "Sends `?isReportable=` to `listIncidents`.",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "dataTable",
       "label": "Every incident",
       "bindsTo": "Incident",
       "columns": [
        "Incident.id",
        "Incident.incidentNumber",
        "Incident.kind",
        "Incident.severity",
        "Incident.status",
        "Incident.venueId",
        "Incident.assetId",
        "Incident.locationDescription",
        "Incident.isReportable",
        "Incident.notificationDueAt",
        "Incident.notifiedAt",
        "Incident.assignedToPrincipalId"
       ],
       "operation": "listIncidents",
       "provenance": "contract maintenance.yaml GET /incidents"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected incident",
       "bindsTo": "Incident",
       "columns": [
        "Incident.id",
        "Incident.incidentNumber",
        "Incident.kind",
        "Incident.severity",
        "Incident.status",
        "Incident.venueId",
        "Incident.assetId",
        "Incident.locationDescription",
        "Incident.isReportable",
        "Incident.notificationDueAt",
        "Incident.notifiedAt",
        "Incident.assignedToPrincipalId",
        "Incident.reportedByPrincipalId",
        "Incident.correctiveWorkOrderId",
        "Incident.occurredAt",
        "Incident.recordedAt"
       ],
       "operation": "listIncidents",
       "provenance": "contract maintenance.yaml GET /incidents"
      },
      {
       "kind": "detailPanel",
       "label": "The incident",
       "bindsTo": "IncidentDetail",
       "columns": [
        "IncidentDetail.id",
        "IncidentDetail.incidentNumber",
        "IncidentDetail.kind",
        "IncidentDetail.severity",
        "IncidentDetail.status",
        "IncidentDetail.venueId",
        "IncidentDetail.assetId",
        "IncidentDetail.locationDescription",
        "IncidentDetail.isReportable",
        "IncidentDetail.notificationDueAt",
        "IncidentDetail.notifiedAt",
        "IncidentDetail.assignedToPrincipalId",
        "IncidentDetail.reportedByPrincipalId",
        "IncidentDetail.correctiveWorkOrderId",
        "IncidentDetail.occurredAt",
        "IncidentDetail.recordedAt"
       ],
       "operation": "getIncident",
       "provenance": "contract maintenance.yaml GET /incidents/{incidentId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Record authority notification",
       "operation": "recordAuthorityNotification",
       "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
      },
      {
       "kind": "secondaryButton",
       "label": "Save incident",
       "operation": "updateIncident",
       "provenance": "contract maintenance.yaml PATCH /incidents/{incidentId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The post-incident restore list.",
   "error": "Could not load. Names which read failed and leaves the post-incident restore untouched.",
   "emptyFirstRun": "No post-incident restore yet. Offers Record authority notification (`recordAuthorityNotification`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on severity, status, isReportable and the post-incident restore are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works offline by design.** Post-incident restore is exactly when the network is worst"
  },
  "apis": [
   {
    "operationId": "listIncidents",
    "contract": "maintenance",
    "purpose": "List incidents",
    "trigger": "onLoad"
   },
   {
    "operationId": "getIncident",
    "contract": "maintenance",
    "purpose": "Read an incident",
    "trigger": "onAction"
   },
   {
    "operationId": "recordAuthorityNotification",
    "contract": "maintenance",
    "purpose": "Record notification to an external authority",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   },
   {
    "operationId": "updateIncident",
    "contract": "maintenance",
    "purpose": "Investigate, escalate or close an incident",
    "trigger": "onAction",
    "invalidates": [
     "listIncidents"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "incidentId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `incidentId`.",
   "preloaded": [
    "Incident.id",
    "Incident.incidentNumber",
    "Incident.kind",
    "Incident.severity",
    "Incident.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-050"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRecordAuthorityNotification",
    "component": "modal",
    "trigger": "Record authority notification",
    "body": "**Collects what `recordAuthorityNotification` sends before it is called.** Required: `authority`, `notifiedAt`. Optional: `reference`, `notifiedByPrincipalId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record authority notification",
     "operation": "recordAuthorityNotification"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "authority",
      "notifiedAt",
      "reference",
      "notifiedByPrincipalId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract maintenance.yaml POST /incidents/{incidentId}/notify-authority"
   },
   {
    "id": "formUpdateIncident",
    "component": "modal",
    "trigger": "Save incident",
    "body": "**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save incident",
     "operation": "updateIncident"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "status",
      "severity",
      "assignedToPrincipalId",
      "investigationNote",
      "rootCause",
      "correctiveActions",
      "correctiveWorkOrderId",
      "attachmentRefs"
     ]
    },
    "provenance": "contract maintenance.yaml PATCH /incidents/{incidentId}"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-045",
  "name": "Arabic / RTL",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/arabic-rtl",
   "component": "apps/venue-staff-app/src/routes/operations/ArabicRtlDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-043"
   ],
   "notes": "**Reached from EMP-043** — language is a device setting. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-045 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-045 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-045 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "**the screen's operations choose no pattern** — no list, no get, no write that groups. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Render the staff app right to left.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen declares no operation the contracts recognise.** Nothing fills it, nothing it does is committed anywhere, and its shape below is a default rather than a reading.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "—",
   "error": "—",
   "emptyFirstRun": "—",
   "offline": "**Fully offline.** Direction is a device setting, not a server one"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-045"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 0 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-046",
  "name": "Sign out",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/sign-out",
   "component": "apps/venue-staff-app/src/routes/operations/SignOutDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-046 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-046 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-046 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`logout`) and no read of a population — it is settings, not a list",
  "purpose": "Leave the shared device safe for the next person.",
  "gaps": [
   {
    "operation": "logout",
    "why": "**`logout` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract identity.yaml POST /auth/logout"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Logout",
       "operation": "logout",
       "provenance": "contract identity.yaml POST /auth/logout"
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
       "impliedBy": "logout"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Closing the session",
   "error": "**Sign-out with a pending journal warns rather than blocks.** A steward handing over a device must not be trapped by a failed sync",
   "emptyFirstRun": "—",
   "offline": "Signs out locally and the journal stays on the device for the next steward"
  },
  "apis": [
   {
    "operationId": "logout",
    "contract": "identity",
    "purpose": "Close the current session",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-046"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-049",
  "name": "Hand over the journal",
  "module": "Operations",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/hand-over-the-journal",
   "component": "apps/venue-staff-app/src/routes/operations/HandOverTheJournalDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-009",
    "EMP-018"
   ],
   "notes": "**Reached from EMP-009** — the journal is handed over at the end of the shift. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-049 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-049 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-049 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listScans` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Move an unsynced journal off a device that is going flat.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Access point id",
       "operation": "listScans",
       "notes": "Sends `?accessPointId=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "textField",
       "label": "Ticket id",
       "operation": "listScans",
       "notes": "Sends `?ticketId=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "textField",
       "label": "Outcome",
       "operation": "listScans",
       "notes": "Sends `?outcome=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "datePicker",
       "label": "Recorded from",
       "operation": "listScans",
       "notes": "Sends `?recordedFrom=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "datePicker",
       "label": "Recorded to",
       "operation": "listScans",
       "notes": "Sends `?recordedTo=` to `listScans`.",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "dataTable",
       "label": "Every scan event",
       "bindsTo": "ScanEvent",
       "columns": [
        "ScanEvent.id",
        "ScanEvent.accessPointId",
        "ScanEvent.venueId",
        "ScanEvent.scopePath",
        "ScanEvent.ticketId",
        "ScanEvent.mediaCode",
        "ScanEvent.outcome",
        "ScanEvent.denyReason",
        "ScanEvent.direction",
        "ScanEvent.operatorPrincipalId",
        "ScanEvent.deviceId",
        "ScanEvent.overridesScanId"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
      },
      {
       "kind": "scanTarget",
       "derived": true,
       "impliedBy": "listScans",
       "notes": "**A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or explain something.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected scan event",
       "bindsTo": "ScanEvent",
       "columns": [
        "ScanEvent.id",
        "ScanEvent.accessPointId",
        "ScanEvent.venueId",
        "ScanEvent.scopePath",
        "ScanEvent.ticketId",
        "ScanEvent.mediaCode",
        "ScanEvent.outcome",
        "ScanEvent.denyReason",
        "ScanEvent.direction",
        "ScanEvent.operatorPrincipalId",
        "ScanEvent.deviceId",
        "ScanEvent.overridesScanId",
        "ScanEvent.overrideReason",
        "ScanEvent.recordedAt",
        "ScanEvent.syncedAt"
       ],
       "operation": "listScans",
       "provenance": "contract access.yaml GET /access/scans"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Sync scans",
       "operation": "syncScans",
       "provenance": "contract access.yaml POST /access/scans"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hand over the list.",
   "error": "Could not load. Names which read failed and leaves the hand over the untouched.",
   "emptyFirstRun": "No hand over the yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the hand over the are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The point of the screen.** It exists because the journal outlives the shift"
  },
  "apis": [
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "List scan events",
    "trigger": "onLoad"
   },
   {
    "operationId": "syncScans",
    "contract": "access",
    "purpose": "Replay scans recorded offline",
    "trigger": "onAction",
    "invalidates": [
     "listScans"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ScanEvent.id",
    "ScanEvent.accessPointId",
    "ScanEvent.venueId",
    "ScanEvent.scopePath",
    "ScanEvent.ticketId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-049"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSyncScans",
    "component": "modal",
    "trigger": "Sync scans",
    "body": "**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sync scans",
     "operation": "syncScans"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "deviceId",
      "scans"
     ]
    },
    "provenance": "contract access.yaml POST /access/scans"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
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
 "acknowledgeAnnouncement": {
  "method": "POST",
  "path": "/announcements/{announcementId}/acknowledge",
  "contract": "workforce",
  "summary": "Confirm you have read it",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
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
 "createInspectionTemplate": {
  "method": "POST",
  "path": "/inspection-templates",
  "contract": "maintenance",
  "summary": "Create an inspection template",
  "permission": "INSPECTION_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "InspectionTemplate",
  "responds": "InspectionTemplate"
 },
 "getAnnouncementReach": {
  "method": "GET",
  "path": "/announcements/{announcementId}/reach",
  "contract": "workforce",
  "summary": "Who has acknowledged, and who has not",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AnnouncementReach"
 },
 "getIncident": {
  "method": "GET",
  "path": "/incidents/{incidentId}",
  "contract": "maintenance",
  "summary": "Read an incident",
  "permission": "INCIDENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "IncidentDetail"
 },
 "listAnnouncements": {
  "method": "GET",
  "path": "/announcements",
  "contract": "workforce",
  "summary": "What staff have been told",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "unacknowledgedOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Announcement"
 },
 "listIncidents": {
  "method": "GET",
  "path": "/incidents",
  "contract": "maintenance",
  "summary": "List incidents",
  "permission": "INCIDENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "severity",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "isReportable",
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
 "listInspectionTemplates": {
  "method": "GET",
  "path": "/inspection-templates",
  "contract": "maintenance",
  "summary": "List inspection templates",
  "permission": "INSPECTION_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "InspectionTemplate"
 },
 "listInspections": {
  "method": "GET",
  "path": "/inspections",
  "contract": "maintenance",
  "summary": "List completed inspections",
  "permission": "INSPECTION_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "templateId",
    "in": "query",
    "required": null
   },
   {
    "name": "assetId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "performedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "performedTo",
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
 "listScans": {
  "method": "GET",
  "path": "/access/scans",
  "contract": "access",
  "summary": "List scan events",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "accessPointId",
    "in": "query",
    "required": null
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedTo",
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
 "logout": {
  "method": "POST",
  "path": "/auth/logout",
  "contract": "identity",
  "summary": "Close the current session",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
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
 "publishAnnouncement": {
  "method": "POST",
  "path": "/announcements",
  "contract": "workforce",
  "summary": "Tell staff something",
  "permission": "ANNOUNCEMENT_PUBLISH",
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
  "requestBody": "Announcement",
  "responds": "Announcement"
 },
 "recordAuthorityNotification": {
  "method": "POST",
  "path": "/incidents/{incidentId}/notify-authority",
  "contract": "maintenance",
  "summary": "Record notification to an external authority",
  "permission": "INCIDENT_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Incident"
 },
 "submitInspection": {
  "method": "POST",
  "path": "/inspections",
  "contract": "maintenance",
  "summary": "Submit a completed inspection",
  "permission": "INSPECTION_SUBMIT",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SubmitInspectionRequest",
  "responds": "InspectionResult"
 },
 "syncScans": {
  "method": "POST",
  "path": "/access/scans",
  "contract": "access",
  "summary": "Replay scans recorded offline",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ScanSyncResult"
 },
 "updateIncident": {
  "method": "PATCH",
  "path": "/incidents/{incidentId}",
  "contract": "maintenance",
  "summary": "Investigate, escalate or close an incident",
  "permission": "INCIDENT_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Incident"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Announcement": {
  "type": "object",
  "x-ticvai-persistence": "workforce.announcement",
  "required": [
   "title",
   "body",
   "kind",
   "publishedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "title": {
    "type": "string",
    "maxLength": 140
   },
   "body": {
    "type": "string",
    "maxLength": 4000
   },
   "kind": {
    "$ref": "#/components/schemas/AnnouncementKind"
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "departmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresAcknowledgement": {
    "type": "boolean"
   },
   "deliveryChannels": {
    "type": "array",
    "description": "How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n",
    "items": {
     "type": "string",
     "enum": [
      "inApp",
      "push"
     ]
    },
    "default": [
     "inApp",
     "push"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "locale": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "AnnouncementKind": {
  "type": "string",
  "description": "`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n",
  "enum": [
   "operational",
   "safety",
   "emergency",
   "hr",
   "celebration"
  ]
 },
 "AnnouncementReach": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from workforce.announcement_receipt",
  "properties": {
   "announcementId": {
    "type": "string",
    "format": "uuid"
   },
   "targeted": {
    "type": "integer"
   },
   "delivered": {
    "type": "integer"
   },
   "acknowledged": {
    "type": "integer"
   },
   "outstanding": {
    "type": "array",
    "description": "**The list that matters.** For an operational notice it measures whether anyone read it; during an emergency it is the roll call.\n",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "onShift": {
       "type": "boolean"
      }
     }
    }
   }
  }
 },
 "DenyReason": {
  "type": "string",
  "description": "Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n",
  "enum": [
   "notFound",
   "notYetValid",
   "expired",
   "alreadyUsed",
   "reentryLimitReached",
   "exitRequiredBeforeReentry",
   "wrongAccessPoint",
   "wrongPerformance",
   "outsideAdmissionWindow",
   "entitlementSuspended",
   "blacklisted",
   "capacityReached",
   "waiverRequired",
   "accompanimentRequired",
   "mediaDeactivated",
   "unpaid",
   "delegatedRightExhausted",
   "delegatedRightRevoked",
   "journeyNotCovered"
  ]
 },
 "Direction": {
  "type": "string",
  "enum": [
   "entry",
   "exit",
   "reentry",
   "crossover"
  ]
 },
 "Incident": {
  "x-ticvai-persistence": "maintenance.incident",
  "type": "object",
  "required": [
   "id",
   "incidentNumber",
   "kind",
   "severity",
   "status",
   "venueId",
   "occurredAt",
   "reportedByPrincipalId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
   },
   "kind": {
    "$ref": "#/components/schemas/IncidentKind"
   },
   "severity": {
    "$ref": "#/components/schemas/IncidentSeverity"
   },
   "status": {
    "$ref": "#/components/schemas/IncidentStatus"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationDescription": {
    "type": "string",
    "nullable": true
   },
   "isReportable": {
    "type": "boolean",
    "description": "Requires notification to an external authority within a statutory window."
   },
   "notificationDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reportedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "correctiveWorkOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "IncidentAuthorityNotification": {
  "x-ticvai-persistence": "maintenance.incident_authority_notification",
  "type": "object",
  "description": "**One notification to an external authority, appended by `recordAuthorityNotification`.** An incident may be reported to more than one authority, or to the same one twice, and each is the evidence that an obligation was met — so each is a row, not an overwrite of `maintenance.incident.notified_at`.\n",
  "required": [
   "id",
   "incidentId",
   "authority",
   "notifiedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentId": {
    "type": "string",
    "format": "uuid"
   },
   "authority": {
    "type": "string",
    "maxLength": 200
   },
   "reference": {
    "type": "string",
    "maxLength": 128,
    "nullable": true
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time"
   },
   "notifiedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "IncidentDetail": {
  "x-ticvai-persistence": "maintenance.incident",
  "allOf": [
   {
    "$ref": "#/components/schemas/Incident"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string",
      "description": "The original report. Never edited — investigation adds to the record."
     },
     "investigationNote": {
      "type": "string",
      "nullable": true,
      "readOnly": true,
      "description": "The latest entry of `investigationNotes`, kept for readers that show one line."
     },
     "investigationNotes": {
      "type": "array",
      "readOnly": true,
      "description": "**Every investigation note, oldest first** (decided 28 September, audit R106 (5)). Read from `maintenance.incident_investigation_note`; appended by `updateIncident`.\n",
      "items": {
       "$ref": "#/components/schemas/IncidentInvestigationNote"
      }
     },
     "rootCause": {
      "type": "string",
      "nullable": true
     },
     "correctiveActions": {
      "type": "string",
      "nullable": true
     },
     "firstAidGiven": {
      "type": "boolean"
     },
     "emergencyServicesCalled": {
      "type": "boolean"
     },
     "witnessCount": {
      "type": "integer"
     },
     "attachmentRefs": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "involvedParties": {
      "type": "array",
      "description": "Who was involved, as given in `ReportIncidentRequest.involvedSubjectIds` and `involvedStaffPrincipalIds`. Read from `maintenance.incident_involved_party`.\n",
      "items": {
       "$ref": "#/components/schemas/IncidentInvolvedParty"
      }
     },
     "authorityNotifications": {
      "type": "array",
      "description": "Read from `maintenance.incident_authority_notification`, oldest first.",
      "items": {
       "$ref": "#/components/schemas/IncidentAuthorityNotification"
      }
     }
    }
   }
  ]
 },
 "IncidentInvestigationNote": {
  "x-ticvai-persistence": "maintenance.incident_investigation_note",
  "type": "object",
  "description": "**One investigation note, appended by `updateIncident`** (decided 28 September, audit R106 (5)). A history rather than a field, so what an investigator thought on Tuesday survives what they found on Thursday.\n",
  "required": [
   "id",
   "incidentId",
   "note",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentId": {
    "type": "string",
    "format": "uuid"
   },
   "note": {
    "type": "string",
    "maxLength": 10000
   },
   "writtenByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "IncidentInvolvedParty": {
  "x-ticvai-persistence": "maintenance.incident_involved_party",
  "type": "object",
  "description": "**One person involved in an incident, by opaque reference.** A guest or member of the public is a `pii.subject` id — personal details live there, the erasable store of ADR-0023, so the incident record survives an erasure request intact. A member of staff is a principal id. Exactly one of the two is set, as `kind` says.\n",
  "required": [
   "id",
   "incidentId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "incidentId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "subject",
     "staff"
    ]
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `pii.subject` id where `kind` is `subject`."
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The staff principal where `kind` is `staff`."
   }
  }
 },
 "IncidentKind": {
  "type": "string",
  "enum": [
   "guestInjury",
   "staffInjury",
   "nearMiss",
   "propertyDamage",
   "equipmentFailure",
   "securityIncident",
   "fireOrEvacuation",
   "foodSafety",
   "environmental",
   "other"
  ]
 },
 "IncidentSeverity": {
  "type": "string",
  "enum": [
   "nearMiss",
   "minor",
   "moderate",
   "major",
   "critical"
  ]
 },
 "IncidentStatus": {
  "type": "string",
  "enum": [
   "reported",
   "underInvestigation",
   "actionRequired",
   "closed"
  ]
 },
 "Inspection": {
  "x-ticvai-persistence": "maintenance.inspection",
  "type": "object",
  "required": [
   "id",
   "templateId",
   "venueId",
   "outcome",
   "performedByPrincipalId",
   "performedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "templateName": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "outcome": {
    "$ref": "#/components/schemas/InspectionOutcome"
   },
   "failedItemCount": {
    "type": "integer"
   },
   "failedSafetyCriticalCount": {
    "type": "integer"
   },
   "performedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "An inspection nobody signed is not an inspection."
   },
   "performedAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "retainUntil": {
    "type": "string",
    "format": "date",
    "nullable": true
   }
  }
 },
 "InspectionItem": {
  "x-ticvai-persistence": "maintenance.inspection_item",
  "type": "object",
  "description": "**One answer to one question, which the API has always accepted and never stored.** `SubmitInspectionRequest.responses[]` takes a key, a value, a pass flag, a note and attachments; the only persistence ever claimed for them was `maintenance.inspection_response`, a table that does not exist.\nSo `maintenance.inspection_template_item` held the questions, `maintenance.inspection` held `failedItemCount` and `failedSafetyCriticalCount`, and **which check failed was accepted over the wire and dropped** — on a record that takes an asset out of service.\nReturned on `InspectionResult`, not on `Inspection`: `listInspections` returns the latter in a list, and twenty item rows per inspection on a list screen is the wrong trade. The counts stay for exactly that reason.\n",
  "required": [
   "id",
   "inspectionId",
   "itemKey"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "inspectionId": {
    "type": "string",
    "format": "uuid"
   },
   "templateItemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Nullable because a template changes and an inspection does not.** An answer recorded against an item that was later removed still has to be readable, so the key below is the durable record and this is the live link.\n"
   },
   "itemKey": {
    "type": "string",
    "maxLength": 120,
    "description": "The template item's `key`, copied at submission and never updated."
   },
   "label": {
    "type": "string",
    "nullable": true,
    "description": "The question as it was asked, copied at submission. **A template reworded next season must not silently reword last season's inspection.**\n"
   },
   "value": {
    "nullable": true,
    "description": "Whatever the item's `kind` calls for — a boolean, a number, a string."
   },
   "passed": {
    "type": "boolean",
    "nullable": true,
    "description": "Null where the item is informational rather than pass or fail."
   },
   "isSafetyCritical": {
    "type": "boolean",
    "default": false,
    "description": "Copied from the template item at submission, for the same reason as `label`: it is what makes `failedSafetyCriticalCount` reproducible, and the template can change.\n"
   },
   "note": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "attachmentAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**A deliberate array, and the same exception as `workforce.sync_conflict.affectedAssignmentIds`**: evidence attached to this answer at the moment it was recorded. It is never queried from the other end — nobody asks which inspection items reference a photograph — and it must not change when an asset library is reorganised.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "InspectionItemKind": {
  "type": "string",
  "enum": [
   "passFail",
   "yesNo",
   "numeric",
   "text",
   "photo",
   "signature"
  ]
 },
 "InspectionOutcome": {
  "type": "string",
  "enum": [
   "passed",
   "passedWithObservations",
   "failed"
  ]
 },
 "InspectionResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "inspection",
   "consequences"
  ],
  "properties": {
   "inspection": {
    "$ref": "#/components/schemas/Inspection"
   },
   "items": {
    "type": "array",
    "description": "**The answers, which had nowhere to live until 20 September.** A failed safety-critical item takes an asset out of service and `consequences` below says it happened; this says which check caused it.\n",
    "items": {
     "$ref": "#/components/schemas/InspectionItem"
    }
   },
   "consequences": {
    "type": "object",
    "description": "What the submission triggered. A failed safety-critical item takes the asset out of service without waiting for anyone to decide.\n",
    "properties": {
     "assetTakenOutOfService": {
      "type": "boolean"
     },
     "workOrdersRaised": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "productsSuspended": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "escalatedToPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   }
  }
 },
 "InspectionTemplate": {
  "x-ticvai-persistence": "maintenance.inspection_template + maintenance.inspection_template_item",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "items"
  ],
  "properties": {
   "instructions": {
    "type": "string",
    "description": "**The procedure itself.** A technician asking how to isolate a chiller is asking a safety question, and the answer has to come from the template rather than from its title.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "appliesToAssetCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "frequency": {
    "type": "string",
    "enum": [
     "preOpening",
     "postClosing",
     "daily",
     "weekly",
     "monthly",
     "annual",
     "adHoc"
    ]
   },
   "items": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "key",
      "label",
      "kind",
      "isRequired"
     ],
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "kind": {
       "$ref": "#/components/schemas/InspectionItemKind"
      },
      "isRequired": {
       "type": "boolean"
      },
      "isSafetyCritical": {
       "type": "boolean",
       "default": false,
       "description": "A failed safety-critical item **blocks the inspection from passing** and cannot be overridden by completing the rest.\n"
      },
      "requiresPhotoOnFail": {
       "type": "boolean",
       "default": true
      },
      "minValue": {
       "type": "number",
       "nullable": true
      },
      "maxValue": {
       "type": "number",
       "nullable": true
      },
      "guidance": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "retentionYears": {
    "type": "integer",
    "default": 7,
    "description": "Compliance inspections are retained alongside the financial trail."
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "OfflineScan": {
  "x-ticvai-persistence": "none — client-side journal",
  "allOf": [
   {
    "$ref": "#/components/schemas/ValidateRequest"
   },
   {
    "type": "object",
    "required": [
     "sequence",
     "localOutcome"
    ],
    "properties": {
     "sequence": {
      "type": "integer",
      "minimum": 1,
      "description": "Monotonic per device. The server processes in this order."
     },
     "localOutcome": {
      "allOf": [
       {
        "$ref": "#/components/schemas/ScanOutcome"
       }
      ],
      "description": "What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"
     },
     "localDenyReason": {
      "$ref": "#/components/schemas/DenyReason"
     },
     "overriddenByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "overrideReason": {
      "type": "string",
      "nullable": true
     }
    }
   }
  ]
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
 "ScanEvent": {
  "x-ticvai-append-only": "recordedAt",
  "x-ticvai-persistence": "access.scan_event",
  "type": "object",
  "required": [
   "id",
   "accessPointId",
   "venueId",
   "outcome",
   "direction",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The scan's client-generated UUIDv7, the key offline replay deduplicates on."
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "ticketId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `Entitlement.id` scanned; null where the media resolved to nothing."
   },
   "mediaCode": {
    "type": "string",
    "nullable": true
   },
   "outcome": {
    "$ref": "#/components/schemas/ScanOutcome"
   },
   "denyReason": {
    "$ref": "#/components/schemas/DenyReason"
   },
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "overridesScanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"
   },
   "overrideReason": {
    "type": "string",
    "nullable": true,
    "description": "The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."
   },
   "dynamicPolicyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."
   },
   "dynamicPolicyVersion": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "The version of that policy in force at the scan, so a report spanning a change counts each version apart."
   },
   "dynamicPolicyResult": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ],
    "nullable": true,
    "description": "What the policy decided, which for a step-up is not the same as the scan's outcome."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."
   },
   "localSequence": {
    "type": "integer",
    "nullable": true,
    "description": "The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."
   },
   "packageVersion": {
    "type": "string",
    "nullable": true,
    "description": "The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null while pending. Differs from recordedAt for offline scans."
   }
  }
 },
 "ScanOutcome": {
  "type": "string",
  "enum": [
   "admitted",
   "denied",
   "overridden"
  ]
 },
 "ScanSyncResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "accepted",
   "results"
  ],
  "properties": {
   "accepted": {
    "type": "integer",
    "description": "Entries processed before any stop."
   },
   "stoppedAtSequence": {
    "type": "integer",
    "nullable": true,
    "description": "Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"
   },
   "results": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "sequence",
      "status"
     ],
     "properties": {
      "id": {
       "type": "string"
      },
      "sequence": {
       "type": "integer"
      },
      "status": {
       "type": "string",
       "enum": [
        "accepted",
        "duplicate",
        "reconciled",
        "rejected"
       ]
      },
      "serverOutcome": {
       "$ref": "#/components/schemas/ScanOutcome"
      },
      "divergence": {
       "type": "string",
       "nullable": true,
       "description": "Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"
      },
      "error": {
       "$ref": "../shared/common.yaml#/components/schemas/Problem"
      }
     }
    }
   }
  }
 },
 "SubmitInspectionRequest": {
  "x-ticvai-persistence": "maintenance.inspection + maintenance.inspection_item",
  "type": "object",
  "required": [
   "id",
   "templateId",
   "venueId",
   "responses",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "responses": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "key",
      "value"
     ],
     "properties": {
      "key": {
       "type": "string"
      },
      "value": {},
      "passed": {
       "type": "boolean",
       "nullable": true
      },
      "note": {
       "type": "string",
       "maxLength": 1000
      },
      "attachmentRefs": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ValidateRequest": {
  "type": "object",
  "required": [
   "id",
   "mediaCode",
   "mediaKind",
   "direction",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7. Also the idempotency key and dedupe key."
   },
   "mediaCode": {
    "type": "string",
    "maxLength": 256,
    "description": "What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"
   },
   "mediaKind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "groupSize": {
    "type": "integer",
    "minimum": 1,
    "description": "For group media admitting several holders on one read."
   },
   "proximityToken": {
    "type": "string",
    "description": "BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time of the read. Authoritative for ordering, not for validity."
   }
  }
 }
}
```
