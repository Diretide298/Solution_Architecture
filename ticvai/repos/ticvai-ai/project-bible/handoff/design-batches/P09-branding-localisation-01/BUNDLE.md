# P09-branding-localisation-01 — P09 · Branding & Localisation

**4 screens · 24 operations · 29 schemas · 4 permissions**

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
  `PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH`. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: listFaqs
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-016` | White-Label Branding Management | listDetail | 11 | 0 | — |
| `ADM-017` | Domain & Certificate Management | listDetail | 4 | 0 | — |
| `ADM-018` | Localisation & Language Pack | listDetail | 5 | 0 | — |
| `ADM-019` | Global Configuration & Defaults | listDetail | 4 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-016",
  "name": "White-Label Branding Management",
  "module": "Branding & Localisation",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C57",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/white-label-branding-management",
   "component": "apps/ticvai-web/src/routes/general/WhiteLabelBrandingManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-017"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **30 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listConfigVersions` reads the population and `getAppIcons` reads one of them — list, select, act",
  "purpose": "See white-label branding management for this venue.",
  "gaps": [
   {
    "operation": "getBrandIdentity",
    "why": "**2 declared operations reach no component on this screen**: getBrandIdentity, getTheme. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every white-label branding",
       "bindsTo": "ConfigVersion",
       "columns": [
        "ConfigVersion.publishedAt",
        "ConfigVersion.publishedByPrincipalId",
        "ConfigVersion.publishedByName",
        "ConfigVersion.note",
        "ConfigVersion.isCurrent",
        "ConfigVersion.scheduledFor",
        "ConfigVersion.contentHash",
        "ConfigVersion.pendingBuildTimeChanges",
        "ConfigVersion.scopePath"
       ],
       "operation": "listConfigVersions",
       "provenance": "contract white-label.yaml GET /tenant-config/versions"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected white-label branding",
       "bindsTo": "AppIcons",
       "columns": [
        "AppIcons.sourceAssetRef",
        "AppIcons.derived",
        "AppIcons.changeScope",
        "AppIcons.liveVersion",
        "AppIcons.requiresRebuild"
       ],
       "operation": "getAppIcons",
       "provenance": "contract white-label.yaml GET /tenant-config/app-icons"
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
       "operation": "createPreview",
       "provenance": "contract white-label.yaml POST /tenant-config/preview"
      },
      {
       "kind": "secondaryButton",
       "label": "Diff",
       "operation": "diffConfigVersion",
       "provenance": "contract white-label.yaml GET /tenant-config/versions/{version}/diff"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "operation": "publishTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Restore",
       "operation": "restoreConfigVersion",
       "provenance": "contract white-label.yaml POST /tenant-config/versions/{version}/restore"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAppIcons",
       "provenance": "contract white-label.yaml PUT /tenant-config/app-icons"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setBrandIdentity",
       "provenance": "contract white-label.yaml PUT /tenant-config/brand"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setTheme",
       "provenance": "contract white-label.yaml PUT /tenant-config/theme"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "publishGate",
       "impliedBy": "publishTenantConfig",
       "notes": "Declares `publishTenantConfig`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The white-label branding list.",
   "error": "Could not load. Names which read failed and leaves the white-label branding untouched.",
   "emptyFirstRun": "No white-label branding yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the white-label branding are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createPreview",
    "contract": "white-label",
    "purpose": "Generate a preview link",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "diffConfigVersion",
    "contract": "white-label",
    "purpose": "Compare a version against the working draft",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAppIcons",
    "contract": "white-label",
    "purpose": "Read app icon set",
    "trigger": "onLoad"
   },
   {
    "operationId": "getBrandIdentity",
    "contract": "white-label",
    "purpose": "Read brand identity",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTheme",
    "contract": "white-label",
    "purpose": "Read colour theme",
    "trigger": "onLoad"
   },
   {
    "operationId": "listConfigVersions",
    "contract": "white-label",
    "purpose": "Version history",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishTenantConfig",
    "contract": "white-label",
    "purpose": "Publish the working draft",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "restoreConfigVersion",
    "contract": "white-label",
    "purpose": "Restore a previous version",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "setAppIcons",
    "contract": "white-label",
    "purpose": "Set app icons",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "setBrandIdentity",
    "contract": "white-label",
    "purpose": "Set logo, favicon and splash",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "setTheme",
    "contract": "white-label",
    "purpose": "Set colour theme",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bannerId",
     "from": "deepLink"
    },
    {
     "name": "pageId",
     "from": "deepLink"
    },
    {
     "name": "policyKind",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`.",
   "preloaded": [
    "AppIcons.sourceAssetRef",
    "AppIcons.derived",
    "AppIcons.changeScope",
    "AppIcons.liveVersion",
    "AppIcons.requiresRebuild"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-016"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 11 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-017",
  "name": "Domain & Certificate Management",
  "module": "Branding & Localisation",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/domain-and-certificate-management",
   "component": "apps/ticvai-web/src/routes/general/DomainAndCertificateManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-016"
   ],
   "transitions": [
    {
     "to": "ADM-016",
     "trigger": "White-Label Branding Management",
     "provenance": "flow F103 step 1→2"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **41 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it. **Rebuilt 24 August.** This screen declared 41 operations and **not one was about a domain** — it carried the bulk-attached white-label set, and no domain or certificate operation existed anywhere in the package. **A white-label platform whose tenants cannot use their own domain is white-label in name only.**",
  "openQuestions": [
   "No contract — not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCustomDomains` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See domain & certificate management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every domain certificate",
       "bindsTo": "CustomDomain",
       "columns": [
        "CustomDomain.id",
        "CustomDomain.hostname",
        "CustomDomain.kind",
        "CustomDomain.status",
        "CustomDomain.verificationMethod",
        "CustomDomain.verificationToken",
        "CustomDomain.certificateExpiresAt",
        "CustomDomain.lastCheckedAt",
        "CustomDomain.failureReason"
       ],
       "operation": "listCustomDomains",
       "provenance": "contract white-label.yaml GET /tenant-domains"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected domain certificate",
       "bindsTo": "CustomDomain",
       "columns": [
        "CustomDomain.id",
        "CustomDomain.hostname",
        "CustomDomain.kind",
        "CustomDomain.status",
        "CustomDomain.verificationMethod",
        "CustomDomain.verificationToken",
        "CustomDomain.certificateExpiresAt",
        "CustomDomain.lastCheckedAt",
        "CustomDomain.failureReason"
       ],
       "operation": "listCustomDomains",
       "provenance": "contract white-label.yaml GET /tenant-domains"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Claim",
       "operation": "claimCustomDomain",
       "provenance": "contract white-label.yaml POST /tenant-domains"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyCustomDomain",
       "provenance": "contract white-label.yaml POST /tenant-domains/{domainId}/verify"
      },
      {
       "kind": "secondaryButton",
       "label": "Release hold",
       "operation": "relinquishCustomDomain",
       "provenance": "contract white-label.yaml DELETE /tenant-domains/{domainId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The domain certificate list.",
   "error": "Could not load. Names which read failed and leaves the domain certificate untouched.",
   "emptyFirstRun": "No domain certificate yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the domain certificate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomDomains",
    "contract": "white-label",
    "purpose": "The domains this tenant has claimed",
    "trigger": "onLoad"
   },
   {
    "operationId": "claimCustomDomain",
    "contract": "white-label",
    "purpose": "Claim a domain and get a verification token",
    "trigger": "onAction",
    "invalidates": [
     "listCustomDomains"
    ]
   },
   {
    "operationId": "verifyCustomDomain",
    "contract": "white-label",
    "purpose": "Check the record and issue the certificate",
    "trigger": "onAction",
    "invalidates": [
     "listCustomDomains"
    ]
   },
   {
    "operationId": "relinquishCustomDomain",
    "contract": "white-label",
    "purpose": "Give the domain up",
    "trigger": "onAction",
    "invalidates": [
     "listCustomDomains"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bannerId",
     "from": "deepLink"
    },
    {
     "name": "pageId",
     "from": "deepLink"
    },
    {
     "name": "policyKind",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    },
    {
     "name": "domainId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`.",
   "preloaded": [
    "CustomDomain.id",
    "CustomDomain.hostname",
    "CustomDomain.kind",
    "CustomDomain.status",
    "CustomDomain.verificationMethod"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-017"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-018",
  "name": "Localisation & Language Pack",
  "module": "Branding & Localisation",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C57",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/localisation-and-language-pack",
   "component": "apps/ticvai-web/src/routes/general/LocalisationAndLanguagePackDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **36 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listFaqs` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Configure localisation & language pack for this venue.",
  "gaps": [
   {
    "operation": "listPolicies",
    "why": "**1 declared operation reach no component on this screen**: listPolicies. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every localisation language pack",
       "bindsTo": "FaqCategory",
       "columns": [
        "FaqCategory.code",
        "FaqCategory.name",
        "FaqCategory.sortOrder",
        "FaqCategory.entries",
        "FaqCategory.scopePath"
       ],
       "operation": "listFaqs",
       "provenance": "contract white-label.yaml GET /tenant-config/faqs"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected localisation language pack",
       "bindsTo": "FaqCategory",
       "columns": [
        "FaqCategory.code",
        "FaqCategory.name",
        "FaqCategory.sortOrder",
        "FaqCategory.entries",
        "FaqCategory.scopePath"
       ],
       "operation": "listFaqs",
       "provenance": "contract white-label.yaml GET /tenant-config/faqs"
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
       "operation": "setLanguages",
       "provenance": "contract white-label.yaml PUT /tenant-config/languages"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setFaqs",
       "provenance": "contract white-label.yaml PUT /tenant-config/faqs"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setPolicy",
       "provenance": "contract white-label.yaml PUT /tenant-config/policies/{policyKind}"
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
       "impliedBy": "setLanguages",
       "label": "Save languages",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listFaqs",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setLanguages",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The localisation language pack list.",
   "error": "Could not load. Names which read failed and leaves the localisation language pack untouched.",
   "emptyFirstRun": "No localisation language pack yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the localisation language pack are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setLanguages",
    "contract": "white-label",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "listFaqs",
    "contract": "white-label",
    "purpose": "List FAQs",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPolicies",
    "contract": "white-label",
    "purpose": "List legal policies",
    "trigger": "onLoad"
   },
   {
    "operationId": "setFaqs",
    "contract": "white-label",
    "purpose": "Set FAQ categories and entries",
    "trigger": "onAction",
    "invalidates": [
     "listFaqs"
    ]
   },
   {
    "operationId": "setPolicy",
    "contract": "white-label",
    "purpose": "Publish a policy version",
    "trigger": "onAction",
    "invalidates": [
     "listFaqs"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bannerId",
     "from": "deepLink"
    },
    {
     "name": "pageId",
     "from": "deepLink"
    },
    {
     "name": "policyKind",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`.",
   "preloaded": [
    "FaqCategory.code",
    "FaqCategory.name",
    "FaqCategory.sortOrder",
    "FaqCategory.entries",
    "FaqCategory.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-018"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "ADM-019",
  "name": "Global Configuration & Defaults",
  "module": "Branding & Localisation",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C95",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/global-configuration-and-defaults",
   "component": "apps/ticvai-web/src/routes/general/GlobalConfigurationAndDefaultsForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — ADM-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId",
      "rightId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "No contract — platform defaults not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPlans` reads the population and `getPlan` reads one of them — list, select, act",
  "purpose": "Change how global behaves here, and see which level the current value came from.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every global defaults",
       "bindsTo": "Plan",
       "columns": [
        "Plan.code",
        "Plan.name",
        "Plan.description",
        "Plan.cellTier",
        "Plan.licensedModules",
        "Plan.limits",
        "Plan.basePrice",
        "Plan.billingPeriod",
        "Plan.includesBrandedApp",
        "Plan.includedAiTokens",
        "Plan.id",
        "Plan.isActive"
       ],
       "operation": "listPlans",
       "provenance": "contract subscription.yaml GET /plans"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected global defaults",
       "bindsTo": "Plan",
       "columns": [
        "Plan.code",
        "Plan.name",
        "Plan.description",
        "Plan.cellTier",
        "Plan.licensedModules",
        "Plan.limits",
        "Plan.basePrice",
        "Plan.billingPeriod",
        "Plan.includesBrandedApp",
        "Plan.includedAiTokens",
        "Plan.id",
        "Plan.isActive",
        "Plan.subscriberCount",
        "Plan.publishedAt"
       ],
       "operation": "getPlan",
       "provenance": "contract subscription.yaml GET /plans/{planId}"
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
       "operation": "createPlan",
       "provenance": "contract subscription.yaml POST /plans"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createPlanVersion",
       "provenance": "contract subscription.yaml POST /plans/{planId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The global defaults list.",
   "error": "Could not load. Names which read failed and leaves the global defaults untouched.",
   "emptyFirstRun": "No global defaults yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the global defaults are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPlans",
    "contract": "subscription",
    "purpose": "List subscription plans",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPlan",
    "contract": "subscription",
    "purpose": "Create a subscription plan",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   },
   {
    "operationId": "createPlanVersion",
    "contract": "subscription",
    "purpose": "Publish a new version of a plan",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   },
   {
    "operationId": "getPlan",
    "contract": "subscription",
    "purpose": "Read a plan",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "planId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `planId`.",
   "preloaded": [
    "Plan.code",
    "Plan.name",
    "Plan.description",
    "Plan.cellTier",
    "Plan.licensedModules"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-019"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "claimCustomDomain": {
  "method": "POST",
  "path": "/tenant-domains",
  "contract": "white-label",
  "summary": "Claim a domain and get a verification token",
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
  "requestBody": null,
  "responds": "CustomDomain"
 },
 "createPlan": {
  "method": "POST",
  "path": "/plans",
  "contract": "subscription",
  "summary": "Create a subscription plan",
  "permission": "PLATFORM_PLAN_MANAGE",
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
  "requestBody": "CreatePlanRequest",
  "responds": "Plan"
 },
 "createPlanVersion": {
  "method": "POST",
  "path": "/plans/{planId}",
  "contract": "subscription",
  "summary": "Publish a new version of a plan",
  "permission": "PLATFORM_PLAN_MANAGE",
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
  "requestBody": "CreatePlanRequest",
  "responds": "Plan"
 },
 "createPreview": {
  "method": "POST",
  "path": "/tenant-config/preview",
  "contract": "white-label",
  "summary": "Generate a preview link",
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
  "requestBody": null,
  "responds": "Preview"
 },
 "diffConfigVersion": {
  "method": "GET",
  "path": "/tenant-config/versions/{version}/diff",
  "contract": "white-label",
  "summary": "Compare a version against the working draft",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "against",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ConfigDiff"
 },
 "getAppIcons": {
  "method": "GET",
  "path": "/tenant-config/app-icons",
  "contract": "white-label",
  "summary": "Read app icon set",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AppIcons"
 },
 "getBrandIdentity": {
  "method": "GET",
  "path": "/tenant-config/brand",
  "contract": "white-label",
  "summary": "Read brand identity",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "BrandIdentity"
 },
 "getPlan": {
  "method": "GET",
  "path": "/plans/{planId}",
  "contract": "subscription",
  "summary": "Read a plan",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Plan"
 },
 "getTheme": {
  "method": "GET",
  "path": "/tenant-config/theme",
  "contract": "white-label",
  "summary": "Read colour theme",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Theme"
 },
 "listConfigVersions": {
  "method": "GET",
  "path": "/tenant-config/versions",
  "contract": "white-label",
  "summary": "Version history",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "listCustomDomains": {
  "method": "GET",
  "path": "/tenant-domains",
  "contract": "white-label",
  "summary": "The domains this tenant has claimed",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CustomDomain"
 },
 "listFaqs": {
  "method": "GET",
  "path": "/tenant-config/faqs",
  "contract": "white-label",
  "summary": "List FAQs",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "FaqCategory"
 },
 "listPlans": {
  "method": "GET",
  "path": "/plans",
  "contract": "subscription",
  "summary": "List subscription plans",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Plan"
 },
 "listPolicies": {
  "method": "GET",
  "path": "/tenant-config/policies",
  "contract": "white-label",
  "summary": "List legal policies",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Policy"
 },
 "publishTenantConfig": {
  "method": "POST",
  "path": "/tenant-config/publish",
  "contract": "white-label",
  "summary": "Publish the working draft",
  "permission": "TENANT_PUBLISH",
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
  "requestBody": null,
  "responds": "ConfigVersion"
 },
 "relinquishCustomDomain": {
  "method": "DELETE",
  "path": "/tenant-domains/{domainId}",
  "contract": "white-label",
  "summary": "Give the domain up",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "restoreConfigVersion": {
  "method": "POST",
  "path": "/tenant-config/versions/{version}/restore",
  "contract": "white-label",
  "summary": "Restore a previous version",
  "permission": "TENANT_PUBLISH",
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
  "requestBody": null,
  "responds": "TenantConfig"
 },
 "setAppIcons": {
  "method": "PUT",
  "path": "/tenant-config/app-icons",
  "contract": "white-label",
  "summary": "Set app icons",
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
  "requestBody": null,
  "responds": "AppIcons"
 },
 "setBrandIdentity": {
  "method": "PUT",
  "path": "/tenant-config/brand",
  "contract": "white-label",
  "summary": "Set logo, favicon and splash",
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
  "requestBody": "BrandIdentity",
  "responds": "BrandIdentity"
 },
 "setFaqs": {
  "method": "PUT",
  "path": "/tenant-config/faqs",
  "contract": "white-label",
  "summary": "Set FAQ categories and entries",
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
  "requestBody": null,
  "responds": "FaqCategory"
 },
 "setLanguages": {
  "method": "PUT",
  "path": "/tenant-config/languages",
  "contract": "white-label",
  "summary": "Set enabled languages and default",
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
  "requestBody": null,
  "responds": "LanguageConfig"
 },
 "setPolicy": {
  "method": "PUT",
  "path": "/tenant-config/policies/{policyKind}",
  "contract": "white-label",
  "summary": "Publish a policy version",
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
  "requestBody": null,
  "responds": "Policy"
 },
 "setTheme": {
  "method": "PUT",
  "path": "/tenant-config/theme",
  "contract": "white-label",
  "summary": "Set colour theme",
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
  "requestBody": "Theme",
  "responds": "Theme"
 },
 "verifyCustomDomain": {
  "method": "POST",
  "path": "/tenant-domains/{domainId}/verify",
  "contract": "white-label",
  "summary": "Check the record and issue the certificate",
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
  "requestBody": null,
  "responds": "CustomDomain"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessibilitySettings": {
  "type": "object",
  "description": "BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n",
  "properties": {
   "largeTextAvailable": {
    "type": "boolean",
    "default": true
   },
   "highContrastAvailable": {
    "type": "boolean",
    "default": true
   },
   "simplifiedNavigationAvailable": {
    "type": "boolean",
    "default": true
   },
   "screenReaderSupported": {
    "type": "boolean",
    "default": true
   },
   "reachableHeightModeAvailable": {
    "type": "boolean",
    "default": false,
    "description": "**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"
   },
   "sessionTimeoutMultiplier": {
    "type": "number",
    "default": 1,
    "description": "**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"
   }
  }
 },
 "AppIcons": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "sourceAssetRef",
   "changeScope"
  ],
  "properties": {
   "sourceAssetRef": {
    "type": "string"
   },
   "derived": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string"
      },
      "size": {
       "type": "string"
      },
      "assetRef": {
       "type": "string"
      }
     }
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true
   },
   "liveVersion": {
    "type": "string",
    "nullable": true,
    "description": "Icon currently shipped. Differs from the draft until the next release."
   },
   "requiresRebuild": {
    "type": "boolean",
    "readOnly": true
   }
  }
 },
 "BrandIdentity": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "logoAssetRef"
  ],
  "properties": {
   "logoAssetRef": {
    "type": "string"
   },
   "logoDarkAssetRef": {
    "type": "string",
    "nullable": true,
    "description": "Used on dark backgrounds. Falls back to the primary logo."
   },
   "faviconAssetRef": {
    "type": "string",
    "nullable": true
   },
   "splashImageAssetRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "splashDurationSeconds": {
    "type": "integer",
    "minimum": 0,
    "maximum": 10,
    "default": 3
   },
   "splashBackgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "showLoadingIndicator": {
    "type": "boolean",
    "default": true
   },
   "splashChangeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Always `buildTime` for native apps."
   }
  }
 },
 "CellTier": {
  "type": "string",
  "enum": [
   "shared",
   "dedicated",
   "isolated",
   "clientHosted"
  ]
 },
 "ChangeScope": {
  "type": "string",
  "description": "Whether a change reaches guests on publish or needs a store release.\n",
  "enum": [
   "runtime",
   "buildTime"
  ]
 },
 "ConfigDiff": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fromVersion",
   "toVersion",
   "changes"
  ],
  "properties": {
   "fromVersion": {
    "type": "string"
   },
   "toVersion": {
    "type": "string"
   },
   "changes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "area",
      "path",
      "changeKind"
     ],
     "properties": {
      "area": {
       "type": "string"
      },
      "path": {
       "type": "string"
      },
      "changeKind": {
       "type": "string",
       "enum": [
        "added",
        "removed",
        "modified"
       ]
      },
      "before": {
       "type": "string",
       "nullable": true
      },
      "after": {
       "type": "string",
       "nullable": true
      },
      "changeScope": {
       "$ref": "#/components/schemas/ChangeScope"
      }
     }
    }
   }
  }
 },
 "ConfigVersion": {
  "x-ticvai-persistence": "whitelabel.config_version",
  "type": "object",
  "required": [
   "version",
   "publishedAt",
   "publishedByPrincipalId",
   "note",
   "isCurrent"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedByName": {
    "type": "string"
   },
   "note": {
    "type": "string"
   },
   "isCurrent": {
    "type": "boolean"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "contentHash": {
    "type": "string"
   },
   "pendingBuildTimeChanges": {
    "type": "array",
    "description": "Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string"
      },
      "description": {
       "type": "string"
      },
      "platforms": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "CreatePlanRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "cellTier",
   "licensedModules",
   "limits",
   "basePrice"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "cellTier": {
    "$ref": "#/components/schemas/CellTier"
   },
   "licensedModules": {
    "type": "array",
    "minItems": 1,
    "description": "**A closed set as of 24 August.** `moduleKey` was a free string, so nothing could join a licence to a screen — **a tenant without an F&B licence was still served every F&B screen**, because no screen said which module it belonged to in a form the licence could match.\n**The key is the join.** `screen.requiresModule` names one of these, and navigation is built from the intersection of what a tenant licensed and what their role permits.\n",
    "items": {
     "$ref": "#/components/schemas/ModuleKey"
    }
   },
   "limits": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/EntitlementLimit"
    }
   },
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "billingPeriod": {
    "type": "string",
    "enum": [
     "monthly",
     "quarterly",
     "annual"
    ]
   },
   "includesBrandedApp": {
    "type": "boolean",
    "description": "Branded native publishing carries per-tenant operational cost and is priced, not absorbed.\n"
   },
   "includedAiTokens": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "CustomDomain": {
  "type": "object",
  "x-ticvai-persistence": "whitelabel.custom_domain",
  "description": "24 August. **`ADM-017 Domain & Certificate Management` declared 41 operations and not one of them was about a domain** — it carried the same bulk-attached set as every other white-label screen, and **no domain or certificate operation existed anywhere in 1,010.**\nA white-label platform whose tenants cannot use their own domain is a white-label platform in name only.\n**Verification before issuance, always.** A certificate issued for a domain the tenant does not control is a certificate issued to whoever asked.\n",
  "required": [
   "id",
   "tenantId",
   "hostname",
   "status"
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
   "hostname": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "guestWeb",
     "guestApp",
     "partnerPortal",
     "developerPortal"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "verifying",
     "verified",
     "issuing",
     "active",
     "failed",
     "expired",
     "revoked"
    ]
   },
   "verificationMethod": {
    "type": "string",
    "enum": [
     "dnsTxt",
     "cname",
     "httpFile"
    ]
   },
   "verificationToken": {
    "type": "string",
    "readOnly": true
   },
   "certificateExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Renewal is a job, not a reminder.** A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder email on a Saturday.\n"
   },
   "lastCheckedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "failureReason": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "EntitlementLimit": {
  "type": "object",
  "required": [
   "metric",
   "limit"
  ],
  "properties": {
   "metric": {
    "$ref": "#/components/schemas/UsageMetric"
   },
   "limit": {
    "type": "integer",
    "nullable": true,
    "description": "Null means unlimited."
   },
   "overageAllowed": {
    "type": "boolean",
    "default": false
   },
   "overageUnitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FaqCategory": {
  "x-ticvai-persistence": "whitelabel.faq_category + whitelabel.faq_entry",
  "type": "object",
  "required": [
   "code",
   "name",
   "entries"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "sortOrder": {
    "type": "integer"
   },
   "entries": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "question",
      "answer"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "question": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "answer": {
       "$ref": "#/components/schemas/LocalisedRichText"
      },
      "sortOrder": {
       "type": "integer"
      },
      "isPublished": {
       "type": "boolean"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "FeatureToggle": {
  "x-ticvai-persistence": "whitelabel.feature_toggle",
  "type": "object",
  "required": [
   "featureKey",
   "isEnabled",
   "changeScope"
  ],
  "properties": {
   "featureKey": {
    "type": "string",
    "enum": [
     "digitalCompanionMode",
     "aiConciergeChat",
     "lostAndFound",
     "pushNotifications",
     "socialSharing",
     "multiLanguage",
     "appleWallet",
     "googlePay",
     "applePay",
     "cashOnDelivery",
     "guestCheckout",
     "uaePassLogin"
    ]
   },
   "displayName": {
    "type": "string"
   },
   "isEnabled": {
    "type": "boolean"
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"
   },
   "requiresConfiguration": {
    "type": "boolean",
    "description": "True where the feature needs credentials or setup elsewhere first."
   }
  }
 },
 "FontConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryLatin"
  ],
  "properties": {
   "primaryLatin": {
    "type": "string"
   },
   "primaryArabic": {
    "type": "string",
    "nullable": true,
    "description": "Required when Arabic is enabled. A Latin face alone leaves Arabic in a system fallback that will not match.\n"
   },
   "secondaryLatin": {
    "type": "string",
    "nullable": true
   },
   "secondaryArabic": {
    "type": "string",
    "nullable": true
   },
   "customFontAssetRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Custom font files are `buildTime`; selecting a bundled face is `runtime`."
   }
  }
 },
 "FooterConfig": {
  "type": "object",
  "x-ticvai-persistence": "control.footer_config",
  "description": "BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n",
  "required": [
   "id",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "heading": {
       "type": "string"
      },
      "links": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "label": {
          "type": "string"
         },
         "url": {
          "type": "string"
         },
         "opensCookiePreferences": {
          "type": "boolean",
          "default": false
         }
        }
       }
      }
     }
    }
   },
   "legalLinks": {
    "type": "object",
    "description": "**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n",
    "properties": {
     "termsUrl": {
      "type": "string"
     },
     "privacyUrl": {
      "type": "string"
     },
     "accessibilityUrl": {
      "type": "string",
      "nullable": true
     },
     "cookiePolicyUrl": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "copyrightText": {
    "type": "string"
   },
   "socialLinks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string"
      },
      "url": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "HeaderConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "layout"
  ],
  "properties": {
   "layout": {
    "type": "string",
    "enum": [
     "logoLeft",
     "logoCentre",
     "logoWithMenu"
    ]
   },
   "showLogo": {
    "type": "boolean",
    "default": true
   },
   "showMenu": {
    "type": "boolean",
    "default": true
   },
   "showNotifications": {
    "type": "boolean",
    "default": true
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   }
  }
 },
 "HomepageLayout": {
  "x-ticvai-persistence": "whitelabel.homepage_section",
  "type": "object",
  "required": [
   "sections"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "sortOrder",
      "isVisible"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "kind": {
       "$ref": "#/components/schemas/HomepageSectionKind"
      },
      "title": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "sortOrder": {
       "type": "integer"
      },
      "isVisible": {
       "type": "boolean"
      },
      "contentPageId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "maxItems": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "LanguageConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "languages",
   "defaultLanguage"
  ],
  "properties": {
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "defaultLanguage": {
    "type": "string"
   },
   "rtlLanguages": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "string"
    }
   },
   "translationGaps": {
    "type": "array",
    "readOnly": true,
    "description": "Content lacking a version in an enabled language.",
    "items": {
     "type": "object",
     "properties": {
      "language": {
       "type": "string"
      },
      "missingCount": {
       "type": "integer"
      },
      "areas": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   }
  }
 },
 "LocalisedRichText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "description": "Keyed by language code. Values are sanitised HTML.",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "ModuleEnablement": {
  "x-ticvai-persistence": "whitelabel.module_enablement",
  "type": "object",
  "required": [
   "moduleKey",
   "isLicensed",
   "isEnabled"
  ],
  "properties": {
   "moduleKey": {
    "$ref": "#/components/schemas/ModuleKey"
   },
   "displayName": {
    "type": "string"
   },
   "isLicensed": {
    "type": "boolean",
    "description": "From the tenant's subscription. False makes enablement impossible."
   },
   "isEnabled": {
    "type": "boolean"
   },
   "referencedBy": {
    "type": "array",
    "readOnly": true,
    "description": "Navigation items and homepage sections pointing at this module.",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "ModuleKey": {
  "type": "string",
  "description": "What a tenant buys, and what a screen belongs to. **One vocabulary for both sides of the join**, because two lists that must agree are one list somebody forgets to update.\n**Grain chosen to match how a venue buys, not how the package is built.** `fnb` is one module even though it spans four contracts; `ticketing` and `access` are separate because a venue can run a museum with no gates and a stadium with no shop.\n",
  "enum": [
   "core",
   "ticketing",
   "access",
   "fnb",
   "retail",
   "inventory",
   "seating",
   "membership",
   "marketing",
   "resources",
   "queue",
   "games",
   "maintenance",
   "accreditation",
   "partner",
   "developerApi",
   "analytics",
   "ai"
  ],
  "x-ticvai-note": "**`core` is listed and cannot be unlicensed.** It exists so a screen can say it belongs to no optional module rather than leaving the field empty — **an empty field and *always on* look identical, and only one of them is a decision.**\n"
 },
 "NavigationConfig": {
  "x-ticvai-persistence": "whitelabel.navigation_item",
  "type": "object",
  "required": [
   "kind",
   "items"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "kind": {
    "type": "string",
    "enum": [
     "bottomNavigation",
     "drawer",
     "tabs"
    ]
   },
   "items": {
    "type": "array",
    "maxItems": 12,
    "items": {
     "type": "object",
     "required": [
      "label",
      "target",
      "isVisible",
      "sortOrder"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "icon": {
       "type": "string"
      },
      "target": {
       "$ref": "#/components/schemas/LinkTarget"
      },
      "isVisible": {
       "type": "boolean",
       "description": "At most five may be visible in bottom navigation; the rest overflow."
      },
      "sortOrder": {
       "type": "integer"
      }
     }
    }
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
 "Plan": {
  "x-ticvai-persistence": "control.subscription_plan",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreatePlanRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version",
     "isActive",
     "subscriberCount"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "version": {
      "type": "string",
      "description": "Existing subscribers stay on the version they were sold. A price change never applies retroactively.\n"
     },
     "isActive": {
      "type": "boolean"
     },
     "subscriberCount": {
      "type": "integer"
     },
     "publishedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "Policy": {
  "x-ticvai-persistence": "whitelabel.policy",
  "type": "object",
  "required": [
   "kind",
   "version",
   "body",
   "effectiveFrom",
   "publishedAt"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/PolicyKind"
   },
   "version": {
    "type": "string",
    "description": "Immutable. A guest who consented to version 3 consented to version 3, and a policy that changes under a recorded consent is a compliance failure.\n"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedRichText"
   },
   "requiresReconsent": {
    "type": "boolean"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
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
 },
 "PolicyKind": {
  "type": "string",
  "enum": [
   "privacy",
   "termsAndConditions",
   "refund",
   "cookie",
   "accessibility"
  ]
 },
 "Preview": {
  "x-ticvai-persistence": "none — short-lived, cache only",
  "type": "object",
  "required": [
   "previewId",
   "url",
   "expiresAt"
  ],
  "properties": {
   "previewId": {
    "type": "string",
    "format": "uuid"
   },
   "url": {
    "type": "string"
   },
   "platform": {
    "type": "string"
   },
   "theme": {
    "type": "string"
   },
   "language": {
    "type": "string"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "TenantConfig": {
  "x-ticvai-persistence": "whitelabel.tenant_config",
  "type": "object",
  "required": [
   "tenantId",
   "version",
   "brand",
   "theme",
   "fonts",
   "navigation",
   "homepage",
   "languages"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "string"
   },
   "isDraft": {
    "type": "boolean"
   },
   "brand": {
    "$ref": "#/components/schemas/BrandIdentity"
   },
   "appIcons": {
    "$ref": "#/components/schemas/AppIcons"
   },
   "theme": {
    "$ref": "#/components/schemas/Theme"
   },
   "fonts": {
    "$ref": "#/components/schemas/FontConfig"
   },
   "footer": {
    "$ref": "#/components/schemas/FooterConfig"
   },
   "notificationBranding": {
    "type": "object",
    "nullable": true,
    "description": "BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n",
    "properties": {
     "senderName": {
      "type": "string"
     },
     "replyToEmail": {
      "type": "string",
      "format": "email"
     },
     "smsSenderId": {
      "type": "string",
      "nullable": true
     },
     "whatsappBusinessId": {
      "type": "string",
      "nullable": true
     },
     "logoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   },
   "enabledPaymentMethods": {
    "type": "array",
    "nullable": true,
    "description": "BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n",
    "items": {
     "type": "string"
    }
   },
   "accessibility": {
    "$ref": "#/components/schemas/AccessibilitySettings"
   },
   "header": {
    "$ref": "#/components/schemas/HeaderConfig"
   },
   "navigation": {
    "$ref": "#/components/schemas/NavigationConfig"
   },
   "homepage": {
    "$ref": "#/components/schemas/HomepageLayout"
   },
   "modules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ModuleEnablement"
    }
   },
   "features": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FeatureToggle"
    }
   },
   "languages": {
    "$ref": "#/components/schemas/LanguageConfig"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Theme": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryColour",
   "secondaryColour",
   "backgroundColour",
   "textColour"
  ],
  "properties": {
   "primaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "secondaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "accentColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "textColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "darkMode": {
    "type": "object",
    "description": "Optional dark variant. Derived from the light theme when absent.",
    "properties": {
     "primaryColour": {
      "type": "string"
     },
     "backgroundColour": {
      "type": "string"
     },
     "textColour": {
      "type": "string"
     }
    }
   },
   "cornerRadius": {
    "type": "integer",
    "minimum": 0,
    "maximum": 32
   }
  }
 }
}
```
