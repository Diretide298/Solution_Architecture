# WS72 — Waiver, Consent & Digital Form Management board 1

**10 screens · 10 operations · 14 schemas · 2 permissions**

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
  `MARKETING_MANAGE, MARKETING_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
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

**CMS-043, CMS-046, CMS-049 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should display) — counts over a population, then the population",
  "purpose": "Provide administrators with a centralized workspace for managing every waiver, consent form and digital declaration configured across TICVAI.",
  "purposeNote": "Authorized administrators can locate, manage and understand the lifecycle and usage of every waiver or consent form from one central workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 14 actions on this screen and the screen declares 1 operation.** Unserved: Liability Waiver, Parent/Guardian Consent, Participation Consent, Media Consent, Membership Declaration, Create Waiver, Duplicate, Create New Version …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "bindsTo": "WaiverConsentCommandCenterView.totalTemplates"
      },
      {
       "kind": "metricTile",
       "label": "Published",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.published"
      },
      {
       "kind": "metricTile",
       "label": "Draft",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.draft"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.scheduled"
      },
      {
       "kind": "metricTile",
       "label": "Expiring",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.expiring"
      },
      {
       "kind": "metricTile",
       "label": "Archived",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.archived"
      },
      {
       "kind": "metricTile",
       "label": "Products Requiring Waiver",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.productsRequiringWaiver"
      },
      {
       "kind": "metricTile",
       "label": "Active Waiver Versions",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.activeWaiverVersions"
      },
      {
       "kind": "metricTile",
       "label": "Waivers Requiring Review",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Display",
       "bindsTo": "WaiverConsentCommandCenterView.waiversRequiringReview"
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
       "label": "Membership Declaration",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Support configurable classifications"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Waiver",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 6 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create New Version",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-041"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 6. 26 of 31 labels bound to a contract property; 45 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Create the master definition of a waiver or consent form before individual content and questions are configured.",
  "purposeNote": "Every waiver has a governed master record, owner, classification and intended business scope before publication.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-042"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a no-code visual builder for creating the actual customer-facing waiver or digital form.",
  "purposeNote": "Authorized administrators can build responsive digital waivers without software development while retaining complete control over mandatory content.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Information Box, Customer Details. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
    "trigger": "onAction",
    "invalidates": [
     "setDigitalWaiverForm"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-043"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 2 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Reusable fields can include; Each field can be; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the information that must be collected from the participant or signatory.",
  "purposeNote": "Administrators can create dynamic forms that collect only the information required for the specific participant, product and scenario.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Customer Lookup. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-044"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 19 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; For group bookings, configure whether) and no display directory — it is settings, not a population",
  "purpose": "Define who is legally or operationally required to complete and sign the waiver.",
  "purposeNote": "before the waiver is considered complete.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Holder, Rental Customer, Customer + Authorized Representative. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
    "trigger": "onAction",
    "invalidates": [
     "setSignatorySignatureGuardian"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-045"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 15 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine which TICVAI products or activities require each waiver.",
  "purposeNote": "Every applicable TICVAI product, event or activity can automatically determine which waiver or consent requirements apply.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Type, Membership. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Ticket Type",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 14 §Allow association with"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership",
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
    "ProductEventExperienceAssociationView.product",
    "ProductEventExperienceAssociationView.ticketType",
    "ProductEventExperienceAssociationView.event",
    "ProductEventExperienceAssociationView.performance",
    "ProductEventExperienceAssociationView.attraction"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-046"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 2 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure whether incomplete status; Configure reminders such as) and no display directory — it is settings, not a population",
  "purpose": "Define when a waiver is required, when it must be completed and what happens if it is not completed.",
  "purposeNote": "Waiver requirements are automatically triggered and enforced according to configurable business rules and participant context.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-047"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Ensure TICVAI maintains a complete historical record of exactly which waiver wording each participant accepted.",
  "purposeNote": "approved version accepted by the signatory.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-048"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 8 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each version should show) and no metric row",
  "purpose": "Configure how the waiver appears across different brands, languages and customer channels.",
  "purposeNote": "Waivers can be delivered as localized, branded and accessible customer experiences without creating separate business logic for each channel.",
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
        "LocalizationBrandingCustomerExperienceConfigurationView.translationStatus",
        "LocalizationBrandingCustomerExperienceConfigurationView.translatorReviewer",
        "LocalizationBrandingCustomerExperienceConfigurationView.approvalStatus",
        "LocalizationBrandingCustomerExperienceConfigurationView.lastUpdated"
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
        "LocalizationBrandingCustomerExperienceConfigurationView.translationStatus",
        "LocalizationBrandingCustomerExperienceConfigurationView.translatorReviewer",
        "LocalizationBrandingCustomerExperienceConfigurationView.approvalStatus",
        "LocalizationBrandingCustomerExperienceConfigurationView.lastUpdated"
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
    "trigger": "onAction",
    "invalidates": [
     "setLocalizationBrandingCustomer"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "LocalizationBrandingCustomerExperienceConfigurationView.sourceLanguage",
    "LocalizationBrandingCustomerExperienceConfigurationView.translationStatus",
    "LocalizationBrandingCustomerExperienceConfigurationView.translatorReviewer",
    "LocalizationBrandingCustomerExperienceConfigurationView.approvalStatus",
    "LocalizationBrandingCustomerExperienceConfigurationView.lastUpdated"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-049"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Fields; Configuration experience; Board 1 Configuration Flow) and no display directory — it is settings, not a population",
  "purpose": "Provide the final governance gate before a waiver becomes operational. Board 1 configured what the waiver is, who must sign it, when it applies, and how it is published. Board 2 manages what happens operationally after a waiver requirement is assigned to a booking, ticket, participant, member, rental, group, or activity.",
  "purposeNote": "No governed waiver can enter production until its content, rules, associations, signatory requirements and customer journey have been successfully validated and approved. Board 1 — Final Screen Register",
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
    "trigger": "onAction",
    "invalidates": [
     "approveWaiverTesting"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-050"
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
  "summary": "Waiver Approval, Testing & Publication Workspace",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "WaiverApprovalTestingPublicationWorkspaceInput",
  "responds": "WaiverApprovalTestingPublicationWorkspaceView"
 },
 "listDynamicFieldQuestion": {
  "method": "GET",
  "path": "/dynamic-field-question",
  "contract": "marketing-crm",
  "summary": "Dynamic Fields, Questions & Conditional Logic",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicFieldsQuestionsConditionalLogicView"
 },
 "listProductEventExperience": {
  "method": "GET",
  "path": "/product-event-experience",
  "contract": "marketing-crm",
  "summary": "Product, Event & Experience Association",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProductEventExperienceAssociationView"
 },
 "listVersioningEffectiveDate": {
  "method": "GET",
  "path": "/versioning-effective-date",
  "contract": "marketing-crm",
  "summary": "Versioning, Effective Dates & Legal Change Control",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VersioningEffectiveDatesLegalChangeControlView"
 },
 "listWaiverConsent": {
  "method": "GET",
  "path": "/waiver-consent",
  "contract": "marketing-crm",
  "summary": "Waiver & Consent Command Center",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "effectiveDate",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WaiverConsentCommandCenterView"
 },
 "listWaiverTemplateMaster": {
  "method": "GET",
  "path": "/waiver-template-master",
  "contract": "marketing-crm",
  "summary": "Waiver Template Library & Master Setup",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WaiverTemplateLibraryMasterSetupView"
 },
 "listWaiverTriggerEligibility": {
  "method": "GET",
  "path": "/waiver-trigger-eligibility",
  "contract": "marketing-crm",
  "summary": "Waiver Trigger, Eligibility & Completion Rules",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WaiverTriggerEligibilityCompletionRulesView"
 },
 "setDigitalWaiverForm": {
  "method": "PUT",
  "path": "/digital-waiver-form",
  "contract": "marketing-crm",
  "summary": "Digital Waiver & Form Builder",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "DigitalWaiverFormBuilderInput",
  "responds": "DigitalWaiverFormBuilderView"
 },
 "setLocalizationBrandingCustomer": {
  "method": "PUT",
  "path": "/localization-branding-customer",
  "contract": "marketing-crm",
  "summary": "Localization, Branding & Customer Experience Configuration",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "LocalizationBrandingCustomerExperienceConfigurationInput",
  "responds": "LocalizationBrandingCustomerExperienceConfigurationView"
 },
 "setSignatorySignatureGuardian": {
  "method": "PUT",
  "path": "/signatory-signature-guardian",
  "contract": "marketing-crm",
  "summary": "Signatory, Signature & Guardian Rule Configuration",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
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
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Digital Waiver & Form Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "heading": {
    "type": "string",
    "description": "Heading"
   },
   "paragraph": {
    "type": "string",
    "description": "Paragraph"
   },
   "legalText": {
    "type": "string",
    "description": "Legal Text"
   },
   "instructions": {
    "type": "string",
    "description": "Instructions"
   },
   "imageLogo": {
    "type": "string",
    "description": "Image/Logo"
   },
   "divider": {
    "type": "string",
    "description": "Divider"
   },
   "informationBox": {
    "type": "string",
    "description": "Information Box"
   },
   "checkbox": {
    "type": "string",
    "description": "Checkbox"
   },
   "acknowledgement": {
    "type": "string",
    "description": "Acknowledgement"
   },
   "question": {
    "type": "string",
    "description": "Question"
   },
   "signature": {
    "type": "string",
    "description": "Signature"
   },
   "initials": {
    "type": "string",
    "description": "Initials"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "customerDetails": {
    "type": "string",
    "description": "Customer Details"
   },
   "guardianDetails": {
    "type": "string",
    "description": "Guardian Details"
   },
   "headings": {
    "type": "string",
    "description": "Headings"
   },
   "paragraphs": {
    "type": "string",
    "description": "Paragraphs"
   },
   "lists": {
    "type": "string",
    "description": "Lists"
   },
   "boldEmphasis": {
    "type": "string",
    "description": "Bold/Emphasis"
   },
   "hyperlinks": {
    "type": "string",
    "description": "Hyperlinks"
   },
   "mandatoryNotices": {
    "type": "string",
    "description": "Mandatory notices"
   },
   "sectionNumbering": {
    "type": "string",
    "description": "Section numbering"
   },
   "desktop": {
    "type": "string",
    "description": "Desktop"
   },
   "mobile": {
    "type": "string",
    "description": "Mobile"
   },
   "tablet": {
    "type": "string",
    "description": "Tablet"
   },
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "kioskOnSite": {
    "type": "string",
    "description": "Kiosk/On-Site"
   }
  }
 },
 "DigitalWaiverFormBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Digital Waiver & Form Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "heading": {
    "type": "string",
    "description": "Heading"
   },
   "paragraph": {
    "type": "string",
    "description": "Paragraph"
   },
   "legalText": {
    "type": "string",
    "description": "Legal Text"
   },
   "instructions": {
    "type": "string",
    "description": "Instructions"
   },
   "imageLogo": {
    "type": "string",
    "description": "Image/Logo"
   },
   "divider": {
    "type": "string",
    "description": "Divider"
   },
   "informationBox": {
    "type": "string",
    "description": "Information Box"
   },
   "checkbox": {
    "type": "string",
    "description": "Checkbox"
   },
   "acknowledgement": {
    "type": "string",
    "description": "Acknowledgement"
   },
   "question": {
    "type": "string",
    "description": "Question"
   },
   "signature": {
    "type": "string",
    "description": "Signature"
   },
   "initials": {
    "type": "string",
    "description": "Initials"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "customerDetails": {
    "type": "string",
    "description": "Customer Details"
   },
   "guardianDetails": {
    "type": "string",
    "description": "Guardian Details"
   },
   "headings": {
    "type": "string",
    "description": "Headings"
   },
   "paragraphs": {
    "type": "string",
    "description": "Paragraphs"
   },
   "lists": {
    "type": "string",
    "description": "Lists"
   },
   "boldEmphasis": {
    "type": "string",
    "description": "Bold/Emphasis"
   },
   "hyperlinks": {
    "type": "string",
    "description": "Hyperlinks"
   },
   "mandatoryNotices": {
    "type": "string",
    "description": "Mandatory notices"
   },
   "sectionNumbering": {
    "type": "string",
    "description": "Section numbering"
   },
   "desktop": {
    "type": "string",
    "description": "Desktop"
   },
   "mobile": {
    "type": "string",
    "description": "Mobile"
   },
   "tablet": {
    "type": "string",
    "description": "Tablet"
   },
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "kioskOnSite": {
    "type": "string",
    "description": "Kiosk/On-Site"
   }
  }
 },
 "DynamicFieldsQuestionsConditionalLogicView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Fields, Questions & Conditional Logic displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "shortText": {
    "type": "string",
    "description": "Short Text"
   },
   "longText": {
    "type": "string",
    "description": "Long Text"
   },
   "number": {
    "type": "string",
    "description": "Number"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "yesNo": {
    "type": "string",
    "description": "Yes/No"
   },
   "checkbox": {
    "type": "string",
    "description": "Checkbox"
   },
   "singleSelect": {
    "type": "string",
    "description": "Single Select"
   },
   "multiSelect": {
    "type": "string",
    "description": "Multi-Select"
   },
   "dropdown": {
    "type": "string",
    "description": "Dropdown"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "mobile": {
    "type": "string",
    "description": "Mobile"
   },
   "address": {
    "type": "string",
    "description": "Address"
   },
   "customerLookup": {
    "type": "string",
    "description": "Customer Lookup"
   },
   "participantLookup": {
    "type": "string",
    "description": "Participant Lookup"
   },
   "signature": {
    "type": "string",
    "description": "Signature"
   },
   "initials": {
    "type": "string",
    "description": "Initials"
   },
   "participantName": {
    "type": "string",
    "description": "Participant Name"
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date-time",
    "description": "Date of Birth"
   },
   "customerId": {
    "type": "string",
    "description": "Customer ID"
   },
   "bookingReference": {
    "type": "string",
    "description": "Booking Reference"
   },
   "ticketNumber": {
    "type": "string",
    "description": "Ticket Number"
   },
   "guardianName": {
    "type": "string",
    "description": "Guardian Name"
   },
   "relationship": {
    "type": "string",
    "description": "Relationship"
   },
   "emergencyContact": {
    "type": "string",
    "description": "Emergency Contact"
   },
   "required": {
    "type": "boolean",
    "description": "Required"
   },
   "optional": {
    "type": "string",
    "description": "Optional"
   },
   "conditional": {
    "type": "string",
    "description": "Conditional"
   },
   "readOnly": {
    "type": "string",
    "description": "Read Only"
   },
   "autoPopulated": {
    "type": "string",
    "description": "Auto-Populated"
   },
   "minimumMaximum": {
    "type": "string",
    "description": "Minimum/Maximum"
   },
   "dateRange": {
    "type": "string",
    "format": "date-time",
    "description": "Date range"
   },
   "format": {
    "type": "string",
    "description": "Format"
   },
   "characterLimit": {
    "type": "integer",
    "description": "Character limit"
   },
   "allowedValues": {
    "type": "string",
    "description": "Allowed values"
   },
   "duplicatingData": {
    "type": "string",
    "description": "duplicating data"
   }
  }
 },
 "LocalizationBrandingCustomerExperienceConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Localization, Branding & Customer Experience Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "arabic": {
    "type": "string",
    "description": "Arabic"
   },
   "english": {
    "type": "string",
    "description": "English"
   },
   "additionalLanguagesAsConfigured": {
    "type": "string",
    "description": "Additional languages as configured"
   },
   "translatedContent": {
    "type": "string",
    "description": "translated content"
   },
   "brandLogo": {
    "type": "string",
    "description": "Brand Logo"
   },
   "venueLogo": {
    "type": "string",
    "description": "Venue Logo"
   },
   "header": {
    "type": "string",
    "description": "Header"
   },
   "footer": {
    "type": "string",
    "description": "Footer"
   },
   "typography": {
    "type": "string",
    "description": "Typography"
   },
   "customerInstructions": {
    "type": "string",
    "description": "Customer Instructions"
   },
   "supportContact": {
    "type": "string",
    "description": "Support Contact"
   },
   "confirmationMessage": {
    "type": "string",
    "description": "Confirmation Message"
   },
   "b2cWeb": {
    "type": "string",
    "description": "B2C Web"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "emailLink": {
    "type": "string",
    "description": "Email Link"
   },
   "qrLink": {
    "type": "string",
    "description": "QR Link"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "posFrontDesk": {
    "type": "string",
    "description": "POS/Front Desk"
   },
   "groupPortal": {
    "type": "string",
    "description": "Group Portal"
   },
   "keyboardNavigation": {
    "type": "string",
    "description": "Keyboard navigation"
   },
   "screenReaderCompatibleLabels": {
    "type": "string",
    "description": "Screen-reader compatible labels"
   },
   "appropriateContrast": {
    "type": "string",
    "description": "Appropriate contrast"
   },
   "clearValidationMessages": {
    "type": "string",
    "description": "Clear validation messages"
   },
   "responsiveLayouts": {
    "type": "string",
    "description": "Responsive layouts"
   }
  }
 },
 "LocalizationBrandingCustomerExperienceConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Localization, Branding & Customer Experience Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "arabic": {
    "type": "string",
    "description": "Arabic"
   },
   "english": {
    "type": "string",
    "description": "English"
   },
   "additionalLanguagesAsConfigured": {
    "type": "string",
    "description": "Additional languages as configured"
   },
   "sourceLanguage": {
    "type": "string",
    "description": "Source Language"
   },
   "translationStatus": {
    "type": "integer",
    "description": "Translation Status"
   },
   "translatorReviewer": {
    "type": "string",
    "description": "Translator/Reviewer"
   },
   "approvalStatus": {
    "type": "integer",
    "description": "Approval Status"
   },
   "lastUpdated": {
    "type": "string",
    "format": "date-time",
    "description": "Last Updated"
   },
   "translatedContent": {
    "type": "string",
    "description": "translated content"
   },
   "brandLogo": {
    "type": "string",
    "description": "Brand Logo"
   },
   "venueLogo": {
    "type": "string",
    "description": "Venue Logo"
   },
   "header": {
    "type": "string",
    "description": "Header"
   },
   "footer": {
    "type": "string",
    "description": "Footer"
   },
   "typography": {
    "type": "string",
    "description": "Typography"
   },
   "customerInstructions": {
    "type": "string",
    "description": "Customer Instructions"
   },
   "supportContact": {
    "type": "string",
    "description": "Support Contact"
   },
   "confirmationMessage": {
    "type": "string",
    "description": "Confirmation Message"
   },
   "b2cWeb": {
    "type": "string",
    "description": "B2C Web"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "emailLink": {
    "type": "string",
    "description": "Email Link"
   },
   "qrLink": {
    "type": "string",
    "description": "QR Link"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "posFrontDesk": {
    "type": "string",
    "description": "POS/Front Desk"
   },
   "groupPortal": {
    "type": "string",
    "description": "Group Portal"
   },
   "keyboardNavigation": {
    "type": "string",
    "description": "Keyboard navigation"
   },
   "screenReaderCompatibleLabels": {
    "type": "string",
    "description": "Screen-reader compatible labels"
   },
   "appropriateContrast": {
    "type": "string",
    "description": "Appropriate contrast"
   },
   "clearValidationMessages": {
    "type": "string",
    "description": "Clear validation messages"
   },
   "responsiveLayouts": {
    "type": "string",
    "description": "Responsive layouts"
   }
  }
 },
 "ProductEventExperienceAssociationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Product, Event & Experience Association displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "activity": {
    "type": "string",
    "description": "Activity"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "camp": {
    "type": "string",
    "description": "Camp"
   },
   "rental": {
    "type": "string",
    "description": "Rental"
   },
   "resource": {
    "type": "string",
    "description": "Resource"
   },
   "package": {
    "type": "string",
    "description": "Package"
   },
   "addOn": {
    "type": "string",
    "description": "Add-On"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "activityLiabilityWaiver": {
    "type": "string",
    "description": "Activity Liability Waiver"
   },
   "safetyAcknowledgement": {
    "type": "string",
    "description": "Safety Acknowledgement"
   },
   "parentGuardianConsent": {
    "type": "boolean",
    "description": "Parent/Guardian Consent"
   },
   "mandatory": {
    "type": "string",
    "description": "Mandatory"
   },
   "optional": {
    "type": "string",
    "description": "Optional"
   },
   "conditional": {
    "type": "string",
    "description": "Conditional"
   },
   "informational": {
    "type": "string",
    "description": "Informational"
   },
   "automaticallyInheritedByApplicableActivities": {
    "type": "string",
    "description": "Automatically inherited by applicable activities"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "futureBookings": {
    "type": "string",
    "description": "Future bookings"
   },
   "tickets": {
    "type": "string",
    "description": "Tickets"
   },
   "participants": {
    "type": "string",
    "description": "Participants"
   },
   "events": {
    "type": "string",
    "description": "Events"
   }
  }
 },
 "SignatorySignatureGuardianRuleConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Signatory, Signature & Guardian Rule Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "purchaser": {
    "type": "string",
    "description": "Purchaser"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "parent": {
    "type": "string",
    "description": "Parent"
   },
   "legalGuardian": {
    "type": "string",
    "description": "Legal Guardian"
   },
   "groupLeader": {
    "type": "string",
    "description": "Group Leader"
   },
   "corporateRepresentative": {
    "type": "string",
    "description": "Corporate Representative"
   },
   "member": {
    "type": "string",
    "description": "Member"
   },
   "rentalCustomer": {
    "type": "string",
    "description": "Rental Customer"
   },
   "otherAuthorizedSignatory": {
    "type": "string",
    "description": "Other Authorized Signatory"
   },
   "signatureRequired": {
    "type": "boolean",
    "description": "Signature Required"
   },
   "initialsRequired": {
    "type": "boolean",
    "description": "Initials Required"
   },
   "typedAcceptance": {
    "type": "string",
    "description": "Typed Acceptance"
   },
   "checkboxAcceptance": {
    "type": "string",
    "description": "Checkbox Acceptance"
   },
   "digitalSignature": {
    "type": "string",
    "description": "Digital Signature"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/Time"
   },
   "signatoryName": {
    "type": "string",
    "description": "Signatory Name"
   },
   "relationship": {
    "type": "string",
    "description": "Relationship"
   },
   "identityVerificationWhereRequired": {
    "type": "boolean",
    "description": "Identity Verification where required"
   },
   "participantGuardian": {
    "type": "string",
    "description": "Participant + Guardian"
   },
   "customerAuthorizedRepresentative": {
    "type": "string",
    "description": "Customer + Authorized Representative"
   },
   "eachParticipantSignsIndividually": {
    "type": "string",
    "description": "Each participant signs individually"
   },
   "guardianSignsForEachMinor": {
    "type": "string",
    "description": "Guardian signs for each minor"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "waiverVersion": {
    "type": "string",
    "description": "Waiver Version"
   },
   "signatory": {
    "type": "string",
    "description": "Signatory"
   },
   "authenticationMethod": {
    "type": "string",
    "description": "Authentication Method"
   },
   "relevantTransactionCustomerReference": {
    "type": "string",
    "description": "Relevant transaction/customer reference"
   },
   "consentEvidence": {
    "type": "string",
    "description": "Consent evidence"
   },
   "organizationSLegalComplianceApproval": {
    "type": "string",
    "description": "organization's legal/compliance approval"
   }
  }
 },
 "SignatorySignatureGuardianRuleConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Signatory, Signature & Guardian Rule Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "purchaser": {
    "type": "string",
    "description": "Purchaser"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "parent": {
    "type": "string",
    "description": "Parent"
   },
   "legalGuardian": {
    "type": "string",
    "description": "Legal Guardian"
   },
   "groupLeader": {
    "type": "string",
    "description": "Group Leader"
   },
   "corporateRepresentative": {
    "type": "string",
    "description": "Corporate Representative"
   },
   "member": {
    "type": "string",
    "description": "Member"
   },
   "rentalCustomer": {
    "type": "string",
    "description": "Rental Customer"
   },
   "otherAuthorizedSignatory": {
    "type": "string",
    "description": "Other Authorized Signatory"
   },
   "signatureRequired": {
    "type": "boolean",
    "description": "Signature Required"
   },
   "initialsRequired": {
    "type": "boolean",
    "description": "Initials Required"
   },
   "typedAcceptance": {
    "type": "string",
    "description": "Typed Acceptance"
   },
   "checkboxAcceptance": {
    "type": "string",
    "description": "Checkbox Acceptance"
   },
   "digitalSignature": {
    "type": "string",
    "description": "Digital Signature"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/Time"
   },
   "signatoryName": {
    "type": "string",
    "description": "Signatory Name"
   },
   "relationship": {
    "type": "string",
    "description": "Relationship"
   },
   "identityVerificationWhereRequired": {
    "type": "boolean",
    "description": "Identity Verification where required"
   },
   "participantGuardian": {
    "type": "string",
    "description": "Participant + Guardian"
   },
   "customerAuthorizedRepresentative": {
    "type": "string",
    "description": "Customer + Authorized Representative"
   },
   "eachParticipantSignsIndividually": {
    "type": "string",
    "description": "Each participant signs individually"
   },
   "guardianSignsForEachMinor": {
    "type": "string",
    "description": "Guardian signs for each minor"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "waiverVersion": {
    "type": "string",
    "description": "Waiver Version"
   },
   "signatory": {
    "type": "string",
    "description": "Signatory"
   },
   "authenticationMethod": {
    "type": "string",
    "description": "Authentication Method"
   },
   "relevantTransactionCustomerReference": {
    "type": "string",
    "description": "Relevant transaction/customer reference"
   },
   "consentEvidence": {
    "type": "string",
    "description": "Consent evidence"
   },
   "organizationSLegalComplianceApproval": {
    "type": "string",
    "description": "organization's legal/compliance approval"
   }
  }
 },
 "VersioningEffectiveDatesLegalChangeControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Versioning, Effective Dates & Legal Change Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "v10": {
    "type": "string",
    "description": "v1.0"
   },
   "v11": {
    "type": "string",
    "description": "v1.1"
   },
   "v20": {
    "type": "string",
    "description": "v2.0"
   },
   "versionNumber": {
    "type": "string",
    "description": "Version Number"
   },
   "createdBy": {
    "type": "string",
    "format": "date-time",
    "description": "Created By"
   },
   "createdDate": {
    "type": "string",
    "format": "date-time",
    "description": "Created Date"
   },
   "changeReason": {
    "type": "string",
    "description": "Change Reason"
   },
   "legalReviewer": {
    "type": "string",
    "description": "Legal Reviewer"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "previousVersionNewVersion": {
    "type": "string",
    "description": "Previous Version ↔ New Version"
   },
   "addedText": {
    "type": "string",
    "description": "Added text"
   },
   "removedText": {
    "type": "string",
    "description": "Removed text"
   },
   "changedQuestions": {
    "type": "string",
    "description": "Changed questions"
   },
   "changedSignatoryRules": {
    "type": "string",
    "description": "Changed signatory rules"
   },
   "changedAssociations": {
    "type": "string",
    "description": "Changed associations"
   }
  }
 },
 "WaiverApprovalTestingPublicationWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Waiver Approval, Testing & Publication Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "requiredLegalTextPresent": {
    "type": "string",
    "description": "Required legal text present"
   },
   "requiredFieldsConfigured": {
    "type": "string",
    "description": "Required fields configured"
   },
   "conditionalRulesValid": {
    "type": "string",
    "description": "Conditional rules valid"
   },
   "signatureRulesConfigured": {
    "type": "string",
    "description": "Signature rules configured"
   },
   "productsEventsAssigned": {
    "type": "string",
    "description": "Products/events assigned"
   },
   "completionRulesConfigured": {
    "type": "string",
    "description": "Completion rules configured"
   },
   "requiredTranslationsApproved": {
    "type": "string",
    "description": "Required translations approved"
   },
   "effectiveDatesValid": {
    "type": "string",
    "description": "Effective dates valid"
   },
   "activityWaiver": {
    "type": "string",
    "description": "✓ Activity Waiver"
   },
   "guardianConsent": {
    "type": "boolean",
    "description": "✓ Guardian Consent"
   },
   "guardianSignature": {
    "type": "string",
    "description": "✓ Guardian Signature"
   },
   "adultDeclaration": {
    "type": "string",
    "description": "✕ Adult Declaration"
   },
   "controlledRollout": {
    "type": "string",
    "description": "Controlled Rollout"
   },
   "submittedBy": {
    "type": "string",
    "description": "Submitted By"
   },
   "reviewedBy": {
    "type": "string",
    "description": "Reviewed By"
   },
   "approvedBy": {
    "type": "integer",
    "description": "Approved By"
   },
   "publishedBy": {
    "type": "string",
    "description": "Published By"
   },
   "dates": {
    "type": "string",
    "description": "Dates"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "comments": {
    "type": "string",
    "description": "Comments"
   },
   "configuration": {
    "type": "string",
    "description": "configuration"
   },
   "enforced": {
    "type": "string",
    "description": "enforced"
   },
   "insideTicketingOrTicketMedia": {
    "type": "string",
    "description": "inside Ticketing or Ticket Media"
   },
   "multipleInconsistentWaiverImplementations": {
    "type": "string",
    "description": "multiple inconsistent waiver implementations"
   },
   "ai": {
    "type": "string",
    "description": "& AI"
   }
  }
 },
 "WaiverApprovalTestingPublicationWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Waiver Approval, Testing & Publication Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "requiredLegalTextPresent": {
    "type": "string",
    "description": "Required legal text present"
   },
   "requiredFieldsConfigured": {
    "type": "string",
    "description": "Required fields configured"
   },
   "conditionalRulesValid": {
    "type": "string",
    "description": "Conditional rules valid"
   },
   "signatureRulesConfigured": {
    "type": "string",
    "description": "Signature rules configured"
   },
   "productsEventsAssigned": {
    "type": "string",
    "description": "Products/events assigned"
   },
   "completionRulesConfigured": {
    "type": "string",
    "description": "Completion rules configured"
   },
   "requiredTranslationsApproved": {
    "type": "string",
    "description": "Required translations approved"
   },
   "effectiveDatesValid": {
    "type": "string",
    "description": "Effective dates valid"
   },
   "activityWaiver": {
    "type": "string",
    "description": "✓ Activity Waiver"
   },
   "guardianConsent": {
    "type": "boolean",
    "description": "✓ Guardian Consent"
   },
   "guardianSignature": {
    "type": "string",
    "description": "✓ Guardian Signature"
   },
   "adultDeclaration": {
    "type": "string",
    "description": "✕ Adult Declaration"
   },
   "controlledRollout": {
    "type": "string",
    "description": "Controlled Rollout"
   },
   "submittedBy": {
    "type": "string",
    "description": "Submitted By"
   },
   "reviewedBy": {
    "type": "string",
    "description": "Reviewed By"
   },
   "approvedBy": {
    "type": "integer",
    "description": "Approved By"
   },
   "publishedBy": {
    "type": "string",
    "description": "Published By"
   },
   "dates": {
    "type": "string",
    "description": "Dates"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "comments": {
    "type": "string",
    "description": "Comments"
   },
   "configuration": {
    "type": "string",
    "description": "configuration"
   },
   "enforced": {
    "type": "string",
    "description": "enforced"
   },
   "insideTicketingOrTicketMedia": {
    "type": "string",
    "description": "inside Ticketing or Ticket Media"
   },
   "multipleInconsistentWaiverImplementations": {
    "type": "string",
    "description": "multiple inconsistent waiver implementations"
   },
   "ai": {
    "type": "string",
    "description": "& AI"
   }
  }
 },
 "WaiverConsentCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Waiver & Consent Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalTemplates": {
    "type": "integer",
    "description": "Total Templates"
   },
   "published": {
    "type": "string",
    "description": "Published"
   },
   "draft": {
    "type": "string",
    "description": "Draft"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "scheduled": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled"
   },
   "expiring": {
    "type": "string",
    "description": "Expiring"
   },
   "archived": {
    "type": "string",
    "description": "Archived"
   },
   "productsRequiringWaiver": {
    "type": "string",
    "description": "Products Requiring Waiver"
   },
   "activeWaiverVersions": {
    "type": "integer",
    "description": "Active Waiver Versions"
   },
   "waiversRequiringReview": {
    "type": "string",
    "description": "Waivers Requiring Review"
   },
   "waiverId": {
    "type": "string",
    "description": "Waiver ID"
   },
   "waiverName": {
    "type": "string",
    "description": "Waiver Name"
   },
   "type": {
    "type": "string",
    "description": "Type"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "associatedProducts": {
    "type": "string",
    "description": "Associated Products"
   },
   "signatoryType": {
    "type": "string",
    "description": "Signatory Type"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "lastModified": {
    "type": "string",
    "format": "date-time",
    "description": "Last Modified"
   },
   "liabilityWaiver": {
    "type": "string",
    "description": "Liability Waiver"
   },
   "parentGuardianConsent": {
    "type": "boolean",
    "description": "Parent/Guardian Consent"
   },
   "participationConsent": {
    "type": "boolean",
    "description": "Participation Consent"
   },
   "medicalDeclaration": {
    "type": "string",
    "description": "Medical Declaration"
   },
   "safetyAcknowledgement": {
    "type": "string",
    "description": "Safety Acknowledgement"
   },
   "mediaConsent": {
    "type": "boolean",
    "description": "Media Consent"
   },
   "rentalAgreement": {
    "type": "string",
    "description": "Rental Agreement"
   },
   "termsAcceptance": {
    "type": "string",
    "description": "Terms Acceptance"
   },
   "membershipDeclaration": {
    "type": "string",
    "description": "Membership Declaration"
   },
   "customForm": {
    "type": "string",
    "description": "Custom Form"
   },
   "preview": {
    "type": "string",
    "description": "Preview"
   },
   "test": {
    "type": "string",
    "description": "Test"
   }
  }
 },
 "WaiverTemplateLibraryMasterSetupView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Waiver Template Library & Master Setup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "waiverId": {
    "type": "string",
    "description": "Waiver ID"
   },
   "waiverName": {
    "type": "string",
    "description": "Waiver Name"
   },
   "internalDescription": {
    "type": "string",
    "description": "Internal Description"
   },
   "waiverType": {
    "type": "string",
    "description": "Waiver Type"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "defaultLanguage": {
    "type": "string",
    "description": "Default Language"
   },
   "applicableCountry": {
    "type": "string",
    "description": "Applicable Country"
   },
   "applicableJurisdiction": {
    "type": "string",
    "description": "Applicable Jurisdiction"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "useMasterTemplate": {
    "type": "string",
    "description": "Use Master Template"
   },
   "businessOwner": {
    "type": "string",
    "description": "Business Owner"
   },
   "legalReviewer": {
    "type": "string",
    "description": "Legal Reviewer"
   },
   "complianceOwner": {
    "type": "string",
    "description": "Compliance Owner"
   },
   "operationalOwner": {
    "type": "string",
    "description": "Operational Owner"
   }
  }
 },
 "WaiverTriggerEligibilityCompletionRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Waiver Trigger, Eligibility & Completion Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "duringCheckout": {
    "type": "string",
    "description": "During Checkout"
   },
   "afterPurchase": {
    "type": "string",
    "description": "After Purchase"
   },
   "beforeTicketIssuance": {
    "type": "string",
    "description": "Before Ticket Issuance"
   },
   "beforeTicketDownload": {
    "type": "string",
    "description": "Before Ticket Download"
   },
   "beforeEvent": {
    "type": "string",
    "description": "Before Event"
   },
   "beforeCheckIn": {
    "type": "string",
    "description": "Before Check-In"
   },
   "beforeAccess": {
    "type": "string",
    "description": "Before Access"
   },
   "beforeEquipmentCollection": {
    "type": "string",
    "description": "Before Equipment Collection"
   },
   "beforeMembershipActivation": {
    "type": "string",
    "description": "Before Membership Activation"
   },
   "beforeActivityStart": {
    "type": "string",
    "description": "Before Activity Start"
   },
   "age": {
    "type": "string",
    "description": "Age"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "activity": {
    "type": "string",
    "description": "Activity"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "participantType": {
    "type": "string",
    "description": "Participant Type"
   },
   "bookingType": {
    "type": "string",
    "description": "Booking Type"
   },
   "immediately": {
    "type": "string",
    "description": "Immediately"
   },
   "beforeTicketRelease": {
    "type": "string",
    "description": "Before Ticket Release"
   },
   "xHoursBeforeEvent": {
    "type": "string",
    "description": "X hours before event"
   },
   "xDaysBeforeVisit": {
    "type": "string",
    "description": "X days before visit"
   },
   "beforeArrival": {
    "type": "string",
    "description": "Before arrival"
   },
   "warnsOnly": {
    "type": "string",
    "description": "Warns only"
   },
   "blocksTicketDownload": {
    "type": "string",
    "description": "Blocks Ticket Download"
   },
   "blocksTicketActivation": {
    "type": "string",
    "description": "Blocks Ticket Activation"
   },
   "blocksCheckIn": {
    "type": "string",
    "description": "Blocks Check-In"
   },
   "blocksAccess": {
    "type": "string",
    "description": "Blocks Access"
   },
   "requiresStaffOverride": {
    "type": "string",
    "description": "Requires Staff Override"
   },
   "t7Days": {
    "type": "string",
    "description": "T−7 days"
   },
   "t3Days": {
    "type": "string",
    "description": "T−3 days"
   },
   "t24Hours": {
    "type": "string",
    "description": "T−24 hours"
   }
  }
 }
}
```
