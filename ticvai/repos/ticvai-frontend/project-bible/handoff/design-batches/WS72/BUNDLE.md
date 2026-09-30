# WS72 — Waiver, Consent & Digital Form Management board 1

**10 screens · 10 operations · 17 schemas · 2 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-041` | Waiver & Consent Command Center | commandCentre | 1 | 0 | — |
| `CMS-042` | Waiver Template Library & Master Setup | configEditor | 1 | 0 | — |
| `CMS-043` | Digital Waiver & Form Builder | listDetail | 1 | 0 | — |
| `CMS-044` | Dynamic Fields, Questions & Conditional Logic | configEditor | 1 | 0 | — |
| `CMS-045` | Signatory, Signature & Guardian Rule Configuration | configEditor | 1 | 0 | — |
| `CMS-046` | Product, Event & Experience Association | listDetail | 1 | 0 | — |
| `CMS-047` | Waiver Trigger, Eligibility & Completion Rules | configEditor | 1 | 0 | — |
| `CMS-048` | Versioning, Effective Dates & Legal Change Control | configEditor | 1 | 0 | — |
| `CMS-049` | Localization, Branding & Customer Experience Configuration | listDetail | 1 | 0 | — |
| `CMS-050` | Waiver Approval, Testing & Publication Workspace | configEditor | 1 | 0 | — |

## Thin screens in this batch

**CMS-043, CMS-049 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-041",
  "name": "Waiver & Consent Command Center",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.1",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/waiver-consent-command-center-cms-041",
   "component": "apps/venue-management-web/src/routes/policy/WaiverConsentCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-042",
    "CMS-043",
    "CMS-044",
    "CMS-045",
    "CMS-046",
    "CMS-047",
    "CMS-048",
    "CMS-049",
    "CMS-050"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-041 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-042",
     "trigger": "Works in Waiver Template Library & Master Setup",
     "provenance": "flow F181 step 1→2",
     "operation": "listWaiverConsent"
    },
    {
     "to": "CMS-043",
     "trigger": "Works in Digital Waiver & Form Builder",
     "provenance": "flow F181 step 3→4",
     "operation": "listWaiverConsent"
    },
    {
     "to": "CMS-044",
     "trigger": "Works in Dynamic Fields, Questions & Conditional Logic",
     "provenance": "flow F181 step 5→6",
     "operation": "listWaiverConsent"
    },
    {
     "to": "CMS-045",
     "trigger": "Works in Signatory, Signature & Guardian Rule Configuration",
     "provenance": "flow F181 step 7→8",
     "operation": "listWaiverConsent"
    },
    {
     "to": "CMS-046",
     "trigger": "Works in Product, Event & Experience Association",
     "provenance": "flow F181 step 9→10",
     "operation": "listWaiverConsent"
    },
    {
     "to": "CMS-047",
     "trigger": "Works in Waiver Trigger, Eligibility & Completion Rules",
     "provenance": "flow F181 step 11→12",
     "operation": "listWaiverConsent"
    },
    {
     "to": "CMS-048",
     "trigger": "Works in Versioning, Effective Dates & Legal Change Control",
     "provenance": "flow F181 step 13→14",
     "operation": "listWaiverConsent"
    },
    {
     "to": "CMS-049",
     "trigger": "Works in Localization, Branding & Customer Experience Configuration",
     "provenance": "flow F181 step 15→16",
     "operation": "listWaiverConsent"
    },
    {
     "to": "CMS-050",
     "trigger": "Works in Waiver Approval, Testing & Publication Workspace",
     "provenance": "flow F181 step 17→18",
     "operation": "listWaiverConsent"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized administrators can locate, manage and understand the lifecycle and usage of every waiver or consent form from one central workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should display) — counts over a population, then the population",
  "purpose": "Provide administrators with a centralized workspace for managing every waiver, consent form and digital declaration configured across TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 16 actions on this screen and the screen declares 1 operation.** Unserved: Liability Waiver, Parent/Guardian Consent, Participation Consent, Media Consent, Rental Agreement, Terms Acceptance, Membership Declaration, Create Waiver …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Support configurable classifications"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search waiver consent",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "WaiverConsentCommandCenterView.type",
        "Brand",
        "Venue",
        "Product",
        "Event",
        "WaiverConsentCommandCenterView.language",
        "WaiverConsentCommandCenterView.status",
        "WaiverConsentCommandCenterView.owner",
        "Effective Date"
       ],
       "notes": "The pack filters this screen by type, brand, venue, product, event, language and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Templates",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.waiverId",
       "notes": "Shows `kpis.totalTemplates` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      },
      {
       "kind": "metricTile",
       "label": "Published",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.status",
       "notes": "Shows `kpis.published` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      },
      {
       "kind": "metricTile",
       "label": "Draft",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.status",
       "notes": "Shows `kpis.draft` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.status",
       "notes": "Shows `kpis.pendingApproval` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      },
      {
       "kind": "metricTile",
       "label": "Scheduled",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.status",
       "notes": "Shows `kpis.scheduled` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      },
      {
       "kind": "metricTile",
       "label": "Expiring",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.effectiveTo",
       "notes": "Shows `kpis.expiring` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      },
      {
       "kind": "metricTile",
       "label": "Archived",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.status",
       "notes": "Shows `kpis.archived` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      },
      {
       "kind": "metricTile",
       "label": "Products Requiring Waiver",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.associatedProducts",
       "notes": "Shows `kpis.productsRequiringWaiver` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      },
      {
       "kind": "metricTile",
       "label": "Active Waiver Versions",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.publishedVersion",
       "notes": "Shows `kpis.activeWaiverVersions` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      },
      {
       "kind": "metricTile",
       "label": "Waivers Requiring Review",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.status",
       "notes": "Shows `kpis.waiversRequiringReview` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over."
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every waiver consent",
       "columns": [
        "WaiverConsentCommandCenterView.waiverId",
        "WaiverConsentCommandCenterView.waiverName",
        "WaiverConsentCommandCenterView.type",
        "WaiverConsentCommandCenterView.version",
        "WaiverConsentCommandCenterView.language",
        "WaiverConsentCommandCenterView.associatedProducts",
        "WaiverConsentCommandCenterView.signatoryType",
        "WaiverConsentCommandCenterView.effectiveFrom",
        "WaiverConsentCommandCenterView.effectiveTo",
        "WaiverConsentCommandCenterView.status",
        "WaiverConsentCommandCenterView.owner",
        "WaiverConsentCommandCenterView.lastModified"
       ],
       "bindsTo": "WaiverConsentCommandCenterView",
       "operation": "listWaiverConsent",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Each record should display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected waiver consent",
       "bindsTo": "WaiverConsentCommandCenterView",
       "columns": [
        "WaiverConsentCommandCenterView.waiverId",
        "WaiverConsentCommandCenterView.waiverName",
        "WaiverConsentCommandCenterView.type",
        "WaiverConsentCommandCenterView.version",
        "WaiverConsentCommandCenterView.language",
        "WaiverConsentCommandCenterView.associatedProducts",
        "WaiverConsentCommandCenterView.signatoryType",
        "WaiverConsentCommandCenterView.effectiveFrom",
        "WaiverConsentCommandCenterView.effectiveTo",
        "WaiverConsentCommandCenterView.status",
        "WaiverConsentCommandCenterView.owner",
        "WaiverConsentCommandCenterView.lastModified"
       ],
       "notes": null,
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Each record should display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Liability Waiver",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Support configurable classifications"
      },
      {
       "kind": "secondaryButton",
       "label": "Parent/Guardian Consent",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Support configurable classifications"
      },
      {
       "kind": "secondaryButton",
       "label": "Participation Consent",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Support configurable classifications"
      },
      {
       "kind": "secondaryButton",
       "label": "Media Consent",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Support configurable classifications"
      },
      {
       "kind": "secondaryButton",
       "label": "Rental Agreement",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Support configurable classifications"
      },
      {
       "kind": "secondaryButton",
       "label": "Terms Acceptance",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Support configurable classifications"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership Declaration",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Support configurable classifications"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Waiver",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver consent list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the waiver consent untouched.",
   "emptyFirstRun": "No waiver consent yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the waiver consent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiverConsent",
    "contract": "marketing-crm",
    "purpose": "Waiver & Consent Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-041",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-041"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 6. 26 of 31 labels bound to a contract property; 47 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-042",
  "name": "Waiver Template Library & Master Setup",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.2",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/waiver-template-library-master-setup-cms-042",
   "component": "apps/venue-management-web/src/routes/policy/WaiverTemplateLibraryMasterSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-041"
   ],
   "exitTo": [
    "CMS-041"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-041, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-041",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F181 step 2→3",
     "operation": "listWaiverTemplateMaster"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every waiver has a governed master record, owner, classification and intended business scope before publication.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Create the master definition of a waiver or consent form before individual content and questions are configured.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Create New, Duplicate Existing, Create From Approved Corporate Template. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Allow"
   },
   {
    "operation": null,
    "why": "**Waiver Template Library & Master Setup declares no operation that writes anything** — its only declared call is `listWaiverTemplateMaster`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Waiver ID",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Waiver Name",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Internal Description",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Waiver Type",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default Language",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable Country/Jurisdiction",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create New",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate Existing",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Create From Approved Corporate Template",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 8 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver template master configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the waiver template master untouched.",
   "emptyFirstRun": "No waiver template master configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiverTemplateMaster",
    "contract": "marketing-crm",
    "purpose": "Waiver Template Library & Master Setup",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-042",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-042"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 14 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-043",
  "name": "Digital Waiver & Form Builder",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.3",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/digital-waiver-form-builder-cms-043",
   "component": "apps/venue-management-web/src/routes/policy/DigitalWaiverFormBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-041"
   ],
   "exitTo": [
    "CMS-041"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-041, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-041",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F181 step 4→5",
     "operation": "setDigitalWaiverForm"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized administrators can build responsive digital waivers without software development while retaining complete control over mandatory content.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a no-code visual builder for creating the actual customer-facing waiver or digital form.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Information Box, Customer Details, Guardian Details. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 9 §Support configurable blocks"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 9"
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
       "label": "Information Box",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 9 §Support configurable blocks"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Details",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 9 §Support configurable blocks"
      },
      {
       "kind": "secondaryButton",
       "label": "Guardian Details",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 9 §Support configurable blocks"
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
   "loading": "The digital waiver form list.",
   "error": "Could not load. Names which read failed and leaves the digital waiver form untouched.",
   "emptyFirstRun": "No digital waiver form yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital waiver form are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDigitalWaiverForm",
    "contract": "marketing-crm",
    "purpose": "Digital Waiver & Form Builder",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-043",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-043"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 3 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-044",
  "name": "Dynamic Fields, Questions & Conditional Logic",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.4",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/dynamic-fields-questions-conditional-logic-cms-044",
   "component": "apps/venue-management-web/src/routes/policy/DynamicFieldsQuestionsConditionalLogic.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-041"
   ],
   "exitTo": [
    "CMS-041"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-041, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-041",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F181 step 6→7",
     "operation": "listDynamicFieldQuestion"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can create dynamic forms that collect only the information required for the specific participant, product and scenario.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Reusable fields can include; Each field can be; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the information that must be collected from the participant or signatory.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Single Select, Customer Lookup. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Support"
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
       "label": "Participant Name",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Reusable fields can include"
      },
      {
       "kind": "selectField",
       "label": "Date of Birth",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Reusable fields can include"
      },
      {
       "kind": "selectField",
       "label": "Customer ID",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Reusable fields can include"
      },
      {
       "kind": "selectField",
       "label": "Booking Reference",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Reusable fields can include"
      },
      {
       "kind": "selectField",
       "label": "Ticket Number",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Reusable fields can include"
      },
      {
       "kind": "selectField",
       "label": "Guardian Name",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Reusable fields can include"
      },
      {
       "kind": "selectField",
       "label": "Relationship",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Reusable fields can include"
      },
      {
       "kind": "selectField",
       "label": "Emergency Contact",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Reusable fields can include"
      },
      {
       "kind": "selectField",
       "label": "Required",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Each field can be"
      },
      {
       "kind": "selectField",
       "label": "Optional",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Each field can be"
      },
      {
       "kind": "selectField",
       "label": "Conditional",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Each field can be"
      },
      {
       "kind": "selectField",
       "label": "Read Only",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Each field can be"
      },
      {
       "kind": "selectField",
       "label": "Auto-Populated",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Each field can be"
      },
      {
       "kind": "selectField",
       "label": "Minimum/Maximum",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Date range",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Format",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Character limit",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed values",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Single Select",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Lookup",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 11 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic fields questions configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the dynamic fields questions untouched.",
   "emptyFirstRun": "No dynamic fields questions configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicFieldQuestion",
    "contract": "marketing-crm",
    "purpose": "Dynamic Fields, Questions & Conditional Logic",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-044",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-044"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 20 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-045",
  "name": "Signatory, Signature & Guardian Rule Configuration",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.5",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/signatory-signature-guardian-rule-configuration-cms-045",
   "component": "apps/venue-management-web/src/routes/policy/SignatorySignatureGuardianRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-041"
   ],
   "exitTo": [
    "CMS-041"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-041, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-041",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F181 step 8→9",
     "operation": "setSignatorySignatureGuardian"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "before the waiver is considered complete.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; For group bookings, configure whether) and no display directory — it is settings, not a population",
  "purpose": "Define who is legally or operationally required to complete and sign the waiver.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Holder, Rental Customer, Other Authorized Signatory, Customer + Authorized Representative. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Support"
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
       "label": "Signature Required",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Initials Required",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Typed Acceptance",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Checkbox Acceptance",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Digital Signature",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Date/Time",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Signatory Name",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Relationship",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "textField",
       "label": "Identity Verification where required",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "textField",
       "label": "Each participant signs individually",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §For group bookings, configure whether"
      },
      {
       "kind": "textField",
       "label": "Guardian signs for each minor",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §For group bookings, configure whether"
      },
      {
       "kind": "textField",
       "label": "Group leader signs where legally/operationally permitted",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §For group bookings, configure whether"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ticket Holder",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Rental Customer",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Other Authorized Signatory",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer + Authorized Representative",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 13 §Support scenarios requiring"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The signatory signature guardian configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the signatory signature guardian untouched.",
   "emptyFirstRun": "No signatory signature guardian configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSignatorySignatureGuardian",
    "contract": "marketing-crm",
    "purpose": "Signatory, Signature & Guardian Rule Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-045",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-045"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 16 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-046",
  "name": "Product, Event & Experience Association",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.6",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/product-event-experience-association-cms-046",
   "component": "apps/venue-management-web/src/routes/policy/ProductEventExperienceAssociation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-041"
   ],
   "exitTo": [
    "CMS-041"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-041, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-041",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F181 step 10→11",
     "operation": "listProductEventExperience"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every applicable TICVAI product, event or activity can automatically determine which waiver or consent requirements apply.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine which TICVAI products or activities require each waiver.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 9 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Type, Attraction, Activity, Membership, Resource, Package, Venue. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14"
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
       "label": "Product",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket Type",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
      },
      {
       "kind": "secondaryButton",
       "label": "Attraction",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
      },
      {
       "kind": "secondaryButton",
       "label": "Activity",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
      },
      {
       "kind": "secondaryButton",
       "label": "Resource",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
      },
      {
       "kind": "secondaryButton",
       "label": "Package",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
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
   "loading": "The product event experience list.",
   "error": "Could not load. Names which read failed and leaves the product event experience untouched.",
   "emptyFirstRun": "No product event experience yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product event experience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductEventExperience",
    "contract": "marketing-crm",
    "purpose": "Product, Event & Experience Association",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ProductEventExperienceAssociationView.targetType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-046",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-046"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 9 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-047",
  "name": "Waiver Trigger, Eligibility & Completion Rules",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.7",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/waiver-trigger-eligibility-completion-rules-cms-047",
   "component": "apps/venue-management-web/src/routes/policy/WaiverTriggerEligibilityCompletionRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-041"
   ],
   "exitTo": [
    "CMS-041"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-041, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-041",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F181 step 12→13",
     "operation": "listWaiverTriggerEligibility"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Waiver requirements are automatically triggered and enforced according to configurable business rules and participant context.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure whether incomplete status; Configure reminders such as) and no display directory — it is settings, not a population",
  "purpose": "Define when a waiver is required, when it must be completed and what happens if it is not completed.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Immediately",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Before Ticket Release",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "textField",
       "label": "X hours before event",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "textField",
       "label": "X days before visit",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Before arrival",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Before access",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Warns only",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure whether incomplete status"
      },
      {
       "kind": "selectField",
       "label": "Blocks Ticket Download",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure whether incomplete status"
      },
      {
       "kind": "selectField",
       "label": "Blocks Ticket Activation",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure whether incomplete status"
      },
      {
       "kind": "selectField",
       "label": "Blocks Check-In",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure whether incomplete status"
      },
      {
       "kind": "selectField",
       "label": "Blocks Access",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure whether incomplete status"
      },
      {
       "kind": "selectField",
       "label": "Requires Staff Override",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure whether incomplete status"
      },
      {
       "kind": "selectField",
       "label": "T−7 days",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure reminders such as"
      },
      {
       "kind": "selectField",
       "label": "T−3 days",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure reminders such as"
      },
      {
       "kind": "selectField",
       "label": "T−24 hours",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 16 §Configure reminders such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver trigger eligibility configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the waiver trigger eligibility untouched.",
   "emptyFirstRun": "No waiver trigger eligibility configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiverTriggerEligibility",
    "contract": "marketing-crm",
    "purpose": "Waiver Trigger, Eligibility & Completion Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-047",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-047"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 15 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-048",
  "name": "Versioning, Effective Dates & Legal Change Control",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.8",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/versioning-effective-dates-legal-change-control-cms-048",
   "component": "apps/venue-management-web/src/routes/policy/VersioningEffectiveDatesLegalChangeControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-041"
   ],
   "exitTo": [
    "CMS-041"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-041, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-041",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F181 step 14→15",
     "operation": "listVersioningEffectiveDate"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "approved version accepted by the signatory.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Ensure TICVAI maintains a complete historical record of exactly which waiver wording each participant accepted.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Previous Version ↔ New Version. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Allow side-by-side comparison"
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
       "label": "Version Number",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Created By",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Created Date",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Change Reason",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Legal Reviewer",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Effective From",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Effective To",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Previous Version ↔ New Version",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 18 §Allow side-by-side comparison"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The versioning effective dates configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the versioning effective dates untouched.",
   "emptyFirstRun": "No versioning effective dates configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVersioningEffectiveDate",
    "contract": "marketing-crm",
    "purpose": "Versioning, Effective Dates & Legal Change Control",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-048",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-048"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 9 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-049",
  "name": "Localization, Branding & Customer Experience Configuration",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.9",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/localization-branding-customer-experience-configuration-cms-049",
   "component": "apps/venue-management-web/src/routes/policy/LocalizationBrandingCustomerExperienceConfigurat.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-041"
   ],
   "exitTo": [
    "CMS-041"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-041, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-041",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F181 step 16→17",
     "operation": "setLocalizationBrandingCustomer"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Waivers can be delivered as localized, branded and accessible customer experiences without creating separate business logic for each channel.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each version should show) and no metric row",
  "purpose": "Configure how the waiver appears across different brands, languages and customer channels.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Additional languages as configured. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 19 §Support"
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
       "label": "Every localization branding customer",
       "columns": [
        "LocalizationBrandingCustomerExperienceConfigurationView.sourceLanguage",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].translationStatus",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].translatorUserId",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].reviewerUserId",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].approvalStatus",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].lastUpdated"
       ],
       "bindsTo": "LocalizationBrandingCustomerExperienceConfigurationView",
       "operation": "setLocalizationBrandingCustomer",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 19 §Each version should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected localization branding customer",
       "bindsTo": "LocalizationBrandingCustomerExperienceConfigurationView",
       "columns": [
        "LocalizationBrandingCustomerExperienceConfigurationView.sourceLanguage",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].translationStatus",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].translatorUserId",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].reviewerUserId",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].approvalStatus",
        "LocalizationBrandingCustomerExperienceConfigurationView.languages[].lastUpdated"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Preview for”, “Accessibility”.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 19 §Each version should show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Additional languages as configured",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 19 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The localization branding customer list.",
   "error": "Could not load. Names which read failed and leaves the localization branding customer untouched.",
   "emptyFirstRun": "No localization branding customer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the localization branding customer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setLocalizationBrandingCustomer",
    "contract": "marketing-crm",
    "purpose": "Localization, Branding & Customer Experience Configuration",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "LocalizationBrandingCustomerExperienceConfigurationView.sourceLanguage",
    "LocalizationBrandingCustomerExperienceConfigurationView.languages[].translationStatus",
    "LocalizationBrandingCustomerExperienceConfigurationView.languages[].approvalStatus",
    "LocalizationBrandingCustomerExperienceConfigurationView.languages[].lastUpdated"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-049",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-049"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 19. 5 of 5 labels bound to a contract property; 14 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-050",
  "name": "Waiver Approval, Testing & Publication Workspace",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "1",
   "number": "11.1.10",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/waiver-approval-testing-publication-workspace-cms-050",
   "component": "apps/venue-management-web/src/routes/policy/WaiverApprovalTestingPublicationWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-041"
   ],
   "exitTo": [
    "CMS-041"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-041, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "No governed waiver can enter production until its content, rules, associations, signatory requirements and customer journey have been successfully validated and approved. Board 1 — Final Screen Register",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Fields; Configuration experience; Board 1 Configuration Flow) and no display directory — it is settings, not a population",
  "purpose": "Provide the final governance gate before a waiver becomes operational. Board 1 configured what the waiver is, who must sign it, when it applies, and how it is published. Board 2 manages what happens operationally after a waiver requirement is assigned to a booking, ticket, participant, member, rental, group, or activity.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Publish Now, Schedule Publication, Publish to Selected Venues, Publish to Selected Products. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 21 §Support"
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
       "label": "Required fields configured",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 21 §Fields"
      },
      {
       "kind": "selectField",
       "label": "11.1.1",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 21 §Configuration experience"
      },
      {
       "kind": "selectField",
       "label": "0",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 21 §Configuration experience"
      },
      {
       "kind": "textField",
       "label": "→ Approve & Publish",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 21 §Board 1 Configuration Flow"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish Now",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 21 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule Publication",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 21 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish to Selected Venues",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 21 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish to Selected Products",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 21 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver approval testing configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the waiver approval testing untouched.",
   "emptyFirstRun": "No waiver approval testing configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveWaiverTesting",
    "contract": "marketing-crm",
    "purpose": "Waiver Approval, Testing & Publication Workspace",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-050",
   "workshopBoard": "wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-050"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 21. 0 of 0 labels bound to a contract property; 8 of 83 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
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
 "approveWaiverTesting": {
  "method": "PUT",
  "path": "/waiver-testing",
  "contract": "marketing-crm",
  "summary": "Move a waiver version through review, approval and publication",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "WaiverApprovalTestingPublicationWorkspaceInput",
  "responds": "WaiverApprovalTestingPublicationWorkspaceView"
 },
 "listDynamicFieldQuestion": {
  "method": "GET",
  "path": "/dynamic-field-question",
  "contract": "marketing-crm",
  "summary": "Dynamic Fields, Questions & Conditional Logic",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "formId",
    "in": "query",
    "required": true
   },
   {
    "name": "version",
    "in": "query",
    "required": false
   },
   {
    "name": "standardOnly",
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
 "listProductEventExperience": {
  "method": "GET",
  "path": "/product-event-experience",
  "contract": "marketing-crm",
  "summary": "Product, Event & Experience Association",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "targetType",
    "in": "query",
    "required": false
   },
   {
    "name": "targetId",
    "in": "query",
    "required": false
   },
   {
    "name": "requirement",
    "in": "query",
    "required": false
   },
   {
    "name": "includeInherited",
    "in": "query",
    "required": false
   },
   {
    "name": "includeImpact",
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
 "listVersioningEffectiveDate": {
  "method": "GET",
  "path": "/versioning-effective-date",
  "contract": "marketing-crm",
  "summary": "Versioning, Effective Dates & Legal Change Control",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "compareWith",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listWaiverConsent": {
  "method": "GET",
  "path": "/waiver-consent",
  "contract": "marketing-crm",
  "summary": "Waiver & Consent Command Center",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "type",
    "in": "query",
    "required": false
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "language",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "ownerUserId",
    "in": "query",
    "required": false
   },
   {
    "name": "effectiveOn",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringWithinDays",
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
 "listWaiverTemplateMaster": {
  "method": "GET",
  "path": "/waiver-template-master",
  "contract": "marketing-crm",
  "summary": "Waiver Template Library & Master Setup",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "waiverType",
    "in": "query",
    "required": false
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "isMasterTemplate",
    "in": "query",
    "required": false
   },
   {
    "name": "q",
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
 "listWaiverTriggerEligibility": {
  "method": "GET",
  "path": "/waiver-trigger-eligibility",
  "contract": "marketing-crm",
  "summary": "Waiver Trigger, Eligibility & Completion Rules",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "triggerPoint",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "setDigitalWaiverForm": {
  "method": "PUT",
  "path": "/digital-waiver-form",
  "contract": "marketing-crm",
  "summary": "Save the layout of a draft waiver version",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "DigitalWaiverFormBuilderInput",
  "responds": "DigitalWaiverFormBuilderView"
 },
 "setLocalizationBrandingCustomer": {
  "method": "PUT",
  "path": "/localization-branding-customer",
  "contract": "marketing-crm",
  "summary": "Set a waiver version's languages, branding and channels",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "LocalizationBrandingCustomerExperienceConfigurationInput",
  "responds": "LocalizationBrandingCustomerExperienceConfigurationView"
 },
 "setSignatorySignatureGuardian": {
  "method": "PUT",
  "path": "/signatory-signature-guardian",
  "contract": "marketing-crm",
  "summary": "Set who must sign a draft waiver version, and how",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "SignatorySignatureGuardianRuleConfigurationInput",
  "responds": "SignatorySignatureGuardianRuleConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "DigitalWaiverFormBuilderInput": {
  "description": "The request body of `setDigitalWaiverForm`, the layout record itself; read-only properties are ignored.",
  "allOf": [
   {
    "$ref": "#/components/schemas/DigitalWaiverFormBuilderView"
   }
  ]
 },
 "DigitalWaiverFormBuilderView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_form_layout",
  "description": "The layout of one waiver version (pack 11.1.3), keyed on `formId` + `formVersion`. Immutable once the version is published, like the version itself.",
  "required": [
   "formId",
   "formVersion",
   "sections"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "formVersion": {
    "type": "integer",
    "minimum": 1
   },
   "sections": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "sectionKey",
      "kind",
      "blocks"
     ],
     "properties": {
      "sectionKey": {
       "type": "string",
       "maxLength": 60
      },
      "kind": {
       "type": "string",
       "enum": [
        "header",
        "participantInformation",
        "waiverTerms",
        "safetyAcknowledgements",
        "questions",
        "consent",
        "signature",
        "custom"
       ]
      },
      "title": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "numbered": {
       "type": "boolean",
       "default": false
      },
      "mandatoryReading": {
       "type": "boolean",
       "default": false,
       "description": "The signatory must tick \"I have read and understood this section\" before continuing."
      },
      "acknowledgementText": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "showWhen": {
       "type": "object",
       "nullable": true,
       "description": "Shown only when the condition holds, e.g. `isMinor` equals `true` shows the guardian section.",
       "required": [
        "subject",
        "operator"
       ],
       "properties": {
        "subject": {
         "type": "string",
         "maxLength": 60,
         "description": "A field key of this version, or `isMinor` (resolved from the waiver's guardian threshold)."
        },
        "operator": {
         "type": "string",
         "enum": [
          "equals",
          "notEquals",
          "in",
          "lessThan",
          "greaterThan",
          "isAnswered"
         ]
        },
        "value": {
         "type": "string",
         "maxLength": 200,
         "nullable": true
        }
       }
      },
      "blocks": {
       "type": "array",
       "items": {
        "type": "object",
        "required": [
         "blockKey",
         "kind"
        ],
        "properties": {
         "blockKey": {
          "type": "string",
          "maxLength": 60
         },
         "kind": {
          "type": "string",
          "enum": [
           "heading",
           "paragraph",
           "legalText",
           "instructions",
           "imageLogo",
           "divider",
           "informationBox",
           "checkbox",
           "acknowledgement",
           "question",
           "signature",
           "initials",
           "date",
           "customerDetails",
           "guardianDetails"
          ]
         },
         "content": {
          "$ref": "#/components/schemas/LocalisedText"
         },
         "assetId": {
          "type": "string",
          "format": "uuid",
          "nullable": true,
          "description": "The image for an `imageLogo` block."
         },
         "fieldKey": {
          "type": "string",
          "maxLength": 60,
          "nullable": true,
          "description": "The `FormField.key` an input block collects; required for input kinds."
         },
         "mandatoryNotice": {
          "type": "boolean",
          "default": false,
          "description": "Rendered as a notice that cannot be collapsed."
         }
        }
       }
      }
     }
    }
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "draft",
     "published",
     "superseded",
     "retired"
    ],
    "description": "`FormDefinition.status` of this version."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "DynamicFieldsQuestionsConditionalLogicView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.form_definition_field + marketing.waiver_field_rule",
  "description": "One field of a waiver version (pack 11.1.4). `fieldType` is the builder's type; the stored `FormField.type` follows from it (shortText text, longText and address longText, yesNo and checkbox boolean, singleSelect and dropdown select, multiSelect multiSelect, mobile phone, the lookups text holding the record id, signature and initials signature).",
  "required": [
   "formId",
   "formVersion",
   "key",
   "label",
   "fieldType",
   "requirement"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "formVersion": {
    "type": "integer",
    "minimum": 1
   },
   "key": {
    "type": "string",
    "maxLength": 60,
    "pattern": "^[a-zA-Z][a-zA-Z0-9_]*$"
   },
   "label": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "helpText": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "fieldType": {
    "type": "string",
    "enum": [
     "shortText",
     "longText",
     "number",
     "date",
     "yesNo",
     "checkbox",
     "singleSelect",
     "multiSelect",
     "dropdown",
     "email",
     "mobile",
     "address",
     "customerLookup",
     "participantLookup",
     "signature",
     "initials"
    ]
   },
   "standardField": {
    "type": "string",
    "nullable": true,
    "enum": [
     "participantName",
     "dateOfBirth",
     "customerId",
     "bookingReference",
     "ticketNumber",
     "guardianName",
     "guardianRelationship",
     "emergencyContact"
    ],
    "description": "Set when the field is one of the reusable standard fields."
   },
   "requirement": {
    "type": "string",
    "enum": [
     "required",
     "optional",
     "conditional",
     "readOnly",
     "autoPopulated"
    ],
    "description": "`conditional` needs `conditions`; `autoPopulated` and `readOnly` need `mapsTo`."
   },
   "options": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "value"
     ],
     "properties": {
      "value": {
       "type": "string",
       "maxLength": 100
      },
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      }
     }
    },
    "description": "The allowed values of a select, dropdown or multi-select field."
   },
   "validation": {
    "type": "object",
    "nullable": true,
    "properties": {
     "minimum": {
      "type": "number",
      "nullable": true
     },
     "maximum": {
      "type": "number",
      "nullable": true
     },
     "dateFrom": {
      "type": "string",
      "format": "date",
      "nullable": true
     },
     "dateTo": {
      "type": "string",
      "format": "date",
      "nullable": true
     },
     "pattern": {
      "type": "string",
      "maxLength": 200,
      "nullable": true,
      "description": "The required format, as a regular expression."
     },
     "maxLength": {
      "type": "integer",
      "minimum": 1,
      "nullable": true,
      "description": "The character limit."
     }
    }
   },
   "conditions": {
    "type": "array",
    "description": "All must hold (AND). For `conditional` fields they decide whether the field is shown and required.",
    "items": {
     "type": "object",
     "required": [
      "subject",
      "operator"
     ],
     "properties": {
      "subject": {
       "type": "string",
       "maxLength": 60,
       "description": "Another field's key, or `isMinor`."
      },
      "operator": {
       "type": "string",
       "enum": [
        "equals",
        "notEquals",
        "in",
        "lessThan",
        "greaterThan",
        "isAnswered"
       ]
      },
      "value": {
       "type": "string",
       "maxLength": 200,
       "nullable": true
      }
     }
    }
   },
   "mapsTo": {
    "type": "string",
    "nullable": true,
    "enum": [
     "guestName",
     "guestDateOfBirth",
     "guestEmail",
     "guestMobile",
     "guestAddress",
     "guestId",
     "ticketHolderName",
     "orderReference",
     "ticketNumber"
    ],
    "description": "The existing TICVAI record the field reads from, where the caller may read it."
   },
   "isPersonalData": {
    "type": "boolean",
    "default": false
   },
   "sortOrder": {
    "type": "integer",
    "minimum": 0,
    "default": 0
   },
   "deleted": {
    "type": "boolean",
    "writeOnly": true,
    "default": false,
    "description": "True removes the field from the draft version."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LocalizationBrandingCustomerExperienceConfigurationInput": {
  "description": "The request body of `setLocalizationBrandingCustomer`, the record itself; read-only properties are ignored.",
  "allOf": [
   {
    "$ref": "#/components/schemas/LocalizationBrandingCustomerExperienceConfigurationView"
   }
  ]
 },
 "LocalizationBrandingCustomerExperienceConfigurationView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_localisation",
  "description": "Languages, branding and channels of one waiver version (pack 11.1.9), keyed on `formId` + `formVersion`.",
  "required": [
   "formId",
   "formVersion",
   "sourceLanguage",
   "languages"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "formVersion": {
    "type": "integer",
    "minimum": 1
   },
   "sourceLanguage": {
    "type": "string",
    "maxLength": 10,
    "description": "The language the legal text is written and reviewed in."
   },
   "languages": {
    "type": "array",
    "minItems": 1,
    "description": "Every language the version is offered in, the source language included. Arabic renders right to left.",
    "items": {
     "type": "object",
     "required": [
      "language",
      "required",
      "translationStatus",
      "approvalStatus"
     ],
     "properties": {
      "language": {
       "type": "string",
       "maxLength": 10
      },
      "required": {
       "type": "boolean",
       "description": "Publication waits for this language's approval."
      },
      "translationStatus": {
       "type": "string",
       "enum": [
        "notStarted",
        "aiDrafted",
        "inTranslation",
        "inReview",
        "complete"
       ]
      },
      "translatorUserId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "reviewerUserId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "approvalStatus": {
       "type": "string",
       "enum": [
        "pending",
        "approved",
        "rejected"
       ]
      },
      "lastUpdated": {
       "type": "string",
       "format": "date-time",
       "readOnly": true
      }
     }
    }
   },
   "branding": {
    "type": "object",
    "properties": {
     "brandLogoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "venueLogoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "themeId": {
      "type": "string",
      "nullable": true,
      "description": "The white-label theme it takes colours and typography from."
     },
     "header": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "footer": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "customerInstructions": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "confirmationMessage": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "supportEmail": {
      "type": "string",
      "format": "email",
      "nullable": true
     },
     "supportPhone": {
      "type": "string",
      "maxLength": 30,
      "nullable": true
     }
    }
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2cWeb",
      "mobileApp",
      "emailLink",
      "qrLink",
      "kiosk",
      "posFrontDesk",
      "groupPortal"
     ]
    },
    "description": "Where the waiver is offered; every channel renders the same version and rules."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
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
 "ProductEventExperienceAssociationView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_association",
  "description": "One waiver attached to one target (pack 11.1.6). The waiver's in-force version applies; the version a guest signed is on their signature.",
  "required": [
   "formId",
   "targetType",
   "requirement",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "formId": {
    "type": "string",
    "format": "uuid",
    "description": "The waiver (`FormDefinition.id`)."
   },
   "waiverName": {
    "type": "string",
    "readOnly": true
   },
   "targetType": {
    "type": "string",
    "enum": [
     "global",
     "brand",
     "venue",
     "product",
     "ticketType",
     "event",
     "performance",
     "attraction",
     "activity",
     "membership",
     "camp",
     "rental",
     "resource",
     "package",
     "addOn"
    ]
   },
   "targetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The catalogue, event, venue or brand id; null only for `global`."
   },
   "targetName": {
    "type": "string",
    "readOnly": true
   },
   "requirement": {
    "type": "string",
    "enum": [
     "mandatory",
     "optional",
     "conditional",
     "informational"
    ]
   },
   "conditionRuleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The eligibility rule (`setWaiverTriggerRule`) that makes a conditional association apply."
   },
   "sequence": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "The order the target's waivers are presented in."
   },
   "overridesAssociationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The inherited association this one replaces for this target."
   },
   "inheritedFrom": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "properties": {
     "associationId": {
      "type": "string",
      "format": "uuid"
     },
     "targetType": {
      "type": "string"
     },
     "targetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "removed"
    ],
    "default": "active"
   },
   "impact": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "What depends on this association now (pack Dependency Impact).",
    "properties": {
     "products": {
      "type": "integer",
      "minimum": 0
     },
     "futureBookings": {
      "type": "integer",
      "minimum": 0
     },
     "tickets": {
      "type": "integer",
      "minimum": 0
     },
     "participants": {
      "type": "integer",
      "minimum": 0
     },
     "events": {
      "type": "integer",
      "minimum": 0
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "SignatorySignatureGuardianRuleConfigurationInput": {
  "description": "The request body of `setSignatorySignatureGuardian`, the rule record itself; read-only properties are ignored.",
  "allOf": [
   {
    "$ref": "#/components/schemas/SignatorySignatureGuardianRuleConfigurationView"
   }
  ]
 },
 "SignatorySignatureGuardianRuleConfigurationView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_signatory_rule",
  "description": "The signatory rules of one waiver version (pack 11.1.5), keyed on `formId` + `formVersion`; immutable once the version is published.",
  "required": [
   "formId",
   "formVersion",
   "primarySignatory",
   "acceptanceMethod",
   "requiresGuardianForMinors"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "formVersion": {
    "type": "integer",
    "minimum": 1
   },
   "primarySignatory": {
    "type": "string",
    "enum": [
     "ticketHolder",
     "purchaser",
     "participant",
     "parent",
     "legalGuardian",
     "groupLeader",
     "corporateRepresentative",
     "member",
     "rentalCustomer",
     "otherAuthorizedSignatory"
    ]
   },
   "allowedSignatories": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "ticketHolder",
      "purchaser",
      "participant",
      "parent",
      "legalGuardian",
      "groupLeader",
      "corporateRepresentative",
      "member",
      "rentalCustomer",
      "otherAuthorizedSignatory"
     ]
    },
    "description": "Who else may sign in the primary signatory's place."
   },
   "coSignature": {
    "type": "string",
    "nullable": true,
    "enum": [
     "participantAndGuardian",
     "customerAndAuthorizedRepresentative"
    ],
    "description": "Set when two people must both sign."
   },
   "signatureRequired": {
    "type": "boolean",
    "default": true
   },
   "initialsRequired": {
    "type": "boolean",
    "default": false
   },
   "acceptanceMethod": {
    "type": "string",
    "enum": [
     "drawnSignature",
     "typedName",
     "checkbox"
    ],
    "description": "Kept equal to `FormDefinition.signatureKind` (drawn, typed, checkbox)."
   },
   "captureRelationship": {
    "type": "boolean",
    "default": true,
    "description": "Whoever signs for someone else states their relationship."
   },
   "identityVerification": {
    "type": "string",
    "enum": [
     "none",
     "signedInAccount",
     "oneTimeCode",
     "idDocumentCheck"
    ],
    "default": "none"
   },
   "requiresGuardianForMinors": {
    "type": "boolean",
    "description": "Written to `FormDefinition.requiresGuardianForMinors`."
   },
   "guardianThresholdAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 25,
    "nullable": true,
    "description": "A participant under this age needs a guardian. Written to `FormDefinition.minimumAge`. No default."
   },
   "guardianThresholdByCountry": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "country",
      "age"
     ],
     "properties": {
      "country": {
       "type": "string",
       "pattern": "^[A-Z]{2}$"
      },
      "age": {
       "type": "integer",
       "minimum": 1,
       "maximum": 25
      }
     }
    },
    "description": "Per-country thresholds that override `guardianThresholdAge`."
   },
   "guardianSignsForEachMinor": {
    "type": "boolean",
    "default": true,
    "description": "One guardian signature per minor, never one for the family."
   },
   "groupSigningModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "eachParticipantIndividually",
      "guardianForEachMinor",
      "groupLeaderForGroup",
      "organisationRepresentativeDeclaration"
     ]
    },
    "description": "The modes a group booking may use. Empty means each participant signs individually."
   },
   "recordedEvidence": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "string",
     "enum": [
      "timestamp",
      "waiverVersion",
      "signatory",
      "authenticationMethod",
      "transactionReference",
      "customerReference",
      "documentHash",
      "deviceInfo",
      "consentEvidence"
     ]
    },
    "description": "Always all of them; listed so the reviewer sees what is kept."
   },
   "legalApprovedBy": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "`FormDefinition.legalReviewedBy`, set at the legal/compliance step of `approveWaiverTesting`."
   },
   "legalApprovedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "VersioningEffectiveDatesLegalChangeControlView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.form_definition, marketing.waiver_version_control (new), marketing.form_submission and marketing.waiver_signature",
  "description": "One version of one waiver and its change control (pack 11.1.8).",
  "required": [
   "formId",
   "versionNumber",
   "status",
   "createdAt"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "waiverName": {
    "type": "string"
   },
   "versionNumber": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "superseded",
     "retired"
    ],
    "description": "`FormDefinition.status` (states/form-definition.yaml)."
   },
   "lifecycleStatus": {
    "type": "string",
    "enum": [
     "draft",
     "review",
     "pendingApproval",
     "approved",
     "scheduled",
     "published",
     "suspended",
     "expired",
     "archived"
    ]
   },
   "createdByUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "changeReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "legalReviewer": {
    "type": "string",
    "nullable": true,
    "description": "`FormDefinition.legalReviewedBy`."
   },
   "legalReviewedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "approvedByUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
   "resignRule": {
    "type": "string",
    "enum": [
     "noResign",
     "resignAtNextBooking",
     "resignBeforeNextVisit"
    ],
    "description": "Whether people who signed an earlier version must sign this one."
   },
   "suspended": {
    "type": "boolean",
    "default": false
   },
   "suspensionReason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "signatureCount": {
    "type": "integer",
    "minimum": 0,
    "description": "Signatures taken against this exact version."
   },
   "comparison": {
    "type": "object",
    "nullable": true,
    "description": "Present when `compareWith` is given.",
    "properties": {
     "comparedWithVersion": {
      "type": "integer",
      "minimum": 1
     },
     "addedText": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "blockKey": {
         "type": "string"
        },
        "language": {
         "type": "string"
        },
        "text": {
         "type": "string"
        }
       }
      }
     },
     "removedText": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "blockKey": {
         "type": "string"
        },
        "language": {
         "type": "string"
        },
        "text": {
         "type": "string"
        }
       }
      }
     },
     "changedQuestions": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Field keys added, removed or changed."
     },
     "changedSignatoryRules": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Names of the signatory-rule properties that differ."
     },
     "changedAssociations": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      },
      "description": "Associations added, removed or changed between the two versions' publication."
     }
    }
   }
  }
 },
 "WaiverApprovalTestingPublicationWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request; appended to marketing.waiver_version_control",
  "description": "One governance action on a waiver version (pack 11.1.10).",
  "required": [
   "formId",
   "formVersion",
   "action"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "formVersion": {
    "type": "integer",
    "minimum": 1
   },
   "action": {
    "type": "string",
    "enum": [
     "submitForReview",
     "completeOperationsReview",
     "completeLegalReview",
     "approve",
     "reject",
     "publish",
     "suspend",
     "reinstate",
     "archive"
    ]
   },
   "comment": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true,
    "description": "Required for `reject` and `suspend`."
   },
   "changeReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true,
    "description": "Required for `submitForReview`."
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
   "resignRule": {
    "type": "string",
    "enum": [
     "noResign",
     "resignAtNextBooking",
     "resignBeforeNextVisit"
    ],
    "description": "Required for `submitForReview` of a version after the first."
   },
   "publication": {
    "type": "object",
    "nullable": true,
    "description": "Required for `publish`.",
    "required": [
     "mode"
    ],
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "publishNow",
       "schedule",
       "selectedVenues",
       "selectedProducts",
       "controlledRollout"
      ]
     },
     "publishAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "Required for `schedule`."
     },
     "venueIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "productIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   }
  }
 },
 "WaiverApprovalTestingPublicationWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_version_control",
  "description": "The governance record of one waiver version with its checklist (pack 11.1.10), keyed on `formId` + `formVersion`.",
  "required": [
   "formId",
   "formVersion",
   "lifecycleStatus",
   "checklist"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "formVersion": {
    "type": "integer",
    "minimum": 1
   },
   "lifecycleStatus": {
    "type": "string",
    "enum": [
     "draft",
     "review",
     "pendingApproval",
     "approved",
     "scheduled",
     "published",
     "suspended",
     "expired",
     "archived"
    ]
   },
   "checklist": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "check",
      "passed",
      "severity"
     ],
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "masterRecordComplete",
        "requiredLegalTextPresent",
        "requiredFieldsConfigured",
        "conditionalRulesValid",
        "signatureRulesConfigured",
        "guardianThresholdSet",
        "guardianSignatureFieldPresent",
        "productsEventsAssigned",
        "completionRulesConfigured",
        "requiredTranslationsApproved",
        "effectiveDatesValid"
       ]
      },
      "passed": {
       "type": "boolean"
      },
      "severity": {
       "type": "string",
       "enum": [
        "critical",
        "warning"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "simulation": {
    "type": "object",
    "nullable": true,
    "description": "Present when scenario parameters were given.",
    "properties": {
     "requiredWaivers": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "formId": {
         "type": "string",
         "format": "uuid"
        },
        "waiverName": {
         "type": "string"
        },
        "version": {
         "type": "integer"
        },
        "requirement": {
         "type": "string",
         "enum": [
          "mandatory",
          "optional",
          "conditional",
          "informational"
         ]
        },
        "applies": {
         "type": "boolean"
        },
        "signatories": {
         "type": "array",
         "items": {
          "type": "string"
         },
         "description": "e.g. participant, legalGuardian."
        }
       }
      }
     },
     "blockedAt": {
      "type": "array",
      "items": {
       "type": "string",
       "enum": [
        "ticketDownload",
        "ticketActivation",
        "checkIn",
        "access"
       ]
      },
      "description": "What a missing signature would block, when `missingSignature` was set."
     }
    }
   },
   "aiFindings": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "severity": {
       "type": "string",
       "enum": [
        "info",
        "warning"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "changeReason": {
    "type": "string",
    "nullable": true
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
   "resignRule": {
    "type": "string",
    "nullable": true,
    "enum": [
     "noResign",
     "resignAtNextBooking",
     "resignBeforeNextVisit"
    ]
   },
   "publication": {
    "type": "object",
    "nullable": true,
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "publishNow",
       "schedule",
       "selectedVenues",
       "selectedProducts",
       "controlledRollout"
      ]
     },
     "publishAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "venueIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "productIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "suspended": {
    "type": "boolean",
    "default": false
   },
   "suspensionReason": {
    "type": "string",
    "nullable": true
   },
   "audit": {
    "type": "object",
    "description": "Who moved it through each stage, and when (pack Audit).",
    "properties": {
     "submittedByUserId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "submittedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "operationsReviewedByUserId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "operationsReviewedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "legalReviewedByUserId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "legalReviewedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "approvedByUserId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "approvedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "publishedByUserId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "publishedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   },
   "history": {
    "type": "array",
    "description": "Every action with its comment, oldest first.",
    "items": {
     "type": "object",
     "properties": {
      "action": {
       "type": "string"
      },
      "byUserId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "comment": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "WaiverConsentCommandCenterView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.form_definition (kind waiver), marketing.waiver_master (new), marketing.waiver_version_control (new) and marketing.waiver_association (new)",
  "description": "One row of the waiver directory (pack 11.1.1), a waiver at its latest version. `status` is the pack's lifecycle, derived from `FormDefinition.status` and the version-control record (draft, review, pendingApproval, approved and scheduled are a `draft` form version at that approval stage; suspended is a published version under an emergency suspension; expired is a version past `effectiveTo`; archived is `retired`).",
  "required": [
   "waiverId",
   "waiverName",
   "type",
   "version",
   "status",
   "lastModified"
  ],
  "properties": {
   "waiverId": {
    "type": "string",
    "format": "uuid",
    "description": "The `FormDefinition.id`."
   },
   "waiverName": {
    "type": "string"
   },
   "type": {
    "type": "string",
    "enum": [
     "liabilityWaiver",
     "parentGuardianConsent",
     "participationConsent",
     "medicalDeclaration",
     "safetyAcknowledgement",
     "mediaConsent",
     "rentalAgreement",
     "termsAcceptance",
     "membershipDeclaration",
     "customForm"
    ]
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "description": "The latest version, whatever its state."
   },
   "publishedVersion": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "The version guests currently sign, when that is not the latest."
   },
   "language": {
    "type": "string",
    "maxLength": 10,
    "description": "The default language from the master record."
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 10
    },
    "description": "Every language the version is published in."
   },
   "associatedProducts": {
    "type": "integer",
    "minimum": 0,
    "description": "Products with an active association (the pack's usage indicator)."
   },
   "associatedVenues": {
    "type": "integer",
    "minimum": 0
   },
   "signatoryType": {
    "type": "string",
    "nullable": true,
    "enum": [
     "ticketHolder",
     "purchaser",
     "participant",
     "parent",
     "legalGuardian",
     "groupLeader",
     "corporateRepresentative",
     "member",
     "rentalCustomer",
     "otherAuthorizedSignatory"
    ],
    "description": "The primary signatory from `setSignatorySignatureGuardian`."
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
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "review",
     "pendingApproval",
     "approved",
     "scheduled",
     "published",
     "suspended",
     "expired",
     "archived"
    ]
   },
   "ownerUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "owner": {
    "type": "string",
    "nullable": true,
    "description": "The owner's display name."
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "lastModified": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WaiverTemplateLibraryMasterSetupView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_master",
  "description": "The master record of one waiver (pack 11.1.2), one per `FormDefinition` of kind `waiver`. The name, wording, fields and versions live on the form; this holds classification, ownership and business scope.",
  "required": [
   "waiverId",
   "waiverType",
   "ownerUserId",
   "businessOwnerUserId",
   "defaultLanguage",
   "templateSource"
  ],
  "properties": {
   "waiverId": {
    "type": "string",
    "format": "uuid",
    "description": "The `FormDefinition.id`; the natural key."
   },
   "waiverName": {
    "type": "string",
    "readOnly": true,
    "description": "`FormDefinition.name`, shown here, written by `createForm`."
   },
   "internalDescription": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true
   },
   "waiverType": {
    "type": "string",
    "enum": [
     "liabilityWaiver",
     "parentGuardianConsent",
     "participationConsent",
     "medicalDeclaration",
     "safetyAcknowledgement",
     "mediaConsent",
     "rentalAgreement",
     "termsAcceptance",
     "membershipDeclaration",
     "customForm"
    ]
   },
   "customTypeLabel": {
    "type": "string",
    "maxLength": 80,
    "nullable": true,
    "description": "The tenant's own classification name; required when `waiverType` is `customForm`."
   },
   "ownerUserId": {
    "type": "string",
    "format": "uuid"
   },
   "department": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for a corporate waiver every brand may use."
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The finance legal entity the waiver is given in favour of."
   },
   "defaultLanguage": {
    "type": "string",
    "maxLength": 10
   },
   "applicableCountries": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{2}$"
    },
    "description": "ISO 3166-1 alpha-2. Empty means the waiver is not yet scoped, which blocks publication."
   },
   "applicableJurisdiction": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "A sub-national jurisdiction where the law differs within a country."
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "draft",
     "review",
     "pendingApproval",
     "approved",
     "scheduled",
     "published",
     "suspended",
     "expired",
     "archived"
    ],
    "description": "The lifecycle status of the latest version (see `listWaiverConsent`)."
   },
   "templateSource": {
    "type": "string",
    "enum": [
     "createNew",
     "duplicateExisting",
     "masterTemplate",
     "corporateTemplate"
    ],
    "default": "createNew"
   },
   "sourceWaiverId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The waiver it was duplicated or created from; required unless `createNew`."
   },
   "sourceVersion": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "isMasterTemplate": {
    "type": "boolean",
    "default": false,
    "description": "Offered in the reusable library. A corporate template is a master template with no `brandId`."
   },
   "businessOwnerUserId": {
    "type": "string",
    "format": "uuid"
   },
   "legalReviewerUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "complianceOwnerUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "operationalOwnerUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalReviewRequired": {
    "type": "boolean",
    "default": true,
    "description": "Whether the approval chain includes the legal/compliance step. On unless the tenant turns it off."
   },
   "usage": {
    "type": "object",
    "readOnly": true,
    "description": "Where the waiver is used now (pack Usage Indicator, Template Dependency).",
    "properties": {
     "products": {
      "type": "integer",
      "minimum": 0
     },
     "venues": {
      "type": "integer",
      "minimum": 0
     },
     "futureBookings": {
      "type": "integer",
      "minimum": 0
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "WaiverTriggerEligibilityCompletionRulesView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_trigger_rule",
  "description": "One trigger, eligibility and completion rule of a waiver (pack 11.1.7).",
  "required": [
   "formId",
   "name",
   "triggerPoint",
   "completionDeadline",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Absent on create."
   },
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "triggerPoint": {
    "type": "string",
    "enum": [
     "duringCheckout",
     "afterPurchase",
     "beforeTicketIssuance",
     "beforeTicketDownload",
     "beforeEvent",
     "beforeCheckIn",
     "beforeAccess",
     "beforeEquipmentCollection",
     "beforeMembershipActivation",
     "beforeActivityStart"
    ]
   },
   "eligibility": {
    "type": "array",
    "description": "All must hold (AND). Empty means every participant the association reaches.",
    "items": {
     "type": "object",
     "required": [
      "attribute",
      "operator",
      "values"
     ],
     "properties": {
      "attribute": {
       "type": "string",
       "enum": [
        "age",
        "isMinor",
        "product",
        "event",
        "venue",
        "activity",
        "customerType",
        "membership",
        "country",
        "channel",
        "participantType",
        "bookingType"
       ]
      },
      "operator": {
       "type": "string",
       "enum": [
        "equals",
        "notEquals",
        "in",
        "notIn",
        "lessThan",
        "greaterThan"
       ]
      },
      "values": {
       "type": "array",
       "minItems": 1,
       "items": {
        "type": "string",
        "maxLength": 100
       }
      }
     }
    }
   },
   "completionDeadline": {
    "type": "object",
    "required": [
     "kind"
    ],
    "properties": {
     "kind": {
      "type": "string",
      "enum": [
       "immediately",
       "beforeTicketRelease",
       "hoursBeforeEvent",
       "daysBeforeVisit",
       "beforeArrival",
       "beforeAccess"
      ]
     },
     "offset": {
      "type": "integer",
      "minimum": 1,
      "nullable": true,
      "description": "Hours for `hoursBeforeEvent`, days for `daysBeforeVisit`."
     }
    }
   },
   "enforcement": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "blockTicketDownload",
      "blockTicketActivation",
      "blockCheckIn",
      "blockAccess"
     ]
    },
    "description": "What an incomplete waiver blocks. Empty means warn only."
   },
   "allowStaffOverride": {
    "type": "boolean",
    "default": false,
    "description": "An authorised operator may admit the participant anyway; the override is recorded."
   },
   "reminders": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "offsetHours",
      "channels"
     ],
     "properties": {
      "offsetHours": {
       "type": "integer",
       "minimum": 1,
       "description": "Hours before the deadline, e.g. 168, 72, 24."
      },
      "channels": {
       "type": "array",
       "minItems": 1,
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      }
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "inactive"
    ],
    "default": "active"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 }
}
```
