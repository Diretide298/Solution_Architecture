# P08-people-access-rights-02 — P08 · People & Access Rights (2 of 2)

**2 screens · 4 operations · 4 schemas · 4 permissions**

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
  `AI_CONFIGURE, APPROVAL_VIEW, ROLE_MANAGE, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **2 of these operations work offline**: getVenueSettings, listRoles
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-088` | Approval Analytics | listDetail | 2 | 0 | — |
| `BO-106` | People & Access Rights | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-088 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-088",
  "name": "Approval Analytics",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 3,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/approvals/approval-analytics",
   "component": "apps/venue-management-web/src/routes/approvals/ApprovalAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-084",
    "BO-085",
    "BO-086"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-084",
     "trigger": "Approval Inbox",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — BO-084 declares entryState.params requestId, so an edge into it must carry them"
    },
    {
     "to": "BO-085",
     "trigger": "Approval Request",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — BO-085 declares entryState.params requestId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Retail board operations wired 24 August.**",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listIndexJobs` reads the population and `getApprovalAnalytics` reads one of them — list, select, act",
  "purpose": "Volumes, decision times and where requests get stuck.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every approval analytics",
       "bindsTo": "IndexJob",
       "columns": [
        "IndexJob.id",
        "IndexJob.sourceId",
        "IndexJob.kind",
        "IndexJob.reason",
        "IndexJob.status",
        "IndexJob.recordsTotal",
        "IndexJob.recordsEmbedded",
        "IndexJob.recordsFailed",
        "IndexJob.failureSample",
        "IndexJob.shadowCollection",
        "IndexJob.shardKey",
        "IndexJob.embeddingModel"
       ],
       "operation": "listIndexJobs",
       "provenance": "contract ai.yaml GET /index-jobs"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval analytics",
       "bindsTo": "ApprovalAnalytics",
       "columns": [
        "ApprovalAnalytics.from",
        "ApprovalAnalytics.to",
        "ApprovalAnalytics.groupBy",
        "ApprovalAnalytics.rows"
       ],
       "operation": "getApprovalAnalytics",
       "provenance": "contract approvals.yaml GET /approval-analytics"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval analytics list.",
   "error": "Could not load. Names which read failed and leaves the approval analytics untouched.",
   "emptyFirstRun": "No approval analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Volumes, times, rejections and bottlenecks",
    "trigger": "onLoad"
   },
   {
    "operationId": "listIndexJobs",
    "contract": "ai",
    "purpose": "Indexing in flight and recently finished",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ApprovalAnalytics.from",
    "ApprovalAnalytics.to",
    "ApprovalAnalytics.groupBy",
    "ApprovalAnalytics.rows"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-088"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-106",
  "name": "People & Access Rights",
  "module": "People & Access Rights",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/people-access-rights",
   "component": "apps/venue-management-web/src/routes/home/PeopleAccessRightsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-053",
    "BO-054",
    "BO-055",
    "BO-056",
    "BO-057",
    "BO-066",
    "BO-084",
    "BO-085",
    "BO-086",
    "BO-087",
    "BO-088"
   ],
   "transitions": [
    {
     "to": "BO-053",
     "trigger": "Staff Directory",
     "carries": [
      "principalId"
     ],
     "provenance": "derived — BO-053 declares entryState.params principalId, so an edge into it must carry them"
    },
    {
     "to": "BO-055",
     "trigger": "Rota & Scheduling",
     "carries": [
      "assignmentId"
     ],
     "provenance": "derived — BO-055 declares entryState.params assignmentId, so an edge into it must carry them"
    },
    {
     "to": "BO-056",
     "trigger": "Time & Attendance",
     "carries": [
      "recordId"
     ],
     "provenance": "derived — BO-056 declares entryState.params recordId, so an edge into it must carry them"
    },
    {
     "to": "BO-066",
     "trigger": "Notification Settings",
     "carries": [
      "announcementId"
     ],
     "provenance": "derived — BO-066 declares entryState.params announcementId, so an edge into it must carry them"
    },
    {
     "to": "BO-084",
     "trigger": "Approval Inbox",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — BO-084 declares entryState.params requestId, so an edge into it must carry them"
    },
    {
     "to": "BO-085",
     "trigger": "Approval Request",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — BO-085 declares entryState.params requestId, so an edge into it must carry them"
    },
    {
     "to": "BO-087",
     "trigger": "Approval Delegations",
     "carries": [
      "delegationId"
     ],
     "provenance": "derived — BO-087 declares entryState.params delegationId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Section landing. **11 screens reach the entry point through here** — before 20 August they reached it through nothing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listRoles` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in people & access rights, and what in it needs attention.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every people access rights",
       "bindsTo": "Role",
       "columns": [
        "Role.id",
        "Role.code",
        "Role.name",
        "Role.description",
        "Role.permissions",
        "Role.inheritsFromRoleId",
        "Role.isSystem",
        "Role.principalCount",
        "Role.grantCount"
       ],
       "operation": "listRoles",
       "provenance": "contract identity.yaml GET /roles"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected people access rights",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "11 screens, each with what needs attention.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search people & access rights",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in people & access rights yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for people & access rights. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listRoles",
    "contract": "identity",
    "purpose": "Roles and who holds them",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more than one venue is asked which before the page renders, rather than shown the first one.",
   "preloaded": [
    "VenueSettings.id",
    "VenueSettings.venueId",
    "VenueSettings.supportHours",
    "VenueSettings.quietHours",
    "VenueSettings.segregatedAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-106"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "getApprovalAnalytics": {
  "method": "GET",
  "path": "/approval-analytics",
  "contract": "approvals",
  "summary": "Volumes, times, rejections and bottlenecks",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ApprovalAnalytics"
 },
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
 },
 "listIndexJobs": {
  "method": "GET",
  "path": "/index-jobs",
  "contract": "ai",
  "summary": "Indexing in flight and recently finished",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "IndexJob"
 },
 "listRoles": {
  "method": "GET",
  "path": "/roles",
  "contract": "identity",
  "summary": "List roles",
  "permission": "ROLE_MANAGE",
  "offlineCapable": true,
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalAnalytics": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from approvals.request",
  "properties": {
   "from": {
    "type": "string",
    "format": "date"
   },
   "to": {
    "type": "string",
    "format": "date"
   },
   "groupBy": {
    "type": "string"
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "raised": {
       "type": "integer"
      },
      "approved": {
       "type": "integer"
      },
      "rejected": {
       "type": "integer"
      },
      "withdrawn": {
       "type": "integer"
      },
      "expired": {
       "type": "integer",
       "description": "**Requests nobody answered.** Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person.\n"
      },
      "escalated": {
       "type": "integer"
      },
      "slaBreached": {
       "type": "integer"
      },
      "medianMinutes": {
       "type": "number"
      },
      "p95Minutes": {
       "type": "number"
      }
     }
    }
   }
  }
 },
 "IndexJob": {
  "type": "object",
  "x-ticvai-persistence": "ai.index_job",
  "required": [
   "id",
   "sourceId",
   "status",
   "startedAt"
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
   "kind": {
    "type": "string",
    "enum": [
     "full",
     "incremental",
     "removal"
    ]
   },
   "reason": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "building",
     "verifying",
     "swapping",
     "complete",
     "failed"
    ]
   },
   "recordsTotal": {
    "type": "integer"
   },
   "recordsEmbedded": {
    "type": "integer"
   },
   "recordsFailed": {
    "type": "integer",
    "description": "**The number to watch.** A source silently failing on 3% of its rows is a search silently missing 3% of the answers, and nothing else in the system will say so.\n"
   },
   "failureSample": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "shadowCollection": {
    "type": "string",
    "nullable": true,
    "description": "A full rebuild writes here and swaps on completion. Reindexing in place leaves the assistant answering from a half-built index.\n"
   },
   "shardKey": {
    "type": "string",
    "readOnly": true,
    "description": "**The tenant boundary on shared placement** (ADR-0021). A collection is shared by every tenant using the same embedding model, and the shard is what separates them — set at provisioning from the tenant, never from a request.\nOn dedicated placement there is one shard and this is still populated, because a tenant moving from shared to dedicated moves a shard rather than being re-indexed.\n"
   },
   "embeddingModel": {
    "type": "string"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string"
     },
     "windows": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string"
     },
     "to": {
      "type": "string"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string"
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       false,
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": false,
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   }
  }
 }
}
```
