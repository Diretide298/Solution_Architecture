# WS59 — Ticket Media   Credential Management board 1

**10 screens · 16 operations · 18 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-334` | Virtual Ticket Command Center | commandCentre | 3 | 0 | — |
| `BO-335` | Virtual Ticket Identity & Master Record Configuration | configEditor | 1 | 0 | — |
| `BO-336` | Virtual Ticket Status & Lifecycle Model | listDetail | 2 | 1 | — |
| `BO-337` | Media Type & Credential Technology Registry | configEditor | 2 | 0 | — |
| `BO-338` | Multi-Media Binding & Association Rules | configEditor | 3 | 2 | — |
| `BO-339` | Credential Identity, Token & Reference Mapping | listDetail | 1 | 0 | — |
| `BO-340` | Entitlement & Cross-Media Synchronization Rules | listDetail | 2 | 1 | — |
| `BO-341` | Media Activation, Priority & Fallback Rules | configEditor | 1 | 0 | — |
| `BO-342` | Media Replacement, Revocation & Rebinding Rules | configEditor | 2 | 2 | — |
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
     "provenance": "derived — BO-100 declares entryState.params  and BO-334 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
  "purposeNote": "Authorized users can locate any Virtual Ticket and immediately understand its ticket status, entitlement, usage state and all associated media from one centralized workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population",
  "purpose": "Provide administrators and operations teams with a centralized view of all Virtual Tickets and their associated media across TICVAI. This is the primary administrative entry point into the Virtual Ticket architecture.",
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
       "bindsTo": "VirtualTicketCommandCenterViewSummary.totalVirtualTickets"
      },
      {
       "kind": "metricTile",
       "label": "Active",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.active"
      },
      {
       "kind": "metricTile",
       "label": "Pending Activation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.pendingActivation"
      },
      {
       "kind": "metricTile",
       "label": "Suspended",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.suspended"
      },
      {
       "kind": "metricTile",
       "label": "Used / Consumed",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.usedConsumed"
      },
      {
       "kind": "metricTile",
       "label": "Partially Consumed",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.partiallyConsumed"
      },
      {
       "kind": "metricTile",
       "label": "Expired",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.expired"
      },
      {
       "kind": "metricTile",
       "label": "Cancelled",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.cancelled"
      },
      {
       "kind": "metricTile",
       "label": "Revoked",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.revoked"
      },
      {
       "kind": "metricTile",
       "label": "Virtual Tickets with Multiple Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.virtualTicketsWithMultipleMedia"
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
       "bindsTo": "VirtualTicketCommandCenterViewSummary.mediaBindingExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Credential Synchronization Issues",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "VirtualTicketCommandCenterViewSummary.credentialSynchronizationIssues"
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
   },
   {
    "operationId": "listVirtualTicketStatus",
    "contract": "access",
    "purpose": "Virtual Ticket Status & Lifecycle Model",
    "trigger": "onLoad"
   },
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-334",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-334"
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
  "purposeNote": "Every issued ticket has one persistent, media-independent Virtual Ticket identity that remains authoritative regardless of which credential technologies are attached to it.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define the authoritative Virtual Ticket object used throughout TICVAI. This screen is extremely important because the Virtual Ticket—not the QR/RFID/card— is the master ticket record.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-335",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-335"
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
  "purposeNote": "state changes across every credential associated with that ticket.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the standardized lifecycle of a Virtual Ticket independently from the lifecycle of individual media.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save ticket status transition",
       "operation": "setTicketStatusTransition",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind Virtual Ticket Status & Lifecycle Model** (BO-336): for one move between Virtual Ticket statuses, whether it is allowed, whether it needs an authorised exception and where it may originate.",
       "provenance": "contract access.yaml PUT /ticket-status-transitions"
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
   },
   {
    "operationId": "setTicketStatusTransition",
    "contract": "access",
    "purpose": "Set a Virtual Ticket status transition rule",
    "trigger": "onAction",
    "invalidates": [
     "listVirtualTicketStatus"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "VirtualTicketStatusLifecycleModelView.toStatus"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-336",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-336"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 11 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetTicketStatusTransition",
    "component": "modal",
    "trigger": "Save ticket status transition",
    "body": "**Collects what `setTicketStatusTransition` sends before it is called.** Required: `id`, `fromStatus`, `toStatus`, `allowed`, `requiresAuthorizedException`, `scopePath`. Optional: `originatingSources`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessTicketStatusTransition",
    "confirm": {
     "label": "Save ticket status transition",
     "operation": "setTicketStatusTransition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "fromStatus",
      "toStatus",
      "allowed",
      "requiresAuthorizedException",
      "scopePath",
      "originatingSources"
     ]
    },
    "provenance": "contract access.yaml PUT /ticket-status-transitions"
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
  "purposeNote": "technologies with their capabilities, providers and technical behavior.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§For each technology configure) and no display directory — it is settings, not a population",
  "purpose": "Maintain the centralized catalogue of credential technologies supported by TICVAI. This makes the credential architecture extensible rather than hard-coded.",
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
    "operationId": "listMediaTypeTechnology",
    "contract": "access",
    "purpose": "Media Type & Technology Library",
    "trigger": "onLoad"
   },
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-337",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-337"
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
  "purposeNote": "Ticket without creating duplicate ticket entitlements.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how one Virtual Ticket can be associated with multiple media simultaneously. This is one of the most important screens in Area 15.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save media binding rule",
       "operation": "setMediaBindingRule",
       "permission": "ACCESS_POINT_CONFIGURE",
       "provenance": "contract access.yaml PUT /media-binding-rules"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete media binding rule",
       "operation": "deleteMediaBindingRule",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "Deletes a binding rule.",
       "provenance": "contract access.yaml DELETE /media-binding-rules/{ruleId}"
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
   },
   {
    "operationId": "setMediaBindingRule",
    "contract": "access",
    "purpose": "Create or replace a multi-media binding rule",
    "trigger": "onAction",
    "invalidates": [
     "listMultiMediaBinding"
    ]
   },
   {
    "operationId": "deleteMediaBindingRule",
    "contract": "access",
    "purpose": "Delete a multi-media binding rule",
    "trigger": "onAction",
    "invalidates": [
     "listMultiMediaBinding"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-338",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-338"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 12 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetMediaBindingRule",
    "component": "modal",
    "trigger": "Save media binding rule",
    "body": "**Collects what `setMediaBindingRule` sends before it is called.** Required: `id`, `scopePath`. Optional: `allowedMediaTypeIds`, `mandatoryMediaTypeIds`, `optionalMediaTypeIds`, `primaryMediaTypeId`, `secondaryMediaTypeIds`, `backupMediaTypeIds`, `temporaryMediaTypeIds`, `minimumMediaRequired`, `maximumActiveMedia`, `mediaCombinations`, `simultaneousActivation`, `exclusiveActivation` and 10 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessMediaBindingRule",
    "confirm": {
     "label": "Save media binding rule",
     "operation": "setMediaBindingRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "allowedMediaTypeIds",
      "mandatoryMediaTypeIds",
      "optionalMediaTypeIds",
      "primaryMediaTypeId",
      "secondaryMediaTypeIds",
      "backupMediaTypeIds",
      "temporaryMediaTypeIds",
      "minimumMediaRequired",
      "maximumActiveMedia",
      "mediaCombinations",
      "simultaneousActivation",
      "exclusiveActivation",
      "productId",
      "ticketType",
      "eventId",
      "venueId"
     ]
    },
    "provenance": "contract access.yaml PUT /media-binding-rules"
   },
   {
    "id": "confirmDeleteMediaBindingRule",
    "component": "confirmDialog",
    "trigger": "Delete media binding rule",
    "body": "**Names what `deleteMediaBindingRule` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml DELETE /media-binding-rules/{ruleId}"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "ruleId",
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
  "purposeNote": "Every supported credential can securely and consistently resolve to its authoritative Virtual Ticket without duplicating ticket entitlement data within individual media.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define how individual media identifiers resolve securely back to the authoritative Virtual Ticket.",
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
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Key references",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 12 §Support appropriate"
      }
     ]
    },
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
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-339",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-339"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 1 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Key references dropped (heading).",
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
  "purposeNote": "All credential media consistently consume and represent the same authoritative Virtual Ticket entitlement and usage state.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Ensure all media attached to a Virtual Ticket share the same authoritative ticket and entitlement state.",
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
        "EntitlementCrossMediaSynchronizationRulesView.monitoredConditions"
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
        "EntitlementCrossMediaSynchronizationRulesView.monitoredConditions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Critical Principle”, “For example, TICVAI must prevent”, “Instead”, “Face Credential”, “Virtual Ticket resolved”, “Access transaction recorded”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 14 §Detect"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save credential event propagation rule",
       "operation": "setCredentialEventPropagationRule",
       "permission": "ACCESS_POINT_CONFIGURE",
       "provenance": "contract access.yaml PUT /credential-event-propagation-rules"
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
   },
   {
    "operationId": "setCredentialEventPropagationRule",
    "contract": "access",
    "purpose": "Set how a ticket lifecycle event propagates to the credential",
    "trigger": "onAction",
    "invalidates": [
     "listEntitlementCrossMedia"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "EntitlementCrossMediaSynchronizationRulesView.monitoredConditions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-340",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-340"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 14. 5 of 5 labels bound to a contract property; 17 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetCredentialEventPropagationRule",
    "component": "modal",
    "trigger": "Save credential event propagation rule",
    "body": "**Collects what `setCredentialEventPropagationRule` sends before it is called.** Required: `id`, `triggerEvent`, `scopePath`. Optional: `revocationAction`, `propagationTargets`, `monitoredConditions`, `propagation`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessCredentialEventPropagationRule",
    "confirm": {
     "label": "Save credential event propagation rule",
     "operation": "setCredentialEventPropagationRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "triggerEvent",
      "scopePath",
      "revocationAction",
      "propagationTargets",
      "monitoredConditions",
      "propagation"
     ]
    },
    "provenance": "contract access.yaml PUT /credential-event-propagation-rules"
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
  "purposeNote": "options without compromising the underlying Virtual Ticket.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure when each credential becomes active and how alternative media behave if the preferred credential cannot be used.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "On download",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "On wallet installation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "On event date",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-341",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-341"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 10 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Credential media can be securely replaced, revoked and rebound while maintaining continuity of the underlying Virtual Ticket and a complete audit history.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure controlled handling of lost, stolen, damaged, compromised or replaced credential media.",
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
       "label": "Wallet credential replacement",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Support"
      },
      {
       "kind": "secondaryButton",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Replace Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 16 §Allow immediate"
      },
      {
       "kind": "primaryButton",
       "label": "Save replacement rule",
       "operation": "setMediaReplacementRevocation",
       "provenance": "contract access.yaml PUT /media-replacement-revocation (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setMediaReplacementRevocation",
    "contract": "access",
    "purpose": "Save replacement rule",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-342",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-342"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 15 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setMediaReplacementRevocation`.",
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
  "purposeNote": "and retain complete traceability of configuration and credential-binding changes. Board 1 — Final Screen Register",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration Simulator; Configuration Owner; AI Configuration Review) and no display directory — it is settings, not a population",
  "purpose": "Provide the final testing and governance environment for Virtual Ticket and multi-media configurations. Board 1 established what the Virtual Ticket is and how multiple credentials can point to the same authoritative ticket. Board 2 defines how each media type is created, designed, configured, branded, populated with data, previewed, tested and published.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-343",
   "workshopBoard": "wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-343"
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
 "deleteMediaBindingRule": {
  "method": "DELETE",
  "path": "/media-binding-rules/{ruleId}",
  "contract": "access",
  "summary": "Delete a multi-media binding rule",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "responds": null
 },
 "listCredentialIdentityToken": {
  "method": "GET",
  "path": "/credential-identity-token",
  "contract": "access",
  "summary": "Credential Identity, Token & Reference Mapping",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "virtualTicketId",
    "in": "query",
    "required": false
   },
   {
    "name": "mediaType",
    "in": "query",
    "required": false
   },
   {
    "name": "credentialReference",
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
 "listEntitlementCrossMedia": {
  "method": "GET",
  "path": "/entitlement-cross-media",
  "contract": "access",
  "summary": "Entitlement & Cross-Media Synchronization Rules",
  "permission": "SCOPE_VIEW",
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MediaTypeCredentialTechnologyRegistryView"
 },
 "listMediaTypeTechnology": {
  "method": "GET",
  "path": "/media-type-technology",
  "contract": "access",
  "summary": "Media Type & Technology Library",
  "permission": "SCOPE_VIEW",
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
  "responds": "MediaTypeTechnologyLibraryView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketType",
    "in": "query",
    "required": false
   },
   {
    "name": "numberOfMedia",
    "in": "query",
    "required": false
   },
   {
    "name": "validity",
    "in": "query",
    "required": false
   },
   {
    "name": "usageStatus",
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
 "listVirtualTicketArchitecture": {
  "method": "GET",
  "path": "/virtual-ticket-architecture",
  "contract": "access",
  "summary": "Virtual Ticket Architecture Testing, Governance & Audit",
  "permission": "AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "changeType",
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
 "listVirtualTicketStatus": {
  "method": "GET",
  "path": "/virtual-ticket-statu",
  "contract": "access",
  "summary": "Virtual Ticket Status & Lifecycle Model",
  "permission": "SCOPE_VIEW",
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
  "responds": "VirtualTicketStatusLifecycleModelView"
 },
 "setCredentialEventPropagationRule": {
  "method": "PUT",
  "path": "/credential-event-propagation-rules",
  "contract": "access",
  "summary": "Set how a ticket lifecycle event propagates to the credential",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "AccessCredentialEventPropagationRule",
  "responds": "AccessCredentialEventPropagationRule"
 },
 "setMediaBindingRule": {
  "method": "PUT",
  "path": "/media-binding-rules",
  "contract": "access",
  "summary": "Create or replace a multi-media binding rule",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "AccessMediaBindingRule",
  "responds": "AccessMediaBindingRule"
 },
 "setMediaReplacementRevocation": {
  "method": "PUT",
  "path": "/media-replacement-revocation",
  "contract": "access",
  "summary": "Save a media replacement rule",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "MediaReplacementRevocationRebindingRulesInput",
  "responds": "MediaReplacementRevocationRebindingRulesView"
 },
 "setTicketStatusTransition": {
  "method": "PUT",
  "path": "/ticket-status-transitions",
  "contract": "access",
  "summary": "Set a Virtual Ticket status transition rule",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "AccessTicketStatusTransition",
  "responds": "AccessTicketStatusTransition"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "VirtualTicketIdentityMasterRecordConfigurationInput",
  "responds": "VirtualTicketIdentityMasterRecordConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessCredentialEventPropagationRule": {
  "type": "object",
  "x-ticvai-persistence": "access.credential_event_propagation_rule",
  "description": "For one ticket lifecycle event, the revocation action on the credential and how the change propagates to every bound medium, with the conditions monitored (declared 29 September, data-model close-out DM1).",
  "required": [
   "id",
   "triggerEvent",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "triggerEvent": {
    "type": "string",
    "enum": [
     "entry",
     "exit",
     "redemption",
     "partialConsumption",
     "cancellation",
     "refund",
     "suspension",
     "reactivation",
     "transfer",
     "exchange",
     "upgrade",
     "reissue",
     "expiry",
     "replacement",
     "manualInvalidation",
     "fraudLock",
     "accountSuspension"
    ],
    "description": "Unique per scope; one vocabulary for both screens that read it (decided 29 September, writers pass)"
   },
   "revocationAction": {
    "type": "string",
    "nullable": true,
    "enum": [
     "invalidate",
     "suspend",
     "replace"
    ],
    "description": "What happens to the credential; refund, exchange and reissue always revoke"
   },
   "propagationTargets": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "centralPlatform",
      "mobileApp",
      "gateNetwork",
      "offlineRevocationPackage",
      "walletCredentialService"
     ]
    }
   },
   "monitoredConditions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "delayedUpdates",
      "conflictingStates",
      "offlineTransactionsPendingSynchronization",
      "providerUpdateFailures",
      "staleWalletCredentials"
     ]
    }
   },
   "propagation": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "How the Virtual Ticket state change reaches every bound medium"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
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
 "AccessMediaBindingRule": {
  "type": "object",
  "x-ticvai-persistence": "access.media_binding_rule",
  "description": "One multi-media binding rule - which media a Virtual Ticket may, must or may optionally carry, in which roles and combinations - for the scope named by its conditions (declared 29 September, data-model close-out DM1).",
  "required": [
   "id",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "allowedMediaTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "mandatoryMediaTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "optionalMediaTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "primaryMediaTypeId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "secondaryMediaTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "backupMediaTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "temporaryMediaTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "minimumMediaRequired": {
    "type": "integer",
    "minimum": 0,
    "default": 0
   },
   "maximumActiveMedia": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "mediaCombinations": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Permitted media combinations"
   },
   "simultaneousActivation": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media that may be active at the same time, e.g. face with RFID"
   },
   "exclusiveActivation": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media whose activation revokes another, e.g. RFID activated revokes temporary paper"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ticketType": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "eventId": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "customerType": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "membership": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "channel": {
    "type": "string",
    "maxLength": 50,
    "nullable": true
   },
   "ageCategory": {
    "type": "string",
    "maxLength": 50,
    "nullable": true
   },
   "country": {
    "type": "string",
    "maxLength": 2,
    "nullable": true,
    "description": "ISO 3166-1 alpha-2"
   },
   "accessEnvironment": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
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
 "AccessTicketStatusTransition": {
  "type": "object",
  "x-ticvai-persistence": "access.ticket_status_transition",
  "description": "One Virtual Ticket lifecycle transition rule - from status, to status, whether allowed, whether it needs an authorised exception and where it may originate (declared 29 September, data-model close-out DM1). Seeded from states/entitlement-status.yaml when a venue is created; setTicketStatusTransition may narrow a move, never add one (decided 29 September, writers pass).",
  "required": [
   "id",
   "fromStatus",
   "toStatus",
   "allowed",
   "requiresAuthorizedException",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "fromStatus": {
    "type": "string",
    "enum": [
     "created",
     "pendingFulfillment",
     "active",
     "partiallyUsed",
     "used",
     "expired",
     "suspended",
     "cancelled",
     "voided",
     "reissuedSuperseded",
     "refunded",
     "transferred",
     "blocked"
    ]
   },
   "toStatus": {
    "type": "string",
    "enum": [
     "created",
     "pendingFulfillment",
     "active",
     "partiallyUsed",
     "used",
     "expired",
     "suspended",
     "cancelled",
     "voided",
     "reissuedSuperseded",
     "refunded",
     "transferred",
     "blocked"
    ],
    "description": "Unique with fromStatus per scope"
   },
   "allowed": {
    "type": "boolean"
   },
   "requiresAuthorizedException": {
    "type": "boolean",
    "default": false,
    "description": "Allowed only with an authorised exception, e.g. used to active"
   },
   "originatingSources": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "orderManagement",
      "cancellation",
      "refund",
      "upgradeConversion",
      "ticketTransfer",
      "membership",
      "expiry",
      "accessUsage",
      "authorizedOperator",
      "api",
      "scheduledProcess"
     ]
    }
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
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
 "CredentialIdentityTokenReferenceMappingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Identity, Token & Reference Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "description": "Token or identifier, masked in administrative views"
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
    "enum": [
     "pending",
     "active",
     "suspended",
     "revoked",
     "expired"
    ],
    "description": "Credential binding status"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "securityProfile": {
    "type": "string",
    "description": "Security profile"
   },
   "protectionMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "tokenization",
      "hashing",
      "encryption",
      "signedPayloads",
      "keyReferences",
      "masking"
     ]
    },
    "description": "How the credential value is protected"
   }
  },
  "required": [
   "credentialBindingId",
   "virtualTicketId",
   "mediaType"
  ]
 },
 "EntitlementCrossMediaSynchronizationRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Entitlement & Cross-Media Synchronization Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "triggerEvent": {
    "type": "string",
    "enum": [
     "entry",
     "exit",
     "redemption",
     "partialConsumption",
     "cancellation",
     "refund",
     "suspension",
     "reactivation",
     "transfer",
     "upgrade",
     "expiry",
     "replacement"
    ],
    "description": "Ticket event this synchronisation rule handles"
   },
   "monitoredConditions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "delayedUpdates",
      "conflictingStates",
      "offlineTransactionsPendingSynchronization",
      "providerUpdateFailures",
      "staleWalletCredentials"
     ]
    },
    "description": "Synchronisation problems detected and alerted"
   },
   "propagation": {
    "type": "string",
    "description": "How the Virtual Ticket state change reaches every bound medium"
   }
  },
  "required": [
   "triggerEvent"
  ]
 },
 "MediaActivationPriorityFallbackRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Activation, Priority & Fallback Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "mediaTypeId": {
    "type": "string",
    "description": "Media type this rule applies to"
   },
   "activationTrigger": {
    "type": "string",
    "enum": [
     "immediateOnIssuance",
     "onTicketActivation",
     "onDownload",
     "onWalletInstallation",
     "onRfidAssignment",
     "onFaceEnrollment",
     "onFirstUse",
     "onEventDate",
     "manualActivation",
     "scheduledActivation"
    ],
    "description": "When this medium becomes active"
   },
   "temporaryMedia": {
    "type": "boolean",
    "description": "Temporary media"
   },
   "validityDuration": {
    "type": "string",
    "description": "ISO 8601 duration, e.g. PT30M"
   },
   "oneTimeUse": {
    "type": "boolean",
    "description": "One-time use"
   },
   "automaticExpiration": {
    "type": "boolean",
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
   "fallbackMediaTypes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Ordered media to use if this one cannot be used, e.g. face unavailable then RFID"
   }
  },
  "required": [
   "mediaTypeId",
   "activationTrigger"
  ]
 },
 "MediaReplacementRevocationRebindingRulesInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Media Replacement, Revocation & Rebinding Rules submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "replacementReason",
   "outcome"
  ],
  "properties": {
   "replacementReason": {
    "type": "string",
    "enum": [
     "lost",
     "stolen",
     "damaged",
     "compromised",
     "customerChangedPhone",
     "rfidFailure",
     "wristbandReplacement",
     "qrCompromise",
     "walletReplacement",
     "faceReEnrollment",
     "incorrectAssignment"
    ],
    "description": "The reason this rule is for, in the vocabulary of `replaceCredential`, so the rule a replacement reads is keyed the way the replacement names it (decided 29 September, writers pass). The old keys map: lostRfidCard to lost or rfidFailure, damagedWristband to wristbandReplacement, compromisedQr to qrCompromise, newMobileDevice to customerChangedPhone, walletCredentialReplacement to walletReplacement, faceReEnrollment unchanged, printedTicketReplacement to damaged, incorrectCredentialAssignment to incorrectAssignment."
   },
   "outcome": {
    "type": "string",
    "enum": [
     "replace",
     "rebind",
     "suspendMedia",
     "revokeMedia"
    ],
    "description": "What happens to the media"
   },
   "numberOfReplacements": {
    "type": "integer",
    "minimum": 0,
    "description": "Maximum replacements per credential"
   },
   "replacementFeeReference": {
    "type": "string",
    "description": "Catalogue product charged for the replacement; empty is free"
   },
   "approvalRequired": {
    "type": "boolean",
    "default": false
   },
   "supervisorApproval": {
    "type": "boolean",
    "default": false
   },
   "identityVerification": {
    "type": "boolean",
    "default": true
   },
   "oldMediaAutomaticallyRevoked": {
    "type": "boolean",
    "default": true
   },
   "gracePeriod": {
    "type": "string",
    "description": "ISO 8601 duration the old media stays valid; empty is none"
   },
   "simultaneousMediaPolicy": {
    "type": "string",
    "enum": [
     "oneActive",
     "allowBothDuringGrace"
    ],
    "default": "oneActive"
   },
   "reasonMandatory": {
    "type": "boolean",
    "default": true
   },
   "reissueAllowed": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "MediaReplacementRevocationRebindingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Replacement, Revocation & Rebinding Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "outcome": {
    "type": "string",
    "enum": [
     "replace",
     "rebind",
     "suspendMedia",
     "revokeMedia"
    ],
    "description": "What happens to the media (decided 29 September, VM close-out)"
   },
   "replacementReason": {
    "type": "string",
    "enum": [
     "lost",
     "stolen",
     "damaged",
     "compromised",
     "customerChangedPhone",
     "rfidFailure",
     "wristbandReplacement",
     "qrCompromise",
     "walletReplacement",
     "faceReEnrollment",
     "incorrectAssignment"
    ],
    "description": "The reason this rule is for, in the vocabulary of `replaceCredential`, so the rule a replacement reads is keyed the way the replacement names it (decided 29 September, writers pass). The old keys map: lostRfidCard to lost or rfidFailure, damagedWristband to wristbandReplacement, compromisedQr to qrCompromise, newMobileDevice to customerChangedPhone, walletCredentialReplacement to walletReplacement, faceReEnrollment unchanged, printedTicketReplacement to damaged, incorrectCredentialAssignment to incorrectAssignment."
   },
   "numberOfReplacements": {
    "type": "integer",
    "description": "Number of replacements"
   },
   "replacementFeeReference": {
    "type": "string",
    "description": "Reference to a fee in pricing configuration; no amount is held here"
   },
   "approvalRequired": {
    "type": "boolean",
    "description": "Approval required"
   },
   "identityVerification": {
    "type": "boolean",
    "description": "Identity verification"
   },
   "oldMediaAutomaticallyRevoked": {
    "type": "boolean",
    "description": "Old media automatically revoked"
   },
   "gracePeriod": {
    "type": "string",
    "description": "ISO 8601 duration, e.g. PT30M"
   },
   "simultaneousMediaPolicy": {
    "type": "string",
    "description": "Simultaneous media policy"
   },
   "reasonMandatory": {
    "type": "boolean",
    "description": "Reason mandatory"
   },
   "supervisorApproval": {
    "type": "boolean",
    "description": "Supervisor approval"
   },
   "reissueAllowed": {
    "type": "boolean",
    "description": "Reissue allowed"
   }
  },
  "required": [
   "replacementReason"
  ]
 },
 "MediaTypeCredentialTechnologyRegistryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Type & Credential Technology Registry displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "enum": [
     "digital",
     "physical",
     "biometric",
     "future"
    ],
    "description": "Media category"
   },
   "provider": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Provider integrations that implement this media type (media type is not the vendor)"
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
    "type": "boolean",
    "description": "Supports visual design"
   },
   "supportsDynamicUpdate": {
    "type": "boolean",
    "description": "Supports dynamic update"
   },
   "supportsRevocation": {
    "type": "boolean",
    "description": "Supports revocation"
   },
   "supportsExpiration": {
    "type": "boolean",
    "description": "Supports expiration"
   },
   "supportsOfflineReference": {
    "type": "boolean",
    "description": "Supports offline reference"
   },
   "supportsReplacement": {
    "type": "boolean",
    "description": "Supports replacement"
   },
   "supportsEncryption": {
    "type": "boolean",
    "description": "Supports encryption"
   },
   "supportsSigning": {
    "type": "boolean",
    "description": "Supports signing"
   },
   "supportedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Supported channels"
   },
   "supportedDevices": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Supported devices"
   },
   "integrationAdapter": {
    "type": "string",
    "description": "Integration adapter"
   }
  },
  "required": [
   "mediaTypeId",
   "name",
   "category"
  ]
 },
 "MediaTypeTechnologyLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Type & Technology Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "active": {
    "type": "boolean",
    "description": "False once retired through `setMediaTypeTechnology`; issued credentials stay valid (decided 29 September, VM close-out)"
   },
   "mediaType": {
    "type": "string",
    "enum": [
     "linearBarcode",
     "twoDimensionalBarcode",
     "qr",
     "rfidContact",
     "rfidProximity",
     "rfidIso15693",
     "rfidOtherStandard",
     "appCredential",
     "mobileWallet",
     "paperTicket",
     "wristband",
     "plasticCard",
     "hotelCard",
     "facePass",
     "faceTag",
     "partnerQr",
     "externalBarcode",
     "thirdPartyCredential"
    ],
    "description": "The kind of medium this profile defines"
   },
   "technology": {
    "type": "string",
    "enum": [
     "barcode",
     "rfid",
     "nfc",
     "magneticStripe",
     "mobile",
     "physical",
     "biometric",
     "external"
    ],
    "description": "Technology family"
   },
   "encodingFormat": {
    "type": "string",
    "description": "encoding format"
   },
   "supportedReaderTypes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "supported reader types"
   },
   "onlineOfflineCapability": {
    "type": "string",
    "enum": [
     "onlineOnly",
     "offlineOnly",
     "onlineAndOffline"
    ],
    "description": "online/offline capability"
   },
   "writableReadOnly": {
    "type": "string",
    "enum": [
     "writable",
     "readOnly"
    ],
    "description": "writable/read-only"
   },
   "securityClassification": {
    "type": "string",
    "description": "security classification"
   },
   "applicableVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Venue ids"
   },
   "applicableProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Product ids"
   },
   "mediaTypeId": {
    "type": "string",
    "description": "Media type profile identifier"
   },
   "name": {
    "type": "string",
    "description": "Profile name"
   }
  }
 },
 "MultiMediaBindingAssociationRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Multi-Media Binding & Association Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Binding rule ID"
   },
   "allowedMedia": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media type IDs allowed"
   },
   "mandatoryMedia": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media type IDs required"
   },
   "optionalMedia": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media type IDs optional"
   },
   "maximumActiveMedia": {
    "type": "integer",
    "description": "Maximum active media"
   },
   "minimumMediaRequired": {
    "type": "integer",
    "description": "Minimum media required"
   },
   "primaryMedia": {
    "type": "string",
    "description": "Primary media"
   },
   "secondaryMedia": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Secondary media"
   },
   "backupMedia": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Backup media"
   },
   "temporaryMedia": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Temporary media"
   },
   "mediaCombination": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Permitted media combinations"
   },
   "simultaneousActivation": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media that may be active at the same time, e.g. face with RFID"
   },
   "exclusiveActivation": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media whose activation revokes another, e.g. RFID activated revokes temporary paper"
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
  },
  "required": [
   "ruleId"
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
 "VirtualTicketArchitectureTestingGovernanceAuditView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket Architecture Testing, Governance & Audit displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "changeType": {
    "type": "string",
    "enum": [
     "configurationChange",
     "mediaBinding",
     "rebinding",
     "activation",
     "suspension",
     "revocation",
     "replacement",
     "resolverChange",
     "ruleChange",
     "approval"
    ],
    "description": "What kind of change was recorded"
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
   "before": {
    "type": "string",
    "description": "State before the change"
   },
   "after": {
    "type": "string",
    "description": "State after the change"
   }
  }
 },
 "VirtualTicketCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "ticketStatus": {
    "type": "string",
    "enum": [
     "created",
     "pendingFulfillment",
     "active",
     "partiallyUsed",
     "used",
     "expired",
     "suspended",
     "cancelled",
     "voided",
     "reissuedSuperseded",
     "refunded",
     "transferred",
     "blocked"
    ],
    "description": "Virtual Ticket status (lifecycle 15.1.3)"
   },
   "usageStatus": {
    "type": "string",
    "enum": [
     "unused",
     "partiallyUsed",
     "used"
    ],
    "description": "How much of the entitlement is consumed"
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
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Valid from"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "Valid to"
   }
  }
 },
 "VirtualTicketCommandCenterViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
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
    "type": "integer",
    "description": "Suspended"
   },
   "usedConsumed": {
    "type": "integer",
    "description": "Used / Consumed"
   },
   "partiallyConsumed": {
    "type": "integer",
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
    "type": "integer",
    "description": "Revoked"
   },
   "virtualTicketsWithMultipleMedia": {
    "type": "integer",
    "description": "Virtual Tickets with Multiple Media"
   },
   "virtualTicketsWithNoActiveMedia": {
    "type": "integer",
    "description": "Virtual Tickets with No Active Media"
   },
   "mediaBindingExceptions": {
    "type": "integer",
    "description": "Media Binding Exceptions"
   },
   "credentialSynchronizationIssues": {
    "type": "integer",
    "description": "Credential Synchronization Issues"
   }
  }
 },
 "VirtualTicketIdentityMasterRecordConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Virtual Ticket Identity & Master Record Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue this configuration applies to"
   },
   "idGenerationPattern": {
    "type": "string",
    "description": "Virtual Ticket ID format: prefix, suffix and length"
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
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media types a ticket of this configuration must carry"
   }
  },
  "required": [
   "venueId"
  ]
 },
 "VirtualTicketIdentityMasterRecordConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket Identity & Master Record Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue this configuration applies to"
   },
   "idGenerationPattern": {
    "type": "string",
    "description": "Virtual Ticket ID format: prefix, suffix and length"
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
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media types a ticket of this configuration must carry"
   }
  },
  "required": [
   "venueId"
  ]
 },
 "VirtualTicketStatusLifecycleModelView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket Status & Lifecycle Model displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fromStatus": {
    "type": "string",
    "enum": [
     "created",
     "pendingFulfillment",
     "active",
     "partiallyUsed",
     "used",
     "expired",
     "suspended",
     "cancelled",
     "voided",
     "reissuedSuperseded",
     "refunded",
     "transferred",
     "blocked"
    ],
    "description": "Status the transition starts from"
   },
   "toStatus": {
    "type": "string",
    "enum": [
     "created",
     "pendingFulfillment",
     "active",
     "partiallyUsed",
     "used",
     "expired",
     "suspended",
     "cancelled",
     "voided",
     "reissuedSuperseded",
     "refunded",
     "transferred",
     "blocked"
    ],
    "description": "Status the transition leads to"
   },
   "originatingSources": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "orderManagement",
      "cancellation",
      "refund",
      "upgradeConversion",
      "ticketTransfer",
      "membership",
      "expiry",
      "accessUsage",
      "authorizedOperator",
      "api",
      "scheduledProcess"
     ]
    },
    "description": "Where this transition may originate"
   },
   "allowed": {
    "type": "boolean",
    "description": "Whether the transition is allowed"
   },
   "requiresAuthorizedException": {
    "type": "boolean",
    "description": "Allowed only with an authorised exception, e.g. Used to Active"
   }
  },
  "required": [
   "fromStatus",
   "toStatus"
  ]
 }
}
```
