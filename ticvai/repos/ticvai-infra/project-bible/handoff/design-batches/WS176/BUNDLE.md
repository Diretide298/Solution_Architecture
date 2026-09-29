# WS176 — Seat Management Venue Mapping Reference v1.0 board 12

**10 screens · 23 operations · 23 schemas · 12 permissions**

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

- **Every control that can be refused must be gated.** 12 permissions apply here:
  `APPROVAL_CONFIGURE, CAPACITY_CONFIGURE, DEVICE_VIEW, PERMISSION_MANAGE, PERMISSION_VIEW, PRODUCT_VIEW, REGION_CONFIGURE, SCOPE_VIEW, SHIFT_OPEN, TENANT_CONFIGURE, TENANT_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1061` | Platform Command Center | listDetail | 2 | 0 | — |
| `BO-1062` | Tenant & Brand Context | listDetail | 3 | 1 | — |
| `BO-1063` | Venue-Specific Configuration | listDetail | 2 | 0 | — |
| `BO-1064` | Naming, Numbering & Localization | listDetail | 2 | 0 | — |
| `BO-1065` | Currency, Timezone & Channels | listDetail | 3 | 0 | — |
| `BO-1066` | Roles, Permissions & Masking | listDetail | 6 | 0 | — |
| `BO-1067` | Seat Approval Workflows | listDetail | 1 | 0 | — |
| `BO-1068` | Lifecycle & Environment Promotion | listDetail | 1 | 0 | — |
| `BO-1069` | Platform Health & Observability | listDetail | 1 | 0 | — |
| `BO-1070` | Setup, Clone & Inheritance | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-1061, BO-1062, BO-1064, BO-1065, BO-1066, BO-1067, BO-1068, BO-1069, BO-1070 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1061",
  "name": "Platform Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "01",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/platform-command-center-bo-1061",
   "component": "apps/venue-management-web/src/routes/access-venue/PlatformCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1062",
    "BO-1063",
    "BO-1064",
    "BO-1065",
    "BO-1066",
    "BO-1067",
    "BO-1068",
    "BO-1069",
    "BO-1070"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1062",
     "trigger": "Tenant & Brand Context",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-1063",
     "trigger": "Venue-Specific Configuration",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-1064",
     "trigger": "Naming, Numbering & Localization",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-1065",
     "trigger": "Currency, Timezone & Channels",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-1066",
     "trigger": "Roles, Permissions & Masking",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-1067",
     "trigger": "Seat Approval Workflows",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-1068",
     "trigger": "Lifecycle & Environment Promotion",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-1069",
     "trigger": "Platform Health & Observability",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    },
    {
     "to": "BO-1070",
     "trigger": "Setup, Clone & Inheritance",
     "provenance": "structural — pack board 12 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a platform-wide view of tenant, venue and environment readiness. Show tenants, brands, venues, environments, active users, pending approvals, deployments and failed jobs. Display service status, API health, capacity, incidents and configuration exceptions. Restrict cross-tenant visibility to authorized platform roles and preserve every context switch. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 50"
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
       "impliedBy": "listVenueMaps",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The platform list.",
   "error": "Could not load. Names which read failed and leaves the platform untouched.",
   "emptyFirstRun": "No platform yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the platform are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVenueMaps",
    "contract": "venue-map",
    "purpose": "Venues and their maps",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSeatMaps",
    "contract": "seating",
    "purpose": "Seat maps across them",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1061",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1061"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1062",
  "name": "Tenant & Brand Context",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "02",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/tenant-brand-context-bo-1062",
   "component": "apps/venue-management-web/src/routes/access-venue/TenantBrandContext.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1061"
   ],
   "exitTo": [
    "BO-1061"
   ],
   "transitions": [
    {
     "to": "BO-1061",
     "trigger": "Back to Platform Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the hierarchy and isolation boundary for seat management. Maintain tenant, legal entity, brand, region, venue ownership, status and data-residency classification. Configure tenant isolation, encryption context, export restriction, cross-brand sharing and support-access policy. Show inherited platform settings and the venues, users, integrations and environments within each context. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 50"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getOrgUnit",
       "notes": "One record, read-only."
      },
      {
       "kind": "detailPanel",
       "label": "Venue setting defaults",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.alerting",
        "VenueSettings.displayCurrencies",
        "VenueSettings.shiftVarianceThreshold",
        "VenueSettings.catalogue",
        "VenueSettings.inventory",
        "VenueSettings.seating",
        "VenueSettings.promotions",
        "VenueSettings.fnb",
        "VenueSettings.queue",
        "VenueSettings.reporting"
       ],
       "operation": "getVenueSettingsDefaults",
       "notes": "**The inherited settings** — the tenant's default for every venue setting, which a venue inherits wherever it leaves a limit null (decided 28 September, audit R094).",
       "provenance": "contract tenancy.yaml GET /venue-settings-defaults"
      },
      {
       "kind": "secondaryButton",
       "label": "Save venue setting defaults",
       "operation": "setVenueSettingsDefaults",
       "permission": "TENANT_CONFIGURE",
       "provenance": "contract tenancy.yaml PUT /venue-settings-defaults"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tenant brand context list.",
   "error": "Could not load. Names which read failed and leaves the tenant brand context untouched.",
   "emptyFirstRun": "No tenant brand context yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tenant brand context are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getOrgUnit",
    "contract": "tenancy",
    "purpose": "Tenant and brand context",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getVenueSettingsDefaults",
    "contract": "tenancy",
    "purpose": "The tenant's default for every venue setting — the inherited settings (audit R094)",
    "trigger": "onLoad"
   },
   {
    "operationId": "setVenueSettingsDefaults",
    "contract": "tenancy",
    "purpose": "Set the tenant's default for every venue setting (tenant scope, TENANT_CONFIGURE; audit R094)",
    "trigger": "onAction",
    "invalidates": [
     "getVenueSettingsDefaults"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1062",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1062"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "orgUnitId",
     "from": "navigation"
    }
   ]
  },
  "overlays": [
   {
    "id": "formSetVenueSettingsDefaults",
    "component": "modal",
    "trigger": "Save venue setting defaults",
    "body": "**Collects what `setVenueSettingsDefaults` sends before it is called.** The body is a `VenueSettings`: every field is the default a venue inherits where it leaves the setting null (decided 28 September, audit R094). Tenant scope; needs `TENANT_CONFIGURE`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "VenueSettings",
    "confirm": {
     "label": "Save venue setting defaults",
     "operation": "setVenueSettingsDefaults"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "supportHours",
      "quietHours",
      "alerting",
      "displayCurrencies",
      "catalogue",
      "inventory",
      "seating",
      "promotions",
      "fnb",
      "queue",
      "reporting"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /venue-settings-defaults"
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
  "id": "BO-1063",
  "name": "Venue-Specific Configuration",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "03",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/venue-specific-configuration-bo-1063",
   "component": "apps/venue-management-web/src/routes/access-venue/VenueSpecificConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1061"
   ],
   "exitTo": [
    "BO-1061"
   ],
   "transitions": [
    {
     "to": "BO-1061",
     "trigger": "Back to Platform Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Set local defaults without creating separate seat systems. Configure default map, lock/hold duration, naming, accessibility, sales channels, approvals and publishing policy. Map local entrances, devices, price/seat categories, operating calendars and venue-specific exceptions. Display which settings inherit from platform/tenant/brand and require justification for permitted overrides. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Configuration Scope of Work | Version 1.0 50 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 50"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getVenueSettings",
       "notes": "One record, read-only. **Shows the configured limits** (decided 28 September, audit R094); a limit the venue has not set is null and shows the tenant default it inherits."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setVenueSettings",
       "label": "Save venue settings",
       "notes": "The act the screen exists for. Saves the venue's own limits; clearing one sends null, which inherits the tenant default (audit R094)."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setVenueSettings"
      },
      {
       "kind": "numberField",
       "label": "Seats per guest booking",
       "bindsTo": "VenueSettings.seating.maxSeatsPerGuestOrder",
       "operation": "setVenueSettings",
       "notes": "**How many seats one guest may take in one booking on Guest Web and the Guest App** (decided 29 September, rev 3 REV3-7). Default 10, from 1 to 50; left empty, the venue inherits the tenant default. `createSeatHold` counts the seats asked for plus those the guest already holds on the performance and refuses above it with `seat-limit-exceeded`. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read it.",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue-specific list.",
   "error": "Could not load. Names which read failed and leaves the venue-specific untouched.",
   "emptyFirstRun": "No venue-specific yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue-specific are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "Venue configuration",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setVenueSettings",
    "contract": "tenancy",
    "purpose": "Change it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1063",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1063"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
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
  "id": "BO-1064",
  "name": "Naming, Numbering & Localization",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "04",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/naming-numbering-localization-bo-1064",
   "component": "apps/venue-management-web/src/routes/access-venue/NamingNumberingLocalization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1061"
   ],
   "exitTo": [
    "BO-1061"
   ],
   "transitions": [
    {
     "to": "BO-1061",
     "trigger": "Back to Platform Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control how seat entities and values appear in each venue and language. Configure venue/section/row/seat code formats, numbering direction, padding, prefixes and reserved values. Maintain translated labels, supported languages, text direction, pluralization and fallback language. Validate uniqueness and preview labels on map, ticket, cart, POS, access device and report. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 51"
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
       "impliedBy": "updateSeats",
       "label": "Save seats",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getRegionSettings",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateSeats"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The naming numbering localization list.",
   "error": "Could not load. Names which read failed and leaves the naming numbering localization untouched.",
   "emptyFirstRun": "No naming numbering localization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the naming numbering localization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateSeats",
    "contract": "seating",
    "purpose": "Naming and numbering",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getRegionSettings",
    "contract": "tenancy",
    "purpose": "Localisation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1064",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1064"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 51. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "regionId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
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
  "id": "BO-1065",
  "name": "Currency, Timezone & Channels",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "05",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/currency-timezone-channels-bo-1065",
   "component": "apps/venue-management-web/src/routes/access-venue/CurrencyTimezoneChannels.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1061"
   ],
   "exitTo": [
    "BO-1061"
   ],
   "transitions": [
    {
     "to": "BO-1061",
     "trigger": "Back to Platform Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure regional display and channel availability. Set currency, rounding, date/time/number formats, timezone, week start and daylight-saving behavior. Enable web, mobile, POS, box office, call center, B2B, partner API and marketplace channels per venue. Define locale defaults and fail-safe behavior when a channel or currency is unavailable. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 51"
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
       "impliedBy": "updateRegionSettings",
       "label": "Save region settings",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateRegionSettings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The currency timezone channels list.",
   "error": "Could not load. Names which read failed and leaves the currency timezone channels untouched.",
   "emptyFirstRun": "No currency timezone channels yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the currency timezone channels are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDenominations",
    "contract": "shift",
    "purpose": "The notes and coins tills count",
    "trigger": "onLoad"
   },
   {
    "operationId": "setDenominations",
    "contract": "shift",
    "purpose": "Set a currency's notes and coins",
    "trigger": "onAction",
    "invalidates": [
     "listDenominations"
    ]
   },
   {
    "operationId": "updateRegionSettings",
    "contract": "tenancy",
    "purpose": "Currency, timezone and channels",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1065",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1065"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 51. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "regionId",
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
  "id": "BO-1066",
  "name": "Roles, Permissions & Masking",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "06",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/roles-permissions-masking-bo-1066",
   "component": "apps/venue-management-web/src/routes/access-venue/RolesPermissionsMasking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1061"
   ],
   "exitTo": [
    "BO-1061"
   ],
   "transitions": [
    {
     "to": "BO-1061",
     "trigger": "Back to Platform Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Enforce least-privilege access to seat administration and operational data. Configure RBAC/PBAC for maps, layouts, inventory, locks, holds, pricing, reports, integrations and audit. Apply venue/region scope, field masking, temporary/delegated access, segregation of duties and emergency override. Preview effective access for a user/context and log sensitive read, export and administrative actions. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 51"
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
       "impliedBy": "listAccessPolicies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createAccessPolicy",
       "label": "Create access policy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAccessPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The roles permissions masking list.",
   "error": "Could not load. Names which read failed and leaves the roles permissions masking untouched.",
   "emptyFirstRun": "No roles permissions masking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the roles permissions masking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessPolicies",
    "contract": "identity",
    "purpose": "Who may see and change what",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createAccessPolicy",
    "contract": "identity",
    "purpose": "Write a policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "simulateAccessPolicy",
    "contract": "identity",
    "purpose": "What this policy would decide, before it decides anything",
    "trigger": "onAction",
    "provenance": "wiring gap, 19 September 2026 — the screen showed the noun and could not act on it"
   },
   {
    "operationId": "updateAccessPolicy",
    "contract": "identity",
    "purpose": "Change a data-access policy, as a new version",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listAccessPolicies"
    ]
   },
   {
    "operationId": "setAccessPolicyState",
    "contract": "identity",
    "purpose": "Submit, approve, activate or retire a policy",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listAccessPolicies"
    ]
   },
   {
    "operationId": "createEmergencyAccessOverride",
    "contract": "identity",
    "purpose": "Bypass the policy, loudly, with a reason and an expiry",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listAccessPolicies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1066",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1066"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 51. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "policyId",
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
  "id": "BO-1067",
  "name": "Seat Approval Workflows",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "07",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-approval-workflows-bo-1067",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatApprovalWorkflows.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1061"
   ],
   "exitTo": [
    "BO-1061"
   ],
   "transitions": [
    {
     "to": "BO-1061",
     "trigger": "Back to Platform Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure governance paths for high-impact seat changes. Define workflow by map/layout, capacity, seat kill, hold, accessibility, pricing, integration and override change type. Set stages, approver roles, thresholds, quorum, SLA, escalation, delegation, comments and evidence. Prevent requester self-approval where segregation rules apply and preserve decision history. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 51",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 51"
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
       "impliedBy": "setVisualWorkflow",
       "label": "Save visual workflow",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setVisualWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seat approval workflows list.",
   "error": "Could not load. Names which read failed and leaves the seat approval workflows untouched.",
   "emptyFirstRun": "No seat approval workflows yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat approval workflows are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualWorkflow",
    "contract": "approvals",
    "purpose": "Seat approval workflows",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1067",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1067"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 51. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1068",
  "name": "Lifecycle & Environment Promotion",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "08",
   "page": 52
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/lifecycle-environment-promotion-bo-1068",
   "component": "apps/venue-management-web/src/routes/access-venue/LifecycleEnvironmentPromotion.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1061"
   ],
   "exitTo": [
    "BO-1061"
   ],
   "transitions": [
    {
     "to": "BO-1061",
     "trigger": "Back to Platform Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Move approved configuration safely from draft to production. Provide Draft, Test, Staging and Production contexts with version, owner, status and dependency checks. Promote signed configuration packages through required gates, automated tests and approvals. Support comparison, rollback, failed-promotion recovery and prohibition of direct unapproved production edits. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 52"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 52"
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
       "impliedBy": "deployConfigurationProfile",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "deployConfigurationProfile"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Promotes this configuration to the target environment.** What is running there now is replaced, and the previous version stays restorable.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lifecycle environment promotion list.",
   "error": "Could not load. Names which read failed and leaves the lifecycle environment promotion untouched.",
   "emptyFirstRun": "No lifecycle environment promotion yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the lifecycle environment promotion are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "deployConfigurationProfile",
    "contract": "tenancy",
    "purpose": "Promote configuration",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1068",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1068"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 52. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "profileId",
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
  "id": "BO-1069",
  "name": "Platform Health & Observability",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "09",
   "page": 52
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/platform-health-observability-bo-1069",
   "component": "apps/venue-management-web/src/routes/access-venue/PlatformHealthObservability.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1061"
   ],
   "exitTo": [
    "BO-1061"
   ],
   "transitions": [
    {
     "to": "BO-1061",
     "trigger": "Back to Platform Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor the technical services that protect seat-state correctness. Show API latency/error, event lag, lock service, inventory service, cache, database, queue and webhook health. Configure SLOs, thresholds, alerts, correlation, incident ownership and capacity forecasts by tenant/venue. Drill from a metric to traces, logs and affected performances without exposing restricted tenant data. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 52"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 52"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getWorkstationHealth",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The platform health observability list.",
   "error": "Could not load. Names which read failed and leaves the platform health observability untouched.",
   "emptyFirstRun": "No platform health observability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the platform health observability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWorkstationHealth",
    "contract": "tenancy",
    "purpose": "Platform health",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1069",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1069"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 52. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "workstationId",
     "from": "session"
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
  "id": "BO-1070",
  "name": "Setup, Clone & Inheritance",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "12",
   "number": "10",
   "page": 52
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/setup-clone-inheritance-bo-1070",
   "component": "apps/venue-management-web/src/routes/access-venue/SetupCloneInheritance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1061"
   ],
   "exitTo": [
    "BO-1061"
   ],
   "transitions": [
    {
     "to": "BO-1061",
     "trigger": "Back to Platform Command Center",
     "provenance": "structural — pack board 12 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Accelerate onboarding while keeping configuration lineage visible. Guide setup of tenant, brand, venue, locale, map, categories, locks/holds, channels, workflows and integrations. Clone an authorized source venue or template and choose which settings, maps and rules to copy or inherit. Show inherited, overridden, missing and conflicting settings and validate completeness before activation. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 52 Board 13 - Seat APIs, Webhooks & Audit Governance Figure 13. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 53",
  "gaps": [
   {
    "operation": null,
    "why": "**Setup, Clone & Inheritance declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 52"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 52"
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
       "impliedBy": "cloneSeatMap",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "cloneSeatMap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The clone inheritance list.",
   "error": "Could not load. Names which read failed and leaves the clone inheritance untouched.",
   "emptyFirstRun": "No clone inheritance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the clone inheritance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "cloneSeatMap",
    "contract": "seating",
    "purpose": "Clone a map into a new venue",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setConfigurationProfile",
    "contract": "tenancy",
    "purpose": "Inherited settings",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1070",
   "workshopBoard": "wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1070"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 52. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "cloneSeatMap": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/clone",
  "contract": "seating",
  "summary": "Clone a map, optionally into another venue",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "SeatMap"
 },
 "createAccessPolicy": {
  "method": "POST",
  "path": "/access-policies",
  "contract": "identity",
  "summary": "Write a policy without writing code",
  "permission": "PERMISSION_MANAGE",
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
  "requestBody": "AccessPolicy",
  "responds": "AccessPolicy"
 },
 "createEmergencyAccessOverride": {
  "method": "POST",
  "path": "/access-overrides",
  "contract": "identity",
  "summary": "Bypass the policy, loudly",
  "permission": "PERMISSION_MANAGE",
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
  "responds": "EmergencyAccessOverride"
 },
 "deployConfigurationProfile": {
  "method": "POST",
  "path": "/configuration-profiles/{profileId}/deploy",
  "contract": "tenancy",
  "summary": "Push a version to a fleet, in stages",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "ProfileDeployment",
  "responds": null
 },
 "getOrgUnit": {
  "method": "GET",
  "path": "/org-units/{orgUnitId}",
  "contract": "tenancy",
  "summary": "Read a scope node",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrgUnit"
 },
 "getRegionSettings": {
  "method": "GET",
  "path": "/regions/{regionId}/settings",
  "contract": "tenancy",
  "summary": "Read region settings",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "RegionSettings"
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
 "getVenueSettingsDefaults": {
  "method": "GET",
  "path": "/venue-settings-defaults",
  "contract": "tenancy",
  "summary": "The tenant's default for every venue setting",
  "permission": "TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
 },
 "getWorkstationHealth": {
  "method": "GET",
  "path": "/workstations/{workstationId}/health",
  "contract": "tenancy",
  "summary": "A score a manager can sort by, and what is dragging it down",
  "permission": "DEVICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "listAccessPolicies": {
  "method": "GET",
  "path": "/access-policies",
  "contract": "identity",
  "summary": "Attribute-based access policies",
  "permission": "PERMISSION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccessPolicy"
 },
 "listDenominations": {
  "method": "GET",
  "path": "/denominations",
  "contract": "shift",
  "summary": "The notes and coins a till counts",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "includeInactive",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Denomination"
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
 "listVenueMaps": {
  "method": "GET",
  "path": "/venue-maps",
  "contract": "venue-map",
  "summary": "Maps for this venue",
  "permission": "VENUE_MAP_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueMap"
 },
 "setAccessPolicyState": {
  "method": "POST",
  "path": "/access-policies/{policyId}/state",
  "contract": "identity",
  "summary": "Submit, approve, activate or retire a policy",
  "permission": "PERMISSION_MANAGE",
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
  "responds": "AccessPolicy"
 },
 "setConfigurationProfile": {
  "method": "PUT",
  "path": "/configuration-profiles",
  "contract": "tenancy",
  "summary": "What a class of workstation is configured to be",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "ConfigurationProfile",
  "responds": "ConfigurationProfile"
 },
 "setDenominations": {
  "method": "PUT",
  "path": "/denominations",
  "contract": "shift",
  "summary": "Set the notes and coins a region's tills count",
  "permission": "REGION_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SetDenominationsRequest",
  "responds": "Denomination"
 },
 "setVenueSettings": {
  "method": "PUT",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Set support hours, quiet hours, segregated access and alerting",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "VenueSettings",
  "responds": "VenueSettings"
 },
 "setVenueSettingsDefaults": {
  "method": "PUT",
  "path": "/venue-settings-defaults",
  "contract": "tenancy",
  "summary": "Set the tenant's default for every venue setting",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "VenueSettings",
  "responds": "VenueSettings"
 },
 "setVisualWorkflow": {
  "method": "PUT",
  "path": "/visual-workflow",
  "contract": "approvals",
  "summary": "Visual Workflow Designer",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "VisualWorkflowDesignerInput",
  "responds": "VisualWorkflowDesignerView"
 },
 "simulateAccessPolicy": {
  "method": "POST",
  "path": "/access-policies/simulate",
  "contract": "identity",
  "summary": "What this policy would decide, before it decides anything",
  "permission": "PERMISSION_VIEW",
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
  "responds": "AccessDecision"
 },
 "updateAccessPolicy": {
  "method": "PUT",
  "path": "/access-policies/{policyId}",
  "contract": "identity",
  "summary": "Change a policy, as a new version",
  "permission": "PERMISSION_MANAGE",
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
  "requestBody": "AccessPolicy",
  "responds": "AccessPolicy"
 },
 "updateRegionSettings": {
  "method": "PUT",
  "path": "/regions/{regionId}/settings",
  "contract": "tenancy",
  "summary": "Update region settings",
  "permission": "REGION_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RegionSettings",
  "responds": "RegionSettings"
 },
 "updateSeats": {
  "method": "PATCH",
  "path": "/seat-maps/{seatMapId}/seats",
  "contract": "seating",
  "summary": "Bulk-amend seats",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "BulkUpdateSeatsRequest",
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessCondition": {
  "type": "object",
  "description": "**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n",
  "required": [
   "attribute",
   "operator"
  ],
  "properties": {
   "attribute": {
    "type": "string",
    "enum": [
     "user.attribute",
     "employee.attribute",
     "employee.onShift",
     "membership.tier",
     "membership.status",
     "accreditation.type",
     "accreditation.status",
     "customer.segment",
     "resource.classification",
     "venue.attribute",
     "venue.id",
     "attraction.attribute",
     "device.kind",
     "device.id",
     "device.trusted",
     "time.ofDay",
     "time.dayOfWeek",
     "time.season",
     "time.withinOperatingHours",
     "event.id",
     "event.status",
     "capacity.utilisationPercent",
     "occupancy.level",
     "risk.score",
     "ticket.status",
     "location.scopePath"
    ]
   },
   "key": {
    "type": "string",
    "nullable": true,
    "description": "For the `*.attribute` forms — which attribute, by code."
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "in",
     "notIn",
     "greaterThan",
     "lessThan",
     "between",
     "contains",
     "startsWith",
     "exists"
    ]
   },
   "value": {
    "nullable": true,
    "description": "The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"
   },
   "values": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "AccessDecision": {
  "type": "object",
  "x-ticvai-persistence": "identity.access_decision",
  "description": "3.3.37. **The decision, the policy version behind it, and the attribute values it actually saw.** The third is what separates *the policy is wrong* from *the data was stale*.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "effect": {
    "type": "string",
    "enum": [
     "permit",
     "deny"
    ]
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decidedBy": {
    "type": "string",
    "enum": [
     "central",
     "deviceBundle"
    ],
    "description": "3.3.29 against 3.3.30 — which evaluator answered."
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "permission": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "matchedPolicies": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "policyId": {
       "type": "string",
       "format": "uuid"
      },
      "version": {
       "type": "integer"
      },
      "effect": {
       "type": "string"
      },
      "matched": {
       "type": "boolean"
      },
      "failedCondition": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "observedAttributes": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Deliberately an open map**, the same keys as `AccessContext.attributes`: the value of every attribute the evaluator actually read, whichever source it came from.\n"
   },
   "overrideId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "latencyMs": {
    "type": "integer",
    "nullable": true
   },
   "scopePathIndex": {
    "type": "string"
   }
  }
 },
 "AccessPolicy": {
  "type": "object",
  "x-ticvai-persistence": "identity.access_policy",
  "description": "3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n",
  "required": [
   "code",
   "name",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Assigned by the server on `createAccessPolicy`; the path names the policy on update."
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "isTemplate": {
    "type": "boolean",
    "default": false
   },
   "permissions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"
   },
   "conditions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AccessCondition"
    }
   },
   "combining": {
    "type": "string",
    "enum": [
     "allMustMatch",
     "anyMayMatch"
    ],
    "default": "allMustMatch"
   },
   "effect": {
    "type": "string",
    "enum": [
     "permit",
     "deny"
    ],
    "description": "**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string",
    "description": "3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"
   },
   "appliesToRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "description": "**Moved only by `setAccessPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "suspended",
     "retired"
    ]
   },
   "version": {
    "type": "integer",
    "default": 1,
    "readOnly": true,
    "description": "Set by the server; every `updateAccessPolicy` writes a new version."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "delegatedAdminRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"
   }
  }
 },
 "BulkUpdateSeatsRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "selection"
  ],
  "properties": {
   "selection": {
    "type": "object",
    "description": "Seats to amend. Combine filters; an empty selection is rejected.",
    "properties": {
     "seatIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "sectionCodes": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "rowLabels": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "attribute": {
    "$ref": "#/components/schemas/SeatAttribute"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "ConfigurationProfile": {
  "type": "object",
  "x-ticvai-persistence": "platform.configuration_profile",
  "description": "Board 1 of the client's POS design set, 20 August. **The board shows 1,248 workstations across four versions and the package modelled none of it** — a firmware version field on the workstation, and nothing that says what a workstation is configured to be.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks alone*, which is the only reason to version a profile at all.\n",
  "required": [
   "id",
   "name",
   "venueKindScope",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "venueKindScope": {
    "type": "array",
    "description": "Which workstation types it applies to. **A ticketing counter and a kitchen display do not share a profile**, and a profile that claims to is a profile somebody deploys to the wrong fleet.\n",
    "items": {
     "type": "string"
    }
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "**Immutable once deployed anywhere.** A change makes a new version, and the old one stays readable — a workstation still running v2.3 must be able to say what v2.3 was. Assigned by the server: 1 on create, and one more each time a change lands on a published version (see `setConfigurationProfile`).\n"
   },
   "settings": {
    "type": "object",
    "additionalProperties": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "deploying",
     "deployed",
     "superseded",
     "rolledBack"
    ],
    "description": "On input only `draft` or `published`; sending `published` publishes this version. The other four are set by deployment and refused on input.\n"
   },
   "deployedCount": {
    "type": "integer",
    "readOnly": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "Denomination": {
  "x-ticvai-persistence": "platform.denomination",
  "description": "**Raised in review by Tanmay: denominations belong in a table, not in JSON.** He is right, and the reason is stronger than storage tidiness — **`orders.cash_movement.denominations` was a jsonb blob, so a note that stops circulating has nothing to deactivate.**\n**The seed is `docs/active/seed-data-proposal.md` section 1** (audit R229, proposed, client to correct): notes 5, 10, 20, 50, 100, 200, 500 and 1000 AED; coins 25 fils, 50 fils and 1 AED. The zero-valued coin in the list first supplied (`Coin, 0, COIN`) is a transcription slip rather than a denomination, is not seeded, and is the kind of row a table refuses and a JSON blob accepts silently.\n**Ordered for counting, not by value.** A cashier counts notes highest first and coins in the order they sit in the drawer, and `sortOrder` is what makes the count screen match the physical tray.\"\n",
  "type": "object",
  "required": [
   "currencyCode",
   "kind",
   "value"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "currencyCode": {
    "type": "string"
   },
   "displayName": {
    "type": "string",
    "description": "What the cashier reads — *AED 500*, *Coin*. Localised, because a count screen is read at speed."
   },
   "kind": {
    "type": "string",
    "enum": [
     "note",
     "coin"
    ]
   },
   "sortOrder": {
    "type": "integer",
    "description": "**Counting order, not value order.** Notes highest first, coins as they sit in the tray.\n"
   },
   "isActive": {
    "type": "boolean",
    "default": true,
    "description": "**The field that makes this a table.** A note withdrawn from circulation is deactivated and stays in the count history — **a JSON blob cannot deactivate anything**, and deleting the value would rewrite every past cash-up that used it.\n"
   },
   "value": {
    "x-ticvai-column": "face_value_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "EmergencyAccessOverride": {
  "type": "object",
  "x-ticvai-persistence": "identity.access_override",
  "description": "3.3.6. **Time-boxed at creation, alerted as well as logged.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "permissions": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "type": "string"
   },
   "createdBy": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "alertedTo": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "OrgUnit": {
  "x-ticvai-persistence": "platform.scope",
  "type": "object",
  "required": [
   "id",
   "level",
   "path",
   "code",
   "name",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "level": {
    "$ref": "#/components/schemas/ScopeLevel"
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "path": {
    "type": "string",
    "description": "Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "isActive": {
    "type": "boolean",
    "description": "False causes every permission query at or beneath this node to resolve to DENY.\n"
   },
   "childCount": {
    "type": "integer",
    "minimum": 0
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
 "Placement": {
  "x-ticvai-persistence": "none — embedded in region_settings",
  "type": "object",
  "description": "Read-only here. Set by the Control Plane at provisioning.\nEvery region is its own logical cell. Placement determines the infrastructure backing it, which is how cost is controlled without varying the split rule: `shared` puts several regions' databases on one cluster; `dedicated` and `isolated` give a region its own. Regions in different countries MUST have placements in their respective jurisdictions.\n",
  "readOnly": true,
  "required": [
   "mode"
  ],
  "properties": {
   "mode": {
    "type": "string",
    "enum": [
     "shared",
     "dedicated",
     "isolated",
     "clientHosted"
    ]
   },
   "cellName": {
    "type": "string"
   },
   "cloudRegion": {
    "type": "string"
   }
  }
 },
 "Point": {
  "type": "object",
  "required": [
   "x",
   "y"
  ],
  "properties": {
   "x": {
    "type": "number"
   },
   "y": {
    "type": "number"
   }
  }
 },
 "ProfileDeployment": {
  "type": "object",
  "x-ticvai-persistence": "platform.profile_deployment",
  "description": "**A deployment is an event with a date, a target and an outcome** — the client's board shows recent deployments with all three and the package had no record of any.\n**Staged rather than all-at-once by default.** Pushing a profile to 1,248 workstations simultaneously is how a venue discovers a bad profile at every till at the same moment.\n",
  "required": [
   "id",
   "profileId",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "profileId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Taken from the path of `deployConfigurationProfile`."
   },
   "version": {
    "type": "integer",
    "description": "The published version to deploy."
   },
   "targetWorkstationIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "targetFilter": {
    "type": "object",
    "nullable": true,
    "description": "By department, type or venue, where the target is a set rather than a list.\n",
    "properties": {
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
     "workstationTypes": {
      "type": "array",
      "description": "The same workstation-type values `ConfigurationProfile.venueKindScope` holds.",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "strategy": {
    "type": "string",
    "enum": [
     "immediate",
     "staged",
     "onNextIdle"
    ],
    "default": "onNextIdle"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "inProgress",
     "completed",
     "partiallyFailed",
     "rolledBack"
    ],
    "readOnly": true
   },
   "succeededCount": {
    "type": "integer",
    "readOnly": true
   },
   "failedCount": {
    "type": "integer",
    "readOnly": true
   },
   "failureReasons": {
    "type": "object",
    "readOnly": true,
    "additionalProperties": {
     "type": "integer"
    },
    "description": "**Grouped, because 40 workstations failing for one reason is one problem** and a list of 40 rows is forty.\n"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "RegionSettings": {
  "x-ticvai-persistence": "platform.region_settings",
  "type": "object",
  "required": [
   "countryCode",
   "currencyCode",
   "currencyScale",
   "timeZone",
   "fiscalYearStartMonth"
  ],
  "properties": {
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "description": "ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell."
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "description": "Decimal places for this region's currency. Varies by currency — some use 2, some use 3. Money columns are numeric(18,4) and carry the scale explicitly, because a fixed 2-place type silently truncates 3-place currencies.\n"
   },
   "timeZone": {
    "type": "string",
    "description": "IANA zone, e.g. `Asia/Dubai`."
   },
   "dateFormat": {
    "type": "string",
    "default": "dd/MM/yyyy"
   },
   "numberFormat": {
    "type": "string",
    "default": "#,##0.00"
   },
   "fiscalYearStartMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 12,
    "description": "Varies by country."
   },
   "allowedAiResidencies": {
    "type": "array",
    "description": "**The region's compliance gate on AI providers** (decided 28 September, audit R203; ADR-0009). The `AiProvider.residency` values a tenant in this region may use; empty means no restriction. `ai.setAiProvider` refuses any other residency with `409 residency-refused`. A prompt carrying guest data that reaches a provider hosted elsewhere is a cross-border transfer, and this is where a region says which it allows.\n",
    "default": [],
    "items": {
     "type": "string"
    }
   },
   "placement": {
    "$ref": "#/components/schemas/Placement"
   },
   "cellName": {
    "type": "string",
    "readOnly": true,
    "description": "The cell serving this region. One cell per tenant per region (ADR-0014).\n"
   }
  }
 },
 "ScopeLevel": {
  "type": "string",
  "description": "**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n",
  "enum": [
   "tenant",
   "brand",
   "region",
   "venue",
   "department",
   "subDepartment",
   "workstation",
   "outlet",
   "subject"
  ]
 },
 "SeatAttribute": {
  "type": "string",
  "description": "BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n",
  "enum": [
   "standard",
   "accessible",
   "companion",
   "obstructedView",
   "restrictedLegroom",
   "premium",
   "houseSeat",
   "buffer",
   "aisle",
   "endOfRow",
   "extraLegroom",
   "powerOutlet",
   "tableService",
   "shaded",
   "covered",
   "nearExit",
   "nearAccessibleWc",
   "wheelchairTransfer",
   "limitedRecline",
   "sofa",
   "beanbag"
  ]
 },
 "SeatMap": {
  "x-ticvai-persistence": "seating.seat_map",
  "allOf": [
   {
    "$ref": "#/components/schemas/SeatMapSummary"
   },
   {
    "type": "object",
    "required": [
     "sections"
    ],
    "properties": {
     "description": {
      "type": "string",
      "nullable": true
     },
     "viewBox": {
      "type": "object",
      "description": "Coordinate space for rendering. Absent when there is no geometry.",
      "nullable": true,
      "properties": {
       "width": {
        "type": "number"
       },
       "height": {
        "type": "number"
       }
      }
     },
     "stagePosition": {
      "$ref": "#/components/schemas/Point"
     },
     "sections": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/Section"
      }
     },
     "isActive": {
      "type": "boolean"
     }
    }
   }
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
 "Section": {
  "x-ticvai-persistence": "seating.section",
  "type": "object",
  "required": [
   "code",
   "name",
   "rowCount",
   "seatCount"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "rowCount": {
    "type": "integer"
   },
   "seatCount": {
    "type": "integer"
   },
   "boundary": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Point"
    },
    "description": "Polygon for rendering. Absent without geometry."
   },
   "viewAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "assets.MediaAsset",
    "description": "**The view of the stage from this section, as a photo**, uploaded through `assets` like any other media (decided 29 September, rev 3 23SEP-14). Optional: where it is null the client renders the view from the imported geometry (the section `boundary`, the map's `stagePosition` and the seat positions), so a closer section shows a larger stage and fewer rows ahead. Set with `updateSeatMap` `sectionViews`, which is allowed on a published map because a photo does not change the map's shape.\n"
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "label",
      "seatCount"
     ],
     "properties": {
      "label": {
       "type": "string"
      },
      "seatCount": {
       "type": "integer"
      },
      "numberingDirection": {
       "type": "string",
       "enum": [
        "leftToRight",
        "rightToLeft"
       ],
       "description": "Which end row numbering starts from. Not recoverable from a manifest and must be stated — it determines whether a guest finds their seat.\n"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "SetDenominationsRequest": {
  "type": "object",
  "description": "Request only. One currency's complete list; anything not in it is deactivated. Entries match existing rows on `kind` and `value` (see `setDenominations`).\n",
  "required": [
   "scopePath",
   "currencyCode",
   "denominations"
  ],
  "properties": {
   "scopePath": {
    "type": "string",
    "description": "The region the write is made at — the materialised path of a `region` scope node. The caller's `REGION_CONFIGURE` grant must cover it.\n"
   },
   "currencyCode": {
    "type": "string",
    "minLength": 3,
    "maxLength": 3
   },
   "denominations": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "displayName",
      "kind",
      "value",
      "sortOrder"
     ],
     "properties": {
      "displayName": {
       "type": "string",
       "maxLength": 60
      },
      "kind": {
       "type": "string",
       "enum": [
        "note",
        "coin"
       ]
      },
      "value": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "sortOrder": {
       "type": "integer",
       "minimum": 0
      },
      "isActive": {
       "type": "boolean",
       "default": true
      }
     }
    }
   }
  }
 },
 "VenueMap": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.map",
  "description": "A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n",
  "required": [
   "id",
   "name",
   "venueId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "Derived from `venueId`. Not sent by a client."
   },
   "kind": {
    "type": "string",
    "enum": [
     "park",
     "floor",
     "zone",
     "parking"
    ]
   },
   "floorLevel": {
    "type": "integer",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "archived"
    ],
    "readOnly": true,
    "description": "`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"
   },
   "publishedVersion": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "The `VenueMapVersion.version` guests are served. Null until the first publish.\n"
   },
   "graphVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"
   },
   "isGeoreferenced": {
    "type": "boolean",
    "readOnly": true,
    "description": "**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"
   },
   "baseAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n",
    "x-ticvai-references": "assets.MediaAsset"
   },
   "baseImageAlignment": {
    "type": "object",
    "nullable": true,
    "description": "**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n",
    "properties": {
     "imageWidthPx": {
      "type": "integer"
     },
     "imageHeightPx": {
      "type": "integer"
     },
     "anchors": {
      "type": "array",
      "minItems": 2,
      "maxItems": 4,
      "items": {
       "type": "object",
       "properties": {
        "planX": {
         "type": "number"
        },
        "planY": {
         "type": "number"
        },
        "imageX": {
         "type": "number"
        },
        "imageY": {
         "type": "number"
        }
       }
      }
     }
    }
   },
   "tileSetRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"
   },
   "boundsGeoJson": {
    "type": "string",
    "nullable": true
   },
   "graphStatus": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "notBuilt",
     "connected",
     "disconnected",
     "partial"
    ],
    "description": "**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"
   }
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
 },
 "VisualWorkflowDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; writes approvals.workflow_definition and a draft approvals.workflow_version (data model for the agreed operations, 29 September)",
  "description": "**What Visual Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "definition": {
    "type": "string",
    "description": "The workflow graph (nodes and connections) as a JSON document"
   },
   "nodeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "start",
      "trigger",
      "task",
      "decision",
      "approval",
      "systemAction",
      "notification",
      "wait",
      "timer",
      "parallelBranch",
      "merge",
      "escalation",
      "subWorkflow",
      "end"
     ]
    },
    "description": "Node kinds used in this workflow"
   },
   "workflowName": {
    "type": "string",
    "description": "Workflow Name"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "businessProcess": {
    "type": "string",
    "description": "Business Process"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective Dates"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "deadEnds",
      "missingOutcomes",
      "circularLoops",
      "missingAssignee",
      "invalidActions"
     ]
    },
    "description": "Design problems the designer found (read-only)"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow identifier; absent on input to create a new workflow"
   },
   "trigger": {
    "type": "string",
    "description": "What starts the workflow"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "description": "Effective to"
   }
  },
  "required": [
   "workflowName",
   "module",
   "definition"
  ]
 },
 "VisualWorkflowDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_definition and its draft approvals.workflow_version (data model for the agreed operations, 29 September)",
  "description": "**What Visual Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "definition": {
    "type": "string",
    "description": "The workflow graph (nodes and connections) as a JSON document"
   },
   "nodeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "start",
      "trigger",
      "task",
      "decision",
      "approval",
      "systemAction",
      "notification",
      "wait",
      "timer",
      "parallelBranch",
      "merge",
      "escalation",
      "subWorkflow",
      "end"
     ]
    },
    "description": "Node kinds used in this workflow"
   },
   "workflowName": {
    "type": "string",
    "description": "Workflow Name"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "businessProcess": {
    "type": "string",
    "description": "Business Process"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective Dates"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "deadEnds",
      "missingOutcomes",
      "circularLoops",
      "missingAssignee",
      "invalidActions"
     ]
    },
    "description": "Design problems the designer found (read-only)"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow identifier; absent on input to create a new workflow"
   },
   "trigger": {
    "type": "string",
    "description": "What starts the workflow"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "description": "Effective to"
   }
  },
  "required": [
   "workflowName",
   "module",
   "definition"
  ]
 }
}
```
