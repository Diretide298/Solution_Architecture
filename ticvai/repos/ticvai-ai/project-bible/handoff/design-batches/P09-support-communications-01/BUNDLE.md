# P09-support-communications-01 — P09 · Support & Communications

**2 screens · 4 operations · 3 schemas · 4 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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
  `ANNOUNCEMENT_PUBLISH, PLATFORM_RELEASE_MANAGE, PLATFORM_RELEASE_VIEW, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-035` | Support & Escalation Console | listDetail | 2 | 1 | — |
| `ADM-036` | Platform Notification Broadcast | listDetail | 4 | 2 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-035",
  "name": "Support & Escalation Console",
  "module": "Support & Communications",
  "requiresModule": "core",
  "wave": 3,
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/support-and-escalation-console",
   "component": "apps/ticvai-web/src/routes/general/SupportAndEscalationConsoleDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-035 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-035 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "No contract — overlaps P12"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Answer a question without needing a person.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every support notice",
       "bindsTo": "SupportNotice",
       "columns": [
        "SupportNotice.id",
        "SupportNotice.supportEndsAt",
        "SupportNotice.message",
        "SupportNotice.affectedTenantIds",
        "SupportNotice.publishedByPrincipalId",
        "SupportNotice.publishedAt",
        "SupportNotice.scopePath"
       ],
       "operation": "listSupportNotices",
       "provenance": "contract platform-ops.yaml GET /support-notices"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishSupportNotice",
       "notes": "Declares `publishSupportNotice`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected support notice",
       "bindsTo": "SupportNotice",
       "columns": [
        "SupportNotice.id",
        "SupportNotice.supportEndsAt",
        "SupportNotice.message",
        "SupportNotice.affectedTenantIds",
        "SupportNotice.publishedByPrincipalId",
        "SupportNotice.publishedAt",
        "SupportNotice.scopePath"
       ],
       "operation": "listSupportNotices",
       "provenance": "contract platform-ops.yaml GET /support-notices"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish support notice",
       "operation": "publishSupportNotice",
       "provenance": "contract platform-ops.yaml POST /support-notices"
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
   "loading": "The support escalation console list.",
   "error": "Could not load. Names which read failed and leaves the support escalation console untouched.",
   "emptyFirstRun": "No support escalation console yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listSupportNotices` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSupportNotices",
    "contract": "platform-ops",
    "purpose": "End-of-support notices",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishSupportNotice",
    "contract": "platform-ops",
    "purpose": "Publish an end-of-support notice",
    "trigger": "onAction",
    "invalidates": [
     "listSupportNotices"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "SupportNotice.id",
    "SupportNotice.supportEndsAt",
    "SupportNotice.message",
    "SupportNotice.affectedTenantIds",
    "SupportNotice.publishedByPrincipalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-035"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPublishSupportNotice",
    "component": "modal",
    "trigger": "Publish support notice",
    "body": "**Collects what `publishSupportNotice` sends before it is called.** Required: `id`, `supportEndsAt`, `publishedAt`. Optional: `message`, `affectedTenantIds`, `publishedByPrincipalId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SupportNotice",
    "confirm": {
     "label": "Publish support notice",
     "operation": "publishSupportNotice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "supportEndsAt",
      "publishedAt",
      "message",
      "affectedTenantIds",
      "publishedByPrincipalId",
      "scopePath"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /support-notices"
   }
  ],
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-036",
  "name": "Platform Notification Broadcast",
  "module": "Support & Communications",
  "requiresModule": "core",
  "wave": 3,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/platform-notification-broadcast",
   "component": "apps/ticvai-web/src/routes/general/PlatformNotificationBroadcastForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-036 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-036 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "No contract — not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Push live platform notification broadcast for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every support notice",
       "bindsTo": "SupportNotice",
       "columns": [
        "SupportNotice.id",
        "SupportNotice.supportEndsAt",
        "SupportNotice.message",
        "SupportNotice.affectedTenantIds",
        "SupportNotice.publishedByPrincipalId",
        "SupportNotice.publishedAt",
        "SupportNotice.scopePath"
       ],
       "operation": "listSupportNotices",
       "provenance": "contract platform-ops.yaml GET /support-notices"
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
       "impliedBy": "publishSupportNotice",
       "notes": "Declares `publishSupportNotice`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected support notice",
       "bindsTo": "SupportNotice",
       "columns": [
        "SupportNotice.id",
        "SupportNotice.supportEndsAt",
        "SupportNotice.message",
        "SupportNotice.affectedTenantIds",
        "SupportNotice.publishedByPrincipalId",
        "SupportNotice.publishedAt",
        "SupportNotice.scopePath"
       ],
       "operation": "listSupportNotices",
       "provenance": "contract platform-ops.yaml GET /support-notices"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish support notice",
       "operation": "publishSupportNotice",
       "provenance": "contract platform-ops.yaml POST /support-notices"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish announcement",
       "operation": "publishAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements"
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
   "loading": "The platform notification broadcast list.",
   "error": "Could not load. Names which read failed and leaves the platform notification broadcast untouched.",
   "emptyFirstRun": "No platform notification broadcast yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listSupportNotices` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishSupportNotice",
    "contract": "platform-ops",
    "purpose": "Publish an end-of-support notice",
    "trigger": "onAction",
    "invalidates": [
     "listSupportNotices"
    ]
   },
   {
    "operationId": "listSupportNotices",
    "contract": "platform-ops",
    "purpose": "End-of-support notices",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAnnouncements",
    "contract": "workforce",
    "purpose": "What has been broadcast",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishAnnouncement",
    "contract": "workforce",
    "purpose": "Broadcast to the platform",
    "trigger": "onAction",
    "invalidates": [
     "listSupportNotices"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "SupportNotice.id",
    "SupportNotice.supportEndsAt",
    "SupportNotice.message",
    "SupportNotice.affectedTenantIds",
    "SupportNotice.publishedByPrincipalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-036"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPublishSupportNotice",
    "component": "modal",
    "trigger": "Publish support notice",
    "body": "**Collects what `publishSupportNotice` sends before it is called.** Required: `id`, `supportEndsAt`, `publishedAt`. Optional: `message`, `affectedTenantIds`, `publishedByPrincipalId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SupportNotice",
    "confirm": {
     "label": "Publish support notice",
     "operation": "publishSupportNotice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "supportEndsAt",
      "publishedAt",
      "message",
      "affectedTenantIds",
      "publishedByPrincipalId",
      "scopePath"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /support-notices"
   },
   {
    "id": "formPublishAnnouncement",
    "component": "modal",
    "trigger": "Publish announcement",
    "body": "**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. Dismissing sends nothing; the screen behind is unchanged.",
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
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
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
 "listSupportNotices": {
  "method": "GET",
  "path": "/support-notices",
  "contract": "platform-ops",
  "summary": "End-of-support notices",
  "permission": "PLATFORM_RELEASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SupportNotice"
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
 "publishSupportNotice": {
  "method": "POST",
  "path": "/support-notices",
  "contract": "platform-ops",
  "summary": "Publish an end-of-support notice",
  "permission": "PLATFORM_RELEASE_MANAGE",
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
  "requestBody": "SupportNotice",
  "responds": "SupportNotice"
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
 "SupportNotice": {
  "type": "object",
  "x-ticvai-persistence": "control.support_notice",
  "required": [
   "id",
   "version",
   "supportEndsAt",
   "publishedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "string"
   },
   "supportEndsAt": {
    "type": "string",
    "format": "date"
   },
   "message": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "affectedTenantIds": {
    "type": "array",
    "readOnly": true,
    "description": "Computed from cell versions, never typed. A notice to the wrong list is worse than none.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 }
}
```
