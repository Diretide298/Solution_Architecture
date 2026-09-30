# WS24 — Communication & Notification Platform Services board 1

**10 screens · 11 operations · 19 schemas · 4 permissions**

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
  `AI_USE, GUEST_VIEW, MARKETING_MANAGE, MARKETING_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
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
| `ADM-047` | AI Delivery Optimization & Communication Platform Diagnostics | listDetail | 2 | 0 | — |

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
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-038 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
  "purposeNote": "Platform administrators can understand communication volume, delivery health, provider performance and operational exceptions from one centralized workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide administrators and technical/operations teams with a centralized view of the health and activity of TICVAI's communication infrastructure. This is not a marketing dashboard.",
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
        "CommunicationServiceCommandCenterView.messagesProcessed",
        "CommunicationServiceCommandCenterView.byChannel[].sent",
        "CommunicationServiceCommandCenterView.delivered",
        "CommunicationServiceCommandCenterView.failed",
        "CommunicationServiceCommandCenterView.pending",
        "CommunicationServiceCommandCenterView.retrying",
        "CommunicationServiceCommandCenterView.averageDeliverySeconds",
        "CommunicationServiceCommandCenterView.providerAvailabilityRate",
        "CommunicationServiceCommandCenterView.byChannel[].channel"
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
        "CommunicationServiceCommandCenterView.messagesProcessed",
        "CommunicationServiceCommandCenterView.byChannel[].sent",
        "CommunicationServiceCommandCenterView.delivered",
        "CommunicationServiceCommandCenterView.failed",
        "CommunicationServiceCommandCenterView.pending",
        "CommunicationServiceCommandCenterView.retrying",
        "CommunicationServiceCommandCenterView.averageDeliverySeconds",
        "CommunicationServiceCommandCenterView.providerAvailabilityRate",
        "CommunicationServiceCommandCenterView.byChannel[].channel"
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
    "CommunicationServiceCommandCenterView.messagesProcessed",
    "CommunicationServiceCommandCenterView.byChannel[].sent"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-038",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-038"
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
  "purposeNote": "Authorized administrators can configure and test multiple communication providers without requiring individual TICVAI modules to maintain direct provider integrations.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the external/internal services used by TICVAI to deliver communications.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Legal Entity, Test Connection, Send Test Message, Validate Credentials, Test Webhook, Verify Delivery Receipt. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Allow different providers by"
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
       "label": "Legal Entity",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 6 §Allow different providers by"
      },
      {
       "kind": "secondaryButton",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-039",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-039"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 12 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Every outbound communication uses a verified and appropriately governed sender identity for the applicable brand, channel and region.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Manage the identities from which TICVAI communications are sent.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-040",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-040"
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
  "purposeNote": "Operational modules can use governed reusable communication templates without embedding message content directly in application code.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Maintain centralized system/transactional communication templates used by TICVAI operational modules. This screen must not replace CRM's marketing template builder.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Attachments where applicable. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Support"
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Attachments where applicable",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 9 §Support"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-041",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-041"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 10 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "appropriate operational notification according to centrally configured rules.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Map TICVAI business events to the operational communications they should generate. This is the core of the event-driven communication architecture.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Product, Venue, Customer, Channel, Transaction Status, Membership, Booking Type. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Product",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 11 §Allow conditions based on"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 11 §Allow conditions based on"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue",
       "provenance": "pack Communication & Notification Platform Services_Reference.pdf, page 11 §Allow conditions based on"
      },
      {
       "kind": "secondaryButton",
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
       "label": "Transaction Status",
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
    "BusinessEventNotificationTriggerMappingView.eventId",
    "BusinessEventNotificationTriggerMappingView.sourceModule"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-042",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-042"
  },
  "apisNote": "Regenerated 9 September 2026 from Communication & Notification Platform Services_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 8 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Communication requests are dynamically routed according to priority, availability, consent, provider health and configured fallback rules.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure based on; Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine how TICVAI delivers a message after a communication requirement has been created.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-043",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-043"
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
  "purposeNote": "No communication is delivered without passing the applicable centralized consent, preference and communication-policy evaluation.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a central enforcement layer ensuring communications respect the appropriate communication rules.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-044",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-044"
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
  "purposeNote": "Failed communications can be identified, diagnosed, retried and resolved without losing the original business-event context.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide technical/operations teams with visibility into communications currently being processed or failing.",
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
        "DeliveryQueueFailureRetryManagementView.status",
        "DeliveryQueueFailureRetryManagementView.communicationId",
        "DeliveryQueueFailureRetryManagementView.sourceModule",
        "DeliveryQueueFailureRetryManagementView.businessEvent",
        "DeliveryQueueFailureRetryManagementView.recipient",
        "DeliveryQueueFailureRetryManagementView.channel",
        "DeliveryQueueFailureRetryManagementView.template",
        "DeliveryQueueFailureRetryManagementView.provider",
        "DeliveryQueueFailureRetryManagementView.priority",
        "DeliveryQueueFailureRetryManagementView.createdAt",
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
        "DeliveryQueueFailureRetryManagementView.status",
        "DeliveryQueueFailureRetryManagementView.communicationId",
        "DeliveryQueueFailureRetryManagementView.sourceModule",
        "DeliveryQueueFailureRetryManagementView.businessEvent",
        "DeliveryQueueFailureRetryManagementView.recipient",
        "DeliveryQueueFailureRetryManagementView.channel",
        "DeliveryQueueFailureRetryManagementView.template",
        "DeliveryQueueFailureRetryManagementView.provider",
        "DeliveryQueueFailureRetryManagementView.priority",
        "DeliveryQueueFailureRetryManagementView.createdAt",
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
    "DeliveryQueueFailureRetryManagementView.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-045",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-045"
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
  "purposeNote": "Management can understand provider reliability, usage and communication cost across the TICVAI platform.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Monitor the operational and commercial performance of communication providers.",
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
        "ProviderHealthUsageCostMonitoringView.averageDeliverySeconds",
        "ProviderHealthUsageCostMonitoringView.averageApiLatencySeconds",
        "ProviderHealthUsageCostMonitoringView.availabilityRate",
        "ProviderHealthUsageCostMonitoringView.retries",
        "ProviderHealthUsageCostMonitoringView.fallbackCount",
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
        "ProviderHealthUsageCostMonitoringView.averageDeliverySeconds",
        "ProviderHealthUsageCostMonitoringView.averageApiLatencySeconds",
        "ProviderHealthUsageCostMonitoringView.availabilityRate",
        "ProviderHealthUsageCostMonitoringView.retries",
        "ProviderHealthUsageCostMonitoringView.fallbackCount",
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
    "ProviderHealthUsageCostMonitoringView.averageDeliverySeconds",
    "ProviderHealthUsageCostMonitoringView.averageApiLatencySeconds",
    "ProviderHealthUsageCostMonitoringView.availabilityRate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-046",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-046"
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
  "purposeNote": "reliability, scalability and cost without interfering with CRM's ownership of customer marketing strategy. Board 1 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Provide an AI intelligence layer focused specifically on communication infrastructure performance, not CRM marketing strategy.",
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
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.healthSummary",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.incidents[]",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.failureGroups[]",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.recommendations[]",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.forecasts[]",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.automatedActions[]"
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
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.healthSummary",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.incidents[]",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.failureGroups[]",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.recommendations[]",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.forecasts[]",
        "AiDeliveryOptimizationCommunicationPlatformDiagnostiView.automatedActions[]"
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
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "Send-time suggestion (kind sendTime): best hour and channel per recipient",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-047",
   "workshopBoard": "wireframes/WS41 Communication & Notification Platform Services Board 1.dc.html#adm-047"
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
  "parameters": [
   {
    "name": "sourceModule",
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
 "listCommunicationService": {
  "method": "GET",
  "path": "/communication-service",
  "contract": "marketing-crm",
  "summary": "Communication Service Command Center",
  "permission": "MARKETING_VIEW",
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
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "CommunicationServiceCommandCenterView"
 },
 "listConsentPreferenceCommunication": {
  "method": "GET",
  "path": "/consent-preference-communication",
  "contract": "marketing-crm",
  "summary": "Consent, Preference & Communication Policy Enforcement",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "decision",
    "in": "query",
    "required": false
   },
   {
    "name": "messageClass",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "subjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
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
 "listDeliveryCommunicationPlatform": {
  "method": "GET",
  "path": "/delivery-communication-platform",
  "contract": "marketing-crm",
  "summary": "AI Delivery Optimization & Communication Platform Diagnostics",
  "permission": "MARKETING_VIEW",
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
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
    "in": "query",
    "required": false
   }
  ],
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
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "sourceModule",
    "in": "query",
    "required": false
   },
   {
    "name": "businessEvent",
    "in": "query",
    "required": false
   },
   {
    "name": "providerId",
    "in": "query",
    "required": false
   },
   {
    "name": "priority",
    "in": "query",
    "required": false
   },
   {
    "name": "failureCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
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
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "providerId",
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
    "name": "messageClass",
    "in": "query",
    "required": false
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
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
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "priorityClass",
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
 "listSystemTransactionalTemplate": {
  "method": "GET",
  "path": "/system-transactional-template",
  "contract": "marketing-crm",
  "summary": "System Transactional Template Registry",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ownership",
    "in": "query",
    "required": false
   },
   {
    "name": "sourceModule",
    "in": "query",
    "required": false
   },
   {
    "name": "businessEvent",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "brandId",
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
 "requestSuggestion": {
  "method": "POST",
  "path": "/ai/suggestions",
  "contract": "ai",
  "summary": "Ask for an answer, however it is currently produced",
  "permission": "AI_USE",
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
  "responds": "Suggestion"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "x-ticvai-persistence": "none — projection over ai.suggestion, marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)",
  "description": "AI findings over the communication platform for the window; empty arrays when AI processing is off.",
  "required": [
   "generatedAt",
   "incidents",
   "recommendations"
  ],
  "properties": {
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "healthSummary": {
    "type": "string"
   },
   "incidents": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "title",
      "detectedAt"
     ],
     "properties": {
      "title": {
       "type": "string"
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "country": {
       "type": "string",
       "pattern": "^[A-Z]{2}$"
      },
      "messageClass": {
       "type": "string",
       "enum": [
        "transactional",
        "operational",
        "service",
        "marketing"
       ]
      },
      "sourceModule": {
       "type": "string",
       "enum": [
        "crm",
        "ticketing",
        "membership",
        "waiver",
        "groupSales",
        "customerService",
        "finance",
        "wallet",
        "resourceManagement",
        "accessControl",
        "other"
       ]
      },
      "baselineFailureRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "currentFailureRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "affectedMessages": {
       "type": "integer",
       "minimum": 0
      },
      "failoverAvailable": {
       "type": "boolean"
      },
      "probableRootCause": {
       "type": "string"
      },
      "detectedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "failureGroups": {
    "type": "array",
    "description": "Failures grouped by probable root cause.",
    "items": {
     "type": "object",
     "required": [
      "probableRootCause",
      "count"
     ],
     "properties": {
      "probableRootCause": {
       "type": "string"
      },
      "failureCategory": {
       "type": "string",
       "enum": [
        "providerUnavailable",
        "invalidAddress",
        "invalidMobile",
        "rateLimited",
        "authenticationError",
        "templateRejected",
        "timeout",
        "consentBlock",
        "unknownError"
       ]
      },
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "count": {
       "type": "integer",
       "minimum": 0
      },
      "firstSeenAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "recommendations": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "summary"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "routing",
        "cost",
        "senderAnomaly"
       ]
      },
      "summary": {
       "type": "string"
      },
      "evidence": {
       "type": "string"
      },
      "estimatedMonthlySaving": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "status": {
       "type": "string",
       "enum": [
        "proposed",
        "applied",
        "dismissed"
       ]
      }
     }
    }
   },
   "forecasts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "driver",
      "date",
      "forecastVolume"
     ],
     "properties": {
      "driver": {
       "type": "string",
       "enum": [
        "majorEvent",
        "ticketRelease",
        "membershipRenewal",
        "groupArrival",
        "waiverDeadline"
       ]
      },
      "referenceId": {
       "type": "string",
       "format": "uuid"
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "date": {
       "type": "string",
       "format": "date"
      },
      "forecastVolume": {
       "type": "integer",
       "minimum": 0
      },
      "capacitySufficient": {
       "type": "boolean"
      }
     }
    }
   },
   "automatedActions": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "action",
      "takenAt"
     ],
     "properties": {
      "action": {
       "type": "string",
       "enum": [
        "providerFailover",
        "queueScaling",
        "retryAdjustment",
        "operationalAlert"
       ]
      },
      "summary": {
       "type": "string"
      },
      "takenAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
 },
 "AiMaturity": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded as jsonb on ai.suggestion and ai.forecast_version",
  "description": "**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.",
  "required": [
   "stage",
   "basedOn"
  ],
  "properties": {
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ],
    "description": "`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."
   },
   "basedOn": {
    "type": "string",
    "description": "The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "source"
     ],
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "venueSettings",
        "startingPattern",
        "calendar",
        "weather",
        "bookingsOnHand",
        "ownHistory",
        "importedHistory",
        "configuration",
        "trainedModel"
       ]
      },
      "detail": {
       "type": "string",
       "nullable": true,
       "description": "e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."
      },
      "observations": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "ownDataShare": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."
   },
   "limitedHistory": {
    "type": "boolean"
   },
   "nextStage": {
    "type": "object",
    "nullable": true,
    "description": "What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.",
    "properties": {
     "stage": {
      "type": "string",
      "enum": [
       "learning",
       "established",
       "learned"
      ]
     },
     "needs": {
      "type": "string"
     },
     "expectedBy": {
      "type": "string",
      "format": "date",
      "nullable": true
     }
    }
   }
  }
 },
 "BusinessEventNotificationTriggerMappingView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.business_event (new), marketing.message_trigger, marketing.message_trigger_condition (new), marketing.message_template",
  "description": "One registered business event and the communications mapped to it; also the body of setBusinessEventMapping (readOnly fields are ignored on write).\n",
  "required": [
   "eventId",
   "eventType",
   "sourceModule",
   "priority",
   "status",
   "communications"
  ],
  "properties": {
   "eventId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The event registry entry."
   },
   "eventType": {
    "type": "string",
    "description": "Registered event name, e.g. TicketIssued, MembershipExpiring."
   },
   "sourceModule": {
    "type": "string",
    "enum": [
     "crm",
     "ticketing",
     "membership",
     "waiver",
     "groupSales",
     "customerService",
     "finance",
     "wallet",
     "resourceManagement",
     "accessControl",
     "other"
    ]
   },
   "eventState": {
    "type": "string",
    "readOnly": true,
    "description": "The precise state that fires it (e.g. scanned, not merely sold)."
   },
   "payloadFields": {
    "type": "array",
    "readOnly": true,
    "description": "Fields the event carries, available to templates as variables.",
    "items": {
     "type": "string"
    }
   },
   "priority": {
    "type": "string",
    "enum": [
     "P1",
     "P2",
     "P3",
     "P4"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "inactive"
    ]
   },
   "communications": {
    "type": "array",
    "description": "One entry per mapped message (message_trigger row); several entries make a multi-channel or scheduled trigger.",
    "items": {
     "type": "object",
     "required": [
      "channel",
      "templateId",
      "offsetMinutes",
      "isActive"
     ],
     "properties": {
      "triggerId": {
       "type": "string",
       "format": "uuid",
       "description": "Present on an existing mapping; omit to create one."
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "templateId": {
       "type": "string",
       "format": "uuid"
      },
      "templateName": {
       "type": "string",
       "readOnly": true
      },
      "offsetMinutes": {
       "type": "integer",
       "description": "0 = immediately; negative = before the anchor (T-30 days = -43200)."
      },
      "anchor": {
       "type": "string",
       "enum": [
        "eventTime",
        "performanceStart",
        "visitEnd"
       ]
      },
      "conditions": {
       "type": "array",
       "description": "All must hold (e.g. customer has a valid email and email is permitted; event within 24 hours).",
       "items": {
        "type": "object",
        "required": [
         "dimension",
         "operator"
        ],
        "properties": {
         "dimension": {
          "type": "string",
          "enum": [
           "product",
           "event",
           "venue",
           "brand",
           "customer",
           "channel",
           "time",
           "transactionStatus",
           "membership",
           "bookingType"
          ]
         },
         "operator": {
          "type": "string",
          "enum": [
           "equals",
           "notEquals",
           "in",
           "withinMinutes",
           "isValid",
           "isPermitted"
          ]
         },
         "value": {
          "type": "string"
         }
        }
       }
      },
      "isActive": {
       "type": "boolean"
      }
     }
    }
   }
  }
 },
 "ChannelProviderConfigurationInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.communication_provider",
  "x-ticvai-record-definition": "For each provider",
  "description": "One delivery provider on one channel (the pack's \"For each provider\" record). Rate limits, timeout and the retry policy apply to every message routed through it; routing between providers is `listRoutingPriorityThrottling`.\n",
  "required": [
   "providerName",
   "channel",
   "account",
   "environment",
   "credentialsSecretRef",
   "role",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "providerName": {
    "type": "string",
    "maxLength": 120
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "account": {
    "type": "string",
    "maxLength": 200,
    "description": "The account or sub-account identifier at the provider."
   },
   "environment": {
    "type": "string",
    "enum": [
     "production",
     "sandbox"
    ]
   },
   "region": {
    "type": "string",
    "description": "Provider data region (e.g. eu-west, me-central); also a routing selector."
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "description": "ISO 3166-1 alpha-2; set when this provider serves one country only."
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "description": "Set when this provider serves one brand only."
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "description": "Set when this provider serves one legal entity only."
   },
   "credentialsSecretRef": {
    "type": "string",
    "description": "Reference into the secret store; the secret itself is never sent, stored or shown."
   },
   "apiConfiguration": {
    "type": "object",
    "additionalProperties": true,
    "description": "Non-secret API settings (base URL, API version, provider-specific options)."
   },
   "webhookConfiguration": {
    "type": "object",
    "properties": {
     "callbackUrl": {
      "type": "string",
      "format": "uri"
     },
     "signingSecretRef": {
      "type": "string",
      "description": "Reference into the secret store for the webhook signing key."
     }
    }
   },
   "rateLimitPerSecond": {
    "type": "integer",
    "minimum": 1
   },
   "rateLimitPerMinute": {
    "type": "integer",
    "minimum": 1
   },
   "timeoutSeconds": {
    "type": "integer",
    "minimum": 1
   },
   "retryPolicy": {
    "type": "object",
    "description": "Waits between attempts, then what happens when they are spent (e.g. 1 min, 5 min, then fallback provider).",
    "required": [
     "waitsSeconds",
     "onExhausted"
    ],
    "properties": {
     "waitsSeconds": {
      "type": "array",
      "maxItems": 10,
      "items": {
       "type": "integer",
       "minimum": 0
      }
     },
     "onExhausted": {
      "type": "string",
      "enum": [
       "fallbackProvider",
       "deadLetter"
      ]
     }
    }
   },
   "role": {
    "type": "string",
    "enum": [
     "primary",
     "secondary",
     "emergencyFallback"
    ]
   },
   "priority": {
    "type": "integer",
    "minimum": 1,
    "description": "Order among providers with the same role and selectors; 1 is tried first."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "standby",
     "degraded",
     "suspended",
     "disabled"
    ]
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "ChannelProviderConfigurationView": {
  "x-ticvai-persistence": "none — the marketing.communication_provider row plus its latest verification",
  "description": "The stored provider record and the outcome of the checks run on save.",
  "allOf": [
   {
    "$ref": "#/components/schemas/ChannelProviderConfigurationInput"
   },
   {
    "type": "object",
    "properties": {
     "lastVerification": {
      "type": "object",
      "readOnly": true,
      "properties": {
       "checkedAt": {
        "type": "string",
        "format": "date-time"
       },
       "credentialsValid": {
        "type": "boolean"
       },
       "connectionOk": {
        "type": "boolean"
       },
       "webhookOk": {
        "type": "boolean"
       },
       "deliveryReceiptOk": {
        "type": "boolean"
       },
       "message": {
        "type": "string"
       }
      }
     }
    }
   }
  ]
 },
 "CommunicationServiceCommandCenterView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)",
  "description": "Platform KPIs and breakdowns for the communication service over the requested window. Counts are messages (one dispatch = one message on one channel), not recipients.\n",
  "required": [
   "windowFrom",
   "windowTo",
   "messagesProcessed",
   "byChannel",
   "byModule"
  ],
  "properties": {
   "windowFrom": {
    "type": "string",
    "format": "date-time"
   },
   "windowTo": {
    "type": "string",
    "format": "date-time"
   },
   "messagesProcessed": {
    "type": "integer",
    "minimum": 0,
    "description": "Messages accepted by the service in the window (the pack's \"Messages Processed Today\")."
   },
   "delivered": {
    "type": "integer",
    "minimum": 0
   },
   "failed": {
    "type": "integer",
    "minimum": 0
   },
   "pending": {
    "type": "integer",
    "minimum": 0
   },
   "retrying": {
    "type": "integer",
    "minimum": 0
   },
   "averageDeliverySeconds": {
    "type": "number",
    "minimum": 0,
    "description": "Mean time from acceptance to provider-confirmed delivery, in (fractional) seconds."
   },
   "providerAvailabilityRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Share of the window the active providers were reachable, weighted by volume."
   },
   "byChannel": {
    "type": "array",
    "description": "Sent volume and health per channel, one row per provider on it (the pack's channel tiles and Channel Health table).",
    "items": {
     "type": "object",
     "required": [
      "channel",
      "sent"
     ],
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "providerName": {
       "type": "string"
      },
      "sent": {
       "type": "integer",
       "minimum": 0
      },
      "successRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "averageLatencySeconds": {
       "type": "number",
       "minimum": 0
      },
      "health": {
       "type": "string",
       "enum": [
        "healthy",
        "warning",
        "critical"
       ]
      }
     }
    }
   },
   "byModule": {
    "type": "array",
    "description": "Volume originating from each TICVAI module.",
    "items": {
     "type": "object",
     "required": [
      "module",
      "volume"
     ],
     "properties": {
      "module": {
       "type": "string",
       "enum": [
        "crm",
        "ticketing",
        "membership",
        "waiver",
        "groupSales",
        "customerService",
        "finance",
        "wallet",
        "resourceManagement",
        "accessControl",
        "other"
       ]
      },
      "volume": {
       "type": "integer",
       "minimum": 0
      },
      "successRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "averageLatencySeconds": {
       "type": "number",
       "minimum": 0
      },
      "health": {
       "type": "string",
       "enum": [
        "healthy",
        "warning",
        "critical"
       ]
      }
     }
    }
   },
   "alerts": {
    "type": "array",
    "description": "Live operational alerts (failure-rate spikes, queued backlogs, providers near their rate limit).",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "severity",
      "message",
      "raisedAt"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "failureRateSpike",
        "queueBacklog",
        "rateLimitApproaching",
        "providerDegraded",
        "other"
       ]
      },
      "severity": {
       "type": "string",
       "enum": [
        "info",
        "warning",
        "critical"
       ]
      },
      "message": {
       "type": "string"
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "raisedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "aiHealthSummary": {
    "type": "string",
    "description": "AI-written plain-language summary of platform health; absent when AI processing is off for the tenant."
   }
  }
 },
 "ConsentDecision": {
  "type": "string",
  "enum": [
   "granted",
   "withdrawn",
   "notAsked"
  ]
 },
 "ConsentPreferenceCommunicationPolicyEnforcementView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.communication_policy_decision",
  "description": "One policy evaluation of one communication, with the inputs as they stood when it was evaluated. Append-only evidence; retained per the tenant's retention policy (ADR-0047). **Job note:** written by the dispatch worker behind `sendTransactionalMessage` and campaign sends (`launchCampaign`) as it evaluates each message, never by an operation of its own (decided 29 September, writers pass; DM6).\n",
  "required": [
   "id",
   "communicationId",
   "subjectId",
   "messageClass",
   "channel",
   "decision",
   "evaluatedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "communicationId": {
    "type": "string",
    "description": "marketing.message_dispatch id."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "messageClass": {
    "type": "string",
    "enum": [
     "transactional",
     "operational",
     "service",
     "marketing"
    ]
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "marketingConsent": {
    "$ref": "#/components/schemas/ConsentDecision"
   },
   "emailPreference": {
    "type": "boolean"
   },
   "smsPreference": {
    "type": "boolean"
   },
   "whatsappPreference": {
    "type": "boolean"
   },
   "pushPreference": {
    "type": "boolean"
   },
   "language": {
    "type": "string",
    "description": "Preferred language (BCP 47) used to pick the template language."
   },
   "contactRestricted": {
    "type": "boolean",
    "description": "A contact restriction (e.g. do-not-contact, legal hold) applied."
   },
   "jurisdiction": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "description": "Country whose policy was applied."
   },
   "suppressionReason": {
    "type": "string",
    "enum": [
     "unsubscribed",
     "invalidEmail",
     "invalidMobile",
     "hardBounce",
     "complaint",
     "administrative"
    ]
   },
   "decision": {
    "type": "string",
    "enum": [
     "allowed",
     "blocked",
     "rerouted",
     "suppressed"
    ]
   },
   "reasons": {
    "type": "array",
    "description": "Why the decision was reached; empty when allowed with nothing notable.",
    "items": {
     "type": "string",
     "enum": [
      "noMarketingConsent",
      "channelPreferenceOff",
      "optedOut",
      "suppressed",
      "contactRestricted",
      "jurisdictionPolicy",
      "channelUnavailable"
     ]
    }
   },
   "reroutedToChannel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "evaluatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DeliveryQueueFailureRetryManagementView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.message_template, marketing.communication_provider (new)",
  "description": "One communication in the delivery queue and where it stands.",
  "required": [
   "communicationId",
   "channel",
   "status",
   "attempts",
   "createdAt"
  ],
  "properties": {
   "communicationId": {
    "type": "string",
    "description": "marketing.message_dispatch id."
   },
   "sourceModule": {
    "type": "string",
    "enum": [
     "crm",
     "ticketing",
     "membership",
     "waiver",
     "groupSales",
     "customerService",
     "finance",
     "wallet",
     "resourceManagement",
     "accessControl",
     "other"
    ]
   },
   "businessEvent": {
    "type": "string",
    "description": "The originating event type, e.g. TicketIssued."
   },
   "businessEventId": {
    "type": "string",
    "description": "The originating event instance, kept so a failed message can be replayed with its context."
   },
   "recipient": {
    "type": "string",
    "description": "Address or number, masked (e.g. j***@example.com) unless the caller holds GUEST_VIEW_PII."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "template": {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "code": {
      "type": "string"
     },
     "name": {
      "type": "string"
     }
    }
   },
   "provider": {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "name": {
      "type": "string"
     }
    }
   },
   "priority": {
    "type": "string",
    "enum": [
     "P1",
     "P2",
     "P3",
     "P4"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "processing",
     "sent",
     "delivered",
     "failed",
     "retrying",
     "deadLettered",
     "cancelled"
    ]
   },
   "attempts": {
    "type": "integer",
    "minimum": 0
   },
   "lastFailureCategory": {
    "type": "string",
    "enum": [
     "providerUnavailable",
     "invalidAddress",
     "invalidMobile",
     "rateLimited",
     "authenticationError",
     "templateRejected",
     "timeout",
     "consentBlock",
     "unknownError"
    ]
   },
   "lastFailureMessage": {
    "type": "string"
   },
   "nextAttemptAt": {
    "type": "string",
    "format": "date-time"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "sentAt": {
    "type": "string",
    "format": "date-time"
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
 "ProviderHealthUsageCostMonitoringView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)",
  "description": "Provider reliability, usage and cost for the window and filters.",
  "required": [
   "windowFrom",
   "windowTo",
   "volume",
   "providers"
  ],
  "properties": {
   "windowFrom": {
    "type": "string",
    "format": "date-time"
   },
   "windowTo": {
    "type": "string",
    "format": "date-time"
   },
   "volume": {
    "type": "integer",
    "minimum": 0
   },
   "successRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "failureRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "averageDeliverySeconds": {
    "type": "number",
    "minimum": 0
   },
   "averageApiLatencySeconds": {
    "type": "number",
    "minimum": 0
   },
   "availabilityRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "retries": {
    "type": "integer",
    "minimum": 0
   },
   "fallbackCount": {
    "type": "integer",
    "minimum": 0,
    "description": "Messages delivered through a fallback provider or channel."
   },
   "cost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "costPerMessage": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providers": {
    "type": "array",
    "description": "Provider comparison.",
    "items": {
     "type": "object",
     "required": [
      "providerId",
      "channel",
      "volume"
     ],
     "properties": {
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "providerName": {
       "type": "string"
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "volume": {
       "type": "integer",
       "minimum": 0
      },
      "successRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      },
      "averageDeliverySeconds": {
       "type": "number",
       "minimum": 0
      },
      "costPerThousand": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "health": {
       "type": "string",
       "enum": [
        "healthy",
        "warning",
        "critical"
       ]
      }
     }
    }
   },
   "breakdown": {
    "type": "array",
    "description": "Usage and cost per value of the groupBy dimension.",
    "items": {
     "type": "object",
     "required": [
      "key",
      "volume"
     ],
     "properties": {
      "key": {
       "type": "string",
       "description": "The dimension value's id or code."
      },
      "label": {
       "type": "string"
      },
      "volume": {
       "type": "integer",
       "minimum": 0
      },
      "cost": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "alerts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "message",
      "raisedAt"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "budgetThreshold",
        "successRateBelowTarget",
        "latencyAboveTarget",
        "slaBreach"
       ]
      },
      "message": {
       "type": "string"
      },
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "raisedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "slaTargets": {
    "type": "array",
    "description": "Contractual provider targets, only where configured.",
    "items": {
     "type": "object",
     "required": [
      "providerId",
      "metric",
      "target"
     ],
     "properties": {
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "metric": {
       "type": "string",
       "enum": [
        "successRate",
        "availabilityRate",
        "averageDeliverySeconds"
       ]
      },
      "target": {
       "type": "number"
      },
      "observed": {
       "type": "number"
      },
      "met": {
       "type": "boolean"
      }
     }
    }
   },
   "aiRecommendations": {
    "type": "array",
    "description": "Advisory provider changes on cost/performance trade-offs.",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "RoutingPriorityThrottlingFallbackRulesView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.communication_routing_rule",
  "description": "One routing rule, read by listRoutingPriorityThrottling and written by setCommunicationRoutingRule. Unset selectors match anything; a rule with more selectors set is more specific.\n",
  "required": [
   "id",
   "channel",
   "providers",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$"
   },
   "brandId": {
    "type": "string",
    "format": "uuid"
   },
   "messageClass": {
    "type": "string",
    "enum": [
     "transactional",
     "operational",
     "service",
     "marketing"
    ]
   },
   "priorityClass": {
    "type": "string",
    "enum": [
     "P1",
     "P2",
     "P3",
     "P4"
    ]
   },
   "recipientType": {
    "type": "string",
    "enum": [
     "customer",
     "partner",
     "employee"
    ]
   },
   "providers": {
    "type": "array",
    "description": "Tried in order; a provider below minimum health is skipped.",
    "items": {
     "type": "object",
     "required": [
      "providerId",
      "role"
     ],
     "properties": {
      "providerId": {
       "type": "string",
       "format": "uuid"
      },
      "providerName": {
       "type": "string",
       "readOnly": true
      },
      "role": {
       "type": "string",
       "enum": [
        "primary",
        "secondary",
        "emergencyFallback"
       ]
      }
     }
    }
   },
   "skipUnhealthyProviders": {
    "type": "boolean",
    "description": "Route past providers whose health is degraded or worse."
   },
   "costAware": {
    "type": "boolean",
    "description": "Among providers meeting the service and compliance rules, prefer the cheapest."
   },
   "channelFallback": {
    "type": "array",
    "description": "Alternate channels, in order, when delivery on this channel fails; used only where consent and preferences permit.",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "throttle": {
    "type": "object",
    "properties": {
     "messagesPerSecond": {
      "type": "integer",
      "minimum": 1
     },
     "messagesPerMinute": {
      "type": "integer",
      "minimum": 1
     },
     "brandMessagesPerMinute": {
      "type": "integer",
      "minimum": 1,
      "description": "Cap across every rule for the same brand."
     },
     "eventMessagesPerMinute": {
      "type": "integer",
      "minimum": 1,
      "description": "Cap per originating business event."
     }
    }
   },
   "isActive": {
    "type": "boolean"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "SenderIdentityDomainBrandConfigurationInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.sender_identity",
  "description": "One identity TICVAI sends from, bound to one brand. Fields apply by channel: email uses sendingDomain/fromName/fromAddress/replyTo; sms uses senderId/country/approvedUses; whatsapp uses businessAccount/phoneNumber/country; push uses application/platform/environment.\n",
  "required": [
   "channel",
   "brandId",
   "providerId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "brandId": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "region": {
    "type": "string"
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "description": "ISO 3166-1 alpha-2 (required for sms and whatsapp)."
   },
   "providerId": {
    "type": "string",
    "format": "uuid",
    "description": "The marketing.communication_provider row this identity is registered with."
   },
   "sendingDomain": {
    "type": "string",
    "maxLength": 253
   },
   "fromName": {
    "type": "string",
    "maxLength": 120
   },
   "fromAddress": {
    "type": "string",
    "format": "email"
   },
   "replyTo": {
    "type": "string",
    "format": "email"
   },
   "senderId": {
    "type": "string",
    "maxLength": 15,
    "description": "Alphanumeric or numeric SMS sender ID as registered in the country."
   },
   "approvedUses": {
    "type": "array",
    "description": "Communication classes this sender may carry.",
    "items": {
     "type": "string",
     "enum": [
      "transactional",
      "operational",
      "service",
      "marketing"
     ]
    }
   },
   "businessAccount": {
    "type": "string",
    "description": "WhatsApp business account identifier at the provider."
   },
   "phoneNumber": {
    "type": "string",
    "pattern": "^\\+[1-9][0-9]{6,14}$",
    "description": "E.164."
   },
   "application": {
    "type": "string",
    "description": "Push application identifier (bundle id / package name)."
   },
   "platform": {
    "type": "string",
    "enum": [
     "ios",
     "android",
     "web"
    ]
   },
   "environment": {
    "type": "string",
    "enum": [
     "production",
     "sandbox"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingVerification",
     "verified",
     "active",
     "suspended",
     "expired"
    ],
    "description": "Set by verification except `active` and `suspended`, which a caller may request."
   },
   "approvedTemplateIds": {
    "type": "array",
    "readOnly": true,
    "description": "WhatsApp templates the provider has approved for this number (marketing.message_template ids).",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "SenderIdentityDomainBrandConfigurationView": {
  "x-ticvai-persistence": "none — the marketing.sender_identity row plus its verification timestamps",
  "description": "The stored sender identity and when it was last verified.",
  "allOf": [
   {
    "$ref": "#/components/schemas/SenderIdentityDomainBrandConfigurationInput"
   },
   {
    "type": "object",
    "properties": {
     "verifiedAt": {
      "type": "string",
      "format": "date-time",
      "readOnly": true
     },
     "verificationExpiresAt": {
      "type": "string",
      "format": "date-time",
      "readOnly": true
     }
    }
   }
  ]
 },
 "Suggestion": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion",
  "description": "One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n",
  "required": [
   "id",
   "kind",
   "basis",
   "maturity",
   "producedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/SuggestionKind"
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "scopePath": {
    "type": "string"
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "What it is about — a product, an outlet, an item, a party."
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "description": "The suggestion itself. Shape depends on `kind`."
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1,
    "description": "**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"
   },
   "explanation": {
    "type": "string",
    "description": "**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"
   },
   "inputs": {
    "type": "object",
    "additionalProperties": true,
    "description": "What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"
   },
   "producerRef": {
    "type": "string",
    "description": "The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"
   }
  }
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "SuggestionKind": {
  "type": "string",
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline.\n",
  "enum": [
   "price",
   "replenishment",
   "requisition",
   "demandForecast",
   "prepPlan",
   "menuEngineering",
   "staffing",
   "slaTarget",
   "waitTime",
   "upsell",
   "segmentation",
   "anomaly",
   "scenario",
   "sendTime",
   "wasteRisk",
   "queueBalancing",
   "itinerary"
  ]
 },
 "SystemTransactionalTemplateRegistryView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.message_template, marketing.message_template_version (new), marketing.message_trigger",
  "description": "One version of one template on one channel and language, with its content and variables.",
  "required": [
   "templateId",
   "code",
   "name",
   "channel",
   "language",
   "version",
   "status",
   "ownership"
  ],
  "properties": {
   "templateId": {
    "type": "string",
    "format": "uuid",
    "description": "marketing.message_template id."
   },
   "code": {
    "type": "string",
    "description": "The human template ID (e.g. TICKET_CONFIRMATION)."
   },
   "name": {
    "type": "string"
   },
   "businessEvent": {
    "type": "string",
    "description": "The registered business event this template answers (e.g. TicketIssued)."
   },
   "sourceModule": {
    "type": "string",
    "enum": [
     "crm",
     "ticketing",
     "membership",
     "waiver",
     "groupSales",
     "customerService",
     "finance",
     "wallet",
     "resourceManagement",
     "accessControl",
     "other"
    ]
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "brandId": {
    "type": "string",
    "format": "uuid"
   },
   "language": {
    "type": "string",
    "description": "BCP 47 tag."
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "archived"
    ]
   },
   "ownership": {
    "type": "string",
    "enum": [
     "platform",
     "crm"
    ],
    "description": "platform = transactional template owned here; crm = marketing template owned by CRM."
   },
   "subject": {
    "type": "string"
   },
   "header": {
    "type": "string"
   },
   "body": {
    "type": "string"
   },
   "footer": {
    "type": "string"
   },
   "ctaLabel": {
    "type": "string"
   },
   "ctaUrl": {
    "type": "string",
    "description": "May contain variables, e.g. {{TicketLink}}."
   },
   "attachmentKinds": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "ticketPdf",
      "invoicePdf",
      "walletPass",
      "calendarInvite",
      "waiverPdf"
     ]
    }
   },
   "variables": {
    "type": "array",
    "description": "Dynamic variables the content uses (e.g. CustomerName, OrderNumber, EventDate, AmountDue).",
    "items": {
     "type": "string"
    }
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 }
}
```
