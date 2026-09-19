# P08-guests-marketing-01 — P08 · Guests & Marketing

**4 screens · 11 operations · 14 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `AI_AUDIT_VIEW, AI_CONFIGURE, CASE_MANAGE, CASE_VIEW, MARKETING_MANAGE, MARKETING_VIEW, PERMISSION_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: getVenueSettings
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-068` | Audit Log | listDetail | 2 | 0 | — |
| `BO-073` | Lost & Found Register | listDetail | 2 | 0 | — |
| `BO-091` | AI Policy & Spend | listDetail | 4 | 0 | — |
| `BO-107` | Guests & Marketing | listDetail | 3 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-068",
  "name": "Audit Log",
  "module": "Guests & Marketing",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/audit-log",
   "component": "apps/venue-management-web/src/routes/venue-operations/AuditLogDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
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
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried `listAiInteractions` alone** — an audit log showing only AI prompts. The platform audit record is `identity.audit_event`. **Rewired 20 August.** **`listAuditRecords` wired 24 August.** This screen declared zero operations — an audit log with nothing behind it — and `platform.audit_record` was written by nothing and read by nothing. **Found by mapping the POS pack**, where four separate frames wanted an audit view. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "Retail Board 6.dc.html#ret-6j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listAuditRecords` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See who changed what at this venue.",
  "gaps": [
   {
    "operation": "listAuditRecords",
    "why": "**1 declared operation reach no component on this screen**: listAuditRecords. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Resolve",
       "operation": "resolvePermissions",
       "provenance": "contract identity.yaml POST /permissions/resolve"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAuditRecords",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "resolvePermissions",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audit log list.",
   "error": "Could not load. Names which read failed and leaves the audit log untouched.",
   "emptyFirstRun": "No audit log yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the audit log are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAuditRecords",
    "contract": "tenancy",
    "purpose": "Who did what, where, and when",
    "trigger": "onLoad"
   },
   {
    "operationId": "resolvePermissions",
    "contract": "identity",
    "purpose": "Simulate a principal's effective permissions",
    "trigger": "onAction",
    "invalidates": [
     "listAuditRecords"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-068",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 6.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-073",
  "name": "Lost & Found Register",
  "module": "Guests & Marketing",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/lost-found-register",
   "component": "apps/venue-management-web/src/routes/venue-operations/LostFoundRegisterDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
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
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried `listCases` and `createCase`.** `LostItem` exists — CL-07 built it as one entity in two directions, lost and found — and a service case is a different thing. **Rewired 20 August.**",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listLostItems` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Match what was lost to what was handed in.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every lost found register",
       "bindsTo": "LostItem",
       "columns": [
        "LostItem.id",
        "LostItem.foundOrLost",
        "LostItem.kind",
        "LostItem.description",
        "LostItem.colour",
        "LostItem.brand",
        "LostItem.venueId",
        "LostItem.lastSeenPointId",
        "LostItem.reportedAt",
        "LostItem.reportedBySubjectId",
        "LostItem.storageLocation",
        "LostItem.status"
       ],
       "operation": "listLostItems",
       "provenance": "contract marketing-crm.yaml GET /lost-items"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected lost found register",
       "bindsTo": "LostItem",
       "columns": [
        "LostItem.id",
        "LostItem.foundOrLost",
        "LostItem.kind",
        "LostItem.description",
        "LostItem.colour",
        "LostItem.brand",
        "LostItem.venueId",
        "LostItem.lastSeenPointId",
        "LostItem.reportedAt",
        "LostItem.reportedBySubjectId",
        "LostItem.storageLocation",
        "LostItem.status",
        "LostItem.photoAssetIds",
        "LostItem.disposeAfter"
       ],
       "operation": "listLostItems",
       "provenance": "contract marketing-crm.yaml GET /lost-items"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Find matches",
       "operation": "matchLostItem",
       "provenance": "contract marketing-crm.yaml POST /lost-items/{itemId}/match"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listLostItems",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "matchLostItem",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lost found register list.",
   "error": "Could not load. Names which read failed and leaves the lost found register untouched.",
   "emptyFirstRun": "No lost found register yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the lost found register are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listLostItems",
    "contract": "marketing-crm",
    "purpose": "Reported and found, with suggested matches",
    "trigger": "onLoad"
   },
   {
    "operationId": "matchLostItem",
    "contract": "marketing-crm",
    "purpose": "Tie a report to a found item, or hand it back",
    "trigger": "onAction",
    "invalidates": [
     "listLostItems"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "itemId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "LostItem.id",
    "LostItem.foundOrLost",
    "LostItem.kind",
    "LostItem.description",
    "LostItem.colour"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-073"
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
  "id": "BO-091",
  "name": "AI Policy & Spend",
  "module": "Guests & Marketing",
  "requiresModule": "ai",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/ai/policy",
   "component": "apps/venue-management-web/src/routes/AiPolicySpend.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001"
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
     "to": "ADM-004",
     "trigger": "Platform Audit Log",
     "provenance": "flow F100 step 2→3",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Added 17 August. **Staff and guest spend shown separately** — a venue can manage the first and cannot stop guests asking questions. At the ceiling the manager decides whether to continue; the assistant does not stop on its own (CF-14). **Index failures sit beside spend on purpose** - both answer the same two questions, is the assistant working and what is it costing, and a failure rate is the cheaper half of that answer.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listIndexFailures` reads the population and `getAiPolicy` reads one of them — list, select, act",
  "purpose": "What the assistant may do here, what it has cost, and what happens at the ceiling.",
  "gaps": [
   {
    "operation": "getAiUsage",
    "why": "**1 declared operation reach no component on this screen**: getAiUsage. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every policy spend",
       "bindsTo": "IndexFailure",
       "columns": [
        "IndexFailure.id",
        "IndexFailure.jobId",
        "IndexFailure.sourceId",
        "IndexFailure.documentRef",
        "IndexFailure.stage",
        "IndexFailure.error",
        "IndexFailure.attempts"
       ],
       "operation": "listIndexFailures",
       "provenance": "contract ai.yaml GET /index-failures"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected policy spend",
       "bindsTo": "AiPolicy",
       "columns": [
        "AiPolicy.id",
        "AiPolicy.scopeLevel",
        "AiPolicy.enabledCapabilities",
        "AiPolicy.allowedRoleIds",
        "AiPolicy.maskedFields",
        "AiPolicy.requiresApprovalFor",
        "AiPolicy.monthlyTokenCeiling",
        "AiPolicy.ceilingBehaviour",
        "AiPolicy.ceilingWarningPercent",
        "AiPolicy.guestCapabilityScope",
        "AiPolicy.retrieveTopK",
        "AiPolicy.rerankTopK",
        "AiPolicy.cacheAnswers",
        "AiPolicy.cacheTtlMinutes",
        "AiPolicy.retainInteractionsDays",
        "AiPolicy.semanticCacheThreshold"
       ],
       "operation": "getAiPolicy",
       "provenance": "contract ai.yaml GET /policy"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setAiPolicy",
       "provenance": "contract ai.yaml PUT /policy"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setAiPolicy",
       "label": "Save ai policy",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAiPolicy",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The policy spend list.",
   "error": "Could not load. Names which read failed and leaves the policy spend untouched.",
   "emptyFirstRun": "No policy spend yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the policy spend are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAiPolicy",
    "contract": "ai",
    "purpose": "What the assistant may do here",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAiPolicy",
    "contract": "ai",
    "purpose": "Set the policy",
    "trigger": "onAction",
    "invalidates": [
     "listIndexFailures"
    ]
   },
   {
    "operationId": "getAiUsage",
    "contract": "ai",
    "purpose": "Usage, cost and performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "listIndexFailures",
    "contract": "ai",
    "purpose": "Records an index could not embed, and at which stage",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiPolicy.id",
    "AiPolicy.scopeLevel",
    "AiPolicy.enabledCapabilities",
    "AiPolicy.allowedRoleIds",
    "AiPolicy.maskedFields"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-091"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-107",
  "name": "Guests & Marketing",
  "module": "Guests & Marketing",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/guests-marketing",
   "component": "apps/venue-management-web/src/routes/home/GuestsMarketingList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-068",
    "BO-073",
    "BO-091"
   ],
   "transitions": [
    {
     "to": "BO-073",
     "trigger": "Lost & Found Register",
     "carries": [
      "itemId",
      "venueId"
     ],
     "provenance": "derived — BO-073 declares entryState.params itemId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Section landing. **3 screens reach the entry point through here** — before 20 August they reached it through nothing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCampaigns` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in guests & marketing, and what in it needs attention.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every guests marketing",
       "bindsTo": "Campaign",
       "columns": [
        "Campaign.name",
        "Campaign.kind",
        "Campaign.channel",
        "Campaign.venueId",
        "Campaign.segmentId",
        "Campaign.content",
        "Campaign.trigger",
        "Campaign.scheduledFor",
        "Campaign.consentPurpose",
        "Campaign.sendWindow",
        "Campaign.id",
        "Campaign.budgetCap"
       ],
       "operation": "listCampaigns",
       "provenance": "contract marketing-crm.yaml GET /campaigns"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected guests marketing",
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
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns"
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
       "notes": "3 screens, each with what needs attention.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search guests & marketing",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in guests & marketing yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for guests & marketing. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCampaigns",
    "contract": "marketing-crm",
    "purpose": "Campaigns and their reach",
    "trigger": "onLoad"
   },
   {
    "operationId": "createCampaign",
    "contract": "marketing-crm",
    "purpose": "Start a campaign",
    "trigger": "onAction",
    "invalidates": [
     "listCampaigns"
    ]
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-107"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "createCampaign": {
  "method": "POST",
  "path": "/campaigns",
  "contract": "marketing-crm",
  "summary": "Create a campaign",
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
  "requestBody": "CreateCampaignRequest",
  "responds": "Campaign"
 },
 "getAiPolicy": {
  "method": "GET",
  "path": "/policy",
  "contract": "ai",
  "summary": "What the assistant may do here",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AiPolicy"
 },
 "getAiUsage": {
  "method": "GET",
  "path": "/usage",
  "contract": "ai",
  "summary": "Usage, cost and performance",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
  "responds": "AiUsageReport"
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
 "listAuditRecords": {
  "method": "GET",
  "path": "/audit-records",
  "contract": "tenancy",
  "summary": "Who did what, where, and when",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "orgUnitId",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "action",
    "in": "query",
    "required": null
   },
   {
    "name": "subjectRef",
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
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "listCampaigns": {
  "method": "GET",
  "path": "/campaigns",
  "contract": "marketing-crm",
  "summary": "List campaigns",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "listIndexFailures": {
  "method": "GET",
  "path": "/index-failures",
  "contract": "ai",
  "summary": "Records an index could not embed",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "jobId",
    "in": "query",
    "required": null
   },
   {
    "name": "stage",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "IndexFailure"
 },
 "listLostItems": {
  "method": "GET",
  "path": "/lost-items",
  "contract": "marketing-crm",
  "summary": "Reported and found, with suggested matches",
  "permission": "CASE_VIEW",
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
  "responds": "LostItem"
 },
 "matchLostItem": {
  "method": "POST",
  "path": "/lost-items/{itemId}/match",
  "contract": "marketing-crm",
  "summary": "Tie a report to a found item, or hand it back",
  "permission": "CASE_MANAGE",
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
  "responds": "LostItem"
 },
 "resolvePermissions": {
  "method": "POST",
  "path": "/permissions/resolve",
  "contract": "identity",
  "summary": "Simulate a principal's effective permissions",
  "permission": "PERMISSION_VIEW",
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
  "responds": null
 },
 "setAiPolicy": {
  "method": "PUT",
  "path": "/policy",
  "contract": "ai",
  "summary": "Set the policy",
  "permission": "AI_CONFIGURE",
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
  "requestBody": "AiPolicy",
  "responds": "AiPolicy"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiPolicy": {
  "type": "object",
  "x-ticvai-persistence": "ai.policy",
  "required": [
   "scopeLevel",
   "enabledCapabilities"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "venue"
    ],
    "description": "Tenant sets the default; a venue may narrow it and never widen it."
   },
   "enabledCapabilities": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "assist",
      "search",
      "generateConfiguration",
      "generateLayout",
      "summarise",
      "explain"
     ]
    }
   },
   "allowedRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "maskedFields": {
    "type": "array",
    "description": "Redacted before a prompt leaves the platform (8.3.73). **Defaults to every field in the pii schema** — a masking list nobody filled in should send nothing rather than everything.\n",
    "items": {
     "type": "string"
    }
   },
   "requiresApprovalFor": {
    "type": "array",
    "description": "8.3.61–8.3.64. Nothing in this list executes without a decision.",
    "items": {
     "type": "string",
     "enum": [
      "pricing",
      "promotion",
      "operational",
      "financial",
      "configuration"
     ]
    }
   },
   "monthlyTokenCeiling": {
    "type": "integer",
    "nullable": true
   },
   "ceilingBehaviour": {
    "type": "string",
    "enum": [
     "warn",
     "warnThenDisable",
     "block"
    ],
    "default": "warn",
    "description": "**Decided 17 August: warn, and let the venue manager choose.** A cap that stops the assistant mid-visit turns a cost control into a guest-facing outage, and the venue has no warning it is about to happen.\nAt the ceiling a notification reaches the venue manager with the spend and the remaining period, and **the assistant keeps answering until somebody decides otherwise**. `warnThenDisable` and `block` exist for a tenant who asks for a hard limit; neither is the default.\n"
   },
   "ceilingWarningPercent": {
    "type": "integer",
    "default": 80,
    "description": "**Warn before the ceiling, not at it.** A manager told at 100% has already spent it; one told at 80% can decide with a week left.\n"
   },
   "guestCapabilityScope": {
    "type": "array",
    "description": "**What a guest-facing assistant may help with, and nothing else** (2.1.28). Bounding the capability is what makes the cost predictable and the safety posture tractable — an assistant that answers anything is one that can be asked anything.\n",
    "items": {
     "type": "string",
     "enum": [
      "ticketSelection",
      "promotions",
      "faq",
      "recommendations",
      "checkout",
      "waitTimes",
      "wayfinding"
     ]
    }
   },
   "retrieveTopK": {
    "type": "integer",
    "default": 30,
    "description": "How many chunks retrieval returns before reranking."
   },
   "rerankTopK": {
    "type": "integer",
    "nullable": true,
    "default": 5,
    "description": "How many survive the rerank and reach the model. **Reranking reduces cost as well as improving quality**, which is unusual — retrieval is cheap and the tokens sent to the model are not.\nNull disables reranking, and a venue with no rerank provider configured runs without it rather than failing.\n"
   },
   "cacheAnswers": {
    "type": "boolean",
    "default": true,
    "description": "**The largest cost lever available at a kiosk.** Guest questions are extraordinarily repetitive — forty questions, thousands of times a day — where staff questions are diverse.\n**Invalidation runs on the same events that invalidate the index.** A cached answer that outlives a price change has misled a guest on the venue's behalf, which is worse than a slow one.\n"
   },
   "cacheTtlMinutes": {
    "type": "integer",
    "default": 60,
    "description": "An upper bound on top of event invalidation, not instead of it. **The key carries `scope_path`** — a cache keyed on the question alone is a cross-venue leak wearing a performance hat.\n"
   },
   "retainInteractionsDays": {
    "type": "integer",
    "description": "How long prompts and responses are kept. **Unresolved — CF-64.** Prompts may carry personal data, so this is a retention decision nobody has made.\n"
   },
   "semanticCacheThreshold": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "default": 0.95,
    "description": "**Similarity above which a cached answer serves a new question.** `cache:answer` is exact-match on question, scope and locale — *what time do you close* and *when do you shut* are two misses and two provider calls.\n\n**Per capability, not global.** A factual venue question tolerates 0.95; a recommendation tolerates nothing. **A tenant who finds it wrong can move it**, which is why it is policy rather than a constant."
   },
   "negativeCacheTtlSeconds": {
    "type": "integer",
    "default": 300,
    "description": "**How long *no answer found* is remembered.** A miss costs a full retrieval and a completion.\n\n**Shorter than a hit deliberately** — the answer may exist tomorrow because somebody indexed it."
   },
   "cascade": {
    "type": "object",
    "nullable": true,
    "description": "**A small model answers and escalates only below a confidence threshold.** `ai.suggestion.confidence` exists and nothing routes on it.",
    "properties": {
     "smallModel": {
      "type": "string"
     },
     "largeModel": {
      "type": "string"
     },
     "escalateBelow": {
      "type": "number",
      "default": 0.7
     }
    }
   },
   "chunking": {
    "type": "object",
    "description": "**The single biggest lever on retrieval quality**, and currently nowhere. **A venue FAQ and a maintenance manual do not chunk the same way.** Per collection, not global.",
    "properties": {
     "sizeTokens": {
      "type": "integer",
      "default": 512
     },
     "overlapTokens": {
      "type": "integer",
      "default": 64
     },
     "strategy": {
      "type": "string",
      "enum": [
       "fixed",
       "sentence",
       "semantic"
      ],
      "default": "sentence"
     }
    }
   },
   "quantisation": {
    "type": "string",
    "enum": [
     "none",
     "scalar",
     "binary"
    ],
    "default": "none",
    "description": "**A decision, never a default.** `scalar` int8 is roughly four times smaller — 49 GB becomes 12 — **and it costs recall**. `binary` is smaller again and needs rescoring against full vectors to be usable.\n\n**A creation decision**: changing it means a rebuild, which is what `shadow_collection` is for. **A tenant whose search quality drops after an infrastructure change should be able to find the line that did it.**"
   },
   "hnsw": {
    "type": "object",
    "nullable": true,
    "description": "**Defaults are tuned for neither our recall nor our latency.** A collection built with the wrong ones needs a rebuild, which is why this is a creation decision like the sparse index.",
    "properties": {
     "m": {
      "type": "integer",
      "default": 16
     },
     "efConstruct": {
      "type": "integer",
      "default": 128
     },
     "efSearch": {
      "type": "integer",
      "default": 64
     }
    }
   },
   "perRequestTokenCeiling": {
    "type": "integer",
    "nullable": true,
    "description": "**One runaway conversation can spend a tenant's month.** `monthlyTokenCeiling` discovers that after it has happened."
   },
   "streamsByCapability": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "**Time to first token and total latency are separate targets.** A concierge that starts answering in 300 ms and finishes in 4 seconds is better than one silent for 2.\n\n**`chat` streams; `generateConfiguration` does not** — nobody watches a config draft assemble."
   },
   "fallbackProviderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-151: **a provider outage with no fallback is every AI surface going dark at once.**\n\n**`residencyRefused` is never failed over.** It is a correct answer, and moving the call elsewhere would defeat the refusal."
   },
   "guardrailShortCircuit": {
    "type": "boolean",
    "default": true,
    "description": "**A refusal a rule can decide never reaches a model.** Cheaper, faster and more consistent than asking a model to refuse."
   }
  }
 },
 "AiUsageReport": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from ai.interaction",
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
      "interactions": {
       "type": "integer"
      },
      "promptTokens": {
       "type": "integer"
      },
      "completionTokens": {
       "type": "integer"
      },
      "costMinor": {
       "type": "integer"
      },
      "p95LatencyMs": {
       "type": "integer"
      },
      "refusalRate": {
       "type": "number"
      },
      "rejectionRate": {
       "type": "number",
       "description": "Proposals a person refused. **The number that says whether the assistant is worth having**, and the one nobody thinks to measure.\n"
      }
     }
    }
   }
  }
 },
 "Campaign": {
  "x-ticvai-persistence": "marketing.campaign",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateCampaignRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "budgetCap": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "budgetSpent": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "readOnly": true,
      "description": "BL-169. **A campaign could spend without limit** — following the promotions `budgetCap` precedent. **Sending stops at the cap rather than overspending and reporting it**, because a marketing budget discovered after it was exceeded is a budget nobody set.\n"
     },
     "status": {
      "$ref": "#/components/schemas/CampaignStatus"
     },
     "isPaused": {
      "type": "boolean"
     },
     "createdByPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     },
     "launchedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "completedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "CampaignContent": {
  "x-ticvai-persistence": "none — embedded in campaign",
  "type": "object",
  "required": [
   "templateId"
  ],
  "properties": {
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectOverride": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "mergeDefaults": {
    "type": "object",
    "additionalProperties": true
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Offer carried by the campaign. Coupon codes are issued from it."
   }
  }
 },
 "CampaignKind": {
  "type": "string",
  "enum": [
   "oneOff",
   "scheduled",
   "triggered",
   "recurring"
  ]
 },
 "CampaignStatus": {
  "type": "string",
  "enum": [
   "draft",
   "scheduled",
   "sending",
   "paused",
   "completed",
   "stopped",
   "failed"
  ]
 },
 "CampaignTrigger": {
  "x-ticvai-persistence": "none — embedded in campaign",
  "type": "object",
  "properties": {
   "event": {
    "type": "string",
    "enum": [
     "bookingConfirmed",
     "visitCompleted",
     "membershipExpiring",
     "birthday",
     "abandonedCart",
     "firstVisit",
     "inactivity"
    ]
   },
   "delayHours": {
    "type": "integer"
   },
   "conditions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/SegmentCriterion"
    }
   }
  }
 },
 "ConsentPurpose": {
  "type": "string",
  "enum": [
   "marketing",
   "personalisation",
   "profiling",
   "thirdPartySharing",
   "aiProcessing",
   "transactional"
  ]
 },
 "CreateCampaignRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "kind",
   "channel",
   "segmentId",
   "content"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "kind": {
    "$ref": "#/components/schemas/CampaignKind"
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "segmentId": {
    "type": "string",
    "format": "uuid"
   },
   "content": {
    "$ref": "#/components/schemas/CampaignContent"
   },
   "trigger": {
    "$ref": "#/components/schemas/CampaignTrigger"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time"
   },
   "consentPurpose": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ConsentPurpose"
     }
    ],
    "default": "marketing"
   },
   "sendWindow": {
    "type": "object",
    "description": "Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen.\n",
    "properties": {
     "startTime": {
      "type": "string"
     },
     "endTime": {
      "type": "string"
     },
     "timeZone": {
      "type": "string"
     }
    }
   }
  }
 },
 "IndexFailure": {
  "type": "object",
  "x-ticvai-persistence": "ai.index_failure",
  "description": "ADR-0033. **Failure is a row somebody works, not a log line.**\n\n`ai.index_job` already counts `records_failed` and holds a `failure_sample`; **this is where the other 4,999 go.**",
  "required": [
   "id"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "jobId": {
    "type": "string",
    "format": "uuid"
   },
   "sourceId": {
    "type": "string",
    "format": "uuid"
   },
   "documentRef": {
    "type": "string",
    "description": "What would not index."
   },
   "stage": {
    "type": "string",
    "enum": [
     "fetch",
     "parse",
     "chunk",
     "embed",
     "upsert"
    ],
    "description": "**Where it failed decides who fixes it.** A parse failure is a document problem; an embed failure is a provider one."
   },
   "error": {
    "type": "string"
   },
   "attempts": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "LostItem": {
  "type": "object",
  "x-ticvai-persistence": "marketing.lost_item",
  "description": "BL-021. **Screens existed on three platforms and `lostAndFound` is a `ModuleKey`, and there was no item, no claim and no match between them** — which is the whole capability.\nGeneric case management holds a conversation about a lost bag. **It cannot tell you that the bag somebody handed in on Tuesday is the one somebody asked about on Monday**, and that match is the only thing the module is for.\n",
  "required": [
   "id",
   "kind",
   "foundOrLost",
   "venueId",
   "reportedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "foundOrLost": {
    "type": "string",
    "enum": [
     "lost",
     "found"
    ],
    "description": "**One entity, two directions.** A guest reports a loss and a steward reports a find, and modelling them separately means matching across two tables that drift.\n"
   },
   "kind": {
    "type": "string",
    "enum": [
     "bag",
     "phone",
     "wallet",
     "keys",
     "clothing",
     "jewellery",
     "documents",
     "toy",
     "buggy",
     "other"
    ]
   },
   "description": {
    "type": "string"
   },
   "colour": {
    "type": "string",
    "nullable": true
   },
   "brand": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "lastSeenPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A point on the venue map. **Where a guest thinks they lost it is the strongest signal for a match**, and it is also the thing they are least sure about.\n"
   },
   "reportedAt": {
    "type": "string",
    "format": "date-time"
   },
   "reportedBySubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "storageLocation": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "matched",
     "claimed",
     "disposed",
     "returned"
    ]
   },
   "photoAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "disposeAfter": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "**A retention date, because unclaimed property has one.** A storeroom with no disposal date is a storeroom that fills, and the date is a venue policy rather than a default.\n"
   }
  }
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
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
