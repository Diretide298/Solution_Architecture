# WS24 — Communication & Notification Platform Services board 1

**10 screens · 10 operations · 12 schemas · 2 permissions**

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
| `ADM-038` | Communication Service Command Center | listDetail | 1 | 0 | — |
| `ADM-039` | Channel & Provider Configuration | configEditor | 1 | 0 | — |
| `ADM-040` | Sender Identity, Domain & Brand Configuration | configEditor | 1 | 0 | — |
| `ADM-041` | System Transactional Template Registry | configEditor | 1 | 0 | — |
| `ADM-042` | Business Event & Notification Trigger Mapping | listDetail | 1 | 0 | — |
| `ADM-043` | Routing, Priority, Throttling & Fallback Rules | configEditor | 1 | 0 | — |
| `ADM-044` | Consent, Preference & Communication Policy Enforcement | listDetail | 1 | 0 | — |
| `ADM-045` | Delivery Queue, Failure & Retry Management | listDetail | 1 | 0 | — |
| `ADM-046` | Provider Health, Usage & Cost Monitoring | listDetail | 1 | 0 | — |
| `ADM-047` | AI Delivery Optimization & Communication Platform Diagnostics | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-038, ADM-044, ADM-045, ADM-047 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-038",
  "name": "Communication Service Command Center",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.1",
   "page": 4
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/communication-service-command-center-adm-038",
   "component": "apps/ticvai-web/src/routes/platform/CommunicationServiceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-039",
    "ADM-040",
    "ADM-041",
    "ADM-042",
    "ADM-043",
    "ADM-044",
    "ADM-045",
    "ADM-046",
    "ADM-047"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-039",
     "trigger": "Works in Channel & Provider Configuration",
     "provenance": "flow F133 step 1→2",
     "operation": "listCommunicationService"
    },
    {
     "to": "ADM-040",
     "trigger": "Works in Sender Identity, Domain & Brand Configuration",
     "provenance": "flow F133 step 3→4",
     "operation": "listCommunicationService"
    },
    {
     "to": "ADM-041",
     "trigger": "Works in System Transactional Template Registry",
     "provenance": "flow F133 step 5→6",
     "operation": "listCommunicationService"
    },
    {
     "to": "ADM-042",
     "trigger": "Works in Business Event & Notification Trigger Mapping",
     "provenance": "flow F133 step 7→8",
     "operation": "listCommunicationService"
    },
    {
     "to": "ADM-043",
     "trigger": "Works in Routing, Priority, Throttling & Fallback Rules",
     "provenance": "flow F133 step 9→10",
     "operation": "listCommunicationService"
    },
    {
     "to": "ADM-044",
     "trigger": "Works in Consent, Preference & Communication Policy Enforcement",
     "provenance": "flow F133 step 11→12",
     "operation": "listCommunicationService"
    },
    {
     "to": "ADM-045",
     "trigger": "Works in Delivery Queue, Failure & Retry Management",
     "provenance": "flow F133 step 13→14",
     "operation": "listCommunicationService"
    },
    {
     "to": "ADM-046",
     "trigger": "Works in Provider Health, Usage & Cost Monitoring",
     "provenance": "flow F133 step 15→16",
     "operation": "listCommunicationService"
    },
    {
     "to": "ADM-047",
     "trigger": "Works in AI Delivery Optimization & Communication Platform Diagnostics",
     "provenance": "flow F133 step 17→18",
     "operation": "listCommunicationService"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide administrators and technical/operations teams with a centralized view of the health and activity of TICVAI's communication infrastructure. This is not a marketing dashboard.",
  "purposeNote": "Platform administrators can understand communication volume, delivery health, provider performance and operational exceptions from one centralized workspace.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every communication service",
       "columns": [
        "CommunicationServiceCommandCenterView.messagesProcessedToday",
        "CommunicationServiceCommandCenterView.emailSent",
        "CommunicationServiceCommandCenterView.smsSent",
        "CommunicationServiceCommandCenterView.whatsappSent",
        "CommunicationServiceCommandCenterView.pushNotifications",
        "CommunicationServiceCommandCenterView.inAppNotifications",
        "CommunicationServiceCommandCenterView.delivered",
        "CommunicationServiceCommandCenterView.failed",
        "CommunicationServiceCommandCenterView.pending",
        "CommunicationServiceCommandCenterView.retrying",
        "CommunicationServiceCommandCenterView.averageDeliveryTime",
        "CommunicationServiceCommandCenterView.providerAvailability"
       ],
       "bindsTo": "CommunicationServiceCommandCenterView",
       "operation": "listCommunicationService",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 4 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected communication service",
       "bindsTo": "CommunicationServiceCommandCenterView",
       "columns": [
        "CommunicationServiceCommandCenterView.messagesProcessedToday",
        "CommunicationServiceCommandCenterView.emailSent",
        "CommunicationServiceCommandCenterView.smsSent",
        "CommunicationServiceCommandCenterView.whatsappSent",
        "CommunicationServiceCommandCenterView.pushNotifications",
        "CommunicationServiceCommandCenterView.inAppNotifications",
        "CommunicationServiceCommandCenterView.delivered",
        "CommunicationServiceCommandCenterView.failed",
        "CommunicationServiceCommandCenterView.pending",
        "CommunicationServiceCommandCenterView.retrying",
        "CommunicationServiceCommandCenterView.averageDeliveryTime",
        "CommunicationServiceCommandCenterView.providerAvailability"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Module Activity”, “Channel Provider Health”, “Health”, “WhatsAp Warni”.",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 4 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The communication service list.",
   "error": "Could not load. Names which read failed and leaves the communication service untouched.",
   "emptyFirstRun": "No communication service yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the communication service are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommunicationService",
    "contract": "marketing-crm",
    "purpose": "Communication Service Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CommunicationServiceCommandCenterView.messagesProcessedToday",
    "CommunicationServiceCommandCenterView.emailSent",
    "CommunicationServiceCommandCenterView.smsSent",
    "CommunicationServiceCommandCenterView.whatsappSent",
    "CommunicationServiceCommandCenterView.pushNotifications",
    "CommunicationServiceCommandCenterView.inAppNotifications"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-038"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 4. 12 of 12 labels bound to a contract property; 12 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-039",
  "name": "Channel & Provider Configuration",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.2",
   "page": 6
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/channel-provider-configuration-adm-039",
   "component": "apps/ticvai-web/src/routes/platform/ChannelProviderConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-038"
   ],
   "exitTo": [
    "ADM-038"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-038, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-038",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F133 step 2→3",
     "operation": "setChannelProvider"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the external/internal services used by TICVAI to deliver communications.",
  "purposeNote": "Authorized administrators can configure and test multiple communication providers without requiring individual TICVAI modules to maintain direct provider integrations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Test Connection, Send Test Message, Validate Credentials, Test Webhook, Verify Delivery Receipt. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Actions"
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
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "SMS",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "WhatsApp",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mobile Push",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "In-App Notification",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Future supported channels",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Test Connection",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Send Test Message",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate Credentials",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Test Webhook",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify Delivery Receipt",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel provider configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel provider untouched.",
   "emptyFirstRun": "No channel provider configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setChannelProvider",
    "contract": "marketing-crm",
    "purpose": "Channel & Provider Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setChannelProvider"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-039"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 11 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-040",
  "name": "Sender Identity, Domain & Brand Configuration",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.3",
   "page": 7
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/sender-identity-domain-brand-configuration-adm-040",
   "component": "apps/ticvai-web/src/routes/platform/SenderIdentityDomainBrandConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-038"
   ],
   "exitTo": [
    "ADM-038"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-038, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-038",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F133 step 4→5",
     "operation": "setSenderIdentityDomain"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Manage the identities from which TICVAI communications are sent.",
  "purposeNote": "Every outbound communication uses a verified and appropriately governed sender identity for the applicable brand, channel and region.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Sending Domain",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "From Name",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "From Address",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reply-To",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Region",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sender ID",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approved Use",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Application",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Platform",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Environment",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business Account",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Phone Number",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Verification Status",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Approved Templates",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 7 §Configure/reference"
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
       "provenance": "contract operation setSenderIdentityDomain"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sender identity domain configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the sender identity domain untouched.",
   "emptyFirstRun": "No sender identity domain configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSenderIdentityDomain",
    "contract": "marketing-crm",
    "purpose": "Sender Identity, Domain & Brand Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setSenderIdentityDomain"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-040"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 19 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-041",
  "name": "System Transactional Template Registry",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.4",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/system-transactional-template-registry-adm-041",
   "component": "apps/ticvai-web/src/routes/platform/SystemTransactionalTemplateRegistry.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-038"
   ],
   "exitTo": [
    "ADM-038"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-038, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-038",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F133 step 6→7",
     "operation": "listSystemTransactionalTemplate"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Maintain centralized system/transactional communication templates used by TICVAI operational modules. This screen must not replace CRM's marketing template builder.",
  "purposeNote": "Operational modules can use governed reusable communication templates without embedding message content directly in application code.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Template ID",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Template Name",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business Event",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Source Module",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Version",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The system transactional template configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the system transactional template untouched.",
   "emptyFirstRun": "No system transactional template configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSystemTransactionalTemplate",
    "contract": "marketing-crm",
    "purpose": "System Transactional Template Registry",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-041"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 9 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-042",
  "name": "Business Event & Notification Trigger Mapping",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.5",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/business-event-notification-trigger-mapping-adm-042",
   "component": "apps/ticvai-web/src/routes/platform/BusinessEventNotificationTriggerMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-038"
   ],
   "exitTo": [
    "ADM-038"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-038, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-038",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F133 step 8→9",
     "operation": "listBusinessEventNotification"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Map TICVAI business events to the operational communications they should generate. This is the core of the event-driven communication architecture.",
  "purposeNote": "appropriate operational notification according to centrally configured rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Customer, Channel, Membership, Booking Type. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Communication & Notification Platform Services_Reference.pdf, page 11 §Allow conditions based on"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Communication & Notification Platform Services_Reference.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Communication & Notification Platform Services_Reference.pdf, page 11"
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
       "label": "Customer",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 11 §Allow conditions based on"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 11 §Allow conditions based on"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 11 §Allow conditions based on"
      },
      {
       "kind": "secondaryButton",
       "label": "Booking Type",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 11 §Allow conditions based on"
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
   "loading": "The business event notification list.",
   "error": "Could not load. Names which read failed and leaves the business event notification untouched.",
   "emptyFirstRun": "No business event notification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the business event notification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBusinessEventNotification",
    "contract": "marketing-crm",
    "purpose": "Business Event & Notification Trigger Mapping",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BusinessEventNotificationTriggerMappingView.t30Days",
    "BusinessEventNotificationTriggerMappingView.t7Days",
    "BusinessEventNotificationTriggerMappingView.t1Day",
    "BusinessEventNotificationTriggerMappingView.eventId",
    "BusinessEventNotificationTriggerMappingView.sourceModule"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-042"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 4 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-043",
  "name": "Routing, Priority, Throttling & Fallback Rules",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.6",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/routing-priority-throttling-fallback-rules-adm-043",
   "component": "apps/ticvai-web/src/routes/platform/RoutingPriorityThrottlingFallbackRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-038"
   ],
   "exitTo": [
    "ADM-038"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-038, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-038",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F133 step 10→11",
     "operation": "listRoutingPriorityThrottling"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure based on; Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine how TICVAI delivers a message after a communication requirement has been created.",
  "purposeNote": "Communication requests are dynamically routed according to priority, availability, consent, provider health and configured fallback rules.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Message Type",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Recipient Type",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Cost",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Provider Health",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Messages per second",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Messages per minute",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Provider limit",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand limit",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Event limit",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 13 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The routing priority throttling configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the routing priority throttling untouched.",
   "emptyFirstRun": "No routing priority throttling configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRoutingPriorityThrottling",
    "contract": "marketing-crm",
    "purpose": "Routing, Priority, Throttling & Fallback Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-043"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 14 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-044",
  "name": "Consent, Preference & Communication Policy Enforcement",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.7",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/consent-preference-communication-policy-enforcement-adm-044",
   "component": "apps/ticvai-web/src/routes/platform/ConsentPreferenceCommunicationPolicyEnforcement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-038"
   ],
   "exitTo": [
    "ADM-038"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-038, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-038",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F133 step 12→13",
     "operation": "listConsentPreferenceCommunication"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a central enforcement layer ensuring communications respect the appropriate communication rules.",
  "purposeNote": "No communication is delivered without passing the applicable centralized consent, preference and communication-policy evaluation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Communication & Notification Platform Services_Reference.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Communication & Notification Platform Services_Reference.pdf, page 14"
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
       "impliedBy": "listConsentPreferenceCommunication",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The consent preference communication list.",
   "error": "Could not load. Names which read failed and leaves the consent preference communication untouched.",
   "emptyFirstRun": "No consent preference communication yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the consent preference communication are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConsentPreferenceCommunication",
    "contract": "marketing-crm",
    "purpose": "Consent, Preference & Communication Policy Enforcement",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ConsentPreferenceCommunicationPolicyEnforcementView.marketingConsent",
    "ConsentPreferenceCommunicationPolicyEnforcementView.emailPreference",
    "ConsentPreferenceCommunicationPolicyEnforcementView.smsPreference",
    "ConsentPreferenceCommunicationPolicyEnforcementView.whatsappPreference",
    "ConsentPreferenceCommunicationPolicyEnforcementView.pushPreference"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-044"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-045",
  "name": "Delivery Queue, Failure & Retry Management",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.8",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/delivery-queue-failure-retry-management-adm-045",
   "component": "apps/ticvai-web/src/routes/platform/DeliveryQueueFailureRetryManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-038"
   ],
   "exitTo": [
    "ADM-038"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-038, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-038",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F133 step 14→15",
     "operation": "listDeliveryQueueFailure"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide technical/operations teams with visibility into communications currently being processed or failing.",
  "purposeNote": "Failed communications can be identified, diagnosed, retried and resolved without losing the original business-event context.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every delivery queue failure",
       "columns": [
        "DeliveryQueueFailureRetryManagementView.pending",
        "DeliveryQueueFailureRetryManagementView.processing",
        "DeliveryQueueFailureRetryManagementView.sent",
        "DeliveryQueueFailureRetryManagementView.delivered",
        "DeliveryQueueFailureRetryManagementView.failed",
        "DeliveryQueueFailureRetryManagementView.retrying",
        "DeliveryQueueFailureRetryManagementView.deadLettered",
        "DeliveryQueueFailureRetryManagementView.cancelled",
        "DeliveryQueueFailureRetryManagementView.communicationId",
        "DeliveryQueueFailureRetryManagementView.sourceModule",
        "DeliveryQueueFailureRetryManagementView.businessEvent",
        "DeliveryQueueFailureRetryManagementView.recipient",
        "DeliveryQueueFailureRetryManagementView.channel",
        "DeliveryQueueFailureRetryManagementView.template",
        "DeliveryQueueFailureRetryManagementView.provider",
        "DeliveryQueueFailureRetryManagementView.priority",
        "DeliveryQueueFailureRetryManagementView.created",
        "DeliveryQueueFailureRetryManagementView.status",
        "DeliveryQueueFailureRetryManagementView.attempts"
       ],
       "bindsTo": "DeliveryQueueFailureRetryManagementView",
       "operation": "listDeliveryQueueFailure",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 16 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected delivery queue failure",
       "bindsTo": "DeliveryQueueFailureRetryManagementView",
       "columns": [
        "DeliveryQueueFailureRetryManagementView.pending",
        "DeliveryQueueFailureRetryManagementView.processing",
        "DeliveryQueueFailureRetryManagementView.sent",
        "DeliveryQueueFailureRetryManagementView.delivered",
        "DeliveryQueueFailureRetryManagementView.failed",
        "DeliveryQueueFailureRetryManagementView.retrying",
        "DeliveryQueueFailureRetryManagementView.deadLettered",
        "DeliveryQueueFailureRetryManagementView.cancelled",
        "DeliveryQueueFailureRetryManagementView.communicationId",
        "DeliveryQueueFailureRetryManagementView.sourceModule",
        "DeliveryQueueFailureRetryManagementView.businessEvent",
        "DeliveryQueueFailureRetryManagementView.recipient",
        "DeliveryQueueFailureRetryManagementView.channel",
        "DeliveryQueueFailureRetryManagementView.template",
        "DeliveryQueueFailureRetryManagementView.provider",
        "DeliveryQueueFailureRetryManagementView.priority",
        "DeliveryQueueFailureRetryManagementView.created",
        "DeliveryQueueFailureRetryManagementView.status",
        "DeliveryQueueFailureRetryManagementView.attempts"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Attempt 1”, “Wait 1 minute”, “Attempt 2”, “Wait 5 minutes”, “Attempt 3”, “Authorized administrators can”.",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 16 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The delivery queue failure list.",
   "error": "Could not load. Names which read failed and leaves the delivery queue failure untouched.",
   "emptyFirstRun": "No delivery queue failure yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the delivery queue failure are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDeliveryQueueFailure",
    "contract": "marketing-crm",
    "purpose": "Delivery Queue, Failure & Retry Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DeliveryQueueFailureRetryManagementView.pending",
    "DeliveryQueueFailureRetryManagementView.processing",
    "DeliveryQueueFailureRetryManagementView.sent",
    "DeliveryQueueFailureRetryManagementView.delivered",
    "DeliveryQueueFailureRetryManagementView.failed",
    "DeliveryQueueFailureRetryManagementView.retrying"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-045"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 16. 19 of 19 labels bound to a contract property; 19 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-046",
  "name": "Provider Health, Usage & Cost Monitoring",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.9",
   "page": 18
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/provider-health-usage-cost-monitoring-adm-046",
   "component": "apps/ticvai-web/src/routes/platform/ProviderHealthUsageCostMonitoring.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-038"
   ],
   "exitTo": [
    "ADM-038"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-038, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-038",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F133 step 16→17",
     "operation": "listProviderHealthUsage"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Monitor the operational and commercial performance of communication providers.",
  "purposeNote": "Management can understand provider reliability, usage and communication cost across the TICVAI platform.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search provider health usage",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 18 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Channel",
        "Provider",
        "Brand",
        "Venue",
        "Module",
        "Country",
        "Message Type"
       ],
       "notes": "The pack filters this screen by channel, provider, brand, venue, module, country and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 18 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every provider health usage",
       "columns": [
        "ProviderHealthUsageCostMonitoringView.volume",
        "ProviderHealthUsageCostMonitoringView.successRate",
        "ProviderHealthUsageCostMonitoringView.failureRate",
        "ProviderHealthUsageCostMonitoringView.deliveryTime",
        "ProviderHealthUsageCostMonitoringView.apiLatency",
        "ProviderHealthUsageCostMonitoringView.availability",
        "ProviderHealthUsageCostMonitoringView.retries",
        "ProviderHealthUsageCostMonitoringView.fallbackUsage",
        "ProviderHealthUsageCostMonitoringView.cost",
        "ProviderHealthUsageCostMonitoringView.costPerMessage"
       ],
       "bindsTo": "ProviderHealthUsageCostMonitoringView",
       "operation": "listProviderHealthUsage",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 18 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected provider health usage",
       "bindsTo": "ProviderHealthUsageCostMonitoringView",
       "columns": [
        "ProviderHealthUsageCostMonitoringView.volume",
        "ProviderHealthUsageCostMonitoringView.successRate",
        "ProviderHealthUsageCostMonitoringView.failureRate",
        "ProviderHealthUsageCostMonitoringView.deliveryTime",
        "ProviderHealthUsageCostMonitoringView.apiLatency",
        "ProviderHealthUsageCostMonitoringView.availability",
        "ProviderHealthUsageCostMonitoringView.retries",
        "ProviderHealthUsageCostMonitoringView.fallbackUsage",
        "ProviderHealthUsageCostMonitoringView.cost",
        "ProviderHealthUsageCostMonitoringView.costPerMessage"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Health”, “Warni”, “Cost Allocation”, “SLA Monitoring”.",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 18 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The provider health usage list.",
   "error": "Could not load. Names which read failed and leaves the provider health usage untouched.",
   "emptyFirstRun": "No provider health usage yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the provider health usage are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProviderHealthUsage",
    "contract": "marketing-crm",
    "purpose": "Provider Health, Usage & Cost Monitoring",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ProviderHealthUsageCostMonitoringView.volume",
    "ProviderHealthUsageCostMonitoringView.successRate",
    "ProviderHealthUsageCostMonitoringView.failureRate",
    "ProviderHealthUsageCostMonitoringView.deliveryTime",
    "ProviderHealthUsageCostMonitoringView.apiLatency",
    "ProviderHealthUsageCostMonitoringView.availability"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-046"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 18. 10 of 17 labels bound to a contract property; 17 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-047",
  "name": "AI Delivery Optimization & Communication Platform Diagnostics",
  "module": "Platform",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Communication & Notification Platform Services_Reference.pdf",
   "board": "1",
   "number": "12.1.10",
   "page": 19
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-delivery-optimization-communication-platform-diagnost-adm-047",
   "component": "apps/ticvai-web/src/routes/platform/AiDeliveryOptimizationCommunicationPlatformDiagn.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-038"
   ],
   "exitTo": [
    "ADM-038"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-038, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Provide an AI intelligence layer focused specifically on communication infrastructure performance, not CRM marketing strategy.",
  "purposeNote": "reliability, scalability and cost without interfering with CRM's ownership of customer marketing strategy. Board 1 — Final Screen Register",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every delivery optimization communication",
       "columns": [
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.businessEvents",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.channels",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.providers",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.queues",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.failures",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.retries",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.latency",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.delivery",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.cost",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.recipientPreferences",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.regionalPerformance",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.historicalPatterns"
       ],
       "bindsTo": "AiDeliveryOptimizationCommunicationPlatformDiagnostiView",
       "operation": "listDeliveryCommunicationPlatform",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 19 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected delivery optimization communication",
       "bindsTo": "AiDeliveryOptimizationCommunicationPlatformDiagnostiView",
       "columns": [
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.businessEvents",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.channels",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.providers",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.queues",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.failures",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.retries",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.latency",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.delivery",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.cost",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.recipientPreferences",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.regionalPerformance",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.historicalPatterns"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Administrators can ask”, “Potential Provider Incident”, “Automation Governance”, “Backend Screen Primary Responsibility”, “Platform communication”, “Marketing & CRM owns”.",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 19 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The delivery optimization communication list.",
   "error": "Could not load. Names which read failed and leaves the delivery optimization communication untouched.",
   "emptyFirstRun": "No delivery optimization communication yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the delivery optimization communication are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDeliveryCommunicationPlatform",
    "contract": "marketing-crm",
    "purpose": "AI Delivery Optimization & Communication Platform Diagnostics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.businessEvents",
    "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.channels",
    "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.providers",
    "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.queues",
    "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.failures",
    "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.retries"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-047"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 19. 12 of 12 labels bound to a contract property; 12 of 79 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listBusinessEventNotification": {
  "method": "GET",
  "path": "/business-event-notification",
  "contract": "marketing-crm",
  "summary": "Business Event & Notification Trigger Mapping",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BusinessEventNotificationTriggerMappingView"
 },
 "listCommunicationService": {
  "method": "GET",
  "path": "/communication-service",
  "contract": "marketing-crm",
  "summary": "Communication Service Command Center",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CommunicationServiceCommandCenterView"
 },
 "listConsentPreferenceCommunication": {
  "method": "GET",
  "path": "/consent-preference-communication",
  "contract": "marketing-crm",
  "summary": "Consent, Preference & Communication Policy Enforcement",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConsentPreferenceCommunicationPolicyEnforcementView"
 },
 "listDeliveryCommunicationPlatform": {
  "method": "GET",
  "path": "/delivery-communication-platform",
  "contract": "marketing-crm",
  "summary": "AI Delivery Optimization & Communication Platform Diagnostics",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiDeliveryOptimizationCommunicationPlatformDiagnostiView"
 },
 "listDeliveryQueueFailure": {
  "method": "GET",
  "path": "/delivery-queue-failure",
  "contract": "marketing-crm",
  "summary": "Delivery Queue, Failure & Retry Management",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DeliveryQueueFailureRetryManagementView"
 },
 "listProviderHealthUsage": {
  "method": "GET",
  "path": "/provider-health-usage",
  "contract": "marketing-crm",
  "summary": "Provider Health, Usage & Cost Monitoring",
  "permission": "MARKETING_VIEW",
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
    "name": "provider",
    "in": "query",
    "required": false
   },
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
    "name": "module",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "messageType",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ProviderHealthUsageCostMonitoringView"
 },
 "listRoutingPriorityThrottling": {
  "method": "GET",
  "path": "/routing-priority-throttling",
  "contract": "marketing-crm",
  "summary": "Routing, Priority, Throttling & Fallback Rules",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RoutingPriorityThrottlingFallbackRulesView"
 },
 "listSystemTransactionalTemplate": {
  "method": "GET",
  "path": "/system-transactional-template",
  "contract": "marketing-crm",
  "summary": "System Transactional Template Registry",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SystemTransactionalTemplateRegistryView"
 },
 "setChannelProvider": {
  "method": "PUT",
  "path": "/channel-provider",
  "contract": "marketing-crm",
  "summary": "Channel & Provider Configuration",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ChannelProviderConfigurationInput",
  "responds": "ChannelProviderConfigurationView"
 },
 "setSenderIdentityDomain": {
  "method": "PUT",
  "path": "/sender-identity-domain",
  "contract": "marketing-crm",
  "summary": "Sender Identity, Domain & Brand Configuration",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "SenderIdentityDomainBrandConfigurationInput",
  "responds": "SenderIdentityDomainBrandConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiDeliveryOptimizationCommunicationPlatformDiagnostiView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What AI Delivery Optimization & Communication Platform Diagnostics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "businessEvents": {
    "type": "string",
    "description": "Business Events"
   },
   "channels": {
    "type": "string",
    "description": "Channels"
   },
   "providers": {
    "type": "string",
    "description": "Providers"
   },
   "queues": {
    "type": "string",
    "description": "Queues"
   },
   "failures": {
    "type": "string",
    "description": "Failures"
   },
   "retries": {
    "type": "integer",
    "description": "Retries"
   },
   "latency": {
    "type": "string",
    "description": "Latency"
   },
   "delivery": {
    "type": "string",
    "description": "Delivery"
   },
   "cost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost"
   },
   "recipientPreferences": {
    "type": "string",
    "description": "Recipient preferences"
   },
   "regionalPerformance": {
    "type": "string",
    "description": "Regional performance"
   },
   "historicalPatterns": {
    "type": "string",
    "description": "Historical patterns"
   },
   "whyDidCommunicationCostIncrease": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "“Why did communication cost increase?”"
   },
   "majorEvents": {
    "type": "string",
    "description": "Major Events"
   },
   "ticketReleases": {
    "type": "string",
    "description": "Ticket Releases"
   },
   "membershipRenewals": {
    "type": "string",
    "description": "Membership Renewals"
   },
   "groupArrivals": {
    "type": "string",
    "description": "Group Arrivals"
   },
   "waiverDeadlines": {
    "type": "string",
    "description": "Waiver Deadlines"
   },
   "providerFailover": {
    "type": "string",
    "description": "Provider Failover"
   },
   "queueScaling": {
    "type": "string",
    "description": "Queue Scaling"
   },
   "operationalAlerting": {
    "type": "string",
    "description": "Operational Alerting"
   },
   "health": {
    "type": "string",
    "description": "health"
   },
   "consentPreferenceCommunicationPolicy": {
    "type": "string",
    "description": "Consent, Preference & Communication Policy"
   },
   "guardianConsentIsIncomplete": {
    "type": "string",
    "description": "“Guardian consent is incomplete.”"
   }
  }
 },
 "BusinessEventNotificationTriggerMappingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Business Event & Notification Trigger Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "t30Days": {
    "type": "string",
    "description": "T−30 days"
   },
   "t7Days": {
    "type": "string",
    "description": "T−7 days"
   },
   "t1Day": {
    "type": "string",
    "description": "T−1 day"
   },
   "eventId": {
    "type": "string",
    "description": "Event ID"
   },
   "sourceModule": {
    "type": "string",
    "description": "Source Module"
   },
   "eventType": {
    "type": "string",
    "description": "Event Type"
   },
   "payload": {
    "type": "string",
    "description": "Payload"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "validEmailEmailPermitted": {
    "type": "string",
    "description": "Valid email + Email permitted"
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
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "transactionStatus": {
    "type": "string",
    "description": "Transaction Status"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "bookingType": {
    "type": "string",
    "description": "Booking Type"
   },
   "ownedWithinCrm": {
    "type": "string",
    "description": "owned within CRM"
   }
  }
 },
 "ChannelProviderConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is control.api_client at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Channel & Provider Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each provider* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "email": {
    "type": "string",
    "description": "Email"
   },
   "sms": {
    "type": "string",
    "description": "SMS"
   },
   "whatsapp": {
    "type": "string",
    "description": "WhatsApp"
   },
   "mobilePush": {
    "type": "string",
    "description": "Mobile Push"
   },
   "inAppNotification": {
    "type": "string",
    "description": "In-App Notification"
   },
   "futureSupportedChannels": {
    "type": "string",
    "description": "Future supported channels"
   },
   "providerName": {
    "type": "string",
    "description": "Provider Name"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "account": {
    "type": "string",
    "description": "Account"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "environment": {
    "type": "string",
    "description": "Environment"
   },
   "credentialsSecretReference": {
    "type": "string",
    "description": "Credentials/Secret Reference"
   },
   "apiConfiguration": {
    "type": "string",
    "description": "API Configuration"
   },
   "webhookConfiguration": {
    "type": "string",
    "description": "Webhook Configuration"
   },
   "rateLimits": {
    "type": "number",
    "description": "Rate Limits"
   },
   "timeout": {
    "type": "string",
    "description": "Timeout"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "exposedDirectlyInTheUi": {
    "type": "string",
    "description": "exposed directly in the UI"
   },
   "providerAPrimary": {
    "type": "string",
    "description": "Provider A — Primary"
   },
   "providerBFallback": {
    "type": "string",
    "description": "Provider B — Fallback"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "testConnection": {
    "type": "string",
    "description": "Test Connection"
   },
   "testWebhook": {
    "type": "string",
    "description": "Test Webhook"
   }
  },
  "x-ticvai-record-definition": "For each provider"
 },
 "ChannelProviderConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Channel & Provider Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "email": {
    "type": "string",
    "description": "Email"
   },
   "sms": {
    "type": "string",
    "description": "SMS"
   },
   "whatsapp": {
    "type": "string",
    "description": "WhatsApp"
   },
   "mobilePush": {
    "type": "string",
    "description": "Mobile Push"
   },
   "inAppNotification": {
    "type": "string",
    "description": "In-App Notification"
   },
   "futureSupportedChannels": {
    "type": "string",
    "description": "Future supported channels"
   },
   "providerName": {
    "type": "string",
    "description": "Provider Name"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "account": {
    "type": "string",
    "description": "Account"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "environment": {
    "type": "string",
    "description": "Environment"
   },
   "credentialsSecretReference": {
    "type": "string",
    "description": "Credentials/Secret Reference"
   },
   "apiConfiguration": {
    "type": "string",
    "description": "API Configuration"
   },
   "webhookConfiguration": {
    "type": "string",
    "description": "Webhook Configuration"
   },
   "rateLimits": {
    "type": "number",
    "description": "Rate Limits"
   },
   "timeout": {
    "type": "string",
    "description": "Timeout"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "exposedDirectlyInTheUi": {
    "type": "string",
    "description": "exposed directly in the UI"
   },
   "providerAPrimary": {
    "type": "string",
    "description": "Provider A — Primary"
   },
   "providerBFallback": {
    "type": "string",
    "description": "Provider B — Fallback"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "testConnection": {
    "type": "string",
    "description": "Test Connection"
   },
   "testWebhook": {
    "type": "string",
    "description": "Test Webhook"
   }
  }
 },
 "CommunicationServiceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Communication Service Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "messagesProcessedToday": {
    "type": "string",
    "description": "Messages Processed Today"
   },
   "emailSent": {
    "type": "string",
    "description": "Email Sent"
   },
   "smsSent": {
    "type": "string",
    "description": "SMS Sent"
   },
   "whatsappSent": {
    "type": "string",
    "description": "WhatsApp Sent"
   },
   "pushNotifications": {
    "type": "integer",
    "description": "Push Notifications"
   },
   "inAppNotifications": {
    "type": "integer",
    "description": "In-App Notifications"
   },
   "delivered": {
    "type": "string",
    "description": "Delivered"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "pending": {
    "type": "integer",
    "description": "Pending"
   },
   "retrying": {
    "type": "string",
    "description": "Retrying"
   },
   "averageDeliveryTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Delivery Time"
   },
   "providerAvailability": {
    "type": "string",
    "description": "Provider Availability"
   },
   "showCommunicationVolumeOriginatingFrom": {
    "type": "integer",
    "description": "Show communication volume originating from"
   },
   "crm": {
    "type": "string",
    "description": "CRM"
   },
   "ticketing": {
    "type": "string",
    "description": "Ticketing"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "waiver": {
    "type": "string",
    "description": "Waiver"
   },
   "groupSales": {
    "type": "string",
    "description": "Group Sales"
   },
   "customerService": {
    "type": "string",
    "description": "Customer Service"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "resourceManagement": {
    "type": "string",
    "description": "Resource Management"
   },
   "accessControl": {
    "type": "string",
    "description": "Access Control"
   },
   "otherTicvaiServices": {
    "type": "string",
    "description": "Other TICVAI Services"
   },
   "eSCy": {
    "type": "string",
    "description": "e s cy"
   },
   "providerC31k97924s": {
    "type": "number",
    "description": "Provider C 31K 97.9% 2.4s"
   },
   "pNg": {
    "type": "string",
    "description": "p ng"
   },
   "push110k99806s": {
    "type": "number",
    "description": "Push 110K 99.8% 0.6s"
   }
  }
 },
 "ConsentPreferenceCommunicationPolicyEnforcementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Consent, Preference & Communication Policy Enforcement displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "marketingConsent": {
    "type": "boolean",
    "description": "Marketing Consent"
   },
   "emailPreference": {
    "type": "string",
    "description": "Email Preference"
   },
   "smsPreference": {
    "type": "string",
    "description": "SMS Preference"
   },
   "whatsappPreference": {
    "type": "string",
    "description": "WhatsApp Preference"
   },
   "pushPreference": {
    "type": "string",
    "description": "Push Preference"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "optOut": {
    "type": "string",
    "description": "Opt-Out"
   },
   "suppression": {
    "type": "string",
    "description": "Suppression"
   },
   "contactRestrictions": {
    "type": "string",
    "description": "Contact Restrictions"
   },
   "transactional": {
    "type": "string",
    "description": "Transactional"
   },
   "operational": {
    "type": "string",
    "description": "Operational"
   },
   "service": {
    "type": "string",
    "description": "Service"
   },
   "marketing": {
    "type": "string",
    "description": "Marketing"
   },
   "unsubscribed": {
    "type": "string",
    "description": "Unsubscribed"
   },
   "invalidEmail": {
    "type": "string",
    "description": "Invalid Email"
   },
   "invalidMobile": {
    "type": "string",
    "description": "Invalid Mobile"
   },
   "hardBounce": {
    "type": "string",
    "description": "Hard Bounce"
   },
   "complaint": {
    "type": "string",
    "description": "Complaint"
   },
   "administrativeSuppression": {
    "type": "string",
    "description": "Administrative Suppression"
   },
   "allowed": {
    "type": "boolean",
    "description": "Allowed"
   },
   "blocked": {
    "type": "string",
    "description": "Blocked"
   },
   "rerouted": {
    "type": "string",
    "description": "Rerouted"
   },
   "suppressed": {
    "type": "string",
    "description": "Suppressed"
   }
  }
 },
 "DeliveryQueueFailureRetryManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Delivery Queue, Failure & Retry Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "pending": {
    "type": "integer",
    "description": "Pending"
   },
   "processing": {
    "type": "string",
    "description": "Processing"
   },
   "sent": {
    "type": "string",
    "description": "Sent"
   },
   "delivered": {
    "type": "string",
    "description": "Delivered"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "retrying": {
    "type": "string",
    "description": "Retrying"
   },
   "deadLettered": {
    "type": "string",
    "description": "Dead-Lettered"
   },
   "cancelled": {
    "type": "integer",
    "description": "Cancelled"
   },
   "communicationId": {
    "type": "string",
    "description": "Communication ID"
   },
   "sourceModule": {
    "type": "string",
    "description": "Source Module"
   },
   "businessEvent": {
    "type": "string",
    "description": "Business Event"
   },
   "recipient": {
    "type": "string",
    "description": "Recipient"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "template": {
    "type": "string",
    "description": "Template"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "created": {
    "type": "string",
    "format": "date-time",
    "description": "Created"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "attempts": {
    "type": "integer",
    "description": "Attempts"
   },
   "reroute": {
    "type": "string",
    "description": "Reroute"
   },
   "changeProvider": {
    "type": "string",
    "description": "Change Provider"
   },
   "inspectFailure": {
    "type": "string",
    "description": "Inspect Failure"
   },
   "replayEventWhereSafe": {
    "type": "string",
    "description": "Replay Event where safe"
   }
  }
 },
 "ProviderHealthUsageCostMonitoringView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Provider Health, Usage & Cost Monitoring displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "volume": {
    "type": "integer",
    "description": "Volume"
   },
   "successRate": {
    "type": "number",
    "description": "Success Rate"
   },
   "failureRate": {
    "type": "number",
    "description": "Failure Rate"
   },
   "deliveryTime": {
    "type": "string",
    "format": "date-time",
    "description": "Delivery Time"
   },
   "apiLatency": {
    "type": "string",
    "description": "API Latency"
   },
   "availability": {
    "type": "string",
    "description": "Availability"
   },
   "retries": {
    "type": "integer",
    "description": "Retries"
   },
   "fallbackUsage": {
    "type": "string",
    "description": "Fallback Usage"
   },
   "cost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost"
   },
   "costPerMessage": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost per Message"
   },
   "erSDelivery1k": {
    "type": "string",
    "description": "er s Delivery 1K"
   },
   "ng": {
    "type": "string",
    "description": "ng"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "trackContractualProviderTargetsWhereConfigured": {
    "type": "string",
    "description": "Track contractual/provider targets where configured"
   }
  }
 },
 "RoutingPriorityThrottlingFallbackRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Routing, Priority, Throttling & Fallback Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "messageType": {
    "type": "string",
    "description": "Message Type"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "recipientType": {
    "type": "string",
    "description": "Recipient Type"
   },
   "cost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost"
   },
   "providerHealth": {
    "type": "string",
    "description": "Provider Health"
   },
   "p1Critical": {
    "type": "string",
    "description": "P1 — Critical"
   },
   "p2High": {
    "type": "string",
    "description": "P2 — High"
   },
   "paymentIssueEventDayNotification": {
    "type": "string",
    "description": "Payment issue, event-day notification"
   },
   "p3Normal": {
    "type": "string",
    "description": "P3 — Normal"
   },
   "ticketConfirmationWaiverReminder": {
    "type": "string",
    "description": "Ticket confirmation, waiver reminder"
   },
   "p4Bulk": {
    "type": "string",
    "description": "P4 — Bulk"
   },
   "nonUrgentHighVolumeCommunication": {
    "type": "integer",
    "description": "Non-urgent high-volume communication"
   },
   "primaryProviderA": {
    "type": "string",
    "description": "Primary → Provider A"
   },
   "messagesPerSecond": {
    "type": "string",
    "description": "Messages per second"
   },
   "messagesPerMinute": {
    "type": "string",
    "description": "Messages per minute"
   },
   "providerLimit": {
    "type": "integer",
    "description": "Provider limit"
   },
   "brandLimit": {
    "type": "integer",
    "description": "Brand limit"
   },
   "eventLimit": {
    "type": "integer",
    "description": "Event limit"
   },
   "complianceRules": {
    "type": "string",
    "description": "compliance rules"
   }
  }
 },
 "SenderIdentityDomainBrandConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is control.api_client at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Sender Identity, Domain & Brand Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "sendingDomain": {
    "type": "string",
    "description": "Sending Domain"
   },
   "fromName": {
    "type": "string",
    "description": "From Name"
   },
   "fromAddress": {
    "type": "string",
    "description": "From Address"
   },
   "replyTo": {
    "type": "string",
    "description": "Reply-To"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "senderId": {
    "type": "string",
    "description": "Sender ID"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "approvedUse": {
    "type": "integer",
    "description": "Approved Use"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "application": {
    "type": "string",
    "description": "Application"
   },
   "platform": {
    "type": "string",
    "description": "Platform"
   },
   "environment": {
    "type": "string",
    "description": "Environment"
   },
   "businessAccount": {
    "type": "string",
    "description": "Business Account"
   },
   "phoneNumber": {
    "type": "string",
    "description": "Phone Number"
   },
   "verificationStatus": {
    "type": "string",
    "description": "Verification Status"
   },
   "approvedTemplates": {
    "type": "integer",
    "description": "Approved Templates"
   }
  }
 },
 "SenderIdentityDomainBrandConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Sender Identity, Domain & Brand Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "sendingDomain": {
    "type": "string",
    "description": "Sending Domain"
   },
   "fromName": {
    "type": "string",
    "description": "From Name"
   },
   "fromAddress": {
    "type": "string",
    "description": "From Address"
   },
   "replyTo": {
    "type": "string",
    "description": "Reply-To"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "senderId": {
    "type": "string",
    "description": "Sender ID"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "approvedUse": {
    "type": "integer",
    "description": "Approved Use"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "application": {
    "type": "string",
    "description": "Application"
   },
   "platform": {
    "type": "string",
    "description": "Platform"
   },
   "environment": {
    "type": "string",
    "description": "Environment"
   },
   "businessAccount": {
    "type": "string",
    "description": "Business Account"
   },
   "phoneNumber": {
    "type": "string",
    "description": "Phone Number"
   },
   "verificationStatus": {
    "type": "string",
    "description": "Verification Status"
   },
   "approvedTemplates": {
    "type": "integer",
    "description": "Approved Templates"
   }
  }
 },
 "SystemTransactionalTemplateRegistryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What System Transactional Template Registry displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketConfirmation": {
    "type": "string",
    "description": "Ticket Confirmation"
   },
   "ticketResend": {
    "type": "string",
    "description": "Ticket Resend"
   },
   "eventReminder": {
    "type": "string",
    "description": "Event Reminder"
   },
   "eventRescheduled": {
    "type": "string",
    "description": "Event Rescheduled"
   },
   "eventCancelled": {
    "type": "string",
    "description": "Event Cancelled"
   },
   "paymentSuccessful": {
    "type": "string",
    "description": "Payment Successful"
   },
   "paymentFailed": {
    "type": "integer",
    "description": "Payment Failed"
   },
   "membershipActivated": {
    "type": "string",
    "description": "Membership Activated"
   },
   "membershipExpiring": {
    "type": "string",
    "description": "Membership Expiring"
   },
   "waiverRequired": {
    "type": "boolean",
    "description": "Waiver Required"
   },
   "guardianConsentRequired": {
    "type": "boolean",
    "description": "Guardian Consent Required"
   },
   "waiverReminder": {
    "type": "string",
    "description": "Waiver Reminder"
   },
   "groupBookingConfirmed": {
    "type": "string",
    "description": "Group Booking Confirmed"
   },
   "depositDue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit Due"
   },
   "templateId": {
    "type": "string",
    "description": "Template ID"
   },
   "templateName": {
    "type": "string",
    "description": "Template Name"
   },
   "businessEvent": {
    "type": "string",
    "description": "Business Event"
   },
   "sourceModule": {
    "type": "string",
    "description": "Source Module"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "subject": {
    "type": "string",
    "description": "Subject"
   },
   "header": {
    "type": "string",
    "description": "Header"
   },
   "body": {
    "type": "string",
    "description": "Body"
   },
   "footer": {
    "type": "string",
    "description": "Footer"
   },
   "cta": {
    "type": "string",
    "description": "CTA"
   },
   "attachmentsWhereApplicable": {
    "type": "string",
    "description": "Attachments where applicable"
   },
   "transactionalTemplatePlatform": {
    "type": "string",
    "description": "Transactional Template — Platform"
   },
   "marketingTemplateCrm": {
    "type": "string",
    "description": "Marketing Template — CRM"
   }
  }
 }
}
```
