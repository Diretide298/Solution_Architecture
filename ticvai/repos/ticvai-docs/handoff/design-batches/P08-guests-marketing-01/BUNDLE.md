# P08-guests-marketing-01 — P08 · Guests & Marketing

**4 screens · 18 operations · 32 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, AUDIT_VIEW, CASE_MANAGE, CASE_VIEW, MARKETING_MANAGE, MARKETING_VIEW, PERMISSION_VIEW, REPORT_VIEW_VENUE, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-068` | Audit Log | listDetail | 3 | 1 | — |
| `BO-073` | Lost & Found Register | listDetail | 3 | 1 | — |
| `BO-091` | AI Policy & Spend | listDetail | 8 | 1 | — |
| `BO-107` | Guests & Marketing | listDetail | 4 | 1 | — |

## Thin screens in this batch

**BO-073 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
   "inferred": true
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried `listAiInteractions` alone** — an audit log showing only AI prompts. The platform audit record is `identity.audit_event`. **Rewired 20 August.** **`listAuditRecords` wired 24 August.** This screen declared zero operations — an audit log with nothing behind it — and `platform.audit_record` was written by nothing and read by nothing. **Found by mapping the POS pack**, where four separate frames wanted an audit view. **Retail board operations wired 24 August.** **Platform-staff access shown 28 September (audit R098)** — `listPlatformStaffGrants` lists every grant a TICVAI operator opened into this tenant, and the `platformStaffGrantId` filter of `listAuditRecords` shows what was done under each.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 6.dc.html#ret-6j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listAuditRecords` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See who changed what at this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Resolve permissions",
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
       "kind": "textField",
       "label": "Org unit id",
       "operation": "listAuditRecords",
       "notes": "Sends `?orgUnitId=` to `listAuditRecords`.",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listAuditRecords",
       "notes": "Sends `?principalId=` to `listAuditRecords`.",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listAuditRecords",
       "notes": "Sends `?workstationId=` to `listAuditRecords`.",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "textField",
       "label": "Action",
       "operation": "listAuditRecords",
       "notes": "Sends `?action=` to `listAuditRecords`.",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "textField",
       "label": "Subject ref",
       "operation": "listAuditRecords",
       "notes": "Sends `?subjectRef=` to `listAuditRecords`.",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listAuditRecords",
       "notes": "Sends `?from=` to `listAuditRecords`.",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "listAuditRecords",
       "notes": "Sends `?to=` to `listAuditRecords`.",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "dataTable",
       "label": "Every audit",
       "bindsTo": "AuditRecord",
       "columns": [
        "AuditRecord.id",
        "AuditRecord.principalId",
        "AuditRecord.orgUnitId",
        "AuditRecord.workstationId",
        "AuditRecord.action",
        "AuditRecord.subjectRef",
        "AuditRecord.occurredAt",
        "AuditRecord.platformStaffGrantId"
       ],
       "operation": "listAuditRecords",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "textField",
       "label": "Platform-staff grant id",
       "operation": "listAuditRecords",
       "notes": "Sends `?platformStaffGrantId=` to `listAuditRecords`, so the log shows only what a platform operator did under that grant. Choosing a row in **Platform-staff grants** fills it (decided 28 September, audit R098).",
       "provenance": "contract tenancy.yaml GET /audit-records"
      },
      {
       "kind": "toggle",
       "label": "Open grants only",
       "operation": "listPlatformStaffGrants",
       "notes": "Sends `?activeOnly=true` to `listPlatformStaffGrants`.",
       "provenance": "contract identity.yaml GET /platform-staff-grants"
      },
      {
       "kind": "dataTable",
       "label": "Platform-staff grants",
       "bindsTo": "PlatformStaffGrant",
       "columns": [
        "PlatformStaffGrant.operatorDisplayName",
        "PlatformStaffGrant.operatorPrincipalId",
        "PlatformStaffGrant.reason",
        "PlatformStaffGrant.ticketRef",
        "PlatformStaffGrant.permissions",
        "PlatformStaffGrant.openedAt",
        "PlatformStaffGrant.expiresAt"
       ],
       "operation": "listPlatformStaffGrants",
       "notes": "**Every platform-staff grant into this tenant is visible here** — open, expired and ended, most recent first. Choosing a grant filters the audit log on `platformStaffGrantId` to show what was done under it (decided 28 September, audit R098).",
       "provenance": "contract identity.yaml GET /platform-staff-grants"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audit log list.",
   "error": "Could not load. Names which read failed and leaves the audit log untouched.",
   "emptyFirstRun": "No audit log yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on orgUnitId, principalId, workstationId, action, subjectRef, from and platformStaffGrantId; the audit log is still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `AUDIT_VIEW`, which `listAuditRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAuditRecords",
    "contract": "tenancy",
    "purpose": "Who did what, where, and when",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPlatformStaffGrants",
    "contract": "identity",
    "purpose": "Every platform-staff grant into this tenant, so the tenant sees when TICVAI staff acted and under what reason (decided 28 September, audit R098)",
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
   "derivedFrom": "wireframes/reference/Retail Board 6.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 6.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formResolvePermissions",
    "component": "modal",
    "trigger": "Resolve permissions",
    "body": "**Collects what `resolvePermissions` sends before it is called.** Required: `principalId`, `roleId`. Optional: `atScopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resolve permissions",
     "operation": "resolvePermissions"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "principalId",
      "roleId",
      "atScopePath"
     ]
    },
    "provenance": "contract identity.yaml POST /permissions/resolve"
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
   "inferred": true
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
       "label": "Every lost",
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
       "label": "The selected lost",
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
       "label": "Find matches for lost item",
       "operation": "matchLostItem",
       "provenance": "contract marketing-crm.yaml POST /lost-items/{itemId}/match"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lost found register list.",
   "error": "Could not load. Names which read failed and leaves the lost found register untouched.",
   "emptyFirstRun": "No lost found register yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listLostItems` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `CASE_VIEW`, which `listLostItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   },
   {
    "operationId": "recordLostItem",
    "contract": "marketing-crm",
    "purpose": "Report something lost, or log something handed in",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
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
  "overlays": [
   {
    "id": "formMatchLostItem",
    "component": "modal",
    "trigger": "Find matches for lost item",
    "body": "**Collects what `matchLostItem` sends before it is called.** Required: `action`. Optional: `otherItemId`, `claimantSubjectId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Find matches for lost item",
     "operation": "matchLostItem"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "otherItemId",
      "claimantSubjectId",
      "note"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /lost-items/{itemId}/match"
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
   "inferred": true,
   "transitions": [
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Job id",
       "operation": "listIndexFailures",
       "notes": "Sends `?jobId=` to `listIndexFailures`.",
       "provenance": "contract ai.yaml GET /index-failures"
      },
      {
       "kind": "selectField",
       "label": "Stage",
       "operation": "listIndexFailures",
       "notes": "Sends `?stage=` to `listIndexFailures`.",
       "provenance": "contract ai.yaml GET /index-failures"
      },
      {
       "kind": "dataTable",
       "label": "Every index failure",
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
       "label": "The selected index failure",
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
      },
      {
       "kind": "detailPanel",
       "label": "The AI usage report",
       "bindsTo": "AiUsageReport",
       "columns": [
        "AiUsageReport.from",
        "AiUsageReport.to",
        "AiUsageReport.groupBy",
        "AiUsageReport.rows"
       ],
       "operation": "getAiUsage",
       "provenance": "contract ai.yaml GET /usage"
      },
      {
       "kind": "detailPanel",
       "label": "The AI policy",
       "bindsTo": "AiPolicy",
       "columns": [
        "AiPolicy.id",
        "AiPolicy.scopeLevel",
        "AiPolicy.scopePath",
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
        "AiPolicy.retainInteractionsDays"
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
       "label": "Save AI policy",
       "operation": "setAiPolicy",
       "provenance": "contract ai.yaml PUT /policy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The policy spend list.",
   "error": "Could not load. Names which read failed and leaves the policy spend untouched.",
   "emptyFirstRun": "No policy spend yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on jobId, stage and the policy spend are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `AI_CONFIGURE`, which `getAiPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   },
   {
    "operationId": "listAiCapabilities",
    "contract": "ai",
    "purpose": "The capability registry",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getEffectiveAiPolicy",
    "contract": "ai",
    "purpose": "The policy in force for a capability at a scope",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "configureAssistantProfile",
    "contract": "ai",
    "purpose": "Define an assistant profile",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAssistantProfiles",
    "contract": "ai",
    "purpose": "Assistant profiles",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiPolicy.id",
    "AiPolicy.scopeLevel",
    "AiPolicy.enabledCapabilities",
    "AiPolicy.allowedRoleIds",
    "AiPolicy.maskedFields"
   ],
   "params": [
    {
     "name": "profileKey",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-091"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetAiPolicy",
    "component": "modal",
    "trigger": "Save AI policy",
    "body": "**Collects what `setAiPolicy` sends before it is called.** Required: `scopeLevel`, `scopePath`, `enabledCapabilities`. Optional: `id`, `allowedRoleIds`, `maskedFields`, `requiresApprovalFor`, `monthlyTokenCeiling`, `ceilingBehaviour`, `ceilingWarningPercent`, `guestCapabilityScope`, `retrieveTopK`, `rerankTopK`, `cacheAnswers`, `cacheTtlMinutes` and 12 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AiPolicy",
    "confirm": {
     "label": "Save AI policy",
     "operation": "setAiPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "scopeLevel",
      "scopePath",
      "enabledCapabilities",
      "id",
      "allowedRoleIds",
      "maskedFields",
      "requiresApprovalFor",
      "monthlyTokenCeiling",
      "ceilingBehaviour",
      "ceilingWarningPercent",
      "guestCapabilityScope",
      "retrieveTopK",
      "rerankTopK",
      "cacheAnswers",
      "cacheTtlMinutes",
      "retainInteractionsDays",
      "semanticCacheThreshold",
      "negativeCacheTtlSeconds"
     ]
    },
    "provenance": "contract ai.yaml PUT /policy"
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
     "provenance": "derived — BO-073 declares entryState.params itemId and BO-107 holds none of them. The edge carries nothing: itemId only pre-selects (deep link or optional), and BO-073 opens on its own"
    },
    {
     "to": "BO-091",
     "trigger": "AI Policy & Spend",
     "provenance": "derived — BO-091 declares entryState.params profileKey and BO-107 holds none of them. The edge carries nothing: BO-091 finds profileKey (listAssistantProfiles) itself, and BO-091 opens on its own"
    }
   ]
  },
  "notes": "Section landing. **3 screens reach the entry point through here** — before 20 August they reached it through nothing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCampaigns` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in guests & marketing.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listCampaigns",
       "notes": "Sends `?status=` to `listCampaigns`.",
       "provenance": "contract marketing-crm.yaml GET /campaigns"
      },
      {
       "kind": "dataTable",
       "label": "Every campaign",
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
      },
      {
       "kind": "metricTile",
       "label": "Takings and admissions today",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.code",
        "KpiValue.name",
        "KpiValue.value",
        "KpiValue.period",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "**Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "3 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search guests & marketing",
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
       "label": "The selected campaign",
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
        "Campaign.budgetCap",
        "Campaign.budgetSpent",
        "Campaign.status",
        "Campaign.isPaused",
        "Campaign.createdByPrincipalId"
       ],
       "operation": "listCampaigns",
       "provenance": "contract marketing-crm.yaml GET /campaigns"
      },
      {
       "kind": "detailPanel",
       "label": "The venue settings",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.currencyCode",
        "VenueSettings.currencyScale",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.biometrics",
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
       "label": "Create campaign",
       "operation": "createCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns"
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
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Today's takings and admissions tiles — `kpiCodes=takings,admissions`, period defaulting to today (decided 28 September, audit R283)",
    "trigger": "onLoad"
   },
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
  "overlays": [
   {
    "id": "formCreateCampaign",
    "component": "modal",
    "trigger": "Create campaign",
    "body": "**Collects what `createCampaign` sends before it is called.** Required: `name`, `kind`, `channel`, `segmentId`, `content`. Optional: `venueId`, `trigger`, `scheduledFor`, `consentPurpose`, `sendWindow`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCampaignRequest",
    "confirm": {
     "label": "Create campaign",
     "operation": "createCampaign"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "kind",
      "channel",
      "segmentId",
      "content",
      "venueId",
      "trigger",
      "scheduledFor",
      "consentPurpose",
      "sendWindow"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /campaigns"
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "configureAssistantProfile": {
  "method": "PUT",
  "path": "/assistant-profiles/{profileKey}",
  "contract": "ai",
  "summary": "Define an assistant profile",
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
  "requestBody": "AiAssistantProfile",
  "responds": "AiAssistantProfile"
 },
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
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "scopePath",
    "in": "query",
    "required": false
   }
  ],
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
 "getEffectiveAiPolicy": {
  "method": "GET",
  "path": "/governance/effective-policy",
  "contract": "ai",
  "summary": "The policy in force for a capability at a scope",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "capabilityKey",
    "in": "query",
    "required": true
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "environment",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiEffectivePolicy"
 },
 "getKpiValues": {
  "method": "GET",
  "path": "/kpi-values",
  "contract": "reporting",
  "summary": "Current values, against target, with movement",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kpiIds",
    "in": "query",
    "required": null
   },
   {
    "name": "kpiCodes",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "period",
    "in": "query",
    "required": null
   },
   {
    "name": "compareTo",
    "in": "query",
    "required": null
   },
   {
    "name": "interval",
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
  "responds": "KpiValue"
 },
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
 },
 "listAiCapabilities": {
  "method": "GET",
  "path": "/governance/capabilities",
  "contract": "ai",
  "summary": "The capability registry",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "family",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "riskClass",
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
 "listAssistantProfiles": {
  "method": "GET",
  "path": "/assistant-profiles",
  "contract": "ai",
  "summary": "Assistant profiles",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "audience",
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
 "listAuditRecords": {
  "method": "GET",
  "path": "/audit-records",
  "contract": "tenancy",
  "summary": "Who did what, where, and when",
  "permission": "AUDIT_VIEW",
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
    "name": "platformStaffGrantId",
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
  "summary": "Reported and found items",
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
  "responds": "Page"
 },
 "listPlatformStaffGrants": {
  "method": "GET",
  "path": "/platform-staff-grants",
  "contract": "identity",
  "summary": "Which platform staff have acted in this tenant, and under what grant",
  "permission": "AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "activeOnly",
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
 "recordLostItem": {
  "method": "POST",
  "path": "/lost-items",
  "contract": "marketing-crm",
  "summary": "Report something lost, or hand something in",
  "permission": "CASE_MANAGE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "LostItem",
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
  "scopeLevel": "venue",
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
 "AiAssistantProfile": {
  "type": "object",
  "x-ticvai-persistence": "ai.assistant_profile",
  "description": "**One assistant runtime, many profiles** (design 5.10, C5; AIC-069..080). The profile decides the audience, roles, knowledge sources, tools, model task and guest scope: guest concierge, support chatbot and staff assistants by role.",
  "required": [
   "profileKey",
   "audience"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "profileKey": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "audience": {
    "type": "string",
    "enum": [
     "staff",
     "guest",
     "support"
    ]
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "module": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
     }
    ],
    "nullable": true
   },
   "collectionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Knowledge collections it retrieves from."
   },
   "toolKeys": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Registered tools it may propose (an assistant only reads; a change request goes to the configuration assistant, AIC-078)."
   },
   "modelTask": {
    "type": "string",
    "description": "The gateway task, e.g. `assistant.staff.answer`. The visit planner agent (29 September, MOB-6) is profile `planner.guest` with task `planner.guest.refine` and the five `venue-map` visit-plan tools. The app publishing guide (M24-08) is profile `guide.appPublishing` with task `assistant.staff.answer`, grounded on the platform's store-publishing collection only."
   },
   "guestCapabilityScope": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "For a guest profile: the same values as `AiPolicy.guestCapabilityScope`, narrowed."
   },
   "locales": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "handoverTarget": {
    "type": "string",
    "nullable": true,
    "description": "Where \"ask a person\" goes: a support queue or a staff role."
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiAutonomyLevel": {
  "type": "integer",
  "minimum": 0,
  "maximum": 4,
  "description": "**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."
 },
 "AiCapabilityFamily": {
  "type": "string",
  "enum": [
   "gatewayAndModels",
   "governance",
   "actionPipeline",
   "knowledgeRetrieval",
   "assistants",
   "analyticsInsights",
   "configurationAssistant",
   "forecasting",
   "anomalyDetection",
   "riskIntelligence",
   "recommendations",
   "decisionRecords",
   "operationsEvaluation",
   "residencyPrivacy"
  ],
  "description": "The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."
 },
 "AiCapabilityRegistration": {
  "type": "object",
  "x-ticvai-persistence": "ai.capability",
  "description": "**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).",
  "required": [
   "capabilityKey",
   "family",
   "riskClass",
   "autonomyLevel"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "capabilityKey": {
    "type": "string",
    "description": "Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."
   },
   "family": {
    "$ref": "#/components/schemas/AiCapabilityFamily"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal",
    "description": "The accountable business owner (AIC-144)."
   },
   "businessFunction": {
    "type": "string",
    "nullable": true
   },
   "riskClass": {
    "$ref": "#/components/schemas/AiRiskClass"
   },
   "autonomyCeiling": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiAutonomyLevel"
     }
    ],
    "readOnly": true,
    "description": "The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."
   },
   "autonomyLevel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiAutonomyLevel"
     }
    ],
    "description": "The level in force at this scope. At most `autonomyCeiling`."
   },
   "dataCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Data categories the capability reads (ADM-524)."
   },
   "lifecycle": {
    "type": "object",
    "description": "Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.",
    "properties": {
     "development": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     },
     "staging": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     },
     "production": {
      "type": "string",
      "enum": [
       "draft",
       "pilot",
       "active",
       "retired"
      ]
     }
    }
   },
   "degradationMode": {
    "type": "string",
    "enum": [
     "rulesOnly",
     "searchOnly",
     "humanHandoff",
     "hidden",
     "failOpen",
     "lastPublished"
    ],
    "description": "What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "paused"
    ],
    "readOnly": true,
    "description": "Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."
   },
   "pausedReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "pausedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiEffectivePolicy": {
  "type": "object",
  "x-ticvai-persistence": "none — resolved from published policy versions, exceptions and ai.policy",
  "description": "**The policy in force for a capability at a scope** (AIC-153, AIC-165; ADM-525, ADM-528): the intersection of the capability, governance policy and the tenant or venue AI policy, with where each part came from.",
  "required": [
   "capabilityKey",
   "autonomyLevel",
   "rules"
  ],
  "properties": {
   "capabilityKey": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "autonomyLevel": {
    "$ref": "#/components/schemas/AiAutonomyLevel"
   },
   "autonomyCeiling": {
    "$ref": "#/components/schemas/AiAutonomyLevel"
   },
   "rules": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "rule": {
       "$ref": "#/components/schemas/AiGovernanceRule"
      },
      "policyKey": {
       "type": "string"
      },
      "version": {
       "type": "integer"
      },
      "scopePath": {
       "type": "string"
      }
     }
    }
   },
   "exceptions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiPolicyException"
    }
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "description": {
       "type": "string"
      },
      "resolvedTo": {
       "$ref": "#/components/schemas/AiGovernanceOutcome"
      }
     }
    },
    "description": "Conflicting rules and the more restrictive result they resolved to (AIC-161)."
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiGovernanceOutcome": {
  "type": "string",
  "enum": [
   "allow",
   "allowWithConditions",
   "prepareOnly",
   "approvalRequired",
   "escalate",
   "block"
  ],
  "description": "What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."
 },
 "AiGovernanceRule": {
  "type": "object",
  "x-ticvai-persistence": "none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList",
  "description": "One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).",
  "required": [
   "effect"
  ],
  "properties": {
   "effect": {
    "$ref": "#/components/schemas/AiGovernanceOutcome"
   },
   "capabilityKeys": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Registered capabilities it applies to. Empty means every capability the policy names."
   },
   "actions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "read",
      "analyze",
      "recommend",
      "generate",
      "prepare",
      "create",
      "modify",
      "publish",
      "execute",
      "delete"
     ]
    },
    "description": "ADM-523: what AI may do, from reading to executing."
   },
   "dataCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Permitted purposes for those categories (AIC-156, AIR-182)."
   },
   "maxAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Above this value the effect escalates one step (for example to `approvalRequired`)."
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Roles the rule applies to; empty means every role."
   },
   "environments": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "development",
      "sandbox",
      "staging",
      "production"
     ]
    },
    "description": "ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."
   },
   "conditions": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."
   }
  }
 },
 "AiPolicy": {
  "type": "object",
  "x-ticvai-persistence": "ai.policy",
  "required": [
   "scopeLevel",
   "scopePath",
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
   "scopePath": {
    "type": "string",
    "description": "**The node this row belongs to, and the key it is written under** — the tenant's node where `scopeLevel` is `tenant`, a venue's where it is `venue`. One row per `scopePath`; `setAiPolicy` writes the row it names and `getAiPolicy` resolves nearest ancestor first (ADR-0018).\n"
   },
   "enabledCapabilities": {
    "type": "array",
    "description": "**Extended on 29 September to the fourteen capabilities of the AI design** (section 1.1, `AiCapabilityFamily`). The six earlier values stay: they are finer switches inside `assistants`, `knowledgeRetrieval` and `configurationAssistant`, and a tenant that set them keeps them. `governance`, `decisionRecords` and `residencyPrivacy` cannot be switched off; listing them is accepted and changes nothing.\n",
    "items": {
     "type": "string",
     "enum": [
      "assist",
      "search",
      "generateConfiguration",
      "generateLayout",
      "summarise",
      "explain",
      "gatewayAndModels",
      "governance",
      "actionPipeline",
      "knowledgeRetrieval",
      "assistants",
      "analyticsInsights",
      "configurationAssistant",
      "forecasting",
      "anomalyDetection",
      "riskIntelligence",
      "recommendations",
      "decisionRecords",
      "operationsEvaluation",
      "residencyPrivacy"
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
    "description": "Redacted before a prompt leaves the platform (8.3.73). **Defaults to every field in the pii schema** — a masking list nobody filled in should send nothing rather than everything.\nEach entry is a column named `schema.table.column`, as the DDL names it — `pii.subject_contact.email`. **Omitted, null and an empty array all take the default**, because each of them is a list nobody filled in. An entry naming no column is refused at save rather than silently masking nothing.\n",
    "items": {
     "type": "string",
     "pattern": "^[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*$"
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
    "description": "**Decided 17 August: warn, and let the venue manager choose.** A cap that stops the assistant mid-visit turns a cost control into a guest-facing outage, and the venue has no warning it is about to happen.\nAt the ceiling a notification reaches the venue manager with the spend and the remaining period, and **the assistant keeps answering until somebody decides otherwise**. `warnThenDisable` and `block` exist for a tenant who asks for a hard limit; neither is the default.\n**Now the default for capabilities without their own entry** in `ceilingBehaviourByCapability` (AI design 5.9).\n"
   },
   "ceilingBehaviourByCapability": {
    "type": "array",
    "x-ticvai-persistence-kind": "valueObject",
    "x-ticvai-persistence-column": "jsonb",
    "description": "**Ceiling behaviour per capability** (AI design 5.9, AIC-227), so a budget never silently disables fraud scoring, which spends no tokens, or a critical capability. A capability not listed takes `ceilingBehaviour`. The guest concierge defaults to `warn` (decided 17 August).\n",
    "items": {
     "type": "object",
     "required": [
      "capability",
      "behaviour"
     ],
     "properties": {
      "capability": {
       "type": "string",
       "description": "An `AiCapabilityFamily` value, or a registered capability key."
      },
      "behaviour": {
       "type": "string",
       "enum": [
        "warn",
        "warnThenDisable",
        "block",
        "neverRestrict"
       ]
      }
     }
    }
   },
   "autonomyOverrides": {
    "type": "array",
    "x-ticvai-persistence-kind": "valueObject",
    "x-ticvai-persistence-column": "jsonb",
    "description": "**Tighten only** (AI design 3.8, AIC-151). A level per capability at or below the capability's ceiling, and on a venue row at or below the tenant row's. Autonomy is separate from user permission (AIC-154).\n",
    "items": {
     "type": "object",
     "required": [
      "capabilityKey",
      "autonomyLevel"
     ],
     "properties": {
      "capabilityKey": {
       "type": "string"
      },
      "autonomyLevel": {
       "$ref": "#/components/schemas/AiAutonomyLevel"
      }
     }
    }
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
      "wayfinding",
      "visitPlanning"
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
    "deprecated": true,
    "description": "How long prompts and responses are kept. **Deprecated 29 September (decision 5):** AI data retention is one tenant configuration with a period per data class, 90 days by default, kept with the tenant's other data-retention settings in `tenancy`, not here. Read for one release and ignored once the tenant setting exists.\n"
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
   },
   "suggestionProviders": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SuggestionProviderAssignments"
     }
    ],
    "readOnly": true,
    "description": "**Which producer answers each `SuggestionKind`**, and what `requestSuggestion` routes by. Written only by `setSuggestionProvider`; `setAiPolicy` leaves it as it was. Held on the tenant row — a venue row does not carry its own.\n"
   }
  }
 },
 "AiPolicyException": {
  "type": "object",
  "x-ticvai-persistence": "ai.policy_exception",
  "description": "**A temporary, recorded exception to a governance policy** (AIC-162, ADM-526): an expiry, an approver and compensating controls. Governance is never bypassed silently.",
  "required": [
   "policyId",
   "reason",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "policyId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.governance_policy"
   },
   "capabilityKey": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "maxLength": 2000
   },
   "compensatingControls": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "startsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "Required. An exception with no end is a policy change, and goes through publication."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "expired",
     "revoked"
    ],
    "readOnly": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "revokedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "revokeReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRiskClass": {
  "type": "string",
  "enum": [
   "low",
   "medium",
   "high",
   "critical"
  ],
  "description": "Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."
 },
 "AiUsageReport": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from ai.activity",
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
      "cost": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
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
   },
   "forecast": {
    "type": "object",
    "nullable": true,
    "description": "**A month-end projection, labelled a forecast** (AI design 2.3, 4.5). Present where `to` is inside the current month. Never added into `rows`.\n",
    "properties": {
     "label": {
      "type": "string",
      "enum": [
       "forecast"
      ]
     },
     "periodEnd": {
      "type": "string",
      "format": "date"
     },
     "projectedTokens": {
      "type": "integer"
     },
     "projectedCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "basis": {
      "type": "string",
      "description": "How it was projected, e.g. the run rate of the last 7 days."
     }
    }
   }
  }
 },
 "AuditRecord": {
  "x-ticvai-append-only": "occurredAt",
  "type": "object",
  "x-ticvai-persistence": "platform.audit_record",
  "description": "26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n",
  "required": [
   "id",
   "action",
   "occurredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "Who acted."
   },
   "orgUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The scope node the action happened in."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The workstation it was done from, where there was one."
   },
   "action": {
    "type": "string",
    "description": "What was done, as the writing operation names it."
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time",
    "description": "When. The list is ordered by this, most recent first."
   },
   "platformStaffGrantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"
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
     },
     "sentCount": {
      "type": "integer",
      "readOnly": true,
      "x-ticvai-persisted": false,
      "description": "**How many messages went out**, counted from `marketing.message_dispatch` at read time rather than kept as a counter on the campaign row, so it cannot drift from the dispatch records it summarises. Test sends are not dispatches of the campaign and are not counted.\n"
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
    "description": "Fallback values for the template's `mergeFields`, by name, used where a guest has no value.",
    "additionalProperties": {
     "type": "string"
    }
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
     "inactivity",
     "entitlementExpiring"
    ],
    "description": "`entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's `expiryNoticeDays` of `validTo`. The notice period is set on the template, so `delayHours` shifts the send within it rather than setting it. An entitlement belonging to a membership is left to `membershipExpiring`, so a member is not told twice."
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
   },
   "sendTimeMode": {
    "type": "string",
    "enum": [
     "fixed",
     "optimised"
    ],
    "default": "fixed",
    "description": "`optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). `fixed` is the behaviour before. Falls back to `scheduledFor` per recipient where there is no suggestion or AI is off."
   },
   "optimiseChannel": {
    "type": "boolean",
    "default": false,
    "description": "With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). Off keeps `channel`."
   },
   "variants": {
    "type": "array",
    "maxItems": 5,
    "nullable": true,
    "description": "**A/B (or up to five-way) content and subject variants** (29 September, build pass, group G2; 22.1.17, BO-772). Each is a subject override and optionally a different template, written by a person or taken from an AI draft (`ai.proposeMarketingContent`, `source` `aiDraft`). Held as rows of `marketing.campaign_variant`. Null or empty is a single-content campaign.",
    "items": {
     "$ref": "#/components/schemas/MarketingCampaignVariant"
    }
   },
   "abTest": {
    "type": "object",
    "nullable": true,
    "description": "How the variants are tested. Required when `variants` has two or more.",
    "properties": {
     "testPercent": {
      "type": "integer",
      "minimum": 5,
      "maximum": 100,
      "default": 20,
      "description": "Share of the audience the variants are tested on; 100 splits everyone and picks no winner."
     },
     "successMetric": {
      "type": "string",
      "enum": [
       "openRate",
       "clickRate",
       "conversionRate",
       "attributedRevenue"
      ],
      "default": "clickRate"
     },
     "decideAfterHours": {
      "type": "integer",
      "minimum": 1,
      "maximum": 168,
      "default": 4
     },
     "winnerRule": {
      "type": "string",
      "enum": [
       "automatic",
       "manual"
      ],
      "default": "automatic"
     },
     "minimumSamplePerVariant": {
      "type": "integer",
      "minimum": 1,
      "default": 500,
      "description": "Below this many sends per variant no winner is declared automatically; a person picks."
     },
     "winningVariantId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "Set by the automatic rule, or by a person through `updateCampaign`."
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
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**Added 29 September (AI design 3.1):** `ai.index_failure` had no scope column and no declared owner, so no policy. The indexed source's scope, copied when the failure is written.\n"
   }
  }
 },
 "KpiValue": {
  "type": "object",
  "description": "BI board 10.3. **Value, target, variance, direction and freshness in one read.**",
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "bucketStart": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."
   },
   "groupKey": {
    "type": "string",
    "nullable": true,
    "description": "The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "period": {
    "type": "string"
   },
   "value": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "target": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "comparison": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "variancePercent": {
    "type": "number",
    "nullable": true
   },
   "direction": {
    "type": "string",
    "enum": [
     "up",
     "down",
     "flat"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "green",
     "amber",
     "red",
     "noTarget"
    ]
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "stale": {
    "type": "boolean",
    "description": "**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"
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
    "readOnly": true,
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
    "format": "date-time",
    "description": "**Device time** — `recordLostItem` is offline-capable, so this is when the loss was reported or the find handed in, not when the device synced. The `recorded_at` of naming-and-style 5.2 for this row.\n"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the record arrived. Equal to `reportedAt` for one recorded online."
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
    "readOnly": true,
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
   "matchedItemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The other side of the match — set by `matchLostItem` `match` (to `otherItemId`) and cleared by `unmatch`, on both items."
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The case the guest raised about it (`raiseMyCase` with `kind` `lostProperty`), where there is one."
   },
   "disposeAfter": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "**A retention date, because unclaimed property has one.** A storeroom with no disposal date is a storeroom that fills, and the date is a venue policy rather than a default.\n"
   }
  }
 },
 "MarketingCampaignVariant": {
  "type": "object",
  "x-ticvai-persistence": "marketing.campaign_variant",
  "description": "One content or subject variant of a campaign, for an A/B test (22.1.17; 29 September, build pass, group G2, from group G1's handoff). Written with its campaign by `createCampaign` and `updateCampaign`.",
  "required": [
   "label"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "campaignId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "marketing.campaign"
   },
   "label": {
    "type": "string",
    "maxLength": 20,
    "description": "A, B, C..."
   },
   "subjectOverride": {
    "type": "object",
    "nullable": true,
    "description": "Subject line by locale.",
    "additionalProperties": {
     "type": "string"
    }
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A different template for this variant; null uses the campaign's `content.templateId`."
   },
   "splitPercent": {
    "type": "integer",
    "minimum": 1,
    "maximum": 100,
    "nullable": true,
    "description": "Share of the test group; null splits evenly."
   },
   "source": {
    "type": "string",
    "enum": [
     "manual",
     "aiDraft"
    ],
    "default": "manual"
   },
   "aiDecisionRecordId": {
    "type": "string",
    "nullable": true,
    "description": "The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`."
   },
   "isWinner": {
    "type": "boolean",
    "default": false,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005), the campaign's."
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
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
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
 "Permission": {
  "type": "string",
  "enum": [
   "SESSION_FORCE_LOGOUT",
   "USER_MANAGE",
   "ROLE_MANAGE",
   "PERMISSION_GRANT",
   "PERMISSION_VIEW",
   "PERMISSION_MANAGE",
   "PLATFORM_TENANT_VIEW",
   "PLATFORM_TENANT_MANAGE",
   "PLATFORM_TENANT_TERMINATE",
   "PLATFORM_PLAN_MANAGE",
   "PLATFORM_CELL_VIEW",
   "PLATFORM_CELL_MANAGE",
   "PLATFORM_BILLING_VIEW",
   "PLATFORM_AI_MANAGE",
   "PLATFORM_BILLING_MANAGE",
   "PLATFORM_RELEASE_VIEW",
   "PLATFORM_RELEASE_MANAGE",
   "PLATFORM_RELEASE_PROMOTE",
   "PLATFORM_MIGRATION_VIEW",
   "PLATFORM_MIGRATION_APPLY",
   "PLATFORM_TENANT_ACCESS",
   "TENANT_CONFIGURE",
   "TENANT_VIEW",
   "TENANT_PUBLISH",
   "SCOPE_VIEW",
   "SCOPE_MANAGE",
   "REGION_CONFIGURE",
   "WORKSTATION_CONFIGURE",
   "PRODUCT_VIEW",
   "PRODUCT_CONFIGURE",
   "PRODUCT_APPROVE",
   "PRODUCT_PUBLISH",
   "PRICE_VIEW",
   "PRICE_CONFIGURE",
   "EVENT_CONFIGURE",
   "PERFORMANCE_CONFIGURE",
   "CAPACITY_CONFIGURE",
   "ORDER_VIEW",
   "ORDER_VIEW_OTHER",
   "ORDER_CREATE",
   "ORDER_MODIFY",
   "ORDER_DISCOUNT",
   "ORDER_CANCEL",
   "ORDER_VOID",
   "ORDER_REFUND",
   "ORDER_REFUND_APPROVE",
   "ORDER_REFUND_BULK",
   "ORDER_EXCHANGE",
   "ORDER_RESCHEDULE",
   "ORDER_REPRINT",
   "PRICE_OVERRIDE",
   "DISCOUNT_APPLY",
   "CREDIT_MANAGE",
   "CREDIT_OVERRIDE",
   "WALLET_VIEW",
   "WALLET_OPERATE",
   "WALLET_CONFIGURE",
   "PAYMENT_VIEW",
   "PAYMENT_CONFIGURE",
   "PAYMENT_PROVIDER_MANAGE",
   "PAYMENT_DISPUTE",
   "SHIFT_OPEN",
   "SHIFT_CLOSE",
   "SHIFT_SUSPEND",
   "SHIFT_CLOSE_OTHER",
   "SHIFT_APPROVE_OPEN",
   "SHIFT_APPROVE_CLOSE",
   "SHIFT_REOPEN",
   "CASH_LIFT",
   "CASH_ADD",
   "CASH_NO_SALE",
   "DEPOSIT_BOX_MODIFY_OWN",
   "DEPOSIT_BOX_MODIFY_OTHER",
   "OVERSHORT_ACCEPT",
   "ACCESS_VALIDATE",
   "ACCESS_OVERRIDE",
   "ACCESS_POINT_CONFIGURE",
   "TURNSTILE_MODE_SET",
   "TICKET_LOOKUP",
   "ACCREDITATION_VIEW",
   "ACCREDITATION_APPLY",
   "ACCREDITATION_APPROVE",
   "ACCREDITATION_ISSUE",
   "ACCREDITATION_MANAGE",
   "ACCREDITATION_CONFIGURE",
   "REPORT_VIEW_OWN",
   "REPORT_VIEW_WORKSTATION",
   "REPORT_VIEW_VENUE",
   "REPORT_VIEW_REGION",
   "REPORT_VIEW_TENANT",
   "REPORT_EXPORT",
   "REPORT_EXPORT_PII",
   "REPORT_MANAGE",
   "REPORT_SCHEDULE",
   "LEDGER_VIEW",
   "LEDGER_POST",
   "LEDGER_APPROVE",
   "TAX_CONFIGURE",
   "ACCOUNT_CONFIGURE",
   "SETTLEMENT_VIEW",
   "SETTLEMENT_RECONCILE",
   "GUEST_VIEW",
   "GUEST_VIEW_PII",
   "GUEST_MANAGE",
   "VENUE_MAP_VIEW",
   "VENUE_MAP_MANAGE",
   "VENUE_MAP_PUBLISH",
   "RESOURCE_VIEW",
   "RESOURCE_BOOK",
   "RESOURCE_MANAGE",
   "RESOURCE_CONFIGURE",
   "RENTAL_VIEW",
   "RENTAL_BOOK",
   "RENTAL_OPERATE",
   "RENTAL_MANAGE",
   "RENTAL_CONFIGURE",
   "RENTAL_PRICE",
   "RENTAL_APPROVE",
   "RENTAL_OVERRIDE",
   "DEVELOPER_VIEW",
   "DEVELOPER_MANAGE",
   "DEVELOPER_ADMIN",
   "LOYALTY_ACCRUE",
   "LOYALTY_REDEEM",
   "LOYALTY_ADJUST",
   "MARKETING_VIEW",
   "MARKETING_MANAGE",
   "MARKETING_SEND",
   "CASE_VIEW",
   "CASE_MANAGE",
   "ASSET_LIBRARY_VIEW",
   "ASSET_LIBRARY_MANAGE",
   "ASSET_LIBRARY_APPROVE",
   "ASSET_LIBRARY_SHARE",
   "QUEUE_VIEW",
   "QUEUE_MANAGE",
   "QUEUE_REDEEM",
   "QUEUE_OVERRIDE",
   "TRANSPORT_VIEW",
   "TRANSPORT_MANAGE",
   "TRANSPORT_PRICE",
   "ASSET_VIEW",
   "ASSET_MANAGE",
   "WORK_ORDER_VIEW",
   "WORK_ORDER_MANAGE",
   "WORK_ORDER_VERIFY",
   "INSPECTION_VIEW",
   "INSPECTION_SUBMIT",
   "INSPECTION_MANAGE",
   "INCIDENT_REPORT",
   "INCIDENT_VIEW",
   "INCIDENT_MANAGE",
   "KIOSK_ATTEND",
   "DEVICE_VIEW",
   "DEVICE_CONFIGURE",
   "DEVICE_MANAGE",
   "APPROVAL_ACT",
   "APPROVAL_DELEGATE",
   "AI_USE",
   "AI_CONFIGURE",
   "AI_APPROVE",
   "AI_AUDIT_VIEW",
   "RISK_REVIEW",
   "RISK_INVESTIGATE",
   "AUDIT_VIEW",
   "APPROVAL_VIEW",
   "APPROVAL_REQUEST",
   "APPROVAL_DECIDE",
   "APPROVAL_CONFIGURE",
   "MAINTENANCE_EXECUTE",
   "MAINTENANCE_APPROVE",
   "WORKFORCE_VIEW",
   "WORKFORCE_MANAGE",
   "ATTENDANCE_RECORD",
   "ANNOUNCEMENT_PUBLISH",
   "ANNOUNCEMENT_EMERGENCY",
   "PARTNER_VIEW",
   "PARTNER_MANAGE",
   "PARKING_CONFIGURE",
   "PAYMENT_VOID",
   "PROCUREMENT_VIEW",
   "PROCUREMENT_REQUEST",
   "PROCUREMENT_MANAGE",
   "PROCUREMENT_RECEIVE"
  ]
 },
 "PermissionSet": {
  "type": "array",
  "items": {
   "$ref": "#/components/schemas/Permission"
  },
  "uniqueItems": true
 },
 "PlatformStaffGrant": {
  "type": "object",
  "x-ticvai-persistence": "identity.platform_staff_grant",
  "description": "**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n",
  "required": [
   "id",
   "operatorPrincipalId",
   "permissions",
   "reason",
   "openedAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The platform operator, from the Control Plane token. Set by the server."
   },
   "operatorDisplayName": {
    "type": "string",
    "readOnly": true
   },
   "permissions": {
    "type": "array",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/Permission"
    }
   },
   "reason": {
    "type": "string"
   },
   "ticketRef": {
    "type": "string",
    "nullable": true
   },
   "openedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The tenant root. **Operations write it at `tenant` scope**; the server sets it."
   }
  }
 },
 "ScopedPermissions": {
  "type": "object",
  "description": "Permissions effective at a given scope path, after deny resolution. Clients filter navigation on this and never compute permissions themselves.\n",
  "required": [
   "scopePath",
   "permissions"
  ],
  "properties": {
   "scopePath": {
    "type": "string",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$"
   },
   "permissions": {
    "$ref": "#/components/schemas/PermissionSet"
   }
  }
 },
 "SuggestionProviderAssignments": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**The routing table for `requestSuggestion`, held on the tenant's `ai.policy` row** as one `jsonb` column (`suggestion_providers`). At most one entry per `kind`.\n",
  "items": {
   "$ref": "#/components/schemas/SuggestionProviderAssignment"
  }
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `setVenueSettings`."
   },
   "calendarDayStartHour": {
    "type": "integer",
    "minimum": 0,
    "maximum": 23,
    "nullable": true,
    "default": 6,
    "description": "**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "readOnly": true,
    "description": "**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "nullable": true,
    "readOnly": true,
    "description": "**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"
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
      "type": "string",
      "description": "IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"
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
         "type": "string",
         "description": "Wall-clock time the desk opens."
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time the desk closes."
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
      "type": "string",
      "description": "Wall-clock time sending stops",
      "in the region's time zone.": null
     },
     "to": {
      "type": "string",
      "description": "Wall-clock time sending resumes",
      "in the region's time zone.": null
     }
    }
   },
   "biometrics": {
    "type": "object",
    "nullable": true,
    "description": "CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false,
      "description": "**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"
     },
     "dpiaReference": {
      "type": "string",
      "nullable": true,
      "maxLength": 200,
      "description": "**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"
     },
     "consentNoticeAcknowledgedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"
     },
     "acknowledgedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "readOnly": true,
      "description": "**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"
     },
     "faceTagPurgeMinutesAfterClose": {
      "type": "integer",
      "nullable": true,
      "default": 0,
      "description": "BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"
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
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
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
       "off",
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": "off",
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
   },
   "displayCurrencies": {
    "type": "array",
    "nullable": true,
    "description": "**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{3}$"
    }
   },
   "cartLeaseSeconds": {
    "type": "integer",
    "nullable": true,
    "minimum": 30,
    "maximum": 3600,
    "default": 900,
    "description": "**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"
   },
   "cartHoldExtensionMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 30,
    "default": 5,
    "description": "How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."
   },
   "cartMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."
   },
   "resaleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 168,
    "default": 24,
    "description": "Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."
   },
   "exchangeCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."
   },
   "rescheduleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."
   },
   "reservationMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."
   },
   "shiftVarianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"
   },
   "catalogue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxVariantsPerProduct": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 2000,
      "default": 200,
      "description": "Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."
     },
     "waitlistOfferHoldMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 1440,
      "default": 30,
      "description": "How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 10,
      "description": "A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationCount": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 50,
      "description": "A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     }
    }
   },
   "inventory": {
    "type": "object",
    "nullable": true,
    "properties": {
     "overReceiptTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 5,
      "description": "Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."
     },
     "countVarianceTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 2,
      "description": "Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."
     },
     "countVarianceApprovalAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"
     }
    }
   },
   "seating": {
    "type": "object",
    "nullable": true,
    "properties": {
     "seatHoldExtensionSeconds": {
      "type": "integer",
      "nullable": true,
      "minimum": 60,
      "maximum": 1800,
      "default": 300,
      "description": "What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."
     },
     "seatHoldMaxExtensions": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 5,
      "default": 2,
      "description": "How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."
     },
     "maxSeatsPerGuestOrder": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 50,
      "default": 10,
      "description": "**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"
     }
    }
   },
   "promotions": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxDiscountPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 30,
      "description": "The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."
     },
     "nearZeroLinePrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"
     }
    }
   },
   "fnb": {
    "type": "object",
    "nullable": true,
    "properties": {
     "recallWindowMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 60,
      "default": 10,
      "description": "Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."
     },
     "compEscalationAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"
     },
     "foodSafetyLeadPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"
     }
    }
   },
   "queue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "crossQueueLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 10,
      "default": 2,
      "description": "Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "reporting": {
    "type": "object",
    "nullable": true,
    "properties": {
     "inlineRunRowLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1000,
      "maximum": 100000,
      "default": 5000,
      "description": "Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."
     },
     "dashboardRefreshBudgetPerMinute": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 24,
      "description": "Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."
     }
    }
   },
   "marketing": {
    "type": "object",
    "nullable": true,
    "properties": {
     "attributionWindowDays": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 30,
      "default": 7,
      "description": "Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "identity": {
    "type": "object",
    "nullable": true,
    "properties": {
     "guestOtpMaxAttempts": {
      "type": "integer",
      "nullable": true,
      "minimum": 3,
      "maximum": 10,
      "default": 5,
      "description": "Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"
     },
     "guestTwoStep": {
      "type": "object",
      "nullable": true,
      "description": "**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n",
      "properties": {
       "enabled": {
        "type": "boolean",
        "default": false,
        "description": "Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."
       },
       "stepUpActions": {
        "type": "array",
        "uniqueItems": true,
        "description": "The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n",
        "items": {
         "type": "string",
         "enum": [
          "changeContactDetails",
          "changePassword",
          "managePaymentMethods",
          "transferTickets",
          "deleteAccount"
         ]
        },
        "default": [
         "changeContactDetails",
         "changePassword",
         "managePaymentMethods",
         "deleteAccount"
        ]
       }
      }
     }
    }
   }
  }
 }
}
```
