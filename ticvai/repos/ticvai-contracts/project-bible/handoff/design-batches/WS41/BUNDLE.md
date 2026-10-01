# WS41 — Privacy  Consent   Preference Management board 1

**10 screens · 18 operations · 25 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-021` | Privacy & Consent Configuration Command Center | configEditor | 2 | 0 | — |
| `CMS-022` | Data Processing Purpose & Lawful Basis Registry | listDetail | 1 | 0 | — |
| `CMS-023` | Consent Purpose & Consent Type Builder | configEditor | 1 | 0 | — |
| `CMS-024` | Communication Preference & Marketing Permission Configuration | configEditor | 1 | 0 | — |
| `CMS-025` | Cookie, Tracking & Digital Technology Registry | listDetail | 6 | 0 | — |
| `CMS-026` | Cookie Banner & Preference Center Designer | configEditor | 2 | 0 | — |
| `CMS-027` | Consent Capture Point & Customer Journey Configuration | configEditor | 1 | 0 | — |
| `CMS-028` | Privacy Notice, Policy & Terms Version Management | listDetail | 2 | 1 | — |
| `CMS-029` | Minor, Guardian & Age-Based Privacy Configuration | configEditor | 1 | 0 | — |
| `CMS-030` | Privacy Configuration Testing, Approval & Publication | configEditor | 2 | 1 | — |

## Thin screens in this batch

**CMS-022, CMS-025, CMS-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-021",
  "name": "Privacy & Consent Configuration Command Center",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.1",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/privacy-consent-configuration-command-center-cms-021",
   "component": "apps/venue-management-web/src/routes/policy/PrivacyConsentConfigurationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-022",
    "CMS-023",
    "CMS-024",
    "CMS-025",
    "CMS-026",
    "CMS-027",
    "CMS-028",
    "CMS-029",
    "CMS-030"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-021 holds none of them. The edge carries nothing: CMS-021 is opened from CMS-001, so this edge is the way back and CMS-001 keeps its own state"
    },
    {
     "to": "CMS-022",
     "trigger": "Works in Data Processing Purpose & Lawful Basis Registry",
     "provenance": "flow F150 step 1→2",
     "operation": "listPrivacyConsent"
    },
    {
     "to": "CMS-023",
     "trigger": "Works in Consent Purpose & Consent Type Builder",
     "provenance": "flow F150 step 3→4",
     "operation": "listPrivacyConsent"
    },
    {
     "to": "CMS-024",
     "trigger": "Works in Communication Preference & Marketing Permission Configuration",
     "provenance": "flow F150 step 5→6",
     "operation": "listPrivacyConsent"
    },
    {
     "to": "CMS-025",
     "trigger": "Works in Cookie, Tracking & Digital Technology Registry",
     "provenance": "flow F150 step 7→8",
     "operation": "listPrivacyConsent"
    },
    {
     "to": "CMS-026",
     "trigger": "Works in Cookie Banner & Preference Center Designer",
     "provenance": "flow F150 step 9→10",
     "operation": "listPrivacyConsent"
    },
    {
     "to": "CMS-027",
     "trigger": "Works in Consent Capture Point & Customer Journey Configuration",
     "provenance": "flow F150 step 11→12",
     "operation": "listPrivacyConsent"
    },
    {
     "to": "CMS-028",
     "trigger": "Works in Privacy Notice, Policy & Terms Version Management",
     "provenance": "flow F150 step 13→14",
     "operation": "listPrivacyConsent"
    },
    {
     "to": "CMS-029",
     "trigger": "Works in Minor, Guardian & Age-Based Privacy Configuration",
     "provenance": "flow F150 step 15→16",
     "operation": "listPrivacyConsent"
    },
    {
     "to": "CMS-030",
     "trigger": "Works in Privacy Configuration Testing, Approval & Publication",
     "provenance": "flow F150 step 17→18",
     "operation": "listPrivacyConsent"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An authorized administrator can centrally understand and manage TICVAI's privacy, consent and preference configuration without navigating individual sales or customer modules.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Display configuration indicators such as; Configuration Type Scope Status) and no display directory — it is settings, not a population",
  "purpose": "Provide administrators with one central dashboard for configuring and governing TICVAI's privacy framework across tenants, brands, venues and customer channels.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Create Consent Purpose, Create Policy, Configure Preferences, Configure Cookies, Configure Capture Point, Test Configuration, Submit for Approval. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Quick Actions"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search privacy consent",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Brand",
        "Country",
        "Venue",
        "Channel",
        "Consent Type",
        "Policy",
        "Language",
        "Status",
        "Effective Date"
       ],
       "notes": "The pack filters this screen by tenant, brand, country, venue, channel, consent type and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Active Consent Purposes",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "selectField",
       "label": "Active Privacy Policies",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "selectField",
       "label": "Communication Preference Types",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "selectField",
       "label": "Cookie Categories",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "textField",
       "label": "Active Consent Capture Points",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "selectField",
       "label": "Supported Languages",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "selectField",
       "label": "Pending Policy Approvals",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "selectField",
       "label": "Scheduled Policy Changes",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "selectField",
       "label": "Configuration Warnings",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "textField",
       "label": "Consent Configurations Requiring Review",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Display configuration indicators such as"
      },
      {
       "kind": "selectField",
       "label": "n From",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Configuration Type Scope Status"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create Consent Purpose",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Policy",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Configure Preferences",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Configure Cookies",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Configure Capture Point",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Test Configuration",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Submit for Approval",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 4 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The privacy consent configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the privacy consent untouched.",
   "emptyFirstRun": "No privacy consent configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoResults": "The filter narrowed it and the privacy consent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrivacyConsent",
    "contract": "marketing-crm",
    "purpose": "Privacy & Consent Configuration Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCustomerPrivacyConsent",
    "contract": "marketing-crm",
    "purpose": "Customer Privacy, Consent & Preference 360°",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-021",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-021"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 4. 0 of 10 labels bound to a contract property; 28 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-022",
  "name": "Data Processing Purpose & Lawful Basis Registry",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.2",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/data-processing-purpose-lawful-basis-registry-cms-022",
   "component": "apps/venue-management-web/src/routes/policy/DataProcessingPurposeLawfulBasisRegistry.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-021"
   ],
   "exitTo": [
    "CMS-021"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-021, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-021",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F150 step 2→3",
     "operation": "listDataProcessingPurpose"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every governed processing purpose can be centrally documented, classified, versioned and associated with the appropriate TICVAI processes.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a central registry explaining why customer data is being collected or processed. This becomes the foundation used by consent forms, policies, customer journeys and downstream systems. Ticket Purchase & Fulfillment Customer Account Management Membership Administration Customer Support Transactional Communication Marketing Communication Personalization Analytics Fraud Prevention Security Biometric Processing Location-Based Services Loyalty Customer Research",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 5"
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
       "impliedBy": "listDataProcessingPurpose",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The data processing purpose list.",
   "error": "Could not load. Names which read failed and leaves the data processing purpose untouched.",
   "emptyFirstRun": "No data processing purpose yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the data processing purpose are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDataProcessingPurpose",
    "contract": "marketing-crm",
    "purpose": "Data Processing Purpose & Lawful Basis Registry",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DataProcessingPurposeLawfulBasisRegistryView.purposeId",
    "DataProcessingPurposeLawfulBasisRegistryView.purposeName",
    "DataProcessingPurposeLawfulBasisRegistryView.description",
    "DataProcessingPurposeLawfulBasisRegistryView.businessOwner",
    "DataProcessingPurposeLawfulBasisRegistryView.dataControllerApplicableOrganization"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-022",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-022"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 54 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-023",
  "name": "Consent Purpose & Consent Type Builder",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.3",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/consent-purpose-consent-type-builder-cms-023",
   "component": "apps/venue-management-web/src/routes/policy/ConsentPurposeConsentTypeBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-021"
   ],
   "exitTo": [
    "CMS-021"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-021, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-021",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F150 step 4→5",
     "operation": "setConsentPurposes"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can create reusable, granular and version-controlled consent definitions without development effort.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the actual consent objects that TICVAI may request from customers.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Consent ID",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Name",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Processing Purpose",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Consent Text",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mandatory / Optional",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "textField",
       "label": "Explicit / Other configured consent method",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default state",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Withdrawal permitted",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Renewal required",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reconfirmation interval",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Age restrictions",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Guardian requirement",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel applicability",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Country applicability",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand applicability",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 7 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setConsentPurposes"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The consent purpose consent configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the consent purpose consent untouched.",
   "emptyFirstRun": "No consent purpose consent configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setConsentPurposes",
    "contract": "marketing-crm",
    "purpose": "Configure consent purposes",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-023",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-023"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 17 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-024",
  "name": "Communication Preference & Marketing Permission Configuration",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.4",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/communication-preference-marketing-permission-configurat-cms-024",
   "component": "apps/venue-management-web/src/routes/policy/CommunicationPreferenceMarketingPermissionConfig.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-021"
   ],
   "exitTo": [
    "CMS-021"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-021, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-021",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F150 step 6→7",
     "operation": "setCommunicationPreferenceMarketing"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "downstream communication systems can consistently enforce.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Administrators define) and no display directory — it is settings, not a population",
  "purpose": "Define how customers control the communications they wish to receive. This screen should integrate strongly with CRM and Marketing but remain governed by the central Privacy Engine.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Channel + Purpose + Brand. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Support"
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
       "label": "Email",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "SMS",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "WhatsApp",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Push Notification",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Phone",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Direct Mail",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Other future channels",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Preference category",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      },
      {
       "kind": "selectField",
       "label": "Communication type",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      },
      {
       "kind": "selectField",
       "label": "Marketing/transactional classification",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      },
      {
       "kind": "selectField",
       "label": "Applicable brands",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      },
      {
       "kind": "selectField",
       "label": "Applicable countries",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      },
      {
       "kind": "selectField",
       "label": "Available channels",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      },
      {
       "kind": "selectField",
       "label": "Customer-editable status",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      },
      {
       "kind": "selectField",
       "label": "Default behavior",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      },
      {
       "kind": "selectField",
       "label": "Consent dependency",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      },
      {
       "kind": "selectField",
       "label": "Expiry/reconfirmation if applicable",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Administrators define"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Channel + Purpose + Brand",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 8 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The communication preference marketing configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the communication preference marketing untouched.",
   "emptyFirstRun": "No communication preference marketing configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCommunicationPreferenceMarketing",
    "contract": "marketing-crm",
    "purpose": "Communication Preference & Marketing Permission Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-024",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-024"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 18 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-025",
  "name": "Cookie, Tracking & Digital Technology Registry",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.5",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/cookie-tracking-digital-technology-registry-cms-025",
   "component": "apps/venue-management-web/src/routes/policy/CookieTrackingDigitalTechnologyRegistry.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-021"
   ],
   "exitTo": [
    "CMS-021"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-021, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-021",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F150 step 8→9",
     "operation": "listCookieTrackingDigital"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators maintain an auditable inventory of governed cookies and tracking technologies, their purposes and applicable consent requirements.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain a centralized registry of cookies, SDKs, pixels and other governed tracking technologies used by TICVAI digital channels. This should cover more than traditional browser cookies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Analytics Tracker, Embedded Service, Other tracking technology. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 10 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 10"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 10"
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
       "label": "Analytics Tracker",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 10 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Embedded Service",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 10 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Other tracking technology",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 10 §Support"
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
   "loading": "The cookie tracking digital list.",
   "error": "Could not load. Names which read failed and leaves the cookie tracking digital untouched.",
   "emptyFirstRun": "No cookie tracking digital yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cookie tracking digital are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCookieTrackingDigital",
    "contract": "marketing-crm",
    "purpose": "Cookie, Tracking & Digital Technology Registry",
    "trigger": "onLoad"
   },
   {
    "operationId": "setTrackingTechnology",
    "contract": "marketing-crm",
    "purpose": "Add, classify, approve or retire a technology",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordCookieScan",
    "contract": "marketing-crm",
    "purpose": "Upload or take in a scan result",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listCookieScans",
    "contract": "marketing-crm",
    "purpose": "Scan runs and what each found",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listCookieScanPolicies",
    "contract": "marketing-crm",
    "purpose": "Scan schedules per channel",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setCookieScanPolicy",
    "contract": "marketing-crm",
    "purpose": "Set a scan schedule and alert recipients",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "CookieTrackingDigitalTechnologyRegistryView.technologyType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-025",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-025"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 3 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-026",
  "name": "Cookie Banner & Preference Center Designer",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.6",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/cookie-banner-preference-center-designer-cms-026",
   "component": "apps/venue-management-web/src/routes/policy/CookieBannerPreferenceCenterDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-021"
   ],
   "exitTo": [
    "CMS-021"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-021, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-021",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F150 step 10→11",
     "operation": "listCookieBannerPreference"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can design and publish branded cookie/privacy preference experiences without requiring source-code changes for ordinary configuration changes.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Provide a no-code designer for privacy/cookie interfaces displayed on digital channels.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Additional configured languages. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Support"
   },
   {
    "operation": null,
    "why": "**Cookie Banner & Preference Center Designer declares no operation that writes anything** — its only declared call is `listCookieBannerPreference`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Logo",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Title",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Buttons",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Position",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Theme",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Branding",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Links",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Category descriptions",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Additional configured languages",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 11 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cookie banner preference configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the cookie banner preference untouched.",
   "emptyFirstRun": "No cookie banner preference configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCookieBannerPreference",
    "contract": "marketing-crm",
    "purpose": "Cookie Banner & Preference Center Designer",
    "trigger": "onLoad"
   },
   {
    "operationId": "setCookieBannerDesign",
    "contract": "marketing-crm",
    "purpose": "Save a banner design as a new draft version",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-026",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-026"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 11 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-027",
  "name": "Consent Capture Point & Customer Journey Configuration",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.7",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/consent-capture-point-customer-journey-configuration-cms-027",
   "component": "apps/venue-management-web/src/routes/policy/ConsentCapturePointCustomerJourneyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-021"
   ],
   "exitTo": [
    "CMS-021"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-021, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-021",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F150 step 12→13",
     "operation": "setConsentCapturePoint"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "without duplicating configuration inside each frontend channel.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Potential capture points include; For each capture point define) and no display directory — it is settings, not a population",
  "purpose": "Define where, when and under what circumstances privacy notices and consent requests appear. This prevents each channel from implementing consent independently.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Account Registration",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Guest Checkout",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Ticket Purchase",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Membership Enrollment",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Annual Pass Enrollment",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Mobile App Registration",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "POS Customer Creation",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Kiosk",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "CRM Customer Creation",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Wallet Enrollment",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Face Enrollment",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Newsletter Signup",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Customer Portal",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Competition/Promotion",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "API/Partner Journey",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §Potential capture points include"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Customer type",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Processing purpose",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Required notice",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Required consent",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Optional preferences",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Consent wording",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Policy version",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Display order",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      },
      {
       "kind": "selectField",
       "label": "Mandatory/optional behavior",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 12 §For each capture point define"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setConsentCapturePoint"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The consent capture point configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the consent capture point untouched.",
   "emptyFirstRun": "No consent capture point configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setConsentCapturePoint",
    "contract": "marketing-crm",
    "purpose": "Consent Capture Point & Customer Journey Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-027",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-027"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 28 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-028",
  "name": "Privacy Notice, Policy & Terms Version Management",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.8",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/privacy-notice-policy-terms-version-management-cms-028",
   "component": "apps/venue-management-web/src/routes/policy/PrivacyNoticePolicyTermsVersionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-021"
   ],
   "exitTo": [
    "CMS-021"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-021, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-021",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F150 step 14→15",
     "operation": "listPrivacyNoticePolicy"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "which version was presented to a customer.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage customer-facing privacy notices and related governed documents with complete version control.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 14"
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
       "label": "Privacy Policy",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 14 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "No Customer Action",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 14 §Allow changes to be marked"
      },
      {
       "kind": "secondaryButton",
       "label": "Save privacy notice policy governance",
       "operation": "setPrivacyNoticePolicyGovernance",
       "permission": "GUEST_MANAGE",
       "notes": "**An upsert keyed on `policyId`: one row per version of one privacy document.** The document itself is white-label's `Policy` (`setPolicy`, never overwritten); this row is what the privacy administrator decides about that version, and is what `listPrivacyNoticePolicy` shows beside it.",
       "provenance": "contract marketing-crm.yaml PUT /privacy-notice-policy"
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
   "loading": "The privacy notice policy list.",
   "error": "Could not load. Names which read failed and leaves the privacy notice policy untouched.",
   "emptyFirstRun": "No privacy notice policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the privacy notice policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrivacyNoticePolicy",
    "contract": "marketing-crm",
    "purpose": "Privacy Notice, Policy & Terms Version Management",
    "trigger": "onLoad"
   },
   {
    "operationId": "setPrivacyNoticePolicyGovernance",
    "contract": "marketing-crm",
    "purpose": "Set the privacy governance of one version of a privacy document",
    "trigger": "onAction",
    "invalidates": [
     "listPrivacyNoticePolicy"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PrivacyNoticePolicyTermsVersionManagementView.documentType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-028",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-028"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 2 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPrivacyNoticePolicyGovernance",
    "component": "modal",
    "trigger": "Save privacy notice policy governance",
    "body": "**Collects what `setPrivacyNoticePolicyGovernance` sends before it is called.** Required: `id`, `policyId`, `documentType`, `status`. Optional: `changeClassification`, `requiresReAcceptance`, `requiresNotification`, `ownerPrincipalId`, `approvedByPrincipalId`, `approvalRequestId`, `approvedAt`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PrivacyNoticeGovernance",
    "confirm": {
     "label": "Save privacy notice policy governance",
     "operation": "setPrivacyNoticePolicyGovernance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "policyId",
      "documentType",
      "status",
      "changeClassification",
      "requiresReAcceptance",
      "requiresNotification",
      "ownerPrincipalId",
      "approvedByPrincipalId",
      "approvalRequestId",
      "approvedAt",
      "scopePath"
     ]
    },
    "provenance": "contract marketing-crm.yaml PUT /privacy-notice-policy"
   }
  ],
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
  "id": "CMS-029",
  "name": "Minor, Guardian & Age-Based Privacy Configuration",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.9",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/minor-guardian-age-based-privacy-configuration-cms-029",
   "component": "apps/venue-management-web/src/routes/policy/MinorGuardianAgeBasedPrivacyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-021"
   ],
   "exitTo": [
    "CMS-021"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-021, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-021",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F150 step 16→17",
     "operation": "setMinorGuardianAge"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "separation between privacy consent and operational waivers.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Where required/configured) and no display directory — it is settings, not a population",
  "purpose": "Provide specialized privacy configuration for journeys involving children and guardians. This is especially important for TICVAI customers operating: Theme parks Attractions Camps Academies Family entertainment Children's events",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Guardian name",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 15 §Where required/configured"
      },
      {
       "kind": "selectField",
       "label": "Relationship",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 15 §Where required/configured"
      },
      {
       "kind": "selectField",
       "label": "Email",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 15 §Where required/configured"
      },
      {
       "kind": "selectField",
       "label": "Mobile",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 15 §Where required/configured"
      },
      {
       "kind": "selectField",
       "label": "Verification status",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 15 §Where required/configured"
      },
      {
       "kind": "selectField",
       "label": "Consent status",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 15 §Where required/configured"
      },
      {
       "kind": "selectField",
       "label": "Consent version",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 15 §Where required/configured"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 15 §Where required/configured"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setMinorGuardianAge"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The minor guardian age-based configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the minor guardian age-based untouched.",
   "emptyFirstRun": "No minor guardian age-based configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMinorGuardianAge",
    "contract": "marketing-crm",
    "purpose": "Minor, Guardian & Age-Based Privacy Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-029",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-029"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 8 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-030",
  "name": "Privacy Configuration Testing, Approval & Publication",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Privacy__Consent___Preference_Management_Reference.pdf",
   "board": "1",
   "number": "17.1.10",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/privacy-configuration-testing-approval-publication-cms-030",
   "component": "apps/venue-management-web/src/routes/policy/PrivacyConfigurationTestingApprovalPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-021"
   ],
   "exitTo": [
    "CMS-021"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-021, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "live customer journeys. Board 1 — Final Screen Register # Backend Screen Core Responsibility 17.1. Privacy & Consent Configuration Command",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Detect configuration problems such as; Central configuration) and no display directory — it is settings, not a population",
  "purpose": "Act as the final governance gate before privacy configurations are deployed into production. No major privacy configuration should move directly from editing to production without validation. Board 1 defines what TICVAI's privacy rules are. Board 2 manages what happens after those rules are live and customers begin interacting with them.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen; 2 are served since the writers pass (29 September): Publish Now, Schedule Publication by `setPrivacyNoticePolicyGovernance`.** Still unserved: Selected Tenant, Selected Brand, Selected Country, Selected Channel. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Support"
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
       "label": "Country",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer age",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer status",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Existing consents",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Existing policy acceptance",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Requested processing",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Missing policy",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "Missing consent mapping",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "Missing language",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "Conflicting consent rules",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "Missing processing purpose",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "Invalid effective dates",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "Unmapped tracking technology",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "Missing guardian rule",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "Unpublished dependency",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "Circular configuration dependency",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Detect configuration problems such as"
      },
      {
       "kind": "selectField",
       "label": "1 Center",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Central configuration"
      },
      {
       "kind": "selectField",
       "label": "2 Registry processed",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Central configuration"
      },
      {
       "kind": "textField",
       "label": "# Backend Screen Core Responsibility",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Central configuration"
      },
      {
       "kind": "selectField",
       "label": "3",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Central configuration"
      },
      {
       "kind": "textField",
       "label": "17.1. Communication Preference & Marketing Marketing/channel",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Central configuration"
      },
      {
       "kind": "textField",
       "label": "4 Permission Configuration permissions",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Central configuration"
      },
      {
       "kind": "selectField",
       "label": "17.1. Cookie/SDK/tracker",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Central configuration"
      },
      {
       "kind": "textField",
       "label": "Cookie, Tracking & Digital Technology Registry",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Central configuration"
      },
      {
       "kind": "selectField",
       "label": "5 inventory",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Central configuration"
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
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule Publication",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Tenant",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Brand",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Country",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Channel",
       "provenance": "pack Privacy__Consent___Preference_Management_Reference.pdf, page 16 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save privacy notice policy governance",
       "operation": "setPrivacyNoticePolicyGovernance",
       "permission": "GUEST_MANAGE",
       "notes": "**An upsert keyed on `policyId`: one row per version of one privacy document.** The document itself is white-label's `Policy` (`setPolicy`, never overwritten); this row is what the privacy administrator decides about that version, and is what `listPrivacyNoticePolicy` shows beside it.",
       "provenance": "contract marketing-crm.yaml PUT /privacy-notice-policy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The privacy testing approval configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the privacy testing approval untouched.",
   "emptyFirstRun": "No privacy testing approval configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approvePrivacyTesting",
    "contract": "marketing-crm",
    "purpose": "Privacy Configuration Testing, Approval & Publication",
    "trigger": "onAction"
   },
   {
    "operationId": "setPrivacyNoticePolicyGovernance",
    "contract": "marketing-crm",
    "purpose": "Set the privacy governance of one version of a privacy document",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-030",
   "workshopBoard": "wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-030"
  },
  "apisNote": "Regenerated 9 September 2026 from Privacy__Consent___Preference_Management_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 40 of 118 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPrivacyNoticePolicyGovernance",
    "component": "modal",
    "trigger": "Save privacy notice policy governance",
    "body": "**Collects what `setPrivacyNoticePolicyGovernance` sends before it is called.** Required: `id`, `policyId`, `documentType`, `status`. Optional: `changeClassification`, `requiresReAcceptance`, `requiresNotification`, `ownerPrincipalId`, `approvedByPrincipalId`, `approvalRequestId`, `approvedAt`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PrivacyNoticeGovernance",
    "confirm": {
     "label": "Save privacy notice policy governance",
     "operation": "setPrivacyNoticePolicyGovernance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "policyId",
      "documentType",
      "status",
      "changeClassification",
      "requiresReAcceptance",
      "requiresNotification",
      "ownerPrincipalId",
      "approvedByPrincipalId",
      "approvalRequestId",
      "approvedAt",
      "scopePath"
     ]
    },
    "provenance": "contract marketing-crm.yaml PUT /privacy-notice-policy"
   }
  ],
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
 "approvePrivacyTesting": {
  "method": "PUT",
  "path": "/privacy-testing",
  "contract": "marketing-crm",
  "summary": "Privacy Configuration Testing, Approval & Publication",
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
  "requestBody": "PrivacyConfigurationTestingApprovalPublicationInput",
  "responds": "PrivacyConfigurationTestingApprovalPublicationView"
 },
 "listCookieBannerPreference": {
  "method": "GET",
  "path": "/cookie-banner-preference",
  "contract": "marketing-crm",
  "summary": "Cookie Banner & Preference Center Designer",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
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
 "listCookieScanPolicies": {
  "method": "GET",
  "path": "/cookie-scan-policy",
  "contract": "marketing-crm",
  "summary": "Scan schedules per channel",
  "permission": "GUEST_VIEW",
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
 "listCookieScans": {
  "method": "GET",
  "path": "/cookie-tracking-digital/scans",
  "contract": "marketing-crm",
  "summary": "Scan runs and what each found",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
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
 "listCookieTrackingDigital": {
  "method": "GET",
  "path": "/cookie-tracking-digital",
  "contract": "marketing-crm",
  "summary": "Cookie, Tracking & Digital Technology Registry",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "technologyType",
    "in": "query",
    "required": false
   },
   {
    "name": "category",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
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
 "listCustomerPrivacyConsent": {
  "method": "GET",
  "path": "/customer-privacy-consent",
  "contract": "marketing-crm",
  "summary": "Customer Privacy, Consent & Preference 360°",
  "permission": "GUEST_VIEW_PII",
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
    "name": "subjectId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "CustomerPrivacyConsentPreference360View"
 },
 "listDataProcessingPurpose": {
  "method": "GET",
  "path": "/data-processing-purpose",
  "contract": "marketing-crm",
  "summary": "Data Processing Purpose & Lawful Basis Registry",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "lawfulBasis",
    "in": "query",
    "required": false
   },
   {
    "name": "sensitiveOnly",
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
 "listPrivacyConsent": {
  "method": "GET",
  "path": "/privacy-consent",
  "contract": "marketing-crm",
  "summary": "Privacy & Consent Configuration Command Center",
  "permission": "GUEST_VIEW",
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
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "consentPurpose",
    "in": "query",
    "required": false
   },
   {
    "name": "policyId",
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
    "name": "effectiveFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "effectiveTo",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "PrivacyConsentConfigurationCommandCenterView"
 },
 "listPrivacyNoticePolicy": {
  "method": "GET",
  "path": "/privacy-notice-policy",
  "contract": "marketing-crm",
  "summary": "Privacy Notice, Policy & Terms Version Management",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "documentType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "language",
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
 "recordCookieScan": {
  "method": "POST",
  "path": "/cookie-tracking-digital/scans",
  "contract": "marketing-crm",
  "summary": "Take in the result of a site or app scan",
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
  "requestBody": "RecordCookieScanRequest",
  "responds": null
 },
 "setCommunicationPreferenceMarketing": {
  "method": "PUT",
  "path": "/communication-preference-marketing",
  "contract": "marketing-crm",
  "summary": "Communication Preference & Marketing Permission Configuration",
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
  "requestBody": "CommunicationPreferenceMarketingPermissionConfiguratInput",
  "responds": "CommunicationPreferenceMarketingPermissionConfiguratView"
 },
 "setConsentCapturePoint": {
  "method": "PUT",
  "path": "/consent-capture-point",
  "contract": "marketing-crm",
  "summary": "Consent Capture Point & Customer Journey Configuration",
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
  "requestBody": "ConsentCapturePointCustomerJourneyConfigurationInput",
  "responds": "ConsentCapturePointCustomerJourneyConfigurationView"
 },
 "setConsentPurposes": {
  "method": "PUT",
  "path": "/consent-purposes",
  "contract": "marketing-crm",
  "summary": "Configure consent purposes",
  "permission": "GUEST_MANAGE",
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
  "responds": "ConsentPurposeConfig"
 },
 "setCookieBannerDesign": {
  "method": "PUT",
  "path": "/cookie-banner-preference",
  "contract": "marketing-crm",
  "summary": "Save a cookie banner design as a new version",
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
  "requestBody": "CookieBannerPreferenceCenterDesignerView",
  "responds": "CookieBannerPreferenceCenterDesignerView"
 },
 "setCookieScanPolicy": {
  "method": "PUT",
  "path": "/cookie-scan-policy",
  "contract": "marketing-crm",
  "summary": "Set how often a channel is scanned and who is alerted",
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
  "requestBody": "CookieScanPolicy",
  "responds": "CookieScanPolicy"
 },
 "setMinorGuardianAge": {
  "method": "PUT",
  "path": "/minor-guardian-age",
  "contract": "marketing-crm",
  "summary": "Minor, Guardian & Age-Based Privacy Configuration",
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
  "requestBody": "MinorGuardianAgeBasedPrivacyConfigurationInput",
  "responds": "MinorGuardianAgeBasedPrivacyConfigurationView"
 },
 "setPrivacyNoticePolicyGovernance": {
  "method": "PUT",
  "path": "/privacy-notice-policy",
  "contract": "marketing-crm",
  "summary": "Set the privacy governance of one version of a privacy document",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "PrivacyNoticeGovernance",
  "responds": "PrivacyNoticeGovernance"
 },
 "setTrackingTechnology": {
  "method": "PUT",
  "path": "/cookie-tracking-digital",
  "contract": "marketing-crm",
  "summary": "Add, classify or retire a tracking technology",
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
  "requestBody": "CookieTrackingDigitalTechnologyRegistryView",
  "responds": "CookieTrackingDigitalTechnologyRegistryView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CommunicationPreferenceMarketingPermissionConfiguratInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "One communication preference category, as the privacy administrator defines it (pack 17.1.4 Configuration).",
  "required": [
   "categoryCode",
   "name",
   "classification",
   "availableChannels",
   "defaultBehavior",
   "customerEditable"
  ],
  "properties": {
   "categoryCode": {
    "type": "string",
    "maxLength": 60,
    "description": "The natural key, e.g. `orderConfirmation`, `promotions`, `birthdayCampaigns`."
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "description": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "classification": {
    "type": "string",
    "enum": [
     "transactional",
     "marketing"
    ],
    "description": "The pack's critical principle. Decides whether consent is needed at all."
   },
   "communicationType": {
    "type": "string",
    "enum": [
     "orderConfirmation",
     "ticketDelivery",
     "paymentInformation",
     "eventChanges",
     "securityMessages",
     "promotions",
     "newEvents",
     "membershipOffers",
     "loyaltyOffers",
     "birthdayCampaigns",
     "partnerOffers",
     "surveys",
     "other"
    ]
   },
   "consentPurpose": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ConsentPurpose"
     }
    ],
    "nullable": true,
    "description": "Required for `marketing`. The purpose whose consent a send checks first."
   },
   "availableChannels": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "applicableBrandIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Empty means every brand of the tenant."
   },
   "applicableCountries": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{2}$"
    },
    "description": "Empty means every country."
   },
   "customerEditable": {
    "type": "boolean",
    "description": "Whether the guest may change it in the preference centre."
   },
   "defaultBehavior": {
    "type": "string",
    "enum": [
     "on",
     "off"
    ],
    "description": "`off` for every `marketing` category (opt-in)."
   },
   "reconfirmAfterMonths": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Ask the guest again after this long; null never."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "retired"
    ],
    "default": "active"
   }
  }
 },
 "CommunicationPreferenceMarketingPermissionConfiguratView": {
  "x-ticvai-persistence": "marketing.communication_preference_type",
  "description": "A stored communication preference category.",
  "allOf": [
   {
    "$ref": "#/components/schemas/CommunicationPreferenceMarketingPermissionConfiguratInput"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true
     },
     "version": {
      "type": "integer",
      "minimum": 1,
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
   }
  ]
 },
 "ConsentCapturePointCustomerJourneyConfigurationInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "One capture point's journey configuration (pack 17.1.7 Journey Configuration).",
  "required": [
   "capturePoint",
   "channel",
   "steps"
  ],
  "properties": {
   "capturePoint": {
    "type": "string",
    "enum": [
     "accountRegistration",
     "guestCheckout",
     "ticketPurchase",
     "membershipEnrolment",
     "annualPassEnrolment",
     "mobileAppRegistration",
     "posCustomerCreation",
     "kiosk",
     "crmCustomerCreation",
     "walletEnrolment",
     "faceEnrolment",
     "newsletterSignup",
     "customerPortal",
     "competitionPromotion",
     "apiPartnerJourney"
    ]
   },
   "channel": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "customerType": {
    "type": "string",
    "enum": [
     "individual",
     "member",
     "corporate",
     "group",
     "school"
    ],
    "nullable": true
   },
   "steps": {
    "type": "array",
    "minItems": 1,
    "maxItems": 20,
    "items": {
     "type": "object",
     "required": [
      "stepKind",
      "displayOrder",
      "mandatory"
     ],
     "properties": {
      "stepKind": {
       "type": "string",
       "enum": [
        "privacyNotice",
        "terms",
        "consent",
        "preferences"
       ]
      },
      "displayOrder": {
       "type": "integer",
       "minimum": 1
      },
      "processingPurposeCode": {
       "type": "string",
       "nullable": true
      },
      "policyKind": {
       "type": "string",
       "nullable": true,
       "description": "For a notice or terms step, the white-label policy kind shown (its current published version is shown; the guest's acceptance records that version)."
      },
      "consentPurpose": {
       "allOf": [
        {
         "$ref": "#/components/schemas/ConsentPurpose"
        }
       ],
       "nullable": true,
       "description": "For a consent step."
      },
      "preferenceCategoryCodes": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "For a preferences step, `setCommunicationPreferenceMarketing` categories."
      },
      "wording": {
       "allOf": [
        {
         "$ref": "#/components/schemas/LocalisedText"
        }
       ],
       "nullable": true,
       "description": "Consent wording shown at this step, per language."
      },
      "mandatory": {
       "type": "boolean",
       "description": "A mandatory step blocks the journey until answered; a marketing consent is never mandatory."
      },
      "showWhen": {
       "type": "string",
       "enum": [
        "always",
        "biometricEnrolmentSelected",
        "belowGuardianAge"
       ],
       "default": "always"
      }
     }
    }
   },
   "skipIfCurrentVersionAccepted": {
    "type": "boolean",
    "default": true
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 10
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "retired"
    ],
    "default": "active"
   }
  }
 },
 "ConsentCapturePointCustomerJourneyConfigurationView": {
  "x-ticvai-persistence": "marketing.consent_capture_point",
  "description": "A stored capture point and its journey, at its current version.",
  "allOf": [
   {
    "$ref": "#/components/schemas/ConsentCapturePointCustomerJourneyConfigurationInput"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version",
     "publicationStatus"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true
     },
     "version": {
      "type": "integer",
      "minimum": 1,
      "readOnly": true
     },
     "publicationStatus": {
      "type": "string",
      "enum": [
       "draft",
       "review",
       "approved",
       "published",
       "superseded"
      ],
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
   }
  ]
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
 "ConsentPurposeConfig": {
  "x-ticvai-persistence": "marketing.consent_purpose + marketing.consent_purpose_channel",
  "type": "object",
  "required": [
   "purpose",
   "channels",
   "noticeVersion",
   "isRequiredForService"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "displayName": {
    "type": "string"
   },
   "description": {
    "type": "string"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string",
    "description": "Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"
   },
   "isRequiredForService": {
    "type": "boolean",
    "description": "True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"
   },
   "expiresAfterMonths": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "ConsentSource": {
  "type": "string",
  "enum": [
   "guestApp",
   "website",
   "kiosk",
   "pos",
   "callCentre",
   "import",
   "agentRecorded",
   "cookieBanner",
   "checkout"
  ],
  "description": "`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."
 },
 "CookieBannerPreferenceCenterDesignerView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.cookie_banner_design",
  "description": "One version of a cookie banner and preference-centre design (pack 17.1.6).",
  "required": [
   "channel",
   "position",
   "languages",
   "rejectIsOneClick",
   "categories"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for the corporate design every brand inherits."
   },
   "inheritsFromId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "type": "string",
    "enum": [
     "b2cWebsite",
     "customerPortal",
     "mobileApp",
     "embeddedCheckout",
     "whiteLabelSite",
     "partnerMicrosite"
    ]
   },
   "logoAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "position": {
    "type": "string",
    "enum": [
     "top",
     "bottom",
     "popup",
     "modal"
    ]
   },
   "themeId": {
    "type": "string",
    "nullable": true,
    "description": "The white-label theme it takes colours and fonts from."
   },
   "buttons": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "action"
     ],
     "properties": {
      "action": {
       "type": "string",
       "enum": [
        "acceptAll",
        "rejectNonEssential",
        "managePreferences",
        "savePreferences",
        "doNotSellOrShare"
       ]
      },
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      }
     }
    }
   },
   "rejectIsOneClick": {
    "type": "boolean",
    "default": true,
    "description": "Must be true."
   },
   "links": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "label",
      "policyKind"
     ],
     "properties": {
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "policyKind": {
       "type": "string",
       "enum": [
        "privacy",
        "cookie",
        "termsAndConditions"
       ]
      }
     }
    }
   },
   "categories": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "category",
      "defaultOn"
     ],
     "properties": {
      "category": {
       "type": "string",
       "enum": [
        "strictlyNecessary",
        "functional",
        "analytics",
        "personalisation",
        "marketing"
       ]
      },
      "description": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "defaultOn": {
       "type": "boolean",
       "description": "True only for `strictlyNecessary`, which is always active."
      }
     }
    }
   },
   "languages": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "maxLength": 10
    },
    "description": "Every language the storefront serves; Arabic renders right to left."
   },
   "regulatoryRegimes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "gdpr",
      "ePrivacy",
      "ccpaCpra",
      "lgpd",
      "uaePdpl",
      "saudiPdpl"
     ]
    },
    "description": "2.6.60 (29 September, build). **The laws this design is published to satisfy**, so compliance is stated rather than assumed. The strictest posture (opt-in, one-click reject, every non-essential category off) already meets GDPR/ePrivacy, LGPD and both PDPLs; `ccpaCpra` adds the \"Do not sell or share\" button (`doNotSellOrShare`) and honours a Global Privacy Control signal as that opt-out."
   },
   "recordIpAddress": {
    "type": "boolean",
    "default": false,
    "description": "2.6.55, \"if legally permitted\" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. Off by default."
   },
   "noticeVersion": {
    "type": "string",
    "readOnly": true,
    "description": "Moves with the cookie policy (white-label `setPolicy`, kind `cookie`)."
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "superseded"
    ],
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
 "CookieConsentChannel": {
  "type": "string",
  "enum": [
   "b2cWebsite",
   "customerPortal",
   "mobileApp",
   "embeddedCheckout",
   "whiteLabelSite",
   "partnerMicrosite"
  ],
  "description": "The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6)."
 },
 "CookieScanPolicy": {
  "type": "object",
  "x-ticvai-persistence": "marketing.cookie_scan_policy",
  "description": "How often one channel's domain or app is scanned and who is alerted (2.6.64).",
  "required": [
   "channel",
   "frequency"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "channel": {
    "$ref": "#/components/schemas/CookieConsentChannel"
   },
   "domainApplication": {
    "type": "string",
    "maxLength": 255,
    "nullable": true
   },
   "frequency": {
    "type": "string",
    "enum": [
     "daily",
     "weekly",
     "monthly",
     false
    ]
   },
   "dayOfWeek": {
    "type": "integer",
    "minimum": 1,
    "maximum": 7,
    "nullable": true,
    "description": "ISO day, for `weekly`."
   },
   "dayOfMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 28,
    "nullable": true,
    "description": "For `monthly`."
   },
   "alertRecipientPrincipalIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "lastRunAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "nextRunAt": {
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
 "CookieScanRun": {
  "type": "object",
  "x-ticvai-persistence": "marketing.cookie_scan_run",
  "description": "One scan taken in by `recordCookieScan` (2.6.57).",
  "required": [
   "channel",
   "scannedAt",
   "source",
   "findingsCount",
   "newlyDetectedCount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "channel": {
    "$ref": "#/components/schemas/CookieConsentChannel"
   },
   "domainApplication": {
    "type": "string",
    "maxLength": 255,
    "nullable": true
   },
   "source": {
    "type": "string",
    "enum": [
     "boughtScanner",
     "ownCrawler",
     "manualUpload"
    ]
   },
   "scannerRef": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "scannedAt": {
    "type": "string",
    "format": "date-time"
   },
   "findingsCount": {
    "type": "integer",
    "minimum": 0
   },
   "newlyDetectedCount": {
    "type": "integer",
    "minimum": 0,
    "description": "What the administrator alert is raised from."
   },
   "missingCount": {
    "type": "integer",
    "minimum": 0,
    "description": "Registry entries for this channel the scan did not see."
   },
   "alertedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   }
  }
 },
 "CookieTrackingDigitalTechnologyRegistryView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.tracking_technology",
  "description": "One governed tracking technology (pack 17.1.5 Registry Fields; BL-073 §4a).",
  "required": [
   "name",
   "provider",
   "technologyType",
   "isThirdParty",
   "channels",
   "status"
  ],
  "properties": {
   "technologyId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string",
    "maxLength": 200,
    "description": "The cookie, SDK, pixel or storage key as it appears on the device."
   },
   "provider": {
    "type": "string",
    "maxLength": 150
   },
   "domainApplication": {
    "type": "string",
    "maxLength": 255,
    "nullable": true,
    "description": "The domain, or the app and version, it was found on."
   },
   "technologyType": {
    "type": "string",
    "enum": [
     "firstPartyCookie",
     "thirdPartyCookie",
     "mobileSdk",
     "analyticsTracker",
     "advertisingPixel",
     "sessionTechnology",
     "personalisationTechnology",
     "embeddedService",
     "localStorageItem",
     "other"
    ]
   },
   "category": {
    "type": "string",
    "enum": [
     "strictlyNecessary",
     "functional",
     "analytics",
     "personalisation",
     "marketing",
     "other"
    ],
    "nullable": true,
    "description": "Null until an administrator classifies it."
   },
   "otherCategoryLabel": {
    "type": "string",
    "maxLength": 80,
    "nullable": true,
    "description": "The organisation-defined category, when `category` is `other`."
   },
   "purpose": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "dataCollected": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "durationDays": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Null for session storage."
   },
   "isThirdParty": {
    "type": "boolean"
   },
   "channels": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "enum": [
      "b2cWebsite",
      "customerPortal",
      "mobileApp",
      "embeddedCheckout",
      "whiteLabelSite",
      "partnerMicrosite"
     ]
    }
   },
   "countries": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{2}$"
    },
    "description": "Empty means every country."
   },
   "processingPurposeCode": {
    "type": "string",
    "nullable": true,
    "description": "The `DataProcessingPurposeLawfulBasisRegistryView.purposeCode` it serves."
   },
   "consentRequired": {
    "type": "boolean",
    "default": true,
    "description": "False only for `strictlyNecessary`."
   },
   "privacyInformation": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true,
    "description": "What the preference centre tells the guest about it."
   },
   "source": {
    "type": "string",
    "enum": [
     "manual",
     "scan"
    ],
    "default": "manual",
    "readOnly": true
   },
   "status": {
    "type": "string",
    "enum": [
     "detected",
     "approved",
     "blocked",
     "retired"
    ],
    "description": "`detected` is treated as `blocked` until approved."
   },
   "firstDetectedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "lastSeenAt": {
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
 "CustomerPrivacyConsentPreference360View": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.guest_profile, marketing.consent_record, marketing.consent_record_channel, marketing.consent_purpose, marketing.privacy_request (new), marketing.tracking_technology, pii.subject",
  "description": "One customer's privacy position (pack 17.2.2). Consent entries are current state; history is `listConsentEvidenceWithdrawal`.",
  "required": [
   "subjectId",
   "consents",
   "policyAcceptance"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "accountStatus": {
    "type": "string",
    "enum": [
     "active",
     "guest",
     "suspended",
     "archived",
     "erased"
    ],
    "description": "`archived` and `erased` are the ADR-0047 lifecycle stages."
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true,
    "description": "BCP 47 tag."
   },
   "ageCategory": {
    "type": "string",
    "enum": [
     "adult",
     "minor",
     "unknown"
    ]
   },
   "guardianSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guardianRelationship": {
    "type": "string",
    "nullable": true,
    "enum": [
     "parent",
     "legalGuardian",
     "other"
    ]
   },
   "openExceptionCount": {
    "type": "integer",
    "minimum": 0,
    "description": "The privacy risk/exception indicator; open exceptions naming this customer."
   },
   "consents": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "channel": {
       "allOf": [
        {
         "$ref": "#/components/schemas/MessageChannel"
        }
       ],
       "nullable": true
      },
      "decision": {
       "type": "string",
       "enum": [
        "granted",
        "declined",
        "withdrawn",
        "expired",
        "notAsked"
       ]
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "capturedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "source": {
       "allOf": [
        {
         "$ref": "#/components/schemas/ConsentSource"
        }
       ],
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean"
      }
     }
    }
   },
   "preferences": {
    "type": "object",
    "properties": {
     "channels": {
      "type": "array",
      "items": {
       "type": "object",
       "required": [
        "channel",
        "optedIn"
       ],
       "properties": {
        "channel": {
         "$ref": "#/components/schemas/MessageChannel"
        },
        "optedIn": {
         "type": "boolean"
        }
       }
      }
     },
     "brandIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "marketingCategories": {
      "type": "array",
      "items": {
       "type": "string",
       "maxLength": 80
      }
     },
     "personalisationEnabled": {
      "type": "boolean"
     }
    }
   },
   "policyAcceptance": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "documentType",
      "currentVersion"
     ],
     "properties": {
      "documentType": {
       "type": "string",
       "enum": [
        "privacyPolicy",
        "cookieNotice",
        "biometricNotice",
        "childrensPrivacyNotice",
        "other"
       ]
      },
      "documentName": {
       "type": "string",
       "nullable": true
      },
      "acceptedVersion": {
       "type": "string",
       "nullable": true
      },
      "acceptedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "currentVersion": {
       "type": "string"
      },
      "requiresReacceptance": {
       "type": "boolean"
      }
     }
    }
   },
   "trackingChoices": {
    "type": "array",
    "description": "Only where the preference is tied to this customer (a signed-in consent).",
    "items": {
     "type": "object",
     "required": [
      "category",
      "decision"
     ],
     "properties": {
      "category": {
       "type": "string",
       "enum": [
        "strictlyNecessary",
        "functional",
        "analytics",
        "personalisation",
        "marketing",
        "other"
       ]
      },
      "decision": {
       "type": "string",
       "enum": [
        "granted",
        "declined"
       ]
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "privacyRequests": {
    "type": "array",
    "description": "Open requests and the 20 most recent completed ones.",
    "items": {
     "type": "object",
     "required": [
      "requestId",
      "requestType",
      "status"
     ],
     "properties": {
      "requestId": {
       "type": "string",
       "format": "uuid"
      },
      "requestType": {
       "type": "string"
      },
      "status": {
       "type": "string",
       "enum": [
        "submitted",
        "inProgress",
        "completed"
       ]
      },
      "submittedAt": {
       "type": "string",
       "format": "date-time"
      },
      "dueAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "dataFootprint": {
    "type": "array",
    "description": "Where this customer's data exists, as counts; the records are reached through `setDataDiscoveryAccess`.",
    "items": {
     "type": "object",
     "required": [
      "system",
      "recordCount"
     ],
     "properties": {
      "system": {
       "type": "string",
       "enum": [
        "crm",
        "ticketing",
        "membership",
        "orders",
        "loyalty",
        "wallet",
        "marketing",
        "waiver",
        "biometricProviderReference",
        "connectedSystem"
       ]
      },
      "systemName": {
       "type": "string",
       "nullable": true,
       "description": "The connected system's name, when `system` is `connectedSystem`."
      },
      "recordCount": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "timeline": {
    "type": "array",
    "description": "The 50 most recent privacy events, newest first.",
    "items": {
     "type": "object",
     "required": [
      "occurredAt",
      "event"
     ],
     "properties": {
      "occurredAt": {
       "type": "string",
       "format": "date-time"
      },
      "event": {
       "type": "string",
       "enum": [
        "accountCreated",
        "policyAccepted",
        "consentGranted",
        "consentDeclined",
        "consentWithdrawn",
        "preferenceChanged",
        "privacyRequestCreated",
        "privacyRequestCompleted",
        "dataExportGenerated",
        "anonymised",
        "archived"
       ]
      },
      "summary": {
       "type": "string",
       "maxLength": 300
      }
     }
    }
   }
  }
 },
 "DataProcessingPurposeLawfulBasisRegistryView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.processing_purpose",
  "description": "One processing purpose in the tenant's register (pack 17.1.2). The lawful basis is the privacy administrator's classification, never the platform's.",
  "required": [
   "purposeCode",
   "purposeName",
   "lawfulBasis",
   "status"
  ],
  "properties": {
   "purposeId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "purposeCode": {
    "type": "string",
    "maxLength": 60,
    "description": "The natural key, e.g. `ticketPurchase`, `marketingCommunication`."
   },
   "purposeName": {
    "type": "string",
    "maxLength": 150
   },
   "description": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true
   },
   "businessOwner": {
    "type": "string",
    "maxLength": 150,
    "nullable": true,
    "description": "The accountable team or person."
   },
   "dataControllerApplicableOrganization": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "The legal entity acting as controller for this purpose."
   },
   "dataCategories": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 80
    },
    "description": "e.g. contact details, payment, date of birth, images."
   },
   "dataSubjectCategories": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "guest",
      "member",
      "minor",
      "guardian",
      "partner",
      "employee",
      "other"
     ]
    }
   },
   "processingActivities": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 150
    }
   },
   "systemsModules": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
    }
   },
   "countriesJurisdictions": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{2}$"
    }
   },
   "lawfulBasis": {
    "type": "string",
    "enum": [
     "consent",
     "contractualNecessity",
     "legalObligation",
     "legitimateInterest",
     "vitalInterest",
     "publicInterest",
     "other",
     "unclassified"
    ],
    "default": "unclassified",
    "description": "Set by the privacy administrator. `unclassified` is flagged, never assumed."
   },
   "lawfulBasisNote": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Required when `lawfulBasis` is `other`."
   },
   "sensitiveCategories": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "biometrics",
      "childrensData",
      "identityDocuments",
      "preciseLocation",
      "health",
      "other"
     ]
    }
   },
   "consentPurposes": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ConsentPurpose"
    },
    "description": "The consent purposes that rely on this processing purpose."
   },
   "policyIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Notices and policies that describe it (white-label `listPolicies`)."
   },
   "capturePointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "retentionPolicyCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "`DataRetentionPolicy.code` values that govern its data."
   },
   "thirdPartyProcessors": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 150
    }
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
     "active",
     "retired"
    ],
    "default": "draft"
   },
   "version": {
    "type": "integer",
    "minimum": 1,
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
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
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
 "MinorGuardianAgeBasedPrivacyConfigurationInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "One jurisdiction's age and guardian rule (pack 17.1.9 Age Rules, Guardian Verification).",
  "required": [
   "country",
   "minorBelowAge",
   "guardianRequiredBelowAge",
   "ageVerificationMethod",
   "guardianVerificationMethods"
  ],
  "properties": {
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "description": "The jurisdiction the rule applies to."
   },
   "minorBelowAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 25,
    "description": "A guest younger than this is a minor. Set by the tenant; no default."
   },
   "guardianRequiredBelowAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 25,
    "description": "A guardian must give privacy consent for a guest younger than this. Not above `minorBelowAge`."
   },
   "ageVerificationMethod": {
    "type": "string",
    "enum": [
     "selfDeclaredDateOfBirth",
     "identityDocument",
     "staffVerification",
     "accountRecord"
    ]
   },
   "guardianVerificationMethods": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "enum": [
      "emailOtp",
      "smsOtp",
      "accountAuthentication",
      "staffVerification",
      "otherApproved"
     ]
    }
   },
   "guardianDataRequired": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "name",
      "relationship",
      "email",
      "mobile"
     ]
    },
    "description": "What is captured about the guardian."
   },
   "restrictMarketing": {
    "type": "boolean",
    "default": true,
    "description": "No marketing to a minor, whatever consent is given."
   },
   "restrictTracking": {
    "type": "boolean",
    "default": true
   },
   "restrictPersonalisation": {
    "type": "boolean",
    "default": true
   },
   "restrictedProcessingPurposeCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Further processing purposes refused for minors (e.g. biometrics without guardian consent)."
   },
   "consentPurposesRequiringGuardian": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ConsentPurpose"
    }
   }
  }
 },
 "MinorGuardianAgeBasedPrivacyConfigurationView": {
  "x-ticvai-persistence": "marketing.minor_privacy_rule",
  "description": "A stored jurisdiction age rule.",
  "allOf": [
   {
    "$ref": "#/components/schemas/MinorGuardianAgeBasedPrivacyConfigurationInput"
   },
   {
    "type": "object",
    "required": [
     "id"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true
     },
     "version": {
      "type": "integer",
      "minimum": 1,
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
 "PrivacyConfigurationTestingApprovalPublicationInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "One action on a privacy change set (pack 17.1.10).",
  "required": [
   "action"
  ],
  "properties": {
   "changeSetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null on the first action, which opens a change set."
   },
   "action": {
    "type": "string",
    "enum": [
     "simulate",
     "validate",
     "submit",
     "publish",
     "rollback"
    ]
   },
   "items": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "configurationType",
      "configurationId"
     ],
     "properties": {
      "configurationType": {
       "type": "string",
       "enum": [
        "processingPurpose",
        "consentPurpose",
        "communicationPreference",
        "capturePoint",
        "cookieBanner",
        "trackingTechnology",
        "minorPrivacyRule",
        "privacyNotice"
       ]
      },
      "configurationId": {
       "type": "string",
       "format": "uuid"
      },
      "version": {
       "type": "integer",
       "minimum": 1
      }
     }
    },
    "description": "The draft versions in the change set. Required when the set is opened."
   },
   "scenario": {
    "type": "object",
    "description": "For `simulate` (the pack's Test Inputs).",
    "properties": {
     "country": {
      "type": "string",
      "pattern": "^[A-Z]{2}$"
     },
     "brandId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "channel": {
      "$ref": "#/components/schemas/ConsentSource"
     },
     "capturePoint": {
      "type": "string",
      "nullable": true
     },
     "customerAge": {
      "type": "integer",
      "minimum": 0,
      "nullable": true
     },
     "customerStatus": {
      "type": "string",
      "enum": [
       "new",
       "returning",
       "member"
      ]
     },
     "productId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "existingConsents": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ConsentPurpose"
      }
     },
     "acceptedPolicyVersions": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "language": {
      "type": "string",
      "maxLength": 10
     }
    }
   },
   "publishAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "For `publish`; null publishes now."
   },
   "target": {
    "type": "object",
    "description": "For `publish`; an empty list means all.",
    "properties": {
     "brandIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "countries": {
      "type": "array",
      "items": {
       "type": "string",
       "pattern": "^[A-Z]{2}$"
      }
     },
     "channels": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ConsentSource"
      }
     }
    }
   },
   "reason": {
    "type": "string",
    "maxLength": 1000,
    "description": "Required for `submit`, `publish` and `rollback`."
   }
  }
 },
 "PrivacyConfigurationTestingApprovalPublicationView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.privacy_change_set",
  "description": "A privacy change set, its validation, approval, publication and audit trail.",
  "required": [
   "changeSetId",
   "status"
  ],
  "properties": {
   "changeSetId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "validated",
     "submitted",
     "approved",
     "scheduled",
     "published",
     "rolledBack",
     "rejected"
    ]
   },
   "items": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "configurationType": {
       "type": "string"
      },
      "configurationId": {
       "type": "string",
       "format": "uuid"
      },
      "version": {
       "type": "integer"
      }
     }
    }
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "code"
     ],
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "missingPolicy",
        "missingConsentMapping",
        "missingLanguage",
        "conflictingConsentRules",
        "missingProcessingPurpose",
        "invalidEffectiveDates",
        "unmappedTrackingTechnology",
        "missingGuardianRule",
        "unpublishedDependency",
        "circularDependency"
       ]
      },
      "configurationId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "simulation": {
    "type": "array",
    "description": "What the scenario's guest would be shown, step by step (from `simulate`; not stored).",
    "items": {
     "type": "object",
     "required": [
      "item",
      "outcome"
     ],
     "properties": {
      "item": {
       "type": "string",
       "description": "e.g. \"Privacy Notice v5.1\", \"Email Marketing\"."
      },
      "outcome": {
       "type": "string",
       "enum": [
        "display",
        "consentRequired",
        "optional",
        "noConsentRequired",
        "notApplicable",
        "guardianFlow"
       ]
      },
      "lawfulBasis": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "approvalRequestId": {
    "type": "string",
    "nullable": true,
    "description": "The approvals-engine request, once submitted."
   },
   "publishAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "audit": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "action",
      "byPrincipalId",
      "at"
     ],
     "properties": {
      "action": {
       "type": "string"
      },
      "byPrincipalId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string",
       "nullable": true
      },
      "before": {
       "type": "object",
       "additionalProperties": true,
       "nullable": true
      },
      "after": {
       "type": "object",
       "additionalProperties": true,
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
 "PrivacyConsentConfigurationCommandCenterView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.consent_purpose, marketing.consent_capture_point (new), marketing.communication_preference_type (new), the cookie categories and white-label's whitelabel.policy (read through listPolicies)",
  "description": "The privacy command centre's figures for the filters given, and the latest configuration changes. Counts are of items currently in force unless the name says otherwise.",
  "required": [
   "activeConsentPurposes",
   "activePrivacyPolicies",
   "pendingPolicyApprovals",
   "configurationWarnings",
   "configurationDirectory"
  ],
  "properties": {
   "activeConsentPurposes": {
    "type": "integer",
    "minimum": 0
   },
   "activePrivacyPolicies": {
    "type": "integer",
    "minimum": 0
   },
   "communicationPreferenceTypes": {
    "type": "integer",
    "minimum": 0
   },
   "cookieCategories": {
    "type": "integer",
    "minimum": 0
   },
   "activeConsentCapturePoints": {
    "type": "integer",
    "minimum": 0
   },
   "supportedLanguages": {
    "type": "integer",
    "minimum": 0
   },
   "pendingPolicyApprovals": {
    "type": "integer",
    "minimum": 0
   },
   "scheduledPolicyChanges": {
    "type": "integer",
    "minimum": 0,
    "description": "Published items with an `effectiveFrom` still in the future."
   },
   "consentConfigurationsRequiringReview": {
    "type": "integer",
    "minimum": 0,
    "description": "Items in `review`, or whose reconfirmation interval has passed."
   },
   "configurationWarnings": {
    "type": "array",
    "maxItems": 100,
    "description": "Configuration checks that failed, most severe first.",
    "items": {
     "type": "object",
     "required": [
      "code",
      "message"
     ],
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "capturePointWithoutNotice",
        "purposeWordingDiffersByChannel",
        "purposeWithoutLawfulBasis",
        "translationMissing",
        "policyExpired",
        "other"
       ]
      },
      "message": {
       "type": "string"
      },
      "configurationType": {
       "type": "string",
       "nullable": true
      },
      "configurationId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "configurationDirectory": {
    "type": "array",
    "maxItems": 50,
    "description": "The 50 most recently changed configuration items, newest `effectiveFrom` first.",
    "items": {
     "type": "object",
     "required": [
      "configurationType",
      "configurationId",
      "name",
      "version",
      "status"
     ],
     "properties": {
      "configurationType": {
       "type": "string",
       "enum": [
        "consentPurpose",
        "privacyPolicy",
        "cookieCategory",
        "capturePoint",
        "communicationPreference",
        "minorPrivacy"
       ]
      },
      "configurationId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "scope": {
       "type": "string",
       "description": "Where it applies, as the scope path's label (a brand, country or channel)."
      },
      "version": {
       "type": "string"
      },
      "effectiveFrom": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "status": {
       "type": "string",
       "enum": [
        "draft",
        "review",
        "approved",
        "scheduled",
        "published",
        "retired"
       ]
      }
     }
    }
   }
  }
 },
 "PrivacyNoticeGovernance": {
  "type": "object",
  "x-ticvai-persistence": "marketing.privacy_notice_governance",
  "description": "**The privacy governance of one version of one privacy document.** The document itself is white-label's `Policy` (`setPolicy`, never overwritten); this row adds what the privacy administrator decides about it: lifecycle status, the change classification (set by an authorised user, **never by AI**), re-acceptance and notification, owner and approval. One row per policy version. Read by `listPrivacyNoticePolicy`; written by `setPrivacyNoticePolicyGovernance` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n",
  "required": [
   "id",
   "policyId",
   "documentType",
   "status"
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
    "description": "The white-label `Policy` version this governs (`documentId` on the view)."
   },
   "documentType": {
    "type": "string",
    "enum": [
     "privacyPolicy",
     "privacyNotice",
     "cookieNotice",
     "marketingNotice",
     "biometricPrivacyNotice",
     "childrensPrivacyNotice",
     "locationServicesNotice",
     "other"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "review",
     "approved",
     "scheduled",
     "published",
     "superseded",
     "archived"
    ],
    "default": "draft"
   },
   "changeClassification": {
    "type": "string",
    "enum": [
     "minor",
     "material"
    ],
    "nullable": true,
    "description": "Set by an authorised user, never by AI."
   },
   "requiresReAcceptance": {
    "type": "boolean",
    "default": false
   },
   "requiresNotification": {
    "type": "boolean",
    "default": false
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The approvals request raised when the row entered `review` (`setPrivacyNoticePolicyGovernance`); its decision stamps `approvedByPrincipalId` and `approvedAt`. (decided 29 September, writers pass)"
   },
   "approvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "PrivacyNoticePolicyTermsVersionManagementView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over whitelabel.policy (read through white-label listPolicies), marketing.privacy_notice_governance and marketing.consent_record",
  "description": "One version of one privacy document, with its governance (pack 17.1.8 Version Information).",
  "required": [
   "documentId",
   "documentType",
   "version",
   "status"
  ],
  "properties": {
   "documentId": {
    "type": "string",
    "format": "uuid"
   },
   "documentType": {
    "type": "string",
    "enum": [
     "privacyPolicy",
     "privacyNotice",
     "cookieNotice",
     "marketingNotice",
     "biometricPrivacyNotice",
     "childrensPrivacyNotice",
     "locationServicesNotice",
     "other"
    ]
   },
   "title": {
    "type": "string"
   },
   "version": {
    "type": "string"
   },
   "language": {
    "type": "string",
    "maxLength": 10
   },
   "owner": {
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
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "review",
     "approved",
     "scheduled",
     "published",
     "superseded",
     "archived"
    ]
   },
   "changeClassification": {
    "type": "string",
    "enum": [
     "minor",
     "material"
    ],
    "nullable": true,
    "description": "Set by an authorised user, never by AI."
   },
   "requiresReAcceptance": {
    "type": "boolean",
    "description": "Guests are asked to accept this version at their next capture point."
   },
   "requiresNotification": {
    "type": "boolean",
    "description": "Guests are told of the change by a transactional message."
   },
   "acceptedCount": {
    "type": "integer",
    "minimum": 0,
    "description": "Guests whose recorded acceptance is of this version."
   }
  }
 },
 "RecordCookieScanRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "scannedAt",
   "channel",
   "findings"
  ],
  "properties": {
   "scannedAt": {
    "type": "string",
    "format": "date-time"
   },
   "channel": {
    "$ref": "#/components/schemas/CookieConsentChannel"
   },
   "domainApplication": {
    "type": "string",
    "maxLength": 255,
    "nullable": true,
    "description": "The domain, or the app and version, scanned."
   },
   "scannerRef": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "The vendor and scan id where the scanner is bought; null for ours or a manual upload."
   },
   "findings": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "name",
      "provider",
      "technologyType",
      "isThirdParty"
     ],
     "properties": {
      "name": {
       "type": "string",
       "maxLength": 200
      },
      "provider": {
       "type": "string",
       "maxLength": 150
      },
      "technologyType": {
       "type": "string",
       "enum": [
        "firstPartyCookie",
        "thirdPartyCookie",
        "mobileSdk",
        "analyticsTracker",
        "advertisingPixel",
        "sessionTechnology",
        "personalisationTechnology",
        "embeddedService",
        "localStorageItem",
        "other"
       ]
      },
      "isThirdParty": {
       "type": "boolean"
      },
      "durationDays": {
       "type": "integer",
       "minimum": 0,
       "nullable": true
      },
      "domainApplication": {
       "type": "string",
       "maxLength": 255,
       "nullable": true
      }
     }
    }
   }
  }
 }
}
```
