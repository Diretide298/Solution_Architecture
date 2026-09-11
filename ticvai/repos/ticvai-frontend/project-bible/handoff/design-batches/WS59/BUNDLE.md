# WS59 — Ticket Media   Credential Management board 1

**10 screens · 10 operations · 11 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ACCESS_POINT_CONFIGURE, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-334` | Virtual Ticket Command Center | commandCentre | 1 | 0 | — |
| `BO-335` | Virtual Ticket Identity & Master Record Configuration | configEditor | 1 | 0 | — |
| `BO-336` | Virtual Ticket Status & Lifecycle Model | listDetail | 1 | 0 | — |
| `BO-337` | Media Type & Credential Technology Registry | configEditor | 1 | 0 | — |
| `BO-338` | Multi-Media Binding & Association Rules | configEditor | 1 | 0 | — |
| `BO-339` | Credential Identity, Token & Reference Mapping | listDetail | 1 | 0 | — |
| `BO-340` | Entitlement & Cross-Media Synchronization Rules | listDetail | 1 | 0 | — |
| `BO-341` | Media Activation, Priority & Fallback Rules | configEditor | 1 | 0 | — |
| `BO-342` | Media Replacement, Revocation & Rebinding Rules | configEditor | 1 | 2 | — |
| `BO-343` | Virtual Ticket Architecture Testing, Governance & Audit | configEditor | 1 | 0 | — |

## Thin screens in this batch

**BO-336, BO-339, BO-340 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-334",
  "name": "Virtual Ticket Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.1",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/virtual-ticket-command-center-bo-334",
   "component": "apps/venue-management-web/src/routes/access-venue/VirtualTicketCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-335",
    "BO-336",
    "BO-337",
    "BO-338",
    "BO-339",
    "BO-340",
    "BO-341",
    "BO-342",
    "BO-343"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-335",
     "trigger": "Works in Virtual Ticket Identity & Master Record Configuration",
     "provenance": "flow F168 step 1→2",
     "operation": "listVirtualTicket"
    },
    {
     "to": "BO-336",
     "trigger": "Works in Virtual Ticket Status & Lifecycle Model",
     "provenance": "flow F168 step 3→4",
     "operation": "listVirtualTicket"
    },
    {
     "to": "BO-337",
     "trigger": "Works in Media Type & Credential Technology Registry",
     "provenance": "flow F168 step 5→6",
     "operation": "listVirtualTicket"
    },
    {
     "to": "BO-338",
     "trigger": "Works in Multi-Media Binding & Association Rules",
     "provenance": "flow F168 step 7→8",
     "operation": "listVirtualTicket"
    },
    {
     "to": "BO-339",
     "trigger": "Works in Credential Identity, Token & Reference Mapping",
     "provenance": "flow F168 step 9→10",
     "operation": "listVirtualTicket"
    },
    {
     "to": "BO-340",
     "trigger": "Works in Entitlement & Cross-Media Synchronization Rules",
     "provenance": "flow F168 step 11→12",
     "operation": "listVirtualTicket"
    },
    {
     "to": "BO-341",
     "trigger": "Works in Media Activation, Priority & Fallback Rules",
     "provenance": "flow F168 step 13→14",
     "operation": "listVirtualTicket"
    },
    {
     "to": "BO-342",
     "trigger": "Works in Media Replacement, Revocation & Rebinding Rules",
     "provenance": "flow F168 step 15→16",
     "operation": "listVirtualTicket"
    },
    {
     "to": "BO-343",
     "trigger": "Works in Virtual Ticket Architecture Testing, Governance & Audit",
     "provenance": "flow F168 step 17→18",
     "operation": "listVirtualTicket"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population",
  "purpose": "Provide administrators and operations teams with a centralized view of all Virtual Tickets and their associated media across TICVAI. This is the primary administrative entry point into the Virtual Ticket architecture.",
  "purposeNote": "Authorized users can locate any Virtual Ticket and immediately understand its ticket status, entitlement, usage state and all associated media from one centralized workspace.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search virtual ticket",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Brand",
        "Venue",
        "Event",
        "VirtualTicketCommandCenterView.product",
        "Performance",
        "VirtualTicketCommandCenterView.ticketType",
        "Channel",
        "Customer",
        "Virtual Ticket Status",
        "Media Type",
        "Number of Media",
        "Validity",
        "VirtualTicketCommandCenterView.usageStatus"
       ],
       "notes": "The pack filters this screen by brand, venue, event, product, performance, ticket type and 7 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Virtual Tickets",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.totalVirtualTickets"
      },
      {
       "kind": "metricTile",
       "label": "Active",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.active"
      },
      {
       "kind": "metricTile",
       "label": "Pending Activation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.pendingActivation"
      },
      {
       "kind": "metricTile",
       "label": "Suspended",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.suspended"
      },
      {
       "kind": "metricTile",
       "label": "Used / Consumed",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.usedConsumed"
      },
      {
       "kind": "metricTile",
       "label": "Partially Consumed",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.partiallyConsumed"
      },
      {
       "kind": "metricTile",
       "label": "Expired",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.expired"
      },
      {
       "kind": "metricTile",
       "label": "Cancelled",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.cancelled"
      },
      {
       "kind": "metricTile",
       "label": "Revoked",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.revoked"
      },
      {
       "kind": "metricTile",
       "label": "Virtual Tickets with Multiple Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.virtualTicketsWithMultipleMedia"
      },
      {
       "kind": "metricTile",
       "label": "Virtual Tickets with No Active Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Media Binding Exceptions",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.mediaBindingExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Credential Synchronization Issues",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterView.credentialSynchronizationIssues"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every virtual ticket",
       "columns": [
        "VirtualTicketCommandCenterView.virtualTicketId",
        "VirtualTicketCommandCenterView.product",
        "VirtualTicketCommandCenterView.eventPerformance",
        "VirtualTicketCommandCenterView.ticketHolder",
        "VirtualTicketCommandCenterView.orderReference",
        "VirtualTicketCommandCenterView.ticketType",
        "VirtualTicketCommandCenterView.seatResourceWhereApplicable",
        "VirtualTicketCommandCenterView.validFromTo",
        "VirtualTicketCommandCenterView.ticketStatus",
        "VirtualTicketCommandCenterView.usageStatus",
        "VirtualTicketCommandCenterView.numberOfLinkedMedia",
        "VirtualTicketCommandCenterView.primaryMedia",
        "VirtualTicketCommandCenterView.lastCredentialActivity",
        "VirtualTicketCommandCenterView.lastModified"
       ],
       "bindsTo": "VirtualTicketCommandCenterView",
       "operation": "listVirtualTicket",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Each record should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected virtual ticket",
       "bindsTo": "VirtualTicketCommandCenterView",
       "columns": [
        "VirtualTicketCommandCenterView.virtualTicketId",
        "VirtualTicketCommandCenterView.product",
        "VirtualTicketCommandCenterView.eventPerformance",
        "VirtualTicketCommandCenterView.ticketHolder",
        "VirtualTicketCommandCenterView.orderReference",
        "VirtualTicketCommandCenterView.ticketType",
        "VirtualTicketCommandCenterView.seatResourceWhereApplicable",
        "VirtualTicketCommandCenterView.validFromTo",
        "VirtualTicketCommandCenterView.ticketStatus",
        "VirtualTicketCommandCenterView.usageStatus",
        "VirtualTicketCommandCenterView.numberOfLinkedMedia",
        "VirtualTicketCommandCenterView.primaryMedia",
        "VirtualTicketCommandCenterView.lastCredentialActivity",
        "VirtualTicketCommandCenterView.lastModified"
       ],
       "notes": "The pack groups this record's detail under its own headings: “VT-2026-009821”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Each record should show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** View Virtual Ticket, View Media, Bind Media, Replace Media, Suspend, Reactivate, Revoke Media, View Usage, View Audit, Diagnose Credential. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Authorized users may"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The virtual ticket list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the virtual ticket untouched.",
   "emptyFirstRun": "No virtual ticket yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the virtual ticket are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVirtualTicket",
    "contract": "access",
    "purpose": "Virtual Ticket Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-334"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 4. 29 of 39 labels bound to a contract property; 50 of 69 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-335",
  "name": "Virtual Ticket Identity & Master Record Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.2",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/virtual-ticket-identity-master-record-configuration-bo-335",
   "component": "apps/venue-management-web/src/routes/access-venue/VirtualTicketIdentityMasterRecordConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-334"
   ],
   "exitTo": [
    "BO-334"
   ],
   "inferred": false,
   "notes": "**Reached from BO-334, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-334",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F168 step 2→3",
     "operation": "setVirtualTicketIdentity"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define the authoritative Virtual Ticket object used throughout TICVAI. This screen is extremely important because the Virtual Ticket—not the QR/RFID/card— is the master ticket record.",
  "purposeNote": "Every issued ticket has one persistent, media-independent Virtual Ticket identity that remains authoritative regardless of which credential technologies are attached to it.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "ID generation pattern",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Ticket classification",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Ticket ownership model",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Holder assignment requirements",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transferability reference",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Validity model",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Consumption model",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Entitlement model",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 6 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Media requirements",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 6 §Configure"
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
       "provenance": "contract operation setVirtualTicketIdentity"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The virtual ticket identity configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the virtual ticket identity untouched.",
   "emptyFirstRun": "No virtual ticket identity configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVirtualTicketIdentity",
    "contract": "access",
    "purpose": "Virtual Ticket Identity & Master Record Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setVirtualTicketIdentity"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-335"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 9 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-336",
  "name": "Virtual Ticket Status & Lifecycle Model",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.3",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/virtual-ticket-status-lifecycle-model-bo-336",
   "component": "apps/venue-management-web/src/routes/access-venue/VirtualTicketStatusLifecycleModel.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-334"
   ],
   "exitTo": [
    "BO-334"
   ],
   "inferred": false,
   "notes": "**Reached from BO-334, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-334",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F168 step 4→5",
     "operation": "listVirtualTicketStatus"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the standardized lifecycle of a Virtual Ticket independently from the lifecycle of individual media.",
  "purposeNote": "state changes across every credential associated with that ticket.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 8"
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
       "impliedBy": "listVirtualTicketStatus",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The virtual ticket status list.",
   "error": "Could not load. Names which read failed and leaves the virtual ticket status untouched.",
   "emptyFirstRun": "No virtual ticket status yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the virtual ticket status are still there. The pack's own statuses are Order Management — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVirtualTicketStatus",
    "contract": "access",
    "purpose": "Virtual Ticket Status & Lifecycle Model",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "VirtualTicketStatusLifecycleModelView.withGovernedAlternativeStates",
    "VirtualTicketStatusLifecycleModelView.suspended",
    "VirtualTicketStatusLifecycleModelView.cancelled",
    "VirtualTicketStatusLifecycleModelView.voided",
    "VirtualTicketStatusLifecycleModelView.reissuedSuperseded"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-336"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 11 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-337",
  "name": "Media Type & Credential Technology Registry",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.4",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-type-credential-technology-registry-bo-337",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaTypeCredentialTechnologyRegistry.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-334"
   ],
   "exitTo": [
    "BO-334"
   ],
   "inferred": false,
   "notes": "**Reached from BO-334, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-334",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F168 step 6→7",
     "operation": "listMediaTypeCredential"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§For each technology configure) and no display directory — it is settings, not a population",
  "purpose": "Maintain the centralized catalogue of credential technologies supported by TICVAI. This makes the credential architecture extensible rather than hard-coded.",
  "purposeNote": "technologies with their capabilities, providers and technical behavior.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Media Type ID",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Name",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Category",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Provider",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Technology",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Token format",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Generation method",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Validation mechanism",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Supports visual design",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Supports dynamic update",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Supports revocation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Supports expiration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Supports offline reference",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Supports replacement",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Supports encryption/signing",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Supported channels",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Supported devices",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      },
      {
       "kind": "selectField",
       "label": "Integration adapter",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 9 §For each technology configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The media type credential configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the media type credential untouched.",
   "emptyFirstRun": "No media type credential configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaTypeCredential",
    "contract": "access",
    "purpose": "Media Type & Credential Technology Registry",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-337"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 18 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-338",
  "name": "Multi-Media Binding & Association Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.5",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/multi-media-binding-association-rules-bo-338",
   "component": "apps/venue-management-web/src/routes/access-venue/MultiMediaBindingAssociationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-334"
   ],
   "exitTo": [
    "BO-334"
   ],
   "inferred": false,
   "notes": "**Reached from BO-334, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-334",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F168 step 8→9",
     "operation": "listMultiMediaBinding"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how one Virtual Ticket can be associated with multiple media simultaneously. This is one of the most important screens in Area 15.",
  "purposeNote": "Ticket without creating duplicate ticket entitlements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Allowed media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mandatory media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Optional media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum active media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum media required",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Primary media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Secondary media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Backup media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Temporary media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Media combination",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Simultaneous activation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Exclusive activation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 11 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-media binding association configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the multi-media binding association untouched.",
   "emptyFirstRun": "No multi-media binding association configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMultiMediaBinding",
    "contract": "access",
    "purpose": "Multi-Media Binding & Association Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-338"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 12 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-339",
  "name": "Credential Identity, Token & Reference Mapping",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.6",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-identity-token-reference-mapping-bo-339",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialIdentityTokenReferenceMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-334"
   ],
   "exitTo": [
    "BO-334"
   ],
   "inferred": false,
   "notes": "**Reached from BO-334, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-334",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F168 step 10→11",
     "operation": "listCredentialIdentityToken"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define how individual media identifiers resolve securely back to the authoritative Virtual Ticket.",
  "purposeNote": "Every supported credential can securely and consistently resolve to its authoritative Virtual Ticket without duplicating ticket entitlement data within individual media.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 12"
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
       "impliedBy": "listCredentialIdentityToken",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential identity token list.",
   "error": "Could not load. Names which read failed and leaves the credential identity token untouched.",
   "emptyFirstRun": "No credential identity token yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential identity token are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialIdentityToken",
    "contract": "access",
    "purpose": "Credential Identity, Token & Reference Mapping",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialIdentityTokenReferenceMappingView.qrToken",
    "CredentialIdentityTokenReferenceMappingView.rfidUid",
    "CredentialIdentityTokenReferenceMappingView.walletObject",
    "CredentialIdentityTokenReferenceMappingView.nfcToken",
    "CredentialIdentityTokenReferenceMappingView.faceReference"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-339"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-340",
  "name": "Entitlement & Cross-Media Synchronization Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.7",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/entitlement-cross-media-synchronization-rules-bo-340",
   "component": "apps/venue-management-web/src/routes/access-venue/EntitlementCrossMediaSynchronizationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-334"
   ],
   "exitTo": [
    "BO-334"
   ],
   "inferred": false,
   "notes": "**Reached from BO-334, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-334",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F168 step 12→13",
     "operation": "listEntitlementCrossMedia"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Ensure all media attached to a Virtual Ticket share the same authoritative ticket and entitlement state.",
  "purposeNote": "All credential media consistently consume and represent the same authoritative Virtual Ticket entitlement and usage state.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every entitlement cross-media synchronization",
       "columns": [
        "EntitlementCrossMediaSynchronizationRulesView.delayedUpdates",
        "EntitlementCrossMediaSynchronizationRulesView.conflictingStates",
        "EntitlementCrossMediaSynchronizationRulesView.offlineTransactionsPendingSynchronization",
        "EntitlementCrossMediaSynchronizationRulesView.providerUpdateFailures",
        "EntitlementCrossMediaSynchronizationRulesView.staleWalletCredentials"
       ],
       "bindsTo": "EntitlementCrossMediaSynchronizationRulesView",
       "operation": "listEntitlementCrossMedia",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 14 §Detect"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected entitlement cross-media synchronization",
       "bindsTo": "EntitlementCrossMediaSynchronizationRulesView",
       "columns": [
        "EntitlementCrossMediaSynchronizationRulesView.delayedUpdates",
        "EntitlementCrossMediaSynchronizationRulesView.conflictingStates",
        "EntitlementCrossMediaSynchronizationRulesView.offlineTransactionsPendingSynchronization",
        "EntitlementCrossMediaSynchronizationRulesView.providerUpdateFailures",
        "EntitlementCrossMediaSynchronizationRulesView.staleWalletCredentials"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Critical Principle”, “For example, TICVAI must prevent”, “Instead”, “Face Credential”, “Virtual Ticket resolved”, “Access transaction recorded”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 14 §Detect"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entitlement cross-media synchronization list.",
   "error": "Could not load. Names which read failed and leaves the entitlement cross-media synchronization untouched.",
   "emptyFirstRun": "No entitlement cross-media synchronization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entitlement cross-media synchronization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEntitlementCrossMedia",
    "contract": "access",
    "purpose": "Entitlement & Cross-Media Synchronization Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "EntitlementCrossMediaSynchronizationRulesView.delayedUpdates",
    "EntitlementCrossMediaSynchronizationRulesView.conflictingStates",
    "EntitlementCrossMediaSynchronizationRulesView.offlineTransactionsPendingSynchronization",
    "EntitlementCrossMediaSynchronizationRulesView.providerUpdateFailures",
    "EntitlementCrossMediaSynchronizationRulesView.staleWalletCredentials"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-340"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 14. 5 of 5 labels bound to a contract property; 17 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-341",
  "name": "Media Activation, Priority & Fallback Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.8",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-activation-priority-fallback-rules-bo-341",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaActivationPriorityFallbackRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-334"
   ],
   "exitTo": [
    "BO-334"
   ],
   "inferred": false,
   "notes": "**Reached from BO-334, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-334",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F168 step 14→15",
     "operation": "listMediaActivationPriority"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure when each credential becomes active and how alternative media behave if the preferred credential cannot be used.",
  "purposeNote": "options without compromising the underlying Virtual Ticket.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Temporary media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Validity duration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "One-time use",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic expiration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Replacement behavior",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Original-media impact",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 15 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "On ticket activation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 15 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The media activation priority configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the media activation priority untouched.",
   "emptyFirstRun": "No media activation priority configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaActivationPriority",
    "contract": "access",
    "purpose": "Media Activation, Priority & Fallback Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-341"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 7 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-342",
  "name": "Media Replacement, Revocation & Rebinding Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.9",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-replacement-revocation-rebinding-rules-bo-342",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaReplacementRevocationRebindingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-334"
   ],
   "exitTo": [
    "BO-334"
   ],
   "inferred": false,
   "notes": "**Reached from BO-334, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-334",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F168 step 16→17",
     "operation": "listMediaReplacementRevocation"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure controlled handling of lost, stolen, damaged, compromised or replaced credential media.",
  "purposeNote": "Credential media can be securely replaced, revoked and rebound while maintaining continuity of the underlying Virtual Ticket and a complete audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Printed ticket replacement, Suspend Media, Revoke Media. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Support"
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
       "label": "Reissue allowed",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number of replacements",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Replacement fee reference",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval required",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Identity verification",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "textField",
       "label": "Old media automatically revoked",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Grace period",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Simultaneous media policy",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reason mandatory",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supervisor approval",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Printed ticket replacement",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Allow immediate"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Allow immediate"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspendMedia",
    "component": "confirmDialog",
    "trigger": "Suspend Media",
    "body": "**Suspend Media on a media replacement revocation is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Allow immediate"
   },
   {
    "id": "confirmRevokeMedia",
    "component": "confirmDialog",
    "trigger": "Revoke Media",
    "body": "**Revoke Media on a media replacement revocation is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Allow immediate"
   }
  ],
  "states": {
   "loading": "The media replacement revocation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the media replacement revocation untouched.",
   "emptyFirstRun": "No media replacement revocation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaReplacementRevocation",
    "contract": "access",
    "purpose": "Media Replacement, Revocation & Rebinding Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-342"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 13 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-343",
  "name": "Virtual Ticket Architecture Testing, Governance & Audit",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "1",
   "number": "15.1.10",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/virtual-ticket-architecture-testing-governance-audit-bo-343",
   "component": "apps/venue-management-web/src/routes/access-venue/VirtualTicketArchitectureTestingGovernanceAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-334"
   ],
   "exitTo": [
    "BO-334"
   ],
   "inferred": false,
   "notes": "**Reached from BO-334, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration Simulator; Configuration Owner; AI Configuration Review) and no display directory — it is settings, not a population",
  "purpose": "Provide the final testing and governance environment for Virtual Ticket and multi-media configurations. Board 1 established what the Virtual Ticket is and how multiple credentials can point to the same authoritative ticket. Board 2 defines how each media type is created, designed, configured, branded, populated with data, previewed, tested and published.",
  "purposeNote": "and retain complete traceability of configuration and credential-binding changes. Board 1 — Final Screen Register",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "→ Technical Review",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 17 §Configuration Owner"
      },
      {
       "kind": "textField",
       "label": "→ Security Review where applicable",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 17 §Configuration Owner"
      },
      {
       "kind": "selectField",
       "label": "→ Operations Review",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 17 §Configuration Owner"
      },
      {
       "kind": "selectField",
       "label": "→ Approval",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 17 §Configuration Owner"
      },
      {
       "kind": "selectField",
       "label": "→ Publication",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 17 §Configuration Owner"
      },
      {
       "kind": "textField",
       "label": "configured lost-credential security policy.”",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 17 §AI Configuration Review"
      },
      {
       "kind": "textField",
       "label": "Replacement/Rebinding → Test & Govern",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 17 §Board 1 configuration flow"
      },
      {
       "kind": "textField",
       "label": "Multi-Format Ticket Media Design Studio—including dedicated design/configuration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 17 §Board 1 configuration flow"
      },
      {
       "kind": "textField",
       "label": "Preview → Validate → Approve & Publish",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 17 §The configuration flow is"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The virtual ticket architecture configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the virtual ticket architecture untouched.",
   "emptyFirstRun": "No virtual ticket architecture configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVirtualTicketArchitecture",
    "contract": "access",
    "purpose": "Virtual Ticket Architecture Testing, Governance & Audit",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-343"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 17. 0 of 0 labels bound to a contract property; 9 of 116 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listCredentialIdentityToken": {
  "method": "GET",
  "path": "/credential-identity-token",
  "contract": "access",
  "summary": "Credential Identity, Token & Reference Mapping",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialIdentityTokenReferenceMappingView"
 },
 "listEntitlementCrossMedia": {
  "method": "GET",
  "path": "/entitlement-cross-media",
  "contract": "access",
  "summary": "Entitlement & Cross-Media Synchronization Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EntitlementCrossMediaSynchronizationRulesView"
 },
 "listMediaActivationPriority": {
  "method": "GET",
  "path": "/media-activation-priority",
  "contract": "access",
  "summary": "Media Activation, Priority & Fallback Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaActivationPriorityFallbackRulesView"
 },
 "listMediaReplacementRevocation": {
  "method": "GET",
  "path": "/media-replacement-revocation",
  "contract": "access",
  "summary": "Media Replacement, Revocation & Rebinding Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaReplacementRevocationRebindingRulesView"
 },
 "listMediaTypeCredential": {
  "method": "GET",
  "path": "/media-type-credential",
  "contract": "access",
  "summary": "Media Type & Credential Technology Registry",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaTypeCredentialTechnologyRegistryView"
 },
 "listMultiMediaBinding": {
  "method": "GET",
  "path": "/multi-media-binding",
  "contract": "access",
  "summary": "Multi-Media Binding & Association Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MultiMediaBindingAssociationRulesView"
 },
 "listVirtualTicket": {
  "method": "GET",
  "path": "/virtual-ticket",
  "contract": "access",
  "summary": "Virtual Ticket Command Center",
  "permission": "SCOPE_VIEW",
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
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "performance",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "customer",
    "in": "query",
    "required": false
   },
   {
    "name": "virtualTicketStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "mediaType",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "VirtualTicketCommandCenterView"
 },
 "listVirtualTicketArchitecture": {
  "method": "GET",
  "path": "/virtual-ticket-architecture",
  "contract": "access",
  "summary": "Virtual Ticket Architecture Testing, Governance & Audit",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VirtualTicketArchitectureTestingGovernanceAuditView"
 },
 "listVirtualTicketStatus": {
  "method": "GET",
  "path": "/virtual-ticket-statu",
  "contract": "access",
  "summary": "Virtual Ticket Status & Lifecycle Model",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VirtualTicketStatusLifecycleModelView"
 },
 "setVirtualTicketIdentity": {
  "method": "PUT",
  "path": "/virtual-ticket-identity",
  "contract": "access",
  "summary": "Virtual Ticket Identity & Master Record Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "VirtualTicketIdentityMasterRecordConfigurationInput",
  "responds": "VirtualTicketIdentityMasterRecordConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CredentialIdentityTokenReferenceMappingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Identity, Token & Reference Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "qrToken": {
    "type": "string",
    "description": "QR Token →"
   },
   "rfidUid": {
    "type": "string",
    "description": "RFID UID →"
   },
   "walletObject": {
    "type": "string",
    "description": "Wallet Object →"
   },
   "nfcToken": {
    "type": "string",
    "description": "NFC Token →"
   },
   "faceReference": {
    "type": "string",
    "description": "Face Reference →"
   },
   "andTheResolverReturns": {
    "type": "string",
    "description": "and the resolver returns"
   },
   "credentialBindingId": {
    "type": "string",
    "description": "Credential Binding ID"
   },
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket ID"
   },
   "mediaType": {
    "type": "string",
    "description": "Media Type"
   },
   "credentialReference": {
    "type": "string",
    "description": "Credential Reference"
   },
   "tokenIdentifier": {
    "type": "string",
    "description": "Token / Identifier"
   },
   "providerReference": {
    "type": "string",
    "description": "Provider Reference"
   },
   "issuedDate": {
    "type": "string",
    "format": "date-time",
    "description": "Issued Date"
   },
   "activationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Activation Date"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "securityProfile": {
    "type": "string",
    "description": "Security profile"
   },
   "tokenization": {
    "type": "string",
    "description": "Tokenization"
   },
   "hashing": {
    "type": "string",
    "description": "Hashing"
   },
   "encryption": {
    "type": "string",
    "description": "Encryption"
   },
   "signedPayloads": {
    "type": "string",
    "description": "Signed payloads"
   },
   "keyReferences": {
    "type": "string",
    "description": "Key references"
   },
   "masking": {
    "type": "string",
    "description": "Masking"
   },
   "dependingOnCredentialTechnology": {
    "type": "string",
    "description": "depending on credential technology"
   }
  }
 },
 "EntitlementCrossMediaSynchronizationRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Entitlement & Cross-Media Synchronization Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "entry": {
    "type": "string",
    "description": "Entry"
   },
   "exit": {
    "type": "string",
    "description": "Exit"
   },
   "redemption": {
    "type": "string",
    "description": "Redemption"
   },
   "partialConsumption": {
    "type": "string",
    "description": "Partial consumption"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "suspension": {
    "type": "string",
    "description": "Suspension"
   },
   "reactivation": {
    "type": "string",
    "description": "Reactivation"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   },
   "replacement": {
    "type": "string",
    "description": "Replacement"
   },
   "mainAdmission": {
    "type": "string",
    "description": "Main admission"
   },
   "delayedUpdates": {
    "type": "string",
    "description": "Delayed updates"
   },
   "conflictingStates": {
    "type": "string",
    "description": "Conflicting states"
   },
   "offlineTransactionsPendingSynchronization": {
    "type": "integer",
    "description": "Offline transactions pending synchronization"
   },
   "providerUpdateFailures": {
    "type": "string",
    "description": "Provider update failures"
   },
   "staleWalletCredentials": {
    "type": "string",
    "description": "Stale wallet credentials"
   }
  }
 },
 "MediaActivationPriorityFallbackRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Activation, Priority & Fallback Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "immediateOnIssuance": {
    "type": "string",
    "description": "Immediate on issuance"
   },
   "onTicketActivation": {
    "type": "string",
    "description": "On ticket activation"
   },
   "onDownload": {
    "type": "string",
    "description": "On download"
   },
   "onWalletInstallation": {
    "type": "string",
    "description": "On wallet installation"
   },
   "onRfidAssignment": {
    "type": "string",
    "description": "On RFID assignment"
   },
   "onFaceEnrollment": {
    "type": "string",
    "description": "On face enrollment"
   },
   "onFirstUse": {
    "type": "string",
    "description": "On first use"
   },
   "onEventDate": {
    "type": "string",
    "format": "date-time",
    "description": "On event date"
   },
   "manualActivation": {
    "type": "string",
    "description": "Manual activation"
   },
   "scheduledActivation": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled activation"
   },
   "temporaryMedia": {
    "type": "string",
    "description": "Temporary media"
   },
   "validityDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Validity duration"
   },
   "oneTimeUse": {
    "type": "string",
    "format": "date-time",
    "description": "One-time use"
   },
   "automaticExpiration": {
    "type": "string",
    "description": "Automatic expiration"
   },
   "replacementBehavior": {
    "type": "string",
    "description": "Replacement behavior"
   },
   "originalMediaImpact": {
    "type": "string",
    "description": "Original-media impact"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   }
  }
 },
 "MediaReplacementRevocationRebindingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Replacement, Revocation & Rebinding Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "lostRfidCard": {
    "type": "string",
    "description": "Lost RFID card"
   },
   "damagedWristband": {
    "type": "string",
    "description": "Damaged wristband"
   },
   "compromisedQr": {
    "type": "string",
    "description": "Compromised QR"
   },
   "newMobileDevice": {
    "type": "integer",
    "description": "New mobile device"
   },
   "walletCredentialReplacement": {
    "type": "string",
    "description": "Wallet credential replacement"
   },
   "faceReEnrollment": {
    "type": "string",
    "description": "Face re-enrollment"
   },
   "printedTicketReplacement": {
    "type": "string",
    "description": "Printed ticket replacement"
   },
   "incorrectCredentialAssignment": {
    "type": "string",
    "description": "Incorrect credential assignment"
   },
   "rfid88721Revoked": {
    "type": "string",
    "description": "RFID-88721 — REVOKED"
   },
   "rfid99211Active": {
    "type": "integer",
    "description": "RFID-99211 — ACTIVE"
   },
   "vt009821Active": {
    "type": "integer",
    "description": "VT-009821 — ACTIVE"
   },
   "numberOfReplacements": {
    "type": "integer",
    "description": "Number of replacements"
   },
   "replacementFeeReference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Replacement fee reference"
   },
   "approvalRequired": {
    "type": "boolean",
    "description": "Approval required"
   },
   "identityVerification": {
    "type": "string",
    "description": "Identity verification"
   },
   "oldMediaAutomaticallyRevoked": {
    "type": "string",
    "description": "Old media automatically revoked"
   },
   "gracePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Grace period"
   },
   "simultaneousMediaPolicy": {
    "type": "string",
    "description": "Simultaneous media policy"
   },
   "reasonMandatory": {
    "type": "string",
    "description": "Reason mandatory"
   },
   "supervisorApproval": {
    "type": "string",
    "description": "Supervisor approval"
   },
   "oldBinding": {
    "type": "string",
    "description": "Old binding"
   },
   "newBinding": {
    "type": "integer",
    "description": "New binding"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "relatedTransaction": {
    "type": "string",
    "description": "Related transaction"
   }
  }
 },
 "MediaTypeCredentialTechnologyRegistryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Type & Credential Technology Registry displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "qr": {
    "type": "string",
    "description": "QR"
   },
   "dynamicQr": {
    "type": "string",
    "description": "Dynamic QR"
   },
   "barcode": {
    "type": "string",
    "description": "Barcode"
   },
   "mobileTicket": {
    "type": "string",
    "description": "Mobile Ticket"
   },
   "pdf": {
    "type": "string",
    "description": "PDF"
   },
   "appleWallet": {
    "type": "string",
    "description": "Apple Wallet"
   },
   "googleWallet": {
    "type": "string",
    "description": "Google Wallet"
   },
   "rfidCard": {
    "type": "string",
    "description": "RFID Card"
   },
   "rfidWristband": {
    "type": "string",
    "description": "RFID Wristband"
   },
   "nfcCard": {
    "type": "string",
    "description": "NFC Card"
   },
   "nfcWristband": {
    "type": "string",
    "description": "NFC Wristband"
   },
   "printedTicket": {
    "type": "string",
    "description": "Printed Ticket"
   },
   "thermalTicket": {
    "type": "string",
    "description": "Thermal Ticket"
   },
   "membershipCard": {
    "type": "string",
    "description": "Membership Card"
   },
   "customWearable": {
    "type": "string",
    "description": "Custom Wearable"
   },
   "faceRecognitionReference": {
    "type": "string",
    "description": "Face Recognition Reference"
   },
   "tenantDefinedIntegrationBasedCredentialTechnology": {
    "type": "string",
    "description": "Tenant-defined / integration-based credential technology"
   },
   "mediaTypeId": {
    "type": "string",
    "description": "Media Type ID"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "technology": {
    "type": "string",
    "description": "Technology"
   },
   "tokenFormat": {
    "type": "string",
    "description": "Token format"
   },
   "generationMethod": {
    "type": "string",
    "description": "Generation method"
   },
   "validationMechanism": {
    "type": "string",
    "description": "Validation mechanism"
   },
   "supportsVisualDesign": {
    "type": "string",
    "description": "Supports visual design"
   },
   "supportsDynamicUpdate": {
    "type": "string",
    "description": "Supports dynamic update"
   },
   "supportsRevocation": {
    "type": "string",
    "description": "Supports revocation"
   },
   "supportsExpiration": {
    "type": "string",
    "description": "Supports expiration"
   },
   "supportsOfflineReference": {
    "type": "string",
    "description": "Supports offline reference"
   },
   "supportsReplacement": {
    "type": "string",
    "description": "Supports replacement"
   },
   "supportsEncryption": {
    "type": "string",
    "description": "Supports encryption"
   },
   "supportsSigning": {
    "type": "string",
    "description": "Supports signing"
   },
   "supportedChannels": {
    "type": "string",
    "description": "Supported channels"
   },
   "supportedDevices": {
    "type": "string",
    "description": "Supported devices"
   },
   "integrationAdapter": {
    "type": "string",
    "description": "Integration adapter"
   },
   "rfidIsTheTechnologyMediaType": {
    "type": "string",
    "description": "RFID is the technology/media type"
   }
  }
 },
 "MultiMediaBindingAssociationRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Multi-Media Binding & Association Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "allowedMedia": {
    "type": "string",
    "description": "Allowed media"
   },
   "mandatoryMedia": {
    "type": "string",
    "description": "Mandatory media"
   },
   "optionalMedia": {
    "type": "string",
    "description": "Optional media"
   },
   "maximumActiveMedia": {
    "type": "string",
    "description": "Maximum active media"
   },
   "minimumMediaRequired": {
    "type": "boolean",
    "description": "Minimum media required"
   },
   "primaryMedia": {
    "type": "string",
    "description": "Primary media"
   },
   "secondaryMedia": {
    "type": "string",
    "description": "Secondary media"
   },
   "backupMedia": {
    "type": "string",
    "description": "Backup media"
   },
   "temporaryMedia": {
    "type": "string",
    "description": "Temporary media"
   },
   "mediaCombination": {
    "type": "string",
    "description": "Media combination"
   },
   "simultaneousActivation": {
    "type": "string",
    "description": "Simultaneous activation"
   },
   "exclusiveActivation": {
    "type": "string",
    "description": "Exclusive activation"
   },
   "face": {
    "type": "string",
    "description": "Face"
   },
   "rfidWristband": {
    "type": "string",
    "description": "RFID Wristband"
   },
   "mobileQr": {
    "type": "string",
    "description": "Mobile QR"
   },
   "rfidCard": {
    "type": "string",
    "description": "RFID Card"
   },
   "mobileQrBeforeWristbandCollection": {
    "type": "string",
    "description": "Mobile QR before wristband collection"
   },
   "appleWallet": {
    "type": "string",
    "description": "Apple Wallet"
   },
   "googleWallet": {
    "type": "string",
    "description": "Google Wallet"
   },
   "dynamicQr": {
    "type": "string",
    "description": "Dynamic QR"
   },
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
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "age": {
    "type": "string",
    "description": "Age"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "accessEnvironment": {
    "type": "string",
    "description": "Access environment"
   }
  }
 },
 "VirtualTicketArchitectureTestingGovernanceAuditView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket Architecture Testing, Governance & Audit displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "sameAuthoritativeEntitlementEvaluated": {
    "type": "string",
    "description": "Same authoritative entitlement evaluated"
   },
   "lostRfid": {
    "type": "string",
    "description": "Lost RFID"
   },
   "revokedQr": {
    "type": "string",
    "description": "Revoked QR"
   },
   "expiredWalletToken": {
    "type": "integer",
    "description": "Expired wallet token"
   },
   "faceUnavailable": {
    "type": "string",
    "description": "Face unavailable"
   },
   "offlineDevice": {
    "type": "integer",
    "description": "Offline device"
   },
   "synchronizationFailure": {
    "type": "string",
    "description": "Synchronization failure"
   },
   "providerOutage": {
    "type": "string",
    "description": "Provider outage"
   },
   "credentialBindingConflict": {
    "type": "string",
    "description": "Credential binding conflict"
   },
   "invalidMediaCombinations": {
    "type": "string",
    "description": "Invalid media combinations"
   },
   "missingSecurityProfile": {
    "type": "string",
    "description": "Missing security profile"
   },
   "missingFallback": {
    "type": "string",
    "description": "Missing fallback"
   },
   "conflictingActivationRules": {
    "type": "string",
    "description": "Conflicting activation rules"
   },
   "excessiveActiveCredentials": {
    "type": "string",
    "description": "Excessive active credentials"
   },
   "brokenProviderIntegration": {
    "type": "string",
    "description": "Broken provider integration"
   },
   "invalidLifecycleDependencies": {
    "type": "string",
    "description": "Invalid lifecycle dependencies"
   },
   "configurationChanges": {
    "type": "string",
    "description": "Configuration changes"
   },
   "mediaBindings": {
    "type": "string",
    "description": "Media bindings"
   },
   "rebindings": {
    "type": "string",
    "description": "Rebindings"
   },
   "activation": {
    "type": "string",
    "description": "Activation"
   },
   "suspension": {
    "type": "string",
    "description": "Suspension"
   },
   "revocation": {
    "type": "string",
    "description": "Revocation"
   },
   "replacement": {
    "type": "string",
    "description": "Replacement"
   },
   "resolverChanges": {
    "type": "string",
    "description": "Resolver changes"
   },
   "ruleChanges": {
    "type": "string",
    "description": "Rule changes"
   },
   "approvals": {
    "type": "string",
    "description": "Approvals"
   },
   "actor": {
    "type": "string",
    "description": "Actor"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "beforeAfter": {
    "type": "string",
    "description": "Before/After"
   },
   "replacementRebindingTestGovern": {
    "type": "string",
    "description": "Replacement/Rebinding → Test & Govern"
   },
   "coreVirtualTicketArchitecture": {
    "type": "string",
    "description": "core Virtual Ticket architecture"
   }
  }
 },
 "VirtualTicketCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalVirtualTickets": {
    "type": "integer",
    "description": "Total Virtual Tickets"
   },
   "active": {
    "type": "integer",
    "description": "Active"
   },
   "pendingActivation": {
    "type": "integer",
    "description": "Pending Activation"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "usedConsumed": {
    "type": "string",
    "description": "Used / Consumed"
   },
   "partiallyConsumed": {
    "type": "string",
    "description": "Partially Consumed"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "cancelled": {
    "type": "integer",
    "description": "Cancelled"
   },
   "revoked": {
    "type": "string",
    "description": "Revoked"
   },
   "virtualTicketsWithMultipleMedia": {
    "type": "string",
    "description": "Virtual Tickets with Multiple Media"
   },
   "mediaBindingExceptions": {
    "type": "integer",
    "description": "Media Binding Exceptions"
   },
   "credentialSynchronizationIssues": {
    "type": "integer",
    "description": "Credential Synchronization Issues"
   },
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket ID"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "eventPerformance": {
    "type": "string",
    "description": "Event / Performance"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "orderReference": {
    "type": "string",
    "description": "Order Reference"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "seatResourceWhereApplicable": {
    "type": "string",
    "description": "Seat / Resource where applicable"
   },
   "validFromTo": {
    "type": "string",
    "description": "Valid From / To"
   },
   "ticketStatus": {
    "type": "integer",
    "description": "Ticket Status"
   },
   "usageStatus": {
    "type": "integer",
    "description": "Usage Status"
   },
   "numberOfLinkedMedia": {
    "type": "integer",
    "description": "Number of Linked Media"
   },
   "primaryMedia": {
    "type": "string",
    "description": "Primary Media"
   },
   "lastCredentialActivity": {
    "type": "string",
    "format": "date-time",
    "description": "Last Credential Activity"
   },
   "lastModified": {
    "type": "string",
    "format": "date-time",
    "description": "Last Modified"
   },
   "productVipConcert": {
    "type": "string",
    "description": "Product: VIP Concert"
   },
   "customerAhmedHassan": {
    "type": "string",
    "description": "Customer: Ahmed Hassan"
   },
   "seatA18": {
    "type": "string",
    "description": "Seat: A-18"
   },
   "statusActive": {
    "type": "integer",
    "description": "Status: Active"
   },
   "media4": {
    "type": "string",
    "description": "Media: 4"
   },
   "bindMedia": {
    "type": "string",
    "description": "Bind Media"
   },
   "reactivate": {
    "type": "string",
    "description": "Reactivate"
   },
   "diagnoseCredential": {
    "type": "string",
    "description": "Diagnose Credential"
   }
  }
 },
 "VirtualTicketIdentityMasterRecordConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Virtual Ticket Identity & Master Record Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "mediaReplacement": {
    "type": "string",
    "description": "Media replacement"
   },
   "qrRegeneration": {
    "type": "string",
    "description": "QR regeneration"
   },
   "rfidReplacement": {
    "type": "string",
    "description": "RFID replacement"
   },
   "walletUpdates": {
    "type": "string",
    "description": "Wallet updates"
   },
   "deviceChanges": {
    "type": "string",
    "description": "Device changes"
   },
   "faceEnrollmentChanges": {
    "type": "string",
    "description": "Face enrollment changes"
   },
   "ticketReprint": {
    "type": "string",
    "description": "Ticket reprint"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "orderLine": {
    "type": "string",
    "description": "Order Line"
   },
   "reservation": {
    "type": "string",
    "description": "Reservation"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productVersion": {
    "type": "string",
    "description": "Product Version"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performanceTimeslot": {
    "type": "string",
    "description": "Performance / Timeslot"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "resource": {
    "type": "string",
    "description": "Resource"
   },
   "priceSnapshot": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Snapshot"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "accessEntitlement": {
    "type": "string",
    "description": "Access entitlement"
   },
   "fulfillmentStatus": {
    "type": "string",
    "description": "Fulfillment status"
   },
   "idGenerationPattern": {
    "type": "string",
    "description": "ID generation pattern"
   },
   "ticketClassification": {
    "type": "string",
    "description": "Ticket classification"
   },
   "ticketOwnershipModel": {
    "type": "string",
    "description": "Ticket ownership model"
   },
   "holderAssignmentRequirements": {
    "type": "string",
    "description": "Holder assignment requirements"
   },
   "transferabilityReference": {
    "type": "string",
    "description": "Transferability reference"
   },
   "validityModel": {
    "type": "string",
    "description": "Validity model"
   },
   "consumptionModel": {
    "type": "string",
    "description": "Consumption model"
   },
   "entitlementModel": {
    "type": "string",
    "description": "Entitlement model"
   },
   "mediaRequirements": {
    "type": "string",
    "description": "Media requirements"
   },
   "rfid77812Vt009821": {
    "type": "string",
    "description": "RFID-77812 → VT-009821"
   },
   "rfid99142Vt009821": {
    "type": "string",
    "description": "RFID-99142 → VT-009821"
   },
   "theVirtualTicketRemainsUnchanged": {
    "type": "string",
    "description": "The Virtual Ticket remains unchanged"
   },
   "valid": {
    "type": "string",
    "description": "Valid"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   }
  }
 },
 "VirtualTicketIdentityMasterRecordConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket Identity & Master Record Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "mediaReplacement": {
    "type": "string",
    "description": "Media replacement"
   },
   "qrRegeneration": {
    "type": "string",
    "description": "QR regeneration"
   },
   "rfidReplacement": {
    "type": "string",
    "description": "RFID replacement"
   },
   "walletUpdates": {
    "type": "string",
    "description": "Wallet updates"
   },
   "deviceChanges": {
    "type": "string",
    "description": "Device changes"
   },
   "faceEnrollmentChanges": {
    "type": "string",
    "description": "Face enrollment changes"
   },
   "ticketReprint": {
    "type": "string",
    "description": "Ticket reprint"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "orderLine": {
    "type": "string",
    "description": "Order Line"
   },
   "reservation": {
    "type": "string",
    "description": "Reservation"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productVersion": {
    "type": "string",
    "description": "Product Version"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performanceTimeslot": {
    "type": "string",
    "description": "Performance / Timeslot"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "resource": {
    "type": "string",
    "description": "Resource"
   },
   "priceSnapshot": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Snapshot"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "accessEntitlement": {
    "type": "string",
    "description": "Access entitlement"
   },
   "fulfillmentStatus": {
    "type": "string",
    "description": "Fulfillment status"
   },
   "idGenerationPattern": {
    "type": "string",
    "description": "ID generation pattern"
   },
   "ticketClassification": {
    "type": "string",
    "description": "Ticket classification"
   },
   "ticketOwnershipModel": {
    "type": "string",
    "description": "Ticket ownership model"
   },
   "holderAssignmentRequirements": {
    "type": "string",
    "description": "Holder assignment requirements"
   },
   "transferabilityReference": {
    "type": "string",
    "description": "Transferability reference"
   },
   "validityModel": {
    "type": "string",
    "description": "Validity model"
   },
   "consumptionModel": {
    "type": "string",
    "description": "Consumption model"
   },
   "entitlementModel": {
    "type": "string",
    "description": "Entitlement model"
   },
   "mediaRequirements": {
    "type": "string",
    "description": "Media requirements"
   },
   "rfid77812Vt009821": {
    "type": "string",
    "description": "RFID-77812 → VT-009821"
   },
   "rfid99142Vt009821": {
    "type": "string",
    "description": "RFID-99142 → VT-009821"
   },
   "theVirtualTicketRemainsUnchanged": {
    "type": "string",
    "description": "The Virtual Ticket remains unchanged"
   },
   "valid": {
    "type": "string",
    "description": "Valid"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   }
  }
 },
 "VirtualTicketStatusLifecycleModelView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket Status & Lifecycle Model displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "withGovernedAlternativeStates": {
    "type": "string",
    "description": "with governed alternative states"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "cancelled": {
    "type": "integer",
    "description": "Cancelled"
   },
   "voided": {
    "type": "string",
    "description": "Voided"
   },
   "reissuedSuperseded": {
    "type": "string",
    "description": "Reissued / Superseded"
   },
   "refunded": {
    "type": "string",
    "description": "Refunded"
   },
   "transferred": {
    "type": "string",
    "description": "Transferred"
   },
   "blocked": {
    "type": "string",
    "description": "Blocked"
   },
   "from": {
    "type": "string",
    "description": "from"
   },
   "qrActive": {
    "type": "integer",
    "description": "QR — Active"
   },
   "rfidLostRevoked": {
    "type": "string",
    "description": "RFID — Lost / Revoked"
   },
   "appleWalletActive": {
    "type": "integer",
    "description": "Apple Wallet — Active"
   },
   "faceActive": {
    "type": "integer",
    "description": "Face — Active"
   },
   "theTicketItselfRemainsValid": {
    "type": "string",
    "description": "The ticket itself remains valid"
   },
   "orderManagement": {
    "type": "string",
    "description": "Order Management"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "ticketTransfer": {
    "type": "string",
    "description": "Ticket Transfer"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   },
   "accessUsage": {
    "type": "string",
    "description": "Access usage"
   },
   "authorizedOperator": {
    "type": "string",
    "description": "Authorized operator"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "scheduledProcess": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled process"
   }
  }
 }
}
```
