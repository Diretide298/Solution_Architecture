# WS103 — Subscription Licensing AI Self Service board 6

**9 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-419` | Provisioning Command Center | listDetail | 0 | 0 | — |
| `ADM-420` | Tenant & Organization Provisioning | listDetail | 0 | 0 | — |
| `ADM-421` | Venue & Operational Structure Creation | configEditor | 0 | 0 | — |
| `ADM-422` | Administrator & Security Initialization | configEditor | 0 | 0 | — |
| `ADM-423` | License & Entitlement Activation | listDetail | 0 | 0 | — |
| `ADM-424` | Module Activation & Dependency Validation | listDetail | 0 | 0 | — |
| `ADM-425` | Venue Template Application | listDetail | 0 | 0 | — |
| `ADM-426` | Initial Configuration & Regional Defaults | configEditor | 0 | 0 | — |
| `ADM-427` | Provisioning Validation & Exception Management | listDetail | 0 | 0 | — |

## Thin screens in this batch

**ADM-419, ADM-420, ADM-423, ADM-424, ADM-425, ADM-427 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-419",
  "name": "Provisioning Command Center",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "1",
   "page": 72
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/provisioning-command-center-adm-419",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/ProvisioningCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-420",
    "ADM-421",
    "ADM-422",
    "ADM-423",
    "ADM-424",
    "ADM-425",
    "ADM-426",
    "ADM-427"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "ADM-420",
     "trigger": "Tenant & Organization Provisioning",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-421",
     "trigger": "Venue & Operational Structure Creation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-422",
     "trigger": "Administrator & Security Initialization",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-423",
     "trigger": "License & Entitlement Activation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-424",
     "trigger": "Module Activation & Dependency Validation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-425",
     "trigger": "Venue Template Application",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-426",
     "trigger": "Initial Configuration & Regional Defaults",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-427",
     "trigger": "Provisioning Validation & Exception Management",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show the overall status of the customer's environment creation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 72"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 72"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The provisioning list.",
   "error": "Could not load. Names which read failed and leaves the provisioning untouched.",
   "emptyFirstRun": "No provisioning yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the provisioning are still there. The pack's own statuses are Pending — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-419"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 72. 0 of 0 labels bound to a contract property; 6 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-420",
  "name": "Tenant & Organization Provisioning",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "2",
   "page": 73
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/tenant-organization-provisioning-adm-420",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/TenantOrganizationProvisioning.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create the customer's isolated TICVAI environment and primary organization structure.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 73"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 73"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The tenant organization provisioning list.",
   "error": "Could not load. Names which read failed and leaves the tenant organization provisioning untouched.",
   "emptyFirstRun": "No tenant organization provisioning yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tenant organization provisioning are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-420"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 73. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-421",
  "name": "Venue & Operational Structure Creation",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "3",
   "page": 74
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/venue-operational-structure-creation-adm-421",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/VenueOperationalStructureCreation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Venue Settings) and no display directory — it is settings, not a population",
  "purpose": "Automatically create the initial venue structure using information collected during onboarding.",
  "gaps": [
   {
    "operation": null,
    "why": "**Venue & Operational Structure Creation declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue Name",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Venue Type",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Address",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Operating Region",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Default Language",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      },
      {
       "kind": "selectField",
       "label": "Operating Model",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 74 §Venue Settings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue operational structure configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the venue operational structure untouched.",
   "emptyFirstRun": "No venue operational structure configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-421"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 74. 0 of 0 labels bound to a contract property; 8 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-422",
  "name": "Administrator & Security Initialization",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "4",
   "page": 75
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/administrator-security-initialization-adm-422",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/AdministratorSecurityInitialization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Security Setup) and no display directory — it is settings, not a population",
  "purpose": "Create the initial authorized customer administrator and establish the tenant security baseline.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "✓ Administrator Account Created",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Email Verified",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "textField",
       "label": "✓ Tenant Access Assigned",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "textField",
       "label": "✓ Default Role Applied",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "textField",
       "label": "✓ Security Policy Applied",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      },
      {
       "kind": "textField",
       "label": "✓ Audit Logging Enabled",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 75 §Security Setup"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The administrator security initialization configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the administrator security initialization untouched.",
   "emptyFirstRun": "No administrator security initialization configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-422"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 75. 0 of 0 labels bound to a contract property; 6 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-423",
  "name": "License & Entitlement Activation",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "5",
   "page": 76
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/license-entitlement-activation-adm-423",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/LicenseEntitlementActivation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Translate the commercial subscription purchased in Board 5 into enforceable technical entitlements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 76"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 76"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The license entitlement activation list.",
   "error": "Could not load. Names which read failed and leaves the license entitlement activation untouched.",
   "emptyFirstRun": "No license entitlement activation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the license entitlement activation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-423"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 76. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-424",
  "name": "Module Activation & Dependency Validation",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "6",
   "page": 77
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/module-activation-dependency-validation-adm-424",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/ModuleActivationDependencyValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Activate the modules purchased in Board 4/5 and verify all required dependencies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 77"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 77"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The module activation dependency list.",
   "error": "Could not load. Names which read failed and leaves the module activation dependency untouched.",
   "emptyFirstRun": "No module activation dependency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the module activation dependency are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-424"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 77. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-425",
  "name": "Venue Template Application",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "7",
   "page": 77
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/venue-template-application-adm-425",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/VenueTemplateApplication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Apply an appropriate initial configuration template based on the venue assessment from Board 2.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 77"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 77"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The venue template application list.",
   "error": "Could not load. Names which read failed and leaves the venue template application untouched.",
   "emptyFirstRun": "No venue template application yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue template application are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-425"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 77. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-426",
  "name": "Initial Configuration & Regional Defaults",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "8",
   "page": 78
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/initial-configuration-regional-defaults-adm-426",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/InitialConfigurationRegionalDefaults.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Low-risk settings such as; Business-critical settings such as) and no display directory — it is settings, not a population",
  "purpose": "Apply safe initial defaults using information already provided during onboarding.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Low-risk settings such as"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Low-risk settings such as"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Low-risk settings such as"
      },
      {
       "kind": "selectField",
       "label": "Venue Type",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Low-risk settings such as"
      },
      {
       "kind": "selectField",
       "label": "Ticket prices",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Tax",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Refund policy",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Payment rules",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Access rules",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Settlement",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      },
      {
       "kind": "selectField",
       "label": "Capacity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 78 §Business-critical settings such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The initial regional defaults configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the initial regional defaults untouched.",
   "emptyFirstRun": "No initial regional defaults configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-426"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 78. 0 of 0 labels bound to a contract property; 11 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-427",
  "name": "Provisioning Validation & Exception Management",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "6",
   "number": "9",
   "page": 79
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/provisioning-validation-exception-management-adm-427",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/ProvisioningValidationExceptionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-419"
   ],
   "exitTo": [
    "ADM-419"
   ],
   "transitions": [
    {
     "to": "ADM-419",
     "trigger": "Back to Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Validate that the environment has been created correctly before handing it to customer configuration.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 79"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 79"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The provisioning validation exception list.",
   "error": "Could not load. Names which read failed and leaves the provisioning validation exception untouched.",
   "emptyFirstRun": "No provisioning validation exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the provisioning validation exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-427"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 79. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
