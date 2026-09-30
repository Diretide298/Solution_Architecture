# WS177 — Seat Management Venue Mapping Reference v1.0 board 13

**10 screens · 11 operations · 17 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `APPROVAL_REQUEST, CAPACITY_CONFIGURE, DEVELOPER_MANAGE, DEVELOPER_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1071` | Integration Command Center | listDetail | 1 | 0 | — |
| `BO-1072` | Seat Management APIs | listDetail | 1 | 0 | — |
| `BO-1073` | API Access & OAuth | listDetail | 4 | 0 | — |
| `BO-1074` | Webhook Configuration | listDetail | 3 | 0 | — |
| `BO-1075` | Seat Event Catalog | listDetail | 1 | 0 | — |
| `BO-1076` | Concurrency, Idempotency & Limits | listDetail | 1 | 0 | — |
| `BO-1077` | Mapping & Transformation | listDetail | 1 | 0 | — |
| `BO-1078` | Monitoring, Retry & Reconciliation | listDetail | 1 | 0 | — |
| `BO-1079` | Immutable Seat Audit Logs | listDetail | 1 | 0 | — |
| `BO-1080` | Integration Approval & Compliance | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-1071, BO-1072, BO-1074, BO-1075, BO-1076, BO-1077, BO-1078, BO-1080 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1071",
  "name": "Integration Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "01",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/integration-command-center-bo-1071",
   "component": "apps/venue-management-web/src/routes/access-venue/IntegrationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1072",
    "BO-1073",
    "BO-1074",
    "BO-1075",
    "BO-1076",
    "BO-1077",
    "BO-1078",
    "BO-1079",
    "BO-1080"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1072",
     "trigger": "Seat Management APIs",
     "provenance": "structural — pack board 13 wiring, 19 September 2026"
    },
    {
     "to": "BO-1073",
     "trigger": "API Access & OAuth",
     "provenance": "structural — pack board 13 wiring, 19 September 2026"
    },
    {
     "to": "BO-1074",
     "trigger": "Webhook Configuration",
     "provenance": "structural — pack board 13 wiring, 19 September 2026"
    },
    {
     "to": "BO-1075",
     "trigger": "Seat Event Catalog",
     "provenance": "structural — pack board 13 wiring, 19 September 2026"
    },
    {
     "to": "BO-1076",
     "trigger": "Concurrency, Idempotency & Limits",
     "provenance": "structural — pack board 13 wiring, 19 September 2026"
    },
    {
     "to": "BO-1077",
     "trigger": "Mapping & Transformation",
     "provenance": "structural — pack board 13 wiring, 19 September 2026"
    },
    {
     "to": "BO-1078",
     "trigger": "Monitoring, Retry & Reconciliation",
     "provenance": "structural — pack board 13 wiring, 19 September 2026"
    },
    {
     "to": "BO-1079",
     "trigger": "Immutable Seat Audit Logs",
     "provenance": "structural — pack board 13 wiring, 19 September 2026"
    },
    {
     "to": "BO-1080",
     "trigger": "Integration Approval & Compliance",
     "provenance": "structural — pack board 13 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor all seat API and webhook consumers from one place. Show request volume, success, latency, failures, retries, active consumers, versions and security alerts. Compare tenant, venue, application, endpoint, event, environment and time period. Surface deprecated clients, abnormal traffic, delivery backlog and reconciliation failures with owner and action. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 54"
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
       "impliedBy": "listApiClients",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The integration list.",
   "error": "Could not load. Names which read failed and leaves the integration untouched.",
   "emptyFirstRun": "No integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "Integrations connected",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1071",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1071"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1072",
  "name": "Seat Management APIs",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "02",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-management-apis-bo-1072",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatManagementApis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1071"
   ],
   "exitTo": [
    "BO-1071"
   ],
   "transitions": [
    {
     "to": "BO-1071",
     "trigger": "Back to Integration Command Center",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Publish a governed catalog of supported seat endpoints. Document APIs for maps/layouts, availability, locks, holds, reservations, allocations, sales and seat history. Show method, path, version, scope, request/response schema, errors, examples, limits and deprecation date. Provide sandbox testing and prevent production calls until client, scopes and integration approval are active. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 54"
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
       "impliedBy": "listSeatMaps",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seat apis list.",
   "error": "Could not load. Names which read failed and leaves the seat apis untouched.",
   "emptyFirstRun": "No seat apis yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat apis are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatMaps",
    "contract": "seating",
    "purpose": "What the seat API exposes",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1072",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1072"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1073",
  "name": "API Access & OAuth",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "03",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/api-access-oauth-bo-1073",
   "component": "apps/venue-management-web/src/routes/access-venue/ApiAccessOauth.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1071"
   ],
   "exitTo": [
    "BO-1071"
   ],
   "transitions": [
    {
     "to": "BO-1071",
     "trigger": "Back to Integration Command Center",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage machine and delegated access to seat services. Register confidential/public clients with tenant, environment, owner, redirect/callback and application purpose. Configure OAuth grant, scopes, token lifetime, mTLS/IP restriction, secret/certificate rotation and revocation. Display secret metadata without exposing stored secret values and audit credential and scope changes. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Configuration Scope of Work | Version 1.0 54 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 54"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Scopes, by module",
       "bindsTo": "ApiScope",
       "operation": "listApiScopes",
       "notes": "**A scope picker grouped by module** (M17-05): `{module}.read` and `{module}.write`, with unlicensed modules shown and disabled rather than hidden. No scope opens a catalogue write (M17-04).",
       "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
      },
      {
       "kind": "banner",
       "label": "Production access",
       "bindsTo": "ProductionAccessRequest",
       "operation": "listProductionAccessRequests",
       "notes": "**Where production access stands** (M17-06): sandbox only, requested (pending), approved (a production client issued by TICVAI) or rejected with the reason. Production keys only after certification; a sandbox key is never promoted.",
       "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listApiClients",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createApiClient",
       "label": "Create API client",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createApiClient"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The api access oauth list.",
   "error": "Could not load. Names which read failed and leaves the api access oauth untouched.",
   "emptyFirstRun": "No api access oauth yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the api access oauth are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApiScopes",
    "contract": "public-api",
    "purpose": "Scopes to choose from, by module",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
   },
   {
    "operationId": "listProductionAccessRequests",
    "contract": "public-api",
    "purpose": "Where production access stands for these clients",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, 17 September minutes M17-05/M17-06 (applied 30 September)"
   },
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "Access and OAuth",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createApiClient",
    "contract": "public-api",
    "purpose": "Issue credentials",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1073",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1073"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1074",
  "name": "Webhook Configuration",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "04",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/webhook-configuration-bo-1074",
   "component": "apps/venue-management-web/src/routes/access-venue/WebhookConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1071"
   ],
   "exitTo": [
    "BO-1071"
   ],
   "transitions": [
    {
     "to": "BO-1071",
     "trigger": "Back to Integration Command Center",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow approved consumers to subscribe to seat lifecycle events. Select events, tenant/venue scope, destination, method, content type, version and filtering conditions. Configure HMAC signature, signing-key rotation, timeout, retry, ordering, batching and dead-letter policy. Test challenge and sample delivery, verify endpoint ownership and block activation until security checks pass. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 55"
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
       "impliedBy": "listWebhookSubscriptions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows. Lists the tenant's subscriptions; an API client filter passes `?clientId=` (decided 28 September, audit R214 (4))."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createWebhookSubscription",
       "label": "Create webhook subscription",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createWebhookSubscription"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The webhook list.",
   "error": "Could not load. Names which read failed and leaves the webhook untouched.",
   "emptyFirstRun": "No webhook yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the webhook are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWebhookSubscriptions",
    "contract": "public-api",
    "purpose": "Webhooks configured",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createWebhookSubscription",
    "contract": "public-api",
    "purpose": "Subscribe",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listWebhookEventTypes",
    "contract": "public-api",
    "purpose": "Events a subscription can take",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1074",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1074"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 55. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1075",
  "name": "Seat Event Catalog",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "05",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-event-catalog-bo-1075",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatEventCatalog.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1071"
   ],
   "exitTo": [
    "BO-1071"
   ],
   "transitions": [
    {
     "to": "BO-1071",
     "trigger": "Back to Integration Command Center",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the versioned events emitted by the seat platform. Catalog map/layout published, availability changed, seat locked/unlocked, held/released, reserved, sold and blocked events. Show schema, required tenant/venue/performance/seat identifiers, timestamp, version and correlation metadata. Manage backward compatibility, deprecation, sample payload and consumer impact for schema changes. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 55"
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
       "impliedBy": "listApiVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seat event catalog list.",
   "error": "Could not load. Names which read failed and leaves the seat event catalog untouched.",
   "emptyFirstRun": "No seat event catalog yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat event catalog are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWebhookEventTypes",
    "contract": "public-api",
    "purpose": "The seat event catalogue (publisher=seating)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1075",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1075"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 55. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1076",
  "name": "Concurrency, Idempotency & Limits",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "06",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/concurrency-idempotency-limits-bo-1076",
   "component": "apps/venue-management-web/src/routes/access-venue/ConcurrencyIdempotencyLimits.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1071"
   ],
   "exitTo": [
    "BO-1071"
   ],
   "transitions": [
    {
     "to": "BO-1071",
     "trigger": "Back to Integration Command Center",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure technical controls that prevent duplicate or conflicting inventory actions. Define expected version/ETag, lock token, conflict response and retry boundary for write operations. Require idempotency key, retention window and duplicate-response behavior for supported commands. Set rate, burst, connection, read/write timeout and payload limits by client, endpoint and environment. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 55"
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
       "impliedBy": "listApiClients",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The concurrency idempotency limits list.",
   "error": "Could not load. Names which read failed and leaves the concurrency idempotency limits untouched.",
   "emptyFirstRun": "No concurrency idempotency limits yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the concurrency idempotency limits are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApiClients",
    "contract": "public-api",
    "purpose": "Limits and idempotency",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1076",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1076"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 55. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1077",
  "name": "Mapping & Transformation",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "07",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/mapping-transformation-bo-1077",
   "component": "apps/venue-management-web/src/routes/access-venue/MappingTransformation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1071"
   ],
   "exitTo": [
    "BO-1071"
   ],
   "transitions": [
    {
     "to": "BO-1071",
     "trigger": "Back to Integration Command Center",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Map external partner fields and codes to TICVAI canonical seat entities. Configure source-to-target identifiers, status/category code mapping, value transformation and defaults. Validate data type, required field, tenant/venue context, referential integrity and unsupported values. Provide test payload, expected result, versioning and safe rollback without modifying the canonical model. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 55",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 55"
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
       "impliedBy": "listWebhookSubscriptions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The mapping transformation list.",
   "error": "Could not load. Names which read failed and leaves the mapping transformation untouched.",
   "emptyFirstRun": "No mapping transformation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the mapping transformation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWebhookSubscriptions",
    "contract": "public-api",
    "purpose": "Mapping and transformation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1077",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1077"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 55. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1078",
  "name": "Monitoring, Retry & Reconciliation",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "08",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/monitoring-retry-reconciliation-bo-1078",
   "component": "apps/venue-management-web/src/routes/access-venue/MonitoringRetryReconciliation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1071"
   ],
   "exitTo": [
    "BO-1071"
   ],
   "transitions": [
    {
     "to": "BO-1071",
     "trigger": "Back to Integration Command Center",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Operate API and event delivery reliably through failure. Trace request or webhook by correlation ID with attempts, response, latency, signature and processing outcome. Configure retry/backoff, retryable errors, expiry, dead-letter queue, replay authority and alert thresholds. Reconcile consumer acknowledgment or downstream state with Seat Inventory and record compensating action. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 56"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 56"
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
       "impliedBy": "listWebhookDeliveries",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The monitoring retry reconciliation list.",
   "error": "Could not load. Names which read failed and leaves the monitoring retry reconciliation untouched.",
   "emptyFirstRun": "No monitoring retry reconciliation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the monitoring retry reconciliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWebhookDeliveries",
    "contract": "public-api",
    "purpose": "Delivery, retry and reconciliation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1078",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1078"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 56. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "subscriptionId",
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
  "id": "BO-1079",
  "name": "Immutable Seat Audit Logs",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "09",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/immutable-seat-audit-logs-bo-1079",
   "component": "apps/venue-management-web/src/routes/access-venue/ImmutableSeatAuditLogs.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1071"
   ],
   "exitTo": [
    "BO-1071"
   ],
   "transitions": [
    {
     "to": "BO-1071",
     "trigger": "Back to Integration Command Center",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide searchable tamper-evident evidence for seat data and administrative actions. Record actor/client, tenant, venue, event, entity, action, before/after, reason, source IP/device and timestamp. Store API request/event correlation, rule/version, approval, outcome and related transaction references. Support permission-controlled search and export, retention/legal hold and integrity verification without log alteration. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 56"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Performance",
       "operation": "getSeatReconciliation",
       "notes": "Sends `?performanceId=` (required) to the one bound read, which returns discrepancies, not audit entries.",
       "provenance": "contract seating.yaml GET /seat-reconciliation"
      },
      {
       "kind": "searchField",
       "label": "Search the audit log",
       "notes": "Actor, entity, action, correlation ID. No audit-log read is bound.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 56"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Seat audit entries",
       "columns": [
        "Timestamp",
        "Actor / client",
        "Tenant",
        "Venue",
        "Event",
        "Entity",
        "Action",
        "Before",
        "After",
        "Reason",
        "Source IP / device",
        "Correlation ID",
        "Rule / version",
        "Approval",
        "Outcome"
       ],
       "notes": "The pack's record; no operation returns it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 56"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Related discrepancy",
       "bindsTo": "SeatDiscrepancy",
       "columns": [
        "SeatDiscrepancy.seatId",
        "SeatDiscrepancy.label",
        "SeatDiscrepancy.kind",
        "SeatDiscrepancy.mapState",
        "SeatDiscrepancy.orderState",
        "SeatDiscrepancy.orderIds",
        "SeatDiscrepancy.detectedAt"
       ],
       "operation": "getSeatReconciliation",
       "notes": "The only thing the bound read offers: a discrepancy linked to the audited seat.",
       "provenance": "contract seating.yaml GET /seat-reconciliation"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Export",
       "notes": "Permission-controlled; no export operation is bound.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 56"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The immutable seat audit list.",
   "error": "Could not load. Names which read failed and leaves the immutable seat audit untouched.",
   "emptyFirstRun": "No immutable seat audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the immutable seat audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatReconciliation",
    "contract": "seating",
    "purpose": "Seat audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1079",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1079"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 56. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.56; contract seating.yaml GET /seat-reconciliation. Pack labels with no schema field yet (shown as plain labels): Seat audit-log read (bound op is getSeatReconciliation), Actor / client, Entity, Action, Before / after, Reason, Source IP / device, Correlation ID, Rule / version, Approval, Outcome, Integrity verification status.",
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
  "id": "BO-1080",
  "name": "Integration Approval & Compliance",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "13",
   "number": "10",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/integration-approval-compliance-bo-1080",
   "component": "apps/venue-management-web/src/routes/access-venue/IntegrationApprovalCompliance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1071"
   ],
   "exitTo": [
    "BO-1071"
   ],
   "transitions": [
    {
     "to": "BO-1071",
     "trigger": "Back to Integration Command Center",
     "provenance": "structural — pack board 13 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern production activation and ongoing compliance of each integration. Route security review, data classification, privacy, architecture, performance and business-owner approval. Attach sandbox results, contract tests, load/security tests, rollback plan, support ownership and incident contacts. Issue time-bound approval, require periodic review and export a controlled compliance evidence package. All writes require authenticated, authorized, idempotent and concurrency-safe requests; events and audit records carry tenant, version and correlation context and are retained under approved policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 56",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 56"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 56"
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
       "impliedBy": "createApprovalRequest",
       "label": "Create approval request",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The integration approval compliance list.",
   "error": "Could not load. Names which read failed and leaves the integration approval compliance untouched.",
   "emptyFirstRun": "No integration approval compliance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the integration approval compliance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createApprovalRequest",
    "contract": "approvals",
    "purpose": "Integration approval",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1080",
   "workshopBoard": "wireframes/WS152 Seat Management Venue Mapping Reference v1.0 Board 13.dc.html#bo-1080"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 56. 0 of 0 labels bound to a contract property; 0 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createApiClient": {
  "method": "POST",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Create a client with scopes and an environment",
  "permission": "DEVELOPER_MANAGE",
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
  "requestBody": "ApiClient",
  "responds": null
 },
 "createApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Raise a request",
  "permission": "APPROVAL_REQUEST",
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
  "requestBody": "CreateApprovalRequest",
  "responds": "ApprovalRequest"
 },
 "createWebhookSubscription": {
  "method": "POST",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "Subscribe to business events",
  "permission": "DEVELOPER_MANAGE",
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
  "requestBody": "WebhookSubscription",
  "responds": "WebhookSubscription"
 },
 "getSeatReconciliation": {
  "method": "GET",
  "path": "/seat-reconciliation",
  "contract": "seating",
  "summary": "The map against the orders, seat by seat",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "SeatDiscrepancy"
 },
 "listApiClients": {
  "method": "GET",
  "path": "/api-clients",
  "contract": "public-api",
  "summary": "Registered clients for this developer",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ApiClient"
 },
 "listApiScopes": {
  "method": "GET",
  "path": "/api-scopes",
  "contract": "public-api",
  "summary": "The scope catalogue, one read and one write scope per module",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "module",
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
 "listProductionAccessRequests": {
  "method": "GET",
  "path": "/production-access-requests",
  "contract": "public-api",
  "summary": "Production access requests, pending first",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "listSeatMaps": {
  "method": "GET",
  "path": "/seat-maps",
  "contract": "seating",
  "summary": "List seat maps",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
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
 "listWebhookDeliveries": {
  "method": "GET",
  "path": "/webhook-subscriptions/{subscriptionId}/deliveries",
  "contract": "public-api",
  "summary": "What was sent, what failed, and why",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "WebhookDelivery"
 },
 "listWebhookEventTypes": {
  "method": "GET",
  "path": "/webhook-event-types",
  "contract": "public-api",
  "summary": "The events a webhook may subscribe to",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "publisher",
    "in": "query",
    "required": false
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
 "listWebhookSubscriptions": {
  "method": "GET",
  "path": "/webhook-subscriptions",
  "contract": "public-api",
  "summary": "The tenant's webhook subscriptions, filterable by API client",
  "permission": "DEVELOPER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "clientId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WebhookSubscription"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApiClient": {
  "type": "object",
  "x-ticvai-persistence": "control.api_client",
  "description": "CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n",
  "required": [
   "id",
   "developerId",
   "name",
   "environment",
   "scopes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "clientId": {
    "type": "string",
    "readOnly": true
   },
   "environment": {
    "type": "string",
    "enum": [
     "sandbox",
     "production"
    ],
    "description": "**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"
   },
   "scopes": {
    "type": "array",
    "description": "**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n",
    "items": {
     "type": "string",
     "pattern": "^[a-zA-Z]+\\.(read|write)$"
    }
   },
   "issuedBy": {
    "type": "string",
    "enum": [
     "partner",
     "ticvai"
    ],
    "readOnly": true,
    "description": "Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"
   },
   "certificationListingId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "control.integration_listing",
    "description": "For a production client, the certified integration it was issued against."
   },
   "credentialTtlDays": {
    "type": "integer",
    "minimum": 1,
    "maximum": 730,
    "nullable": true,
    "description": "Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the key stops working unless rotated. No token is issued after it."
   },
   "allowedTenantIds": {
    "type": "array",
    "description": "13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "ipAllowList": {
    "type": "array",
    "description": "13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n",
    "items": {
     "type": "string"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked"
    ],
    "readOnly": true
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**A credential unused for a year is a credential nobody will notice being stolen.**\n"
   }
  }
 },
 "ApiScope": {
  "type": "object",
  "x-ticvai-persistence": "none — generated at release from x-ticvai-api-scope on each partner-callable operation",
  "description": "**One module scope** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, and the operations it opens.\n**A write scope never opens a catalogue write** (M17-04): `ticketing.write` opens carts, orders and holds for a partner or developer client, and no product, price list, price, channel capacity, lifecycle or alternative-code write, since those operations are not partner-callable and carry no `x-ticvai-api-scope`. Only a platform-staff `ApiLicence.catalogueWriteException` opens one, for one named client.\n",
  "required": [
   "scope",
   "module",
   "access"
  ],
  "properties": {
   "scope": {
    "type": "string",
    "description": "e.g. `ticketing.read`."
   },
   "module": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
   },
   "access": {
    "type": "string",
    "enum": [
     "read",
     "write"
    ]
   },
   "description": {
    "type": "string"
   },
   "operations": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "contract": {
       "type": "string"
      },
      "operationId": {
       "type": "string"
      }
     }
    }
   },
   "licensed": {
    "type": "boolean",
    "description": "Whether the caller's tenant licenses the module (`ApiLicence.licensedModules`)."
   }
  }
 },
 "ApprovalDecision": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision",
  "required": [
   "level",
   "principalId",
   "decision",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "level": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "isDelegate": {
    "type": "boolean"
   },
   "delegatedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject"
    ]
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "usedMfa": {
    "type": "boolean"
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration",
   "productChange",
   "pricingChange"
  ]
 },
 "ApprovalMode": {
  "type": "string",
  "description": "11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n",
  "enum": [
   "sequential",
   "parallel",
   "consensus",
   "majority"
  ]
 },
 "ApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "approvals.request",
  "required": [
   "id",
   "kind",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "rerouteOnNoApprover": {
    "type": "boolean",
    "default": true,
    "description": "BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"
   },
   "outOfOfficeDelegateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "allowEmailApproval": {
    "type": "boolean",
    "default": false,
    "description": "**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"
   },
   "reopenedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ApprovalStatus"
   },
   "subjectContract": {
    "type": "string"
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "matrixVersion": {
    "type": "integer"
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "currentLevel": {
    "type": "integer"
   },
   "totalLevels": {
    "type": "integer"
   },
   "pendingApprovers": {
    "type": "array",
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
      "isDelegate": {
       "type": "boolean"
      }
     }
    }
   },
   "decisions": {
    "type": "array",
    "description": "Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n",
    "items": {
     "$ref": "#/components/schemas/ApprovalDecision"
    }
   },
   "escalations": {
    "type": "array",
    "description": "11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "fromLevel": {
       "type": "integer"
      },
      "toLevel": {
       "type": "integer"
      },
      "wasAutomatic": {
       "type": "boolean"
      }
     }
    }
   },
   "resubmittedFromId": {
    "type": "string",
    "nullable": true
   },
   "reopenedFromId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "aiAssessment": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.",
    "properties": {
     "riskScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "riskBand": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high",
       "critical"
      ]
     },
     "priorityScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "escalationSuggestion": {
      "type": "object",
      "description": "A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.",
      "properties": {
       "action": {
        "type": "string",
        "enum": [
         "escalate",
         "addBackupApprover",
         "none"
        ]
       },
       "reason": {
        "type": "string",
        "nullable": true
       }
      }
     },
     "signals": {
      "type": "array",
      "maxItems": 10,
      "description": "The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.",
      "items": {
       "type": "object",
       "properties": {
        "code": {
         "type": "string"
        },
        "contribution": {
         "type": "number"
        },
        "detail": {
         "type": "string",
         "nullable": true
        }
       }
      }
     },
     "scoreId": {
      "type": "string",
      "format": "uuid",
      "description": "The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."
     },
     "decisionRecordId": {
      "type": "string",
      "description": "The ai decision record, for the audit of what the AI said and why."
     },
     "assessedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "returned",
   "informationRequested",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
 },
 "CreateApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "kind",
   "subjectContract",
   "subjectType",
   "subjectId",
   "scopePath",
   "summary"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "subjectContract": {
    "type": "string",
    "description": "Which contract owns the thing being approved."
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "description": "**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string",
    "maxLength": 300,
    "description": "What the approver sees in their queue before opening it."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true
   },
   "justification": {
    "type": "string",
    "maxLength": 1000
   },
   "isDraft": {
    "type": "boolean",
    "default": false,
    "description": "True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"
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
 "ProductionAccessRequest": {
  "type": "object",
  "x-ticvai-persistence": "control.production_access_request",
  "description": "**A developer's request for production keys** (17 September minutes, M17-06): sandbox, then certification, then production.\n",
  "required": [
   "id",
   "developerId",
   "sandboxClientId",
   "listingId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "developerId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "sandboxClientId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "control.api_client"
   },
   "listingId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "control.integration_listing"
   },
   "scopes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "allowedTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "ipAllowList": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "approved",
     "rejected",
     "withdrawn"
    ],
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "productionClientId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "control.api_client"
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "SeatDiscrepancy": {
  "type": "object",
  "description": "Board 4.8. **A seat sold twice and a seat sold to nobody are both invisible until somebody counts.**\n",
  "properties": {
   "seatId": {
    "type": "string",
    "format": "uuid"
   },
   "label": {
    "type": "string"
   },
   "mapState": {
    "type": "string"
   },
   "orderState": {
    "type": "string"
   },
   "orderIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "kind": {
    "type": "string",
    "enum": [
     "soldTwice",
     "soldNotMarked",
     "markedNotSold",
     "heldAndSold",
     "orphanedHold"
    ]
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "SeatMapStatus": {
  "type": "string",
  "enum": [
   "draft",
   "validated",
   "published",
   "archived"
  ]
 },
 "SeatMapSummary": {
  "x-ticvai-persistence": "seating.seat_map",
  "type": "object",
  "required": [
   "id",
   "name",
   "venueId",
   "status",
   "seatCount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "$ref": "#/components/schemas/SeatMapStatus"
   },
   "seatCount": {
    "type": "integer"
   },
   "sectionCount": {
    "type": "integer"
   },
   "hasGeometry": {
    "type": "boolean",
    "description": "False when only a manifest has been imported. Such a map can be sold from a list but not rendered.\n"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WebhookDelivery": {
  "type": "object",
  "x-ticvai-persistence": "control.webhook_delivery",
  "description": "13.1.30. **The log a developer needs most**, and without it every question becomes a support ticket.\n",
  "required": [
   "id",
   "subscriptionId",
   "eventType",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subscriptionId": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "eventType": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "delivered",
     "failed",
     "retrying",
     "abandoned"
    ]
   },
   "attemptCount": {
    "type": "integer"
   },
   "responseCode": {
    "type": "integer",
    "nullable": true
   },
   "responseBodyExcerpt": {
    "type": "string",
    "nullable": true,
    "description": "**Truncated, and it is what makes the log useful** — a 500 with the receiver's own error message in it answers the question without a conversation.\n"
   },
   "isReplay": {
    "type": "boolean",
    "default": false
   },
   "isTest": {
    "type": "boolean",
    "default": false,
    "description": "Sent by `testWebhookSubscription` (VM close-out, 29 September). Marked in the payload so a receiver never books it, and never counted towards `consecutiveFailures`.\n"
   },
   "deliveredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WebhookEventCatalogueEntry": {
  "type": "object",
  "x-ticvai-persistence": "none — read from the event catalogue (events/*.yaml) shipped with the release",
  "description": "One event a webhook may subscribe to, as the event catalogue declares it. What a receiver needs to write a handler: the name, the version in the payload, who publishes it, what it is about and when, and the payload fields.\n",
  "required": [
   "name",
   "version",
   "publisher"
  ],
  "properties": {
   "name": {
    "$ref": "#/components/schemas/WebhookEventType"
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "publisher": {
    "type": "string",
    "description": "The one context that publishes it."
   },
   "aggregate": {
    "type": "string",
    "description": "What the event is about. Delivery is ordered within one instance of it."
   },
   "description": {
    "type": "string"
   },
   "emittedWhen": {
    "type": "string",
    "nullable": true
   },
   "payload": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "type"
     ],
     "properties": {
      "field": {
       "type": "string"
      },
      "type": {
       "type": "string"
      },
      "required": {
       "type": "boolean",
       "default": true
      },
      "notes": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "WebhookEventType": {
  "type": "string",
  "description": "**The webhook event catalogue: every event a subscription may name** (29 September, build pass). Each value is the `name` of an event in `events/` — `aggregate.pastTenseFact`, published through `platform.outbox` by exactly one context. A name is added here in the same change that adds its event file, and never before.\n**Added 29 September**, each closing a requirement that had the webhook mechanism and nothing to subscribe to:\n| Events | Publisher | Requirement | |---|---|---| | `device.statusChanged`, `device.tamperDetected`, `device.enrolmentChanged`, `device.firmwareReleased`, `device.firmwareRolloutCompleted` | tenancy | 16.9.56 | | `accreditation.applicationDecided`, `accreditation.holderStatusChanged`, `accreditation.credentialIssued`, `accreditation.renewalDue` | accreditation | 12.1.53 | | `approval.requested`, `approval.escalated`, `approval.stepCompleted`, `approval.expired` | approvals | 11.1.64, 11.1.66 | | `seat.held`, `seat.released`, `seat.blocked`, `seatMap.published` | seating | 21.13.4 | | `consent.deviceConsentRecorded`, `consent.deviceConsentClaimed` | marketing | 2.6.65 | | `order.chargebackRecorded` | orders | 8.3.11 to 8.3.15 (a tenant's own finance or fraud tooling) | | `entitlement.expiringSoon` | access | 5.5.30 (a tenant's own CRM) | | `apiClient.anomalyDetected` | public-api | 17 September minutes M17-07 (added 30 September with its event file) |\n**Published and deliberately not offered** (29 September, build pass, group G2): `identity.credentialResetRequested` and `identity.loginRecorded` are security signals, and a stream of them to an outside receiver is a map of which accounts are under attack; `storefront.sessionEvent` is high-volume fraud telemetry, not a business fact a receiver acts on.\n",
  "enum": [
   "access.validated",
   "accreditation.applicationDecided",
   "accreditation.credentialIssued",
   "accreditation.holderStatusChanged",
   "accreditation.renewalDue",
   "ai.ceilingApproaching",
   "apiClient.anomalyDetected",
   "approval.escalated",
   "approval.expired",
   "approval.granted",
   "approval.rejected",
   "approval.requested",
   "approval.stepCompleted",
   "assets.documentIndexed",
   "cart.abandoned",
   "catalogue.productPublished",
   "consent.deviceConsentClaimed",
   "consent.deviceConsentRecorded",
   "conversation.handedOver",
   "device.enrolmentChanged",
   "device.firmwareReleased",
   "device.firmwareRolloutCompleted",
   "device.statusChanged",
   "device.tamperDetected",
   "entitlement.expiringSoon",
   "entitlement.issued",
   "entitlement.statusChanged",
   "fnb.menuPublished",
   "fnb.orderReady",
   "inventory.purchaseOrderReceived",
   "ledger.journalPosted",
   "ledger.periodClosed",
   "maintenance.assetReturnedToService",
   "maintenance.templatePublished",
   "maintenance.workOrderCompleted",
   "marketing.caseClosed",
   "order.chargebackRecorded",
   "order.completed",
   "order.paid",
   "order.refunded",
   "performance.cancelled",
   "reporting.definitionPublished",
   "retail.merchandisePublished",
   "seat.blocked",
   "seat.held",
   "seat.released",
   "seat.sold",
   "seatMap.published",
   "shift.closed",
   "stock.depleted",
   "tenant.suspended",
   "whitelabel.contentPublished"
  ]
 },
 "WebhookSubscription": {
  "type": "object",
  "x-ticvai-persistence": "control.webhook_subscription",
  "description": "13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n",
  "required": [
   "id",
   "clientId",
   "endpointUrl",
   "eventTypes",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "clientId": {
    "type": "string",
    "format": "uuid"
   },
   "endpointUrl": {
    "type": "string"
   },
   "eventTypes": {
    "type": "array",
    "description": "**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. Each entry is a name from the webhook event catalogue (`WebhookEventType`).\n",
    "items": {
     "$ref": "#/components/schemas/WebhookEventType"
    }
   },
   "filters": {
    "type": "object",
    "nullable": true,
    "description": "13.3.22. Tenant, venue, or a business condition on the payload.",
    "additionalProperties": true
   },
   "signingSecret": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "description": "**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingVerification",
     "active",
     "paused",
     "failing",
     "disabled"
    ],
    "readOnly": true
   },
   "consecutiveFailures": {
    "type": "integer",
    "readOnly": true
   },
   "disabledReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"
   }
  }
 }
}
```
